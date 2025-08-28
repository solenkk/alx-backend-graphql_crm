import os
from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    """
    Celery task to generate weekly CRM report
    Summarizes total orders, customers, and revenue
    """
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Set up GraphQL client
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=True,
            retries=3,
            timeout=30
        )
        
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Define the GraphQL query to get report data
        query = gql("""
            query GenerateCRMReport {
                totalCustomers: customers_aggregate {
                    aggregate {
                        count
                    }
                }
                totalOrders: orders_aggregate {
                    aggregate {
                        count
                    }
                }
                totalRevenue: orders_aggregate {
                    aggregate {
                        sum {
                            totalAmount
                        }
                    }
                }
            }
        """)
        
        # Execute the query
        result = client.execute(query)
        
        # Extract data from response
        total_customers = result['totalCustomers']['aggregate']['count']
        total_orders = result['totalOrders']['aggregate']['count']
        total_revenue = result['totalRevenue']['aggregate']['sum']['totalAmount'] or 0
        
        # Format the report message
        report_message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue:.2f} revenue"
        
        # Log the report to file
        log_file = '/tmp/crm_report_log.txt'
        with open(log_file, 'a') as f:
            f.write(report_message + '\n')
        
        print(f"CRM report generated: {report_message}")
        return report_message
        
    except Exception as e:
        # Error logging
        error_log = '/tmp/crm_report_error_log.txt'
        error_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Report generation failed: {str(e)}"
        
        with open(error_log, 'a') as f:
            f.write(error_message + '\n')
        
        print(error_message)
        return 
    ["import requests"]