# ==========================================
# HOUSE PRICE PREDICTION - COMPLETE PROJECT
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ================================
# STEP 1: LOAD DATA
# ================================

df = pd.read_csv("data/raw/train.csv")

print("Dataset Shape:", df.shape)

# ================================
# STEP 2: EDA
# ================================

# Sale Price Distribution
plt.figure(figsize=(8,5))
sns.histplot(df["SalePrice"], kde=True)
plt.title("Sale Price Distribution")
plt.savefig("outputs/saleprice_dist.png")
plt.close()

# Correlation Heatmap
plt.figure(figsize=(12,8))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("outputs/heatmap.png")
plt.close()

# ================================
# STEP 3: DATA CLEANING
# ================================

df = df.drop(columns=["Alley", "PoolQC", "Fence", "MiscFeature"], errors='ignore')

df.fillna(df.median(numeric_only=True), inplace=True)
df.fillna("None", inplace=True)

print("Missing Values:", df.isnull().sum().sum())

# ================================
# STEP 4: FEATURE SELECTION
# ================================

features = [
    "OverallQual",
    "GrLivArea",
    "GarageCars",
    "TotalBsmtSF",
    "FullBath",
    "YearBuilt"
]

X = df[features]
y = df["SalePrice"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================================
# STEP 5: MODEL TRAINING
# ================================

lr = LinearRegression()
lr.fit(X_train, y_train)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# ================================
# STEP 6: EVALUATION
# ================================

lr_pred = lr.predict(X_test)
rf_pred = rf.predict(X_test)

def evaluate(y_true, y_pred, name):
    print(f"\n{name}")
    print("MAE:", mean_absolute_error(y_true, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_true, y_pred)))
    print("R2 Score:", r2_score(y_true, y_pred))

evaluate(y_test, lr_pred, "Linear Regression")
evaluate(y_test, rf_pred, "Random Forest")

# ================================
# STEP 7: VISUALIZATION
# ================================

plt.scatter(y_test, rf_pred)
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted (Random Forest)")
plt.savefig("outputs/actual_vs_predicted.png")
plt.close()

# ================================
# STEP 8: SAMPLE PREDICTION
# ================================

sample_house = [[7, 1500, 2, 800, 2, 2005]]

predicted_price = rf.predict(sample_house)

print("\nSample House Predicted Price:", predicted_price[0])

# Save Random Forest model
joblib.dump(rf, "models/house_price_model.pkl")

print("Model saved successfully!")