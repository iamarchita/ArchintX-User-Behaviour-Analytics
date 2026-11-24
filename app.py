
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="User Behaviour Analytics",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
ANALYTICS_DIR = BASE_DIR / "data" / "analytics"

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    users = pd.read_csv(DATA_DIR / "users_clean.csv")
    courses = pd.read_csv(DATA_DIR / "courses_clean.csv")
    enrollments = pd.read_csv(DATA_DIR / "enrollments_clean.csv")
    activity = pd.read_csv(DATA_DIR / "user_activity_clean.csv")
    cohort = pd.read_csv(ANALYTICS_DIR / "cohort_retention.csv")

    users["registration_date"] = pd.to_datetime(users["registration_date"])
    enrollments["enrollment_date"] = pd.to_datetime(enrollments["enrollment_date"])
    activity["event_timestamp"] = pd.to_datetime(activity["event_timestamp"])

# Exclude activity before user registration
    activity = activity.merge(
    users[["user_id", "registration_date"]],
    on="user_id",
    how="left"
)

    activity = activity[
    activity["event_timestamp"] >= activity["registration_date"]
].copy()

    activity = activity.drop(columns=["registration_date"])

    activity["duration_seconds"] = pd.to_numeric(
    activity["duration_seconds"], errors="coerce"
)

    return users, courses, enrollments, activity, cohort


try:
    users, courses, enrollments, activity, cohort = load_data()
except Exception as e:
    st.error(f"Unable to load project data: {e}")
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("User Behaviour Analytics")
st.sidebar.caption("Learning Platform Intelligence Dashboard")

