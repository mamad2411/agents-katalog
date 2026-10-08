---
description: 
globs: 
alwaysApply: true
---
# Commit Message Rules

## ⚠️ IMPORTANT: ALWAYS USE THE AUTO-COMMIT SCRIPT ⚠️
**All team members must use our auto-commit script instead of regular git commands:**

```bash
npm run commit "description of changes" "Type"
```

Example:
```bash
npm run commit "add dark mode toggle" "Feat"
```

The script automatically:
- Formats the commit message according to our standards
- Determines the appropriate scope based on modified files
- Handles add, commit, and push operations in one command

## Format
All commit messages follow this format:
```
<type>(<scope>): <description>
```

Where:
- `<type>`: The type of change (see below)
- `<scope>`: The area of the codebase affected (component, feature, etc.)
- `<description>`: A brief description of the change

## Types of Commits
- **Feat**: New feature or functionality
  - Example: `Feat(player): add audio speed control`
- **Fix**: Bug fix
  - Example: `Fix(api): resolve authentication token expiration issue`
- **Docs**: Documentation changes
  - Example: `Docs(readme): update installation instructions`
- **Refactor**: Code changes that neither fix bugs nor add features
  - Example: `Refactor(utils): simplify date formatting functions`
- **Style**: Changes related to styling, formatting, or UI (not affecting functionality)
  - Example: `Style(tailwind): update button hover states`
- **Test**: Adding or updating tests
  - Example: `Test(unit): add tests for user authentication`
- **Chore**: Maintenance tasks, dependency updates, etc.
  - Example: `Chore(deps): update dependencies to latest versions`

## Common Scopes
The scope specifies the part of the codebase affected:
- `component`: Changes to UI components
- `api`: Changes to the API layer
- `utils`: Changes to utility functions
- `ui`: Changes to UI library components
- `styles`: Changes to styling or CSS
- `app`: Changes to main application structure
- `page`: Changes to specific pages
- `assets`: Changes to public assets
- `deps`: Dependency updates
- `test`: Test-related changes

## Description Guidelines
The description contains a succinct explanation of the change:
- Use the imperative, present tense: "add" not "added" or "adds"
- Don't capitalize the first letter
- No period (.) at the end

## Workflow Rules
1. Before committing, check for any linting errors or inconsistencies
2. Ensure all code follows the project's style guidelines
3. Verify the changes work as intended before committing
4. Always commit and push the code base after each change
5. Remember to update the relevant documentation when making significant changes

## Auto-commit Tool Usage (REQUIRED)

### Interactive Mode
If you don't provide arguments, the script will prompt you for information:

```bash
npm run commit
```

This will:
1. Show you a list of valid commit types
2. Ask for your commit message
3. Ask you to select a commit type
4. Confirm the formatted commit message before proceeding

### Direct Mode
For quicker commits, provide the message and type directly:

```bash
npm run commit "your commit message" "Type"
```

For example:
```bash
npm run commit "fix user authentication bug" "Fix"
npm run commit "add dark mode toggle" "Feat"
npm run commit "update README installation steps" "Docs"
```

## ❌ DO NOT USE MANUAL GIT COMMANDS ❌
Avoid using manual git commands for committing. If for some reason the auto-commit script cannot be used, the standard command pattern would be:

```
git add . && git commit -m "<type>(<scope>): <description>" && git push --set-upstream origin --force
```

But this approach should only be used in exceptional circumstances with team lead approval.
