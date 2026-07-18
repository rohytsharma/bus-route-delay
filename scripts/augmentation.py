"""
augmentation.py — Synthetic delay & location augmentation.

BODS provides no historical archive of live location (SIRI-VM) data, so a
year-long delay signal cannot be downloaded directly. This module generates a
documented, literature-informed synthetic delay signal, grounded in a real
SIRI-VM sample's schema and value ranges (per the brief's Strategy 3:
"Synthetic data augmentation... preserving the statistical distribution of
originals").

Distribution choice: a shifted Gamma distribution, consistent with the
right-skewed shape of real bus-delay data reported by Mazloumi, Currie and
Rose (2010). Delay is structured by hour-of-day, day-of-week and route so the
downstream ML models have genuine, learnable signal rather than pure noise.
"""

import numpy as np


# Merseyside / St Helens bounding box - the real geography these routes run in
LAT_MIN, LAT_MAX = 53.30, 53.48
LON_MIN, LON_MAX = -2.98, -2.65

PEAK_HOURS = (7, 8, 9, 16, 17, 18)
PEAK_MULTIPLIER = 1.6
WEEKEND_MULTIPLIER = 0.7
GAMMA_SHAPE = 2.0
BASE_SCALE = 2.2
DELAY_SHIFT_MINUTES = -2.0  # allows small negative values (early arrivals)


def seed_route_risk_factors(route_names, seed=42):
    """Assign each route a persistent 'inherent unreliability' multiplier
    (0.6-1.8x), giving the model genuine route-level structure to learn."""
    rng = np.random.default_rng(seed)
    unique_routes = sorted(set(route_names))
    return {r: float(rng.uniform(0.6, 1.8)) for r in unique_routes}


def generate_delay_minutes(hour, route_description, day_of_week, route_risk_factors, rng=None):
    """Generate one synthetic delay value (minutes) for a trip instance."""
    if rng is None:
        rng = np.random.default_rng()
    peak = PEAK_MULTIPLIER if hour in PEAK_HOURS else 1.0
    weekend = WEEKEND_MULTIPLIER if day_of_week in ("Saturday", "Sunday") else 1.0
    route_factor = route_risk_factors.get(route_description, 1.0)
    scale = BASE_SCALE * peak * weekend * route_factor
    delay = rng.gamma(GAMMA_SHAPE, scale) + DELAY_SHIFT_MINUTES
    return round(float(delay), 2)


def generate_synthetic_coordinates(rng=None):
    """Generate a synthetic (latitude, longitude) pair within the real
    Merseyside bounding box."""
    if rng is None:
        rng = np.random.default_rng()
    lat = float(rng.uniform(LAT_MIN, LAT_MAX))
    lon = float(rng.uniform(LON_MIN, LON_MAX))
    return lat, lon


if __name__ == "__main__":
    # Small demonstration
    rng = np.random.default_rng(42)
    routes = ["Liverpool - St Helens", "Southport - Ormskirk", "Kirkby - Prescot"]
    factors = seed_route_risk_factors(routes)
    for r in routes:
        d = generate_delay_minutes(hour=8, route_description=r, day_of_week="Monday",
                                    route_risk_factors=factors, rng=rng)
        lat, lon = generate_synthetic_coordinates(rng)
        print(f"{r:25s} delay={d:6.2f} min   lat={lat:.4f}  lon={lon:.4f}")
