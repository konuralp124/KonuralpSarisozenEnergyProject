import math
import random

def data_stream():
    """
    Simulates an energy consumption data stream with daily and weekly seasonality,
    random noise, anomalies, and concept drift.

    Yields:
    - value: Simulated energy consumption at each time step.
    - is_true_anomaly: Boolean indicating whether an anomaly was introduced at this time step.
    """
    time = 0
    daily_period = 24
    weekly_period = 168  # 7 days * 24 hours
    base_consumption = 100  # Base energy consumption level
    drift_rate = 0.001  # Rate at which concept drift occurs

    while True:
        # Simulate daily seasonality
        daily_seasonality = 12 * math.sin(2 * math.pi * (time % daily_period) / daily_period)
        
        # Simulate weekly seasonality
        weekly_seasonality = 6 * math.sin(2 * math.pi * (time % weekly_period) / weekly_period)
        
        # Simulate concept drift
        drift = drift_rate * time  # Gradual increase over time
        
        # Combine base consumption with seasonality and drift
        value = base_consumption + daily_seasonality + weekly_seasonality + drift
        
        # Add random noise
        noise = random.uniform(-2, 2)
        value += noise
        
        # Introduce anomalies at random intervals
        is_true_anomaly = False
        if random.random() < 0.02:  # 2% chance to introduce an anomaly
            anomaly_direction = random.choice([-1, 1])
            anomaly_magnitude = anomaly_direction * random.uniform(30, 50)
            value += anomaly_magnitude
            print(f"Anomaly introduced at time {time}: {value}")
            is_true_anomaly = True

        yield value, is_true_anomaly
        time += 1  # Assuming each iteration represents one hour
