---
name: daily-context
description: Use when the user runs /daily-context or asks to pull today's Slack, Jira, Confluence, or Google Docs activity into their org-roam daily note. Gathers today's cloud activity via MCP connectors and writes deduplicated entries with the daily-note CLI.
---

# daily-context — today's cloud activity → org-roam daily note

Pull today's activity from Slack, Jira, Confluence, and Google Docs into
`~/org-roam/daily/YYYY-MM-DD.org`. Things 3 import is handled separately by
`things-to-daily` — do NOT run it from this skill.

## Orchestration (IMPORTANT)

Do NOT gather MCP data in the main session — dispatch all four verticals as
parallel subagents in a single message (Agent tool, subagent_type:
general-purpose). Models: `haiku` for Jira, Confluence, and Docs; `sonnet`
for Slack (thread summaries need a little judgment).

Each subagent prompt must contain, verbatim: the Writing rules section below,
that vertical's section below, and today's date (YYYY-MM-DD, local time).
Subagents load MCP tool schemas with ToolSearch as needed.

When all subagents return, print a run summary: entries added / skipped as
duplicates per section, and anything that degraded (auth failure, unsupported
query, missing connector) — never fail the whole run because one vertical
failed.

## Writing rules (include verbatim in every subagent prompt)

- Write entries ONLY with the `daily-note` CLI (Bash tool); never edit org
  files directly:

  ```
  printf '%s\n' "<body>" | daily-note append --section <Section> --key '<KEY>' --heading '<HEADING>'
  ```

  or with no body:

  ```
  daily-note append --section <Section> --key '<KEY>' --heading '<HEADING>' </dev/null
  ```

- Headings and bodies may contain quotes/apostrophes — quote shell arguments accordingly (prefer single quotes, or escape as needed).
- `skipped: <KEY>` output means the entry already exists — count it as a
  duplicate, not an error.
- The KEY must appear in the heading or body. Headings are org links, so a
  heading like `[[<url>][<description>]]` with KEY=<url> satisfies this.
- Maximum 50 entries for your section; keep the most recent if over.
- Skip bot/app messages and automated notifications.
- Summaries: 1–2 lines, factual, no editorializing, do not invent TODOs.
- Report back: added / skipped / errors counts and any degradation notes.

## Slack (section: Slack, model: sonnet)

1. Resolve my identity (slack_search_users for my display name if needed).
2. Threads I posted in today: `slack_search_public_and_private` with
   `from:me` scoped to today. Group results by thread; for each unique
   thread, `slack_read_thread` and write a one-line factual topic summary.
   - Heading: `[[<permalink>][#<channel>: <topic>]]`
   - Body: the 1–2 line summary
   - Key: the message permalink
3. Mentions of me today (search for my @handle), excluding threads already
   captured in step 2. Same entry shape.
4. Saved for later: try search with the `is:saved` modifier. If the connector
   rejects it or results look unavailable, skip and add
   "saved-for-later unavailable via connector" to your report.

## Jira (section: Jira, model: haiku)

1. `getAccessibleAtlassianResources` for the cloudId; `atlassianUserInfo` for
   my identity.
2. `searchJiraIssuesUsingJql`:
   `updated >= startOfDay() AND (assignee = currentUser() OR reporter = currentUser()) ORDER BY updated DESC`
   Additionally try
   `issuekey IN updatedBy(currentUser(), startOfDay()) ORDER BY updated DESC`
   to catch issues I touched but don't own; if that function is unsupported,
   proceed with the first query alone and note it in your report.
3. Per issue — heading: `[[https://<site>.atlassian.net/browse/<KEY>][<KEY>: <summary>]] — <what I did>`
   where "what I did" is created / commented / transitioned / updated (from
   the changelog/comments when cheap to determine; otherwise "updated").
   Key: the issue key (e.g. `RENG-1234`). No body needed.

## Confluence (section: Confluence, model: haiku)

1. `searchConfluenceUsingCql`:
   `contributor = currentUser() and lastmodified >= startOfDay() order by lastmodified desc`
2. Per page — heading: `[[<page-url>][<page title>]] — edited`
   (use `— commented` when the result is clearly a comment contribution).
   Key: the page URL. No body needed.

## Google Docs (section: Docs, model: haiku)

1. `search_files` (Google Drive connector) for files modified today with
   `modifiedByMe`; restrict to Docs/Sheets/Slides types.
2. Per file — heading: `[[<webViewLink>][<file name>]] — edited`.
   Key: the file's webViewLink URL. No body needed.
3. Comment activity is only capturable if the connector exposes it; if not,
   note "Docs comment activity unavailable" in your report rather than
   guessing.
