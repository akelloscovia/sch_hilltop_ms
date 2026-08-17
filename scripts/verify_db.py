#!/usr/bin/env python3
import sqlite3
from pprint import pprint
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'school_management.db')
DB_PATH = os.path.abspath(DB_PATH)
print('DB path:', DB_PATH)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print('\nLatest 3 admission_applications:')
try:
    cur.execute('SELECT id, student_name, parent_name, parent_email, grade_applied, contact_number, status, submitted_at FROM admission_applications ORDER BY submitted_at DESC LIMIT 3')
    rows = cur.fetchall()
    for r in rows:
        pprint(r)
except Exception as e:
    print('Error querying admissions:', e)

print('\nLatest 3 messages:')
try:
    cur.execute('SELECT id, sender_id, recipient_id, subject, body, is_read, created_at FROM messages ORDER BY created_at DESC LIMIT 3')
    rows = cur.fetchall()
    for r in rows:
        pprint(r)
except Exception as e:
    print('Error querying messages:', e)

conn.close()
