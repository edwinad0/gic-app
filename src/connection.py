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
