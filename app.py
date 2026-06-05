###################################################################################################################
# Imports
###################################################################################################################
# Import standard python modules/packages
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json

# Imports from this project 
from ductcalc.models import DuctSegment, Fitting, Path
from ductcalc.system import calculate_path_pressure_drop
from ductcalc.fitting_db import FITTINGS, get_fitting
from ductcalc.canvas import (
    build_canvas_duct_segments,
    find_connections,
    group_connected_paths,
    parse_canvas_segments,
)

###################################################################################################################
# Code
###################################################################################################################

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


##### Title
st.title("Duct Pressure Drop Calculator")
#####


##### Inputs
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


col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Add Duct"):
        st.session_state["path_items"].append(
            {
                "type": "duct",
                "length_ft": length_ft,
                "diameter_in": diameter_in,
                "airflow_cfm": airflow_cfm,
            }
        )

with col2:
    if st.button("Add Fitting"):
        st.session_state["path_items"].append(
            {
                "type": "fitting",
                "fitting_type": selected_fitting_id,
                "diameter_in": diameter_in,
                "airflow_cfm": airflow_cfm,
            }
        )

with col3:
    if st.button ("Clear Path"):
        st.session_state["path_items"] = []
        st.rerun()

with col4:
    calculate  = st.button("Calculate")
#####


##### Display the item list
st.subheader("Current Path")

for i, item in enumerate(st.session_state["path_items"]):

    col1, col2 = st.columns([5,1])

    with col1:
        if item["type"] == "duct":
            st.write(
                f"{i+1}. Duct | "
                f"{item['length_ft']} ft | "
                f"{item['diameter_in']} in | "
                f"{item['airflow_cfm']} CFM"
            )

        elif item["type"] == "fitting":
            fitting_data = get_fitting(item["fitting_type"])
            st.write(
                f"{i+1}. {fitting_data['name']} | "
                f"{item['diameter_in']} in | "
                f"{item['airflow_cfm']} CFM"
            )

    with col2:
        if st.button("Delete", key=f"delete_{i}"):
            st.session_state["path_items"].pop(i)
            st.rerun()
#####

##### Canvas Drawing
st.subheader("Duct Layout Canvas")

canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=4,
    stroke_color="#000000",
    background_color="#ffffff",
    height=400,
    width=700,
    drawing_mode="line",
    key="duct_canvas",
)

canvas_segments = []
segments = []
connections = []

if canvas_result.json_data is not None:

    
    objects = canvas_result.json_data.get("objects",[])

    pixels_per_foot=st.number_input(
        "Drawing Scale (pixels per foot)",
        min_value=1.0,
        value=10.0,
    )

    canvas_diameter_in=st.number_input(
        "Canvas Duct Diameter (in)",
        min_value=1.0,
        value=12.0,
    )

    canvas_airflow_cfm=st.number_input(
        "Canvas Airflow (CFM)",
        min_value=0.0,
        value=1000.0,
    )

    segments=parse_canvas_segments(
        objects=objects,
        pixels_per_foot=pixels_per_foot,
    )

    canvas_segments=build_canvas_duct_segments(
        canvas_segments=segments,
        diameter_in=canvas_diameter_in,
        airflow_cfm=canvas_airflow_cfm,
    )

    connections=find_connections(segments)
    paths=group_connected_paths(connections)

    path=Path(
        name="Canvas Path",
        items=canvas_segments
    )

    result = calculate_path_pressure_drop(path)

    st.metric(
        "Canvas Pressure Drop",
        f"{result['total_pressure_drop_inwg']:.3f} in. w.g.",
    )


    


# st.subheader("canvas debug")
# st.write("segments")
# for segment in segments:
#     st.write(
#         f"Segment {segment.id}: "
#         f"({segment.x1:.1f}, {segment.y1:.1f})"
#         f"to "
#         f"({segment.x2:.1f}, {segment.y2:.1f})"
#     )

# st.write("connections")
# for seg1,seg2 in connections:
#     st.write(f"Segment {seg1} connects to Segment {seg2}")

# st.write("grouped paths")
# for i, path in enumerate(paths, start=1):
#     st.write(f"Path {i}: Segments {path}")


######  Calculation
if calculate:
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
