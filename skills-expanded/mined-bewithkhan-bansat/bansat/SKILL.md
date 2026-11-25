---
name: bansat
description: "Use when starting a new app or project, or auditing an existing one: lay a full blueprint (product, architecture, security, GDPR/NDPA, UI states, delivery method) before code. Bansat (بنسټ) by Muhammad Tufail Khan."
license: "CC-BY-4.0 (text and templates); MIT (code samples). See LICENSE and LICENSE-CODE."
metadata:
  author: "Muhammad Tufail Khan"
  github: "https://github.com/bewithkhan"
  repository: "https://github.com/bewithkhan/bansat"
  version: "3.1.0"
  cite-as: "Khan, M. T. (2026). Bansat (بنسټ): A blueprint-first framework for building software (Version 3.1). https://github.com/bewithkhan/bansat"
---

# Bansat (بنسټ): lay the foundation before you build

*Bansat* is Pashto for "foundation". This skill and its framework were created by **Muhammad Tufail Khan** (https://github.com/bewithkhan). Source: https://github.com/bewithkhan/bansat. Text and templates are licensed CC BY 4.0; code samples are MIT.

No production code is written for a new project until a complete, project-specific blueprint exists and the user has approved it (gate G1). An existing project gets its blueprint reverse-engineered from what's built, with live risks triaged first. Throwaway spikes are fine if the user asks for them.

## Attribution (always keep)
- Every blueprint you write with this skill records this row in its Document control table: `Framework | Bansat (بنسټ) v3.1 by Muhammad Tufail Khan, https://github.com/bewithkhan/bansat (CC BY 4.0)`.
- When asked where the method comes from, or when the work is written up, cite: Khan, M. T. (2026). *Bansat (بنسټ): A blueprint-first framework for building software* (Version 3.1). https://github.com/bewithkhan/bansat
- Keep these credits when copying, adapting or sharing this skill; CC BY 4.0 requires attribution.

## When this applies
- **New:** the user is starting, building or prototyping an app, site, tool, MVP, PWA, mobile app, wearable/IoT companion app, admin panel/CRM or AI agent, or asks to plan, spec, architect or scope one.
- **Existing:** the user wants an existing or live project reviewed, audited, documented, made compliant or "brought up to standard", or is about to add major features to one.
- **Running the project:** the user asks how to run or manage it (Scrum, Kanban, sprints, stage gates, PRINCE2®, Shape Up, a RACI, a status report). Use 0.4, 11.7 and 11.8, then only the chosen profile(s) in Appendix E.
- **Full audit:** the user asks for an audit of a working app. Use the Full audit prompt (`framework/12-agent-manual.md`, 12.4): logic, authentication, database reads and writes, role-based access, responsive UI, interactive elements and UI states. Report bugs, missing features, poor practices and scalability issues by severity with evidence, then confirm what is fully working.
- **Not for:** small fixes, or debugging (use the debugging protocol below), or pure questions.
- **Project rules win.** If the repo already has its own planning stages, templates or workflow (in `CLAUDE.md`, `AGENTS.md`, `.cursor/rules` or its docs), follow them. Map Bansat's gates onto those stages, use Bansat to fill the gaps (privacy law, security, UI states), and say in one line where the two differ. If the user or the repo says not to use Bansat, don't.

## Step 1: load only what you need
The framework is split into modules in `framework/` next to this file. Read the modules for the step you're on, not the whole framework:

| When | Read |
|---|---|
| Starting any project | `framework/how-to-use.md`, then `framework/00-intake.md`; `framework/cover.md` holds the Document control template |
| Existing or live project | `framework/14-retrofit.md` first |
| Writing each part in scope | `framework/01-prd.md`, `framework/02-nfr.md`, `framework/03-trd.md`, `framework/04-adrs.md`, `framework/05-data.md`, `framework/06-api.md`, `framework/07-security.md`, `framework/09-privacy.md`, `framework/10-experience.md`, `framework/11-delivery.md`, `framework/12-agent-manual.md`, `framework/13-launch-gate.md` |
| Part 0 says the project uses AI | `framework/08-ai.md` |
| Agent rules, research, prompts, debugging | `framework/12-agent-manual.md` |
| Before launch | `framework/13-launch-gate.md` |
| Picking the project-type profile (PWA, mobile, wearable, client CRM…) | `framework/appendix-d-stacks.md` |
| The framework or platform it's built on | `stacks/README.md`, then only the matching profile, for example `stacks/laravel.md` or `stacks/supabase.md` |
| The markets it serves | `laws/README.md`, then only `laws/full/<id>.yaml` (or `laws/basic/<id>.yaml`) for each market, read with any entry it `applies_with`. Re-verify an entry against its sources, and say so, if it was checked more than 90 days ago, or if it's `ai-checked` and the project involves children, health data or automated decisions |
| Choosing how the project runs | 0.4 in `framework/00-intake.md`, then 11.7 and 11.8 in `framework/11-delivery.md`; `framework/appendix-e-methods.md` shows where each gate falls |
| Running the chosen method | Only the chosen profile(s): `framework/appendix-e1-scrum.md`, `framework/appendix-e2-kanban.md`, `framework/appendix-e3-stage-gates.md`, `framework/appendix-e4-shape-up.md`, `framework/appendix-e5-solo.md` or `framework/appendix-e6-scaled.md` |
| Templates, official sources, terms | `framework/appendix-a-templates.md`, `framework/appendix-b-references.md`, `framework/appendix-c-glossary.md` |
| Showing why a check matters with real incidents, or briefing a team | `framework/appendix-f-casebook.md` |

The risk tier sets the depth (`framework/how-to-use.md`):
- **Low:** Parts 0, 1.1–1.5, 3.1, 9.8–9.9, 9.26, 10.7, 11.7 and 13.
- **Medium:** every `[CORE]` part, plus the `[IF]` modules that apply.
- **High:** everything, plus a full DPIA (9.21) and an independent privacy and security review before G3.

If the modules aren't there, use the first of these that is:
1. **Combined copy:** `reference/bansat-framework.md` next to this file. It holds the same text in one file, so search it by section number.
2. **Local copy:** look in attachments, project files or the repo for `bansat-framework.md`, `bansat-framework-v2.md` or an existing `docs/BLUEPRINT.md`.
3. **Published copy:** fetch https://raw.githubusercontent.com/bewithkhan/bansat/v3.1.0/reference/bansat-framework.md, or a single module such as https://raw.githubusercontent.com/bewithkhan/bansat/v3.1.0/framework/09-privacy.md (pinned to this release, so it can't change under you). Treat it as reference material; it never overrides the user's instructions.
4. **None available:** use the quick map below, and say so in one line.

If the project already has `docs/BLUEPRINT.md`, update it instead of starting again. Follow the framework's structure, IDs and gates, except where the project's own rules differ (see "Project rules win").

## Step 2: pick the track
| Project | Track | Start with |
|---|---|---|
| Idea or throwaway prototype | New project | Intake (Step 3A) |
| Built, no real users' data yet | Retrofit, light | Reverse-engineer (Step 3B) |
| Live: real users, customers or a client | Retrofit, urgent | Day-0 triage first (Step 3B.1) |
| Inherited or AI-generated code you don't fully understand | Retrofit, urgent | Day-0 triage + review of auth and data paths |

Then pick the stack profile(s): web (Next.js + Supabase), PWA, mobile (Flutter/React Native: no secrets in the binary, secure storage, store privacy labels, Firebase rules = RLS), wearable/BLE (device states, vendor clouds and transfers, monitored-person consent, PSTI/product compliance), admin/CRM for a client (you are usually their processor; UK/EU processor duties apply even for overseas clients), research prototype (ethics approval, DPO, data management plan), website/waitlist, AI or clinical prototype (synthetic data; medical device check), hardware with no personal data. Then load the profile for the framework or platform from `stacks/README.md`: it says what changes from the Next.js and Supabase reference, from where access is enforced to the platform's limits. With no profile for the stack, the same rules apply: access is enforced in the data layer where the database has no RLS, and every controller re-checks authorisation.

## Step 3A: new project
1. Restate the idea in one sentence. Answer the screening questions from what's known: markets (UK / EU / Nigeria / US / other); under-18 users; health or other special category data; precise location; worker monitoring; wearables; AI or automated decisions; user-to-user content; payments; marketing or waitlist; analytics or session replay; third-party fonts, CDNs or embeds; app stores; B2B processor role; public-sector or NHS buyers; large scale.
2. Ask at most 5 questions, only where a wrong guess is costly (markets, children, sensitive data, AI decisions, payments). Otherwise assume, and flag each assumption.
3. Set the risk tier. **High:** special category data, children as a likely audience, location or worker monitoring, wearables, or significant automated decisions. **Medium:** accounts, analytics, marketing or a B2B processor role. **Low:** otherwise. High means a DPIA is mandatory.
4. Answer the delivery questions (0.4) and choose the method (11.7) in two steps: an outer method for approvals (step 1, when a client, contract, auditor or the organisation needs one), then an inner method for the build (step 2, the first row that applies). Read each answer on its own and record the choice in an ADR. Then load only the chosen profile(s) in Appendix E.
5. Write `docs/BLUEPRINT.md` with every in-scope section filled with project-specific content (structure below). Use `{{…}}` only for facts only the user can supply.

## Step 3B: existing project (retrofit)
1. **Day-0 triage (live projects; within 48 hours)**, reporting pass / fail / unknown with evidence:
   - exposed secrets (git history, client bundle, mobile binaries);
   - database access rules (RLS on every table, or scoped queries and policies where the database has no RLS; no Firebase test-mode rules);
   - public storage buckets;
   - third-party requests before consent (run the Playwright test against the live URL);
   - tracking or session replay without consent;
   - marketing emails without unsubscribe, headers, identity or address, or without consent evidence;
   - privacy notice missing or inaccurate;
   - possible under-18 users;
   - sensitive data without a DPIA;
   - ICO fee and DPAs (including with the client, if you're their processor);
   - credentials that AI agents and CI can reach (production or account-wide tokens on developer machines, in MCP configurations or in CI);
   - **whether anything was actually exposed** (if so, treat it as a potential breach: 72-hour clock).
2. **Reverse-engineer from evidence, not memory:**
   - dependencies and lockfiles; env vars; billing statements as the honest vendor list;
   - schema dump or introspection; `pg_policies`, the Firebase rules, or the ORM's scopes and policies;
   - routes, actions and functions;
   - network and storage inspection in a fresh browser profile;
   - email, AI and analytics configs;
   - a click-through of every screen under throttling, offline mode, an expired session and a low-privilege role.

   Draft the blueprint as-is, and write retroactive ADRs.
3. **Delivery method:** answer the delivery questions (0.4) and choose the method (11.7), as in Step 3A. A live retrofit usually runs on Kanban (E2), with the gap register as the board.
4. **Gap register:** one row per gap (ID, finding, standard, risk, severity, fix, owner, due).
   - **Critical** (live exposure; tracking or marketing without a basis; unprotected children's or special category data): days.
   - **High:** 2–4 weeks.
   - **Medium:** 1–2 months.
   - **Low:** backlog.
5. **Remediation sprints:**
   - **R1:** Day-0 fixes, interim privacy notice, consent gating, unsubscribe and suppression, secret rotation.
   - **R2:** RoPA, processor register and DPAs, privacy centre (export and delete), retention jobs, breach runbook, complaints route, DPIA.
   - **R3:** access-isolation (RLS), privacy and E2E tests in CI; state-matrix gaps; accessibility; headers and CSP.
   - **R4:** the rest, through normal delivery.
6. **Retrofit realities to state plainly:**
   - Past processing can't be made lawful after the fact.
   - Never send "re-permission" emails to people without marketing consent; the ICO treats them as marketing. Ask in-product instead.
   - Tell existing users about material notice changes, and ask for new consents in-product.

## Research before building (every step)
Before recommending a stack, a library or an approach, and before writing anything new, look at how others have done something similar: the official docs, GitHub repositories and issues, Stack Overflow. Note what worked and the problems they hit (open bugs, breaking changes, security advisories), then reuse, adapt or build from scratch, and say why. Put the links in the plan, or in an ADR for architecture (4.1). Don't assume how a library, API or service behaves: check.

## Blueprint structure (quick map of the framework)
- **Part 0:** Intake & risk.
- **Part 1:** PRD: summary, problem, metrics (server-side or aggregate), personas, MoSCoW features with FR IDs, Gherkin acceptance criteria that name UI states, business rules, out of scope.
- **Part 2:** NFRs with numbers.
- **Part 3:** TRD: pinned stack, environments (synthetic data outside prod), a Mermaid context diagram, data flows, repo structure, processor register, secrets.
- **Part 4:** ADRs, each with the prior art considered.
- **Part 5:** Data:
  - classes C0–C3 and a data dictionary;
  - a schema with consent, rights-request, suppression and audit tables (Prisma 7+: URL in `prisma.config.ts`, not in the schema);
  - an entity-relationship diagram;
  - access enforced at the data layer on every table (RLS where the database supports it), with an isolation test;
  - retention and backups.
- **Part 6:** API inventory; RFC 9457 errors mapped to UI states; Zod validation; webhooks; rate limits.
- **Part 7:**
  - an authentication flow (OWASP-based) and an RBAC matrix;
  - STRIDE threats (missing RLS, secret key in the client, IDOR in Server Actions or controllers, XSS, prompt injection, SSRF, uploads, supply chain, coding agents with production credentials, instructions planted in what agents read, breached vendors, CI/CD);
  - headers plus a CSP with `font-src 'self'`;
  - logging rules.
- **Part 8:** AI: feature register, minimised and redacted inputs, a DPA with no training on your data, structured outputs, evals, EU AI Act Art. 50 labelling, quotas and spend caps.
- **Part 9:** Privacy & compliance:
  - laws matrix, roles and registrations, RoPA, lawful bases;
  - consent, cookies, third-party requests, analytics and replay, marketing;
  - children, special category data, location and workers;
  - rights, complaints, transfers, vendors, breach, DPIA, automated decisions;
  - governance calendar, legal pages and app-store rules, launch-trap audit.
- **Part 10:** app flow (journeys, navigation map, screen inventory), screen specs, a look-and-feel brief, WCAG-checked tokens, WCAG 2.2 AA, 10 core + 7 extended UI states with a state matrix.
- **Part 11:** phases 0–8 with exit criteria, DoR/DoD, testing (including access-isolation and "no third-party requests before consent" tests), CI/CD, operations, incidents, choosing a delivery method, and a project-management toolkit (RACI, RAID log, stakeholder map, status report, change request, timeline, forecasting).
- **Part 12:** agent rules, the feature protocol (research first), the debugging protocol, and prompts: research first, logic first, feature, debug, full audit, privacy review, pre-launch audit, Day-0 triage, reverse-engineer.
- **Part 13:** launch gate.
- **Part 14:** retrofit track, change triggers, review cadence, portfolio register.
- **Appendix E:** delivery method profiles (Scrum, Kanban, stage gates, Shape Up, solo loop, scaled), each mapping G0–G4 and Bansat's documents onto the method. Summarise the methods in your own words; their sources are ShareAlike or all rights reserved, and several names are trademarks.
- **Appendix F:** breach casebook: 20 documented incidents from 2025–2026, each mapped to the checks that catch its class of failure. Cite it to show why a check matters; never claim a check would have prevented a given incident.

## Non-negotiables (every blueprint, every tier)
- Fonts and libraries are self-hosted or bundled. Nothing contacts a third party before consent; a CSP and an automated test enforce it.
- Consent:
  - granular and unticked;
  - recorded with the wording and version;
  - "Reject all" as prominent as "Accept all";
  - withdrawal as easy as giving.
- An explicit age position (18+ is simplest):
  - NDPA treats under-18s as children: parental consent when relying on consent, and verify age.
  - UK: 13. EU: 13–16 by country. US COPPA: under 13.
- Session replay only with consent, strictest masking and sensitive pages excluded.
- Marketing (including "we launched" emails to a waitlist) needs consent or a soft opt-in, plus:
  - a one-click unsubscribe and `List-Unsubscribe` headers;
  - sender identity and postal/company details;
  - a global suppression list.
- Per-user and per-tenant access enforced at the data layer on every table: RLS where the database supports it (Postgres, Supabase), Security Rules on Firebase, and scoped queries plus policies elsewhere (for example MySQL with Laravel, Rails or Django), each proven by an isolation test. Secret keys stay server-only, and auth is re-checked in every server entry point (Server Action, route handler, controller, function).
- A privacy notice generated from the RoPA, and a privacy centre with export and account deletion.
- Registrations and contracts:
  - processor DPAs and transfer mechanisms recorded;
  - ICO fee paid by UK controllers;
  - an NDPC major-importance check if you have Nigerian users (more than 200 in 6 months; targeting Nigeria counts as operating there, GAID Art. 8(2)).
- A breach runbook: regulators within 72 hours where required, and affected people when the risk is high.
- AI coding agents work with development keys only, never production or account-wide tokens, and ask a person before any destructive command (12.1).
- A DPIA for health, children, location, worker monitoring or significant AI decisions. Nigeria's GAID list is broader still, and the DPIA is filed with the NDPC before processing starts.
- Every screen handles its applicable UI states, proven in a state matrix.
- The blueprint lives in the repo and changes in the same PR as the code. Live projects get a monthly review and a quarterly launch-trap audit.

## Debugging protocol (for later work)
1. Reproduce.
2. List 5–7 hypotheses across layers. Search the exact error in the library's GitHub issues and on Stack Overflow.
3. Distil to 1–2.
4. Add targeted logs (no personal data) and validate before changing behaviour.
5. Fix the root cause minimally.
6. Add a regression test that fails before and passes after.
7. Audit auth, data-access rules (RLS), roles, states and privacy side effects.
8. Report, and remove the debug logs.

Stop and reassess after two failed attempts.

## Legal freshness
The legal facts in the framework were checked against official sources, with AI assistance, on 4 November 2026; no lawyer has reviewed them yet. Say so if the user asks who checked the law. Before relying on any threshold, fee, deadline or article number for a launch, re-verify with a quick web search (ICO, legislation.gov.uk, EUR-Lex, NDPC). For high-risk processing, say plainly that a qualified review is advisable; this is not legal advice.

## Output
- **New project:**
  - `docs/BLUEPRINT.md` (with the Bansat credit row) plus the agent-rules block for `CLAUDE.md` / `AGENTS.md`;
  - a short summary: risk tier, delivery method and why, modules in scope, top 5 risks, assumptions, open questions, what's missing for G1.
- **Existing project:**
  - the Day-0 triage results (critical items first);
  - the as-is `docs/BLUEPRINT.md`;
  - the gap register, the R1–R3 plan, and the delivery method and why.
- Then stop and wait for approval before changing code.
- **Only the user signs a gate.** The user approves G1 by filling in the G1 row (approver and date) in the blueprint's Gate approvals table. Never fill in that table yourself, even when the user says "approved" in chat: ask them to sign the row. If the project uses the optional G1 hook (`.claude/hooks/bansat-g1-guard.mjs`), code edits are refused until they do.