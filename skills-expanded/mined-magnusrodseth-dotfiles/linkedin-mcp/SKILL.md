---
name: linkedin-mcp
description: Read LinkedIn DMs/threads, look up people and company profiles, search and inspect job postings, and send messages or connection requests via the linkedin MCP server. Use when the user asks to check LinkedIn messages/inbox, read a conversation, search messages, look up a profile or company, search jobs, send a LinkedIn DM, or send/accept a connection request.
---

# LinkedIn MCP

Driven by the `linkedin` MCP server (registered globally as `uvx linkedin-scraper-mcp@latest`). All tools are exposed under the `mcp__linkedin__*` namespace and operate on a real authenticated browser session for the signed-in account.

The signed-in user is **Magnus Rødseth** — LinkedIn username `magnus-rodseth` (https://www.linkedin.com/in/magnus-rodseth/). When the user says "my profile", "me", "my inbox", or "my messages", that's this account.

## Quick start

- Read recent DMs: `mcp__linkedin__get_inbox` (defaults to 20 most recent threads).
- Open a thread by participant name/handle: `mcp__linkedin__get_conversation` with `linkedin_username`.
- Find a thread by content: `mcp__linkedin__search_conversations` with `keywords`, then open via returned `thread_id`.
- Look up a profile: `mcp__linkedin__get_person_profile` with `linkedin_username` (and optional `sections`).
- Look up a company: `mcp__linkedin__get_company_profile` with `company_name`.

## Workflows

### Reading DMs (the main use case)

1. Default to `get_inbox` (limit 5–20) for "what's in my inbox" type asks. Don't go above 20 unless the user wants a backlog scan.
2. To open a specific thread:
   - If the user names a person (e.g. "the thread with Jane Doe"): pass their handle as `linkedin_username` to `get_conversation`. If they have multiple threads (e.g. organic + InMail), use `search_conversations` first to enumerate `thread_id`s, then call `get_conversation` with the right `thread_id`.
   - If they describe content ("the message about the contract"): use `search_conversations` with tight `keywords`.
3. **Side-effect warning:** `get_conversation` (by username) and `search_conversations` enumerate matches by clicking rows in LinkedIn's UI, which **may mark them as read**. Keep `limit` small (≤10) on noisy queries, and prefer `thread_id` once known to skip enumeration.

### Sending a message

1. Confirm the recipient and full message text with the user verbatim before calling.
2. Call `mcp__linkedin__send_message` with `confirm_send: true`. Without confirmation it won't send.
3. If the recipient isn't directly messageable from their profile, fetch `get_person_profile` first to obtain the `profile_urn` and pass it to `send_message` — that's more reliable than the Message-button lookup.

### Profile and people lookups

- `get_person_profile` always scrapes the main page. Add `sections` (comma-separated) only for what you need: `experience`, `education`, `interests`, `honors`, `languages`, `certifications`, `skills`, `projects`, `contact_info`, `posts`. Heavy sections (e.g. `posts`, 30+ certs) — bump `max_scrolls` and request them in a separate call to avoid slowing other sections.
- `search_people` takes `keywords` and optional `location` — use it to find a handle when only a name/role is known.
- `get_sidebar_profiles` pulls "More profiles for you", "Explore premium profiles", "People you may know" recommendations from a given profile page.

### Jobs

1. `search_jobs` with `keywords` (+ optional `location`, `experience_level`, `job_type`, `work_type`, `date_posted`, `easy_apply`, `sort_by`, `max_pages`). Returns `job_id`s.
2. `get_job_details` with a `job_id` for the full posting.

### Companies

- `get_company_profile` with `company_name` (the URL slug, e.g. `anthropic`, `docker`). Add `sections` (`posts`, `jobs`) only when needed.
- `get_company_posts` for just the feed.

### Connection requests

- `connect_with_person` sends or accepts a connection request (with optional `note`). Annotated `destructiveHint`, so confirm with the user before calling.

### Cleanup

- `close_session` releases the browser session — call when the user signals they're done with LinkedIn work in this conversation, or when retrying after a session error.

## Conventions

- **Handles, not URLs.** Pass `magnus-rodseth`, not `https://www.linkedin.com/in/magnus-rodseth/`.
- **Tool calls serialize.** The server queues tool calls behind a single browser. Don't try to parallelize multiple linkedin tools.
- **Cold start.** First call after install can stall on Patchright Chromium download; if it errors with setup-in-progress, retry after a moment.
- **Auth failures.** If tools fail with auth/session errors, the user can re-login: `uvx linkedin-scraper-mcp@latest --login`.

## Write operations require confirmation

These tools change state and must be confirmed with the user before invocation:

- `send_message` (must pass `confirm_send: true`)
- `connect_with_person` (sends/accepts a request)
