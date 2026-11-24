
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
OUTPUT_DIR = BASE_DIR / "data" / "analytics"
CHART_DIR = OUTPUT_DIR / "charts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

print("========== PYTHON ANALYTICS STARTED ==========")

# Load cleaned datasets
users = pd.read_csv(DATA_DIR / "users_clean.csv")
activity = pd.read_csv(DATA_DIR / "user_activity_clean.csv")

# Convert dates
users["registration_date"] = pd.to_datetime(users["registration_date"])
activity["event_timestamp"] = pd.to_datetime(activity["event_timestamp"])

# Add registration date to activity records
activity = activity.merge(
    users[["user_id", "registration_date"]],
    on="user_id",
    how="left"
)

# Exclude activity occurring before user registration
activity = activity[
    activity["event_timestamp"] >= activity["registration_date"]
].copy()

# Create month columns
users["cohort_month"] = (
    users["registration_date"].dt.to_period("M")
)

activity["activity_month"] = (
    activity["event_timestamp"].dt.to_period("M")
)

activity["duration_seconds"] = pd.to_numeric(
    activity["duration_seconds"], errors="coerce"
)

# 1. Monthly Engagement Analysis
monthly = activity.groupby("activity_month").agg(
    total_events=("event_id", "count"),
    active_users=("user_id", "nunique"),
    avg_duration_seconds=("duration_seconds", "mean")
).reset_index()

monthly["new_users"] = monthly["activity_month"].map(
    users.groupby("cohort_month").size()
).fillna(0).astype(int)

monthly["activity_month"] = monthly["activity_month"].astype(str)

monthly.to_csv(
    OUTPUT_DIR / "monthly_engagement.csv",
    index=False
)

print("\nMONTHLY ENGAGEMENT")
print(monthly.to_string(index=False))

# 2. Cohort Retention Analysis
cohort_activity = activity[
    ["user_id", "activity_month"]
].drop_duplicates()

cohort_activity = cohort_activity.merge(
    users[["user_id", "cohort_month"]],
    on="user_id",
    how="left"
)

cohort_activity["cohort_index"] = (
    (cohort_activity["activity_month"].dt.year -
     cohort_activity["cohort_month"].dt.year) * 12
    +
    (cohort_activity["activity_month"].dt.month -
     cohort_activity["cohort_month"].dt.month)
)

cohort_counts = cohort_activity.groupby(
    ["cohort_month", "cohort_index"]
)["user_id"].nunique().reset_index(name="active_users")

cohort_sizes = users.groupby("cohort_month").size()

retention = cohort_counts.copy()

retention["cohort_size"] = retention["cohort_month"].map(
    cohort_sizes
)

retention["retention_rate"] = (
    retention["active_users"] /
    retention["cohort_size"] * 100
).round(2)

cohort_pivot = retention.pivot(
    index="cohort_month",
    columns="cohort_index",
    values="retention_rate"
)

cohort_pivot.index = cohort_pivot.index.astype(str)
cohort_pivot.columns = [
    f"Month_{int(col)}" for col in cohort_pivot.columns
]

cohort_pivot.to_csv(
    OUTPUT_DIR / "cohort_retention.csv"
)

print("\nCOHORT RETENTION (%)")
print(cohort_pivot.to_string())

# 3. Monthly Active Users Chart
plt.figure(figsize=(9, 5))
plt.plot(
    monthly["activity_month"],
    monthly["active_users"],
    marker="o"
)
plt.title("Monthly Active Users")
plt.xlabel("Month")
plt.ylabel("Active Users")
plt.grid(True)
plt.tight_layout()
plt.savefig(CHART_DIR / "monthly_active_users.png")
plt.close()

# 4. Monthly Events Chart
plt.figure(figsize=(9, 5))
plt.bar(
    monthly["activity_month"],
    monthly["total_events"]
)
plt.title("Monthly User Activity Events")
plt.xlabel("Month")
plt.ylabel("Total Events")
plt.tight_layout()
plt.savefig(CHART_DIR / "monthly_events.png")
plt.close()

# 5. Cohort Retention Heatmap
plt.figure(figsize=(9, 5))
plt.imshow(cohort_pivot, aspect="auto", cmap="Blues")
plt.colorbar(label="Retention (%)")
plt.xticks(
    range(len(cohort_pivot.columns)),
    cohort_pivot.columns
)
plt.yticks(
    range(len(cohort_pivot.index)),
    cohort_pivot.index
)
plt.title("Cohort Retention Analysis")
plt.xlabel("Cohort Period")
plt.ylabel("Registration Cohort")
plt.tight_layout()
plt.savefig(CHART_DIR / "cohort_retention_heatmap.png")
plt.close()

print("\nAnalytics files saved successfully!")
print("Output folder:", OUTPUT_DIR)
