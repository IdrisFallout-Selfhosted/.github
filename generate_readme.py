import os
import requests

def fetch_repo_names():
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Fetch repositories from GitHub API
    response = requests.get(f'https://api.github.com/orgs/{org}/repos', headers=headers)

    if response.status_code == 200:
        repos = response.json()
        # Print only the repository names
        for repo in repos:
            print(repo['name'])
    else:
        print(f"Failed to fetch repositories. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_repo_names()
