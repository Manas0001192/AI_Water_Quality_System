
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import joblib

df = pd.read_csv("water_potability.csv")

X = df.drop("Potability", axis=1)
y = df["Potability"]

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("model", RandomForestClassifier(n_estimators=200))
])

pipeline.fit(X, y)
joblib.dump(pipeline, "model.pkl")

print("Model Saved Successfully")
