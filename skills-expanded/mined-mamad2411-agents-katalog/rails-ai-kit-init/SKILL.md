---
name: rails-ai-kit-init
description: "Initialize a new project from the rails-ai-kit starter kit. Clones the repo, creates a new GitHub repository, remaps git remotes (origin → new project, upstream → rails-ai-kit), runs bin/setup, and verifies the app boots. Use this skill when the user says things like: 'start a new rails-ai-kit project', 'scaffold a new app from rails-ai-kit', 'create a new project from the kit', 'init rails-ai-kit for...', 'new project called...', 'clone rails-ai-kit as...', or wants to bootstrap a new Rails + React + Inertia app from the starter kit."
---

# Rails AI Kit — Project Initializer

Automates the full setup of a new project from the [rails-ai-kit](https://github.com/AAlvAAro/rails-ai-kit) starter kit. Handles git remote configuration, GitHub repo creation, dependency installation, database preparation, and boot verification — so the project is ready to build features immediately.

This is NOT just a clone. It produces a properly configured project with:
- `origin` pointing to the new project repo (ready for `git push`)
- `upstream` pointing to `AAlvAAro/rails-ai-kit` (ready for `git fetch upstream && git merge upstream/main`)
- All dependencies installed, database migrated, and dev server verified

## Workflow Overview

```
Input (project name, optional org)
  → Clone rails-ai-kit
    → Create new GitHub repo
      → Remap git remotes
        → Clean git history (optional)
          → Run bin/setup
            → Verify boot
              → Present result + next steps
```

---

## Step 0: Gather Inputs

Determine these values from the user's message or ask if missing:

| Input | Example | Required? |
|-------|---------|-----------|
| Project name | `cafeteria-pro` | Yes |
| GitHub owner/org | `AAlvAAro` | Default: `AAlvAAro` |
| Repo visibility | `private` or `public` | Default: `private` |
| Fresh history? | yes/no | Default: no (keep rails-ai-kit history) |
| Parent directory | `/Users/aalvaaro/Projects` | Default: current working directory |

**Project name rules:**
- Must be lowercase kebab-case (e.g., `my-saas-app`, not `MySaasApp`)
- Will be used as: directory name, GitHub repo name, Kamal service name, and database name

If the user says something like "start a new project called Cafeteria Pro", infer:
- Project name: `cafeteria-pro`
- Repo: `AAlvAAro/cafeteria-pro`
- Confirm before proceeding

---

## Step 1: Clone rails-ai-kit

Clone the starter kit into the target directory with the new project name:

```bash
git clone https://github.com/AAlvAAro/rails-ai-kit.git <parent-dir>/<project-name>
cd <parent-dir>/<project-name>
```

Verify the clone succeeded by checking for key files:
- `Gemfile` exists
- `package.json` exists
- `CLAUDE.md` exists
- `bin/setup` exists
- `app/frontend/pages/` directory exists

If any are missing, abort and report the error.

---

## Step 2: Create GitHub Repository

Create the new repo on GitHub using `gh`:

```bash
gh repo create <owner>/<project-name> --<visibility> --source=. --remote=new-origin
```

If `gh` is not authenticated, instruct the user to run `! gh auth login` and retry.

If the repo already exists, ask the user whether to:
- Use the existing repo (skip creation)
- Choose a different name
- Abort

---

## Step 3: Remap Git Remotes

Configure remotes so `origin` is the new project and `upstream` tracks rails-ai-kit:

```bash
# Rename the original origin to upstream
git remote rename origin upstream

# Rename the remote created by gh to origin
git remote rename new-origin origin
```

Verify the remote setup:

```bash
git remote -v
```

Expected output:
```
origin    git@github.com:<owner>/<project-name>.git (fetch)
origin    git@github.com:<owner>/<project-name>.git (push)
upstream  https://github.com/AAlvAAro/rails-ai-kit.git (fetch)
upstream  https://github.com/AAlvAAro/rails-ai-kit.git (push)
```

If remotes don't match, fix them before proceeding.

---

## Step 4: Initialize Git History

**If the user chose fresh history:**

```bash
# Remove existing git history
rm -rf .git
git init
git add -A
git commit -m "Initial commit from rails-ai-kit

Scaffolded from https://github.com/AAlvAAro/rails-ai-kit

Co-Authored-By: Claude <noreply@anthropic.com>"

# Re-add remotes
git remote add origin git@github.com:<owner>/<project-name>.git
git remote add upstream https://github.com/AAlvAAro/rails-ai-kit.git
```

> Note: Fresh history means `git merge upstream/main` won't work for future updates — warn the user about this tradeoff.

**If keeping history (default):**

Create an initial project commit to mark the fork point:

```bash
git commit --allow-empty -m "Initialize <project-name> from rails-ai-kit

Forked from https://github.com/AAlvAAro/rails-ai-kit
upstream remote tracks the starter kit for future updates.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Step 5: Push to Origin

Push the initial state to the new repo:

```bash
git push -u origin main
```

Verify with:

```bash
gh repo view <owner>/<project-name> --json url --jq '.url'
```

---

## Step 6: Run bin/setup

Install all dependencies and prepare the database:

```bash
bin/setup --skip-server
```

This runs:
1. `bundle install` — Ruby gems
2. `npm install` — Node packages
3. `bin/rails db:prepare` — Database creation and migration

**If bin/setup fails**, diagnose the error:

| Error | Fix |
|-------|-----|
| `pg` gem install fails | Check PostgreSQL is installed: `brew install postgresql@17` or `brew install postgresql` |
| `node` not found | Check Node.js is installed: `node --version` |
| Database connection refused | Check PostgreSQL is running: `brew services start postgresql` |
| `ruby` version mismatch | Check `.ruby-version` and install the required version via `rbenv` or `asdf` |
| `vite` not found | Run `npm install` manually, then retry |

If the error is not in the table, read the full error output and attempt to fix it. Ask the user only if the fix requires system-level changes (installing Homebrew packages, changing system config).

---

## Step 7: Verify Boot

Start the dev server and verify it responds:

```bash
# Start in background
bin/dev &
DEV_PID=$!

# Wait for server to boot
sleep 8

# Check if it responds
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000

# Kill the background server
kill $DEV_PID 2>/dev/null
```

**Success:** HTTP 200 (or 302 redirect to login page).

**If boot fails:**
1. Check `log/development.log` for errors
2. Check Vite is running (port 5173)
3. Check Rails is running (port 3000)
4. Report the specific error to the user

---

## Step 8: Project-Specific Configuration

After successful boot, apply these customizations:

### 8A: Update Application Name

Search and replace the default app name in key files:

```bash
# Find references to the default app name in configuration
grep -r "rails-ai-kit\|RailsAiKit\|rails_ai_kit" --include="*.rb" --include="*.yml" --include="*.json" --include="*.ts" --include="*.tsx" -l
```

Update these files with the new project name:
- `config/application.rb` — module name
- `package.json` — `name` field
- `app/frontend/components/app-logo.tsx` — displayed app name

Do NOT rename the `CLAUDE.md` references to rails-ai-kit — those are documentation about the kit's conventions and should stay as-is.

### 8B: Generate deploy.yml (if not already configured)

If the user mentions a deployment domain, update `config/deploy.yml`:

```yaml
service: <project-name>
image: ghcr.io/<owner>/<project-name>

proxy:
  ssl: true
  host: <project-name>.alvarodelgado.dev
```

---

## Step 9: Present Result

Display a summary:

```
✅ Project <project-name> is ready!

📁 Location: <parent-dir>/<project-name>
🔗 GitHub:   https://github.com/<owner>/<project-name>
🔀 Remotes:
   origin   → <owner>/<project-name> (your project)
   upstream → AAlvAAro/rails-ai-kit (starter kit)

🛠️ Status:
   Dependencies: ✅ installed
   Database:     ✅ migrated
   Dev server:   ✅ boots successfully

📋 Next steps:
   1. cd <parent-dir>/<project-name>
   2. bin/dev                          # Start development
   3. Open http://localhost:3000
   4. Use /feature-planner to spec your first feature

🔄 To pull starter kit updates later:
   git fetch upstream
   git merge upstream/main
```

---

## Behavior Notes

- **Never push to rails-ai-kit.** The entire point of this skill is to prevent that. Always verify remotes before any push.
- **Keep it fast.** The user wants to start building, not wait through a long setup. Skip unnecessary confirmations — confirm once at Step 0, then execute.
- **Diagnose, don't bail.** If `bin/setup` fails, read the error and attempt a fix before asking the user. Common issues (missing Postgres, wrong Ruby version) have known solutions.
- **Default to keeping history.** Fresh history is a destructive choice that breaks upstream merging. Only do it if explicitly requested.
- **The `--skip-server` flag matters.** `bin/setup` without it will start the dev server and block the script. Always use `--skip-server` for automated setup, then verify boot separately.
