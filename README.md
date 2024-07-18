#.github

Automates the fetching and printing of GitHub repositories of the authenticated user using the GitHub API.

## Requirements

- Python 3.x
- A GitHub personal access token with the `public_repo` scope

## Usage

```
python generate_readme.py
```

This will print a list of your GitHub repositories and their URLs to the console.

## Code Explanation

The `generate_readme.py` script performs the following steps:

1. Imports the necessary modules.
2. Retrieves the GitHub personal access token from the environment variable `GITHUB_TOKEN`.
3. Creates a request header with the `Authorization` header set to the token.
4. Sends a GET request to the GitHub API's `/user/repos` endpoint to fetch the list of repositories.
5. Parses the response as JSON and iterates over the list of repositories.
6. For each repository, prints the repository name and its URL to the console.