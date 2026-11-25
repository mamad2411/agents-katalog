---
name: devops
description: Day-to-day DevOps for solo developers and small teams — git workflow (status, branches, commits, rebase), conventional commit messages, deployment basics, environment variables, and CI/CD fundamentals. Use when the user asks about git commands, resolving merge conflicts, setting up a deployment, managing .env files, or understanding a CI pipeline. Not a Kubernetes or cloud-architecture reference.
---

# Skill: DevOps

> **Purpose**: Manage code, deploy, and automate with confidence.

## When to Use
- Git workflow questions
- Deployment setup
- Environment configuration
- CI/CD understanding

---

## Git Workflow

### Daily Commands
```bash
# Check status
git status

# Stage and commit
git add .
git commit -m "fix: resolve null pointer in UserService"

# Push to remote
git push origin main
```

### Commit Message Format
```
type: short description

Types:
  feat:     New feature
  fix:      Bug fix
  refactor: Code change that neither fixes nor adds
  docs:     Documentation only
  test:     Adding/updating tests
  chore:    Build, config, tooling changes
```

### Branching Strategy
```bash
# Create feature branch
git checkout -b feature/add-user-search

# Work on it, commit...
git add .
git commit -m "feat: add user search by email"

# Push branch
git push origin feature/add-user-search

# After review, merge to main
git checkout main
git pull origin main
git merge feature/add-user-search
git push origin main

# Clean up
git branch -d feature/add-user-search
```

### Undo Mistakes
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git checkout -- .

# Fix last commit message
git commit --amend -m "correct message"

# Unstage a file
git reset HEAD file.txt
```

---

## Environment Variables

### Why
Never hardcode secrets, URLs, or config that changes between environments.

### How (Node.js)
```bash
# .env file (NEVER commit this)
DB_HOST=localhost
DB_PORT=5432
API_KEY=sk-abc123
```

```javascript
// Load with dotenv
require('dotenv').config();
const dbHost = process.env.DB_HOST;
const apiKey = process.env.API_KEY;
```

### How (Java)
```java
// Read from system environment
String dbHost = System.getenv("DB_HOST");
if (dbHost == null) {
    System.err.println("DB_HOST not set, using default");
    dbHost = "localhost";
}
```

### .gitignore
```
# Always ignore
.env
node_modules/
*.class
target/
.idea/
.DS_Store
```

---

## Deployment Basics

### Simple Deployment Checklist
1. ✅ All tests pass locally
2. ✅ Environment variables are set on the server
3. ✅ `.gitignore` excludes secrets and build artifacts
4. ✅ Build the project: `npm run build` or `javac *.java`
5. ✅ Run on server: `node dist/index.js` or `java Main`

### Environments
| Environment | Purpose | Data |
|-------------|---------|------|
| `development` | Local coding | Fake/test data |
| `staging` | Pre-release testing | Copy of production data |
| `production` | Real users | Real data |

---

## CI/CD Concept

**CI (Continuous Integration)**: Automatically run tests when you push code.
**CD (Continuous Deployment)**: Automatically deploy when tests pass.

### Simple GitHub Actions Example
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install
      - run: npm test
```

### Mental Model
```
Push code → CI runs tests → Tests pass? → Deploy
                           → Tests fail? → Fix and push again
```

---

## Best Practices
1. **Commit often** — small, focused commits are easier to review and revert
2. **Never commit secrets** — use `.env` + `.gitignore`
3. **Pull before push** — avoid merge conflicts
4. **Branch per feature** — keep main clean
5. **Automate repetitive tasks** — if you do it 3+ times, script it

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| Committing `.env` or secrets | Add to `.gitignore` immediately |
| Huge commits with mixed changes | One commit per logical change |
| Working directly on `main` | Use feature branches |
| No `.gitignore` | Create it before first commit |
| Manual deployments | Set up basic CI/CD |
