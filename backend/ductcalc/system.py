from ductcalc.models import DuctSegment, Fitting
from ductcalc.friction import straight_duct_pressure_drop
from ductcalc.fittings import fitting_pressure_drop

def calculate_item_pressure_drop(item):
    if isinstance(item, DuctSegment):
        return straight_duct_pressure_drop(item)
    
    if isinstance(item, Fitting):
        return fitting_pressure_drop(
            velocity_pressure_inwg=item.velocity_pressure_inwg,
            loss_coefficient=item.loss_coefficient,
        )
    
    raise TypeError(f"Unsupported system item: {type(item)}")

def calculate_system_pressure_drop(items):
    total_pressure_drop = 0

    results = []

    for item in items:
        item_pressure_drop = calculate_item_pressure_drop(item)
        total_pressure_drop += item_pressure_drop

        results.append(
            {
                "item": item,
                "pressure_drop_inwg": item_pressure_drop,
            }
        )

    return {
        "items": results,
        "total_pressure_drop_inwg": total_pressure_drop,
    }