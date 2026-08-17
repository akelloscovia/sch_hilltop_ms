#!/usr/bin/env python3
"""Seed the database with default website content and admin accounts.

This script imports the app factory and uses the app context to create
initial records (contact info, home page, about page) if they don't exist.

Usage:
  python seed_db.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import sys

# Load .env if present
project_root = Path(__file__).resolve().parents[1]
dotenv_path = project_root / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# Ensure the project `mgnt` directory is on sys.path so `import app` works
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models.website import WebsiteContactInfo, HomePage, AboutPage

app = create_app()  # uses FLASK_ENV from env or default

with app.app_context():
    created = []

    # Contact info
    if not WebsiteContactInfo.query.first():
        contact = WebsiteContactInfo(
            address=os.getenv('DEFAULT_ADDRESS', 'Kasangati, Wakiso District, Uganda'),
            phone_number=os.getenv('DEFAULT_PHONE', '+256 771 234 567'),
            email=os.getenv('DEFAULT_EMAIL', 'info@hilltopjunior.ug'),
            working_hours=os.getenv('DEFAULT_WORKING_HOURS', 'Monday - Friday: 7:00 AM - 5:00 PM'),
            additional_notes=os.getenv('DEFAULT_ADDITIONAL_NOTES', 'Office hours: 8:00 AM - 4:00 PM')
        )
        db.session.add(contact)
        created.append('WebsiteContactInfo')

    # Home page
    if not HomePage.query.first():
        import json
        core_values = json.dumps([
            {"title": "Community", "description": "We build connections between students, staff and families."},
            {"title": "Respect", "description": "We value diversity, kindness and dignity for all."},
            {"title": "Excellence", "description": "We strive for high standards in learning and behavior."}
        ])
        home = HomePage(
            hero_title=os.getenv('HERO_TITLE', 'Hilltop Junior School Kasangati'),
            hero_subtitle=os.getenv('HERO_SUBTITLE', 'Nurturing Excellence & Character Development'),
            hero_image=os.getenv('HERO_IMAGE', ''),
            about_title=os.getenv('ABOUT_TITLE', 'Welcome to Hilltop Junior School'),
            about_text=os.getenv('ABOUT_TEXT', 'Hilltop Junior School is a warm and vibrant learning community.'),
            about_link=os.getenv('ABOUT_LINK', '/about'),
            core_values=core_values
        )
        db.session.add(home)
        created.append('HomePage')

    # About page
    if not AboutPage.query.first():
        about = AboutPage(
            hero_title=os.getenv('ABOUT_HERO_TITLE', 'About Hilltop Junior School'),
            hero_description=os.getenv('ABOUT_HERO_DESC', 'We provide a safe, friendly, and inclusive environment where every child thrives.'),
            hero_image=os.getenv('ABOUT_HERO_IMAGE', '')
        )
        db.session.add(about)
        created.append('AboutPage')

    if created:
        db.session.commit()
        print('Seeded:', ', '.join(created))
    else:
        print('Nothing to seed; database already has initial records.')
