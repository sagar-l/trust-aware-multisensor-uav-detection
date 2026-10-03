import random


def generate_sensor_data():
    """
    Generate simulated readings for Radar, RF and EO/IR sensors.

    These are demonstration values, not real sensor measurements.
    """

    sensors = ["Radar", "RF", "EO/IR"]

    sensor_data = []

    for sensor in sensors:

        signal_quality = round(
            random.uniform(0.70, 1.00), 2
        )

        availability = round(
            random.uniform(0.80, 1.00), 2
        )

        reliability = round(
            random.uniform(0.75, 1.00), 2
        )

        confidence = round(
            random.uniform(0.70, 0.95), 2
        )

        sensor_data.append({
            "sensor": sensor,
            "signal_quality": signal_quality,
            "availability": availability,
            "reliability": reliability,
            "confidence": confidence
        })

    return sensor_data