# Efficient Data Stream Anomaly Detection

## Project Description

This project involves developing a Python application capable of detecting anomalies in a continuous data stream that simulates energy consumption data. The data stream incorporates regular patterns (daily and weekly seasonality), random noise, anomalies (both positive and negative), and concept drift. The anomaly detection algorithm uses an Exponentially Weighted Moving Average (EWMA) to adapt to changes in the data over time such as seasonal changes and gradual changes like concept drift, with a delayed anomaly detection mechanism to ensure statistical reliability. The application includes real-time visualization of the data stream, detected anomalies, true anomalies, and performance metrics (precision, recall, and F1 score).

## Objectives

- **Algorithm Implementation**: Utilize EWMA for anomaly detection, suitable for adapting to concept drift and seasonal variations.
- **Data Stream Simulation**: Create a function to emulate energy consumption data with seasonality, noise, anomalies, and concept drift.
- **Anomaly Detection**: Develop a real-time mechanism to accurately flag anomalies after accumulating enough data points.
- **Performance Evaluation**: Compute and display performance metrics (precision, recall, F1 score) in real-time.
- **Visualization**: Provide a real-time visualization tool to display the data stream, detected anomalies, true anomalies, and performance metrics.

## Files

- `data_stream.py`: Simulates the energy consumption data stream.
- `anomaly_detection.py`: Contains the EWMA-based anomaly detection algorithm with delayed detection.
- `visualization.py`: Handles real-time visualization of the data, anomalies, and performance metrics.
- `requirements.txt`: Lists external libraries required.
- `README.md`: Project description and algorithm explanation.

## Data Stream Simulation

The `data_stream.py` script simulates a realistic energy consumption data stream by incorporating the following components:

### Daily Seasonality

- **Implementation**: Modeled using a sine function with a 24-hour period.
- **Equation**:

	$$\text{Daily Seasonality} = 12 \times \sin\left(\frac{2\pi \times (\text{time} \mod 24)}{24}\right)$$

- **Explanation**: Represents typical daily fluctuations in energy consumption, such as higher usage during the day and lower usage at night.

### Weekly Seasonality

- **Implementation**: Modeled using a sine function with a 168-hour period (7 days * 24 hours).
- **Equation**:

	$$\text{Weekly Seasonality} = 6 \times \sin\left(\frac{2\pi \times (\text{time} \mod 168)}{168}\right)$$

- **Explanation**: Captures variations between weekdays and weekends, reflecting different energy usage patterns.

### Random Noise

- **Implementation**: Added using a uniform random distribution between -5 and 5.
- **Equation**:

	$$\text{Noise} = \text{random.uniform}(-2, 2)$$

- **Explanation**: Introduces variability to mimic unpredictable fluctuations in real-world energy consumption data.

### Anomalies

- **Implementation**: Introduced at random intervals with a 2% chance at each time step.
- **Types**:
	- **Positive Anomalies**: Sudden spikes in energy consumption.
	- **Negative Anomalies**: Sudden drops in energy consumption.
- **Equation**:

	$$\text{Anomaly Magnitude} = \text{Anomaly Direction} \times \text{random.uniform}(30, 50)$$

	- **Anomaly Direction**: Randomly chosen as -1 or 1.

- **Explanation**: Simulates unexpected events affecting energy consumption, such as equipment failures or unusual high-demand events.

### Concept Drift

- **Implementation**: Simulated as a gradual increase in the base energy consumption over time.
- **Equation**:

 $$\text{Concept Drift} = \text{Drift Rate} \times \text{time}$$

	- **Drift Rate**: Set to a small positive value (e.g., 0.001) to represent gradual changes.

- **Explanation**: Represents long-term changes in energy consumption patterns due to factors like seasonal shifts or increasing demand.

### Combined Data Stream Equation

The overall energy consumption value at each time step is calculated as:

$$\text{Energy Consumption} = \text{Base Consumption} + \text{Daily Seasonality} + \text{Weekly Seasonality} + \text{Concept Drift} + \text{Noise} + \text{Anomalies}$$

- **Base Consumption**: A constant value representing the average energy usage (e.g., 100 units).

## Algorithm Explanation

### Exponentially Weighted Moving Average (EWMA)

EWMA is used to calculate a weighted average of past observations, where the weights decrease exponentially over time. This makes the algorithm more sensitive to recent data, allowing it to adapt quickly to changes, such as concept drift and seasonal changes in energy consumption patterns. To clarify, EMWA gives more wight to recent data while at the same time being affected by the past data. This fits the project description as well as the designed simulation because seasonal changes and concept drift require further adjustments not to give false positive results for anomalies in cases where these changes are actually part of "changes occuring periodically" or "changes occuring gradually". If less weight is given to past data as new data comes, the algorithm is more advanced to adjust itself to seasonality and drifts. Besides, it can also easily detect the recent changes in data by comparing the new data to recent ongoing trend, and it can identify an anomaly that would not be identified otherwise. To examplify, if an anomaly occurs during the period of a seasonal change, EMWA can handle it better compared to a simple moving average algorithm because EMWA will be more aware of the seasonal pattern that the data is currently in.