page = st.sidebar.radio(
    "Dashboard Sections",
    [
        "Overview",
        "User Analytics",
        "Course Analytics",
        "Engagement Analytics"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Data range: August – November 2026")

# ---------------- HEADER ----------------
st.title("User Behaviour Analytics")
st.caption("Analytics dashboard for user engagement, learning performance and retention.")


# ---------------- GLOBAL FILTERS ----------------
st.sidebar.subheader("Dashboard Filters")

min_date = min(
    activity["event_timestamp"].min().date(),
    enrollments["enrollment_date"].min().date(),
    users["registration_date"].min().date()
)

max_date = max(
    activity["event_timestamp"].max().date(),
    enrollments["enrollment_date"].max().date(),
    users["registration_date"].max().date()
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

segment_options = sorted(
    users["user_segment"].dropna().astype(str).str.strip().unique()
)

selected_segments = st.sidebar.multiselect(
    "User Segment",
    options=segment_options,
    default=segment_options
)
selected_courses = st.sidebar.multiselect(
    "Course",
    options=sorted(courses["course_name"].dropna().unique()),
    default=sorted(courses["course_name"].dropna().unique())
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date


# ---------------- APPLY FILTERS ----------------

# Identify users belonging to selected segments
segment_user_ids = users.loc[
    users["user_segment"].astype(str).str.strip().isin(selected_segments),
    "user_id"
]

# Filter users by registration date and segment
filtered_users = users[
    (users["registration_date"].dt.date >= start_date) &
    (users["registration_date"].dt.date <= end_date) &
    (users["user_id"].isin(segment_user_ids))
].copy()

# Filter enrollments by user, date and course
filtered_enrollments = enrollments[
    (enrollments["user_id"].isin(segment_user_ids)) &
    (enrollments["enrollment_date"].dt.date >= start_date) &
    (enrollments["enrollment_date"].dt.date <= end_date)
].merge(
    courses[["course_id", "course_name"]],
    on="course_id",
    how="left"
)

filtered_enrollments = filtered_enrollments[
    filtered_enrollments["course_name"].isin(selected_courses)
].copy()

# Filter activity by user and activity date
filtered_activity = activity[
    (activity["user_id"].isin(segment_user_ids)) &
    (activity["event_timestamp"].dt.date >= start_date) &
    (activity["event_timestamp"].dt.date <= end_date)
].copy()

# Apply course filter while retaining non-course events
selected_course_ids = courses.loc[
    courses["course_name"].isin(selected_courses),
    "course_id"
]

filtered_activity = filtered_activity[
    filtered_activity["course_id"].isna() |
    filtered_activity["course_id"].isin(selected_course_ids)
].copy()




# ---------------- OVERVIEW ----------------
if page == "Overview":

    total_users = filtered_users["user_id"].nunique()

    verified_users = filtered_users.loc[
        filtered_users["is_verified"].astype(str).str.lower().isin(
            ["true", "1"]
        ),
        "user_id"
    ].nunique()

    total_enrollments = len(filtered_enrollments)

    completed = filtered_enrollments[
        filtered_enrollments["completion_date"].notna()
    ].shape[0]

    completion_rate = (
        completed / total_enrollments * 100
        if total_enrollments else 0
    )

    active_users = filtered_activity["user_id"].nunique()
    total_events = len(filtered_activity)

    selected_course_count = filtered_enrollments[
        "course_id"
    ].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Registered Users", f"{total_users:,}")
    c2.metric("Verified Users", f"{verified_users:,}")
    c3.metric("Total Enrollments", f"{total_enrollments:,}")
    c4.metric("Completion Rate", f"{completion_rate:.2f}%")

    c5, c6, c7 = st.columns(3)

    c5.metric("Active Users", f"{active_users:,}")
    c6.metric("Activity Events", f"{total_events:,}")
    c7.metric("Courses with Enrollments", f"{selected_course_count:,}")

    st.divider()

    left, right = st.columns(2)

    with left:
        segment_data = filtered_users[
            "user_segment"
        ].value_counts().reset_index()

        segment_data.columns = ["User Segment", "Users"]

        fig = px.pie(
            segment_data,
            names="User Segment",
            values="Users",
            hole=0.45,
            title="User Segment Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        monthly = filtered_activity.copy()

        monthly["Month"] = monthly[
            "event_timestamp"
        ].dt.strftime("%Y-%m")

        monthly_data = monthly.groupby("Month")[
            "user_id"
        ].nunique().reset_index()

        monthly_data.columns = ["Month", "Active Users"]

        fig = px.line(
            monthly_data,
            x="Month",
            y="Active Users",
            markers=True,
            title="Monthly Active Users"
        )

        st.plotly_chart(fig, use_container_width=True)




# ---------------- USER ANALYTICS ----------------
elif page == "User Analytics":

    st.subheader("User Analytics")
    st.caption("User segmentation, acquisition and registration insights")

    # Prepare filtered user data
    user_data = filtered_users.copy()

    if user_data.empty:
        st.info("No users available for the selected filters.")

    else:
        # Standardize verification values
        user_data["verified_flag"] = (
            user_data["is_verified"]
            .astype(str)
            .str.lower()
            .isin(["true", "1", "yes"])
        )

        # ---------------- USER KPIs ----------------
        total_users = user_data["user_id"].nunique()
        verified_users = user_data.loc[
            user_data["verified_flag"], "user_id"
        ].nunique()

        verification_rate = (
            verified_users / total_users * 100
            if total_users else 0
        )

        total_cities = user_data["city"].nunique()

        k1, k2, k3 = st.columns(3)

        k1.metric("Total Users", f"{total_users:,}")
        k2.metric("Verified Users", f"{verified_users:,}")
        k3.metric("Verification Rate", f"{verification_rate:.2f}%")

        st.divider()

        # ---------------- SEGMENT ANALYSIS ----------------
        col1, col2 = st.columns(2)

        with col1:
            segment_data = (
                user_data.groupby("user_segment")["user_id"]
                .nunique()
                .reset_index(name="Users")
            )

            fig = px.bar(
                segment_data.sort_values("Users", ascending=False),
                x="user_segment",
                y="Users",
                text="Users",
                title="Users by Segment"
            )

            st.plotly_chart(fig, use_container_width=True)

        # ---------------- ACQUISITION ANALYSIS ----------------
        with col2:
            source_data = (
                user_data.groupby("acquisition_source")
                .agg(
                    total_users=("user_id", "nunique"),
                    verified_users=("verified_flag", "sum")
                )
                .reset_index()
            )

            source_data["verification_rate"] = (
                source_data["verified_users"]
                / source_data["total_users"] * 100
            ).round(2)

            fig = px.bar(
                source_data.sort_values(
                    "verification_rate", ascending=False
                ),
                x="acquisition_source",
                y="verification_rate",
                text="verification_rate",
                title="Verification Rate by Acquisition Source"
            )

            fig.update_xaxes(tickangle=-30)
            st.plotly_chart(fig, use_container_width=True)

        # ---------------- REGISTRATION TREND ----------------
        st.subheader("User Registration Trend")

        registration = user_data.copy()

        registration["Month"] = (
            registration["registration_date"].dt.strftime("%Y-%m")
        )

        registration_data = (
            registration.groupby("Month")["user_id"]
            .nunique()
            .reset_index(name="New Users")
        )

        fig = px.line(
            registration_data,
            x="Month",
            y="New Users",
            markers=True,
            text="New Users",
            title="Monthly New User Registrations"
        )

        fig.update_xaxes(type="category")
        st.plotly_chart(fig, use_container_width=True)

        # ---------------- DEVICE ANALYSIS ----------------
        st.subheader("User Device Distribution")

        device_data = (
            user_data.groupby("device_type")["user_id"]
            .nunique()
            .reset_index(name="Users")
        )

        fig = px.pie(
            device_data,
            names="device_type",
            values="Users",
            hole=0.45,
            title="User Device Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------- USER DRILL-DOWN ----------------
        st.subheader("User Details")

        user_details = user_data[
            [
                "user_id",
                "user_segment",
                "city",
                "registration_date",
                "acquisition_source",
                "device_type",
                "verified_flag"
            ]
        ].copy()

        user_details = user_details.rename(
            columns={"verified_flag": "is_verified"}
        )

        user_details["is_verified"] = (
            user_details["is_verified"].map(
                {True: "Yes", False: "No"}
            )
        )

        st.dataframe(
            user_details.sort_values(
                "registration_date", ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing {len(user_details)} users matching the selected filters."
        )


# ---------------- COURSE ANALYTICS ----------------
elif page == "Course Analytics":

    st.subheader("Course Performance")

    course_data = filtered_enrollments.copy()

    performance = course_data.groupby("course_name").agg(
        enrollments=("enrollment_id", "count"),
        completed=("enrollment_status",
                   lambda x: (x == "Completed").sum()),
        incomplete=("enrollment_status",
                    lambda x: (x != "Completed").sum()),
        avg_progress=("progress_percent", "mean")
    ).reset_index()

    performance["avg_progress"] = performance["avg_progress"].round(2)

    performance["dropoff_rate"] = (
        performance["incomplete"] /
        performance["enrollments"] * 100
    ).round(2)

    if performance.empty:
        st.info("No course data available for selected filters.")

    else:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                performance.sort_values(
                    "enrollments", ascending=False
                ),
                x="course_name",
                y="enrollments",
                title="Course-wise Enrollments",
                text="enrollments"
            )
            fig.update_xaxes(tickangle=-35)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                performance.sort_values(
                    "avg_progress", ascending=False
                ),
                x="course_name",
                y="avg_progress",
                title="Average Course Progress (%)",
                text="avg_progress"
            )
            fig.update_xaxes(tickangle=-35)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Course Performance Details")

        st.dataframe(
            performance.sort_values(
                "enrollments", ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )



# ---------------- ENGAGEMENT ANALYTICS ----------------
elif page == "Engagement Analytics":

    st.subheader("User Engagement & Retention")
    st.caption(
        "Engagement trends, platform usage, user activity and cohort retention"
    )

    engagement = filtered_activity.copy()

    if engagement.empty:

        st.info("No activity available for the selected filters.")

    else:

        # ---------------- ENGAGEMENT KPIs ----------------
        total_events = len(engagement)
        active_users = engagement["user_id"].nunique()

        avg_duration = engagement["duration_seconds"].mean()
        avg_duration = 0 if pd.isna(avg_duration) else avg_duration

        total_platforms = engagement["platform"].nunique()

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("Active Users", f"{active_users:,}")
        k2.metric("Total Events", f"{total_events:,}")
        k3.metric("Avg Event Duration", f"{avg_duration:.2f} sec")
        k4.metric("Platforms Used", f"{total_platforms:,}")

        st.divider()

        # ---------------- DAILY ACTIVE USERS ----------------
        st.subheader("Daily Active Users")

        daily_data = (
            engagement.groupby(
                engagement["event_timestamp"].dt.date
            )["user_id"]
            .nunique()
            .reset_index(name="DAU")
        )

        daily_data.columns = ["Date", "DAU"]

        fig = px.line(
            daily_data,
            x="Date",
            y="DAU",
            markers=True,
            title="Daily Active Users Trend"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------- WEEKLY ACTIVE USERS ----------------
        st.subheader("Weekly Active Users")

        weekly = engagement.copy()

        weekly["Week Start"] = (
            weekly["event_timestamp"]
            .dt.to_period("W-SUN")
            .apply(lambda x: x.start_time.date())
        )

        weekly_data = (
            weekly.groupby("Week Start")["user_id"]
            .nunique()
            .reset_index(name="WAU")
        )

        fig = px.bar(
            weekly_data,
            x="Week Start",
            y="WAU",
            text="WAU",
            title="Weekly Active Users Trend"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------- MONTHLY ACTIVE USERS ----------------
        st.subheader("Monthly Engagement")

        monthly = engagement.copy()

        monthly["Month"] = (
            monthly["event_timestamp"].dt.strftime("%Y-%m")
        )

        monthly_data = monthly.groupby("Month").agg(
            total_events=("event_id", "count"),
            active_users=("user_id", "nunique"),
            avg_duration=("duration_seconds", "mean")
        ).reset_index()

        monthly_data["avg_duration"] = (
            monthly_data["avg_duration"].round(2)
        )

        col1, col2 = st.columns(2)

        with col1:

            fig = px.line(
                monthly_data,
                x="Month",
                y="total_events",
                markers=True,
                title="Monthly Activity Events"
            )

            fig.update_xaxes(type="category")
            st.plotly_chart(fig, use_container_width=True)

        with col2:

            fig = px.line(
                monthly_data,
                x="Month",
                y="active_users",
                markers=True,
                title="Monthly Active Users (MAU)"
            )

            fig.update_xaxes(type="category")
            st.plotly_chart(fig, use_container_width=True)

        # ---------------- DAU / MAU RATIO ----------------
        st.subheader("Daily Engagement Ratio")

        daily_data["Month"] = pd.to_datetime(
            daily_data["Date"]
        ).dt.strftime("%Y-%m")

        monthly_active = monthly_data[
            ["Month", "active_users"]
        ].rename(
            columns={"active_users": "MAU"}
        )

        ratio_data = daily_data.merge(
            monthly_active,
            on="Month",
            how="left"
        )

        ratio_data["DAU_MAU_Ratio"] = (
            ratio_data["DAU"] /
            ratio_data["MAU"] * 100
        ).round(2)

        fig = px.line(
            ratio_data,
            x="Date",
            y="DAU_MAU_Ratio",
            markers=True,
            title="DAU / MAU Ratio (%)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------- PLATFORM DISTRIBUTION ----------------
        st.subheader("Platform Usage")

        col1, col2 = st.columns(2)

        with col1:

            platform_data = (
                engagement["platform"]
                .value_counts()
                .reset_index()
            )

            platform_data.columns = ["Platform", "Events"]

            fig = px.pie(
                platform_data,
                names="Platform",
                values="Events",
                hole=0.4,
                title="Platform Usage Distribution"
            )

            st.plotly_chart(fig, use_container_width=True)

        # ---------------- EVENT DISTRIBUTION ----------------
        with col2:

            event_data = (
                engagement["event_type"]
                .value_counts()
                .reset_index()
            )

            event_data.columns = ["Event Type", "Events"]

            fig = px.bar(
                event_data.sort_values(
                    "Events", ascending=False
                ),
                x="Event Type",
                y="Events",
                text="Events",
                title="User Event Distribution"
            )

            fig.update_xaxes(tickangle=-35)

            st.plotly_chart(fig, use_container_width=True)

        # ---------------- COHORT RETENTION ----------------
        st.subheader("Cohort Retention Analysis")

        cohort_users = users[
            (users["user_segment"].astype(str).str.strip().isin(
                selected_segments
            )) &
            (users["registration_date"].dt.date >= start_date) &
            (users["registration_date"].dt.date <= end_date)
        ].copy()

        if cohort_users.empty:

            st.info("No registration cohorts available for these filters.")

        else:

            cohort_users["cohort_month"] = (
                cohort_users["registration_date"].dt.to_period("M")
            )

            cohort_activity = filtered_activity.merge(
                cohort_users[
                    ["user_id", "cohort_month"]
                ],
                on="user_id",
                how="inner"
            )

            cohort_activity["activity_month"] = (
                cohort_activity["event_timestamp"].dt.to_period("M")
            )

            cohort_activity["period_number"] = (
                (cohort_activity["activity_month"].dt.year -
                 cohort_activity["cohort_month"].dt.year) * 12
                +
                (cohort_activity["activity_month"].dt.month -
                 cohort_activity["cohort_month"].dt.month)
            )

            cohort_sizes = (
                cohort_users.groupby("cohort_month")["user_id"]
                .nunique()
            )

            cohort_rows = []

            for cohort_month, cohort_size in cohort_sizes.items():

                max_period = (
                    (end_date.year - cohort_month.year) * 12
                    + end_date.month - cohort_month.month
                )

                row = {
                    "Cohort": str(cohort_month)
                }

                cohort_user_ids = set(
                    cohort_users.loc[
                        cohort_users["cohort_month"] == cohort_month,
                        "user_id"
                    ]
                )

                for period in range(max_period + 1):

                    active_count = (
                        cohort_activity[
                            (cohort_activity["cohort_month"] == cohort_month) &
                            (cohort_activity["period_number"] == period)
                        ]["user_id"].nunique()
                    )

                    row[f"Month_{period}"] = round(
                        active_count / cohort_size * 100, 2
                    )

                cohort_rows.append(row)

            cohort_display = pd.DataFrame(cohort_rows).set_index("Cohort")

            fig = px.imshow(
                cohort_display,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Blues",
                labels={
                    "x": "Cohort Period",
                    "y": "Registration Cohort",
                    "color": "Retention (%)"
                },
                title="Monthly Cohort Retention Heatmap"
            )

            fig.update_yaxes(type="category")
            fig.update_xaxes(type="category")

            st.plotly_chart(fig, use_container_width=True)

        # ---------------- ENGAGEMENT DRILL-DOWN ----------------
        st.subheader("User Engagement Details")

        user_engagement = engagement.groupby("user_id").agg(
            total_events=("event_id", "count"),
            last_activity=("event_timestamp", "max"),
            avg_duration=("duration_seconds", "mean"),
            platforms_used=("platform", "nunique")
        ).reset_index()

        user_engagement["avg_duration"] = (
            user_engagement["avg_duration"].round(2)
        )

        user_engagement = user_engagement.sort_values(
            "total_events",
            ascending=False
        )

        st.dataframe(
            user_engagement,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing engagement details for {len(user_engagement)} users."
        )


st.sidebar.divider()
st.sidebar.caption("User Behaviour Analytics")
