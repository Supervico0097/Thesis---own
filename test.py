import numpy as np

training_RMSE = np.array([12.51, 11.66, 12.30, 12.39, 11.67])
test_RMSE = np.array([13.03, 12.78, 16.94, 16.48, 15.43])

training_r_squared = np.array([0.77, 0.76, 0.85, 0.77, 0.81])
test_r_squared = np.array([0.71, 0.6, 0.75, 0.62, 0.7])

print(np.mean(training_RMSE))
print(np.std(training_RMSE, ddof=1))
print(np.mean(test_RMSE))
print(np.std(test_RMSE, ddof=1))
print(np.mean(training_r_squared))
print(np.std(training_r_squared, ddof=1))
print(np.mean(test_r_squared))
print(np.std(test_r_squared, ddof=1))
