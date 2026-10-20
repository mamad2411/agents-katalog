---
description: "Create a new branch with conventional naming based on description"
allowed-tools: ["Bash", "Read"]
---

Create a new git branch with conventional naming based on the provided description.

Usage: `/new-branch <description of the branch purpose>`

Process:
1. **Analyze Description**: Take the provided description and analyze the type of work:
   - **feature/**: New features or enhancements
   - **fix/**: Bug fixes
   - **docs/**: Documentation changes
   - **chore/**: Maintenance tasks, dependency updates
   - **refactor/**: Code refactoring without functional changes
   - **test/**: Adding or updating tests
   - **style/**: Code formatting, styling changes
   - **perf/**: Performance improvements

2. **Extract Keywords**: From the description, extract 2-3 key words that describe the work
   - Remove articles (a, an, the)
   - Use lowercase with hyphens
   - Keep meaningful words only
   - Maximum 50 characters total

3. **Generate Branch Name**: Combine type and keywords
   - Format: `<type>/<keywords-with-hyphens>`
   - Examples:
     - "Add user authentication system" → `feature/user-authentication`
     - "Fix memory leak in parser" → `fix/memory-leak-parser`
     - "Update installation docs" → `docs/installation-update`
     - "Refactor database queries" → `refactor/database-queries`

4. **Create Branch**: 
   - Check current git status
   - Ensure working directory is clean
   - Create and checkout the new branch
   - Show confirmation with branch name

5. **Branch Setup**:
   - Display the new branch name
   - Show current status
   - Suggest next steps (make changes, commit, push)

Example:
```
Input: "Add OAuth2 login integration with Google"
Output: feature/oauth2-google-login
Command: git checkout -b feature/oauth2-google-login
```