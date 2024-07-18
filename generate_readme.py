import os
import requests
import base64

def fetch_readme_content():
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
    headers = {'Authorization': f'token {token}'}
    response = requests.get(f'https://api.github.com/repos/IdrisFallout-Selfhosted/.github/contents/profile/README.md', headers=headers)
    readme_data = response.json()

    # Decode base64 content
    readme_content = base64.b64decode(readme_data['content']).decode('utf-8')

    return readme_content

def update_readme_with_repos():
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Fetch repositories from GitHub API
    response = requests.get(f'https://api.github.com/orgs/{org}/repos', headers=headers)
    repos = response.json()

    # Generate Markdown table for repositories
    markdown_table = "\n## Repositories\n\n"
    markdown_table += "| Repository |\n"
    markdown_table += "|------------|\n"
    for repo in repos:
        markdown_table += f"| [{repo['name']}]({repo['html_url']}) |\n"

    # Append table to existing README content
    readme_content = fetch_readme_content()
    updated_readme_content = readme_content + markdown_table

    # Base64 encode the updated content
    encoded_content = base64.b64encode(updated_readme_content.encode('utf-8')).decode('utf-8')

    # Commit changes using GitHub REST API
    commit_message = "Update README with organization repository list"
    api_url = f'https://api.github.com/repos/IdrisFallout-Selfhosted/.github/contents/profile/README.md'
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "sha": readme_data['sha']
    }

    response = requests.put(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("README.md updated successfully.")
    else:
        print(f"Failed to update README.md. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    update_readme_with_repos()
