---
name: gh-create-issue
displayName: Create github issue
description: Create github issue by using user provided instructions an also by exploring current codebase.
version: 1.0.0
tags: [github, issues, management]
---

# Instructions
1. Only include title, description for the issue.
2. use the `gh` cli to create issue. eg: 
```bash
gh issue create --title "test issue title" --body "test issue description"```
3. If the title and body of the issue is not clear enough gather information by exploring the codebase and asking user follow up questions.

# Requirements
1. Only create a plan and ask the user if they would like to change anything. Until proceeds.
2. When asked to proceed only create the github issue and exit. Don't do anything else.
