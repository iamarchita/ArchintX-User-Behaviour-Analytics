# ArchintX – AI-Powered User Behaviour Analytics System

## Project Overview

An end-to-end data analytics project developed as part of the **ArchintX Advanced Data Analytics Internship**.

The project analyzes learner behaviour across registrations, acquisition sources, course discovery, enrollments, learning activity, engagement, retention, and course completion.

It transforms raw activity data into meaningful KPIs, business insights, and actionable recommendations through Python, MySQL, SQL, and an interactive Streamlit dashboard.

**GitHub Repository:** [ArchintX – User Behaviour Analytics](https://github.com/iamarchita/ArchintX-User-Behaviour-Analytics)

## Project Objectives

- Analyze user registrations and acquisition sources.
- Measure Daily, Weekly, and Monthly Active Users (DAU, WAU, MAU).
- Evaluate user retention and engagement patterns.
- Analyze course enrollment and completion rates.
- Identify inactive users and funnel drop-off points.
- Compare engagement across user segments, devices, cities, and platforms.
- Generate evidence-based business insights and recommendations.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and analytics |
| Pandas & NumPy | Data cleaning, manipulation, and analysis |
| MySQL | Relational database management |
| SQL | KPI calculations and business analysis |
| Streamlit | Interactive dashboard |
| Plotly | Interactive data visualizations |
| Matplotlib & Seaborn | Exploratory data analysis and charts |
| Git & GitHub | Version control and project hosting |

## Project Structure

```text
ArchintX_User_Behaviour_Analytics/
│
├── data/
│   ├── analytics/
│   │   ├── charts/
│   │   ├── cohort_retention.csv
│   │   └── monthly_engagement.csv
│   │
│   ├── cleaned/
│   │   ├── cleaning_summary.csv
│   │   ├── courses_clean.csv
│   │   ├── enrollments_clean.csv
│   │   ├── user_activity_clean.csv
│   │   └── users_clean.csv
│   │
│   └── quarantine/
│       ├── date_anomalies.csv
│       ├── negative_duration_records.csv
│       └── unknown_events.csv
│
├── reports/
│   ├── screenshots/
│   ├── Data_Quality_Report.md
│   ├── Database_Setup.md
│   ├── ER_Diagram.md
│   ├── Insights_and_Recommendations.md
│   ├── KPI_Definitions.md
│   ├── KPI_Validation.md
│   └── Test_Cases.md
│
├── scripts/
│   ├── 01_eda.py
│   ├── 02_data_cleaning.py
│   ├── 03_load_mysql.py
│   └── 04_python_analytics.py
│
├── sql/
│   ├── 01_active_user_metrics.sql
│   ├── 01_sql_verification.sql
│   ├── 02_business_analysis.sql
│   └── 03_create_tables.sql
│
├── app.py
├── users.csv
├── courses.csv
├── enrollments.csv
├── user_activity.csv
├── Final_Project_Report.md
├── requirements.txt
├── README.md
└── .gitignore
```

## Project Workflow

1. **Data Ingestion:** Load and validate four raw CSV datasets.
2. **Exploratory Data Analysis:** Examine data distributions, patterns, and quality issues.
3. **Data Cleaning:** Handle duplicates, negative durations, invalid events, and data inconsistencies.
4. **Database Management:** Create relational MySQL tables and load cleaned datasets.
5. **SQL Analysis:** Calculate engagement, retention, funnel, enrollment, and completion metrics.
6. **Python Analytics:** Perform cohort analysis, segmentation, and KPI calculations.
7. **Dashboard Development:** Build an interactive Streamlit dashboard.
8. **Validation:** Reconcile SQL and Python KPIs and document edge-case tests.
9. **Business Insights:** Identify patterns and develop actionable recommendations.

## Setup and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/iamarchita/ArchintX-User-Behaviour-Analytics.git

cd ArchintX-User-Behaviour-Analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Exploratory Data Analysis

```bash
python scripts/01_eda.py
```

### 5. Perform Data Cleaning

```bash
python scripts/02_data_cleaning.py
```

### 6. Configure MySQL Database

- Start the MySQL server.
- Configure database credentials according to the database setup instructions.
- Execute the SQL schema creation script.
- Load the cleaned datasets into MySQL.

Refer to [Database Setup Guide](reports/Database_Setup.md) for detailed instructions.

### 7. Run Python Analytics

```bash
python scripts/04_python_analytics.py
```

### 8. Launch the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## Dashboard Modules

The interactive dashboard includes four major modules:

- **Overview:** Key performance indicators and overall platform activity.
- **User Analytics:** Registration trends, user segments, and acquisition analysis.
- **Course Analytics:** Course enrollment, completion, and performance.
- **Engagement Analytics:** Active users, retention, activity trends, and engagement patterns.

The dashboard provides interactive date, user segment, and course filters along with charts and detailed analytical tables.

## Reports and Documentation

Detailed project documentation is available in the `reports/` directory.

| Document | Description |
|---|---|
| [Final Project Report](Final_Project_Report.md) | Complete project findings and analysis |
| [Data Quality Report](reports/Data_Quality_Report.md) | Data quality issues and cleaning summary |
| [Database Setup](reports/Database_Setup.md) | Database configuration and execution |
| [ER Diagram](reports/ER_Diagram.md) | Relational database structure |
| [KPI Definitions](reports/KPI_Definitions.md) | KPI formulas and calculation definitions |
| [KPI Validation](reports/KPI_Validation.md) | SQL and Python metric reconciliation |
| [Test Cases](reports/Test_Cases.md) | Validation and edge-case testing |
| [Insights & Recommendations](reports/Insights_and_Recommendations.md) | Analytical findings and business recommendations |

## Dataset Information

The project includes four synthetic CSV datasets:

| Dataset | Records | Description |
|---|---:|---|
| users.csv | 120 | Learner information |
| courses.csv | 12 | Course catalogue |
| enrollments.csv | 220 | User-course enrollment and progress |
| user_activity.csv | 2,210 | Timestamped platform activity |

Raw datasets are preserved separately from cleaned datasets. Invalid or anomalous records are documented in quarantine files.

## Key Deliverables

- End-to-end Python data analytics pipeline.
- MySQL relational database and SQL KPI queries.
- Interactive Streamlit dashboard.
- Data quality and validation reports.
- Cohort retention and engagement analysis.
- Final project report with business insights and recommendations.
