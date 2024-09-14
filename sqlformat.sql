CREATE DATABASE teacherdata_db;
use teacherdata_db;

CREATE TABLE course_schedule (
    course_code VARCHAR(10),
    section VARCHAR(10),
    instructors TEXT,
    room VARCHAR(10),
    days VARCHAR(50),
    hours VARCHAR(50)
);
