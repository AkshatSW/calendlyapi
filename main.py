import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    """Load API key from config.json."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        return config['api_key']
    except FileNotFoundError:
        logging.error("config.json file not found.")
        return None
    except KeyError:
        logging.error("API key not found in config.json.")
        return None
    except json.JSONDecodeError:
        logging.error("Error decoding config.json.")
        return None

API_TOKEN = load_config()

if not API_TOKEN:
    raise SystemExit("API token is required. Please check your config.json file.")

def get_user_info():
    logging.info("Retrieving user information...")
    user_url = 'https://api.calendly.com/users/me'
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(user_url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        logging.info("User information retrieved successfully.")
        logging.info(f"Response JSON: {json.dumps(user_data, indent=2)}")
        
        if 'current_organization' in user_data['resource']:
            organization_uri = user_data['resource']['current_organization']
            logging.info(f"Organization URI: {organization_uri}")
            return organization_uri
        else:
            logging.error("No organization information found in the response.")
            return None
    else:
        logging.error(f"Error retrieving user information: {response.status_code}, {response.text}")
        return None

def get_event_types(organization_uri):
    logging.info("Retrieving event types...")
    event_types_url = 'https://api.calendly.com/event_types'
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    params = {
        'organization': organization_uri
    }
    response = requests.get(event_types_url, headers=headers, params=params)
    
    if response.status_code == 200:
        event_types = response.json()
        logging.info("Event types retrieved successfully.")
        logging.info(f"Response JSON: {json.dumps(event_types, indent=2)}")
        
        if 'collection' in event_types:
            for event in event_types['collection']:
                logging.info(f"Event Name: {event['name']}, Event URI: {event['uri']}")
            return event_types
        else:
            logging.error("The 'collection' key was not found in the response.")
            return None
    elif response.status_code == 403:
        logging.error("Permission Denied: Ensure your API token has the correct permissions.")
        logging.error(f"Response: {response.text}")
        return None
    else:
        logging.error(f"Error retrieving event types: {response.status_code}, {response.text}")
        return None

def main():
    organization_uri = get_user_info()
    if organization_uri:
        get_event_types(organization_uri)
    else:
        logging.error("Unable to retrieve organization URI.")

if __name__ == "__main__":
    main()
