#!/usr/bin/env python3
import jwt
import time
import sys
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Get PEM file path
pem = sys.argv[1]

# Get the Client ID
client_id = sys.argv[2]

# Open PEM
with open(pem, 'rb') as pem_file:
    private_key = serialization.load_pem_private_key(
        pem_file.read(),
        password=None,
        backend=default_backend()
    )

payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600,
    
    # GitHub App's client ID
    'iss': client_id
}

# Create JWT
encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')

print(f"JWT:  {encoded_jwt}")

installation_id=50723686

# Define the API URL
url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"

# Define the headers
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {encoded_jwt}",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Make the POST request
response = requests.post(url, headers=headers)

response_json = response.json()
access_token = response_json.get('token')
print("Token:", access_token)

# Print the response
print("Response Status Code:", response.status_code)
#print("Response Body:", response.json.get('token'))

headers_trigger_workflow = {
    "Accept": "application/vnd.github.everest-preview+json",
    "Authorization": f"Bearer {access_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

data = {
    "event_type": "argocd-event"
}

url_trigger_workflow = f"https://api.github.com/repos/P304821/python-hello-post-sync/dispatches"

response_trigger_workflow = requests.post(url_trigger_workflow, headers=headers_trigger_workflow, json=data)

print("Response Status Code:", response_trigger_workflow.status_code)
