#!/usr/bin/env python3
"""Run migrations then seed the database.

Usage:
  python migrate_and_seed.py
"""
import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
python = sys.executable

print('Running migrations...')
res = subprocess.run([python, str(project_root / 'scripts' / 'run_migrations.py')])
if res.returncode != 0:
    print('Migrations failed; aborting.')
    sys.exit(res.returncode)

print('\nSeeding database...')
res = subprocess.run([python, str(project_root / 'scripts' / 'seed_db.py')])
if res.returncode != 0:
    print('Seeding failed.')
    sys.exit(res.returncode)

print('\nMigrate and seed completed successfully.')