**Formula:**

- **EWMA:**
	$$\text{EWMA}_t = \alpha \cdot x_t + (1 - \alpha) \cdot \text{EWMA}_{t-1}$$

	- $$\( x_t \)$$ : Current data point at time \( t \).
	- $$\( \alpha \)$$ : Smoothing factor (between 0 and 1).

- **Variance:**
	$$\sigma_t^2 = \alpha \cdot (x_t - \text{EWMA}_t)^2 + (1 - \alpha) \cdot \sigma_{t-1}^2$$

- **Standard Deviation:**

	$$\sigma_t = \sqrt{\sigma_t^2}$$

**Anomaly Detection:**

An anomaly is flagged if the absolute deviation of the current data point from the EWMA exceeds a certain threshold times the standard deviation, starting after a minimum number of data points have been processed:

$$\text{If } |x_t - \text{EWMA}_t| > \text{Threshold} \times \sigma_t, \text{ then flag as anomaly}$$

### Delayed Anomaly Detection

To ensure statistical reliability, anomaly detection starts only after a specified number of data points (`min_data_points`) have been accumulated. This allows the EWMA and variance estimates to stabilize.

- **Minimum Data Points (`min_data_points`)**: Default is set to 30 but can be adjusted.
- **Behavior**: Anomaly detection logic is skipped until the required number of data points is reached.

## Parameter Tuning

### Smoothing Factor (`alpha`)

- Controls the weight given to recent observations.
- Higher values (e.g., 0.5) make the EWMA more responsive.
- Adjustments are based on how quickly you want the algorithm to adapt to changes. Requires a certain level of domain knowledge.

### Threshold (`threshold`)

- Determines the sensitivity of anomaly detection.
- Typical values are between 2 and 3 standard deviations.
- Lower values make the algorithm more sensitive but may increase false positives.

### Minimum Data Points (`min_data_points`)

- Specifies when to start anomaly detection.
- A higher value ensures more reliable statistics but delays detection.
- Balance between early detection and statistical confidence.

## Error Handling and Data Validation

- Initial EMWA=Mean of first 10 data points->prevents standard deviation from being 0 and allows to calculate standard variations after checking the anomaly.
- Edge cases, such as insufficient data points, are managed to prevent exceptions.
- Performance evaluation is present.

## Limitations

- **Sensitivity to Noise**: The EWMA method may overreact to sudden, short-term fluctuations (noise) if the smoothing factor is set too high. That's why, with current functions and parameters, 0.2 is sufficient for the given domain simulation: energy consumption.
- **Univariate Analysis**: The algorithm analyzes one variable (energy consumption) and does not consider potential correlations with other variables.

## Optimizations
- The algorithm choice and its implementation itself is optimized. It is based on recursive calculation of EMWA; hence it does not require directly memorizing every single past data but deals with one value at a time, whenever a new data point is being checked. The algorithm processes each data point individually, performing a fixed number of operations regardless of the size of the data stream. It maintains a constant amount of state information (EWMA, variance, etc.) and does not store past data points after the initialization phase. Besides, efficient recursive calculations are used within the algorithm whenever needed, such as the calculations of varience&standard deviation within for loop. 

- Total Time Complexity for N Data Points: O(N)

## Visualization

The `visualization.py` script provides a real-time visualization of the energy consumption data, detected anomalies, true anomalies, and performance metrics.

### Features

- **Energy Consumption Plot**: Displays the simulated energy consumption data over time.
- **EWMA Plot**: Shows the EWMA line to visualize the moving average.
- **Detected Anomalies**: Marks the anomalies detected by the algorithm with red dots.
- **True Anomalies**: Marks the actual anomalies introduced in the simulation with orange 'x' markers.
- **Performance Metrics**: Calculates and displays precision, recall, and F1 score in real-time on the plot.
- **Interactive Visualization**: Updates dynamically as new data points are processed.

### Performance Metrics

- **Precision**: Proportion of detected anomalies that are true anomalies.

 $$\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}$$

- **Recall**: Proportion of true anomalies that were correctly detected.

 $$\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}$$

- **F1 Score**: Harmonic mean of precision and recall, providing a balance between the two.

	$$\text{F1 Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

## Possible Future Enhancements

- **Dynamic Thresholding and Alpha**: We can implement dynamic thresholds and alphas based on recent data variability to improve detection accuracy. However, for threshold, since threshold is utilized with the standard daviation of the past data, it is already dynamic to a certain extent in terms of its effect on detection. 
- **Machine Learning**:We can use advanced machine learning algorithms, though it would require more computational power.
## How to Run the Project

1. **Install Dependencies**:
	pip install -r requirements.txt
	 
2. **Run visualization.py** 
	python3 visualization.py