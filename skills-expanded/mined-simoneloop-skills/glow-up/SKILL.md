---
name: glow-up
description: >-
  Curate and modernize a GitHub profile to target a specific professional
  positioning (e.g. "AI/ML engineer"). Use when the user wants to clean up their
  GitHub, audit/triage repositories, decide what to make public/private/archive,
  scan repos for leaked secrets or PII, scrub secrets from git history, build a
  profile README from a CV/résumé, choose pinned repos, or "improve how my GitHub
  looks to recruiters/employers". Covers gh auth, repo inventory, secret/PII
  scanning, visibility curation, history cleanup, and CV-driven positioning.
  Also use when the user wants to polish or improve a SINGLE repository:
  write or rewrite a README, add description/topics/badges, or make a specific
  repo look more professional and showcase-ready.
  Also use for the personal portfolio site (USERNAME.github.io / GitHub Pages):
  audit or improve it so the user's body of work emerges from the site, propose
  a featured-projects section synced with the showcase repos, or suggest creating
  the site when the user has no personal website at all.
---

# GitHub Profile Curation

Standing guidance for auditing and reshaping a GitHub account so it presents the
person the way they want to be seen professionally — while never leaking secrets
or breaking the things their CV points to.

This skill is **generic** (works for any account) but ships with safe defaults.
Apply the principles below throughout the task; they are not one-time steps.

## Operating principles (read first)

1. **Confirm before anything irreversible or outward-facing.** Changing repo
   visibility, archiving, deleting, and `push --force` are impactful. Propose a
   plan, get explicit approval, then execute. Approval for one action is not
   approval for the next.
2. **Secrets that were ever public are compromised.** Making a repo private,
   deleting a file, or rewriting history does **not** un-leak them. The only real
   remedy is to **rotate/revoke** the credential. Always say this out loud.
3. **Never hide what the CV/portfolio links to.** Repos referenced from the
   user's CV, LinkedIn, or live sites must stay public — making them private
   breaks those links. Detect them in the positioning brief and protect them.
4. **Scan before you publish.** Before turning any private repo public, inspect
   it for secrets/PII. Also scan already-public repos — they may already leak.
5. **Identity hygiene.** Commit with the user's intended identity. Keep personal
   vs work (employer) identities separate — usually a per-repo local
   `user.name`/`user.email` rather than changing the global config. Verify which
   identity a clone will use before committing.
6. **Match the user's commit conventions. Do NOT add AI co-author trailers**
   (e.g. `Co-Authored-By: …`) unless the user explicitly asks for them.
7. **Report faithfully.** If a step is skipped or a tool lacks a scope, say so.

## Prerequisites & environment

- Requires the GitHub CLI (`gh`) authenticated as the **target account**.
  Check with `gh auth status`. If missing, guide `gh auth login` (interactive —
  the user runs it). For deletes you need the `delete_repo` scope:
  `gh auth refresh -h github.com -s delete_repo`.
- On Windows, `gh` is often not on a fresh shell's PATH even when installed.
  Use the full path (e.g. `"C:\Program Files\GitHub CLI\gh.exe"`) or reload PATH.
- Helper scripts ship with this skill under `${CLAUDE_SKILL_DIR}/scripts/`.

## Single-repo polish (standalone mode)

Use this mode when the user points at **one specific repo** and wants it to look
more professional — without running a full profile audit. Triggers: "crea un
README", "migliora questo repo", "rendilo più accattivante", "write a README for
this repo", "polish this repo", "add description/topics".

### R0 — Identify the repo
Resolve `OWNER/REPO` from context (currently open repo, URL the user pasted, or
ask). Check `gh auth status` matches the owner.

### R1 — Read the repo
Before writing anything, understand what the repo actually does:
- `gh api repos/OWNER/REPO/git/trees/HEAD?recursive=1 --jq '.tree[].path'` — file tree
- Read key source files: `main.*`, `app.*`, `index.*`, notebooks (`.ipynb`), config files
- Fetch repo metadata: `gh repo view OWNER/REPO --json description,repositoryTopics,homepageUrl,primaryLanguage,languages`
- Spawn an Explore agent for repos with many files or multiple notebooks — it reads
  excerpts efficiently and returns a structured summary of what the project does,
  data sources, models/algorithms, results, and tech stack.

