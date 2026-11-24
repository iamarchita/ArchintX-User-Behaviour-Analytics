
import pandas as pd
import numpy as np
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load datasets
users = pd.read_csv(BASE_DIR / "users.csv")
courses = pd.read_csv(BASE_DIR / "courses.csv")
enrollments = pd.read_csv(BASE_DIR / "enrollments.csv")
activity = pd.read_csv(BASE_DIR / "user_activity.csv")

datasets = {
    "Users": users,
    "Courses": courses,
    "Enrollments": enrollments,
    "User Activity": activity
}

print("\n========== DATASET OVERVIEW ==========")

for name, df in datasets.items():
    print(f"\n{name}")
    print("-" * 40)
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print("Column Names:", list(df.columns))

print("\n========== DATA TYPES ==========")

for name, df in datasets.items():
    print(f"\n{name}")
    print(df.dtypes)

print("\n========== MISSING VALUES ==========")

for name, df in datasets.items():
    print(f"\n{name}")
    print(df.isnull().sum())

print("\n========== DUPLICATE RECORDS ==========")

for name, df in datasets.items():
    print(f"{name}: {df.duplicated().sum()}")

print("\n========== STATISTICAL SUMMARY ==========")

for name, df in datasets.items():
    print(f"\n{name}")
    print(df.describe(include="all").T)

print("\nEDA inspection completed successfully!")

print("\n========== DATA QUALITY VALIDATION ==========")

# 1. Duplicate activity records
print("\n1. DUPLICATE ACTIVITY RECORDS")
print(activity[activity.duplicated(keep=False)].sort_values("event_id"))

# 2. Duplicate event IDs
print("\n2. DUPLICATE EVENT IDs")
print(activity[activity["event_id"].duplicated(keep=False)].sort_values("event_id"))

# 3. Negative durations
print("\n3. NEGATIVE DURATIONS")
print(activity[activity["duration_seconds"] < 0])

# 4. Event type distribution
print("\n4. EVENT TYPE DISTRIBUTION")
print(activity["event_type"].value_counts(dropna=False))

# 5. Enrollment status distribution
print("\n5. ENROLLMENT STATUS DISTRIBUTION")
print(enrollments["enrollment_status"].value_counts(dropna=False))

# 6. Progress validation
print("\n6. INVALID PROGRESS VALUES")
print(enrollments[
    (enrollments["progress_percent"] < 0) |
    (enrollments["progress_percent"] > 100)
])

# 7. Invalid foreign key references
print("\n7. INVALID USER REFERENCES")
print("Enrollments:", 
      (~enrollments["user_id"].isin(users["user_id"])).sum())
print("Activity:",
      (~activity["user_id"].isin(users["user_id"])).sum())

print("\n8. INVALID COURSE REFERENCES")
print("Enrollments:",
      (~enrollments["course_id"].isin(courses["course_id"])).sum())
print("Activity:",
      (~activity["course_id"].dropna().isin(courses["course_id"])).sum())

# 9. Date validation
print("\n9. DATE VALIDATION")

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

print("Invalid registration dates:",
      users["registration_date"].isna().sum())

print("Invalid enrollment dates:",
      enrollments["enrollment_date"].isna().sum())

print("Invalid completion dates:",
      enrollments["completion_date"].isna().sum())

print("Invalid activity timestamps:",
      activity["event_timestamp"].isna().sum())

# 10. Enrollment before registration
registration_map = users.set_index("user_id")["registration_date"]

enrollment_registration = enrollments["user_id"].map(registration_map)

print("\nEnrollments before registration:",
      (enrollments["enrollment_date"] < enrollment_registration).sum())

# 11. Activity before registration
activity_registration = activity["user_id"].map(registration_map)

print("Activities before registration:",
      (activity["event_timestamp"].dt.normalize() <
       activity_registration).sum())

print("\nDetailed validation completed!")
