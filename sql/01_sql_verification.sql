
USE user_behaviour_analytics;

-- 1. Verify all four tables
SHOW TABLES;

-- 2. Verify actual table structures
SHOW CREATE TABLE users;
SHOW CREATE TABLE courses;
SHOW CREATE TABLE enrollments;
SHOW CREATE TABLE user_activity;

-- 3. Verify row counts
SELECT 'users' AS table_name, COUNT(*) AS total_rows FROM users
UNION ALL
SELECT 'courses', COUNT(*) FROM courses
UNION ALL
SELECT 'enrollments', COUNT(*) FROM enrollments
UNION ALL
SELECT 'user_activity', COUNT(*) FROM user_activity;

-- 4. Verify primary keys and foreign keys
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME, CONSTRAINT_NAME;

-- 5. Verify indexes
SHOW INDEX FROM users;
SHOW INDEX FROM courses;
SHOW INDEX FROM enrollments;
SHOW INDEX FROM user_activity;

-- 6. Verify enrollment status
SELECT
    enrollment_status,
    COUNT(*) AS total_enrollments
FROM enrollments
GROUP BY enrollment_status;

-- 7. Verify completion status vs completion date
SELECT
    COUNT(*) AS total_enrollments,
    SUM(enrollment_status = 'Completed') AS completed_by_status,
    SUM(completion_date IS NOT NULL) AS completed_by_date,
    SUM(
        (enrollment_status = 'Completed')
        <> (completion_date IS NOT NULL)
    ) AS mismatched_records
FROM enrollments;

-- 8. Verify activity event counts
SELECT
    COUNT(*) AS total_events,
    COUNT(DISTINCT event_id) AS unique_event_ids,
    COUNT(DISTINCT user_id) AS distinct_users,
    SUM(duration_seconds < 0) AS negative_durations
FROM user_activity;

-- 9. Verify invalid foreign key references
SELECT COUNT(*) AS invalid_user_references
FROM enrollments e
LEFT JOIN users u ON e.user_id = u.user_id
WHERE u.user_id IS NULL;

SELECT COUNT(*) AS invalid_course_references
FROM enrollments e
LEFT JOIN courses c ON e.course_id = c.course_id
WHERE c.course_id IS NULL;
