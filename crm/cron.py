import datetime
import requests
from gql import gql,client
from gql.transport.requests import RequestsHTTPTransport, Client
LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    """
    Logs a heartbeat message with timestamp to a log file every 5 minutes.
    Optionally queries the GraphQL hello field to verify endpoint responsiveness.
    """
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Optional: check GraphQL 'hello' field
    try:
        query = """
        query {
          hello
        }
        """
        response = requests.post(
            GRAPHQL_ENDPOINT,
            json={'query': query},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        graphql_status = "OK" if 'data' in data and 'hello' in data['data'] else "Failed"
    except Exception:
        graphql_status = "Failed"

    message = f"{now} CRM is alive - GraphQL status: {graphql_status}\n"

    with open(LOG_FILE, "a") as f:
        f.write(message)
