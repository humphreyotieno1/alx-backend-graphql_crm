#!/usr/bin/env python3

import os
import sys
import json
from datetime import datetime

# Add the project directory to the Python path
sys.path.append('/home/banta/Desktop/Projects/alx-backend-graphql_crm')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
import django
django.setup()

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock_products():
    # GraphQL endpoint
    url = 'http://localhost:8000/graphql'
    
    # Set up the GraphQL client
    transport = RequestsHTTPTransport(url=url, verify=False, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # GraphQL mutation to update low stock products
    mutation = gql("""
    mutation UpdateLowStockProducts($restockAmount: Int!) {
        updateLowStockProducts(restockAmount: $restockAmount) {
            success
            message
            updatedProducts {
                id
                name
                stock
            }
        }
    }
    """)
    
    try:
        # Execute the mutation with restock amount of 20
        result = client.execute(mutation, variable_values={"restockAmount": 20})
        
        # Get the current timestamp for logging
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Extract the response data
        response = result.get('updateLowStockProducts', {})
        success = response.get('success', False)
        message = response.get('message', 'No message returned')
        updated_products = response.get('updatedProducts', [])
        
        # Format the log entry
        log_entry = f"[{timestamp}] {message}\n"
        
        if updated_products:
            log_entry += "Updated products:\n"
            for product in updated_products:
                log_entry += f"  - {product['name']}: Stock updated to {product['stock']}\n"
        
        # Write to log file
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(log_entry)
        
        print("Low stock products updated successfully!")
        return True
        
    except Exception as e:
        error_msg = f"[{timestamp}] Error updating low stock products: {str(e)}\n"
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(error_msg)
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    update_low_stock_products()
