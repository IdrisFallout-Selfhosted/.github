import os
import requests

user = os.getenv('COMMITTER_NAME')

def is_contributor(repo_name, user, token, org):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(f'https://api.github.com/repos/{org}/{repo_name}/collaborators/{user}/permission', headers=headers)

    if response.status_code == 200:
        permission = response.json().get('permission', '')
        return permission in ['admin', 'write']
    return False

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
        for repo in repos:
            repo_name = repo['name']
            if is_contributor(repo_name, user, token, org):
                print(repo_name)
    else:
        print(f"Failed to fetch repositories. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_repo_names()
