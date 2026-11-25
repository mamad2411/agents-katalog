---
name: pull-confluence
description: Use when a Confluence page or space must be fetched, ingested into docs/raw, refreshed in sources.json, or propagated into a verified OKF/wiki artifact. Applies to Confluence URLs, page IDs, raw mirror refreshes, provenance updates, and commit-ready documentation changes.
---

# Pull Confluence

Use this skill as the controlled pipeline for Confluence documentation. Keep the
four layers separate:

```text
pull       -> outputs/confluence/        (temporary, untracked)
ingest     -> docs/raw/                 (tracked upstream mirror)
provenance -> sources.json + wiki/index.md
compile    -> docs/wiki/                (curated OKF artifact, deliberate edit)
```

Pulling a page does not automatically create or update a wiki summary. Ingesting
a raw page does not prove that an existing wiki artifact still covers it.

## Use The Right Mode

| Request | Mode | Writes tracked files? |
|---|---|---:|
| Inspect the latest page without importing it | pull-only | No |
| Add or refresh a page in the local mirror | ingest | Yes: `docs/raw/` |
| Refresh all already-ingested Confluence pages | bulk ingest | Yes: `docs/raw/` |
| Update a curated summary after its source changed | compile/verify | Yes: `docs/wiki/` |
| Prepare the result for commit/push | commit-ready | Yes, only after all gates pass |

Do not use this skill for Jira issues. Use `pull-jira` for Jira read/ingest and
`jira-write` for Jira mutations.

## Preconditions

- Work from the repository root.
- Use the repository's `.env` with the caller's own `ATLASSIAN_EMAIL` and
  `ATLASSIAN_API_TOKEN`. Never copy credentials into commands or files.
- Confirm the page belongs to `CONFLUENCE_SITE` (default:
  `https://ipas-tech.atlassian.net`). Override the environment variable instead
  of editing scripts.
- For a normal local preflight, run:

```bash
bash bin/doctor.sh --quick
```

`doctor.sh` is primarily an offline health/document check. It checks `bash`,
`curl`, `python3`, `jq`, `pandoc`, the local environment, OKF validation,
secrets, links, and raw fidelity. Missing Atlassian credentials are warnings in
the offline chain; live freshness still requires valid credentials.

## Phase 1: Normalize And Pull

Accept either a numeric page ID or a URL. Resolve a URL to its numeric page ID
before ingesting. Do not use a filename or title as identity.

For inspection only:

```bash
CONFLUENCE_PAGE_ID=405143554 bash bin/fetch-confluence-page.sh
```

This writes JSON, HTML, and metadata under `outputs/confluence/`. It is
gitignored and does not modify `docs/raw/`.

For a URL, use the repository helper when you need the canonical page ID and
temporary response:

```bash
bash bin/fetch-confluence-url.sh "https://ipas-tech.atlassian.net/wiki/spaces/SN/pages/405143554/example"
```

For a page that should enter the repository, skip the temporary-only step and
use the ingest phase below.

## Phase 2: Ingest The Raw Mirror

Single page, multiple pages, or all already-known page IDs:

```bash
bash bin/ingest-confluence.sh 405143554
bash bin/ingest-confluence.sh 405143554 398492045
bash bin/ingest-confluence.sh
```

The ingest script is the authority for writing `docs/raw/`. It must be allowed
to manage identity and filenames:

- Existing pages are matched by `page_id` frontmatter, never by slug.
- A title/slug change renames the existing raw file rather than creating a
  duplicate.
- An unchanged upstream `version` is a zero-diff no-op.
- Pages in `bin/ingest-denylist.txt` are skipped. Never bypass the denylist.
- A BLOCK secret-scan result rolls back files touched by this run and exits
  non-zero.

Read the complete ingest summary before continuing:

- `Created`, `Updated`, `Renamed`, or `Skipped (unchanged)` are normal.
- `Failed (permanent) > 0` means stop and investigate.
- A denylisted page is intentionally not imported; report it instead of
  retrying or force-ingesting it.
- A page with empty/placeholder content requires human review before it becomes
  a trusted source.
- Retry noise is acceptable only when `failed: 0`; repeated retries or any
  permanent failure is an ingestion incident.

If a page needs a subtype, add `<pageId> <subtype>` to
`bin/ingest-subtype-map.txt`. Do not add page-specific branches to the ingest
script.

## Phase 3: Regenerate Provenance In Order

Run all three commands after any ingest that changes a raw file. The order is
mandatory:

```bash
python3 -sS bin/generate-ledger.py
bash bin/check-staleness.sh
python3 -sS bin/generate-wiki-index.py
```

Why the middle command matters: `generate-ledger.py` resets freshness fields to
`unknown` when a local source version changes. `check-staleness.sh` is the only
step that verifies the local version against upstream and restores
`current`/`stale` plus `upstream_version`.

