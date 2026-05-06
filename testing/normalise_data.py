import sqlite3
import shutil
import os

DB_PATH = "roles.db"
BACKUP_PATH = "roles_backup_before_normalise.db"


def backup_db():
    if os.path.exists(DB_PATH):
        shutil.copy(DB_PATH, BACKUP_PATH)
        print(f"✔ Backup created: {BACKUP_PATH}")
    else:
        print("❌ roles.db not found. Exiting.")
        exit()


def title_case_safe(text):
    if not text:
        return text
    return text.strip().title()


# ------------------------------------------------------------
# NORMALISE LEAD NAMES
# ------------------------------------------------------------
def normalise_leads(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, lead FROM job_profiles")
    rows = cur.fetchall()

    updated = 0
    for job_id, lead in rows:
        new_lead = title_case_safe(lead)
        if new_lead != lead:
            cur.execute(
                "UPDATE job_profiles SET lead = ? WHERE id = ?",
                (new_lead, job_id)
            )
            updated += 1
            print(f"Lead updated: '{lead}' → '{new_lead}'")

    print(f"\n✔ Normalised {updated} lead names.\n")


# ------------------------------------------------------------
# NORMALISE TITLES
# ------------------------------------------------------------
def normalise_titles(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM job_profiles")
    rows = cur.fetchall()

    updated = 0
    for job_id, title in rows:
        new_title = title_case_safe(title)
        if new_title != title:
            cur.execute(
                "UPDATE job_profiles SET title = ? WHERE id = ?",
                (new_title, job_id)
            )
            updated += 1
            print(f"Title updated: '{title}' → '{new_title}'")

    print(f"\n✔ Normalised {updated} job titles.\n")


# ------------------------------------------------------------
# NORMALISE SKILLS + REMOVE DUPLICATES SAFELY
# ------------------------------------------------------------
def normalise_skills(conn):
    cur = conn.cursor()
    cur.execute("SELECT rowid, job_profile_id, skill_name FROM skills")
    rows = cur.fetchall()

    updated = 0
    deleted = 0

    seen = {}  # job_profile_id → set of normalised skills

    for rowid, job_id, skill in rows:
        clean = title_case_safe(skill)

        if job_id not in seen:
            seen[job_id] = set()

        # If already seen → delete this row
        if clean in seen[job_id]:
            cur.execute("DELETE FROM skills WHERE rowid = ?", (rowid,))
            deleted += 1
            print(f"Duplicate removed for job {job_id}: '{skill}' → '{clean}'")
            continue

        # Track the clean version
        seen[job_id].add(clean)

        # Update if needed
        if clean != skill:
            cur.execute(
                "UPDATE skills SET skill_name = ? WHERE rowid = ?",
                (clean, rowid)
            )
            updated += 1
            print(f"Skill updated: '{skill}' → '{clean}'")

    print(f"\n✔ Normalised {updated} skills.")
    print(f"✔ Removed {deleted} duplicate skills.\n")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== NORMALISING LEADS, TITLES & SKILLS IN roles.db ===\n")

    backup_db()

    conn = sqlite3.connect(DB_PATH)

    normalise_leads(conn)
    normalise_titles(conn)
    normalise_skills(conn)

    conn.commit()
    conn.close()

    print("\n🎉 Done! Your database is now clean, consistent, and duplicate‑free.\n")
