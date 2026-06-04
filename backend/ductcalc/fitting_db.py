FITTINGS = {
    "round_90_elbow": {
        "id": "round_90_elbow",
        "name": "90 Degree Round Elbow",
        "loss_coefficient": 0.25,
    },
    "round_45_elbow": {
        "id": "round_45_elbow",
        "name": "45 Degree Round Elbow",
        "loss_coefficient": 0.14,
    },
    "straight_through_tee": {
        "id": "straight_through_tee",
        "name": "Straight Through Tee",
        "loss_coefficient": 0.20,
    },
    "supply_diffuser": {
        "id": "supply_diffuser",
        "name": "Supply Diffuser",
        "loss_coefficient": 0.50,
    },
}

def get_fitting(fitting_input):
    fitting_input = fitting_input.lower()

    # Match identifier
    if fitting_input in FITTINGS:
        return FITTINGS[fitting_input]

    # Match display name
    for fitting_data in FITTINGS.values():
        if fitting_data["name"].lower() == fitting_input:
            return fitting_data

    raise KeyError(f"Fitting not found: {fitting_input}")


def get_loss_coefficient(fitting_type):
    fitting = get_fitting(fitting_type)
    return fitting["loss_coefficient"]