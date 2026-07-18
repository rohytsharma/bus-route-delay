
Bus Open Data Service AVL to Timetables data matching
 GOV.UK

________________________________________

AVL to Timetable data matching
The AVL to Timetable matching zip contains a series of CSVs which give machine-readable results of the sampled AVL and Timetable data that currently reside in BODS.

Note that the matching report only covers the data from primary data sources on BODS which is timetables data in TransXChange format, bus location data in SIRI-VM format.
Fares data in NeTEX are not included in the AVL to Timetable matching report.

The AVL to Timetables feed matching is a weekly score of a published data feed. Daily random samples of data packets are collected for each published feed to be matched and then collated together to create a weekly report along with a weekly associated summary score for that report. This is usually done on every Monday of the week. This is the latest matching score for this feed.

Please note that BODS doesn't check every single packet of data but we do a random sampling throughout the day in order to determine these reports and scores.

Please work with your technology suppliers to provide the most accurate data so that download data consumers and eventually your bus passengers can benefit.


The zipped CSVs matching report
The AVL to Timetable matching zip contains 7 distinct CSVs:
-   avl_to_timetable_match_summary.csv: this contains a high-level overview result of how
        well the sampled AVL vehicle activities data from collected feeds on BODS matched accurately
        to all of the Timetables data on BODS. This also shows break down scores per key matching
        fields.
-   blockref.csv: this contains a detailed granular view of the missing or mismatched BlockRef value
        within the analysed journeys in SIRI VM and the Block number field in the timetables data
-   destinationref.csv: this contains a detailed granular view of the missing or mismatched
        Destinationref value within the analysed journeys in SIRI VM and the JourneyPatternTimingLink/To/
        StopPointRef field in TransXChange format of the timetables data.
-   directionref.csv: this contains a detailed granular view of the missing or mismatched Direction
        ref value within the analysed journeys in SIRI VM and the Direction from JourneyPattern field in
        TransXChange format of the timetables data
-   originref.csv: this contains a detailed granular view of the missing or mismatched OriginRef value
        within the analysed journeys in SIRI VM and the JourneyPatternTimingLink/from/StopPointRef field
	in TransXChange format of the timetables data
-   all_siri_vm_analysed.csv: this contains helpful counts of all of the AVL messages collected
        and analysed.
-   uncountedvehicleactivities.csv: this contains a detailed granular view of vehicle activities that
        were collected and counted. But unable to analyse due to gross errors in both vehicle location
        and timetables data published within BODS.

Field definitions:
The AVL to Timetables contains certain table field headers, the definitions and explanations of which
can be found below.


avl_to_timetable_match_summary.csv
Field name                                   Definition

SIRI field                                   List of SIRI VM fields where there is an equivalent matching field in the TxC-PTI data and TXC-PTI fields MUST be an absolute match of text and formatting.
TXC match field                              List of TxC fields where there is an equivalent matching field in the SIRI VM data and SIRI VM fields MUST be an absolute match of text and formatting.
Total vehicleActivities analysed             The total number of vehicle activities collected from a feed and analysed per report
Total count of SIRI fields populated         The total number of SIRI VM fields populated from the collected vehicle activities
%populated                                   Percentage figure of SIRI VM fields populated from the collected vehicle activities
Successful match with TXC                    The total number of SIRI VM fields successfully matched with equivalent matching timetables fields
%match                                       Percentage figure of SIRI VM fields successfully matched with equivalent matching timetables fields
Notes                                        This provides additional details or notes to assist publishers and suppliers to provide most accurate data

blockref.csv
Field name                                   Definition

SD ResponseTimestamp                         Time individual response element was created
RecordedAtTime                               Time at which VEHICLE data was recorded.
AVL data set name BODS                       The internal BODS generated data set name given for an AVL data feed.
AVL data set ID BODS                         The internal BODS generated ID of the operator/publisher providing data on BODS.
DatedVehicleJourneyRef in SIRI               Unique identifier describing vehicle journey that a vehicle is running. This must be the same in the TicketMachine/JourneyCode as the corresponding object in the timetables data
VehicleRef in SIRI                           A reference to the specific VEHICLE making a journey.
Timetable file name                          The internal BODS generated data set name given for TxC data set.
Timetable data set ID BODS                   The internal BODS generated ID of the operator/publisher providing data on BODS
DepartureTime in TXC                         The departure time from the first stop in the journey pattern
BlockRef in SIRI                             Block that vehicle is running in SIRI VM. If this has also been provided in the timetables data, the input should be the same ID as the corresponding object in the timetables data.
BlockNumber in TXC                           Block number that vehicle is running in TxC
SIRI XML line number                         The exact line number of the file provided to BODS. This is usually generated by the publisher or their supplier for SIRI VM
TransXChange XML line number                 The exact line number of the file provided to BODS. This is usually generated by the publisher or their supplier
Error note                                   This provides additional notes in plain English assisting publishers and suppliers address the errors identified in the report and provide most accurate data

