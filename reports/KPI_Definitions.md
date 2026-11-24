# KPI Definitions and Formulas

## Project
ArchintX – AI-Powered User Behaviour Analytics

The following KPIs are calculated using cleaned data and validated through SQL and Python analytics.

| KPI | Definition / Calculation |
|---|---|
| Registrations | Count of distinct registered users within the selected period |
| DAU | Distinct users with qualifying activity on a given day |
| WAU | Distinct users with qualifying activity during a week |
| MAU | Distinct users with qualifying activity during a calendar month |
| DAU/MAU Ratio | (Daily Active Users / Monthly Active Users) × 100 |
| Course Enrollment Rate | (Users enrolled / Eligible registered users) × 100 |
| Course Completion Rate | (Completed enrollments / Total eligible enrollments) × 100 |
| Week 1 Retention | Users returning during days 7–13 after registration / Eligible registered users × 100 |
| Week 4 Retention | Users returning during days 28–34 after registration / Eligible registered users × 100 |
| Inactive Users | Users with no qualifying activity in the last 14 or 30 days |
| Average Engagement Duration | Total valid activity duration / Valid duration records |

## Activity Definition

Qualifying activity includes valid, cleaned user activity events occurring on or after the user's registration date.

Pre-registration activity is excluded from post-registration engagement analysis.

## Funnel Stages

The distinct-user funnel tracks:

1. Registration
2. Login
3. Course view
4. Enrollment
5. Lesson start
6. Course completion

Stage counts represent distinct users reaching each stage. They are not necessarily sequential conversions because users may perform actions in different orders.

## Completion Rate

- Completed enrollments: 69
- Total enrollments: 220
- Completion rate: 31.36%

Incomplete enrollments are not automatically treated as permanent drop-offs.

## Retention Windows

- Week 1: Days 7–13 after registration.
- Week 4: Days 28–34 after registration.

Retention is based on at least one qualifying return activity event within the respective window.

## Important Notes

- November 2026 activity data is partial, available only through November 8.
- Later cohort retention values are treated as unavailable when the observation window is incomplete, not as zero.
- KPI values are calculated from source data rather than hardcoded.
- Date ranges and filters affect KPI calculations.