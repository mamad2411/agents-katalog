---
name: api-docsite-to-cli
description: Use when building a CLI from an API docs site.
license: MIT
metadata:
  hermes:
    tags:
    - cli
    - api
    - scraping
    - python
    - workflow
    - verification
    related_skills:
    - bash-cli-patterns
    - writing-plans
    - python-code-style
    - github
    - subagent-driven-development
    - api-endpoint-probing
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
    platforms:
    - macos
    - linux
  imported_from: hermes
---

# API Docsite → CLI

End-to-end workflow for turning an API documentation site into a working, verified CLI tool. Developed on rail-cli (RailGo data service, 13 endpoints).

## Trigger

- User points at an API docs URL and wants a CLI/client/tool around it
- Any task: "把 X 的 API 封装成 CLI / 写个工具调用这些接口"

## Workflow (verified order)

### Phase 0: Discover the docs site structure

1. Probe the site: `curl -sL <url>/sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`
2. **Apifox-hosted docs sites** (detect: HTML contains `cdn.apifox.com`, `x-doc-selfhost: true`):
   - Every page has a `.md` endpoint: `<pageid>.md` returns clean Markdown (full OpenAPI YAML included)
   - `llms.txt` lists every page with its `.md` URL — fetch all pages from there, no HTML scraping needed
   - Dedup `?nav=N` variants (same page, different sidebar position)
3. Save pages as `references/NN-名称.md` (numbered, Chinese/English title)

### Phase 1: Verify the REAL API (critical — docs site ≠ API host)

**Load `api-endpoint-probing` and follow its workflow** — it is the deep reference for this phase (find real host, curl probes, error shapes, pitfalls).

Rail-cli lesson: the docs host may redirect all `/api/*` paths to docs HTML (WAF 302 → `/help/index.html`) while OpenAPI `servers: []` is empty. Never assume the docs host serves the API. The real host usually hides in official client source (e.g. `DefaultApiUrls.cs`) or docs-site JS config tokens.

### Phase 2: Parallel verification (subagents)

Dispatch 3 leaf subagents in parallel (max 3 concurrent); probe mechanics come from `api-endpoint-probing`:
- **A: V1/group-1 endpoints** — success shape + error behavior (invalid value, missing param)
- **B: V2/group-2 endpoints** — success shape + optional-param behavior (date formats, kind, no-param)
- **C: local environment** — Python version (`/usr/bin/python3` may be old while `python3` hits a newer brew/conda!), git status, proxy env vars, gzip behavior, UTF-8

**Then cross-verify key claims yourself** — subagent self-reports can be wrong (rail-cli's V2 subagent reported "all endpoints fail" because it never found the real host; direct curl proved otherwise).

### Phase 3: Plan

Write `docs/PLAN.md` (user preference: plan at `docs/PLAN.md`, not `docs/plans/<date>.md`):
- Top section: **0. 可行性验证** — the real endpoint matrix table, response structures, decision impacts
- Task list: bite-sized, each with exact files, code, verify commands, commit step

### Phase 4: Implement

Zero-dependency Python (stdlib only: `urllib` + `argparse` + `json`):
- `rail` (shebang `#!/usr/bin/env python3` — **never hardcode `/usr/bin/python3`**, it may be 3.9 without `dict | None` support)
- `rail_cli/client.py` — client class with `get_v1`/`get_v2` (or per-group) methods, per-group base URLs from env vars with defaults
- `rail_cli/cli.py` — argparse subcommands mirroring API categories

Key argparse trick — **global flags in both positions**:
```python
common = argparse.ArgumentParser(add_help=False)
common.add_argument("--pretty", action="store_true", default=argparse.SUPPRESS, ...)
# every subparser: sub.add_parser("x", parents=[common])
```
- `parents=[common]` lets `rail --pretty cmd` AND `rail cmd --pretty` both work
- `default=argparse.SUPPRESS` is REQUIRED: without it the subparser's `False` default overwrites the top-level parsed value (`rail -v cmd` silently loses verbose)

Response handling:
- If API groups have different wrapper conventions (V1 raw JSON vs V2 `{success,msg,data}`), check the wrapper in the client and raise on `success:false` with the `msg`
- Param-name drift between docs and reality: verify by probing (rail-cli: `getCoachPic`/`mapLine` use `train`, others use `trainNum`)

### Phase 5: Verify (integration test)

Run every subcommand against the live API, assert valid JSON per command. Test error paths (invalid train → HTTP 400, exit code 1). Verify `--verbose` prints request URL.

### Phase 6: Publish

- `git init -b main`; `.gitignore` (`__pycache__/`, `.DS_Store`, `.env`, venv)
- Public repo: `gh repo create <owner>/<repo> --public --source=. --remote=origin`
- **Commit discipline** (write these rules into `AGENTS.md`):
  - 禁止 `git add .` / `-A` — only specific paths
  - One commit per task, Conventional Commits (`feat:`/`fix:`/`docs:`)
  - Commit then push immediately
- README in the user's language (Chinese for this user): subcommand tables, usage examples, env vars
- Optional: wrap as a Hermes skill so agents can call the CLI from any session

## Pitfalls checklist

- [ ] Docs host ≠ API host (WAF 302, empty `servers: []`) — find real host in client source
- [ ] `?nav=N` URLs are duplicates — dedup via sitemap
- [ ] `/usr/bin/python3` vs `python3` version difference
- [ ] urllib doesn't send `Accept-Encoding` → no gzip handling needed (server compresses only on request)
- [ ] Subagent reports may be stale/wrong — cross-verify with your own curl
- [ ] Global flags need `parents=[common]` + `default=argparse.SUPPRESS`
- [ ] Terminal multi-command chains may trigger approval blocking — split into single commands
- [ ] Chinese params: urllib auto-encodes; responses come as `\uXXXX` — `json.loads` handles it

## References

- **`api-endpoint-probing`** — deep reference for Phase 1/2 (find real host, probe shapes, error classification)
- rail-cli implementation: https://github.com/mrtsels/rail-cli (docs/PLAN.md has the full verification record)
- `bash-cli-patterns` — cross-platform bash CLI patterns
- `writing-plans` — plan structure conventions