destinationref.csv
Field name                                   Definition

SD ResponseTimestamp                         Time individual response element was created
RecordedAtTime                               Time at which VEHICLE data was recorded.
AVL data set name BODS                       The internal BODS generated data set name given for an AVL data feed.
AVL data set ID BODS                         The internal BODS generated ID of the operator/publisher providing data on BODS.
DatedVehicleJourneyRef in SIRI               Unique identifier describing vehicle journey that a vehicle is running. This must be the same in the TicketMachine/JourneyCode as the corresponding object in the timetables data
VehicleRef in SIRI                           A reference to the specific VEHICLE making a journey.
Timetable file name                          The internal BODS generated data set name given for TxC data set.
Timetable data set ID BODS                   The internal BODS generated ID of the operator/publisher providing data on BODS
DepartureTime in TXC                         The departure time from the first stop in the journey pattern
DestinationRef in SIRI                       The identifier of the destination of the journey; used to help identify the vehicle to the public. This shall be a valid ATCOCode from the NaPTAN database, and same as the ID to the corresponding object in the timetables data.
StopPointRef in TxC                          Origin ID of the journey as defined in the JourneyPatternTimingLink/from/StopPointRef. This must be the same ID as the corresponding object in the location data.
SIRI XML line number                         The exact line number of the file provided to BODS. This is usually generated by the publisher or their supplier for SIRI VM
TransXChange XML line number                 The exact line number of the file provided to BODS. This is usually generated by the publisher or their supplier
Error note                                   This provides additional notes in plain English assisting publishers and suppliers address the errors identified in the report and provide most accurate data

directionref.csv
Field name                                   Definition

SD ResponseTimestamp                         Time individual response element was created
RecordedAtTime                               Time at which VEHICLE data was recorded.
AVL data set name BODS                       The internal BODS generated data set name given for an AVL data feed.
AVL data set ID BODS                         The internal BODS generated ID of the operator/publisher providing data on BODS.
DatedVehicleJourneyRef in SIRI               Unique identifier describing vehicle journey that a vehicle is running. This must be the same in the TicketMachine/JourneyCode as the corresponding object in the timetables data
VehicleRef in SIRI                           A reference to the specific VEHICLE making a journey.
Timetable file name                          The internal BODS generated data set name given for TxC data set.
Timetable data set ID BODS                   The internal BODS generated ID of the operator/publisher providing data on BODS
DepartureTime in TXC                         The departure time from the first stop in the journey pattern
DirectionRef in SIRI                         Direction of the journey (for example INBOUND/OUTBOUND). This must be the same direction as the corresponding object in the timetables data.
Direction from JourneyPattern in TXC         Direction of the journey as defined in the Journey Pattern. This must be the same direction as the corresponding object in the location data.
SIRI XML line number                         The exact line number of the file provided to BODS. This is usually generated by the publisher or their supplier for SIRI VM
TransXChange XML line number                 The exact line number of the file provided to BODS. This is usually generated by the publisher or their supplier
Error note                                   This provides additional notes in plain English assisting publishers and suppliers address the errors identified in the report and provide most accurate data

originref.csv
Field name                                   Definition

SD ResponseTimestamp                         Time individual response element was created
RecordedAtTime                               Time at which VEHICLE data was recorded.
AVL data set name BODS                       The internal BODS generated data set name given for an AVL data feed.
AVL data set ID BODS                         The internal BODS generated ID of the operator/publisher providing data on BODS.
DatedVehicleJourneyRef in SIRI               Unique identifier describing vehicle journey that a vehicle is running. This must be the same in the TicketMachine/JourneyCode as the corresponding object in the timetables data
VehicleRef in SIRI                           A reference to the specific VEHICLE making a journey.
Timetable file name                          The internal BODS generated data set name given for TxC data set.
Timetable data set ID BODS                   The internal BODS generated ID of the operator/publisher providing data on BODS
DepartureTime in TXC                         The departure time from the first stop in the journey pattern
OriginRef in SIRI                            The identifier of the origin of the journey; used to help identify the VEHICLE JOURNEY on arrival boards. This shall be a valid ATCOCode from the NaPTAN database, and same as the ID to the corresponding object in the timetables data.
StopPointRef in TxC                          Origin ID of the journey as defined in the JourneyPatternTimingLink/from/StopPointRef. This must be the same ID as the corresponding object in the location data.
SIRI XML line number                         The exact line number of the file provided to BODS. This is usually generated by the publisher or their supplier for SIRI VM
TransXChange XML line number                 The exact line number of the file provided to BODS. This is usually generated by the publisher or their supplier
Error note                                   This provides additional notes in plain English assisting publishers and suppliers address the errors identified in the report and provide most accurate data

all_siri_vm_analysed.csv
Field name                                   Definition

