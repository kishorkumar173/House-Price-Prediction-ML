# ================================
# STEP 2: EDA + VISUALIZATION
# ================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/raw/train.csv")

# ------------------------------
# 1. TARGET DISTRIBUTION
# ------------------------------
plt.figure(figsize=(8,5))
sns.histplot(df["SalePrice"], kde=True)
plt.title("Sale Price Distribution")
plt.savefig("outputs/saleprice_dist.png")
plt.show()

# ------------------------------
# 2. CORRELATION HEATMAP
# ------------------------------
plt.figure(figsize=(12,8))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("outputs/heatmap.png")
plt.show()

# ------------------------------
# 3. TOP CORRELATED FEATURES
# ------------------------------
corr_target = corr["SalePrice"].sort_values(ascending=False)
print("\nTop Correlated Features:\n", corr_target.head(10))

# ------------------------------
# 4. SCATTER PLOTS
# ------------------------------
important_features = ["GrLivArea", "OverallQual", "GarageCars"]

for feature in important_features:
    plt.figure()
    sns.scatterplot(x=df[feature], y=df["SalePrice"])
    plt.title(f"{feature} vs SalePrice")
    plt.savefig(f"outputs/{feature}_vs_price.png")
    plt.show()
    
    # ================================
# STEP 3: DATA CLEANING
# ================================

# Drop columns with too many missing values
df = df.drop(columns=["Alley", "PoolQC", "Fence", "MiscFeature"], errors='ignore')

# Fill missing numerical values
df.fillna(df.median(numeric_only=True), inplace=True)

# Fill categorical values
df.fillna("None", inplace=True)

print("\nMissing values after cleaning:\n", df.isnull().sum().sum())

# Save cleaned data
df.to_csv("data/processed/cleaned_data.csv", index=False)
print("Cleaned data saved!")