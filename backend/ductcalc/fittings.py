
# Calculate pressure drop associated with fittings
def fitting_pressure_drop(velocity_pressure_inwg, loss_coefficient):
    return loss_coefficient * velocity_pressure_inwg