# MCP (Model Control Protocol) Documentation

This document outlines how the MCP servers are used in the cozy_youtube_videos project for GitHub integration and other external services.

## Overview

The Model Control Protocol (MCP) allows our AI assistants to interact with external services like GitHub, enabling repository management, file operations, and other integrations directly from the Cursor IDE.

## GitHub Integration

### Repository Management

#### Creating Repositories
```
mcp__create_repository
- name: Repository name (required)
- description: Repository description
- private: Whether the repository should be private (default: false)
- autoInit: Whether to initialize with README (default: false)
```

#### Forking Repositories
```
mcp__fork_repository
- owner: Original repository owner (required)
- repo: Repository name (required)
- organization: Organization to fork to (optional)
```

#### Creating Branches
```
mcp__create_branch
- owner: Repository owner (required)
- repo: Repository name (required)
- branch: Name for the new branch (required)
- from_branch: Source branch (optional, defaults to main/master)
```

### File Operations

#### Getting File Contents
```
mcp__get_file_contents
- owner: Repository owner (required)
- repo: Repository name (required)
- path: Path to the file or directory (required)
- branch: Branch to get contents from (optional)
```

#### Creating or Updating Files
```
mcp__create_or_update_file
- owner: Repository owner (required)
- repo: Repository name (required)
- path: Path where to create/update the file (required)
- message: Commit message (required)
- content: Content of the file (required)
- branch: Branch to create/update the file in (required)
- sha: SHA of the file being replaced (required when updating)
```

#### Pushing Multiple Files
```
mcp__push_files
- owner: Repository owner (required)
- repo: Repository name (required)
- branch: Branch to push to (required)
- message: Commit message (required)
- files: Array of files to push (required)
  - path: File path (required)
  - content: File content (required)
```

### Issue and Pull Request Management

#### Creating Issues
```
mcp__create_issue
- owner: Repository owner (required)
- repo: Repository name (required)
- title: Issue title (required)
- body: Issue description
- labels: Array of labels
- assignees: Array of assignees
- milestone: Milestone number
```

#### Creating Pull Requests
```
mcp__create_pull_request
- owner: Repository owner (required)
- repo: Repository name (required)
- title: Pull request title (required)
- head: Branch with changes (required)
- base: Branch to merge into (required)
- body: Pull request description
- draft: Whether it's a draft PR
- maintainer_can_modify: Whether maintainers can modify
```

### Search Operations

#### Searching Repositories
```
mcp__search_repositories
- query: Search query (required)
- page: Page number for pagination
- perPage: Results per page (max: 100)
```

#### Searching Code
```
mcp__search_code
- q: Search query (required)
- order: Sort order (asc/desc)
- page: Page number
- per_page: Results per page (max: 100)
```

#### Searching Issues and PRs
```
mcp__search_issues
- q: Search query (required)
- sort: Sort field
- order: Sort order (asc/desc)
- page: Page number
- per_page: Results per page (max: 100)
```

#### Searching Users
```
mcp__search_users
- q: Search query (required)
- sort: Sort field
- order: Sort order (asc/desc)
- page: Page number
- per_page: Results per page (max: 100)
```

## Best Practices

1. **Authentication**: MCP handles authentication automatically, but ensure you have the necessary permissions for the operations you're performing.

2. **Rate Limiting**: Be mindful of GitHub's rate limits. Avoid making too many requests in a short period.

3. **Error Handling**: Always check for errors in the response and handle them appropriately.

4. **Large Files**: Avoid pushing very large files through MCP. GitHub has file size limits (typically 100MB).

5. **Sensitive Information**: Never commit sensitive information like API keys, passwords, or personal data.

6. **Atomic Commits**: Make commits atomic (focused on a single change) when possible.

7. **Descriptive Messages**: Use clear, descriptive commit messages that explain the purpose of the change.

## Project-Specific Usage

For the cozy_youtube_videos project, we primarily use MCP for:

1. **Repository Management**: Creating and maintaining the project repository
2. **File Operations**: Adding and updating project files
3. **Documentation**: Keeping README, PROJECT_GUIDE, and other documentation up to date

### Example: Adding a New Script

```python
# Example of using MCP to add a new utility script
mcp__create_or_update_file(
    owner="beaubranton4",
    repo="cozy_youtube_videos",
    path="scripts/utils/new_utility.py",
    message="Add new utility script for XYZ functionality",
    content="#!/usr/bin/env python3\n\n# Script content here...",
    branch="main"
)
```

### Example: Creating an Issue for a Feature Request

```python
# Example of using MCP to create an issue
mcp__create_issue(
    owner="beaubranton4",
    repo="cozy_youtube_videos",
    title="Feature Request: Automatic Thumbnail Generation",
    body="It would be helpful to have a script that automatically generates thumbnails based on video content.",
    labels=["enhancement", "automation"]
)
```

## Troubleshooting

If you encounter issues with MCP:

1. Check that you're using the correct parameters for the function
2. Verify that you have the necessary permissions for the operation
3. Check for rate limiting issues
4. Look for error messages in the response
5. Try breaking down complex operations into smaller steps