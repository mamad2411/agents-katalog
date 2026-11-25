---
name: github-cache-hygiene
description: "GitHub quota/cache hygiene: Gitcrawl archives, Octopool-backed gh, freshness, limits."
---

# GitHub Cache Hygiene

Goal: discover in the local Gitcrawl archive first, then use the existing Octopool-backed `gh` shim for current GitHub metadata and authorized writes.

## Default Path

Start with local archive reads:

```bash
gitcrawl search prs "<terms>" -R owner/repo --state open --json number,title,url
```

```bash
gitcrawl threads owner/repo --numbers 123 --include-closed --json
```

`--include-closed` keeps closed or merged candidates in scope. Archive state can lag GitHub; it is not proof of current state.

Then use bare PATH `gh` when current metadata is needed. On Peter's machines it is expected to be the Octopool-backed shim, so supported JSON reads share the fleet cache without changing authentication or command routing:

```bash
gh search issues "<terms>" -R owner/repo --state open --json number,title,state,url,updatedAt,labels,author
gh search prs "<terms>" -R owner/repo --state open --json number,title,state,url,updatedAt,isDraft,author
gh issue list -R owner/repo --state open --author user --assignee user --label bug --json number,title,url
gh pr list -R owner/repo --state open --author user --label dependencies --json number,title,url
gh issue view 123 -R owner/repo --json number,title,state,body,comments,labels,url
gh pr view 123 -R owner/repo --json number,title,state,url,headRefName,headRefOid
gh pr checks 123 -R owner/repo --json name,state,bucket,link
gh run list -R owner/repo --branch branch-name --json databaseId,workflowName,status,conclusion,url
gh pr diff 123 -R owner/repo --patch
```

Use exact refs and narrow fields. Avoid broad loops like one `gh issue view` per result when a single `gh search` or `gh issue list --json ...` can answer the first-pass question.

For CI, avoid tight `gh run list` / `gh run view` polling loops. After a push or workflow dispatch, identify one exact run, then poll that run at 30s, 60s, then 120s intervals. Fetch logs once, only after failure or explicit request. Reuse prior output instead of re-reading completed runs.

## Freshness

Local answers are good for discovery, duplicate search, old thread review, author/label triage, and "is there likely already an issue/PR?" checks.

Use a live call when:

- writing, commenting, closing, merging, rerunning, or editing
- checking final current state before a maintainer action
- verifying CI status after a push
- the local result is missing or obviously stale
- the user asks for latest/live state

Hydrate exact PR details only when the local archive needs files, commits, checks, or run summaries for repeated review:

```bash
gitcrawl sync owner/repo --numbers 123 --with pr-details
```

This refresh spends GitHub API calls and updates Gitcrawl's archive, not Octopool's separate `gh` cache. Bare `gh` reads do not auto-hydrate the Gitcrawl archive.

`gitcrawl gh` is retired and exits `2` with a migration note. Replace those recipes with archive reads followed by bare `gh`; the note is not an authentication failure. Do not run `octopool login`, change tokens/auth/PATH/config, or bypass the existing shim to repair a retired command.

After a write, do one targeted readback, not a broad rescan.

## Octopool

Inspect cache behavior when rate limits are suspected:

```bash
octopool whoami
octopool health
octopool stats --since 1h
octopool stats --since 24h --json
```

Check the saved-vs-backend totals, eligible hit rate, top route kinds, fallbacks, and client attribution. A missing client or unexpected server means that machine is outside the shared fleet cache.

Use `OCTOPOOL_NO_FALLBACK=1` only for a bounded read probe that must prove relay coverage. Do not set it globally; mutations and unsupported reads still need real `gh`.

For relay-only proof:

```bash
OCTOPOOL_NO_FALLBACK=1 gh api repos/owner/repo --jq .full_name
```

## Agent Etiquette

Batch questions by repo and state. Reuse data already printed in the session. Back off CI polling; inspect logs only once for a failed run. Use bare PATH `gh` for ordinary reads and authorized writes; let Octopool own fallback to the real CLI. Do not bypass the shim with an absolute real-`gh` path or a binary override to replace retired Gitcrawl recipes.
