CREATE TABLE IF NOT EXISTS job_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead TEXT,
    title TEXT,
    grade TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_profile_id INTEGER,
    skill_name TEXT,
    FOREIGN KEY(job_profile_id) REFERENCES job_profiles(id)
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_profile_id INTEGER,
    task_text TEXT,
    FOREIGN KEY(job_profile_id) REFERENCES job_profiles(id)
);

