# AGENTS.md

## Repo
- Repo name: `network-agent`
- Product name: `Network Growth Agent`
- Language: Python 3.11 required. The repo virtual environment must be recreated with Python 3.11 if it drifts.

## Project Purpose

`network-agent` is a multi-agent system that reduces the time spent on professional networking and personal-brand building for a job search. It manages prospect outreach, relationship tracking, LinkedIn content creation, and calendar coordination - with a human-in-the-loop approval step before any external action that can realistically be automated (posting content, blocking calendar time).

This is not an automation/spam tool. No agent may autonomously send a LinkedIn connection request, message, or post. Outreach messages are permanently draft-only in MVP scope: the user manually copies drafted outreach into LinkedIn and sends it themselves. LinkedIn posting is the only LinkedIn action with a realistic API automation path, and it still requires explicit human approval via the Telegram interface.

## Non-Negotiable Rules

- No agent may submit a LinkedIn connection request or direct message automatically. LinkedIn's public developer API does not support programmatic connection requests, connection-request notes, regular direct messages, or InMail for individual developer accounts. Those capabilities are restricted to partner-only Sales Navigator/Talent Solutions APIs.
- LinkedIn outreach output is permanently draft-only in MVP scope. The user manually copies and sends drafted outreach messages in the LinkedIn app.
- LinkedIn publishing may be automated only through `LinkedInPublishingGateway` and `LinkedInApiClient`, only for approved posts, and only after a separate explicit Telegram confirmation of a frozen request.
- No agent may scrape or programmatically search LinkedIn. Prospect data is manually provided by the user (name, profile URL, notes) and enriched by agents - never discovered via scraping.
- No agent may fabricate shared connections, experiences, skills, or credentials the user has not actually stated.
- Follow-up cadence defaults to `FOLLOWUP_CADENCE_DAYS=21`, stored as a configurable value in the SQLite `core_intent` table and loaded from human-edited `core_intent.json`. Agents must read the configured value, not hardcode cadence logic.
- Calendar blocking only triggers on explicit user confirmation (e.g., `/meeting_confirmed`), never on inferred/parsed natural language intent from a reply.
- All model calls must go through `ModelOrchestrationAgent`. No agent calls an LLM/VLM/image provider directly.
- `NetworkOrchestrator` coordinates all specialist agents. Telegram bot handlers call the orchestrator, never agents directly.
- `LinkedInApiClient` is the only module allowed to make LinkedIn HTTP requests. `LinkedInPublishingGateway` owns frozen previews, durable confirmation, idempotency, and audit state; it has no content-generation logic.
- LinkedIn uses the official authorization-code OAuth flow and REST APIs directly. LinkedIn MCP is prohibited: do not configure, call, create, or maintain a LinkedIn MCP server.
- Phase 8G-B1 requests only `openid`, `profile`, and `w_member_social`; tokens are encrypted before storage.
- Phase 8G-B2 supports explicitly confirmed text and single-image member posts. Phase 8G-B3 adds richer member formats through the same request lifecycle. Authentication or package approval alone never enables publishing.

## Agent Architecture

`NetworkOrchestrator` coordinates:

