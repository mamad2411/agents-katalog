---
name: commit-messages
description: Generate clear, conventional commit messages from staged changes
---

# Commit Message Generator

Generate clear, well-structured commit messages based on the staged changes. Don't add claude co-author credits.

## Process

1. **Analyze staged changes**: Review all staged files to understand what changed and why.

2. **Determine the type of change**:
   - `feat`: A new feature
   - `fix`: A bug fix
   - `refactor`: Code restructuring without behavior change
   - `docs`: Documentation only
   - `test`: Adding or updating tests
   - `chore`: Build, CI, dependency updates
   - `perf`: Performance improvement
   - `style`: Formatting, whitespace (no logic change)

3. **Write the message**:
   - **Subject line**: `type(scope): concise description` (max 72 chars)
   - **Body** (if needed): Explain _why_, not _what_ — the diff shows what changed
   - **Footer** (if needed): Breaking changes, issue references

## Rules

- Use imperative mood: "add feature" not "added feature"
- Don't end the subject with a period
- Keep subject under 72 characters
- Separate subject from body with a blank line
- Body should explain motivation and contrast with previous behavior
- Reference issues when applicable: `Fixes #123`, `Closes #456`

## Output

Provide the commit message ready to use, formatted as:

```
type(scope): subject line

Optional body explaining why the change was made.

Optional footer with references.
```
