import os
import requests
import base64


def fetch_readme_content():
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
    headers = {
        'Authorization': f'token {token}',
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
            repos.extend(repo_data)
            page += 1
        else:
            print(f"Failed to fetch repositories. Status code: {response.status_code}")
            print(response.text)
            break
    return repos


def update_readme_with_repos():
    token = os.getenv('GITHUB_TOKEN')
    org = os.getenv('GITHUB_ORGANIZATION')
    committer_name = os.getenv('COMMITTER_NAME')
    committer_email = os.getenv('COMMITTER_EMAIL')
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }

    # Fetch repositories from GitHub API
    repos = get_repos(org, token)

    # Generate Markdown table for repositories
    markdown_table = "| Repository | Description | Visibility |\n"
    markdown_table += "|------------|-------------|------------|\n"
    for repo in repos:
        # Fetch repository description
        description = repo['description'] if repo['description'] else "No description provided."
        visibility = "<span style='color:red'>Private</span>" if repo[
            'private'] else "<span style='color:green'>Public</span>"
        markdown_table += f"| [{repo['name']}]({repo['html_url']}) | {description} | {visibility} |\n"

    # Fetch current README content and SHA
    readme_content, sha = fetch_readme_content()
    if readme_content is not None and sha is not None:
        # Check if a section already exists in README content
        start_index = readme_content.find("## Repositories")
        if start_index != -1:
            end_index = readme_content.find("## ", start_index + 1)
            if end_index == -1:
                end_index = len(readme_content)

            # Remove the existing table if it exists
            updated_readme_content = readme_content[
                                     :start_index] + "## Repositories\n\n" + markdown_table + readme_content[end_index:]
        else:
            # Append new section and table
            updated_readme_content = readme_content + "\n## Repositories\n\n" + markdown_table

        # Base64 encode the updated content
        encoded_content = base64.b64encode(updated_readme_content.encode('utf-8')).decode('utf-8')

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


if __name__ == "__main__":
    update_readme_with_repos()
