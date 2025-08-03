# Simple user model with database operations
import sqlite3
import hashlib
from config.database import get_db_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_to_dict(user):
    if user:
        user_dict = dict(user)

        user_dict.pop('password', None)
        return user_dict
    return None

def create_user(name, email, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                    (name, email, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    return [user_to_dict(user) for user in users]

def get_user_by_id(user_id):

    conn = get_db_connection()
    user = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user_to_dict(user)

def update_user(user_id, name=None, email=None):

    conn = get_db_connection()
    updates = []
    params = []
    
    if name:
        updates.append("name = ?")
        params.append(name)
    if email:
        updates.append("email = ?")
        params.append(email)
    
    if not updates:
        conn.close()
        return False
    
    params.append(user_id)
    result = conn.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", params)
    conn.commit()
    conn.close()
    
    return result.rowcount > 0

def delete_user(user_id):

    conn = get_db_connection()
    result = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return result.rowcount > 0

def search_users_by_name(name):

    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", 
                       (f"%{name}%",)).fetchall()
    conn.close()
    return [user_to_dict(user) for user in users]

def authenticate_user(email, password):

    hashed_password = hash_password(password)
    conn = get_db_connection()
    user = conn.execute("SELECT id, name, email FROM users WHERE email = ? AND password = ?", 
                      (email, hashed_password)).fetchone()
    conn.close()
    return user_to_dict(user)
