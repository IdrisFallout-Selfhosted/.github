import os
import requests
import base64

def fetch_readme_content():
    """
    Fetches the current content of README.md from the specified GitHub repository.
    """
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
        return readme_content
    else:
        print(f"Failed to fetch README.md. Status code: {response.status_code}")
        print(response.text)
        return None

def update_readme_with_repos():
    """
    Updates the README.md in the specified GitHub repository with a table listing organization repositories.
    """
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
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

        # Generate Markdown table for repositories
        markdown_table = "\n## Repositories\n\n"
        markdown_table += "| Repository |\n"
        markdown_table += "|------------|\n"
        for repo in repos:
            markdown_table += f"| [{repo['name']}]({repo['html_url']}) |\n"

        # Append table to existing README content
        readme_content = fetch_readme_content()

        if readme_content:
            updated_readme_content = readme_content + markdown_table

            # Base64 encode the updated content
            encoded_content = base64.b64encode(updated_readme_content.encode('utf-8')).decode('utf-8')

            # Fetch latest README sha
            readme_data = requests.get(f'https://api.github.com/repos/{org}/.github/contents/profile/README.md', headers=headers).json()
            sha = readme_data['sha']

            # Commit changes using GitHub REST API
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
