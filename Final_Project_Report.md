# Final Project Report
## ArchintX – AI-Powered User Behaviour Analytics System

**Project:** Advanced Data Analytics Internship  
**Technology:** Python, Pandas, NumPy, MySQL, SQL, Streamlit and Plotly  
**Author:** Archita Gupta

---

## 1. Executive Summary

This project develops an end-to-end user behaviour analytics system to understand how learners register, engage with the platform, discover courses, enroll, and complete learning activities.

The solution processes four CSV datasets, performs data cleaning and validation, stores the cleaned data in MySQL, calculates business KPIs using SQL and Python, and presents the findings through an interactive Streamlit dashboard.

The analysis focuses on user acquisition, engagement, retention, course performance, funnel activity and inactivity.

**Dataset note:** All records are synthetic training data. The findings do not represent actual ArchintX users or real business performance.

## 2. Dataset Overview

| Dataset | Raw Records | Cleaned Records |
|---|---:|---:|
| Users | 120 | 120 |
| Courses | 12 | 12 |
| Enrollments | 220 | 220 |
| User Activity | 2,210 | 2,192 |

The project uses four relational tables: `users`, `courses`, `enrollments` and `user_activity`.

## 3. Methodology

1. Loaded four CSV datasets using Python and Pandas.
2. Profiled missing values, duplicates, data types, invalid events and relationships.
3. Cleaned the datasets while preserving original raw files.
4. Quarantined unknown events, negative-duration records and date anomalies.
5. Designed and populated a MySQL relational database with primary keys, foreign keys and indexes.
6. Developed SQL queries for user activity, acquisition, course performance, retention, funnel and inactivity analysis.
7. Used Pandas and NumPy for monthly engagement, cohort analysis and segmentation.
8. Developed an interactive Streamlit dashboard using Plotly.

## 4. Data Quality and Cleaning

The cleaning process identified and handled:

- 10 duplicate activity records removed.
- 12 unique negative-duration records identified; their duration values were set to NULL and the original records were saved separately.
- 8 unknown event records quarantined.
- 1,085 pre-registration date anomalies identified and preserved for review.
- Missing course IDs retained where events were not course-specific.
- Missing completion dates retained for incomplete enrollments.

The final cleaned activity dataset contains 2,192 records.

Raw CSV files were preserved separately from cleaned datasets.

## 5. KPI Results and Business Question Analysis

### 5.1 User Acquisition

The dataset contains 120 registered users.

| Acquisition Source | Registrations | Verified Users | Verification Rate |
|---|---:|---:|---:|
| Organic Search | 23 | 19 | 82.61% |
| Direct | 21 | 18 | 85.71% |
| College Community | 21 | 19 | 90.48% |
| Referral | 20 | 17 | 85.00% |
| Instagram | 19 | 15 | 78.95% |
| LinkedIn | 16 | 14 | 87.50% |

Organic Search generated the highest number of registrations. College Community recorded the highest verification rate.

Enrollment rates were also compared by registration month and acquisition source. For example, in October, Direct recorded 4 enrollments among 10 registered users (40%), while Instagram recorded 1 among 8 (12.5%). These differences are descriptive and should be interpreted cautiously because cohort sizes are small.

### 5.2 Daily, Weekly and Monthly Engagement

DAU, WAU and MAU were calculated using distinct users with qualifying post-registration activity. The DAU/MAU ratio was defined as daily active users divided by calendar-month active users, multiplied by 100.

Monthly post-registration activity:

| Month | Activity Events | Active Users |
|---|---:|---:|
| August 2026 | 135 | 32 |
| September 2026 | 345 | 76 |
| October 2026 | 532 | 114 |
| November 2026* | 176 | 97 |

October recorded the highest activity among the observed months. November is partial data through November 8 and is not directly comparable with complete months.

### 5.3 Course Enrollment and Completion

There were 220 enrollments, of which 69 were completed.

**Overall course completion rate:**

69 / 220 × 100 = **31.36%**

Communication Skills recorded the highest enrollment count with 27 enrollments and 8 completions. Power BI also recorded 8 completions from 21 enrollments.

SQL Fundamentals had the highest course-level completion proportion: 6 out of 13 enrollments (46.15%). Django Development recorded 5 completions from 23 enrollments (21.74%).

These results describe the observed dataset; incomplete enrollments should not automatically be interpreted as permanent abandonment.

### 5.4 User Engagement by Segment

| User Segment | Users | Post-registration Events | Average Duration (Seconds) |
|---|---:|---:|---:|
| Student | 32 | 335 | 423.21 |
| Job Seeker | 26 | 267 | 378.98 |
| Fresher | 24 | 231 | 398.93 |
| Internship Seeker | 21 | 192 | 403.98 |
| Developer | 17 | 163 | 378.15 |

Students generated the highest number of post-registration events. All 17 Developer users were registered, but only 16 had qualifying post-registration activity.

### 5.5 City, Device and Platform Analysis

**City engagement:** Bengaluru recorded 233 post-registration events from 21 active users, the highest event count among the listed cities. Chennai recorded 138 events from 18 active users.

**Device engagement:**

| Device | Users | Active Users | Events |
|---|---:|---:|---:|
| Desktop | 40 | 40 | 444 |
| Mobile | 43 | 43 | 427 |
| Tablet | 37 | 36 | 317 |

**Platform engagement:**

