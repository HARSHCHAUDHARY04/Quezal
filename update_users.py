#!/usr/bin/env python3
"""
Script to update existing users with user_type column
"""

import sqlite3
import os

def update_existing_users():
    """Add user_type column to existing users table and set default values"""
    
    db_path = 'quezal.db'
    
    if not os.path.exists(db_path):
        print("Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if user_type column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_type' not in columns:
            print("Adding user_type column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN user_type TEXT DEFAULT 'student'")
            print("✓ user_type column added")
        else:
            print("✓ user_type column already exists")
        
        # Update existing users without user_type to have 'student' as default
        cursor.execute("UPDATE users SET user_type = 'student' WHERE user_type IS NULL")
        updated_count = cursor.rowcount
        
        if updated_count > 0:
            print(f"✓ Updated {updated_count} existing users with default user_type 'student'")
        else:
            print("✓ All users already have user_type set")
        
        # Show current users
        cursor.execute("SELECT id, email, name, user_type FROM users")
        users = cursor.fetchall()
        
        print(f"\nCurrent users in database:")
        print("-" * 50)
        for user in users:
            print(f"ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Type: {user[3]}")
        
        conn.commit()
        print("\n✓ Database update completed successfully!")
        
    except Exception as e:
        print(f"Error updating database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_existing_users()
