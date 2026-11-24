# Data Quality and Edge-Case Test Cases

## Objective
To verify that the data cleaning and analytics pipeline handles duplicate, invalid, missing, and incomplete records appropriately.

## Test Cases

| Test Case | Input / Issue | Expected Handling | Actual Result |
|---|---|---|---|
| Duplicate activity records | 10 duplicate rows | Remove duplicate records | 10 duplicates removed |
| Negative durations | Negative activity durations | Replace invalid durations with NULL | 12 unique records handled |
| Unknown event types | 8 unrecognized events | Quarantine invalid events | 8 records quarantined |
| Missing course IDs | Course ID missing in some activity records | Preserve valid non-course events | Records retained where appropriate |
| Invalid foreign keys | Invalid user/course references | Identify invalid references | 0 invalid references found |
| Incomplete enrollments | Missing completion dates | Preserve incomplete enrollment records | 151 records retained |
| Users without activity | No post-registration activity | Identify users without qualifying activity | User U0036 identified |
| Pre-registration activity | Events before user registration | Exclude from engagement analytics | Excluded from Python analytics |
| Incomplete retention cohorts | Insufficient observation period | Avoid treating unavailable retention as zero | October W4 interpreted as incomplete |

## Data Quality Summary

- Raw activity records: 2,210
- Duplicate records removed: 10
- Unknown events quarantined: 8
- Negative-duration records handled: 12
- Cleaned activity records: 2,192
- Date anomalies flagged: 1,085

## Conclusion

The pipeline handles major data quality issues without unnecessarily deleting valid records. Invalid and anomalous records are handled separately, while incomplete business records are preserved where appropriate.

Note: These results document the data checks and handling performed during the project. They should not be interpreted as evidence of a separate automated unit-testing framework.