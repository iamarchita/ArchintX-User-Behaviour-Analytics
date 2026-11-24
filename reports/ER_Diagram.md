# Entity Relationship Diagram

## ArchintX – AI-Powered User Behaviour Analytics

```mermaid
erDiagram
    USERS ||--o{ ENROLLMENTS : has
    COURSES ||--o{ ENROLLMENTS : contains
    USERS ||--o{ USER_ACTIVITY : generates
    COURSES ||--o{ USER_ACTIVITY : relates_to

    USERS {
        VARCHAR user_id PK
        VARCHAR user_segment
        VARCHAR city
        DATE registration_date
        VARCHAR acquisition_source
        VARCHAR device_type
        TINYINT is_verified
    }

    COURSES {
        VARCHAR course_id PK
        VARCHAR course_name
        VARCHAR category
        VARCHAR difficulty
        DECIMAL duration_hours
    }

    ENROLLMENTS {
        VARCHAR enrollment_id PK
        VARCHAR user_id FK
        VARCHAR course_id FK
        DATE enrollment_date
        INT progress_percent
        VARCHAR enrollment_status
        DATE completion_date
    }

    USER_ACTIVITY {
        VARCHAR event_id PK
        VARCHAR user_id FK
        DATETIME event_timestamp
        VARCHAR event_type
        VARCHAR course_id FK
        VARCHAR session_id
        INT duration_seconds
        VARCHAR platform
    }
