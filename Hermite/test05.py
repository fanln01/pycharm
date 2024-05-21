import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the function to fit
def model(x, c0, c1):
    return x / (c0 * x + c1)

# Given data points
x_data = np.array([1, 2, 4, 5])
y_data = np.array([0.33, 0.40, 0.44, 0.45])

# Perform curve fitting
params, covariance = curve_fit(model, x_data, y_data)

# Extract the parameters
c0, c1 = params

# Print the parameters
print(f"c0 = {c0}, c1 = {c1}")

# Plot the data and the fitted curve
x_fit = np.linspace(1, 5, 100)
y_fit = model(x_fit, c0, c1)

plt.scatter(x_data, y_data, label='Data Points')
plt.plot(x_fit, y_fit, label='Fitted Curve', color='red')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
