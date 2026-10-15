---
name: torre-cli
description: Use this when you need to discover jobs or analyze candidate/role fit on Torre.ai — search opportunities by skill/role, remote, location, organization, and compensation, fetch a single opportunity, or pull a person's public genome (bio, strengths, experiences) to compute a match. Read-only; no account or token needed.
version: 0.1.0
homepage: https://github.com/jjuanrivvera/torre-cli
license: MIT
allowed-tools: Bash(torre:*)
metadata: {"openclaw":{"category":"jobs","emoji":"💼","requires":{"bins":["torre"],"env":[]},"install":[{"kind":"brew","formula":"jjuanrivvera/torre-cli/torre-cli","bins":["torre"]},{"kind":"go","package":"github.com/jjuanrivvera/torre-cli/cmd/torre@latest","bins":["torre"]}]}}
---

# torre — Torre.ai jobs CLI

`torre` is a read-only client for the [Torre.ai](https://torre.ai) public API. Prefer it over
raw `curl`: it targets the live hosts (`search.torre.co` for search, `torre.ai/api` for
detail/genome), builds the opportunity-search request body correctly, and gives you clean
JSON/`-o id` output plus a built-in `--jq`.

## Prerequisites
- Install: `brew install jjuanrivvera/torre-cli/torre-cli` or
  `go install github.com/jjuanrivvera/torre-cli/cmd/torre@latest`.
- No account or token needed for job search — every wrapped endpoint is public. (An optional
  `TORRE_TOKEN` exists for higher limits but never blocks the public path.) `torre doctor`
  verifies connectivity.

## Golden rules
1. **A skill search needs an experience level.** Torre rejects a bare skill, so `--experience`
   defaults to `potential-to-develop`; other values: `1-plus-years`, `2-plus-years`,
   `3-plus-years`, `5-plus-years`.
2. **Emit machine output** for downstream steps: `-o json`, `-o id`, or slice with `--jq`.
3. **Not every flag narrows results.** `--skill` narrows the server-side search; the **hard**
   (client-side) filters are `--since`, `--location-type`/`--remote-anywhere`, and
   `--comp-disclosed-only` — they compose (AND). By contrast `--location` and
   `--compensation`/`--currency`/`--periodicity` are **ranking hints** Torre applies
   server-side — they nudge relevance/ordering, they do NOT restrict results to that location or
   pay (a remote role carries no location and is not dropped). Page with `--limit`/`--size`/`--all`.
   For a remote LATAM/Colombian contractor, `--remote-anywhere` (shorthand for
   `--location-type remote_anywhere`) is the key quality filter — roles open to any country —
   and `--comp-disclosed-only` drops roles that hide their pay.
5. **Results are relevance-ordered, not date-ordered** — they span years. For a job hunt,
   date-filter with `--since` (alias `--posted-after`): absolute `YYYY-MM-DD` or relative
   `Nd`/`Nw` (e.g. `7d`, `2w`). It filters `.created` client-side, so pair it with `--all` or
   a larger `--limit` to scan enough candidates.
4. **`genome` is large** — always `--jq` or `-o json` a slice; it's ideal for computing a
   candidate/role match against a profile.

## Workflow (discover → inspect → match)

```sh
# 1. Discover — recent remote Go roles, as JSON
torre jobs search --skill golang --remote --limit 20 -o json

# 2. Nudge relevance by location/pay (ranking hints, NOT hard filters), or filter by recency
torre jobs search --skill "backend" --location Colombia -o json   # location boosts ranking, not a filter
torre jobs search --skill go --compensation 3000 --currency 'USD$' --periodicity monthly -o json  # comp boosts ranking, not a filter
torre jobs search --skill go --since 7d --all -o json   # --since IS a hard filter: only posted in the last 7 days
torre jobs search --skill go --remote-anywhere --limit 100 -o id   # hard filter: roles open to ANY country
torre jobs search --skill go --comp-disclosed-only --since 14d -o json   # only roles that disclose pay, last 14 days

# 3. Inspect one opportunity
torre jobs get <opportunity-id> -o json

# 4. Pull a person's genome to compute fit
torre genome <username> --jq '{name:.person.name, skills:[.strengths[].name]}'
```

## Cheatsheet

| Task | Command |
|---|---|
| Remote roles by skill | `torre jobs search --skill <skill> --remote --limit 20` |
| Location ranking hint (not a filter) | `torre jobs search --skill <skill> --location Colombia` |
| By organization | `torre jobs search --skill <skill> --organization <org>` |
| Compensation ranking hint (not a filter) | `torre jobs search --skill <skill> --compensation 3000 --currency 'USD$'` |
| Recently posted | `torre jobs search --skill <skill> --since 7d --all` (or `--posted-after 2026-07-12`) |
| Remote, open to any country | `torre jobs search --skill <skill> --remote-anywhere --limit 100 -o id` |
| Specific location types | `torre jobs search --skill <skill> --location-type remote_anywhere,remote_timezones` |
| Only roles that disclose pay | `torre jobs search --skill <skill> --comp-disclosed-only` |
| One opportunity | `torre jobs get <id> -o json` |
| Just ids | `torre jobs search --skill <skill> -o id` |
| Person's genome | `torre genome <username> -o json` |
| People search | `torre people search --skill <skill> --location Colombia` |
| See the request | `torre jobs search --skill go --dry-run` |

## Troubleshooting
- **Empty results for a skill:** check the `--skill`/`--experience` text — those narrow the
  search. `--location`/`--compensation` are ranking hints, not filters, so they won't zero out
  results (add `--since`/`--remote-anywhere`/`--comp-disclosed-only` if you need a hard cutoff).
- **Only ~99 results even with `--all`/`--limit 200`:** expected. The opportunities `_search`
  endpoint ignores `offset` and caps a page at 99, so ~99 distinct is the ceiling from this API.
  Results are de-duplicated by `.id` (the earlier `--limit 100` → 100 rows / ~20 unique bug is
  fixed). Narrow with `--skill`/`--remote-anywhere` to surface the most relevant within that cap.
- **Genome too big:** slice it with `--jq` rather than dumping the whole object.
- **Connectivity:** `torre doctor` checks config, both hosts, and a live request.
