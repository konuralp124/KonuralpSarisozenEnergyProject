from math import sqrt, pi, sin

def anomaly_detection(data_stream, alpha=0.2, threshold=3, min_data_points=30):
    """
    Detects anomalies in a data stream using an adaptive EWMA, starting after accumulating enough data.
    Further details can be found in README.md
    Parameters:
    - data_stream: Generator yielding (data_point, is_true_anomaly).
    - alpha: Smoothing factor for EWMA.
    - threshold: Number of standard deviations for anomaly detection.
    - min_data_points: Minimum number of data points before starting anomaly detection.

    Yields:
    - data_point: The current data point.
    - ewma: The updated EWMA.
    - std_dev: The updated standard deviation.
    - is_anomaly: Boolean indicating whether the current data point is detected as an anomaly.
    - is_true_anomaly: Boolean indicating whether the current data point is a true anomaly, based on data stream simulation flag.
    """
    #Generate some initial data batch to initialize values of EMWA, variance, and std_dev.
    initial_data = []
    for _ in range(min(min_data_points, 10)):
        data_point, is_true_anomaly = next(data_stream)
        initial_data.append(data_point)
        yield data_point, data_point, 0, False, is_true_anomaly

    # Initialize EWMA and variance based on the initial data batch and its mean
    #This is important for error handling and validity because otherwise if we simply equlize emwa with the first data point other than the mean of first 10, we would have to initialize varience as 0, which would have created problems in updating varience before the detection of anomaly.
    ewma = sum(initial_data) / len(initial_data)
    variance = sum((x - ewma) ** 2 for x in initial_data) / len(initial_data)
    std_dev = sqrt(variance) 

    data_count = len(initial_data)  # Number of data points processed
    time = data_count
    is_anomaly = False

    for data_point, is_true_anomaly in data_stream:
        # Calculate deviation from the previous EWMA for anomaly detection
        deviation = abs(data_point - ewma)

        if deviation > threshold * std_dev:
            is_anomaly = True
            print(f"Anomaly detected at time {time}: {data_point}")
        else:
            is_anomaly = False

        # Update EWMA
        ewma = alpha * data_point + (1 - alpha) * ewma

        #Update variance and standard deviation
        variance = alpha * (data_point - ewma) ** 2 + (1 - alpha) * variance

        std_dev = sqrt(variance) 

        yield data_point, ewma, std_dev, is_anomaly, is_true_anomaly

        # Print the results instead of yielding to simulate console output.
        # print(f"Time: {time}, Data Point: {data_point}, EWMA: {ewma:.2f}, Std Dev: {std_dev:.2f}, "
        #       f"Is Anomaly: {is_anomaly}, True Anomaly: {is_true_anomaly}")

        time += 1
        data_count += 1