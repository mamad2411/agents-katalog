---
name: maplab-durable-job-orchestrator
description: Automatically turn MAPLAB goals that require sustained work, several rounds, multiple tools or agents, background waiting, A8 media production, or Hermes training into durable jobs that resume until an Owner-viewable result or a genuine decision gate. Use when the user says continue, keep running, do several rounds, finish the whole workflow, deliver the result, generate and upload, or otherwise should not have to choose a tool or repeatedly prompt the agent.
---

# MAPLAB durable job orchestrator

The Owner states the outcome; the agent chooses DeerFlow, Codex/Hermes continuation, and domain workers. Never require the Owner to remember `/research-*`, a model name, or a worker name.

## Route automatically

Create or continue a durable job when one or more apply:

- the user asks to keep going, run several rounds, finish end to end, or return only when a result is ready;
- the work spans research plus generation, QA, upload, browser work, or more than one role;
- a provider job or render may outlive the current turn;
- progress has stopped before the stated acceptance condition;
- A8 is asked to generate music/video or upload a reviewable YouTube draft;
- Hermes is asked to train, evaluate, or repair LINE replies over several rounds.

A small one-turn lookup or edit stays synchronous. An explicit `/research-public` remains a diagnostic override, not the normal user experience.

## Build the control loop

1. Read `AGENT_CORE.md` when present, `CURRENT_STATUS.md`, `pitfalls.md`, and the active Task Card.
2. Create or load the durable job under `workbook/reviews/MAPLAB-DURABLE-JOBS/`. Follow [references/job-contract.md](references/job-contract.md).
3. Record the user's outcome, acceptance evidence, authorization already granted, budgets, domain owner, next bounded action, and Resume Prompt.
4. Choose execution surfaces without exposing that choice to the Owner:
   - DeerFlow: public/synthetic research, decomposition, comparison, and next-action reasoning.
   - Domain worker: private assets, customer data, LINE corpus, A8 rendering, platform adapters, and fixed local scripts.
   - Codex thread heartbeat: wake and continue cross-tool, authenticated-browser, or repo work that a one-shot process cannot finish.
5. After every bounded action, verify an artifact or live surface, update the job receipt, and either continue automatically or enter a named gate.
6. Finish only when the Owner can inspect the promised artifact/link and the receipt proves it. A plan, worker chat, process exit, or API 200 alone is not completion.

## Break objective-level plateaus

Method novelty is not outcome progress. Before every bounded action, compare the
last three receipts against the job's Owner-facing acceptance and primary
objective metrics, not only method fingerprints or test counts. Read
[references/objective-plateau-sop.md](references/objective-plateau-sop.md) when
two consecutive actions changed code, infrastructure, prompts, or synthetic
proof without advancing an Owner-facing acceptance item.

- Record `objective_metrics_before`, `objective_metrics_after`,
  `owner_acceptance_delta`, `unlocked_next_action`, and `attempt_consumed`.
- Two consecutive zero objective deltas trigger the first-principles five
  questions before any further execution, even when fingerprints differ.
- Do not spend a domain attempt on the review/re-route itself. State
  `attempt_consumed=false` and preserve the prior attempt count. This exemption
  may be used once for the detected plateau; the next executed domain
  experiment consumes one attempt. A pure poll/readback of an already-running
  external action does not.
- Defer or split infrastructure/security work that is not a current blocker.
  A synthetic gate may continue only when the receipt names the exact
  immediately executable Owner-facing action it unlocks, proves every other
  prerequisite is satisfied, and gives a fixed stop condition. A split
  supporting job gets an explicit lower priority and attempt/spend cap and may
  not displace the main job unless an urgent verified safety issue or the Owner
  changes priority.
- After the circuit breaker, the next action must be the smallest falsifiable
  experiment against the real objective, not a broader version of the same
  supporting system.

## Use authorization already present

Do not ask again for an action the Owner explicitly included in the goal. Examples:

- “生歌＋影片” authorizes the necessary bounded generation calls for that job.
- “上傳到 YouTube 給我看” authorizes a private/unlisted draft upload and readback; it does not authorize public publication unless the Owner also says publish/public.
- “持續多跑幾輪 LINE 訓練” authorizes offline evaluation rounds and lesson updates; it never authorizes sending to customers.

Ask only when a new action would add spend, disclose private material to a new third party, make content public, delete/overwrite material, or require a creative/business choice that materially changes the result. Before reporting a blocker, run the three-layer blocker review and include attempts, why they failed, and the smallest Owner action.

## Keep private payloads out of DeerFlow/OpenRouter

DeerFlow may see public prompts or a sanitized job descriptor such as role, phase, pass/fail, missing evidence, and next-action candidates. It must not receive raw LINE conversations, customer data, quotes, orders, private media, browser state, credentials, private repo content, or investment data.

For a private workflow, the local domain worker performs the action and writes a minimal status packet. DeerFlow reasons over that packet only. Treat the current LINE corpus as private even though sender names were replaced: dates, addresses, budgets, quotes, and conversation semantics remain identifying. Local Ollama may be used when the workflow genuinely needs model reasoning over private content and the domain SOP permits it.

## Domain routes

- A8: read `skills/a8-produce-to-publish-sop.md` and the active A8 Task Card. Continue research, generation, render, full playback QA, packaging, and any already-authorized private/unlisted upload until an Owner-viewable link/artifact exists. Do not treat an intermediate review renderer as final.
- Hermes LINE: read `docs/hermes-line-reply-training-plan.md` and `handoff/tasks/T-A6-HERMES-LINE-GYM-001.md`. Run bounded repair rounds, update `loop_state.json` and `current_lessons.md`, and continue toward the seven-run threshold. Never connect the training loop to customer sending.
- SEO patrol: read `handoff/tasks/T-A2-HERMES-SEO-COACH-001.md` and `.agents/skills/maplab-seo-coach-patrol/SKILL.md`. A deterministic public sensor decides material delta first; Hermes queues at most one proposal-only A2/Codex domain action. WordPress/Ads/Rank Math writes, customer messages, and private-data egress remain disabled.
- Public research: invoke the hardened DeerFlow adapter automatically when deep or multi-source public research materially helps. Preserve sources and a receipt; no slash command is required.

## Completion and wake-up rules

- `RUNNING`: another safe bounded action exists; continue without asking.
- `WAITING_EXTERNAL`: a provider/render is running; record poll time and let the heartbeat resume.
- `OWNER_REVIEW`: a concrete artifact/link is ready and a real human choice is required.
- `BLOCKED`: only after the same blocker survives the three-layer review; include the five-minute Owner action.
- `COMPLETED`: acceptance evidence and Owner-facing readback both exist.

Never convert “the current turn ended” into a job state. The file-backed job and heartbeat survive the session.