1. `ProspectDiscoveryAgent` - structured intake and enrichment of manually-provided prospect info. In Phase 8F it may create review-only candidates from stored, approved public-signal metadata, score and deduplicate them, and convert them to CRM prospects only after explicit user approval. It does not search or scrape LinkedIn, fetch profiles, collect private contact data, or contact anyone.
2. `ProfileContextAgent` - extracts deterministic prospect context from user-provided profile text/notes for outreach drafting, and owns deterministic personal-brand profile validation, version retrieval, and prompt-ready rendering. Personal-brand versions live in SQLite; the JSON seed is an initialization input only, and normal workflows use the active SQLite version.
3. `OutreachDraftAgent` - drafts connection requests and follow-up messages. Permanently draft-only; never sends, because LinkedIn's public API does not support programmatic outreach for individual developer accounts.
4. `RelationshipTrackerAgent` - CRM. Tracks contact status, last-touch date, follow-up-due flags, meeting status.
5. `ContentInspirationAgent` - drafts LinkedIn posts inspired by (not copied from) high-engagement creator patterns in similar niches. It also owns the storytelling/editor role: revisions rewrite the complete narrative through `ModelOrchestrationAgent`, must materially change the text, and preserve immutable text versions. There is no separate StorytellerAgent. In Phase 8D it converts source-traced opportunities into reviewable content packages with alternative hooks, factual-claim records, personal-angle safeguards, controlled revisions, and image coordination through `image_gateway`. It does not fetch sources, score signals, create opportunities, call providers outside the approved model/image boundaries, publish to LinkedIn, or interact with Telegram directly. User-uploaded images take precedence when explicitly selected.
6. `CalendarAgent` - blocks calendar time on explicit meeting confirmation via `/meeting_confirmed`. Email invites are future scope, not MVP.
7. `RefinementLoopAgent` - tracks reply/engagement outcomes for `OutreachDraftAgent` and `ContentInspirationAgent`, proposes refinements, and tests them against a fixed evaluation set. See Refinement Loop Rules below.
8. `SignalIntelligenceAgent` - normalizes, canonicalizes, deduplicates, and persists items from explicitly approved public RSS or Atom feeds. In Phase 8C it also applies deterministic eligibility gates and scoring, requests bounded semantic analysis only through `ModelOrchestrationAgent`, combines auditable final scores, and persists reviewable content opportunities. It does not fetch directly, draft final posts, call image providers, discover prospects, interact with Telegram, schedule work, or publish to LinkedIn.

Supporting integration modules (not decision-making agents):

9. `LinkedInPublishingGateway` - durable frozen-preview, confirmation, idempotency, and uncertainty boundary. It delegates provider HTTP only to `LinkedInApiClient` and has no content-generation logic.
10. `LinkedInApiClient` - the sole official LinkedIn REST HTTP boundary for allowlisted Posts, Images, Videos, and Documents operations. It never reads business tables or decides approval.
11. `public_signal_gateway` - thin HTTP and RSS/Atom parsing boundary for explicitly approved public sources. It validates URLs and network targets but does not persist, score, or generate content.

## Refinement Loop Rules

- `core_intent.json` is human-editable and loaded into the SQLite `core_intent` table on startup or explicit reload. Agents read the SQLite table, not the JSON file directly.
- Personal-brand profile facts are human-controlled, versioned in SQLite, and separate from both `core_intent` and `refinable_parameters`. Refinement workflows must not silently change them.
- Agents must distinguish interests, affiliations, attendance, employment, completed work, achievements, and verified personal experience. They must not invent personal experiences or convert broad positioning into factual claims.
- `RefinementLoopAgent` may only modify the SQLite `refinable_parameters` table (tone variations, phrasing patterns, structural choices).
- `RefinementLoopAgent` must never modify `core_intent.json` or the SQLite `core_intent` table. Changes to `core_intent.json` require explicit human edit, never agent-written.
- Every refinement is versioned and logged to the SQLite `refinement_history` table with: version, timestamp, what changed, why, metric before/after, and a diff against v1 (the original).
- Before a refinement is accepted, run a semantic drift check: does the refined prompt still satisfy every rule in the SQLite `core_intent` table? Reject if any rule is violated, regardless of metric improvement.
- Cap automatic refinement iterations at 5. After 5 cycles, pause and require human review before continuing.
- Any refinement must be able to be rolled back to any prior version.

## Interface

Telegram bot is the primary interface. All approval, editing, and confirmation flows happen via Telegram commands and inline replies. Data is persisted in SQLite for MVP, not just in-memory or chat history.

## Development Rules

