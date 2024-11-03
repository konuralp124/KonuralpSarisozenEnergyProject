import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from anomaly_detection import anomaly_detection
from data_stream import data_stream

def live_plot(alpha=0.2, threshold=3, min_data_points=30):
    """
    Real-time visualization of energy consumption data and detected anomalies,
    including performance metrics like precision, recall, and F1 score.

    Parameters:
    - alpha: Smoothing factor for EWMA.
    - threshold: Number of standard deviations for anomaly detection.
    - min_data_points: Minimum number of data points before starting anomaly detection.
    """
    # Create a figure and axis for plotting
    fig, ax = plt.subplots()

    # Lists to store data for plotting
    x_data, y_data = [], []
    ewma_data = []
    anomaly_x, anomaly_y = [], []
    true_anomaly_x, true_anomaly_y = [], []

    # Plot elements
    line, = ax.plot([], [], 'b-', label='Energy Consumption')
    ewma_line, = ax.plot([], [], 'g--', label='EWMA')
    anomalies_scatter = ax.scatter([], [], c='r', label='Detected Anomalies')
    true_anomalies_scatter = ax.scatter([], [], c='orange', marker='x', label='True Anomalies')
    performance_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    # Initialize performance metrics
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    def update(frame):
        nonlocal true_positives, false_positives, false_negatives

        data_point, ewma, std_dev, is_anomaly, is_true_anomaly = frame
        x = len(x_data)

        x_data.append(x)
        y_data.append(data_point)
        ewma_data.append(ewma)

        line.set_data(x_data, y_data)
        ewma_line.set_data(x_data, ewma_data)

        # Update anomalies
        if is_anomaly:
            anomaly_x.append(x)
            anomaly_y.append(data_point)
            anomalies_scatter.set_offsets(list(zip(anomaly_x, anomaly_y)))

        if is_true_anomaly:
            true_anomaly_x.append(x)
            true_anomaly_y.append(data_point)
            true_anomalies_scatter.set_offsets(list(zip(true_anomaly_x, true_anomaly_y)))

        # Update performance metrics
        if is_anomaly and is_true_anomaly:
            true_positives += 1
        elif is_anomaly and not is_true_anomaly:
            false_positives += 1
        elif not is_anomaly and is_true_anomaly:
            false_negatives += 1

        precision = (true_positives / (true_positives + false_positives)
                     if (true_positives + false_positives) > 0 else 0)
        recall = (true_positives / (true_positives + false_negatives)
                  if (true_positives + false_negatives) > 0 else 0)
        f1_score = (2 * precision * recall / (precision + recall)
                    if (precision + recall) > 0 else 0)

        performance_text.set_text(f'Precision: {precision:.2f}, Recall: {recall:.2f}, F1 Score: {f1_score:.2f}')

        # Adjust axes limits
        ax.set_xlim(max(0, x - 100), x + 10)  # Show the last 100 data points
        y_min = min(y_data[-100:] + ewma_data[-100:] + [min(anomaly_y + true_anomaly_y + [float('inf')])]) - 10
        y_max = max(y_data[-100:] + ewma_data[-100:] + [max(anomaly_y + true_anomaly_y + [float('-inf')])]) + 10
        ax.set_ylim(y_min, y_max)

        ax.set_xlabel('Time (Hours)')
        ax.set_ylabel('Energy Consumption (kWh)')
        ax.set_title('Real-Time Energy Consumption Monitoring')
        ax.legend(loc='upper left')

        return line, ewma_line, anomalies_scatter, true_anomalies_scatter, performance_text

    # Create the animation
    ani = FuncAnimation(
        fig,
        update,
        frames=anomaly_detection(
            data_stream(),
            alpha=alpha,
            threshold=threshold,
            min_data_points=min_data_points
        ),
        interval=100,
        blit=False  # Disable blitting to allow axes updates
    )

    plt.show()

if __name__ == "__main__":
    live_plot()




