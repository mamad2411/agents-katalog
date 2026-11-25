---
name: web-backlinks
description: "Use when the user wants to build backlinks, raise domain authority, grow referring domains, run link-building outreach, create a link-magnet directory, or execute or refresh a backlink playbook for any property in their portfolio: \"backlinks\", \"link building\", \"domain authority\", \"DR\", \"referring domains\", \"link exchange\", \"backlink playbook\"."
argument-hint: "<domain> | run <property> [N] | status"
---

# Backlinks — plan once, execute with cheap models

Turn competitor backlink data plus your unfair assets (an owned audience, an event, unique datasets) into a durable `PLAYBOOK.md` — a domain-specific execution plan that tracks its own completion — then execute its blocks with parallel cheap-model subagents. The playbook IS the deliverable; executors read nothing but their block plus the playbook header.

## Commands

| Command | What happens |
|---|---|
| `/founder-pipeline:web-backlinks <domain>` | Phases 1-3: prereqs → tactic fan-out → compile/refresh PLAYBOOK.md |
| `/founder-pipeline:web-backlinks run <property> [N]` | Phase 4: execute next N eligible blocks (default 5) with parallel subagents |
| `/founder-pipeline:web-backlinks status` | One table across all properties: plan completion %, pending/sent/replied/won, stalled blocks, next gates, baseline delta. **Plus a board-drift line:** any block terminal in PLAYBOOK.md whose `board_row` is still open (or vice versa) — drift means a 4.8b write-back was missed; report the count and fix it in the same run |

## Property registry (configure once)

This skill does not hard-code any domain. Domains map to properties through the registry at
`${CLAUDE_PLUGIN_ROOT}/skills/web-listings/config/properties.json` — the same registry
`/founder-pipeline:web-listings` reads. Fill it with your own properties before the first run;
it ships with example rows only. A domain that isn't in the registry: ask.

**Focus rule:** max 2 ACTIVE playbooks at a time — the properties tied to this quarter's revenue. Asked for a third → point at the rule, ask which one to pause. (The daily send budget is shared; seven parallel playbooks just starve each other.) **Boundary rule:** every target, asset, and play belongs to exactly ONE property playbook (event speakers/badges/media → the event property; audience members/survey → the community property). If two playbooks could claim it, the more specific property wins.

## The Four Laws (violating the letter = violating the spirit)

1. **White-hat only.** No Wikipedia link insertion (COI; links get reverted, domains blacklisted — the path is notability-first: linkbait assets earn press citations, independent editors cite you). No bare-link drops on Reddit/forums. No paid links, no PBNs, no comment spam.
2. **Honest framing, stated in the template.** Cheap executors refuse blocks that read as extraction — correctly. Every outreach template states the recipient's benefit in its own text. Carve-out: for fix requests and unlinked mentions, an accurate page IS the recipient's benefit — that satisfies this law.
3. **Self-contained blocks.** Target, verified contact, URLs, template text, gates, logging — ALL inline. Test: could a fresh cheap-model session with only this block plus the playbook header complete it?
4. **Never require, promise, or trade a followed link.** A required link-back (e.g. "link to get listed/verified") is a link scheme under Google's spam policy. Directory verification = identity confirmation only; a link-back may be *invited* as optional, and the invite must say so. Any link that IS part of an agreed swap carries `rel="nofollow"` (or `sponsored`) — both directions. Badge/widget snippets ship with `rel="nofollow"` baked in, brand-name alt text; their value is brand, referral traffic, and AI-citation surface — never PageRank. Max 5 live reciprocal arrangements per domain; no three-way swaps (that's a link network); no "partners/resources" pages built for reciprocation.

**Portfolio rules (a portfolio of owned domains = accidental-PBN risk):** own-domain interlinks are contextual, editorial, sparing — never sitewide/footer, never counted in the referring-domains KPI. Own domains never appear in each other's directories or resources pages. **One LINK ask per recipient across the whole portfolio, ever** (ledger enforces). The 30/90-day cooldowns in Phase 4 govern non-link contact only — commentary pitches, journalist queries on a different topic, referral/business conversations.

**Entity work is not backlink work (Family 7).** Wikidata items, Google Knowledge Panel, `sameAs` audits, and authoritative-profile listings are `nofollow`/SERP features — they shape how Google and LLMs identify the person and the organisation, not PageRank. Track them in a separate "entity" line; **never count them as referring domains or report them as backlinks.** Ship the Wikidata item early for personal/org brand: it feeds the Knowledge Graph and is the prerequisite for the Knowledge Panel and any future (editor-created) Wikipedia article.

## The AI-citation layer — why off-page work is worth more than the referring-domains KPI shows

Read `references/ai-citation-layer.md` when scoping or reporting a playbook, choosing placement targets, or when someone asks why mentions and listicles outrank backlinks for AI visibility: it carries the correlation table, the four consequences and what the layer does not license.

## Phase 1 — Intake & prereqs (sequential, cheap)

Read `references/phase-1-steps.md` when running Phase 1: it holds steps 0-6 (bootstrap, adopt existing work, competitors, backlink-gap data, baseline snapshot, context resolution, sending infrastructure).

