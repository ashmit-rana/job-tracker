import sqlite3;

DB_NAME = "jobs.db"

def get_connection(): 
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db(): 
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role NOT NULL,
            status TEXT NOT NULL default 'Applied',
            applied_date TEXT,
            notes TEXT
        )
        """
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database ready")
    


