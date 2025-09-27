# pip install scikit-learn numpy matplotlib để chạy code



from sklearn.datasets import make_blobs
import numpy as np
from sklearn.ensemble import IsolationForest 
import matplotlib.pyplot as plt

np.random.seed(3)
X, _ = make_blobs(n_samples=300, centers=1, cluster_std=.3, center_box=(10,10))
outliers, _ = make_blobs(n_samples=5, centers=1, cluster_std=.05, center_box=(11,11))
X = np.concatenate([X,outliers])
DTRTYFTFT
plt.figure(figsize=(7,7))
plt.scatter(X[:, 0], X[:, 1], marker="o", s=25, edgecolor="b")

IF = IsolationForest(n_estimators=100, contamination=.05)
predictions = IF.fit_predict(X)

outlier_index = np.where(predictions==-1)
values = X[outlier_index]   
plt.figure(figsize=(7,7))
plt.scatter(X[:,0], X[:,1], s=25, marker="o", edgecolor = 'b') 
plt.scatter(values[:,0], values[:,1], s=25, marker="o", color='r') 

plt.show()