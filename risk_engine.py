
def classify_risk(wqi, ml_prob):
    if wqi > 200 or ml_prob < 0.4:
        return "CRITICAL"
    elif wqi > 100 or ml_prob < 0.6:
        return "WARNING"
    else:
        return "SAFE"
