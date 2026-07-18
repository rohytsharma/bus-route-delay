"""
preprocessing.py — TransXChange XML ingestion and cleaning.

Standalone module version of the ingestion/cleaning logic used in
bus_delay_risk_scoring.ipynb. Import these functions directly, or run this
file as a script to parse the timetable data on its own.
"""

import glob
import os
import xml.etree.ElementTree as ET

NS = {'txc': 'http://www.transxchange.org.uk/'}
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def parse_duration(s):
    """Parse an ISO-8601 duration (e.g. 'PT3M0S') into minutes (float)."""
    if not s or not s.startswith('PT'):
        return 0.0
    s = s[2:]
    mins, num = 0.0, ''
    for ch in s:
        if ch.isdigit():
            num += ch
        else:
            if ch == 'H':
                mins += float(num) * 60
            elif ch == 'M':
                mins += float(num)
            elif ch == 'S':
                mins += float(num) / 60
            num = ''
    return mins


def parse_transxchange_file(path):
    """Parse one TransXChange XML file into a list of trip-level dict rows.

    Returns (rows, error) where error is None on success or 'parse_error' on failure.
    """
    rows = []
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return rows, 'parse_error'
    root = tree.getroot()

    routes = {}
    for r in root.findall('.//txc:Routes/txc:Route', NS):
        rid = r.attrib.get('id')
        desc = r.find('txc:Description', NS)
        routes[rid] = desc.text.strip() if desc is not None and desc.text else 'Unknown'

    journey_patterns = {}
    for svc in root.findall('.//txc:Services/txc:Service', NS):
        sc_el = svc.find('txc:ServiceCode', NS)
        service_code = sc_el.text if sc_el is not None else None
        line_el = svc.find('.//txc:Lines/txc:Line/txc:LineName', NS)
        line_name = line_el.text if line_el is not None else None
        std = svc.find('txc:StandardService', NS)
        if std is not None:
            for jp in std.findall('txc:JourneyPattern', NS):
                jp_id = jp.attrib.get('id')
                d_el = jp.find('txc:Direction', NS)
                rr_el = jp.find('txc:RouteRef', NS)
                journey_patterns[jp_id] = {
                    'direction': d_el.text if d_el is not None else None,
                    'route_ref': rr_el.text if rr_el is not None else None,
                    'service_code': service_code,
                    'line_name': line_name,
                }

    fname = os.path.basename(path)
    for vj in root.findall('.//txc:VehicleJourneys/txc:VehicleJourney', NS):
        vjc_el = vj.find('txc:VehicleJourneyCode', NS)
        dep_el = vj.find('txc:DepartureTime', NS)
        jpr_el = vj.find('txc:JourneyPatternRef', NS)
        lineref_el = vj.find('txc:LineRef', NS)
        jp_id = jpr_el.text if jpr_el is not None else None
        jp_info = journey_patterns.get(jp_id, {})
        route_desc = routes.get(jp_info.get('route_ref'), 'Unknown')

        op = vj.find('txc:OperatingProfile', NS)
        days = []
        if op is not None:
            dow = op.find('.//txc:RegularDayType/txc:DaysOfWeek', NS)
            if dow is not None:
                for child in dow:
                    tag = child.tag.split('}')[-1]
                    if tag in WEEKDAYS:
                        days.append(tag)
                    elif tag == 'MondayToFriday':
                        days.extend(WEEKDAYS[:5])
                    elif tag == 'MondayToSaturday':
                        days.extend(WEEKDAYS[:6])
                    elif tag in ('MondayToSunday', 'Everyday'):
                        days.extend(WEEKDAYS)
                    elif tag == 'Weekend':
                        days.extend(['Saturday', 'Sunday'])

        total_runtime = 0.0
        for vjtl in vj.findall('txc:VehicleJourneyTimingLink', NS):
            rt_el = vjtl.find('txc:RunTime', NS)
            if rt_el is not None and rt_el.text:
                total_runtime += parse_duration(rt_el.text)

        rows.append({
            'source_file': fname,
            'service_code': jp_info.get('service_code'),
            'line_name': jp_info.get('line_name'),
            'vehicle_journey_code': vjc_el.text if vjc_el is not None else None,
            'line_ref': lineref_el.text if lineref_el is not None else None,
            'route_description': route_desc,
            'direction': jp_info.get('direction'),
            'scheduled_departure_time': dep_el.text if dep_el is not None else None,
            'operating_days': ','.join(sorted(set(days), key=WEEKDAYS.index)) if days else None,
            'scheduled_duration_minutes': round(total_runtime, 2),
        })
    return rows, None


def parse_all_files(timetable_dir):
    """Parse every .xml file in a directory. Returns (all_rows, errors)."""
    xml_files = sorted(glob.glob(os.path.join(timetable_dir, "*.xml")))
    all_rows, errors = [], []
    for f in xml_files:
        rows, err = parse_transxchange_file(f)
        if err:
            errors.append((f, err))
        all_rows.extend(rows)
    return all_rows, errors


if __name__ == "__main__":
    import sys
    from config.spark_config import TIMETABLE_DIR

    directory = sys.argv[1] if len(sys.argv) > 1 else TIMETABLE_DIR
    rows, errs = parse_all_files(directory)
    print(f"Parsed {len(rows)} trip rows from {directory} ({len(errs)} errors)")
