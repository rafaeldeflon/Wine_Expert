# This is a scrip to test the flask API.

import requests
import json

# URL of the Flask application (when the flask app is executed the url is genareted)
url = 'http://127.0.0.1:5000/predict'

# Load the test data from the JSON file (input the path to the json testing file)
with open('/YOUR_PATH', 'r') as file:
    data = json.load(file)

# Set the headers
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'test-script'  
}

# Send a POST request to the Flask application with the test data
response = requests.post(url, headers=headers, json=data)

# Check the status code and handle errors
status_code = response.status_code
print('Status Code:', status_code)

if status_code == 200:
    try:
        response_json = response.json()
        print('Response JSON:', response_json)
    except requests.exceptions.JSONDecodeError:
        print('Error: Response is not in JSON format')
else:
    print('Error: Received status code', status_code)
    print('Response Text:', response.text)