### R2 — Assess gaps
Check what's missing or weak:
| Asset | How to check | Action if missing |
|-------|-------------|-------------------|
| README | `gh api .../contents/README.md` → 404 = absent | Create from scratch |
| Description | `gh repo view` → empty string | Propose one-liner |
| Topics | `repositoryTopics` empty | Suggest 3–6 relevant tags |
| Homepage URL | `homepageUrl` empty | Fill if live demo/site exists |
| License | look for `LICENSE` file | Note as missing (don't add without asking) |
| Badges | README has no shields | Suggest CI, language version, license |

### R3 — Draft README
Structure the README from actual code content — never fabricate details:
```
# Project title  (descriptive, not just the repo slug)
> One-sentence hook — what it does and why it matters

## Overview / Pipeline  (diagram or short prose)
## Notebooks / Modules  (table linking each file with a description)
## Usage / Quickstart   (install + run commands)
## Features / Key findings  (bullets from actual results)
## Tech stack
## Results               (only if you read actual metrics from the code)
```
- Show the full draft to the user **before** committing.
- Derive section names from the project type: ML → Pipeline + Results; API/service →
  Endpoints + Quickstart; frontend → Screenshots + Setup; library → API reference.
- Do NOT invent accuracy numbers, benchmark scores, or results you didn't read from
  the code. Write "see notebook" if the metrics are buried in output cells.

### R4 — Update repo metadata
After README approval, also update description and topics in one command:
```bash
gh repo edit OWNER/REPO \
  --description "short one-liner (≤120 chars)" \
  --add-topic topic1 --add-topic topic2 \
  --homepage "https://..." # only if a real URL exists
```
Show the proposed values before running.

### R5 — Commit
Use whatever mechanism is available — pick the first that applies:

1. **Local clone already exists** — write the file normally, `git add`, `git commit`, `git push`.
2. **GitHub MCP server wired** — use the MCP `create_or_update_file` tool directly.
3. **Only `gh` available, no local clone** — use the GitHub Contents API via `gh api`:
   ```bash
   ENCODED=$(printf '%s' "$README_CONTENT" | base64 -w 0)
   SHA=$(gh api repos/OWNER/REPO/contents/README.md --jq '.sha' 2>/dev/null || echo "")
   gh api repos/OWNER/REPO/contents/README.md \
     --method PUT \
     --field message="docs: add README" \
     --field content="$ENCODED" \
     ${SHA:+--field sha="$SHA"} \
     --field branch="main"
   ```

Commit message: `docs: add README` (create) or `docs: update README` (update).
No `Co-Authored-By` trailer unless the user asks.

---

## Personal site polish (USERNAME.github.io)

The profile README is a business card; `USERNAME.github.io` is the shop window.
Run this mode when the user points at their personal site, and **proactively
propose it** whenever positioning work (single-repo polish, Phase 3, Phase 7)
reveals that the site is missing, stale, or doesn't show the user's work —
especially if the user has no other personal website.

### S0 — Detect
- Does `USERNAME/USERNAME.github.io` exist, and is Pages live?
  `gh api repos/USERNAME/USERNAME.github.io/pages --jq '{url:.html_url,status:.status}'`
- Does the user have a site elsewhere? Check the profile `blog` field
  (`gh api users/USERNAME --jq '.blog'`) and the CV/positioning brief.
- **No personal website at all → propose creating `USERNAME.github.io`**: free
  hosting, custom-domain ready, and the natural home for a portfolio. Propose
  it with a concrete outline — don't build unasked.

### S1 — Audit the site as a portfolio
Open the live site and the repo source. Judge everything against one question:
**does the user's body of work emerge from the site?** A visitor should leave
knowing what the user has *built*, not just who they are.

| Aspect | What to check |
|--------|---------------|
| Positioning | Hero/headline matches the target positioning and the profile README |
| Projects | A featured-projects section exists, mirrors the showcase repos, and links to repo / live demo |
| Freshness | Copy reflects the current role and stack; last deploy is recent |
| Completeness | No placeholder pages, dead routes, or "coming soon" stubs |
| Contact | Email / LinkedIn / GitHub reachable in one click |
| Mobile | Layout *adapts* on a phone viewport (nav, columns) — not merely shrinks |
| Meta / SEO | `<title>`, meta description, favicon, Open Graph tags |
| Link circularity | Profile README → site, site → repos, showcased repos' `--homepage` → site |

### S2 — Propose, don't impose
Present the findings as a **prioritized recommendation list** (impact vs effort)
and let the user pick what to do. Typical proposals, in rough priority order:
1. Add/refresh a featured-projects section fed by the showcase repos (names,
   one-liners, tech tags, links) — this is what makes the work emerge.
2. Align the hero copy with the current positioning.
3. Finish or remove half-built pages.
4. Add contact links (email, LinkedIn, GitHub).
5. Fix mobile layout; add meta/SEO basics.
6. Set `gh repo edit OWNER/REPO --homepage <site-url>` on showcased repos.

### S3 — Execute & verify before deploy
A Pages repo deploys on push — treat every push as a **production deploy**:
- Build locally; screenshot key pages at desktop *and* mobile viewports and show
  the user **before** pushing.
- Keep the site's existing stack and visual identity — polish, don't rebuild,
  unless the user explicitly asks for a redesign.
- Source all content from real repos and the positioning brief — never invent
  projects, metrics, or roles. Reuse the R-mode and Phase 1 inventory data.
- Apply R5 commit rules (user's conventions, correct identity, no AI trailers).

---

## Phase 0 — Setup & preflight (run FIRST)
Don't start the audit until setup passes:
- `gh` is **installed** and `gh auth status` shows the **intended account** (warn
  loudly if it shows a work/org account when the user means their personal one).
  This skill uses `gh`'s OS keyring, so no token in settings is required; if you
  instead wire the GitHub MCP server, put its token in `.claude/settings.local.json`
  (auto-gitignored), not the shared `settings.json`.
- Establish the **commit identity** for any repo you will commit to.

## Phase 1 — Inventory
Pull structured metadata for every repo and build a picture:
```
gh repo list --limit 200 --json name,description,visibility,isFork,isArchived,\
primaryLanguage,languages,pushedAt,createdAt,stargazerCount,forkCount,diskUsage,\
repositoryTopics,homepageUrl
```
Or run `${CLAUDE_SKILL_DIR}/scripts/repo-inventory.sh`. Note languages, recency,
forks, empty repos, and anything that looks personal or low-signal.

## Phase 2 — Positioning brief
Ask the user for the **target positioning** (the role/identity to project) and
for their **CV/résumé + links** (LinkedIn, portfolio, live sites). From these:
- Extract the narrative, key skills, certifications, and flagship projects.
- **Extract every GitHub URL the CV references** → mark those repos PROTECTED
  (never private). This is the single most important safety check in the skill.

## Phase 3 — Classify
Bucket each repo with a one-line rationale and present as a table:
- **Showcase / pin** — best work that backs the target positioning.
- **Keep public** — fine to keep, including CV-linked (protected) repos.
- **Hide → private (+ archive)** — exercises, course work, jokes, noisy forks.
- **Delete** — empty/throwaway repos.
- **Leave private** — already-private, keep so.

Get the user's decisions (an `AskUserQuestion` with the ambiguous repos works
well). Cross-check decisions against the PROTECTED set before executing.

## Phase 4 — Secret & PII scan
For any repo you plan to make public (and as a spot-check on public repos), scan
for credentials and personal data **before** changing visibility:
- Run `${CLAUDE_SKILL_DIR}/scripts/scan-secrets.sh <owner/repo | path>`.
- See [references/secret-scanning.md](references/secret-scanning.md) for the
  pattern list, `gitleaks`/`git-filter-repo` usage, and the history-scrub +
  rotation procedure.
- If a repo is dirty, do **not** publish it. Report findings (redact the secret
  values) and propose cleanup.

## Phase 5 — Execute visibility changes (after approval)
Use `gh`. Order matters and there are gotchas — see
[references/visibility-curation.md](references/visibility-curation.md):
- Make private **before** archiving (you cannot edit an archived repo):
  `gh repo edit OWNER/REPO --visibility private --accept-visibility-change-consequences`
  then `gh repo archive OWNER/REPO --yes`.
- Make public: `gh repo edit OWNER/REPO --visibility public --accept-visibility-change-consequences`
  (only after a clean scan).
- Delete needs the `delete_repo` scope. If absent, fall back to private and tell
  the user how to grant the scope.

## Phase 6 — Remediate leaked secrets (if any were found)
1. **Rotate/revoke first** — the user does this (BotFather `/revoke`, rotate API
   keys, change passwords). Non-negotiable; do it regardless of repo cleanup.
2. Replace hardcoded secrets in code with environment variables; delete files
   that are pure secrets/PII.
3. Scrub git history (orphan-commit reset or `git filter-repo`) and `push --force`
   — only with explicit approval. Procedure in
   [references/secret-scanning.md](references/secret-scanning.md).

## Phase 7 — Profile positioning
Build the public-facing layer — see
[references/profile-positioning.md](references/profile-positioning.md):
- **Profile README**: create the special `USERNAME/USERNAME` repo with a
  `README.md` derived from the CV (headline, bio, skills, featured projects,
  live links). Show a draft before publishing.
- **Pinned repos**: recommend the 6 that best match the positioning (pinning has
  no API — the user does it in the GitHub UI).
- **Descriptions & topics**: fill in missing ones on showcased repos.
- Use **reliable badges** (shields.io). Avoid depending on the shared
  `github-readme-stats` instance — it rate-limits and renders "Error Fetching
  Resource". For a reliable stats card, self-host it.
- **Personal site**: check `USERNAME.github.io` (see *Personal site polish*).
  If it exists but doesn't showcase the user's work, propose the S1 audit; if
  the user has no personal site at all, propose creating one. The profile
  README and the site should tell the same story and link to each other.

## Done
Summarize what changed (visibility counts, secrets handled, README live) and list
the user's remaining manual actions (rotate credentials, pin repos, grant scopes).
