---
name: setup-github-action
description: Set up Claude Code GitHub Action for automated PR reviews and issue handling
allowed-tools: Bash, Read, Write, Glob
disable-model-invocation: true
---

# Setup Claude Code GitHub Action

Configure the official Claude Code GitHub Action for automated PR reviews and issue handling.

## Prerequisites

- GitHub repository with admin access
- Anthropic API key (for self-hosted) OR Claude GitHub App installed

## Instructions

### Option 1: Claude GitHub App (Recommended)

```bash
# Install the GitHub App
# Run this command and follow the prompts
/install-github-app
```

### Option 2: Self-Hosted with API Key

#### Step 1: Create Workflow File

Create `.github/workflows/claude-code.yml`:

```yaml
name: Claude Code

on:
  pull_request:
    types: [opened, synchronize, reopened]
  issue_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude-review:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          mode: review

  claude-implement:
    if: |
      github.event_name == 'issue_comment' &&
      contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          mode: implement

  claude-auto-assign:
    if: |
      github.event_name == 'issues' &&
      github.event.action == 'assigned' &&
      github.event.assignee.login == 'claude-bot'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          mode: implement
```

#### Step 2: Add API Key Secret

```bash
# Add your Anthropic API key as a repository secret
gh secret set ANTHROPIC_API_KEY
```

#### Step 3: Configure Permissions

Ensure the workflow has appropriate permissions in repository settings:
- Settings → Actions → General → Workflow permissions
- Select "Read and write permissions"
- Check "Allow GitHub Actions to create and approve pull requests"

### Advanced Configurations

#### Path-Specific Reviews

Only trigger reviews for certain file changes:

```yaml
on:
  pull_request:
    paths:
      - 'src/**'
      - '!src/**/*.test.ts'  # Exclude test files
```

#### Custom Review Instructions

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    mode: review
    custom_instructions: |
      Focus on:
      - Security vulnerabilities
      - Performance implications
      - API backward compatibility

      Ignore:
      - Minor style issues (handled by linter)
      - Test coverage (separate workflow)
```

#### Structured Output

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    mode: review
    output_format: json
    output_schema: |
      {
        "type": "object",
        "properties": {
          "approved": {"type": "boolean"},
          "critical_issues": {"type": "array"},
          "suggestions": {"type": "array"}
        }
      }
```

## Usage

### Trigger Review
PRs automatically reviewed on open/update.

### Request Implementation
Comment on any issue:
```
@claude implement this feature
```

### Auto-Assign
Assign the `claude-bot` user to an issue for automatic implementation.

## Output

```markdown
## GitHub Action Setup Complete

### Created Files
- `.github/workflows/claude-code.yml`

### Required Secrets
- `ANTHROPIC_API_KEY` (set via `gh secret set`)

### Features Enabled
- [x] Automatic PR review
- [x] @claude mention implementation
- [x] Auto-assign implementation

### Test It
1. Create a test PR
2. Watch the Actions tab for the review
```

## References

- [Claude Code Action - GitHub Marketplace](https://github.com/marketplace/actions/claude-code-action-official)
- [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)
