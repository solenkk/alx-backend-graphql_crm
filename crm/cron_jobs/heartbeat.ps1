cd C:\Users\cv\OneDrive\Desktop\alx-project\alx-backend-graphql_crm
python manage.py shell -c "
from crm.cron import log_crm_heartbeat
log_crm_heartbeat()
print('Heartbeat logged')"
