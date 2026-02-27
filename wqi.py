
def calculate_wqi(row):
    weights = {
        "ph": 0.2,
        "TDS": 0.2,
        "Turbidity": 0.2,
        "Hardness": 0.2,
        "Sulfate": 0.2
    }

    total_weight = sum(weights.values())
    wqi = 0

    for param, weight in weights.items():
        if param in row:
            wqi += row[param] * weight

    return wqi / total_weight
