import os
import requests
import base64

def fetch_readme_content():
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://api.github.com/repos/{org}/.github/contents/profile/README.md', headers=headers)

    if response.status_code == 200:
        readme_data = response.json()
        # Decode base64 content
        readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        return readme_content, readme_data['sha']
    elif response.status_code == 404:
        return None, None  # README.md not found
    else:
        print(f"Failed to fetch README.md. Status code: {response.status_code}")
        print(response.text)
        return None, None

def is_contributor(repo_name, user):
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://api.github.com/repos/{org}/{repo_name}/collaborators/{user}/permission', headers=headers)

    if response.status_code == 200:
        permission = response.json().get('permission', '')
        return permission in ['admin', 'write']
    return False

def update_readme_with_repos():
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
    user = os.getenv('GITHUB_USERNAME')
    committer_name = os.getenv('COMMITTER_NAME')
    committer_email = os.getenv('COMMITTER_EMAIL')
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }

    # Fetch repositories from GitHub API
    response = requests.get(f'https://api.github.com/orgs/{org}/repos', headers=headers)

    if response.status_code == 200:
        repos = response.json()
        print(f"Fetched repositories: {repos}")  # Debugging info

        # Generate Markdown table for repositories
        markdown_table = "\n## Repositories\n\n"
        markdown_table += "| Repository | Description | Visibility |\n"
        markdown_table += "|------------|-------------|------------|\n"

        for repo in repos:
            repo_name = repo['name']
            is_contrib = is_contributor(repo_name, user)
            if is_contrib:
                description = repo['description'] if repo['description'] else "No description provided."
                visibility = "<span style='color:red'>Private</span>" if repo['private'] else "<span style='color:green'>Public</span>"
                markdown_table += f"| [{repo_name}]({repo['html_url']}) | {description} | {visibility} |\n"

        print(markdown_table)  # Debugging info

        # Fetch current README content and SHA
        readme_content, sha = fetch_readme_content()
        if readme_content is not None and sha is not None:
            start_index = readme_content.find("## Repositories")
            if start_index != -1:
                readme_content = readme_content[:start_index].strip()
                updated_readme_content = readme_content + markdown_table
            else:
                updated_readme_content = readme_content + markdown_table

            encoded_content = base64.b64encode(updated_readme_content.encode('utf-8')).decode('utf-8')

            commit_message = "Update README with organization repository list"
            api_url = f'https://api.github.com/repos/{org}/.github/contents/profile/README.md'
            payload = {
                "message": commit_message,
                "content": encoded_content,
                "sha": sha,
                "committer": {"name": committer_name, "email": committer_email}
            }

            response = requests.put(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                print("README.md updated successfully.")
            else:
                print(f"Failed to update README.md. Status code: {response.status_code}")
                print(response.text)
        else:
            print("Failed to fetch README content.")
    else:
        print(f"Failed to fetch repositories. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    update_readme_with_repos()
