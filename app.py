import streamlit as st

from ductcalc.models import DuctSegment, Fitting, Path
from ductcalc.system import calculate_path_pressure_drop
from ductcalc.fitting_db import FITTINGS

if "path_items" not in st.session_state:
    st.session_state["path_items"] = []

st.title("Duct Pressure Drop Calculator")

st.subheader("Straight Duct")

length_ft = st.number_input("Length (ft)", min_value=0.0, value=100.0)
diameter_in = st.number_input("Diameter (in)", min_value=1.0, value=12.0)
airflow_cfm = st.number_input("Airflow (CFM)", min_value=0.0, value=1000.0)

st.subheader("Fitting")


selected_fitting_id = st.selectbox(
    "Fitting Type",
    options=list(FITTINGS.keys()),
    format_func=lambda x: FITTINGS[x]["name"]
)


if st.button("Add Duct"):
    st.session_state["path_items"].append(
        {
            "type": "duct",
            "length_ft": length_ft,
            "diameter_in": diameter_in,
            "airflow_cfm": airflow_cfm,
        }
    )

if st.button("Add Fitting"):
    st.session_state["path_items"].append(
        {
            "type": "fitting",
            "fitting_type": selected_fitting_id,
            "diameter_in": diameter_in,
            "airflow_cfm": airflow_cfm,
        }
    )

if st.button("Clear Path"):
    st.session_state["path_items"] = []
    st.rerun()




# Display the item list
st.subheader("Current Path")

for i, item in enumerate(st.session_state["path_items"]):

    if item["type"] == "duct":
        st.write(
            f"{i+1}. Duct - "
            f"{item['length_ft']} ft, "
            f"{item['diameter_in']} in"
        )

    elif item["type"] == "fitting":
        st.write(
            f"{i+1}. Fitting - "
            f"{item['fitting_type']}"
        )





######  Calculation
if st.button("Calculate"):
    duct = DuctSegment(
        length_ft=length_ft,
        diameter_in=diameter_in,
        airflow_cfm=airflow_cfm,
    )

    fitting = Fitting(
        fitting_type=selected_fitting_id,
        diameter_in=diameter_in,
        airflow_cfm=airflow_cfm,
    )

    path = Path(
        name="Path 1",
        items=[duct, fitting],
    )

    result = calculate_path_pressure_drop(path)

    st.subheader("Results")

    st.write(f"Velocity: {duct.velocity_fpm:.0f} fpm")
    st.write(f"Velocity Pressure: {duct.velocity_pressure_inwg:.3f} in. w.g.")
    st.write(f"Total Pressure Drop: {result['total_pressure_drop_inwg']:.3f} in. w.g.")

    st.table(
        [
            {
                "Item": type(row["item"]).__name__,
                "Pressure Drop (in. w.g.)": round(row["pressure_drop_inwg"], 3),
            }
            for row in result["items"]
        ]
    )