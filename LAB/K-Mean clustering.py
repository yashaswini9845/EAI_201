INPUT:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

data = pd.read_csv("C:\Users\mgyas\Downloads\WA_Fn-UseC_-Telco-Customer-Churn (1).csv")
print("Data shape:", data.shape)
print(data.head())

#Preprocessing here we Droping ID column 
data.drop('customerID', axis=1, inplace=True)

# Handling the missing or blank TotalCharges.
data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
data['TotalCharges'].fillna(data['TotalCharges'].median(), inplace=True)

# Encode categorical columns
for col in data.columns:
    if data[col].dtypes == 'object':
        if len(data[col].unique()) == 2:
            data[col] = LabelEncoder().fit_transform(data[col])
        else:
            data = pd.get_dummies(data, columns=[col], drop_first=True)

# 3.4 Standardize numerical data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

#  PCA - Reduce to 2 components
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)
print("Explained variance ratio:", pca.explained_variance_ratio_)
print("Total variance explained:", round(sum(pca.explained_variance_ratio_)*100, 2), "%")

# Plot PCA scatter
plt.figure(figsize=(8,6))
plt.scatter(pca_data[:,0], pca_data[:,1])
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("PCA - 2D Scatter Plot")
plt.show()

# K-Means - Find best number of clusters
inertia = []
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(pca_data)
    inertia.append(km.inertia_)

plt.figure(figsize=(6,4))
plt.plot(range(2,11), inertia, 'bo-')
plt.xlabel('k')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()

# Silhouette Score check
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42)
    preds = km.fit_predict(pca_data)
    print(f"k={k}, Silhouette Score={silhouette_score(pca_data, preds):.3f}")

# Apply K-Means with chosen k (e.g. 3)
best_k = 3
kmeans = KMeans(n_clusters=best_k, random_state=42)
data['Cluster'] = kmeans.fit_predict(pca_data)

# Visualize clusters
plt.figure(figsize=(8,6))
sns.scatterplot(x=pca_data[:,0], y=pca_data[:,1], hue=data['Cluster'], palette='Set2')
plt.title("K-Means Clusters on PCA Data")
plt.show()

# Analyzing clusters in original data
summary = data.groupby('Cluster')[['MonthlyCharges','TotalCharges','tenure','Churn']].mean()
print("\nCluster Summary:")
print(summary)

# Visualize MonthlyCharges by cluster
plt.figure(figsize=(6,4))
sns.boxplot(x='Cluster', y='MonthlyCharges', data=data)
plt.title("Monthly Charges by Cluster")
plt.show()

# Visualize tenure by cluster
plt.figure(figsize=(6,4))
sns.boxplot(x='Cluster', y='tenure', data=data)
plt.title("Tenure by Cluster")
plt.show()


OUTPUT:


Data shape: (7043, 21)
   customerID  gender  SeniorCitizen Partner Dependents  ...  PaperlessBilling              PaymentMethod MonthlyCharges TotalCharges Churn
0  7590-VHVEG  Female              0     Yes         No  ...               Yes           Electronic check          29.85        29.85    No 
1  5575-GNVDE    Male              0      No         No  ...                No               Mailed check          56.95       1889.5    No 
2  3668-QPYBK    Male              0      No         No  ...               Yes               Mailed check          53.85       108.15   Yes 
3  7795-CFOCW    Male              0      No         No  ...                No  Bank transfer (automatic)          42.30      1840.75    No 
4  9237-HQITU  Female              0      No         No  ...               Yes           Electronic check          70.70       151.65   Yes 

[5 rows x 21 columns]
c:\Users\ThisPC\Desktop\text_folder_for_trials\11_10_25_lab\datahandellab.py:19: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.

For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.


  data['TotalCharges'].fillna(data['TotalCharges'].median(), inplace=True)
Explained variance ratio: [0.322288   0.12301522]
Total variance explained: 44.53 %
k=2, Silhouette Score=0.674
k=3, Silhouette Score=0.586
k=4, Silhouette Score=0.509
k=5, Silhouette Score=0.464
k=6, Silhouette Score=0.451
k=7, Silhouette Score=0.403
k=8, Silhouette Score=0.396
k=9, Silhouette Score=0.394
k=10, Silhouette Score=0.398

Cluster Summary:
         MonthlyCharges  TotalCharges     tenure     Churn
Cluster
0             88.099144   4911.263169  55.403081  0.112965
1             21.079194    668.099443  30.547182  0.074050
2             68.572972   1124.024890  16.320126  0.469182
