def calculate_fusion(sensor_data):
    total_weight = 0
    weighted_confidence = 0

    for sensor in sensor_data:
        confidence = sensor["confidence"]
        trust = sensor["trust"]

        weighted_confidence += confidence * trust
        total_weight += trust

    if total_weight == 0:
        return 0

    final_confidence = weighted_confidence / total_weight

    return round(final_confidence, 2)