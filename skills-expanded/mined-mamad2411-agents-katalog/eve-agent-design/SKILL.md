---
name: eve-agent-design
description: Design and build a working agent with Vercel's eve framework. Use when the user wants to build, plan, or architect an AI agent with eve — choosing the right eve features (tools, skills, connections, channels, subagents, schedules, sandbox), then building it step by step with auth, approvals, and evals. Complements the official vercel/eve skill, which covers API reference via bundled docs.
---

# eve agent design

You are helping the user go from "I want an agent that does X" to a deployed, secured, eval-covered eve agent. eve is Vercel's filesystem-first framework for durable backend agents: an agent is a directory of files (`instructions.md`, `tools/`, `skills/`, `channels/`, ...) that eve compiles and runs durably on the Workflow SDK.

**Source of truth rule:** this skill is the design methodology. For exact API signatures, always read the version-matched docs bundled in the user's project at `node_modules/eve/docs/` (start with its `README.md`) before writing eve code. If eve isn't installed yet, scaffold first (Phase 4), then read the bundled docs.

Reference files in this skill:
- `references/feature-map.md` — every eve surface, when to use it, and decision tables
- `references/security-checklist.md` — trust model, hardening steps, pre-production checklist
- `references/testing-and-evals.md` — eval strategy, `defineEval`, `mockModel`, CI gating

## The workflow

Work through the phases in order, starting with Phase 0 (detect what already exists). Do not skip Phase 1 (discovery) or Phase 2 (system design) — the design trace is where agent quality is decided; features, security posture, and eval strategy all fall out of it. Keep the user in the loop at each phase boundary: show what you decided and why before building on it.

## Phase 0 — Detect the starting point

Before asking anything, check the working directory — never ask the user something the filesystem can answer:

- `node_modules/eve/docs/` exists → eve is installed; read its `README.md` now and note the version (`npm ls eve`).
- `agent/` with `instructions.md` or `agent.ts` → an existing eve agent. Inventory it with `eve info` and treat the work as extending/hardening, not greenfield — Phases 1–2 then focus on what's missing or undesigned, and Phases 5–6 apply to the existing surfaces too.
- `package.json` without eve → candidate for `eve init .` (needs no `agent/` files yet).
- Empty or unrelated directory → plan a fresh `npx eve@latest init <name>` scaffold.

Only ask the user when the situation is genuinely ambiguous, e.g. they mention an existing project that isn't the current directory (ask where it lives), or the current directory is an unrelated codebase (ask whether to add the agent here or scaffold a sibling project). Never scaffold into a directory you haven't inspected.

## Phase 1 — Understand what they're building

Interview the user before touching code. Ask only what isn't already clear from their request, batched into one round (use the AskUserQuestion tool if available):

1. **Job**: What should the agent do, concretely? What does a successful interaction look like end to end?
2. **Surface**: Who talks to it and where — a web app, Slack, Discord, Teams, Telegram, SMS/voice, GitHub, Linear, another service via API, or only a schedule/cron?
3. **Integrations**: What external systems does it read or write (APIs, databases, SaaS tools)? Do those expose an MCP server or an OpenAPI spec, or will you call them from custom code?
4. **Identity**: Does it act as one shared app identity, or on behalf of each end user (per-user OAuth)? Is it multi-tenant?
5. **Risk**: Which actions are irreversible or sensitive (payments, emails, deletes, writes to production, regulated data)? What data must never reach the model or leave the system?
6. **Cadence**: Purely reactive to messages, or also scheduled/background work?
7. **Runtime needs**: Does it need to run code/shell commands, work with files, or do long multi-step analysis?
8. **Hosting**: Vercel (default, easiest) or self-hosted Node?

Summarize the answers back as a one-paragraph agent spec and get confirmation.

## Phase 2 — Design the system before choosing features

This is the most important phase. Do not pick eve features or write a directory tree yet — first design the agent's *behavior* and get the user to sign off on it. Work through these steps in conversation, one at a time:

1. **Trace the core scenarios end to end.** For each core job (2–4 traces: the main happy path, a sensitive-action path, and one messy/ambiguous path), narrate the runtime sequence concretely, as a numbered walkthrough:
   - What arrives — which surface, what the message/webhook/cron tick looks like, who the caller is.
   - What the agent knows at that moment — instructions, any loaded skill, history, durable state.
   - Each decision and action in order: *"it calls `lookup_order` with `{orderId: "1042"}`, which queries the orders DB and returns status + items"* — name the action, show example input and output, say where the data lives.
   - Where it must stop for a human — an approval before an irreversible step, or a clarifying question when input is ambiguous — and what resuming looks like.
   - What goes back to the user, in what form, on what surface.

   Write the traces with real example data, not abstractions. A trace that says "the agent processes the request" is not a trace.

