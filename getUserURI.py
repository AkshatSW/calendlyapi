import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace with your actual Calendly API token
API_TOKEN = 'eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzI2MzIzNjA0LCJqdGkiOiJmOGJjNGIyMi02ZjM3LTRjYzQtYTE1OS1mYWMyNGQ0YzMxNGIiLCJ1c2VyX3V1aWQiOiJCR0FGWU5CS0dKSlpBWU9VIn0.78bGiffxAEvkG3ttrAF7rx4IgnzM_OLKTYMADOeMpL_6FeJ0iAb3sKOtKDYDFfaMHaZSaeQTS5ZNoxTnRvVMmQ'

def get_user_uri():
    logging.info("Retrieving user information...")
    user_url = 'https://api.calendly.com/users/me'
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(user_url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        user_uri = user_data['resource']['uri']
        logging.info("User URI retrieved successfully.")
        logging.info(f"User URI: {user_uri}")
        return user_uri
    else:
        logging.error(f"Error retrieving user information: {response.status_code}, {response.text}")
        return None

if __name__ == "__main__":
    get_user_uri()
