---
name: pull-jira
description: Fetches Jira issues (read-only) and ingests curated ones as docs/raw/jira-<KEY>.md files. Use when the user provides a Jira issue key, asks to search/read sprint or board data, or wants a specific issue's documentation pulled into docs/raw/. For creating, updating, transitioning, commenting, or linking issues, use jira-write instead.
---

# Pull Jira Skill

Read-only Jira access: fetch/search issues, boards, sprints, transitions —
plus ingesting a curated subset of issues into `docs/raw/jira-<KEY>.md`. This
skill is **read-only by construction**: every script it documents is a
`GET`. Anything that writes to Jira (create/update/transition/comment/link)
is deliberately out of scope here — see `jira-write`, which has its own
dry-run/confirm gate that this skill does not need.

This is a port of the mother repo's `pull-jira` skill (92 lines). What
changed:

- **Plain-file storage.** Fetched issues are written to `docs/raw/jira-<KEY>.md` by
  `bin/ingest-jira.sh`, never stored in an external system or database.
- **No hardcoded site or project.** Mother's examples hardcoded a specific
  Atlassian site domain and project key `DP` inline. Site is now
  `${JIRA_SITE:-https://ipas-tech.atlassian.net}` (same default-in-script
  convention as `pull-confluence`'s `CONFLUENCE_SITE`); there is no default
  project — every example below uses `SN` because that's this repo's
  project, but every script takes `JIRA_PROJECT_KEY`/`JIRA_JQL` as an
  explicit input, never a baked-in constant.
- **Two scripts mother listed don't exist in this repo and are not
  referenced below:** `list-jira-projects.sh` and `assign-jira-issue.sh`.
  Re-assignment happens only at issue-creation time via
  `JIRA_ASSIGNEE_ID` (see `jira-write`) — there is no standalone re-assign
  script in this repo's `bin/`, by design.

## When to Use

- User provides a Jira issue key ("what's SN-41 about")
- "Search issues in this sprint / this JQL"
- "What transitions are available for this issue"
- "Pull this issue into raw/ for the doc corpus"

Do NOT use for creating/updating/transitioning/commenting/linking an
issue — that's `jira-write`, gated behind a dry-run/confirm step because
those calls touch the team's live Jira board.

## Prerequisites

- `.env` with `ATLASSIAN_EMAIL` + `ATLASSIAN_API_TOKEN` (shared with
  Confluence auth). `bin/lib/auth.sh` loads it.
- `JIRA_SITE` defaults to `${JIRA_SITE:-https://ipas-tech.atlassian.net}` in
  every script below — override for a different Atlassian site, don't edit
  the scripts.
- Output of ad-hoc fetches goes to `${JIRA_OUT_DIR:-outputs/jira}/`
  (gitignored).

## Read scripts

| Script | Env vars | Endpoint |
|---|---|---|
| `bin/fetch-jira-issue.sh` | `JIRA_ISSUE_KEY`, `JIRA_FIELDS`, `JIRA_EXPAND` | `GET /rest/api/3/issue/{key}` |
| `bin/search-jira-issues.sh` | `JIRA_JQL`, `JIRA_MAX_RESULTS` (default 50), `JIRA_FIELDS`, `JIRA_NEXT_PAGE_TOKEN` | `POST /rest/api/3/search/jql` |
| `bin/get-jira-transitions.sh` | `JIRA_ISSUE_KEY` | `GET /rest/api/3/issue/{key}/transitions` |
| `bin/list-jira-boards.sh` | `JIRA_PROJECT_KEY`, `JIRA_BOARD_TYPE` | `GET /rest/agile/1.0/board` |
| `bin/list-jira-sprints.sh` | `JIRA_BOARD_ID`, `JIRA_SPRINT_STATE` | `GET /rest/agile/1.0/board/{id}/sprint` |
| `bin/list-jira-issue-types.sh` | `JIRA_PROJECT_KEY` | `GET /rest/api/3/issue/createmeta/{key}/issuetypes` |

```bash
# Read an issue
JIRA_ISSUE_KEY=SN-41 bash bin/fetch-jira-issue.sh

# Search sprint issues (POST /rest/api/3/search/jql -- the old GET /rest/api/3/search
# is deprecated per Atlassian CHANGE-2046; pagination is cursor-based via
# nextPageToken, not startAt/total)
JIRA_JQL="project=SN AND sprint=29930" JIRA_MAX_RESULTS=100 bash bin/search-jira-issues.sh

# See available transitions before calling jira-write's transition step
JIRA_ISSUE_KEY=SN-41 bash bin/get-jira-transitions.sh

# Boards / sprints for a project
JIRA_PROJECT_KEY=SN bash bin/list-jira-boards.sh
JIRA_BOARD_ID=4564 JIRA_SPRINT_STATE=active bash bin/list-jira-sprints.sh
```

## Ingesting a curated issue into `docs/raw/`

```bash
bash bin/ingest-jira.sh SN-41
bash bin/ingest-jira.sh SN-41 SN-42   # multiple issues in one run
```

`bin/ingest-jira.sh` (task #6) has **no bulk/refresh-all mode** — unlike
`bin/ingest-confluence.sh`, it always requires an explicit issue key (or
list). Jira ingestion into `docs/raw/` is a deliberately curated subset chosen
by a human, not a mirror of the whole project; running it with zero args
is a usage error by design, not a missing feature.

What it writes: `docs/raw/jira-<KEY>.md`, identity keyed by the issue key itself
(see `use-kb` — Jira's `page_id` frontmatter field is the issue key, not
Jira's internal immutable `id`). Idempotence is gated on epoch-seconds of
`fields.updated`, Jira's closest equivalent to Confluence's `version`
counter — unchanged `updated` means the run is a no-op.

**Only three fields are converted into the file:** `summary` (-> title),
`issuetype` (-> a one-line marker), and `description` (ADF -> markdown via
`bin/adf_to_md.py`, a hand-rolled converter since `pandoc` can't read ADF).
Status, assignee, priority, labels, comments, and everything else Jira
exposes are deliberately excluded — this pipeline is for documentation, not
status tracking, and those fields would force a rewrite on every routine
board update.

Same secret-scan gate as `pull-confluence`: `bin/scan-secrets.sh` runs over
every file this run touched; a BLOCK-tier hit rolls the run back and aborts
non-zero.

## After ingesting

```bash
python3 -sS bin/generate-ledger.py
python3 -sS bin/generate-wiki-index.py
```

Same as `pull-confluence` — only needed if a `docs/wiki/` artifact also needs
updating to reflect the new/refreshed issue.

## Notes

- Body format for `description` is Atlassian Document Format (ADF), not
  HTML — that's why Jira needs its own converter instead of reusing
  Confluence's `pandoc` step.
- Every script `unset`s `AUTH` after use.
- If a real issue is ever re-keyed (moved to a different project, which
  changes its key), nothing here detects that the new key and the old
  `docs/raw/jira-<OLD-KEY>.md` are the same issue — a known, accepted gap (see
  `docs/raw/SCHEMA.md`'s "Jira identity and version" section), not something
  this skill works around.
