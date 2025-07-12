#!/usr/bin/env python3

import os
import sys
import json
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append('/home/banta/Desktop/Projects/alx-backend-graphql_crm')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
import django
django.setup()

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def send_order_reminders():
    # GraphQL endpoint
    url = 'http://localhost:8000/graphql'
    
    # Set up the GraphQL client
    transport = RequestsHTTPTransport(url=url, verify=False, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # Calculate date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # GraphQL query to get pending orders from the last 7 days
    query = gql("""
    query GetPendingOrders($since: String!) {
        allOrders(filter: {
            status: "pending",
            orderDate_Gte: $since
        }) {
            edges {
                node {
                    id
                    orderDate
                    customer {
                        email
                    }
                }
            }
        }
    }
    """)
    
    try:
        # Execute the query
        result = client.execute(query, variable_values={"since": seven_days_ago})
        
        # Get the current timestamp for logging
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Log the results
        log_entries = []
        orders = result.get('allOrders', {}).get('edges', [])
        
        if not orders:
            log_entry = f"{timestamp} - No pending orders found in the last 7 days.\n"
        else:
            log_entry = f"{timestamp} - Found {len(orders)} pending order(s):\n"
            for order in orders:
                order_id = order['node']['id']
                customer_email = order['node']['customer']['email']
                order_date = order['node']['orderDate']
                log_entry += f"  - Order ID: {order_id}, Customer: {customer_email}, Date: {order_date}\n"
        
        # Write to log file
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            f.write(log_entry)
        
        print("Order reminders processed!")
        return True
        
    except Exception as e:
        error_msg = f"{timestamp} - Error processing order reminders: {str(e)}\n"
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            f.write(error_msg)
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    send_order_reminders()
