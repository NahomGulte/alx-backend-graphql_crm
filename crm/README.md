# CRM Celery Reporting Setup

## 🧩 Requirements

- Redis installed and running on localhost
- Python packages:
  - celery
  - django-celery-beat
  - requests

## 🚀 Setup Instructions

1. **Install Redis** (Ubuntu):

   ```bash
   sudo apt update
   sudo apt install redis
   sudo systemctl start redis
   sudo systemctl enable redis
