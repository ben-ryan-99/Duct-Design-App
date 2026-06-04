from ductcalc.models import DuctSegment, Fitting, Path
from ductcalc.system import calculate_critical_path


branch_a = Path(
    name="Branch A",
    items=[
        DuctSegment(length_ft=100, diameter_in=12, airflow_cfm=1000),
        Fitting(
            name="Round elbow",
            loss_coefficient=0.25,
            diameter_in=12,
            airflow_cfm=1000,
        ),
    ],
)

branch_b = Path(
    name="Branch B",
    items=[
        DuctSegment(length_ft=150, diameter_in=10, airflow_cfm=800),
        Fitting(
            name="Round elbow",
            loss_coefficient=0.35,
            diameter_in=10,
            airflow_cfm=800,
        ),
    ],
)

result = calculate_critical_path([branch_a, branch_b])

for path in result["paths"]:
    print(path["path_name"])
    print(f"Total Pressure Drop: {path['total_pressure_drop_inwg']:.3f} in. w.g.")
    print()

print(f"Critical Path: {result['critical_path_name']}")
print(
    f"Critical Path Pressure Drop: "
    f"{result['critical_path_pressure_drop_inwg']:.3f} in. w.g."
)