#!/usr/bin/env python3
import requests
import json
import time
from pprint import pprint

BASE = "http://127.0.0.1:5010/api/v1"

# 1) Pick a gallery image
try:
    r = requests.get(f"{BASE}/gallery")
    imgs = r.json() if r.status_code == 200 else []
except Exception:
    imgs = []

if imgs:
    chosen = imgs[0]
    image_url = chosen.get('image') or f"/api/v1/gallery/files/{chosen.get('filename')}"
else:
    # fallback to known file
    image_url = "/api/v1/gallery/files/Screenshot_2026-06-14_205539.png"

print('Chosen image URL:', image_url)

# 2) Update about page with hero_images pointing to the gallery image
about_payload = {
    'vision': 'To nurture confident, creative, and responsible learners.',
    'mission': 'To provide accessible quality education in a safe, supportive, and inclusive environment.',
    'director': 'Mr. John Smith',
    'head_teacher': 'Mrs. Sarah Johnson',
    'deputy_head_teacher': 'Mr. David Ochieng',
    'achievements': 'Award-winning school with excellent exam results.',
    'hero_images': [image_url]
}

print('Updating /about...')
resp = requests.put(f"{BASE}/about", json=about_payload)
print('PUT /about status:', resp.status_code)
try:
    pprint(resp.json())
except Exception:
    print(resp.text[:200])

# 3) Create or update contact info
contact_data = {
    "address": "Kasangati, Wakiso District, Uganda",
    "phone_number": "+256 771 234 567",
    "email": "info@hilltopjunior.ug",
    "working_hours": "Monday - Friday: 7:00 AM - 5:00 PM",
    "additional_notes": "Office hours: 8:00 AM - 4:00 PM. For emergencies, call the duty officer."
}
print('\nUpdating contact info...')
getc = requests.get(f"{BASE}/contact_info")
if getc.status_code == 200:
    items = getc.json()
    # normalize wrapper shapes
    if isinstance(items, dict) and 'data' in items:
        items = items.get('data')
    if isinstance(items, dict) and 'result' in items:
        items = items.get('result')
    if isinstance(items, list) and len(items) > 0:
        cid = items[0].get('id')
        if cid:
            r2 = requests.put(f"{BASE}/contact_info/{cid}", json=contact_data)
        else:
            r2 = requests.post(f"{BASE}/contact_info", json=contact_data)
    else:
        r2 = requests.post(f"{BASE}/contact_info", json=contact_data)
else:
    r2 = requests.post(f"{BASE}/contact_info", json=contact_data)
print('contact response:', r2.status_code)
try:
    pprint(r2.json())
except Exception:
    print(r2.text[:200])

# 4) Submit a test admission application
print('\nSubmitting test application...')
application = {
    'student_name': 'Test Student',
    'date_of_birth': '2016-05-20',
    'parent_name': 'Alice Parent',
    'parent_email': 'alice.parent@example.com',
    'contact_number': '+256770000001',
    'grade_applied': 'Primary 1'
}
ra = requests.post(f"{BASE}/admissions/apply", json=application)
print('apply status:', ra.status_code)
try:
    pprint(ra.json())
except Exception:
    print(ra.text[:200])

# give DB a moment
time.sleep(0.5)

# 5) Verify in database via app context
print('\nVerifying in DB...')
try:
    from app import create_app, db
    app = create_app()
    with app.app_context():
        from app.models.website import AdmissionApplication
        from app.models.communication import Message
        app_q = AdmissionApplication.query.order_by(AdmissionApplication.submitted_at.desc()).first()
        msg_q = Message.query.order_by(Message.created_at.desc()).first()
        print('\nLatest AdmissionApplication:')
        if app_q:
            pprint(app_q.to_dict())
        else:
            print('No AdmissionApplication found')
        print('\nLatest Message:')
        if msg_q:
            pprint(msg_q.to_dict())
        else:
            print('No Message found')
except Exception as e:
    print('DB verification failed:', str(e))

print('\nDone')
