---
name: github-context-loader
version: 1.0.0
description: >
  Pulls the latest context, skills and CLAUDE.md from Prash1407's GitHub repos
  at the start of every Claude session. Use this skill when starting a new
  conversation, when told to "pull from GitHub", "sync context", "load skills
  from GitHub", or "was gibt es Neues in meinen Repos". Also triggers on
  "Brain OS sync", "reload skills", or "GitHub pull".
---

# GitHub Context Loader

Pulls latest CLAUDE.md and skill updates from Prash1407's GitHub repos
into the active session context.

---

## Repos to sync (in order)

| Repo | What to pull | Load into |
|---|---|---|
| `Prash1407/kleinanzeigen-reader` | `CLAUDE.md`, `SKILL.md` | Active context |

Add more repos here as the Brain OS ecosystem grows.

---

## Step 1 — Pull CLAUDE.md from each repo

```bash
curl -s \
  -H "Accept: application/vnd.github.v3.raw" \
  "https://raw.githubusercontent.com/Prash1407/kleinanzeigen-reader/main/CLAUDE.md"
```

Read the output and treat it as active session context.

---

## Step 2 — Check for recent commits

```bash
curl -s \
  "https://api.github.com/repos/Prash1407/kleinanzeigen-reader/commits?per_page=3" \
  | python3 -c "
import sys, json
commits = json.load(sys.stdin)
for c in commits:
    print(c['commit']['author']['date'][:10], '---', c['commit']['message'][:60])
"
```

Summarize any changes since the last session in one sentence.

---

## Step 3 — Pull updated scripts if needed

If commits touch scripts/ or references/, fetch updated files:

```bash
curl -s -H "Accept: application/vnd.github.v3.raw" \
  "https://raw.githubusercontent.com/Prash1407/kleinanzeigen-reader/main/scripts/extract.py" \
  > /tmp/kl_extract.py

curl -s -H "Accept: application/vnd.github.v3.raw" \
  "https://raw.githubusercontent.com/Prash1407/kleinanzeigen-reader/main/scripts/compare.py" \
  > /tmp/kl_compare.py
```

Use /tmp/kl_extract.py and /tmp/kl_compare.py for the rest of the session.

---

## Output after sync

Report exactly:

```
GitHub sync: Prash1407/kleinanzeigen-reader
Last commit: [date] -- [message]
Scripts: /tmp/kl_extract.py, /tmp/kl_compare.py
Status: ready
```
