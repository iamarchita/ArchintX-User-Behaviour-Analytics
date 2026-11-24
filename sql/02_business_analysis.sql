
USE user_behaviour_analytics;

-- =====================================================
-- 1. ACQUISITION SOURCE: REGISTRATION AND ENROLLMENT RATE
-- Cohort = registration month.
-- Numerator = distinct cohort users enrolled on/after registration.
-- Denominator = distinct registered users in that cohort.
-- =====================================================

SELECT
    DATE_FORMAT(u.registration_date, '%Y-%m') AS cohort_month,
    u.acquisition_source,
    COUNT(DISTINCT u.user_id) AS registered_users,
    COUNT(DISTINCT e.user_id) AS enrolled_users,
    ROUND(
        COUNT(DISTINCT e.user_id) * 100.0 /
        NULLIF(COUNT(DISTINCT u.user_id), 0), 2
    ) AS enrollment_rate_pct
FROM users u
LEFT JOIN enrollments e
    ON u.user_id = e.user_id
    AND e.enrollment_date >= u.registration_date
GROUP BY cohort_month, u.acquisition_source
ORDER BY cohort_month, registered_users DESC;


-- =====================================================
-- 2. COURSE PERFORMANCE AND DROP-OFF
-- Drop-off = enrollment not marked Completed.
-- This does not prove permanent abandonment.
-- =====================================================

SELECT
    c.course_name,
    COUNT(e.enrollment_id) AS total_enrollments,
    SUM(e.enrollment_status = 'Completed') AS completed_enrollments,
    SUM(e.enrollment_status <> 'Completed') AS incomplete_enrollments,
    ROUND(AVG(e.progress_percent), 2) AS avg_progress_pct,
    ROUND(
        SUM(e.enrollment_status <> 'Completed') * 100.0 /
        NULLIF(COUNT(e.enrollment_id), 0), 2
    ) AS dropoff_rate_pct,
    ROUND(
        SUM(e.enrollment_status = 'Completed') * 100.0 /
        NULLIF(COUNT(e.enrollment_id), 0), 2
    ) AS completion_rate_pct
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
ORDER BY total_enrollments DESC;


-- =====================================================
-- 3. COURSE COMPLETION RATE
-- Numerator = completed enrollments.
-- Denominator = all enrollments in the dataset.
-- =====================================================

SELECT
    COUNT(*) AS eligible_enrollments,
    SUM(enrollment_status = 'Completed') AS completed_enrollments,
    ROUND(
        SUM(enrollment_status = 'Completed') * 100.0 /
        NULLIF(COUNT(*), 0), 2
    ) AS overall_completion_rate_pct
FROM enrollments;


-- =====================================================
-- 4. USER FUNNEL
-- Qualifying activity excludes pre-registration events.
-- Stages are distinct-user reach, not necessarily sequential.
-- =====================================================

WITH qualifying_activity AS (
    SELECT DISTINCT
        a.user_id,
        a.event_type
    FROM user_activity a
    JOIN users u
        ON a.user_id = u.user_id
    WHERE a.event_timestamp >= u.registration_date
)
SELECT
    (SELECT COUNT(DISTINCT user_id) FROM users)
        AS registered_users,

    (SELECT COUNT(DISTINCT user_id)
     FROM qualifying_activity
     WHERE event_type = 'login')
        AS users_logged_in,

    (SELECT COUNT(DISTINCT user_id)
     FROM qualifying_activity
     WHERE event_type = 'view_course')
        AS users_viewed_course,

    (SELECT COUNT(DISTINCT user_id)
     FROM enrollments)
        AS users_enrolled,

    (SELECT COUNT(DISTINCT user_id)
     FROM qualifying_activity
     WHERE event_type = 'start_lesson')
        AS users_started_lesson,

    (SELECT COUNT(DISTINCT user_id)
     FROM qualifying_activity
     WHERE event_type = 'complete_course')
        AS users_completed_course;


-- =====================================================
-- 5. WEEK 1 AND WEEK 4 RETENTION
-- Week 1 return window: days 7–13 after registration.
-- Week 4 return window: days 28–34 after registration.
-- Return activity = any cleaned event after registration.
-- =====================================================

