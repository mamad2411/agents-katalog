---
name: github-monitor
description: Monitor your GitHub repos for new projects and significant updates. Generates Reddit + Twitter draft posts for approval before publishing. Triggers on "check my github", "github monitor", "new repos", or any GitHub monitoring request.
inputs:
  - name: github_username
    type: string
    required: true
    description: GitHub username whose public repos to monitor
outputs:
  - name: new_repos
    type: list
    description: List of new or recently updated repos, each with {name, description, url, pushed_at}
  - name: ship_drafts
    type: list
    description: Social media draft posts for each new repo, each with {platform, content}
---

# GitHub Monitor Skill

Monitor your public GitHub repos. When new repos appear or significant updates happen, generate social media drafts and send for approval.

---

## Configuration

Set your GitHub username at the top of your state file or as an env var:

```bash
export GITHUB_USERNAME="yourusername"
```

---

## Core Principle

**Product is content.** Don't fabricate stories. Translate "what I built" into social posts.

---

## Detection Logic

### 1. Fetch Current Repos

```bash
# New repos (sorted by creation date)
gh api /users/$GITHUB_USERNAME/repos?sort=created&per_page=10

# Recently updated repos (sorted by push date)
gh api /users/$GITHUB_USERNAME/repos?sort=pushed&per_page=10
```

### 2. Compare Against State

Read `memory/github-monitor-state.json` and compare.

### 3. Trigger Conditions (any one triggers a draft)

| Condition | How to Detect |
|-----------|---------------|
| New public repo | `created_at` newer than any known repo |
| Significant update | `pushed_at` changed AND >= 3 new commits since last check |
| Star milestone | Stars crossed 10, 50, 100, 500, 1000 |

### 4. Gather Content for Draft

```bash
# Read README
gh api /repos/$GITHUB_USERNAME/{repo}/readme --jq .content | base64 -d

# Recent commits
gh api /repos/$GITHUB_USERNAME/{repo}/commits?per_page=5

# Repo metadata (description, language, stars, forks)
gh api /repos/$GITHUB_USERNAME/{repo}
```

---

## Draft Generation Rules

### Voice & Tone

- First-person perspective
- Authentic, technical, no hype
- Show the work, not the dream

### Banned Words

NEVER use: Revolutionize, Supercharge, Game-changer, 10x, Viral, Hacks, Disrupt, Groundbreaking, Revolutionary, Mind-blowing

### Reddit Draft

**Target subreddits:** r/SideProject, r/coolgithubprojects (pick based on repo type)

**Format:**
```
Title: [Concise, descriptive — what it does]

Body:
## The Problem
[1-2 sentences: what pain point this solves]

## What I Built
[2-3 sentences: what the repo does, key features]

## How It Works
[Brief technical overview, stack/approach]

## What I Learned
[1-2 genuine takeaways from building this]

GitHub: https://github.com/{username}/{repo}

Happy to answer questions!
```

### Twitter Draft

**Format:** 1-3 tweets, concise and punchy.

```
Tweet 1: [Hook — what problem + what I built]
Tweet 2: [Key technical detail or interesting finding]
Tweet 3: [Link + invitation to check it out]

GitHub: https://github.com/{username}/{repo}
```

Keep each tweet under 280 chars. Natural flow.

---

## Approval Flow

### Send Draft to User

```
New project detected!

{repo_name}
{description}

--- Reddit Draft (r/{subreddit}) ---
{reddit_draft}

--- Twitter Draft ---
{twitter_draft}

Reply "post" to publish both, or tell me what to change.
```

### User Responses

| User says | Action |
|-----------|--------|
| "post" / "send" / "go" | Publish to Reddit + Twitter |
| "reddit only" | Publish Reddit only |
| "twitter only" | Publish Twitter only |
| "change X to Y" | Revise draft and re-send |
| No reply | Do nothing. NEVER auto-post. |

---

## Publishing

### Reddit

Use AppleScript Chrome automation (see `reddit-cultivate` skill):

1. Get modhash from `/api/me.json`
2. POST to `/api/submit` with:
   - `sr`: subreddit name
   - `kind`: "self"
   - `title`: post title
   - `text`: post body (markdown)
   - `uh`: modhash

### Twitter

Use Twikit:

```bash
cd ~/crawlee-social-scraper  # or wherever your Twikit setup lives
source venv/bin/activate
python3 -c "
import asyncio
from twikit import Client

async def post():
    client = Client('en-US')
    client.load_cookies('twitter_cookies.json')
    await client.create_tweet(text='''TWEET_TEXT_HERE''')

asyncio.run(post())
"
```

### After Publishing

1. Record published URLs in `memory/github-monitor-state.json` under `posted_repos`
2. Log to daily memory file `memory/YYYY-MM-DD.md`
3. Report back: "Published! Reddit: [url] | Twitter: [url]"

---

## State File

Location: `memory/github-monitor-state.json`

```json
{
  "github_username": "yourusername",
  "last_checked": "2026-01-01T09:00:00Z",
  "known_repos": {
    "repo_name": {
      "created_at": "2026-01-01T16:37:12Z",
      "last_pushed_at": "2026-01-01T17:58:31Z",
      "last_known_commits": 5,
      "stars": 1
    }
  },
  "posted_repos": ["repo_name"],
  "star_milestones_notified": {
    "repo_name": [10]
  }
}
```

---

## First Run Behavior

On the very first run (when `last_checked` is null):

1. Fetch all public repos
2. Record them ALL in `known_repos` (baseline snapshot)
3. Do NOT trigger any notifications
4. Reply: "First sync complete. Recorded {N} public repos. Will notify you of new repos and significant updates going forward."

---

## Cron Schedule

Runs 3x daily: 09:00, 15:00, 21:00 (your local time)

If nothing new: reply `HEARTBEAT_OK` (no notification).

---

## Star Milestones

When a repo crosses a milestone, send a celebratory notification:

```
Your repo {repo_name} just hit {milestone} stars!

Current: {stars} stars | {forks} forks

Want me to draft a "milestone update" post?
```

Milestones: 10, 50, 100, 500, 1000, 5000, 10000
