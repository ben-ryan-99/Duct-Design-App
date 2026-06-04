FITTINGS = {
    "round_90_elbow": {
        "name": "90 Degree Round Elbow",
        "loss_coefficient": 0.25,
    },
    "round_45_elbow": {
        "name": "45 Degree Round Elbow",
        "loss_coefficient": 0.14,
    },
    "straight_through_tee": {
        "name": "Straight Through Tee",
        "loss_coefficient": 0.20,
    },
    "supply_diffuser": {
        "name": "Supply Diffuser",
        "loss_coefficient": 0.50,
    },
}

def get_fitting(fitting_type):
    return FITTINGS[fitting_type]


def get_loss_coefficient(fitting_type):
    return FITTINGS[fitting_type]["loss_coefficient"]