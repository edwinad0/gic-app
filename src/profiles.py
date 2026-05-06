from .connection import get_conn

def insert_profile(lead, title, grade, description, tasks, skills):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO job_profiles (lead, title, grade, description)
        VALUES (?, ?, ?, ?)
    """, (lead, title, grade, description))

    job_id = cur.lastrowid

    for t in tasks:
        cur.execute("""
            INSERT INTO tasks (job_profile_id, task_text)
            VALUES (?, ?)
        """, (job_id, t.strip()))

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

    cur.execute("SELECT task_text FROM tasks WHERE job_profile_id = ?", (job_id,))
    tasks = [r[0] for r in cur.fetchall()]

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

    cur.execute("""
        UPDATE job_profiles
        SET lead = ?, title = ?, grade = ?, description = ?
        WHERE id = ?
    """, (lead, title, grade, description, job_id))

    cur.execute("DELETE FROM tasks WHERE job_profile_id = ?", (job_id,))
    for t in tasks:
        cur.execute("""
            INSERT INTO tasks (job_profile_id, task_text)
            VALUES (?, ?)
        """, (job_id, t.strip()))

    cur.execute("DELETE FROM skills WHERE job_profile_id = ?", (job_id,))
    for s in skills:
        cur.execute("""
            INSERT INTO skills (job_profile_id, skill_name)
            VALUES (?, ?)
        """, (job_id, s.strip().title()))

    conn.commit()
    conn.close()

    
def get_name_for_person_id(person_id):
    """
    Return the person's name (lead field) for a given person ID.
    """
    try:
        person_id = int(person_id)
    except (TypeError, ValueError):
        return None

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT lead
        FROM job_profiles
        WHERE id = ?
    """, (person_id,))

    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def count_people_in_role(title):
    """
    Return the number of profiles with a given role title (case-insensitive).
    """
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
