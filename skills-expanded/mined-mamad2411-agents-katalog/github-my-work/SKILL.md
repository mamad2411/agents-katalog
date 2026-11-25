---
name: github-my-work
description: >-
  Show open GitHub Issues assigned to you in the target repo, grouped by priority
  label (P0 first), with clickable issue links. Use whenever the user asks "what's
  on my plate", "my GitHub issues", "what should I work on next", "show my open
  issues", or starts the day wanting their remaining work. Read-only — it lists,
  it never changes anything.
effort: max
---

# github-my-work

List open issues assigned to you in the target repo, sorted by priority (P0 → P1 →
P2 → P3 → unlabeled). Rendered as a table with clickable links. Entirely read-only.

## Run it

Prereqs: `gh auth login` (or `$env:GH_TOKEN`), `$env:GH_OWNER` + `$env:GH_REPO` set.

```powershell
$env:GH_OWNER = "Cartagena365"
$env:GH_REPO  = "GlassHull"
gh issue list `
  --repo "$env:GH_OWNER/$env:GH_REPO" `
  --assignee @me `
  --state open `
  --json number,title,labels,url `
  --jq '.[] | [.number, .title, (.labels | map(.name) | join(", ")), .url] | @tsv'
```

Format the output as a table sorted by priority label. Issues labeled `P0` come
first, then `P1`, `P2`, `P3`, then unlabeled. The `#` column should be a clickable
terminal hyperlink (use `\e]8;;URL\e\\TEXT\e]8;;\e\\` for OSC 8 links in terminals
that support them).

## After listing

The top P0/P1 item is the highest-priority actionable issue — a good "do next". If
the user wants to turn a *findings source* into new issues, hand off to
**findings-to-github-issues**.