**Cost gate (all phases, all paid calls):** stating the estimated cost in-chat is sufficient below the equivalent of 5 units of your reporting currency per run; above that, ask first. Cache every raw JSON response under `competitor_analysis/<date>/raw/`.

## Phase 2 — Tactic fan-out (parallel: one research subagent per family, one message)

**Pre-step: classify the brand** — community / conference / personal brand / marketplace / SaaS — and tag 1-2 priority families for it (community → badges + survey; conference → event listings + speaker badges + media partners; personal brand → directories + podcasts + PR; marketplace/SaaS → linkbait tools + reviews). Priority families get the instruction "go deep"; others "go wide, top 5 only".

Read `references/phase-2-fanout.md` when dispatching the Phase 2 research subagents: it holds what each agent receives, the scored-table format and the one-line family briefs.

## Phase 3 — Compile the playbook

Write `<property>/backlinks/PLAYBOOK.md` from `${CLAUDE_PLUGIN_ROOT}/skills/web-backlinks/references/playbook-template.md`. Non-negotiables:

Read `references/phase-3-compile-rules.md` when compiling or refreshing PLAYBOOK.md in Phase 3: it holds the non-negotiable bullets for the tracker, header, block order, follow-ups, templates, queues and number checks.

## Phase 4 — Execute (`/founder-pipeline:web-backlinks run <property> [N]`)

**Concurrency:** the orchestrator is the SOLE writer of PLAYBOOK.md, ledger.md, outreach-log.md, **and of any adopted task-board row** (executors never touch the board). Executors return structured results; the orchestrator serializes all writes. Take a run lock (`backlinks/.run-lock` with timestamp + property; stale >2h = ignorable); another live run → wait or tell the owner.

