
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Output directories
OUTPUT_DIR = BASE_DIR / "data" / "cleaned"
QUARANTINE_DIR = BASE_DIR / "data" / "quarantine"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

# Load raw datasets
users = pd.read_csv(BASE_DIR / "users.csv")
courses = pd.read_csv(BASE_DIR / "courses.csv")
enrollments = pd.read_csv(BASE_DIR / "enrollments.csv")
activity = pd.read_csv(BASE_DIR / "user_activity.csv")

# Convert date columns
users["registration_date"] = pd.to_datetime(
    users["registration_date"], errors="coerce"
)

enrollments["enrollment_date"] = pd.to_datetime(
    enrollments["enrollment_date"], errors="coerce"
)

enrollments["completion_date"] = pd.to_datetime(
    enrollments["completion_date"], errors="coerce"
)

activity["event_timestamp"] = pd.to_datetime(
    activity["event_timestamp"], errors="coerce"
)

print("========== DATA CLEANING STARTED ==========")

# 1. Remove exact duplicate activity records
before = len(activity)

activity = activity.drop_duplicates().copy()

print("Duplicate records removed:", before - len(activity))

# 2. Handle negative durations
negative_mask = activity["duration_seconds"] < 0

negative_records = activity[negative_mask].copy()

negative_records["issue"] = "Negative duration"

negative_records.to_csv(
    QUARANTINE_DIR / "negative_duration_records.csv",
    index=False
)

activity.loc[negative_mask, "duration_seconds"] = pd.NA

print("Negative durations handled:", len(negative_records))

# 3. Quarantine unknown event types
unknown_mask = (
    activity["event_type"].str.strip().str.lower()
    == "unknown_event"
)

unknown_events = activity[unknown_mask].copy()

activity = activity[~unknown_mask].copy()

unknown_events.to_csv(
    QUARANTINE_DIR / "unknown_events.csv",
    index=False
)

print("Unknown events quarantined:", len(unknown_events))

# 4. Identify enrollment date anomalies
registration_map = users.set_index("user_id")["registration_date"]

enrollment_registration = enrollments["user_id"].map(
    registration_map
)

enrollment_anomalies = enrollments[
    enrollments["enrollment_date"] < enrollment_registration
].copy()

enrollment_anomalies["issue"] = "Enrollment before registration"

# 5. Identify activity date anomalies
activity_registration = activity["user_id"].map(
    registration_map
)

activity_anomalies = activity[
    activity["event_timestamp"].dt.normalize()
    < activity_registration
].copy()

activity_anomalies["issue"] = "Activity before registration"

# Save date anomalies separately
date_anomalies = pd.concat(
    [enrollment_anomalies, activity_anomalies],
    ignore_index=True,
    sort=False
)

date_anomalies.to_csv(
    QUARANTINE_DIR / "date_anomalies.csv",
    index=False
)

# 6. Save cleaned datasets
users.to_csv(OUTPUT_DIR / "users_clean.csv", index=False)
courses.to_csv(OUTPUT_DIR / "courses_clean.csv", index=False)
enrollments.to_csv(
    OUTPUT_DIR / "enrollments_clean.csv", index=False
)
activity.to_csv(
    OUTPUT_DIR / "user_activity_clean.csv", index=False
)

# 7. Generate cleaning summary
summary = pd.DataFrame({
    "Dataset": [
        "Users",
        "Courses",
        "Enrollments",
        "User Activity"
    ],
    "Original Rows": [
        120,
        12,
        220,
        2210
    ],
    "Cleaned Rows": [
        len(users),
        len(courses),
        len(enrollments),
        len(activity)
    ]
})

summary.to_csv(
    OUTPUT_DIR / "cleaning_summary.csv",
    index=False
)

print("\n========== CLEANING SUMMARY ==========")
print(summary.to_string(index=False))

print("\nDate anomalies identified:",
      len(enrollment_anomalies) + len(activity_anomalies))

print("\nCleaned datasets saved successfully!")
print("Quarantine files saved successfully!")
