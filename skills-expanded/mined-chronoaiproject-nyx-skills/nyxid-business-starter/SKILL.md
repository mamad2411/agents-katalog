---
name: nyxid-business-starter
description: Owner onboarding for small businesses on NyxBot. Use when the owner asks to set up a queue manager, a business FAQ, or reservations (alone or combined), or names this skill. Interviews the owner, connects Notion, Telnyx and CMA, has a CMA worker build the Notion hub and research the FAQ, creates one customer-facing front-desk specialist, sets guest access and approvals, links a Telegram bot, and runs a test. Guidance only; it grants no permissions.
version: "0.14"
metadata:
  category: tool-based
  tool-list:
    - nyx__connect_service
    - nyx__wait_for_connection
    - nyx__search_tools
    - nyx__call_tool
    - nyxid__list_my_services
    - nyxid__set_approval_mode
    - nyxid__spawn_subagent
    - nyxid__update_subagent
    - nyxid__set_guest_access
    - nyxid__search_agent_skills
    - nyxid__preview_agent_skill
    - nyxid__set_agent_skills
    - nyxid__channel_bot_setup_link
    - nyxid__update_channel_access
    - nyxid__create_schedule
    - nyxid__settings_link
    - nyxid__remember
  tag:
    - nyxbot
    - onboarding
    - small-business
    - notion
    - telnyx
    - cma
---

# Business starter

