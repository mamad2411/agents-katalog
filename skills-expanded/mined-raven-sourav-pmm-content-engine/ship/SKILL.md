# Ship — Safe Push to Remote

## Trigger
User says "/ship", "ship it", "ship this", or "safe push".

For normal "push" or "commit this" — commit and push normally but still never commit secrets.

## Purpose
Audited push for a PUBLIC repo. Prevents accidental secret leaks, catches files that shouldn't be public, and ensures clear commit messages. Think of it as checking your pockets before walking through the door.

## Process

### Step 1 — Pre-flight check
1. Run `git status` and `git diff --staged` (or `git diff` if nothing staged yet)
2. Show the user a **plain-English summary**: what files changed, what the changes do, how many additions/deletions
3. If nothing to commit, say so and stop

### Step 2 — Secret scan
Scan **every staged/changed file** for these patterns:

**API keys & tokens:**
- `sk-ant-`, `sk-` (Anthropic, OpenAI)
- `ghp_`, `gho_`, `github_pat_` (GitHub)
- `AKIA` (AWS access key)
- `xoxb-`, `xoxp-` (Slack)
- `whsec_` (Stripe webhook)
- `pk_live_`, `sk_live_`, `rk_live_` (Stripe)

**Generic secret patterns:**
- `API_KEY=`, `api_key=`, `apikey=` followed by a value
- `SECRET=`, `secret=` followed by a value
- `TOKEN=`, `token=` followed by a value
- `PASSWORD=`, `password=` followed by a value
- `PRIVATE_KEY` followed by content
- `Bearer ` followed by a token (not in docs/examples)
- `Basic ` followed by encoded credentials

**Dangerous files:**
- `.env`, `.env.local`, `.env.production` (even if gitignored — verify)
- `credentials.json`, `service-account.json`, `*.pem`, `*.key`
- Files > 10MB (large binaries don't belong in git)

**Production hazards:**
- Hardcoded `http://localhost` or `http://127.0.0.1` in non-config, non-test files

**If ANY match is found:**
- **STOP immediately.** Do not push.
- Show the exact file, line, and matched pattern
- If the pattern is in `.env.example` with placeholder values (like `sk-ant-...`), that's fine — skip it
- If a secret appears to have been committed in a prior commit, warn: **"This secret is burned. Deleting it from code doesn't help — bots already scraped it. Rotate the key immediately."**

### Step 3 — Stage and commit
1. If changes aren't staged yet, show which files will be staged and ask user to confirm
2. Stage specific files (never `git add .` or `git add -A` without reviewing)
3. Write a clear commit message: imperative mood, what changed and why
4. Show the commit message to user before committing
5. Commit

### Step 4 — Push
1. `git push origin <current-branch>`
2. **Never force push** unless user explicitly requests it AND you warn what will be lost
3. If push is rejected (remote has new commits), explain and offer `git pull --rebase` first

### Step 5 — Confirm
One line: `Shipped: {commit message} → origin/{branch} ({N} files, +{additions} -{deletions})`

## Rules
- Never skip the secret scan — even for "just a quick fix"
- Never commit `.env`, `.env.local`, credentials, or private key files
- Never force push without explicit user request + warning about consequences
- `.env.example` with placeholder values is fine to commit
- If in doubt about a file, ask the user before staging
- This skill is portable — works for any git repo, not just this project
