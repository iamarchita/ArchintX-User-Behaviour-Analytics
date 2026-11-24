# KPI Reconciliation and Validation

## Objective
To verify that key analytics metrics calculated using SQL and Python are consistent when the same dataset, filters, and KPI definitions are applied.

## SQL vs Python Validation

The following metrics were cross-checked between SQL queries and Python analytics:

| Metric | SQL Result | Python Result | Status |
|---|---:|---:|---|
| Post-registration activity events | 1,188 | 1,188 | Matched |
| Distinct active users | 119 | 119 | Matched |
| Average activity duration | 399.25 sec | 399.25 sec | Matched |

## Validation Rules

- Pre-registration activity records were excluded from engagement calculations.
- Duplicate activity records were removed before analysis.
- Negative activity durations were converted to NULL.
- The same date filters and metric definitions were used for comparison.
- Average duration was calculated using valid duration values.

## Conclusion

The selected engagement metrics produced consistent results in SQL and Python. This confirms that the two analytical approaches are aligned for the validated metrics.

Note: The validation above covers the listed metrics and does not imply that every KPI in the project was independently reconciled.