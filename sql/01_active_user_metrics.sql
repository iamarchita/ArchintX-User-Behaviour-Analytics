
USE user_behaviour_analytics;

-- DAU, MAU and DAU/MAU Ratio

-- Qualifying activity definition:
-- All cleaned activity events, including login and logout.
-- Activity before user registration is excluded.

WITH qualifying_activity AS (
    SELECT DISTINCT
        a.user_id,
        DATE(a.event_timestamp) AS activity_date,
        DATE_FORMAT(a.event_timestamp, '%Y-%m') AS activity_month
    FROM user_activity a
    INNER JOIN users u
        ON a.user_id = u.user_id
    WHERE a.event_timestamp >= u.registration_date
),

daily_active AS (
    SELECT
        activity_date,
        activity_month,
        COUNT(DISTINCT user_id) AS DAU
    FROM qualifying_activity
    GROUP BY activity_date, activity_month
),

monthly_active AS (
    SELECT
        activity_month,
        COUNT(DISTINCT user_id) AS MAU
    FROM qualifying_activity
    GROUP BY activity_month
)

SELECT
    d.activity_date,
    d.activity_month,
    d.DAU,
    m.MAU,
    ROUND(
        d.DAU * 100.0 / NULLIF(m.MAU, 0),
        2
    ) AS DAU_MAU_Ratio_Percent
FROM daily_active d
JOIN monthly_active m
    ON d.activity_month = m.activity_month
ORDER BY d.activity_date;


-- WEEKLY ACTIVE USERS (WAU)

SELECT
    YEARWEEK(a.event_timestamp, 3) AS year_week,
    MIN(DATE(a.event_timestamp)) AS week_start_date,
    MAX(DATE(a.event_timestamp)) AS last_activity_date,
    COUNT(DISTINCT a.user_id) AS WAU,
    COUNT(*) AS total_events
FROM user_activity a
INNER JOIN users u
    ON a.user_id = u.user_id
WHERE a.event_timestamp >= u.registration_date
GROUP BY YEARWEEK(a.event_timestamp, 3)
ORDER BY year_week;


-- REGISTRATION TRENDS

-- 1. Daily registrations
SELECT
    DATE(registration_date) AS registration_day,
    COUNT(*) AS new_users
FROM users
GROUP BY DATE(registration_date)
ORDER BY registration_day;


-- 2. Weekly registrations
SELECT
    YEARWEEK(registration_date, 3) AS year_week,
    MIN(DATE(registration_date)) AS week_start,
    COUNT(*) AS new_users
FROM users
GROUP BY YEARWEEK(registration_date, 3)
ORDER BY year_week;


-- 3. Monthly registrations
SELECT
    DATE_FORMAT(registration_date, '%Y-%m') AS registration_month,
    COUNT(*) AS new_users
FROM users
GROUP BY DATE_FORMAT(registration_date, '%Y-%m')
ORDER BY registration_month;


-- 4. Registrations by acquisition source
SELECT
    acquisition_source,
    COUNT(*) AS new_users
FROM users
GROUP BY acquisition_source
ORDER BY new_users DESC;


-- 5. Registrations by user segment
SELECT
    user_segment,
    COUNT(*) AS new_users
FROM users
GROUP BY user_segment
ORDER BY new_users DESC;

