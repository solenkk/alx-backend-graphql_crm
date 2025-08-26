#!/usr/bin/env pwsh

# Navigate to your actual project directory
Set-Location -Path "C:\Users\cv\OneDrive\Desktop\alx-project\alx-backend-graphql_crm"

# Execute Django management command to delete inactive customers
python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta

print('Starting customer cleanup...')

# First, let's check what models are available
import crm.models
print('Available models:', [name for name in dir(crm.models) if not name.startswith('_')])

# Try to import specific models - adjust based on what you find above
try:
    # Try common model names - adjust these based on what you found
    from crm.models import Customer, Order
    print('Successfully imported Customer and Order models')
    
    # Find customers with no orders in the last year
    one_year_ago = timezone.now() - timedelta(days=365)

    # Customers with no orders at all
    customers_no_orders = Customer.objects.filter(order__isnull=True)

    # Customers with orders, but none in the last year
    customers_old_orders = Customer.objects.filter(
        order__created_at__lt=one_year_ago
    ).exclude(
        order__created_at__gte=one_year_ago
    ).distinct()

    # Combine both sets
    inactive_customers = customers_no_orders | customers_old_orders
    count = inactive_customers.count()

    print(f'Found {count} inactive customers to delete')

    if count > 0:
        inactive_customers.delete()
        print(f'Deleted {count} inactive customers')

    # Log the results
    import os
    log_dir = 'C:/tmp'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    with open('C:/tmp/customer_cleanup_log.txt', 'a') as f:
        f.write(f'{timezone.now()}: Deleted {count} inactive customers\n')

    print('Cleanup completed successfully')

except ImportError as e:
    print(f'Import error: {e}')
    print('Please check your model names and update the script accordingly')
except Exception as e:
    print(f'Error during cleanup: {e}')
"