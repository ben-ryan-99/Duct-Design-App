import math

# Standard air properties at ~70°F and sea level
AIR_DENSITY = 1.204  # kg/m³
AIR_VISCOSITY = 1.81e-5  # Pa·s

# Galvanized steel roughness
ROUGHNESS_M = 0.00015


def reynolds_number(velocity_mps, diameter_m):
    return (AIR_DENSITY * velocity_mps * diameter_m) / AIR_VISCOSITY


def friction_factor(reynolds, diameter_m):
    """
    Swamee-Jain approximation for turbulent flow.
    """
    return 0.25 / (
        math.log10(
            (ROUGHNESS_M / (3.7 * diameter_m))
            + (5.74 / (reynolds ** 0.9))
        )
    ) ** 2


def straight_duct_pressure_drop(segment):
    """
    Returns pressure drop in inches w.g.
    """

    # Unit conversions
    diameter_m = segment.diameter_in * 0.0254
    length_m = segment.length_ft * 0.3048

    airflow_m3s = segment.airflow_cfm * 0.000471947

    area_m2 = math.pi * diameter_m**2 / 4

    velocity_mps = airflow_m3s / area_m2

    reynolds = reynolds_number(
        velocity_mps,
        diameter_m
    )

    f = friction_factor(
        reynolds,
        diameter_m
    )

    delta_p_pa = (
        f
        * (length_m / diameter_m)
        * (AIR_DENSITY * velocity_mps**2 / 2)
    )

    # Pascals → inches water gauge
    delta_p_inwg = delta_p_pa / 249.0889

    return delta_p_inwg