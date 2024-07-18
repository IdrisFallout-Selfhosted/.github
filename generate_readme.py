import os
import requests

def fetch_repos():
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'}
    response = requests.get('https://api.github.com/user/repos', headers=headers)
    repos = response.json()

    for repo in repos:
        print(f'Repo name: {repo["name"]} - URL: {repo["html_url"]}')

if __name__ == "__main__":
    fetch_repos()