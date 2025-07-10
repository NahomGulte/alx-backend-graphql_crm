#!/bin/bash

# Determine the directory of the script regardless of how it is called
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Assume manage.py is located two levels above this script directory
project_root="$(cd "$script_dir/../.." && pwd)"

# Change to project root
cd "$project_root" || {
  echo "Failed to change directory to project root: $project_root"
  exit 1
}

# Run the Django shell command and capture number of deleted customers
deleted_count=$(python3 manage.py shell -c "
from django.utils.timezone import now
from datetime import timedelta
from crm.models import Customer
from django.db.models import Q
one_year_ago = now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(~Q(order__created_at__gte=one_year_ago)).delete()
print(deleted)
")

# Log with timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') Deleted $deleted_count customers due to inactivity" >> /tmp/customer_cleanup_log.txt
