# sleep_analysis.py

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # ✅ Non-interactive backend (prevents blocking)
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api as sm
import datetime
import sys
import os


# 🧩 SETTINGS
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)
pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x: f"{x:.4f}")

# 📁 Paths
out_dir = "/Users/danli/Documents/sleep"
os.makedirs(out_dir, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
master_path = f"{out_dir}/sleep_full_regression_report_{timestamp}.txt"

# 1️⃣ Load data
file_path = f"{out_dir}/sql_clean_sleep.csv"
df = pd.read_csv(file_path)

# 2️⃣ Basic overview
print("📄 Dataset Shape:", df.shape)
print("\n🔍 Columns:\n", df.columns)
print("\n✅ Data Types:\n", df.dtypes)
print("\n🧹 Missing Values:\n", df.isnull().sum())

# 🧹 Clean Sleep Disorder Column
df["sleep_disorder"] = (
    df["sleep_disorder"]
    .astype(str)
    .str.replace("\r", "", regex=False)
    .str.strip()
)
print("\n✅ Cleaned Sleep Disorder Categories:\n", df["sleep_disorder"].value_counts())

# 3️⃣ Descriptive statistics
print("\n📊 Summary Statistics:\n", df.describe(include="all"))

# 🔗 Correlation
numeric_df = df.select_dtypes(include=["float64", "int64"])
corr = numeric_df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap - Sleep Dataset")
plt.tight_layout()
plt.savefig(f"{out_dir}/correlation_heatmap_{timestamp}.png")
plt.close()

# -------------------------------
# 🧮 REGRESSION ANALYSIS
# -------------------------------
df = df.drop(columns=["id"], errors="ignore").dropna()

# Model 1
model1 = smf.ols("quality_of_sleep ~ stress_level", data=df).fit()

# Model 2
model2 = smf.ols("quality_of_sleep ~ stress_level * Physical_Activity_level", data=df).fit()

# Model 3
model3 = smf.ols("""
    quality_of_sleep ~ stress_level * Physical_Activity_level
                     + sleep_duration
                     + age
                     + heart_rate
""", data=df).fit()

# 🎨 Interaction Plot
sns.lmplot(
    x="stress_level",
    y="quality_of_sleep",
    hue="Physical_Activity_level",
    data=df,
    palette="coolwarm",
    scatter_kws={"alpha": 0.6}
)
plt.title("Interaction: Stress × Physical Activity on Sleep Quality")
plt.tight_layout()
plt.savefig(f"{out_dir}/interaction_plot_{timestamp}.png")
plt.close()

# -------------------------------
# 🔮 Multinomial Logistic Regression
# -------------------------------
X = df[["stress_level", "quality_of_sleep"]]
X = sm.add_constant(X)
y = df["sleep_disorder"].astype("category")
mnlogit_model = sm.MNLogit(y, X).fit()
params = mnlogit_model.params
odds_ratios = np.exp(params)

# Predicted probabilities
stress_vals = np.linspace(df["stress_level"].min(), df["stress_level"].max(), 100)
avg_quality = df["quality_of_sleep"].mean()
pred_df = pd.DataFrame({"const": 1, "stress_level": stress_vals, "quality_of_sleep": avg_quality})
pred_probs = mnlogit_model.predict(pred_df)
pred_probs.columns = mnlogit_model.params.index  # ✅ Fixed label assignment

plt.figure(figsize=(8,6))
for disorder in pred_probs.columns:
    plt.plot(stress_vals, pred_probs[disorder], label=disorder)
plt.title("Predicted Probability of Sleep Disorder vs Stress Level")
plt.xlabel("Stress Level")
plt.ylabel("Predicted Probability")
plt.legend(title="Disorder Type")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{out_dir}/sleep_disorder_probabilities_{timestamp}.png")
plt.close()

# -------------------------------
# 🧠 Extended Multinomial Model
# -------------------------------
X_full = df[["stress_level", "quality_of_sleep", "sleep_duration", "heart_rate", "age"]]
X_full = sm.add_constant(X_full)
mnlogit_model_full = sm.MNLogit(y, X_full).fit()
params_full = mnlogit_model_full.params
odds_ratios_full = np.exp(params_full)

# -------------------------------
# 💾 WRITE ALL RESULTS TO ONE FILE
# -------------------------------
with open(master_path, "w") as f:
    f.write("📊 FULL SLEEP ANALYSIS REPORT\n")
    f.write(f"Generated on: {timestamp}\n\n")

    for name, model in [
        ("🧩 Model 1 – Stress → Quality of Sleep", model1),
        ("💪 Model 2 – Stress × Physical Activity Interaction", model2),
        ("📈 Model 3 – Full Regression with Covariates", model3),
        ("🔮 Multinomial Model – Predict Sleep Disorder", mnlogit_model),
        ("🧠 Extended Multinomial Model – With Sleep Duration, HR, Age", mnlogit_model_full),
    ]:
        f.write(f"{'='*120}\n{name}\n{'='*120}\n\n")
        f.write(model.summary().as_text())
        f.write("\n\n")

    f.write("\n📊 Multinomial Odds Ratios:\n")
    f.write(odds_ratios.to_string())
    f.write("\n\n📊 Extended Model Odds Ratios:\n")
    f.write(odds_ratios_full.to_string())
    f.write("\n")

print(f"\n✅ All regression and multinomial summaries saved to:\n   {master_path}\n")
print("✅ All plots saved to:", out_dir)
print("\n✅ Analysis complete.\n")
sys.stdout.flush()
