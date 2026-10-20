---
name: devel-jb-devcontainer
description: "-| | 5173 | Vite dev server | React dashboard with HMR | | 19420 | Go API backend | `skillshare ui` server | | 3000 | Docusaurus | `docs` command in devcontainer |  ## Common Mistakes to Avoid  1."
domain: cybersecurity
---

-|
| 5173 | Vite dev server | React dashboard with HMR |
| 19420 | Go API backend | `skillshare ui` server |
| 3000 | Docusaurus | `docs` command in devcontainer |

## Common Mistakes to Avoid

1. **Running `ss` on host** — macOS binary won't match Linux container; always `docker exec`
2. **Forgetting `cd /workspace`** — Go tests fail if HOME was changed by ssenv
3. **Using `make test` on host** — builds macOS binary, then tests run against wrong arch
4. **Skipping `--init` on ssenv create** — env won't have config; most commands will fail
5. **Not cleaning up ssenv** — `ssenv delete <name> --force` after done; or ask user
6. **Running from /workspace root without -g** — the `ss` wrapper auto-redirects to `~/demo-project` in project mode; use `-g` for global or set `SKILLSHARE_DEV_ALLOW_WORKSPACE_PROJECT=1`
7. **Running `make build` before testing** — unnecessary; the `ss` wrapper auto-builds from source every time

## Rules

- **All CLI execution inside devcontainer** — no exceptions
- **Use ssenv for stateful tests** — don't pollute default HOME
- **Always verify** — run the command and check output; never assume it worked
- **Clean up** — delete ssenv environments after use (or ask user)
- **Report container ID** — set `$CONTAINER` at the start and reuse throughout
