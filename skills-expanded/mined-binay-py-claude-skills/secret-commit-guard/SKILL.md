---
name: secret-commit-guard
description: Git pre-commit hook that blocks commits containing secrets, for any repo. Scans only the lines being added for API keys and tokens (Anthropic, OpenAI, AWS, GitHub, GitLab, Stripe, Slack, Google, npm, PyPI, Hugging Face and more), private keys, JWTs, passwords in database URLs, auth headers and KEY=value assignments, and refuses .env, *.pem, *.p12 and id_rsa files outright. Installs next to an existing pre-commit hook without replacing it, and can also scan the working tree or the whole git history. Use when the user wants to stop secrets being committed, set up a pre-commit secret check, asks whether a repo has leaked keys in its history, or before open-sourcing a repo.
---

# secret-commit-guard

`scripts/secret-guard.mjs` is zero-dependency Node 22+. It works in any git repo, not only ones Claude touches, and in Git Bash on Windows (the hook is a `sh` script that calls `node`).

```
node secret-guard.mjs install        # in the repo: adds .git/hooks/pre-commit (keeps an existing hook and runs it after)
node secret-guard.mjs uninstall      # removes it and puts the previous hook back
node secret-guard.mjs scan-staged    # what the hook runs: added lines of the staged diff
node secret-guard.mjs scan [path]    # files git tracks in the working tree (optionally one folder)
node secret-guard.mjs scan-history   # every commit on every branch: commit, file:line, type
node secret-guard.mjs test 'API_KEY=…'   # what the rules say about one line or filename
node tests/run.mjs                   # 93 tests: 57 rule cases + install/commit/chain/uninstall/history in throwaway repos
```
`install` copies the script into `.git/hooks/secret-guard.mjs`, so the hook keeps working if this skill folder moves. Running `install` again updates it in place. Exit codes: `scan` and `scan-history` return 1 when they find something, so they also work in CI.

## What it blocks
| Kind | Examples |
|---|---|
| Provider keys (by prefix) | `sk-ant-`, OpenAI `sk-`/`sk-proj-`, Stripe `sk_live_`/`rk_live_`/`whsec_`, AWS `AKIA…` + `aws_secret_access_key`, GitHub `ghp_`/`gho_`/`github_pat_`, GitLab `glpat-`, Slack `xox?-` + webhook URLs, Google `AIza…` + `GOCSPX-`, npm `npm_`, PyPI `pypi-`, Hugging Face `hf_`, Resend, SendGrid, Groq, DigitalOcean, Shopify, Telegram bot, Azure storage `AccountKey=` |
| Structural | `-----BEGIN … PRIVATE KEY-----`, JWTs, `postgres://user:pass@…` (and mysql, mongodb, redis, amqp, mssql), `https://user:pass@…`, `Authorization: Bearer …`, `--password=…` |
| Assignments | `UPPER_NAME_WITH_TOKEN/SECRET/PASSWORD/API_KEY=value` (env files, shell, YAML), and a quoted literal assigned to any name containing key/secret/token/password **only if it looks random** (20+ chars with 2+ digits and Shannon entropy ≥ 3.7, or 32+ hex chars) |
| Files, whatever they contain | `.env`, `.env.local`, `.env.production` … (not `.env.example`/`.sample`/`.template`), `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `id_rsa`/`id_ed25519`/`id_ecdsa`/`id_dsa` |

Not flagged: values that are references (`process.env.X`, `os.environ[…]`, `${VAR}`, `${{ secrets.X }}`, `config.value`, paths, URLs, numbers), placeholders (`changeme`, `your-key-here`, `<…>`, `xxxx`, `{password}`, anything containing "example", like AWS's `AKIAIOSFODNN7EXAMPLE`), one-line `BEGIN…XXXX…END` key samples in docs, lockfiles, and binary files (by content; binary sensitive *filenames* like `.p12` are still blocked). On a copy of npm's own source (2,246 files) `scan` reported one finding, a base64 password in a README.

Only **added** lines in the staged diff are scanned, so an old line elsewhere in an edited file doesn't block you. The full secret is never printed, only the first 6 characters.

## False positives
- Put `secret-guard: allow` in a comment on the line (`// secret-guard: allow`, `# secret-guard: allow`).
- Or list paths in `.secret-guard-ignore` at the repo root, one gitignore-style glob per line: `tests/fixtures/`, `*.p12`, `docs/**/*.md`. A pattern without `/` matches at any depth.

## When it blocks
It prints `file:line  type  (first 6 chars…)` for each finding, then the fixes: move the value to an environment variable or secret manager; `git reset HEAD <file>` and add the file to `.gitignore`; mark a false positive; and `git commit --no-verify` only if you are certain. **A secret that was already pushed is compromised**: rotate it at the provider first, then clean history (`git filter-repo` / BFG) if needed.

## Existing hooks and hook managers
- An existing `.git/hooks/pre-commit` is renamed to `pre-commit.secret-guard-chained` and runs after the scan with the same arguments; its exit code still counts. `uninstall` renames it back.
- If `core.hooksPath` is set (husky, lefthook, a shared hooks folder), `install` changes nothing and prints the line to add to that hook: `node "<path>/secret-guard.mjs" scan-staged || exit 1`.

## Limits (tell the user)
- Pattern and entropy based. It catches common, well-formed keys; it misses secrets with no recognizable shape (a plain password in a string assigned to an unrelated name, a key split across lines or strings, base64-encoded or encrypted blobs).
- A git hook is local and optional: `git commit --no-verify`, a fresh clone, or a GUI that skips hooks bypasses it. For a team, also run `scan` in CI or turn on GitHub push protection.
- If `node` is not on PATH when git runs the hook, it prints a warning and allows the commit. Internal errors also allow the commit, with a message.
- `scan-history` reads `git log -p --all` (excluding `refs/claude-checkpoints/*` snapshots from bash-checkpoint). It reports each secret once, at the newest commit that added it; it does not see reflog-only commits or other clones.
- `scan` reads files up to 2 MB and skips lockfiles; `.secret-guard-ignore` applies to all three scan modes.
