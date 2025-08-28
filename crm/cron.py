"""
Cron jobs for the CRM application
"""

import os
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

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

def update_low_stock():
    """
    Cron job that updates low-stock products every 12 hours
    Executes the UpdateLowStockProducts mutation and logs results
    """
    try:
        timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
        
        # Set up GraphQL client
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=True,
            retries=3,
            timeout=30
        )
        
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Define the mutation - MUST match the exact GraphQL mutation name
        mutation = gql("""
            mutation UpdateLowStockProducts {
                updateLowStockProducts(increment: 10) {
                    message
                    updatedCount
                    products {
                        name
                        stock
                    }
                }
            }
        """)
        
        # Execute the mutation
        result = client.execute(mutation)
        update_data = result['updateLowStockProducts']
        
        # Log the results to the REQUIRED file path
        log_file = '/tmp/low_stock_updates_log.txt'
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} - {update_data['message']}\n")
            f.write(f"{timestamp} - Updated {update_data['updatedCount']} products\n")
            
            if update_data['products']:
                for product in update_data['products']:
                    f.write(f"{timestamp} - Product: {product['name']}, New Stock: {product['stock']}\n")
            else:
                f.write(f"{timestamp} - No low-stock products found\n")
        
        print(f"Low stock update completed: {update_data['message']}")
        return True
        
    except Exception as e:
        # Error logging
        error_log = '/tmp/low_stock_updates_error_log.txt'
        with open(error_log, 'a') as f:
            f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} Low stock update failed: {str(e)}\n")
        
        print(f"Low stock update failed: {e}")
        return False