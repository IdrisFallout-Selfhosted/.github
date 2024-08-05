import os
import requests


def get_repos(org, token):
    repos = []
    page = 1
    while True:
        response = requests.get(f'https://api.github.com/orgs/{org}/repos',
                                headers={'Authorization': f'token {token}'},
                                params={'per_page': 100, 'page': page})
        if response.status_code == 200:
            repo_data = response.json()
            if not repo_data:
                break
            repos.extend(repo['name'] for repo in repo_data)
            page += 1
        else:
            print(f"Failed to fetch repositories. Status code: {response.status_code}")
            print(response.text)
            break
    return repos


def is_contributor(repo_name, user, org, token):
    response = requests.get(f'https://api.github.com/repos/{org}/{repo_name}/collaborators/{user}/permission',
                            headers={'Authorization': f'token {token}'})
    if response.status_code == 200:
        permission = response.json().get('permission', '')
        return permission in ['admin', 'write']
    return False


def main():
    org = os.getenv('GITHUB_ORGANIZATION')
    token = os.getenv('GITHUB_TOKEN')
    user = os.getenv('COMMITTER_NAME')

    if not org or not token or not user:
        print(
            "Error: One or more environment variables (GITHUB_ORGANIZATION, GITHUB_TOKEN, COMMITTER_NAME) are not set.")
        return

    # Get all repos in the organization
    repos = get_repos(org, token)

    # Check contributor status for each repo
    for repo in repos:
        if is_contributor(repo, user, org, token):
            print(repo)


if __name__ == "__main__":
    main()
