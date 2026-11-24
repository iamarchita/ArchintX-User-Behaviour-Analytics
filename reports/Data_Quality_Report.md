# Data Quality Report

## Project
ArchintX – AI-Powered User Behaviour Analytics

## 1. Dataset Overview

| Dataset | Raw Records |
|---|---:|
| Users | 120 |
| Courses | 12 |
| Enrollments | 220 |
| User Activity | 2,210 |

## 2. Data Cleaning Summary

- Removed 10 duplicate activity records.
- Identified 12 unique negative-duration events after duplicate removal; their duration values were set to NULL.
- Quarantined 8 records containing unknown event types.
- Validated user and course references; no invalid foreign-key references were found.
- Preserved missing course IDs where activity events were not course-related.
- Preserved missing completion dates for incomplete enrollments.
- Identified pre-registration date anomalies and flagged them for analysis instead of deleting the records.
- Original raw CSV files were kept unchanged.

## 3. Cleaned Dataset Summary

| Dataset | Cleaned Records |
|---|---:|
| Users | 120 |
| Courses | 12 |
| Enrollments | 220 |
| User Activity | 2,192 |

## 4. Data Quality Observations

- 151 enrollments had missing completion dates, which is expected for incomplete enrollments.
- 753 activity records had missing course IDs, mainly because not all events are course-specific.
- 1085 pre-registration date anomalies were identified in the date-anomaly analysis output.
- No invalid user or course references were found.

## 5. Data Handling Approach

The cleaning process used Python and Pandas. Duplicate removal, invalid event quarantine, duration validation and date-anomaly checks were performed.

Cleaned data was stored separately from raw data to preserve data integrity.

## 6. Conclusion

The cleaning process improved data consistency while preserving valid records and retaining important data-quality exceptions for further analysis.