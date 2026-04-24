import sqlite3, bcrypt

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users
           (email TEXT PRIMARY KEY,
            name TEXT,
            password TEXT)"""
    )
    conn.close()

def register_user(name, email, password):
    conn = sqlite3.connect("users.db")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn.execute("INSERT INTO users VALUES (?,?,?)", (email, name, hashed))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect("users.db")
    cur = conn.execute("SELECT password,name FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[0].encode()):
        # return true and the user name
        return True, row[1]
    return False, None