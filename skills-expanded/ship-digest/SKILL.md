---
name: ship-digest
description: Detect new GitHub repos and generate formatted ship announcements for social media. Monitors your GitHub profile for new repos pushed today, writes a technical digest, and drafts Twitter/Reddit posts for approval. Triggers on "ship digest", "new repos", "what did I ship", "github ship", or any shipping announcement request.
inputs:
  - name: github_username
    type: string
    required: true
    description: GitHub username to check for newly pushed repos
outputs:
  - name: new_repos
    type: list
    description: List of new repos detected today, each with {name, description, url, pushed_at, readme_summary}
  - name: social_drafts
    type: list
    description: Draft social posts for each repo, each with {hook_type, content, platform}
---

# Ship Digest Skill

Automatically detect new GitHub repos and turn them into social media announcements.

---

## Setup

```bash
export GITHUB_USERNAME="yourusername"
```

---

## How It Works

1. Fetch your GitHub repos sorted by `pushed_at`
2. Compare against a state file (`memory/ship-digest-state.json`)
3. For any new repo pushed today → analyze README + commits
4. Generate a technical digest + social media drafts
5. Send drafts for approval (NEVER auto-post)

---

## Workflow

### Step 1: Fetch New Repos

```bash
gh api /users/$GITHUB_USERNAME/repos?sort=pushed&per_page=10
```

Compare `pushed_at` timestamps against state file. A repo is "new" if:
- Not in state file at all, OR
- `pushed_at` is today and has 3+ new commits since last check

### Step 2: Analyze Repo Content

```bash
# README
gh api /repos/$GITHUB_USERNAME/{repo}/readme --jq .content | base64 -d

# Recent commits
gh api /repos/$GITHUB_USERNAME/{repo}/commits?per_page=5

# File tree (for tech stack detection)
gh api /repos/$GITHUB_USERNAME/{repo}/git/trees/HEAD?recursive=1 --jq '[.tree[].path] | join(", ")'
```

### Step 3: Generate Ship Digest

Output format:

```
🚢 Ship Digest — [date]

Caught a new repo: **{repo_name}**, pushed today.

**What you shipped:**
[2-3 sentence technical description based on README + commits]

📊 **{N} lines** in initial commit. [Tech stack summary].
→ github.com/{username}/{repo}

---

**✍️ DRAFT — Option A: [Hook type]**
[Twitter draft A]

**✍️ DRAFT — Option B: [Hook type]**
[Twitter draft B]

Reply "A" or "B" to post, or tell me what to change.
```

### Step 4: Await Approval

User picks Option A or B (or requests edits). Then post using `social-post` skill or `twitter-cultivate` skill.

NEVER auto-post without explicit user confirmation.

---

## Draft Generation Rules

### Voice
- First-person, authentic, no hype
- Lead with the problem solved OR the interesting technical choice
- Include one specific metric (lines of code, platforms supported, speed improvement)

### Hook Types to Try
1. **Contrarian Hook** — "Everyone says X, but actually Y"
2. **Data Hook** — "[Number] lines. [N] platforms. [capability]."
3. **Problem Hook** — "Every [person] hits [pain point] eventually..."
4. **Story Hook** — "Been thinking about [problem] for [time]. Finally shipped something."

### Banned Words
Never use: revolutionize, supercharge, game-changer, 10x, viral, hacks, disrupt, groundbreaking

---

## State File

Location: `memory/ship-digest-state.json`

```json
{
  "github_username": "yourusername",
  "last_checked": "ISO8601",
  "known_repos": {
    "repo-name": {
      "pushed_at": "ISO8601",
      "last_commit_count": 42,
      "announced": true
    }
  }
}
```

---

## Cron Schedule

Runs 2x daily: 09:00 and 16:00 (your local time).

If no new repos: reply `HEARTBEAT_OK`.
