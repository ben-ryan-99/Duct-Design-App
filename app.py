import streamlit as st
import json

from ductcalc.models import DuctSegment, Fitting, Path
from ductcalc.system import calculate_path_pressure_drop
from ductcalc.fitting_db import FITTINGS, get_fitting

if "path_items" not in st.session_state:
    st.session_state["path_items"] = []

###### Import or export path from JSON text
with st.expander("Import / Export JSON", expanded=False):
    st.subheader("Import JSON")

    json_input = st.text_area(
        "Paste path JSON here",
        height=150,
        placeholder='[{"type": "duct", "length_ft": 100, "diameter_in": 12, "airflow_cfm": 1000}]',
    )

    if st.button("Import JSON"):
        try:
            imported_items = json.loads(json_input)

            if not isinstance(imported_items, list):
                st.error("JSON must be a list of path items.")
            else:
                st.session_state["path_items"] = imported_items
                st.success("Path imported successfully.")
                st.rerun()

        except json.JSONDecodeError as error:
            st.error(f"Invalid JSON: {error}")

    st.subheader("Export JSON")

    path_json = json.dumps(
        st.session_state["path_items"],
        indent=2,
    )

    st.code(path_json, language="json")

    st.download_button(
        label="Download Path JSON",
        data=path_json,
        file_name="duct_path.json",
        mime="application/json",
    )
#########

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
    duct_count = 0
    fitting_count = 0
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



##### Export JSON
# st.subheader("Export JSON")

# path_json = json.dumps(
#     st.session_state["path_items"],
#     indent=2,
# )

# st.code(path_json, language="json")

# st.download_button(
#     label="Download Path JSON",
#     data=path_json,
#     file_name="duct_path.json",
#     mime="application/json",
# )
#####


######  Calculation
if st.button("Calculate"):
    path_items = []

    for item in st.session_state["path_items"]:
        if item["type"] == "duct":
            path_items.append(
                DuctSegment(
                    length_ft=item["length_ft"],
                    diameter_in=item["diameter_in"],
                    airflow_cfm=item["airflow_cfm"],
                )
            )

        elif item["type"] == "fitting":
            path_items.append(
                Fitting(
                    fitting_type=item["fitting_type"],
                    diameter_in=item["diameter_in"],
                    airflow_cfm=item["airflow_cfm"],
                )
            )

    path = Path(
        name="Path 1",
        items=path_items,
    )

    result = calculate_path_pressure_drop(path)

    rows = []

    for index, row in enumerate(result["items"], start=1):
        item = row["item"]

        if isinstance(item, DuctSegment):
            item_name = f"Straight Duct {index}"
            item_type = "Duct"
            length_ft_display = item.length_ft

        elif isinstance(item, Fitting):
            fitting_data = get_fitting(item.fitting_type)
            item_name = f"{fitting_data['name']} {index}"
            item_type = "Fitting"
            length_ft_display = "-"

        rows.append(
            {
                "#": index,
                "Item": item_name,
                "Type": item_type,
                "Length (ft)": length_ft_display,
                "Diameter (in)": item.diameter_in,
                "Airflow (CFM)": item.airflow_cfm,
                "Velocity (fpm)": round(item.velocity_fpm, 0),
                "VP (in. w.g.)": round(item.velocity_pressure_inwg, 3),
                "Pressure Drop (in. w.g.)": round(row["pressure_drop_inwg"], 3),
            }
        )

    st.subheader("Calculation Table")

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
    )

    st.metric(
        "Total Pressure Drop",
        f"{result['total_pressure_drop_inwg']:.3f} in. w.g.",
    )
