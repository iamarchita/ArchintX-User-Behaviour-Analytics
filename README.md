# ArchintX – AI-Powered User Behaviour Analytics System

## Project Overview
An end-to-end data analytics project that analyzes user behaviour, engagement, retention, course performance and acquisition patterns using Python, MySQL and Streamlit.

## Objectives
- Analyze user registrations and acquisition sources.
- Measure DAU, WAU, MAU and retention.
- Evaluate course enrollment and completion.
- Identify user engagement and inactivity patterns.
- Generate actionable business insights and recommendations.

## Technology Stack
- Python
- Pandas and NumPy
- MySQL
- SQL
- Streamlit
- Plotly
- Matplotlib and Seaborn

## Project Structure

```text
ArchintX_User_Behaviour_Analytics/
│
├── data/
│   ├── cleaned/
│   ├── quarantine/
│   └── analytics/
│
├── reports/
│   ├── Database_Setup.md
│   ├── Data_Quality_Report.md
│   ├── ER_Diagram.md
│   ├── Insights_and_Recommendations.md
│   └── KPI_Definitions.md
│
├── scripts/
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
└── user_activity.csv
```

## Setup and Execution

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure MySQL
- Start MySQL Server.
- Configure database credentials in the project connection settings.
- Execute `sql/03_create_tables.sql`.
- Load the cleaned data using `scripts/03_load_mysql.py`.

Refer to `reports/Database_Setup.md` for detailed instructions.

### 3. Run Analytics

```bash
python scripts/04_python_analytics.py
```

### 4. Launch Dashboard

```bash
streamlit run app.py
```

## Dashboard Modules
- Overview
- User Analytics
- Course Analytics
- Engagement Analytics

The dashboard provides interactive date, user segment and course filters with visualizations and detailed tables.

## Reports and Documentation
The `reports/` directory contains the database setup guide, ER diagram, data quality report, KPI definitions, and business insights with recommendations.

## Data Note
The project uses synthetic datasets for demonstration and analytical purposes. Raw datasets are preserved separately from cleaned data.

## Author
Archita Gupta

## Project Context
Developed as part of the ArchintX Data Analytics Internship.
