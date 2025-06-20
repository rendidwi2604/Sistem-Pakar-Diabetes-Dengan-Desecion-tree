import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("diabetes_cleaned_final_with_sehat.csv")

# Pisahkan fitur dan target
X = df.drop(columns=['Target'])
y = df['Target']

# Latih model
clf = DecisionTreeClassifier(max_depth=4, random_state=42)
clf.fit(X, y)

# Gambar pohon keputusan
plt.figure(figsize=(20, 10))
plot_tree(clf, feature_names=X.columns, class_names=[str(i) for i in sorted(y.unique())], filled=True)
plt.savefig("decision_tree_diabetes.png")
