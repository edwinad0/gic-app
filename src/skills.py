from .connection import get_conn

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
