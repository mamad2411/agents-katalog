---
description: Run Git and Commit Conventions Check
globs: ['.git/**/*', 'package.json', '.gitignore']
---

# Operations: Git & Commit Conventions

<audit_rules>

- You MUST enforce Conventional Commits format: `type(scope): description`. Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `revert`.
- You MUST ensure commit messages are in the imperative mood (e.g., "Add feature" not "Added feature" or "Adding feature").
- You MUST verify that commit bodies wrap at 72 characters and separate subject from body with a blank line.
- You MUST prevent commits of large binary files (>1MB) to repository history. Use Git LFS or external storage.
- You MUST enforce proper .gitignore configuration to prevent committing sensitive files, build artifacts, or dependency directories.
- You MUST verify branch names follow the convention: `feature/description`, `fix/description`, or `hotfix/description`.
  </audit_rules>

<example_good>

```bash
# Good commit messages
feat(auth): add OAuth2 integration with Google
fix(api): resolve null pointer exception in user service
docs(readme): update installation instructions for Windows
refactor(checkout): extract payment processing into separate module
test(user): add unit tests for email validation
chore(deps): update React to v18.2.0

# Good branch names
feature/oauth-integration
fix/payment-bug
hotfix/security-vulnerability
```

</example_good>

<example_bad>

```bash
# BAD commit messages
"Added login feature" # Wrong mood
"fix:fixed the bug" # Redundant
"update" # Too generic
"feat: add login; fix: update styles; docs: update readme" # Multiple changes in one commit

# BAD branch names
login-feature
bug-fix
master
```

</example_bad>

<example_gitignore>

# .gitignore

# Dependencies

node_modules/
.pnp
.pnp.js

# Production builds

.next/
out/
build/
dist/

# Environment variables

.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs

npm-debug.log*
yarn-debug.log*
yarn-error.log\*

# Runtime data

pids
_.pid
_.seed
\*.pid.lock

# Coverage directory used by tools like istanbul

coverage/
\*.lcov

# IDE

.vscode/
.idea/

# OS

.DS_Store
Thumbs.db

# Large binary files (use Git LFS instead)

_.zip
_.tar.gz
_.exe
_.dmg
</example_gitignore>
