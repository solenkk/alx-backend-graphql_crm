#!/usr/bin/env python3
"""
Script to send order reminders for pending orders from the last 7 days
using GraphQL queries.
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
import django
django.setup()

async def send_order_reminders():
    """Query GraphQL for recent orders and log reminders"""
    
    # GraphQL endpoint
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql/")
    
    async with Client(
        transport=transport,
        fetch_schema_from_transport=True,
    ) as session:
        # Calculate date 7 days ago
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        # GraphQL query to get recent orders with customer emails
        query = gql("""
            query GetRecentOrders($since: String!) {
                recentOrders(days: 7) {
                    id
                    product
                    quantity
                    created_at
                    customer {
                        name
                        email
                    }
                }
            }
        """)
        
        try:
            # Execute the query
            result = await session.execute(query, variable_values={"since": seven_days_ago})
            
            # Process the results
            orders = result.get('recentOrders', [])
            
            # Log the results
            log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Found {len(orders)} recent orders\n"
            
            for order in orders:
                customer = order.get('customer', {})
                log_message += f"  Order ID: {order.get('id')}, Customer Email: {customer.get('email', 'N/A')}\n"
            
            # Write to log file
            log_dir = '/tmp'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            with open('/tmp/order_reminders_log.txt', 'a') as f:
                f.write(log_message + "\n")
            
            print("Order reminders processed!")
            print(f"Logged {len(orders)} orders to /tmp/order_reminders_log.txt")
            
        except Exception as e:
            error_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}\n"
            with open('/tmp/order_reminders_log.txt', 'a') as f:
                f.write(error_msg)
            print(f"Error processing order reminders: {e}")

def main():
    """Main function to run the async task"""
    asyncio.run(send_order_reminders())

if __name__ == "__main__":
    main()