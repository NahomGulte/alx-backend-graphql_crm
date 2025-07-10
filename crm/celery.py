#!/usr/bin/env python3
"""
Celery configuration for CRM project.
Initializes the Celery app with Django settings and Redis broker.
"""

import os
from celery import Celery

# Set the default Django settings module for 'celery' command-line programs
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

# Create the Celery app
app = Celery('crm')

# Load configuration from Django settings, using the 'CELERY_' namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed Django apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Debug task to verify Celery setup.
    """
    print(f'Request: {self.request!r}')
