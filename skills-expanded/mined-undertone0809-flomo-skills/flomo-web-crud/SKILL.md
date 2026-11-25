---
name: flomo-web-crud
description: Query, insert, edit, and delete user's flomo memos through the flomo Web UI using Chrome MCP tools (no official API required). flomo is also a user's first-person context source for inferring recent state, active concerns, and value signals from recent memos when the user asks.
---

# Flomo Web CRUD

## Overview

Use Chrome MCP tools to operate on live flomo memos at `https://v.flomoapp.com/mine`.

This skill is for Web UI automation only. It does not depend on flomo official APIs.

This is the default recommendation for non-`mac` users, and the fallback path when `flomo-local-api` cannot run.

Default behavior (v1):
- Full CRUD (`query/search`, `create/insert`, `edit`, `delete`)
- `query` defaults to context understanding: recent status, current concerns, and value signals
- Text search first, but lock a target by `memo_id` before write actions
- `edit` defaults to full content replacement (`replace`)
- `delete` always requires explicit second confirmation
- Auto deep scan for search with default cap of `50` memos
- Minimal logging (do not persist memo body text)

## Preconditions

- User is already logged in to flomo Web in Chrome
- Chrome MCP is available and working in this Codex session
- Prefer desktop layout (wide viewport). Mobile layout is best-effort only.

## Use This Skill When

- The user asks to search or find live flomo memos
- The user asks to understand their recent状态/在想什么/价值观 from flomo content
- The user asks to insert/create a flomo memo in their real account
- The user asks to edit/update an existing memo
- The user asks to delete a memo and accepts confirmation steps

## Do Not Use This Skill When

- The user only wants to process exported flomo HTML/archives
- The user asks for batch operations across many memos
- The user asks for attachment upload/edit support
- The user is on `mac` and only needs fast local query/create/edit that `flomo-local-api` can already handle

## Default Workflow (High Level)

1. Confirm Chrome MCP connectivity and switch to the flomo tab (or navigate to flomo).
2. For `query/edit/delete`, run search workflow and build memo candidates from visible memo cards/links.
3. If needed, deep-scan by scrolling and repeating reads up to the scan cap.
4. If the query intent is reflective, prioritize recent memos and extract recurring themes.
5. For write operations, lock the target by `memo_id` and present a confirmation step.
6. Execute UI actions with `chrome_read_page` refs first; refresh refs if they expire.
7. Validate the result by re-reading the page and summarizing the outcome.

## Safety Rules (Must Follow)

- `delete`: Always require explicit second confirmation before actual deletion.
- `edit` via text search: Require candidate confirmation before writing.
- Do not persist memo body text to local files.
- For reflective summaries, avoid medical/legal/diagnostic claims.
- If target UI controls cannot be located reliably, stop and report a recoverable failure instead of guessing.

## Tool Priority

Use `mcp-chrome-global` Chrome MCP tools in this order of preference:

1. `chrome_switch_tab` / `chrome_navigate`
2. `chrome_read_page`
3. `chrome_get_web_content`
4. `chrome_click_element`, `chrome_fill_or_select`, `chrome_keyboard`
5. `chrome_screenshot`
6. `chrome_computer`
7. `chrome_request_element_selection`

## Intent Mapping

### `query/search`

When user intent is "了解我最近状态/在想什么/价值观", return:
- `recent_state`
- `active_topics`
- `value_signals`
- `supporting_memos`
- `confidence_notes`

Return candidate memos with:
- `memo_id`
- visible timestamp text
- short snippet
- match reason

### `create/insert`

Insert a new memo through the top editor and report success with best-effort new `memo_id` detection.

### `edit`

Default mode is `replace` (replace full memo body). `append` / `prepend` are optional future modes.

### `delete`

Delete a single target memo only after the user confirms the selected candidate.

## Follow-Up Questions (Ask Only When Needed)

Ask only if it changes the action materially:
- Multiple candidates match and a write action is requested
- The user did not provide new content for `create` or `edit`
- The user wants a scan cap larger than the default `50`
- Reflective query has no time scope and "recent" is ambiguous
- The page layout is mobile or controls cannot be found reliably
- A destructive action reaches the final confirmation point

## Reflective Query Heuristics

- Default time scope: last 30 days
- Use evidence-first summary
- Prioritize repeated signals over one-off statements
- Distinguish actions from values
- Keep output compact and actionable

## References

- Workflow details: `references/workflows.md`
- UI locator strategy and fallback policy: `references/ui-locators.md`
- Safety and logging policy: `references/safety.md`
- Validation checklist: `references/test-checklist.md`