| Platform | Events | Active Users | Average Duration (Seconds) |
|---|---:|---:|---:|
| iOS | 418 | 106 | 406.97 |
| Android | 391 | 107 | 405.09 |
| Web | 379 | 108 | 384.68 |

iOS recorded the highest event count, while Web recorded the highest number of distinct active users. User counts across platforms may overlap.

### 5.6 Funnel Analysis

Distinct users reaching each observed stage:

| Funnel Stage | Distinct Users |
|---|---:|
| Registration | 120 |
| Login | 99 |
| Course View | 92 |
| Enrollment | 104 |
| Lesson Start | 81 |
| Course Completion Event | 28 |

The registration-to-login difference is 21 users, while 7 fewer users reached course view than login.

The enrollment count exceeds the course-view count. Therefore, these figures represent distinct-user stage reach, not a strictly sequential conversion funnel. The 28 users with a course-completion activity event are also a different measurement from the 69 completed enrollment records.

### 5.7 Retention Analysis

Overall Week 1 retention was 76.67% (92 out of 120 users), using the days 7–13 return window.

Week 4 retention must account for cohort maturity:

| Cohort | Users | Week 1 Retention | Week 4 Retention |
|---|---:|---:|---:|
| August 2026 | 40 | 77.50% | 82.50% |
| September 2026 | 39 | 84.62% | 69.23% |
| October 2026 | 41 | 68.29% | Incomplete |

For the two cohorts with a fully observable Week 4 window, 60 of 79 users returned (75.95%). October Week 4 retention is not treated as zero because the observation window is incomplete.

Return activity is defined as at least one qualifying post-registration activity event in the relevant retention window.

### 5.8 Inactive Users

As of November 8, 2026:

- 8 users had no qualifying activity for at least 14 days.
- 1 user had no qualifying activity for at least 30 days.

These thresholds help identify users who may benefit from re-engagement.

### 5.9 Funnel and Course Drop-off

The enrollment dataset contains 151 incomplete enrollments out of 220 (68.64%). This indicates incomplete course records at the observation point, not confirmed permanent drop-off.

The funnel stage counts and course enrollment completion counts use different measurement units and event definitions. They should not be combined into a single sequential conversion calculation.

## 6. Key Insights

1. **Acquisition:** Organic Search generated the highest registrations (23 users), while College Community had the highest verification rate (90.48%).

2. **Engagement Growth:** October recorded 532 post-registration events from 114 active users, the highest among the observed months.

3. **Course Completion:** Overall enrollment completion was 31.36%, with 69 completed enrollments out of 220.

4. **Course Performance:** SQL Fundamentals had the highest course completion proportion (46.15%), while Communication Skills had the most enrollments (27).

5. **Segment Behaviour:** Students generated the highest post-registration activity, with 335 events from 32 users.

6. **Retention:** Week 1 retention was 76.67%. Among fully observed cohorts, Week 4 retention was 75.95%.

7. **Platform Usage:** iOS recorded 418 post-registration events, the highest among the three platforms.

8. **Geographic Engagement:** Bengaluru recorded the highest city-level activity with 233 events.

9. **Inactivity:** Eight users were inactive for at least 14 days, and one user was inactive for at least 30 days as of November 8, 2026.

10. **Data Quality:** The raw activity dataset contained duplicates, negative durations and unknown event types. Cleaning and quarantine steps improved analytical consistency while preserving an audit trail.

## 7. Business Recommendations

1. **Improve Course Completion:** Review course progress and completion patterns to identify where learners may need additional learning support, reminders or simpler course structures.

2. **Strengthen Retention:** Introduce onboarding guidance and timely engagement reminders to encourage users to return during the first month.

3. **Optimize Acquisition:** Investigate why verification and enrollment rates differ by acquisition source before prioritizing marketing channels.

4. **Re-engage Inactive Users:** Consider targeted reminders or course suggestions for users inactive for 14 or more days.

5. **Improve Course Experience:** Review course-level enrollment, progress and completion patterns to identify opportunities to improve learning content and engagement.

## 8. Dashboard Overview

The Streamlit dashboard contains four main sections:

- Overview
- User Analytics
- Course Analytics
- Engagement Analytics

It supports date, user-segment and course filters, interactive Plotly visualizations and drill-down tables.

Dashboard screenshots should be included with the final submission.

## 9. Limitations

- The dataset is synthetic and relatively small; results are not representative of actual platform performance.
- November activity is partial through November 8, 2026.
- Later cohort retention windows may be incomplete.
- Funnel stages are based on distinct-user stage reach and are not strictly sequential.
- Incomplete enrollments do not necessarily indicate permanent abandonment.
- Observational patterns do not establish causal relationships.
- Pre-registration date anomalies were flagged and excluded from post-registration engagement analysis.

## 10. Conclusion

The project demonstrates an end-to-end analytics workflow combining Python data processing, MySQL storage, SQL business analysis, cohort and segmentation analysis, and an interactive Streamlit dashboard.

The resulting solution provides a reproducible foundation for understanding user acquisition, engagement, retention and course performance. It also demonstrates how data quality validation and clearly defined KPIs support more reliable analytical decisions.

## 11. Individual Contribution

The project work included dataset understanding, Python-based ingestion and cleaning, data validation, MySQL schema design and loading, SQL KPI development, Python analytics, dashboard development, documentation and business recommendations.

**Author:** Archita Gupta  
**Project:** ArchintX – AI-Powered User Behaviour Analytics System  
**Internship Area:** Data Analytics