WITH user_retention AS (
    SELECT
        u.user_id,
        DATE_FORMAT(u.registration_date, '%Y-%m') AS cohort_month,
        MAX(
            CASE WHEN DATEDIFF(
                DATE(a.event_timestamp), DATE(u.registration_date)
            ) BETWEEN 7 AND 13 THEN 1 ELSE 0 END
        ) AS week1_returned,
        MAX(
            CASE WHEN DATEDIFF(
                DATE(a.event_timestamp), DATE(u.registration_date)
            ) BETWEEN 28 AND 34 THEN 1 ELSE 0 END
        ) AS week4_returned
    FROM users u
    LEFT JOIN user_activity a
        ON u.user_id = a.user_id
        AND a.event_timestamp >= u.registration_date
    GROUP BY u.user_id, cohort_month
)
SELECT
    cohort_month,
    COUNT(*) AS cohort_users,
    SUM(week1_returned) AS week1_returned_users,
    ROUND(AVG(week1_returned) * 100, 2) AS week1_retention_pct,
    SUM(week4_returned) AS week4_returned_users,
    ROUND(AVG(week4_returned) * 100, 2) AS week4_retention_pct
FROM user_retention
GROUP BY cohort_month
ORDER BY cohort_month;


-- =====================================================
-- 6. INACTIVE USERS
-- Reference date = latest qualifying activity date.
-- Users with no qualifying activity are also counted inactive.
-- =====================================================

WITH qualifying_activity AS (
    SELECT
        a.user_id,
        DATE(a.event_timestamp) AS activity_date
    FROM user_activity a
    JOIN users u
        ON a.user_id = u.user_id
    WHERE a.event_timestamp >= u.registration_date
),
last_activity AS (
    SELECT
        user_id,
        MAX(activity_date) AS last_activity_date
    FROM qualifying_activity
    GROUP BY user_id
),
reference_date AS (
    SELECT MAX(activity_date) AS as_of_date
    FROM qualifying_activity
)
SELECT
    r.as_of_date,
    COUNT(*) AS total_registered_users,
    SUM(
        la.last_activity_date IS NULL
        OR DATEDIFF(r.as_of_date, la.last_activity_date) >= 14
    ) AS inactive_14_days,
    SUM(
        la.last_activity_date IS NULL
        OR DATEDIFF(r.as_of_date, la.last_activity_date) >= 30
    ) AS inactive_30_days
FROM users u
LEFT JOIN last_activity la
    ON u.user_id = la.user_id
CROSS JOIN reference_date r
GROUP BY r.as_of_date;


-- =====================================================
-- 7. ENGAGEMENT BY USER SEGMENT
-- =====================================================

SELECT
    u.user_segment,
    COUNT(DISTINCT u.user_id) AS registered_users,
    COUNT(DISTINCT a.user_id) AS active_users,
    COUNT(a.event_id) AS total_events,
    ROUND(AVG(a.duration_seconds), 2) AS avg_duration_seconds
FROM users u
LEFT JOIN user_activity a
    ON u.user_id = a.user_id
    AND a.event_timestamp >= u.registration_date
GROUP BY u.user_segment
ORDER BY registered_users DESC;


-- =====================================================
-- 8. ENGAGEMENT BY CITY
-- =====================================================

SELECT
    u.city,
    COUNT(DISTINCT u.user_id) AS registered_users,
    COUNT(DISTINCT a.user_id) AS active_users,
    COUNT(a.event_id) AS total_events
FROM users u
LEFT JOIN user_activity a
    ON u.user_id = a.user_id
    AND a.event_timestamp >= u.registration_date
GROUP BY u.city
ORDER BY registered_users DESC;


-- =====================================================
-- 9. ENGAGEMENT BY DEVICE TYPE
-- =====================================================

SELECT
    u.device_type,
    COUNT(DISTINCT u.user_id) AS registered_users,
    COUNT(DISTINCT a.user_id) AS active_users,
    COUNT(a.event_id) AS total_events
FROM users u
LEFT JOIN user_activity a
    ON u.user_id = a.user_id
    AND a.event_timestamp >= u.registration_date
GROUP BY u.device_type
ORDER BY total_events DESC;


-- =====================================================
-- 10. ENGAGEMENT BY PLATFORM
-- Users may appear on multiple platforms.
-- Platform user counts are not mutually exclusive.
-- =====================================================

SELECT
    a.platform,
    COUNT(*) AS total_events,
    COUNT(DISTINCT a.user_id) AS active_users,
    ROUND(AVG(a.duration_seconds), 2) AS avg_duration_seconds
FROM user_activity a
JOIN users u
    ON a.user_id = u.user_id
WHERE a.event_timestamp >= u.registration_date
GROUP BY a.platform
ORDER BY total_events DESC;
