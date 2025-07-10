#!/bin/bash

# Activate your virtual environment if needed
# source /path/to/venv/bin/activate

# Run the Django shell command to delete inactive customers and capture the count
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
echo \"\$(date '+%Y-%m-%d %H:%M:%S') Deleted \$deleted_count customers due to inactivity\" >> /tmp/customer_cleanup_log.txt
