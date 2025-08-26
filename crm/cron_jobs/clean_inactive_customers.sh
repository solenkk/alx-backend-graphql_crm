#!/bin/bash

# Navigate to project directory (adjust path as needed)
cd /path/to/your/project

# Execute Django management command to delete inactive customers
python manage.py shell << EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order

# Find customers with no orders in the last year
one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(
    order__isnull=True
) | Customer.objects.filter(
    order__created_at__lt=one_year_ago
).distinct()

count = inactive_customers.count()
inactive_customers.delete()

# Log the results
with open('/tmp/customer_cleanup_log.txt', 'a') as f:
    f.write(f"{timezone.now()}: Deleted {count} inactive customers\\n")
EOF
["alx-backend-graphql_crm/crm/cron_jobs/clean_inactive_customers.sh"]
["print"]