Do not hand-edit `sources.json` or `docs/wiki/index.md`; regenerate them.

## Phase 4: Propagate Into OKF/wiki Deliberately

After provenance regeneration, find artifacts that cite the changed source:

```bash
python3 -sS -c "
import json
source = 'CONF-SN-405143554'
ledger = json.load(open('sources.json'))
for entry in ledger.values():
    if entry.get('source_id') == source:
        print(entry.get('wiki_artifacts', []))
"
```

Then choose one outcome for each affected artifact:

1. **Artifact still complete and accurate:** run verification only.
2. **Artifact needs new claims/elements:** use
   `.claude/skills/recompile-wiki/SKILL.md`, or update the curated
   `docs/wiki/` artifact with source-backed claims and citations. Do not copy
   the entire raw page into the wiki by default.
3. **Artifact is intentionally high-level:** use a scoped
   `coverage_exclusions` entry with a precise reason and `applies_to` value;
   never hide fabricated/unsourced claims with a broad unscoped exclusion.
4. **No suitable artifact exists:** leave the raw source indexed and create a
   new OKF artifact only when its topic, scope, `artifact_id`, and provenance
   are clear.

For citation work, use:

```bash
python3 -sS bin/okf-cite.py --missing docs/wiki/TOPIC/ARTIFACT.md
```

The raw mirror remains the authority for exact wording, fields, status codes,
and business rules. A wiki summary may omit details; it must not invent them.

## Phase 5: Verify Before Commit

Run the focused checks first:

```bash
python3 -sS bin/okf-validate.py docs/wiki docs/tasks
python3 -sS bin/okf-freshness.py
python3 -sS bin/okf-verify.py docs/wiki/TOPIC/ARTIFACT.md
python3 -sS bin/okf-coverage.py docs/wiki/TOPIC/ARTIFACT.md
```

Run `okf-verify.py` and `okf-coverage.py` only for affected artifacts when
iterating, but run the full gate before commit:

```bash
bash bin/doctor.sh
git diff --check
git status --short
```

The full doctor gate includes raw frontmatter, OKF conformance, secret scan,
links, freshness reporting, OKF verify/coverage, and raw fidelity. Freshness is
informational; BLOCK secrets, invalid frontmatter, broken links, failed verify,
failed coverage, or raw-fidelity failures are blockers.

WARN-tier secret findings (rule R3, normally internal host:port documentation)
are non-blocking and may be expected on specific source pages. Do not add an
allowlist entry merely to make an expected WARN disappear. Only BLOCK-tier
findings require remediation or a reviewed exemption.

If a focused validator reports a pre-existing repository gap, record it in the
completion report instead of hiding it or weakening the validator. Current
task/wiki conformance is expected to pass; a future failure must be triaged as
either a regression from this ingest or an already-known baseline issue.

Do not commit when the ingest summary has permanent failures or when a source
is `unknown` solely because `check-staleness.sh` was skipped.

## Generated-File Rules

- Never hand-edit `docs/raw/*.md`, `sources.json`, or `docs/wiki/index.md`.
- Curated `docs/wiki/<topic>/*.md` artifacts may be edited only as deliberate
  source-backed compilations, followed by OKF verification and coverage.
- Attachments stay under `outputs/confluence/assets/<pageId>/` unless a curated
  artifact explicitly needs a reviewed, committed asset.
- Do not commit `.env`, API tokens, temporary outputs, or raw secret-bearing
  denylisted pages.

## Failure Handling

| Symptom | Action |
|---|---|
| 401/403 | Stop; check credentials/site/permission. Do not retry blindly. |
| 404 | Confirm site and page ID; do not create a new raw file from a guessed slug. |
| 429/5xx or timeout | Let the ingest retry policy run; investigate if permanent failures remain. |
| Denylist warning | Do not bypass; the page is intentionally excluded. |
| Secret BLOCK | Stop, inspect the touched source, redact or obtain a reviewed exception. |
| `stale: unknown` after refresh | Run `check-staleness.sh`, then regenerate the wiki index. |
| OKF coverage failure | Determine whether the artifact is incomplete, over-broad in `upstream_refs`, or needs a narrowly justified exclusion. |

## Completion Contract

Report these facts after the workflow:

- Input page IDs and site.
- Ingest result: created/updated/renamed/skipped/denylisted/failed.
- Whether `sources.json` and `docs/wiki/index.md` were regenerated.
- Affected wiki artifact IDs and whether each was verified/recompiled/deferred.
- Gate results, including freshness counts (`current`/`stale`/`unknown`) and any
  informational warnings.
- Files changed and whether the worktree is ready for commit.

Violating the letter of this workflow is violating its purpose: preserve
page-ID identity, provenance truth, source confidentiality, and citable OKF
knowledge across every refresh.
