## .github

This is a repository containing automated scripts for managing the profile section of the organization's GitHub page.

### Functionality

- Fetches the latest repository list from the organization.
- Updates the README.md file with a markdown table containing the repository name, description, and visibility.
- Commits the changes to the organization's .github/profile/README.md file.

### Required Environment Variables

- `GITHUB_TOKEN`: A personal access token with sufficient permissions to update the organization's repository.
- `GITHUB_ORGANIZATION`: The name of the organization to update the repository list for.
- `COMMITTER_NAME`: The name of the committer to be used in the git commit.
- `COMMITTER_EMAIL`: The email address of the committer to be used in the git commit.

### Usage

To use the script, simply run the following command:

```
python generate_readme.py
```

### Notes

- The script assumes that the organization's profile repository is named `.github`.
- The script only updates the README.md file in the organization's `.github/profile` directory.
- The script does not delete any existing repository list in the README.md file. If you want to remove the existing list, you will need to edit the README.md file manually.