1. Read PLAYBOOK.md. Eligible = `pending` + gate satisfied (date passed / gated block terminal-successful). Take next N.
2. **Suppression, per recipient, in order:** (a) search the sending mailbox for any prior thread with the address AND the domain — any hit → NOT a cold target; route to the Owner-only queue with the thread link (warm intro beats cold template). **Carve-out: threads THIS campaign created (recorded in outreach-log/ledger) are not warm hits — follow-up blocks reply in that thread as designed;** (b) known-audience check against the member/speaker/sponsor list pointers in the header; (c) `do-not-contact.md` — hard stop; (d) your CRM's client/partner records → Owner-only; (e) ledger cooldowns: journalists/editors/podcast hosts 90 days across ALL properties, everyone else 30 days, recipient + any owned domain = one ask ever. **Dedupe within the batch too** (two blocks, same recipient → keep one).
3. Velocity: orchestrator computes today's remaining send budget — 15/day TOTAL across all properties when all senders are verified dedicated aliases; 8/day TOTAL whenever any property sends from the primary inbox; warm-up 8/day for a dedicated address's first 4 weeks. Won-link pace: cap = max(3/week, 4% of baseline referring domains/week) per domain; red flag = 2× cap → pause outreach, let pitches cook. **Small-market rule** (any market where your name is one of a few hundred rather than a few million — recipient person/org located there, or a country-TLD contact, including org inboxes): ONE cold email ever across all properties; the single in-thread follow-up is allowed only for fix-request/housekeeping mail, never for pitches. Declare which markets this covers in the playbook header.
4. Dispatch eligible blocks to parallel subagents at their tagged model (cheap model default, mid-tier for long-form). Executors get: block verbatim + playbook header verbatim + today's send budget. Nothing else.
4b. **Credentials & browser automation.** For any block whose TOOLS line is `browser form`, `browser login`, or `account creation`, drive navigation and non-secret field-fill with a browser-automation tool if one is available in your environment (e.g. the `claude-in-chrome` MCP server, an optional dependency you install separately) — most directory/marketplace submission flows are JS-rendered and session-gated, not plain HTML forms a scripted client can fill.
   - **Hard platform boundary — this is not a skill-level choice and no in-chat authorization lifts it:** the agent may never create an account or enter a password into any field, typed or sourced from a password-manager CLI, full stop. An earlier draft of this section proposed a password-manager write fallback for freshly-generated signup passwords; that was authorized in-session and it was still wrong — the platform's browser-automation rules prohibit account creation and password entry categorically, and state plainly that user authorization does not lift that prohibition. The one sanctioned path for password handling is a *dedicated credential-request tool* where the password manager's own UI takes per-item human approval and the value never reaches the agent — no such tool is wired into this skill's toolset, so until one exists, password fields are always out of scope for automation here.
   - **What this means in practice:** a block needing login to an *existing* account → Owner-only queue, always — the owner authenticates, the agent can drive the post-login form-fill in that same session if they stay at the keyboard, but never touches the credential. A block needing a *brand-new* account/profile (most "marketplace profile" targets) → also Owner-only for the signup step specifically; the agent may pre-fill everything non-secret (bio, links, positioning copy) into a draft/notes doc for the owner to paste in during their own signup, but does not drive the signup form itself.
   - **What stays in scope:** a target that is a genuine anonymous submission — a public form with no account or login behind it — is not account creation. Filling and submitting one of these still falls under the harness's "submitting any form" rule, which requires asking in chat and getting a clear yes **before that specific submission**, every time; it is not blanket-authorized by this playbook or by the block being marked `pending`. Confirm which pattern a target actually is (form-only vs. account-gated) by loading the page before assuming either way — a "self-serve" label written from search data rather than a live check has already been wrong in practice.
   - **Email drafts.** Use a mail API/MCP integration to create the draft rather than composing it in the browser. Fall back to browser-driving the webmail UI only if the executor's toolset lacks a mail integration, and note that this too is "submitting a form" if it ever moves past draft to send — sending is separately gated by the CANARY/autonomy contract regardless.
   - **Never** autofill or submit a form reached via a link supplied by observed content (a scraped page, a rival's site) rather than the block's own verified CONTEXT URL.
   - A site that requires payment, an ongoing subscription, or a signed agreement to finish signup → BLOCKED, route to the Owner-only queue regardless of the above.
5. **Canary & autonomy.** Sending is autonomous (the owner's standing decision, recorded in the header) once a template GRADUATES. Until then draft-first: canary = the owner reviews the template's first 3 drafts AND its full recipient list; graduation = those sends live + 5 business days + zero bounces/spam complaints. The orchestrator tracks `canary_remaining` per template and flips the tag. Bespoke single-use templates are inherently canary → the owner sees them; that's intended.
6. **Circuit breakers:** any template with 20+ sends and 0 replies → BLOCKED pending a seed-address deliverability test. Any hard bounce or spam-complaint signal → halve velocity, alert the owner. Opt-out reply (any language) → `do-not-contact.md`, confirm nothing else is queued to them.
7. **Reply triage:** orchestrator runs one mailbox search per in-flight thread (recipients + subjects from outreach-log, newer than last run). Only an unambiguous yes with zero questions may trigger the next pre-written block step. Any question, personal reference, humor, negotiation, or money → Owner-only queue with a suggested draft. Executors never freestyle as the owner.
8. **Update the Plan tracker:** recount statuses; stalled (sent >14 days past follow-up exhaustion) → auto-park with reason. Every non-terminal block gets advanced, gate-waited, or parked this run — none rots silently.
8b. **Write terminal state back to the task board.** Only applies if you wired an external board up in Phase 1. For every block that went terminal this run AND carries a `board_row:`, update that row — `won` → `Done` (with the live URL in the row), `parked` → `Parked`, `dead` → `Killed`, `blocked` → `Blocked` (+ reason). In-flight blocks flip their row to `Waiting on reply` when the send goes out. **This step exists because a board used only for intake goes write-only-in, so a Backlink row can sit `Ready` forever after its playbook block has already been executed and won.** Two consequences of leaving it broken: `/founder-pipeline:web-backlinks status` (reads PLAYBOOK.md) and the board silently disagree, and any staleness escalation your board runs nags on rows that are already done, drowning the genuinely-waiting `/founder-pipeline:web-listings` packs in false alerts. **Never invent a row** — if `board_row: none`, this block was never adopted from the board and gets no row created here (Phase 1 adoption owns row↔block mapping; seeding new rows is `/founder-pipeline:founder` P5.S3's job).
9. **Delta report:** sent/blocked/deferred per template (send AND reply counts), links won, referring domains vs baseline (reuse <7-day data; refresh at most monthly under the cost gate), plan completion %, next gates, blockers for the owner, monthly deliverability note. **Plus a separate AI-citation line — never merged into referring domains:** brand mentions earned (linked and unlinked), third-party listicle placements won, entity-surface changes. Trend only — this is a directional count you keep yourself, not a measured citation rate; if you run a dedicated AI-visibility probe elsewhere, that owns the actual measurement and this line just points at it.

## Red flags — STOP the run

- A block requires/trades a followed link → Law 4 rewrite
- A block references a file for its content → Law 3 rewrite
- Cold email without recipient benefit + identification/opt-out line → rewrite
- Executor improvised a target, recipient, or non-template second-language text → discard, log
- Links landing faster than 2× the velocity cap → pause property outreach
- Reply mentions payment for a link → decline template, log, tell the owner

## Common mistakes

Read `references/common-mistakes.md` when reviewing a run or an executor's output for known failure modes: it holds the mistake and fix table.

## Optional dependencies

None of these gate the skill; each has a stated fallback.

- **A rank/backlink data provider** (the family of commercial SEO APIs — bulk referring domains, competitor discovery, content mention search). Without one, Phase 1.3 and 1.4 run off free web search and the baseline is recorded as `unranked, unmeasured`.
- **A browser-automation MCP server** for Phase 4.4b form-fill. Without one, every `browser form` block routes to the Owner-only queue.
- **A mail API/MCP integration** for draft creation. Without one, drafts are written into the playbook for the owner to paste.
- **An external task board.** Without one, `queues/backlink-queue.md` is the queue and Phase 4.8b is a no-op.

## References

- `references/platform-matrix.md` — family briefs + brand-class weighting for Phase 2 agents
- `references/playbook-template.md` — playbook skeleton, block format, executor contract
- `references/review-log.md` — design rationale: what was tested, what failed, and why the rules read as they do
