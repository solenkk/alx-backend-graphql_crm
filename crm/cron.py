"""
Cron jobs for the CRM application
"""

import os
from datetime import datetime

def log_crm_heartbeat():
    """
    Log a heartbeat message every 5 minutes to confirm CRM health
    """
    try:
        # Create timestamp
        timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
        message = f"{timestamp} CRM is alive"
        
        # Log to file
        log_dir = '/tmp'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(message + "\n")
        
        # Optional: Verify GraphQL endpoint is responsive
        try:
            from gql import gql, Client
            from gql.transport.requests import RequestsHTTPTransport
            
            # Use synchronous transport instead of async for cron jobs
            transport = RequestsHTTPTransport(
                url="http://localhost:8000/graphql/",
                verify=True,
                retries=2,
                timeout=5
            )
            
            client = Client(transport=transport, fetch_schema_from_transport=True)
            
            # Simple query to test endpoint
            query = gql("""
                query {
                    hello
                }
            """)
            
            result = client.execute(query)
            
            # Log successful response
            with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                f.write(f"{timestamp} GraphQL endpoint responsive: {result.get('hello', 'OK')}\n")
                
        except ImportError:
            # gql library not available, skip GraphQL test
            with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                f.write(f"{timestamp} GraphQL test skipped (gql not installed)\n")
                
        except Exception as e:
            # Log GraphQL connection error but don't fail the cron job
            with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                f.write(f"{timestamp} GraphQL test failed: {str(e)}\n")
        
        return True
        
    except Exception as e:
        # If file logging fails, create error log
        try:
            with open('/tmp/crm_heartbeat_error_log.txt', 'a') as f:
                f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} Heartbeat logging failed: {str(e)}\n")
        except:
            # Final fallback - print to console
            print(f"Heartbeat logging failed: {e}")
        return False