You are setting up a customer-facing front desk for the owner's business. The owner
picks one or more modules: **queue** (walk-in queue with SMS), **faq** (answers from
the business's own facts), **reservations** (booking requests saved to Notion).
Work through the steps in order, one step per message. Never skip the confirmation
cards NyxID raises, and never ask the owner to paste a secret into chat: use connect
links and settings links.

**Reading this skill.** The steps point to files under `references/`. Attach this
skill to yourself first (`nyxid__preview_agent_skill`, then `nyxid__set_agent_skills`
for NyxBot) and read each reference with `nyxid__skill_read` (`path`
`references/<file>.md`, following `next_offset`). Reading the whole package from
Ornn in one call is cut off at your tool-result limit. Never ask the CMA worker to
send skill files back; it has its own copy.

## Facts that shape the design

- Customers talk to the front desk as **guests**. Guest turns get the specialist's
  description and persona, but **no skills, no memory**. Everything a customer
  needs must be in the description (2048 characters) or in Notion pages the
  specialist reads at guest time. Build it that way.
- Guests may only do what `guest_access` allows per service: `read` (lookups),
  `use` (lookups and creating new things), `all`. Guests are refused any call that
  needs owner approval.
- NyxID's published Notion operations cover the whole hub, including
  `{notion slug}__notion_create_database`. The CMA worker builds it with those
  operations (step 4). If CMA is unavailable, create the databases yourself
  with the same operation and the schemas in references/notion-hub.md.
- Dates and "today" use the business timezone, not UTC.
- NyxID's platform Telnyx offering is AI chat only. SMS uses the owner's own
  Telnyx account through `api-telnyx` (or `api-telnyx-oauth`): their number, their
  messaging profile and their local sender registration.
- One channel bot links to exactly one agent, so all chosen modules share one
  front-desk specialist. Organization specialists cannot link channel bots; set
  this up on the owner's personal account.

## Steps

1. **Scope.** Confirm the modules, business name, city/country, timezone and the
   owner's preferred customer language. If the owner arrived from a checklist
   message, read the modules from it and confirm them.
2. **Interview.** Ask only the questions for the chosen modules
   (references/interview.md). As soon as you have the answers (often already in
   the owner's first message), and before ending that turn, save them with
   `nyxid__remember` as 1-3 notes starting "{business} setup:" (each at most 500
   characters; policies, contacts and sources only, never customer data).
   Attaching this skill and every CMA wait can reset your working context, and long
   owner messages then come back truncated. At hand-over, replace these notes with
   the hub IDs note.
3. **Connect services** (references/services.md). Use `nyx__connect_service` and
   `nyx__wait_for_connection`. Needed: Notion (always), CMA (for setup), Telnyx
   (queue SMS), Firecrawl (FAQ research, optional). Ask the owner to create an
   empty Notion page named "NyxBot - {business}" and share it with the NyxID
   integration during Notion consent. Record the exact connected slugs, e.g.
   `api-notion-3`, from `nyxid__list_my_services`.
4. **Build the Notion hub with CMA** (references/cma-handoff.md, task
   `notion-hub`). Then verify by reading the parent page children and each
   database's schema yourself. Do not trust the worker's report alone.
5. **Research the FAQ with CMA** (faq module, task `faq-research`). Meanwhile ask
   the owner to send the menu as a photo or PDF in this chat; read it yourself and
   append it to the FAQ Menu section (one line per dish with its price) with the
   Notion append-blocks operation. When the worker reports, show the owner its
   "Open questions" list, get answers and append them (source "owner"). Never
   publish ingredient, allergen, halal, vegan or price claims the owner or an
   official source did not state.
6. **Create the front desk** only after step 4's hub IDs are verified, so the
   description carries real IDs (editing it later needs a specialist read that
   can fail). Compose its description from
   references/front-desk-description.md (stay under 2048 characters; count).
   `nyxid__spawn_subagent` with name `front-desk` (if listing specialists fails,
   still call spawn; a duplicate name returns an error you can act on), the
   owner's chosen display name,
   persona from the owner's tone, and services = the Notion slug, `ornn-api`
   (a specialist reads its own attached skill through Ornn; without this grant its
   skill fails to load with `api_key_scope_forbidden`) and the Telnyx slug if queue
   SMS is on. Then attach the **latest** version of the Ornn skill
   `nyxid-business-front-desk` (GUID a41f05ed-994f-4f26-ab89-a28ad0b24ccc): look it
   up with `nyxid__agent_skill_versions` (never reuse a version remembered from an
   earlier setup), preview it with `nyxid__preview_agent_skill`, then
   `nyxid__set_agent_skills` for `front-desk`.
7. **Permissions** (references/go-live.md): guest access, approval settings, SMS
   mode, optional Full access override, optional confirmation schedule.
8. **Channel.** `nyxid__channel_bot_setup_link` (platform `telegram`, agent
   `front-desk`). After the owner finishes, `nyxid__update_channel_access` with
   `private_chats: everyone` so customers can chat.
9. **Test.** Owner smoke test first, read-only: message the front desk "queue"
   and "pending bookings" (nyxid__message_subagent) and check its answers cite the
   hub. Do not create test rows in a live hub unless the owner asks; mark any
   test rows Left or Cancelled with Notes "setup test". Then the customer test in
   references/go-live.md from a second Telegram account (the owner is never a
   guest).
10. **Clean up CMA.** Stop the worker, then delete it (deleting a running agent
    fails). It is not needed for daily operation.
11. **Hand over.** Summarize: bot link, Notion hub link, owner commands ("queue",
    "next", "served 12", "pending bookings", "confirm R-4F2A"), what customers can
    do, known limits, and how to pause (Disable the bot or set private chats to
    owner). Remember the hub IDs with `nyxid__remember`, prefixed with the business
    name so several businesses never mix.

## Rules

- Each module is optional; never create databases, grants or schedules for modules
  the owner did not choose.
- Prefer the narrowest permission that works. Explain each permission card in one
  plain sentence before it appears.
- If a step fails, say exactly what failed and what the owner can do; do not claim
  completion. If specialist listing or waiting tools fail, continue: spawning and
  messaging still work, and specialist reports arrive on their own. Re-running a step must not duplicate databases or specialists: check
  for existing ones first.
- After an interrupted turn, a restart or a context reset you see a recap in which
  long owner messages may be cut short (marked truncated, or with a "…" in the
  middle). Before treating any interview answer as missing, read the owner's full
  messages with `nyx__conversation_history`. Never ask the owner again for, or tell
  a worker it lacks, something the owner already sent.
- NyxID wakes you without an owner message at most 3 times in a row (CMA ready,
  CMA finished and specialist reports each count); after that the thread waits for
  the owner. So send both CMA tasks in one input, and after
  `nyxid__message_subagent` call `nyxid__wait_for_subagents` in the same turn.
  Whenever you end a turn expecting a wake-up, tell the owner: "If I haven't
  updated you in a few minutes, reply 'continue'." Never promise that NyxID will
  resume you.
- Customer data lives only in the owner's Notion. Never put it in skills, memory,
  descriptions or CMA prompts.
