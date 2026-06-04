from ductcalc.fittings import fitting_pressure_drop

def test_fitting_pressure_drop():
    dp = fitting_pressure_drop(
        velocity_pressure_inwg=0.10,
        loss_coefficient = 0.25
    )

    assert dp == 0.025