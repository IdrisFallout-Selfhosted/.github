import os
import requests

def fetch_repos():
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
    headers = {'Authorization': f'token {token}'}
    response = requests.get(f'https://api.github.com/orgs/{org}/repos', headers=headers)
    repos = response.json()

    repo_list = []
    for repo in repos:
        repo_list.append(f'| [{repo["name"]}]({repo["html_url"]}) | {repo["description"] or "No description"} |')

    return repo_list

def update_readme(repo_list):
    readme_path = 'README.md'

    table_header = "| Repository | Description |\n|------------|-------------|\n"
    table_rows = "\n".join(repo_list)

    with open(readme_path, 'a') as readme_file:
        readme_file.write("\n## Organization Repositories\n")
        readme_file.write(table_header)
        readme_file.write(table_rows)
        readme_file.write("\n")

if __name__ == "__main__":
    repos = fetch_repos()
    update_readme(repos)
