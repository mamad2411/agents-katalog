---
name: openevidence
description: Query OpenEvidence (clinical evidence assistant) without an MCP server. Closely mirrors the openevidence-mcp tool surface - check auth, list question history, fetch an article, or ask a new question (with optional follow-up thread). Use when the user asks medical / evidence-based clinical questions, references OpenEvidence, asks for "OE answers", or wants citations + BibTeX from OpenEvidence. Portable to claude.ai's /mnt sandbox - just drop the folder and a fresh cookies.json next to scripts/oe.py.
---

# OpenEvidence (portable)

A stdlib-only Python port of `openevidence-mcp`. One CLI (`scripts/oe.py`) with four subcommands matching the MCP tools.

| MCP tool          | Skill command                              | Purpose                                                  |
| ----------------- | ------------------------------------------ | -------------------------------------------------------- |
| `oe_auth_status`  | `python3 scripts/oe.py auth-status`        | Confirm `cookies.json` still authenticates `/api/auth/me` |
| `oe_history_list` | `python3 scripts/oe.py history`            | Paginated question history with optional search          |
| `oe_article_get`  | `python3 scripts/oe.py article <uuid>`     | Fetch an article, extract answer + figures, save artifacts |
| `oe_ask`          | `python3 scripts/oe.py ask "<question>"`   | Submit a new question, optionally wait, save artifacts   |

Output of every command is a single JSON object on stdout - same shape the MCP returns to its client.

## Setup (one time)

1. **Cookies**. Export the OpenEvidence cookies from a logged-in browser tab (e.g. "Cookie-Editor" extension → "Export → JSON"). Save as `cookies.json` next to this `SKILL.md`. The format is either a flat array of cookie objects or `{ "cookies": [...] }` (Playwright storage state). The file is gitignored.
2. **Verify**. `python3 scripts/oe.py auth-status` should print `"authenticated": true`. Status `401`/`403` means the cookies expired - re-export.

Cookie lookup order: `$OE_COOKIES`, `./cookies.json`, the skill folder, `~/.openevidence/cookies.json`.

## Common workflows

**Ask a question, wait for completion, save artifacts** (the default):

```bash
python3 scripts/oe.py ask "First-line therapy for adult community-acquired pneumonia in a hospitalized patient"
```

> Note: behavior differs from the MCP tool. The MCP `oe_ask` is now fire-and-forget by default (returns a pending `article_id`; pass `wait_for_completion:true` to block, or fetch later via `oe_article_get`). THIS portable CLI waits by default — override with `--no-wait`.

Returns `{ article_id, status, extracted_answer_raw, figures, artifacts }`. Artifacts land in `$OE_ARTIFACT_DIR` or `./oe-artifacts/<article_id>/` and include:

- `answer.md` - markdown answer with `<visual>` tags resolved to `![alt](url)`
- `article.json` - raw API payload
- `citations.json` - normalized citations with optional Crossref validation
- `citations.bib` - BibTeX, Crossref-augmented when matched
- `crossref-validation.json` - per-citation validation summary
- `figures.json` + `figures/` - figure metadata and downloaded images

**Follow-up in the same thread** (use the `article_id` you got back):

```bash
python3 scripts/oe.py ask "What if the patient has a beta-lactam allergy?" --follow-up <uuid>
```

**Re-fetch / re-save an existing article**:

```bash
python3 scripts/oe.py article <uuid>
```

**Browse history**:

```bash
python3 scripts/oe.py history --limit 20 --search "pneumonia"
```

## Useful flags

- `--no-wait` (ask): return immediately after creating the article; poll later with `article <id>`.
- `--timeout 240 --poll-interval-ms 1500` (ask): tune polling for long-running answers.
- `--no-save`: skip artifact writes (response only).
- `--no-crossref`: skip Crossref DOI validation (faster; offline-friendly).
- `--no-bibtex`: drop `bibtex` from the response (still written to `citations.bib`).
- `--mailto you@example.com` (or `OE_CROSSREF_MAILTO`): use Crossref polite pool.
- `--disable-caching`, `--personalization`, `--article-type`, `--variant`: pass-through to the OpenEvidence `/api/article` request.

## Environment overrides

| Variable                | Default                                  |
| ----------------------- | ---------------------------------------- |
| `OE_BASE_URL`           | `https://www.openevidence.com`           |
| `OE_COOKIES`            | (lookup order above)                     |
| `OE_ARTIFACT_DIR`       | `./oe-artifacts`                         |
| `OE_CROSSREF_MAILTO`    | unset                                    |

## Using this skill in claude.ai's /mnt sandbox

1. Upload (or copy) the `openevidence-skill/` folder into `/mnt/user-data/openevidence-skill/`.
2. Place a fresh `cookies.json` at `/mnt/user-data/openevidence-skill/cookies.json` (the file is gitignored - do not commit it back).
3. Invoke via Bash, e.g. `python3 /mnt/user-data/openevidence-skill/scripts/oe.py ask "..."`.

The script needs only Python 3.10+ stdlib (no `pip install`). All artifacts stay inside the sandbox under `./oe-artifacts/` unless `OE_ARTIFACT_DIR` overrides.

## Troubleshooting

- `cookies.json not found` → export cookies and place beside `SKILL.md`, or set `$OE_COOKIES`.
- `"authenticated": false` with status 401/403 → cookies expired; re-export.
- `OpenEvidence returned no article id` → API rejected the question payload (try shorter prompt or different `--variant`).
- Figures fail to download → individual download errors are swallowed; `figures.json` still records the URLs.
