import sqlite3


def get_conn():
    """Return a SQLite connection to roles.db."""
    return sqlite3.connect("roles.db", check_same_thread=False)


def init_db():
    """Initialise the database using schema.sql."""
    print("Running init_db...")

    try:
        with open("schema.sql") as f:
            schema = f.read()
            print("Loaded schema.sql successfully.")
    except FileNotFoundError:
        print("ERROR: schema.sql not found!")
        return

    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(schema)
    conn.commit()
    conn.close()

    print("Database initialised.")


# ------------------------------------------------------------
# INSERT / DELETE PROFILES
# ------------------------------------------------------------

def insert_profile(lead, title, grade, description, tasks, skills):
    conn = get_conn()
    cur = conn.cursor()

    # Insert job profile (no description anymore)
    cur.execute("""
        INSERT INTO job_profiles (lead, title, grade, description)
        VALUES (?, ?, ?, ?)
    """, (lead, title, grade, description))

    job_id = cur.lastrowid

    # Insert tasks
    for t in tasks:
        cur.execute("""
            INSERT INTO tasks (job_profile_id, task_text)
            VALUES (?, ?)
        """, (job_id, t.strip()))

    # Insert skills
    for s in skills:
        cur.execute("""
            INSERT INTO skills (job_profile_id, skill_name)
            VALUES (?, ?)
        """, (job_id, s.strip().title()))

    conn.commit()
    conn.close()
    return job_id


def delete_profile(job_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE job_profile_id=?", (job_id,))
    cur.execute("DELETE FROM skills WHERE job_profile_id=?", (job_id,))
    cur.execute("DELETE FROM job_profiles WHERE id=?", (job_id,))

    conn.commit()
    conn.close()


# ------------------------------------------------------------
# PROFILE RETRIEVAL
# ------------------------------------------------------------

def get_all_profiles():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, lead, title, grade, created_at
        FROM job_profiles
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def count_people_in_role(title):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM job_profiles
        WHERE LOWER(title) = LOWER(?)
    """, (title,))

    (count,) = cur.fetchone()
    conn.close()
    return count


# ------------------------------------------------------------
# SKILLS
# ------------------------------------------------------------

def get_skills_for_title(title):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.skill_name
        FROM skills s
        JOIN job_profiles j ON j.id = s.job_profile_id
        WHERE LOWER(j.title) = LOWER(?)
    """, (title,))

    rows = cur.fetchall()
    conn.close()

    return sorted({r[0].title() for r in rows})


def get_weighted_skills_for_title(title):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.skill_name
        FROM skills s
        JOIN job_profiles j ON j.id = s.job_profile_id
        WHERE LOWER(j.title) = LOWER(?)
    """, (title,))

    rows = cur.fetchall()
    conn.close()

    freq = {}
    for (skill,) in rows:
        clean = skill.strip().title()
        freq[clean] = freq.get(clean, 0) + 1

    return sorted(freq.items(), key=lambda x: x[1], reverse=True)


# ------------------------------------------------------------
# TASKS
# ------------------------------------------------------------

def get_tasks_for_role(title):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT t.task_text
        FROM tasks t
        JOIN job_profiles j ON j.id = t.job_profile_id
        WHERE LOWER(j.title) = LOWER(?)
    """, (title,))

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]


def get_tasks_for_person(lead):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT t.task_text
        FROM tasks t
        JOIN job_profiles j ON j.id = t.job_profile_id
        WHERE LOWER(j.lead) = LOWER(?)
    """, (lead,))

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]


# ------------------------------------------------------------
# PERSON SKILLS
# ------------------------------------------------------------

def get_skills_for_person(lead):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.skill_name
        FROM skills s
        JOIN job_profiles j ON j.id = s.job_profile_id
        WHERE LOWER(j.lead) = LOWER(?)
    """, (lead,))

    rows = cur.fetchall()
    conn.close()

    return sorted({r[0].title() for r in rows})

def get_tasks_for_person_id(person_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT t.task_text
        FROM tasks t
        JOIN job_profiles j ON j.id = t.job_profile_id
        WHERE j.id = ?
    """, (person_id,))

    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_skills_for_person_id(person_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.skill_name
        FROM skills s
        JOIN job_profiles j ON j.id = s.job_profile_id
        WHERE j.id = ?
    """, (person_id,))

    rows = cur.fetchall()
    conn.close()
    return sorted({r[0].title() for r in rows})



# ------------------------------------------------------------
# EDIT PROFILE
# ------------------------------------------------------------

def get_job_profile(job_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT lead, title, grade, description
        FROM job_profiles
        WHERE id = ?
    """, (job_id,))
    row = cur.fetchone()

    if not row:
        return None

    # Fetch tasks
    cur.execute("SELECT task_text FROM tasks WHERE job_profile_id = ?", (job_id,))
    tasks = [r[0] for r in cur.fetchall()]

    # Fetch skills
    cur.execute("SELECT skill_name FROM skills WHERE job_profile_id = ?", (job_id,))
    skills = [r[0] for r in cur.fetchall()]

    conn.close()

    return {
        "lead": row[0],
        "title": row[1],
        "grade": row[2],
        "description": row[3],
        "tasks": tasks,
        "skills": skills
    }


def update_profile(job_id, lead, title, grade, description, tasks, skills):
    conn = get_conn()
    cur = conn.cursor()

    # Update main profile fields
    cur.execute("""
        UPDATE job_profiles
        SET lead = ?, title = ?, grade = ?, description = ?
        WHERE id = ?
    """, (lead, title, grade, description, job_id))

    # Replace tasks
    cur.execute("DELETE FROM tasks WHERE job_profile_id = ?", (job_id,))
    for t in tasks:
        cur.execute("""
            INSERT INTO tasks (job_profile_id, task_text)
            VALUES (?, ?)
        """, (job_id, t.strip()))

    # Replace skills
    cur.execute("DELETE FROM skills WHERE job_profile_id = ?", (job_id,))
    for s in skills:
        cur.execute("""
            INSERT INTO skills (job_profile_id, skill_name)
            VALUES (?, ?)
        """, (job_id, s.strip().title()))

    conn.commit()
    conn.close()

