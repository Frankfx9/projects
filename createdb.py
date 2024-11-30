import sqlite3
import hashlib

def setup_users():
    # Connect to the database
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()

    # Create users table if not exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS userdata (
            username TEXT PRIMARY KEY,
            password TEXT,
            status TEXT DEFAULT 'online'
        )
    ''')

    # Hash passwords
    johndane_password = hashlib.sha256("workaholic".encode()).hexdigest()
    kevdav_password = hashlib.sha256("john4life".encode()).hexdigest()

    # Insert or replace users
    users = [
        ("johndane", johndane_password),
        ("kevdav", kevdav_password)
    ]

    cur.executemany('''
        INSERT OR REPLACE INTO userdata (username, password) 
        VALUES (?, ?)
    ''', users)

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Users setup completed successfully!")

# Run the setup
if __name__ == "__main__":
    setup_users()