# backend/tests/test_friction.py

from ductcalc.models import DuctSegment
from ductcalc.friction import straight_duct_pressure_drop


def test_pressure_drop():
    duct = DuctSegment(
        length_ft=100,
        diameter_in=12,
        airflow_cfm=1000
    )

    dp = pressure_drop(duct)

    print(f"Velocity: {duct.velocity_fpm:.0f} fpm")
    print(f"VP: {duct.velocity_pressure_inwg:.3f} in.w.g.")
    print(f"Pressure Drop: {pressure_drop(duct):.3f} in.w.g.")

    assert dp > 0