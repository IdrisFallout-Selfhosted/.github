import os
import requests

def fetch_repos(org):
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'}
    response = requests.get(f'https://api.github.com/orgs/{org}/repos', headers=headers)
    repos = response.json()

    markdown_table = ""
    for repo in repos:
        markdown_table += f"| [{repo['name']}]({repo['html_url']}) |\n"

    return markdown_table

if __name__ == "__main__":
    org = os.getenv('GITHUB_ORGANIZATION')
    markdown_content = fetch_repos(org)

    with open('README.md', 'a') as f:
        f.write("\n## Repositories\n")
        f.write(markdown_content)
