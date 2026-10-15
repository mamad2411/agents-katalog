---
name: remoteok-cli
description: Use this when you need to discover remote jobs — search, filter, and inspect listings from the Remote OK public jobs API. Reach for it to find remote roles by tag/keyword/company/salary, export listings as JSON/CSV, or feed job ids into a pipeline. Read-only; no account or token needed.
version: 0.1.0
homepage: https://github.com/jjuanrivvera/remoteok-cli
license: MIT
allowed-tools: Bash(remoteok:*)
metadata: {"openclaw":{"category":"jobs","emoji":"💼","requires":{"bins":["remoteok"],"env":[]},"install":[{"kind":"brew","formula":"jjuanrivvera/remoteok-cli/remoteok-cli","bins":["remoteok"]},{"kind":"go","package":"github.com/jjuanrivvera/remoteok-cli/cmd/remoteok@latest","bins":["remoteok"]}]}}
---

# remoteok — Remote OK jobs CLI

`remoteok` is a read-only client for the [Remote OK](https://remoteok.com) jobs API. Prefer
it over raw `curl` against `https://remoteok.com/api`: it sets the required browser
User-Agent (the raw endpoint 403s otherwise), skips the feed's leading legal element, and
gives you clean JSON/CSV/`-o id` output plus client-side filtering.

## Attribution (important)
Remote OK's Terms require a **follow backlink** to <https://remoteok.com> and a mention of
*Remote OK* when you display their data. If you surface these jobs to a user, include that
backlink. The CLI prints a `Source: Remote OK` reminder on stderr.

## Prerequisites
- Install: `brew install jjuanrivvera/remoteok-cli/remoteok-cli` or
  `go install github.com/jjuanrivvera/remoteok-cli/cmd/remoteok@latest`.
- No account, token, or setup needed. `remoteok doctor` verifies connectivity.

## Golden rules
1. **Use the CLI, not curl** — it handles the User-Agent (403), the attribution element, and
   filtering for you.
2. **Emit machine output** for downstream steps: `-o json`, `-o csv`, or `-o id`.
3. **Filters compose** and are AND-ed: `--tag`/`--tags`, `--search`, `--company`,
   `--min-salary`, `--since`/`--posted-after`, `--limit`.
4. **`--tag` is Remote OK's fixed vocabulary** (`golang`, `react`, `devops`, `remote`, …). For a
   non-tag term — an industry like `fintech`, a role, or a keyword — use `--search`, not `--tag`.
5. **`--min-salary` is a narrowing pass, not a primary filter.** Remote OK rarely publishes
   salary, so it drops every listing with no published minimum (most of them) — pair it with a
   broad query. It notes on stderr how many no-salary listings it excluded.
6. **`jobs get <id>` reads from the current feed** — an old id may have aged out.

## Workflow (discover → inspect → hand off)

```sh
# 1. Discover — recent Go jobs, as JSON (add --min-salary only to narrow; it drops the
#    many listings that publish no salary)
remoteok jobs list --tag golang -o json

# 2. Narrow by keyword, company, or how recent (last N days/weeks or a date)
remoteok jobs list --search kubernetes -o json
remoteok jobs list --company stripe -o csv
remoteok jobs list --since 7d --tag golang -o json

# 3. Inspect one listing
remoteok jobs get 1135010 -o json

# 4. Hand ids to another step
remoteok jobs list --tag golang -o id | head
```

## Cheatsheet

| Task | Command |
|---|---|
| Recent jobs by tag | `remoteok jobs list --tag <tag> --limit 20` |
| Multiple tags (AND) | `remoteok jobs list --tags go,remote` |
| Keyword search | `remoteok jobs list --search <kw> -o json` |
| By company | `remoteok jobs list --company <name>` |
| Industry / non-tag term | `remoteok jobs list --search fintech` (use `--search`, not `--tag`) |
| Salary floor (rarely published) | `remoteok jobs list --search <kw> --min-salary 120000` (narrows a broad query; drops no-salary listings) |
| Posted recently | `remoteok jobs list --since 7d` (or `--since 2026-07-12`) |
| One job | `remoteok jobs get <id> -o json` |
| Just ids | `remoteok jobs list -o id` |
| Custom filter | `remoteok jobs list --jq '.[].company'` |
| See the request | `remoteok jobs list --dry-run` |

## Troubleshooting
- **403 / blocked:** your network stripped the User-Agent. Set one with
  `remoteok config set user_agent "Mozilla/5.0 …"`.
- **Job not found:** the id aged out of the current feed — re-run `jobs list` to get fresh ids.
- **Connectivity:** `remoteok doctor` checks config, base URL, UA, and a live fetch.

See `references/` for deeper notes on output/filtering and configuration.