2. **Derive the tool inventory from the traces.** Every distinct action the traces used becomes a candidate tool or connection, as a one-line contract: name, purpose, input → output, side effect class (read-only / reversible write / irreversible), data source or system it touches. Merge near-duplicates. Cut anything no trace needed — if no scenario calls it, it doesn't exist.

3. **Assign every decision to a decider.** For each branch point in the traces, decide *who* makes the call:
   - the **model** (goes in instructions or a skill),
   - **code** (goes inside a tool — validation, tenant scoping, thresholds),
   - a **human** (approval gate or `ask_question`).
   Getting this split right is most of agent design. Anything correctness- or safety-critical should be code or human, not model judgment.

4. **Sketch the data flow.** What enters the model's context (and what must never — secrets, raw PII, whole tables); what leaves the system, to where; which credentials exist and which side of the trust boundary each lives on.

5. **Walk the failure modes** and give each an answer in the design: a tool errors mid-task; a replayed step re-fires a side effect (idempotency); the model over-calls an expensive tool (budget/limits); the user asks something out of scope (refusal in instructions); a session runs away on cost (token limits).

Present the result compactly — scenario traces, tool contract table, decision-owner list, data-flow notes, failure answers — and iterate with the user until they would sign off. Each trace later becomes an eval in Phase 6.

## Phase 3 — Map the design to eve features

Now translate the confirmed design into an architecture plan using `references/feature-map.md`: the `agent/` directory tree you intend to build, with one line per file tying it back to the trace or contract that motivated it. Core mapping heuristics:

| Requirement | eve feature |
|---|---|
| Behavior/persona/rules that always apply | `agent/instructions.md` |
| A typed action in code you control (API call, DB query) | `agent/tools/<name>.ts` (`defineTool`) |
| External service with an MCP server or OpenAPI spec | `agent/connections/<name>.ts` — prefer this over hand-rolled tools |
| A long procedure needed only sometimes (runbook, playbook) | `agent/skills/<name>.md` — not instructions, not a tool |
| Users reach it from Slack/Discord/Teams/Telegram/Twilio/GitHub/Linear | `agent/channels/<name>.ts` (built-in channel) |
| Web/HTTP/custom frontend | the default eve HTTP channel + `useEveAgent`; custom surfaces via `defineChannel` |
| Recurring background work | `agent/schedules/<name>.ts` or `.md` (root-only, UTC cron) |
| A specialist with a different prompt or narrower tools | `agent/subagents/<id>/` — only if a skill won't do |
| Parallel fan-out over independent subtasks | the built-in `agent` tool (no authoring needed) |
| Remember things across turns in a session | `defineState` (never for cross-session data — use a DB/connection) |
| Run code, shell, or file work | the built-in sandbox tools; override `agent/sandbox/` only for setup, seeding, backend, or network policy |
| Per-tenant/per-user tools, skills, or instructions | `defineDynamic` |
| Audit logging, metrics, persistence of events | `agent/hooks/<name>.ts` (observe-only) |
| Sensitive/irreversible actions | `approval` on the tool or connection (Phase 5) |

Default choices unless the user objects: nested layout (`agent/` under app root), default model (or `anthropic/claude-sonnet-5` gateway id explicitly), default sandbox backend, start with the fewest files that work. Present the plan and confirm before building.

## Phase 4 — Build incrementally

Build in this order, verifying each step before the next. eve is designed for this: start with two files, grow by adding files.

