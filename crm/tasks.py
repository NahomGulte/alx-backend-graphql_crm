#!/usr/bin/env python3
"""
Celery task to generate weekly CRM report using GraphQL.
"""

import datetime
import requests
from celery import shared_task

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/crm_report_log.txt"

@shared_task
def generate_crm_report():
    """
    Fetches total customers, orders, and revenue from GraphQL and logs it.
    """
    query = """
    query {
      allCustomers {
        totalCount
      }
      allOrders {
        totalCount
        edges {
          node {
            totalAmount
          }
        }
      }
    }
    """

    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            json={'query': query},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()['data']

        customer_count = data['allCustomers']['totalCount']
        order_count = data['allOrders']['totalCount']
        revenue = sum(
            float(edge["node"]["totalAmount"])
            for edge in data["allOrders"]["edges"]
        )

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} - Report: {customer_count} customers, {order_count} orders, {revenue:.2f} revenue\n")

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.datetime.now()} - Failed to generate report: {str(e)}\n")
