---
name: kelet-integration
description: >
  Integrates Kelet into AI applications end-to-end: instruments agentic flows with OTEL tracing, maps session
  boundaries, adds user feedback signals (VoteFeedback, edit tracking, coded behavioral hooks), generates
  synthetic signal evaluator deeplinks, and verifies the integration. Kelet is an AI agent that performs Root Cause
  Analysis on AI app failures — it ingests traces and signals, clusters failure patterns, and suggests fixes.
  Use when the developer mentions Kelet or asks to integrate, set up, instrument, or add tracing/signals/feedback
  to their AI app. Triggers on: "integrate Kelet", "set up Kelet", "add Kelet", "instrument my agent",
  "connect Kelet", "use Kelet".
license: CC-BY-4.0
metadata:
  author: kelet-ai
  url: https://kelet.ai
  version: "1.5.10"
allowed-tools: Read Write Edit Glob Grep Bash AskUserQuestion ExitPlanMode WebFetch(https://docs-ai.kelet.ai) WebFetch(https://kelet.ai)
---

# Kelet Integration

**Enter plan mode immediately.** First action of the skill: call `EnterPlanMode` so the entire analysis → mapping → signals → plan sequence runs read-only. Only call `ExitPlanMode` after the user approves the final implementation plan at Implementation Approval.

**North star: brilliant developer experience, fastest possible time to value.** The developer should feel like Kelet integrated itself — minimal inputs from them, maximum value immediately visible in the console.

**Kelet silences runtime errors.** Config + transport failures never raise — a misconfigured integration looks identical to a working one. (Invalid caller args, e.g. out-of-range `score`, still raise `ValueError` at dev time.)

**Fetch live docs before writing code:** `GET https://docs-ai.kelet.ai/chat?q=<question>` (preferred) or fetch `https://kelet.ai/docs/llms.txt` for the index.

---

## Onboarding

Open with a welcome banner: `🕵️  Welcome to Kelet — your AI detective`. Kelet is a reasoning agent that ingests traces + signals, clusters failures, suggests fixes. Teach these concepts before any code — keep the detective metaphor alive through the bullets:

- **Trace = the scene.** Every LLM call + tool use auto-recorded after `kelet.configure()`.
- **Signal = the tip.** 👎, edit, abandon — points the detective at something worth investigating. Not a verdict: 👎 means _start looking here_.
- **Synthetic = forensic tools.** Automated signals from trace data. No code.
- **Session = the case file.** Traces grouped by one unit of work.
- **Project = the jurisdiction.** One per agentic use case. Wrong project = invisible in RCA.
- Next: silent analysis + **≤3 `AskUserQuestion` calls (ideally 2)**

---

## Integration Modes

**Lightweight (default):** Fewest possible code changes — ideally just `kelet.configure()`. Add `agentic_session()` only if required (see Sessions), managed synthetics (zero code), and at most 1–2 coded signals only if they're trivially wired to an existing hook. Default to this unless the developer says "expand", "add more signals", or "go deep".

**Full:** all signal layers + VoteFeedback UI + complete failure mode mapping.

When in doubt: lightweight. Every extra code change is a cost to the developer.

---

## Presentation Style

Tone: warm + expert. Concept before mechanics. Open each checkpoint with a banner: `<emoji>  <PHASE>` — one word, uppercase, nothing else. Phases: `MAPPING`, `SIGNALS`, `PLAN`, `IMPLEMENT`, `VERIFY`.

Progress tracker — exactly these labels:

```
📍  Mapping 🔄 → Signals ○ → Plan ○ → Implement ○ → Verify ○
```

Internal work (e.g. `0a`, `0b`, `1`, sub-steps) stays silent. The user sees progress only when a phase flips to ✅.

---

## Key Rules

- **Be concise — never repeat yourself.** Every token costs time. State each fact once, collect data methodically, don't re-explain what was already covered.
- **Always `AskUserQuestion`** for input — never free-form text. Use `multiSelect: true` for lists.
- **At most 3 `AskUserQuestion` calls total (ideally 2).** If you can infer it — don't ask.
- **Pre-flight (outside budget):** If no app description in trigger message, ask: "What does your AI app do and how do users interact with it?" before reading files.
- **Silent analysis first.** Stay in plan mode through Checkpoints 1 and 2; only call `ExitPlanMode` at Implementation Approval.
- **If Kelet already in deps:** skip setup, focus on what was asked. Analysis pass + Verify still apply.
- **Match the app's visual style.** Any UI added (VoteFeedback buttons, copy button, retry, etc.) must use the app's existing CSS classes, design tokens, and component patterns — not arbitrary inline styles or emoji defaults. Read the stylesheet and existing components before writing children.

Question slots:

1. Checkpoint 1 — confirm project/workflow map
2. Checkpoint 2 — confirm plan + collect keys + project name
3. Only if deployment is truly unknown and secrets can't proceed safely

No micro-confirmations between these.

---

## Analysis Pass (Silent)

> 🧠 Read everything before asking anything. Developer should be confirmed, not quizzed.

Read silently — no questions yet. Cover:

1. **Deps** — AI frameworks, UI stack, package manager
2. **Entrypoint** — where `configure()` goes
3. **LLM call sites** — flows, orchestration patterns
4. **Session tracking** — conversation IDs, request IDs, Redis keys, DB columns. Evaluate semantics: does the candidate ID change at reset/new-conversation? If not, surface the mismatch. See [references/implementation.md](references/implementation.md).
5. **Existing feedback UI** — thumbs, ratings, edits, retries, copy buttons. Wire to these; don't replace.
6. **Deployment infra** — scan before asking: `helm/`, `charts/`, `.github/workflows/`, `vercel.json`, `railway.json`, `render.yaml`, `fly.toml`, `docker-compose.yml`, `Procfile`, `*.tf`, `template.yaml`
7. **Multi-env deploys** — any sign the app ships to more than one environment (per-env overlays, values, manifests, config, `.env.*`): flag for Checkpoint 1.

Skip styling, auth, unrelated business logic. Flag other repos/services in the agentic flow — developer should run this skill there too.

**Build the Project Map:**

```
Use case: [what the agents do]
Flows → Kelet projects:
  - flow "X" → project "X"
User-facing: yes/no
Stack: [server] + [LLM framework]
Config: .env / .envrc / k8s
Deployment: [platform | none found]
Mode: lightweight | full
```

**Build an ASCII architecture diagram** showing data flow and where session IDs travel.

---

## Checkpoint 1: Mapping Confirmation

Present diagram + project map + integration mode + brief workflow summary (steps, what success/failure looks like from the agent's perspective).

`AskUserQuestion`: "Does this diagram, map, and workflow summary accurately represent your system? Anything I missed?"

If session semantics are genuinely ambiguous — include it in this question, don't burn a separate slot.

If multi-env deploys were detected, also ask whether to use one Kelet project across envs or one per env — per-env keeps non-prod noise out of prod traces; single-project is simpler.

If corrections change flow count, framework, or session structure — redo the analysis pass. **Don't proceed to signal analysis until confirmed.**

---

## Signal Analysis Pass (Internal Reasoning)

> 🧠 DO NOT SHOW THIS REASONING TO THE USER. Surface final proposals at Checkpoint 2.

Think like an investigator planting clues: *if something goes wrong later, what breadcrumbs would help trace the source?* Don't predict failures — instrument the moments that would reveal them after the fact.

**The one filter:** Can Kelet derive this clue from the session trace? → synthetic (zero code). Requires a human action or external event? → coded signal.

**What diagnostic clue does this signal drop?** If you can't name the question it answers for a developer staring at broken traces, it's noise — drop it. [references/signals.md](references/signals.md) is a prompt, not a menu.

**Synthetic:** Anchor Task Completion, add 1–2 for this app's "good"/"bad". ONE per dimension.

**Coded (0–2 max):** User-facing; server-side only if consumer is a system or feedback is endpoint-driven.

- `kind`: `FEEDBACK` · `EDIT` · `EVENT` · `METRIC` · `ARBITRARY` — `source`: `HUMAN` · `LABEL` · `SYNTHETIC`
- Stack picks *how*, not *what*: React → `@kelet-ai/feedback-ui`; other frontends → TS SDK `signal()`; server → Python/TS SDK.
- Candidates: vote, edit-on-AI-output, copy, retry, abandon, session reset. Copy is usually worth it anywhere AI text renders. Rephrase is not a coded candidate — see below.
- **Rephrase → always LLM synthetic, never coded.** Keyword/prefix matching misses implicit rephrase (reworded, no keyword — where most value lives) and fires on innocent clarifications. Right layer: LLM synthetic scoring the *preceding* turn when the user re-asks or corrects. Don't ship prefix-match as a "temporary" substitute. Abandon and retry may be coded when tied to an explicit trigger (button click, timeout, explicit API) — never inferred from message text.

Prepare for Checkpoint 2: signal proposals + project name suggestion + "what you'll see" preview.

---

## Checkpoint 2: Confirm Plan + Collect Inputs

Present signal findings + **complete lightweight plan**. Don't ask the developer to design it — propose it.

**Still in plan mode — don't `ExitPlanMode` yet.**

Single `AskUserQuestion` (`multiSelect: true`), structured as:

1. **Proposed synthetic evaluators** (multiSelect) — list each proposed evaluator as an option so the developer explicitly picks which ones go into the project. Include "None" as an option.
2. **Plan approval** — "Does the rest of the plan look right?"
3. **Keys + project name** (only what's missing):
   - `KELET_API_KEY` (`sk-kelet-...`) — get at console.kelet.ai/api-keys. **Required for synthetic auto-create.**
   - Publishable key (`pk-kelet-...`) — only if VoteFeedback is in the plan.
   - Project name: **create it first** at console.kelet.ai → top-nav → New Project. Wrong name = silent routing failure; server returns 404 with a hint, surface it.
4. **API key mode** (only if synthetic evaluators were selected):
   - "Paste secret key (sk-kelet-...)" → primary auto-create.
   - "I'll grab one" → halt: "Get a key at console.kelet.ai/api-keys (10 seconds), paste it here to continue."
   - "I can't paste secrets here" → deeplink fallback.

### Creating the evaluators

**Primary (key pasted):** before the curl, print verbatim:

> ⏳ Creating your evaluators. This takes **1–3 minutes** (sometimes up to 5) — Kelet generates each config with an LLM and runs a dedup pass. Sit tight; don't cancel.

Then run per [references/signals.md § Primary: API call](references/signals.md).

On 200: `✅ Created N evaluators in {project}: {name1}, {name2}, {name3}. First results in ~3min at https://console.kelet.ai/{project}/signals`

**Fallback (can't paste):** build the base64 markdown link per [references/signals.md](references/signals.md).

### What you'll see

Show the table — **only rows for items in the proposed plan:**

| After implementing                | Visible in Kelet console                             |
| --------------------------------- | ---------------------------------------------------- |
| `kelet.configure()`               | LLM spans in Traces: model, tokens, latency, errors  |
| `agentic_session()`               | Sessions view: full conversation grouped for RCA     |
| VoteFeedback                      | Signals: 👍/👎 correlated to exact trace             |
| Edit signals (`useFeedbackState`) | Signals: what users corrected — reveals model errors |
| Platform synthetics               | Signals: automated quality scores                    |

Only write `source=SYNTHETIC` code if developer explicitly asks AND platform can't implement it — explain why the platform can't handle it and ask them to confirm before proceeding.

---

## Implementation Approval

**Exception:** if deployment was flagged unknown AND secrets can't be safely handled, use question slot 3: "How do you deploy? How are secrets managed?" → follow [references/deployment.md](references/deployment.md). Skip if deployment was identified or irrelevant.

Present the full implementation plan, call `ExitPlanMode` for approval, then implement.

---

## API Keys

Two types — never mix:

- **Secret** (`KELET_API_KEY`, `sk-kelet-...`): server-only. **The SDK accepts either key type without erroring** — using the wrong one is a silent failure.
- **Publishable** (`VITE_KELET_PUBLISHABLE_KEY` / `NEXT_PUBLIC_KELET_PUBLISHABLE_KEY`, `pk-kelet-...`): frontend only.

Write to config: `.env` → `KEY=value` · `.envrc` → `export KEY=value` · K8s → secrets manifest. Add to `.gitignore`. Never hardcode project name — always env var. When the app has both a server and a frontend, write keys to both env files — secret key to server `.env`, publishable key to `frontend/.env` (or wherever Vite/Next picks it up). Follow [references/deployment.md](references/deployment.md) for production.

**Gating `configure()`.** Gate on the API key only — never AND on project:

```python
if settings.kelet_api_key:
    kelet.configure(api_key=settings.kelet_api_key, project=settings.kelet_project)
```

AND-gating turns a blank-project drift into silent no-traces. Empty project with a valid key surfaces as a routing error in the console — that's what you want.

---

## Sessions

A session = one unit of work. New context = new session.

**`agentic_session()` NOT required** (auto-instrumented):
LangChain/LangGraph · LlamaIndex · CrewAI · Haystack · Google ADK (`kelet[google-adk]` recommended) · pydantic-ai · DSPy · Langfuse · Langroid · anything using OpenInference/OpenLLMetry

⚠️ **Override — read the REQUIRED block below first.** The list above assumes the framework also owns the session ID (short-lived in-process runs). If the app generates the session ID itself (Redis, DB, server-issued UUID) or you orchestrate multiple LLM calls across requests, `agentic_session(session_id=...)` is REQUIRED *regardless of framework* — the framework doesn't know your ID and spans become unlinked. When in doubt, wrap.

⚠️ **Bare LiteLLM** — traces are auto-captured, but LiteLLM does **not** propagate session/agent context into its spans. If LiteLLM is called directly (not through another supported framework like Google ADK), wrap calls in `agentic_session()` (and optionally `kelet.agent()`) to group them. When LiteLLM runs under another instrumented framework, the parent span provides context — no wrapping needed.

If unlisted — research before omitting.

**`agentic_session(session_id=...)` REQUIRED** (both silent if omitted):

- **App owns the session ID** (Redis, DB, server-generated): framework doesn't know it → VoteFeedback linkage breaks
- **You own the loop** (agent A → agent B, Temporal, custom orchestrators): no framework sets the overall session ID → spans appear as unlinked traces. TS: `agenticSession({ sessionId }, callback)`.

⚠️ **Vercel AI SDK** — supported framework but doesn't set session IDs: use `agenticSession()` at route level.

**User identity ≠ session ID.** Stable identifiers (phone, email, user_id) outlive sessions. If the app has a stable user identity: generate UUID per conversation as `kelet_session_id`, regenerate on reset. Silently assess the identifier: non-PII (internal user ID, opaque UUID) → wire as `user_id=` without asking. Obvious PII (phone, email) → omit, but **call it out prominently**: "⚠️ `user_id=` was not set — your user identifier is PII (phone/email). If you have a non-PII user ID, pass it here to enable per-user RCA." Genuinely ambiguous → fold into Checkpoint 1, don't burn a separate slot.

See [references/api.md](references/api.md) for signatures. See [references/stack-notes.md](references/stack-notes.md) for per-stack gotchas.

---

## Implementation Reference

See [references/implementation.md](references/implementation.md) for the decision tree and steps.

**Python:**

```python
kelet.configure(api_key=..., project=...)  # at startup
async with kelet.agentic_session(session_id=session_id):
    result = await agent.run(...)
kelet.shutdown()  # at teardown — flushes buffered spans, else silent drop on pod rotation
```

**TypeScript** — `agenticSession` is **callback-based**, not a context manager (critical difference):

```ts
await agenticSession({ sessionId }, async () => {
    return await chain.invoke(...);
});
```

**TS:** Call `configure({ project })` explicitly if not using env vars, or set `KELET_API_KEY` + `KELET_PROJECT` and it auto-resolves on first signal. **Python:** `kelet.configure()` reads env vars eagerly at call time. With `pydantic-settings` (loads `.env` into a Settings object, not `os.environ`), pass `api_key=` and `project=` explicitly — bare call raises `ValueError`.

**Next.js:** `KeletExporter` in `instrumentation.ts` via `@vercel/otel`. Two silent-if-omitted configs — see stack-notes.md.
**React:** `KeletProvider` at root. `VoteFeedback` / `useFeedbackState` / `useKeletSignal` for feedback.

---

## Verification

> 🕵️ Kelet silences errors — build passing is not evidence. Only the console confirms it.

- Every agentic entry point covered by `agentic_session()` or supported framework
- Session ID consistent end-to-end: client → server → `agentic_session()` → response header → VoteFeedback
- `configure()` called once at startup, not per-request
- `kelet.shutdown()` called at teardown (FastAPI `lifespan` `finally:` / Django SIGTERM / Celery `worker_shutdown`) — else BatchSpanProcessor drops buffered spans
- Secret key server-only — never in frontend bundle
- Check [references/common-mistakes.md](references/common-mistakes.md) for silent failure modes on detected stack
- Smoke test: trigger LLM call → open Kelet console → verify sessions appear (allow a few minutes)
- If VoteFeedback added: screenshot the feedback bar. Confirm `document.querySelectorAll('button button').length === 0`
- After ANY frontend change: screenshot existing pages — tsconfig overrides can silently break unrelated pages