- Keep the MVP scoped to the 8 specialist agents and supporting integration modules above. Do not add new agents without updating this file first.
- Prefer structured data (typed dataclasses/pydantic models) over loose dicts, consistent with prior projects (`video-data-agent`, `ads-agent`).
- Keep Telegram bot handlers thin - they validate input and call `NetworkOrchestrator`, never agents directly.
- Telegram profile commands call `NetworkOrchestrator`; they never access profile tables directly.
- Keep model orchestration separate from bot handlers and from business logic.
- Content opportunities are not post drafts. `ContentInspirationAgent` remains the future owner of approved post packages; personal-brand facts and scoring configuration remain human-controlled.
- Approval for later posting remains internal. Publication additionally requires an unexpired frozen request and explicit `/confirm_publish <request_id>`; freeform consent is invalid.
- Phase 8E adds no specialist agent. The briefing runner is operational infrastructure that invokes `NetworkOrchestrator`; it may prepare review work but cannot approve, publish, send outreach, or alter profiles and scoring weights.
- `public_signal_gateway` is the only public-feed HTTP boundary. It validates RSS/Atom URLs, blocks LinkedIn and private-network targets, and does not write SQLite or call models.
- Use mock mode by default for all model/image calls during development (`MOCK_MODE=true`), same pattern as `ads-agent`.
- Use Nvidia NIM as the default model provider (same pattern as `video-data-agent`), configurable via `.env`.

## Testing Rules

- Every agent needs unit tests for normal cases and edge cases.
- `RefinementLoopAgent` needs tests proving: core_intent violations are rejected even when metrics improve; iteration cap is enforced; rollback works; SQLite history log is append-only and accurate.
- `CalendarAgent` needs tests proving it never triggers without explicit `/meeting_confirmed` command.
- `OutreachDraftAgent` and `ContentInspirationAgent` need tests proving no fabricated claims appear in output (no invented shared connections, skills, or credentials).
- Follow-up cadence logic needs tests proving it reads `FOLLOWUP_CADENCE_DAYS` from `core_intent` and never suggests contact more frequently than the configured default of 21 days.
- LinkedIn publishing tests must prove disabled/mock network isolation, exact frozen payloads and asset hashes, one-time confirmation, replay prevention, no automatic write retries, secret redaction, and durable uncertainty.
- Rich LinkedIn formats must use the same durable publication request path. Media URNs may come only from provider initialization responses, article URLs must pass public HTTPS checks, and uncertain processing must never trigger polling or an automatic retry.
- Startup reconciliation may only mark interrupted LinkedIn writes uncertain. It must never resume, repeat, or infer success for a provider write.
- Manual uncertainty resolution is append-only and must preserve the original request state and provider uncertainty evidence.

## QA Edge Cases

- Prospect with missing/incomplete profile data.
- Prospect marked meeting-confirmed with no email on file (should not attempt invite).
- Refinement that improves reply-rate metric but violates core_intent (must be rejected).
- User uploads image AND requests generated image in the same post (user upload wins by default).
- Follow-up due for a prospect who already replied (should not re-trigger).
- Telegram command sent with malformed/missing arguments.
- LinkedIn publish attempted without prior approval flag (must be rejected).

## Required Commands

After any code change:

```bash
python -m pytest
python -m mypy .
python -m ruff check .
```

Phase 9 release checks may also be run with:

```bash
python scripts/release_check.py
```

This gate is local and provider-write-free. It validates configuration,
command registration, tracked-file secret patterns, SQLite migration and
read-only integrity, then runs the required test, type, and lint commands.
Real LinkedIn publishing remains disabled unless a separately approved,
package-specific live test explicitly changes both publishing switches.

Phase 10 deployment remains single-instance and SQLite-backed. Telegram
access is deny-by-default through numeric `TELEGRAM_ALLOWED_USER_IDS`; no
display-name or username authorization is allowed. Production packaging uses
the reviewed systemd units in `deploy/`, a stable HTTPS reverse proxy for the
LinkedIn callback, restricted persistent directories, and verified backup
scripts. A real domain, owner Telegram ID, and explicit operational approval
are required before private-beta startup.

If these are missing, create the closest equivalent scripts.

## Final Response Rule for Codex

Whenever completing a task, summarize:
1. What files changed
2. What was implemented
3. What tests were added
4. What commands were run
5. Any known limitations or ambiguities needing my clarification
