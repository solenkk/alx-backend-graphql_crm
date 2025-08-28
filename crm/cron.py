"""
Cron jobs for the CRM application
"""

import os
from datetime import datetime
from django.utils import timezone

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
            from gql.transport.aiohttp import AIOHTTPTransport
            import asyncio
            
            async def test_graphql():
                transport = AIOHTTPTransport(url="http://localhost:8000/graphql/")
                async with Client(transport=transport) as session:
                    query = gql("""
                        query {
                            __schema {
                                types {
                                    name
                                }
                            }
                        }
                    """)
                    await session.execute(query)
                    return True
            
            # Run the test
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(test_graphql())
            
            if result:
                with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                    f.write(f"{timestamp} GraphQL endpoint is responsive\n")
                    
        except Exception as e:
            with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                f.write(f"{timestamp} GraphQL test failed: {str(e)}\n")
        
        return True
        
    except Exception as e:
        # If file logging fails, print to console
        print(f"Heartbeat logging failed: {e}")
        return False