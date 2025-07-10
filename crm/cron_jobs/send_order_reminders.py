#!/usr/bin/env python3
"""
Script to query pending orders from GraphQL endpoint and
log order reminders. Designed to be run daily via cron.
"""

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


def main() -> None:
    """
    Queries orders from the last 7 days and logs reminders.
    """
    # Calculate date 7 days ago in ISO format (assuming order_date stored as ISO strings)
    seven_days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat()

    # Set up the GraphQL client
    transport = RequestsHTTPTransport(
        url=GRAPHQL_ENDPOINT,
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    # GraphQL query to get orders with order_date >= seven_days_ago
    query = gql(
        """
        query ($since: DateTime!) {
          orders(filter: { order_date_gte: $since }) {
            edges {
              node {
                id
                customer {
                  email
                }
                order_date
              }
            }
          }
        }
        """
    )

    params = {"since": seven_days_ago}

    try:
        result = client.execute(query, variable_values=params)
        orders = result.get("orders", {}).get("edges", [])

        with open(LOG_FILE, "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for edge in orders:
                order = edge["node"]
                order_id = order["id"]
                email = order["customer"]["email"] if order.get("customer") else "No email"
                log_file.write(f"{timestamp} Order ID: {order_id}, Customer Email: {email}\n")

        print("Order reminders processed!")
    except Exception as e:
        print(f"Error during GraphQL query or logging: {e}")


if __name__ == "__main__":
    main()
