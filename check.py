from ductcalc.models import Fitting

elbow = Fitting(
    name = "bill",
    fitting_type="round_90_elbow",
    diameter_in=12,
    airflow_cfm=1000
)

print(elbow.loss_coefficient)