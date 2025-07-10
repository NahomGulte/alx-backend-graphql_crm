#!/bin/bash

# Get the current working directory before changes
cwd=$(pwd)

# Get the directory of this script file
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Assume project root is two levels up from script_dir
project_root="$(cd "$script_dir/../.." && pwd)"

# Change directory to the project root and handle failure
if cd "$project_root"; then
    echo "Changed directory to project root: $project_root"
else
    echo "Failed to change directory to project root from $cwd"
    exit 1
fi

# Run the Django shell command and capture deleted customers count
deleted_count=$(python3 manage.py shell -c "
from django.utils.timezone import now
from datetime import timedelta
from crm.models import Customer
from django.db.models import Q
one_year_ago = now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(~Q(order__created_at__gte=one_year_ago)).delete()
print(deleted)
")

# Log result with timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') Deleted $deleted_count customers due to inactivity" >> /tmp/customer_cleanup_log.txt
