from ductcalc.models import DuctSegment, Fitting
from ductcalc.system import calculate_system_pressure_drop


def test_system_pressure_drop():
    items = [
        DuctSegment(
            length_ft=100,
            diameter_in=12,
            airflow_cfm=1000,
        ),
        Fitting(
            fitting_type = "round_90_elbow",
            airflow_cfm = 1000,
            diameter_in = 12
        ),
    ]

    result = calculate_system_pressure_drop(items)

    assert result["total_pressure_drop_inwg"] > 0
    assert len(result["items"]) == 2