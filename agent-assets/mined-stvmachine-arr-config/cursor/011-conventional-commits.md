---
description: Use when user asks to commit
alwaysApply: false
---
# Conventional Commits

When committing changes, use the Conventional Commit Messages specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Common Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks
- `style`: Code style changes (formatting, etc.)

## Examples

- `feat(docker): add tdarr service`
- `fix(scripts): correct user group setup`
- `docs: update README with service ports`
- `refactor: move Python scripts to scripts/ directory`

## Specification Details

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

- Commits MUST be prefixed with a type, which consists of a noun, feat, fix, etc., followed by the OPTIONAL scope, OPTIONAL !, and REQUIRED terminal colon and space.
- The type `feat` MUST be used when a commit adds a new feature to your application or library.
- The type `fix` MUST be used when a commit represents a bug fix for your application.
- A scope MAY be provided after a type. A scope MUST consist of a noun describing a section of the codebase surrounded by parenthesis, e.g., `fix(parser):`
- A description MUST immediately follow the colon and space after the type/scope prefix. The description is a short summary of the code changes.
- A longer commit body MAY be provided after the short description, providing additional contextual information about the code changes. The body MUST begin one blank line after the description.
- Breaking changes MUST be indicated in the type/scope prefix of a commit, or as an entry in the footer.
- If included as a footer, a breaking change MUST consist of the uppercase text BREAKING CHANGE, followed by a colon, space, and description.
