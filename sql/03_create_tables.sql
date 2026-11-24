
-- =====================================================
-- ArchintX: AI-Powered User Behaviour Analytics
-- Database schema creation script
-- Database: user_behaviour_analytics
-- DBMS: MySQL
-- =====================================================

CREATE DATABASE IF NOT EXISTS user_behaviour_analytics
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

USE user_behaviour_analytics;


-- 1. USERS TABLE

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(30) NOT NULL,
    user_segment VARCHAR(50) DEFAULT NULL,
    city VARCHAR(100) DEFAULT NULL,
    registration_date DATE DEFAULT NULL,
    acquisition_source VARCHAR(100) DEFAULT NULL,
    device_type VARCHAR(50) DEFAULT NULL,
    is_verified TINYINT(1) DEFAULT NULL,
    PRIMARY KEY (user_id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- 2. COURSES TABLE

CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(30) NOT NULL,
    course_name VARCHAR(150) DEFAULT NULL,
    category VARCHAR(100) DEFAULT NULL,
    difficulty VARCHAR(50) DEFAULT NULL,
    duration_hours DECIMAL(8,2) DEFAULT NULL,
    PRIMARY KEY (course_id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- 3. ENROLLMENTS TABLE

CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id VARCHAR(30) NOT NULL,
    user_id VARCHAR(30) DEFAULT NULL,
    course_id VARCHAR(30) DEFAULT NULL,
    enrollment_date DATE DEFAULT NULL,
    progress_percent INT DEFAULT NULL,
    enrollment_status VARCHAR(50) DEFAULT NULL,
    completion_date DATE DEFAULT NULL,
    PRIMARY KEY (enrollment_id),
    KEY user_id (user_id),
    KEY course_id (course_id),
    CONSTRAINT enrollments_ibfk_1
        FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT enrollments_ibfk_2
        FOREIGN KEY (course_id) REFERENCES courses (course_id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- 4. USER ACTIVITY TABLE

CREATE TABLE IF NOT EXISTS user_activity (
    event_id VARCHAR(30) NOT NULL,
    user_id VARCHAR(30) DEFAULT NULL,
    event_timestamp DATETIME DEFAULT NULL,
    event_type VARCHAR(100) DEFAULT NULL,
    course_id VARCHAR(30) DEFAULT NULL,
    session_id VARCHAR(50) DEFAULT NULL,
    duration_seconds INT DEFAULT NULL,
    platform VARCHAR(50) DEFAULT NULL,
    PRIMARY KEY (event_id),
    KEY user_id (user_id),
    KEY course_id (course_id),
    CONSTRAINT user_activity_ibfk_1
        FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT user_activity_ibfk_2
        FOREIGN KEY (course_id) REFERENCES courses (course_id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- End of schema creation script
