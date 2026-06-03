from ductcalc.models import DuctSegment


def test_velocity():
    duct = DuctSegment(
        length_ft=100,
        diameter_in=12,
        airflow_cfm=1000
    )

    assert duct.velocity_fpm > 1000