1. **Scaffold** (skip if Phase 0 found an existing agent): `npx eve@latest init <name>` (new) or `eve init .` (existing project with `package.json` and no `agent/` yet). Requires Node 24+. Stop the interactive TUI; use `eve dev --no-ui` for headless verification. Model credential: `AI_GATEWAY_API_KEY` or `vercel link` for gateway ids; provider key (e.g. `ANTHROPIC_API_KEY`) plus `@ai-sdk/<provider>` for direct models.
2. **Read the bundled docs** at `node_modules/eve/docs/README.md` — follow its reading order for each surface you're about to author.
3. **Instructions + agent.ts**: write `instructions.md` from the Phase 1 spec and Phase 2 decision-owner list — identity, scope, what to refuse, when to ask vs act. Set `model` in `agent.ts`; add `limits` (token budgets) early for anything with cost exposure.
4. **Tools**: one file per action, snake_case filename (that's the model-facing name). Model-facing `description` written for routing; Zod `inputSchema`; JSON-serializable output; use `toModelOutput` to shrink rich outputs. Tools run in the app runtime with `process.env` — never return secrets or raw sensitive data. Interrupted steps re-run: make side effects idempotent or gate them with `approval`.
5. **Connections**: `defineMcpClientConnection` / `defineOpenAPIConnection`. Choose app-scoped auth (`getToken` from env/secret manager) vs user-scoped (`connect()` via Vercel Connect, or `defineInteractiveAuthorization` self-hosted). User-scoped requires route auth that resolves a real user — wire that dependency consciously.
6. **Verify the core loop**: run `eve info` (confirms discovery + diagnostics), then `eve dev --no-ui` and drive a session over HTTP or the TUI. Fix discovery issues before adding surfaces (`eve info` is the first debugging move; artifacts land under `.eve/`).
7. **Then the outer surfaces**, each verified as added: skills → channels → schedules → subagents → hooks/state. Note: `eve dev` never fires cron schedules — test them via dispatch or `eve start`.

Keep each addition small and runnable. Prefer deleting a feature over shipping an unverified one.

## Phase 5 — Security hardening

Do this before any real data or traffic, using `references/security-checklist.md` in full. The non-negotiables:

1. **Route auth**: replace scaffolded `placeholderAuth()` in `agent/channels/eve.ts` with a real `AuthFn` walk (`vercelOidc()`, `httpBasic()`, `oidc()`, `jwtHmac()`, or custom app-session auth). Never ship `localDev()` alone; anonymous access requires an explicit `none()`.
2. **Approvals**: every tool or connection that can pay, message, delete, write externally, or touch regulated data gets `approval` (`always()`, `once()`, or an input-dependent policy, e.g. amount thresholds, tenant checks via `ctx.session.auth`). Omitted approval = `never()` — the default is permissive.
3. **Sandbox egress**: default is `allow-all`. For anything non-toy set `deny-all` or an allow-list in `onSession`/backend factory; use credential brokering for authenticated egress so secrets never enter the sandbox.
4. **Harness audit**: review built-in tools (`bash`, `web_fetch`, `web_search`, file tools, `agent`). `disableTool()` anything the agent shouldn't have; override with wrappers to add guards/logging.
5. **Channel verification**: platform channels need their signing secrets set; custom channels must verify HMAC signatures in constant time and never trust body-supplied identity.
6. **Data minimization**: filter/redact tool outputs; don't pass sensitive data into subagent messages; multi-tenant agents must scope every query and approval policy by `ctx.session.auth` (see `docs/patterns/multi-tenant-*` in the bundled docs).

## Phase 6 — Evals, then ship

No agent is done without evals. Use `references/testing-and-evals.md`. Minimum bar:

1. `evals/evals.config.ts` plus smoke evals: for each core job, `t.send(...)` → `t.succeeded()` + `t.calledTool(...)` + one content check (`t.check(t.reply, includes(...))`).
2. A negative eval: the agent does *not* call tools / take action when it shouldn't.
3. If any tool has `approval`, an eval that exercises the pause/approve/resume flow (`t.requireInputRequest`, `t.respond`).
4. Deterministic runtime tests use `mockModel` on a fixture agent; judge (`t.judge.autoevals.*`) only for fuzzy quality bars.
5. CI runs `eve eval --strict`.

Ship: `eve build` → fix diagnostics → `eve deploy` (Vercel; links project, cron schedules become Vercel Cron) or `eve build && eve start` self-hosted (pick a non-Vercel sandbox backend and your own route auth). Verify the deployment with `eve dev <url>` and confirm an unauthenticated request gets a 401. Add `agent/instrumentation.ts` (OTel) if the user needs observability.

## Style rules for this skill

- Recommend the smallest design that does the job; every file must earn its place. Skills over subagents, connections over hand-rolled API tools, built-ins over overrides.
- Never invent eve APIs from memory — confirm signatures against `node_modules/eve/docs` for the installed version. eve is in beta and moves fast.
- Surface the security trade-offs of each choice as you make it, not as an afterthought at the end.
