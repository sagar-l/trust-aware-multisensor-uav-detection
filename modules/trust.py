def calculate_trust(signal_quality, availability, reliability):
    """
    Calculate the trust score of a sensor.

    Trust is based on:
    - Signal Quality: 40%
    - Availability: 30%
    - Reliability: 30%
    """

    trust = (
        0.4 * signal_quality
        + 0.3 * availability
        + 0.3 * reliability
    )

    return round(trust, 2)