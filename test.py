import numpy as np

# training_RMSE = np.array([])
# test_RMSE = np.array([])
#
# training_r_squared = np.array([])
# test_r_squared = np.array([])

NDCG = np.array([0.19, 0.13, 0.18])
PrecisionAtN = np.array([0.18, 0.15, 0.19])

# print(np.mean(training_RMSE))
# print(np.std(training_RMSE, ddof=1))
# print(np.mean(test_RMSE))
# print(np.std(test_RMSE, ddof=1))
# print(np.mean(training_r_squared))
# print(np.std(training_r_squared, ddof=1))
# print(np.mean(test_r_squared))
# print(np.std(test_r_squared, ddof=1))

print(np.mean(NDCG))
print(np.std(NDCG, ddof=1))
print(np.mean(PrecisionAtN))
print(np.std(PrecisionAtN, ddof=1))
