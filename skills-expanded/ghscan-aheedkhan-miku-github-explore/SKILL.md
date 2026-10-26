---
name: github-explore
description: >-
  Explore GitHub for security research — search repos/code, read files, skim
  releases/commits, study prior art (C2 frameworks, PoCs, patches). Use when
  hunting implementations, comparing designs, or verifying how a fix landed.
---

# GitHub explore (prior art)

## Goal
Find **real code** fast: reference RATs/C2s, public PoCs, vendor patches, library APIs — then cite paths/SHAs in notes.

## Tool: `github`
Explore actions (prefer these over guessing):

| Action | Purpose |
|--------|---------|
| `search_repos` | Discover projects (`query`: keywords, language, stars) |
| `code_search` | Find symbols/strings (`query`, optional `repo`) — often needs `GITHUB_TOKEN` |
| `repo_view` | Stars, description, default branch, topics |
| `contents` | List directory (`repo`, `path`, optional `ref`) |
| `file_get` | Read a file (`repo`, `path`, optional `ref`) |
| `release_list` | Tags/assets |
| `commit_list` | Recent history (`path` optional) |

PR/issue actions stay available for the user's own repos.

Also: `web_fetch` on `raw.githubusercontent.com/...` or advisory HTML when API is rate-limited.

## Research workflows

### Prior art for a RAT / C2 feature
1. `search_repos` — e.g. `sliver c2`, `havoc demon`, `merlin agent`
2. `repo_view` on shortlist (license, activity)
3. `contents` from repo root → drill to implant/transport
4. `file_get` the beacon loop / HTTP handler
5. Diff against *your* design; note ATT&CK overlap
6. Save citations under `workspace/malware-authoring/` + `rag_remember`

### CVE / patch study
1. From advisory, note repo + commit if linked
2. `commit_list` / `file_get` at vulnerable tag vs fixed tag (`ref`)
3. Summarize root cause in `workspace/cves/CVE-….md`
4. Hand off harness design → `cve-malware-test`

### API / library usage
1. `code_search` for the API symbol
2. Read 2–3 call sites with `file_get`
3. Prefer official examples + one battle-tested project

## Query tips
- Scope: `query` can include `language:c`, `stars:>500`, org names
- Code search: `CreateRemoteThread language:c`, `repo:owner/name EtwEventWrite`
- Always record `owner/repo@path` + commit/tag in notes

## Parallelism
- Leaf A: `search_repos` + shortlist
- Leaf B: `file_get` top candidates
- Parent: synthesize trade-offs, write notes

## Honesty
- Stars ≠ quality; check last push + license
- PoCs may be incomplete or trapped — verify before trusting
- Don't paste entire copyrighted trees into git — cite + short excerpts

## Never
- Force-push / mass-clone malware corpora into this repo
- Treat one random Gist as ground truth
- Skip RAG notes after a long explore session
