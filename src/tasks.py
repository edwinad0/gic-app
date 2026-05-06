from .connection import get_conn

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
