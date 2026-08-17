#!/usr/bin/env python3
"""Run Alembic migrations against the configured DATABASE_URL.

Usage:
  python run_migrations.py

This script reads `DATABASE_URL` from the environment or .env file
and runs `alembic upgrade head` programmatically.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
project_root = Path(__file__).resolve().parents[1]
dotenv_path = project_root / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print('ERROR: DATABASE_URL is not set. Copy mgnt/.env.sample to .env and set DATABASE_URL.')
    sys.exit(1)

# Run alembic programmatically
from alembic.config import Config
import alembic.command

alembic_cfg = Config(str(project_root / 'migrations' / 'alembic.ini'))
# Ensure alembic uses the provided URL
alembic_cfg.set_main_option('sqlalchemy.url', DATABASE_URL)
# Ensure alembic knows where the migration scripts live
alembic_cfg.set_main_option('script_location', str(project_root / 'migrations'))

print('Running migrations against:', DATABASE_URL)
try:
    alembic.command.upgrade(alembic_cfg, 'head')
    print('Migrations applied successfully.')
except Exception as e:
    print('Migration failed:', e)
    sys.exit(2)