Version                                      Siri VM standard field
ResponseTimestamp (ServiceDelivery)          Siri VM standard field
ProducerRef                                  Siri VM standard field
ResponseTimestamp (VehicleMonitoringDelivery)Siri VM standard field
RequestMessageRef                            Siri VM standard field
ValidUntil                                   Siri VM standard field
ShortestPossibleCycle                        Siri VM standard field
RecordedAtTime                               Siri VM standard field
ItemIdentifier                               Siri VM standard field
ValidUntilTime                               Siri VM standard field
LineRef                                      Siri VM standard field
DirectionRef                                 Siri VM standard field
DataFrameRef                                 Siri VM standard field
DatedVehicleJourneyRef                       Siri VM standard field
PublishedLineName                            Siri VM standard field
OperatorRef                                  Siri VM standard field
OriginRef                                    Siri VM standard field
OriginName                                   Siri VM standard field
DestinationRef                               Siri VM standard field
DestinationName                              Siri VM standard field
OriginAimedDepartureTime                     Siri VM standard field
Longitude                                    Siri VM standard field
Latitude                                     Siri VM standard field
Bearing                                      Siri VM standard field
VehicleRef                                   Siri VM standard field
BlockRef                                     Siri VM standard field
DriverRef                                    Siri VM standard field

uncountedvehicleactivities.csv
Field name                                   Definition

SD ResponseTimestamp                         Time individual response element was created
AVL data set name BODS                       The name of the AVL dataset in BODS that contains the record which could not be analysed
AVL data set ID BODS                         The ID of the AVL dataset in BODS that contains the record which could not be analysed
OperatorRef                                  This shall be the operator's National Operator Code (NOC) from the Traveline NOC database and same as the ID to the corresponding object in the timetables data.
LineRef                                      Name or number by which the LINE is known to the public. This shall be the same as the corresponding object in the timetables data provided to BODS.
RecordedAtTime                               Time at which VEHICLE data was recorded.
DatedVehicleJourneyRef in SIRI               Unique identifier describing vehicle journey that a vehicle is running. This shall be the same as the corresponding object in the timetables data and should be a globally unique identifier.
Error note: Reason it could not be analysed against TXCA description of the data that could not be successfully matched. These align with the steps below and the reasons why a record cannot be successfully analysed. Reason it could not be analysed to TXC

Process
To be able to compare data for any given journey it is necessary to first identify a single journey in both the SIRI and TxC datasets. The SIRI delivery is the starting point for the process.

Step 1
Using OperatorRef and LineRef from the SIRI data locate the TxC files that contain data for the operator and line. There may be multiple files.
Check which of the files contain data valid for the date of the SIRI data. This will require checking the OperatingPeriod to find data which is valid for the date being tested.
a.	If file(s) found, continue to step 2.
b.	If no file found then mark the vehicle journey as failed to be analysed.

Step 2
From the Step 1 subset of TxC files search each file for any that contain a JourneyCode that matches with the DatedVehicleJourneyRef from the SIRI journey.
a.	If file(s) found with matching JourneyCodes, continue to step 3.
b.	If no file found then mark the vehicle journey as failed to be analysed.

Step 3
From the Step 2 subset of TxC files search each file for an OperatingProfile that is appropriate for the date of the SIRI data - type of day for date being tested. For example 1 April 2022 was a Friday.
a.	If file(s) found with a matching OperatingProfile, continue to step 4.
b.	If no matching OperatingProfile is found, then mark the vehicle journey as failed to be analysed.

Step 4
From the Step 3 subset of TxC files use the file with the highest RevisionNumber that is valid for the date of the SIRI data to find the correct file.
a.	If only one file is identified after filtering by RevisionNumber, move to step 5.
b.	If there is more than one file remaining after reading the RevisionNumber, mark they vehicle journey as failed to be analysed.

Step 5
You will have only one file when you reach this Step.
Search within the file for JourneyCode to find the JourneyCode with an OperatingProfile that is valid for the date being tested. There may be more than one matching JourneyCode within a TxC if it is used for example for journeys operating on weekdays and weekends.
a.	If a single JourneyCode is identified that is valid on the correct day, move to step 6.
b.	If there is more than one valid JourneyCode found, mark the vehicle journey as failed to be analysed.

Step 6
Once a single JourneyCode with an appropriate OperatingPeriod and OperatingProfile is identified testing can progress to the remaining pairs of values described earlier in this document.
If DatedVehicleJourneyRef from the selected SIRI delivery is unable to be matched to a single JourneyCode in a TxC file then the analysis should fail for all data types.

Step 7
It will be necessary to identify the correct direction, destination and origin information for the full journey details being tested.
Start with identifying the JourneyPattern for the journeys Direction. Knowing the JourneyPattern allows identification all JourneyPatternSection used in the JourneyPattern. Knowing the JourneyPatternSection allows the first and last sections to be identified. These are required to locate the origin and destination information.
The OriginRef is the StopPointRef in the From element of the first JourneyPatternSection of the JourneyPattern.
The DestinationRef is the StopPointRef in the To element of the last JourneyPatternSection of the JourneyPattern.
