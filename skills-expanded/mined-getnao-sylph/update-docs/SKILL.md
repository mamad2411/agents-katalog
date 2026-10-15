---
name: update-docs
description: Detect user-facing features in recently merged PRs and open a PR in the docs repo adding the missing documentation.
---

# Update Docs

When the user runs `/update-docs`, scan recently merged PRs for user-facing
changes and open a documentation PR.

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| GitHub | Read merged PRs, create docs PRs |

## Prerequisites

Both repos must be cloned locally:
- **Product repo**: the main codebase (configured in CONTEXT.md)
- **Docs repo**: the documentation site (configured in CONTEXT.md or asked on first run)

State file: `agents/cmo/_state/docs_last_refresh.txt` (plain text, single ISO date).

---

## Step 1: Determine the PR window

1. Read `agents/cmo/_state/docs_last_refresh.txt` if it exists
2. If the file exists, use its date as `SINCE`
3. If it does NOT exist (first run), use `today - 15 days` as `SINCE`
4. Record `TODAY` as the date to write back at the end

---

## Step 2: List merged PRs

```bash
gh pr list -R <product-repo> \
  --state merged \
  --search "merged:>=<SINCE>" \
  --limit 100 \
  --json number,title,url,mergedAt,body,author,files
```

Keep the full list - every PR appears in the final summary, even those that don't need docs.

---

## Step 3: Classify each PR

For each PR, decide: **user-facing or not?**

**User-facing** (needs docs):
- New feature in the UI, CLI, API, or configuration
- New command, flag, setting, integration, or UI element
- Behavior change that affects how users interact with the product
- New capability that a user would want to know about
- Anything that belongs in release notes

**NOT user-facing** (skip):
- Refactors, internal cleanups, tests, CI, infra
- Dependency bumps, lockfile updates
- Backend-only changes invisible to users
- Bug fixes that restore already-documented behavior
- Brand, marketing, or internal tooling changes

When unsure, read the PR body and changed files. If still ambiguous, err on **no docs** and note it in the summary.

---

## Step 4: Fetch current docs state

Pull latest from the docs repo:

```bash
cd <docs-repo> && git checkout main && git pull
```

Before writing any new doc, search the repo for existing coverage (grep on keywords from the PR title/body). If a relevant page exists, **update it** instead of creating a new one.

---

## Step 5: Write the docs

For each user-facing PR that needs docs:

1. Identify the right section and subfolder
2. Either update an existing page or create a new one
3. Follow the style of neighboring pages - tone, frontmatter, headings, code blocks
4. If you create a new page, add it to the navigation/sitemap config
5. Keep docs factual and concise - no marketing voice, direct tone
6. Only document what actually shipped - read the PR diff if the description is thin. Never invent behavior.

---

## Step 6: Create a new branch and PR

```bash
cd <docs-repo>
git checkout -b docs/refresh-<TODAY>
git add <changed files>
git commit -m "docs: refresh for PRs merged since <SINCE>"
git push -u origin docs/refresh-<TODAY>
gh pr create -R <docs-repo> \
  --title "docs: refresh for PRs merged since <SINCE>" \
  --body "<PR summary - see template below>"
```

### PR summary template

Every PR from Step 2 must appear in the list, in merge order. Use these exact shapes:

```
- PR merged #123 <PR title> - no docs added
- PR merged #124 <PR title> - added docs - <one-line description of what was documented and where>
```

No other bullet shapes. No section grouping. Keep it a flat list.

If zero PRs were user-facing, skip PR creation and just update the state file.

---

## Step 7: Log the refresh

Write `TODAY` (ISO date) to `agents/cmo/_state/docs_last_refresh.txt`:

```bash
echo "<TODAY>" > agents/cmo/_state/docs_last_refresh.txt
git add agents/cmo/_state/docs_last_refresh.txt
git commit -m "chore(cmo): log docs refresh <TODAY>"
git push
```

The next run picks up from this date.

---

## Step 8: Report back

Return to the user:
- Docs PR URL (or "no user-facing PRs this run" if none)
- Number of PRs reviewed / number that got docs
- The full PR summary list (same content as the PR body)
- New last-refresh date

## Guardrails

- **Never modify source code** - docs changes only
- **Link to source PRs** in the docs PR description
- **One docs PR per batch** - group related changes together
- **Flag ambiguity** - if a PR's user impact is unclear, ask before documenting
- **Never invent features** - only document what the diff shows

## Self-improvement

After the docs PR is reviewed and merged:

1. If the reviewer requests changes to doc structure, tone, or coverage scope, update the relevant step in this skill file
2. If a PR classification was wrong (documented something that didn't need docs, or missed something that did), refine the classification guide in Step 3
3. Update `_insights.md` with patterns: which PRs consistently need docs, which doc styles get approved without changes
4. If the PR summary format needs adjustment based on reviewer feedback, update the template in Step 6
