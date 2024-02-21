import requests
import xml.etree.ElementTree as ET
import json

def get_user_device_verification_code(client_id):
    device_url = 'https://github.com/login/oauth/authorize'
    payload = {
        'client_id': client_id,
    }
    headers = {
        'Accept': 'application/json'
    }
    session = requests.Session()    
    response = session.post(device_url, json=payload, headers=headers)
    
    print(response.content.decode())
    # return json.loads(response.content.decode())['device_code']

def authenticate_github(client_id, verification_code):
    auth_url = 'https://github.com/login/oauth/access_token'
    payload = {
        'client_id': client_id,
    }
    headers = {
        'Accept': 'application/json'
    }
    response = requests.post(auth_url, json=payload, headers=headers)
    print(response.content.decode())
    # try:
    #     response_json = response.json()
    # except ValueError:
    #     print("Response content:", response.content)
    #     raise
    # if response.status_code == 200:
    #     return response_json['access_token']
    # else:
    #     print("Error response:", response_json)
    #     return None

def get_repositories(access_token):
    headers = {'Authorization': f'token {access_token}'}
    repos_url = 'https://api.github.com/user/repos'
    response = requests.get(repos_url, headers=headers)
    if response.status_code == 200:
        return [repo['full_name'] for repo in response.json()]
    else:
        return []

def get_dependencies(repository):
    pom_url = f'https://raw.githubusercontent.com/{repository}/main/pom.xml'
    response = requests.get(pom_url)
    dependencies = []
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for dependency in root.findall('.//dependency'):
            group_id = dependency.find('groupId').text
            artifact_id = dependency.find('artifactId').text
            version = dependency.find('version').text
            dependencies.append(f"{group_id}: Version {version}")
    return dependencies

if __name__ == "__main__":
    # Step 1: Take Client ID and Client Secret as input
    client_id = input("Enter your GitHub Client ID: ")
    # client_secret = input("Enter your GitHub Client Secret: ")

    verification_code = get_user_device_verification_code(client_id)

    # Step 2: Authenticate with GitHub
    # access_token = authenticate_github(client_id, client_secret)

    # if access_token:
    #     print("Authentication successful.")

    #     # Step 3: Get list of repositories
    #     repositories = get_repositories(access_token)

    #     if repositories:
    #         print(f"Found {len(repositories)} repositories.")

    #         # Step 4: Select one repository
    #         selected_repo = repositories[0]
    #         print(f"Selected repository: {selected_repo}")

    #         # Step 5: Get dependencies from pom.xml
    #         dependencies = get_dependencies(selected_repo)

    #         if dependencies:
    #             print("Dependencies:")
    #             for dependency in dependencies:
    #                 print(dependency)
    #         else:
    #             print("No dependencies found.")
    #     else:
    #         print("No repositories found.")
    # else:
    #     print("Authentication failed.")
