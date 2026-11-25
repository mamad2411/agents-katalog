---
name: agent-harness-engineer
description: Audit, redesign, and maintain the harness around an AI agent — the instruction, memory, tool, and check layer that shapes every run. Use when the user says "my agent keeps forgetting", "my instructions file is a mess", "audit my CLAUDE.md / AGENTS.md", "the agent ignores my rules", "context keeps getting re-derived every run", "set up my agent's operating files", or asks about agent memory, agent handoffs, SOUL.md, skill libraries, instruction bloat, harness design, or migrating agent context between tools. Covers mapping every instruction file, evidence-labeling rules, the six-outcome triage (keep / one-home / load-later / turn-into-check / probation / retire), the four-part core brief, knowledge-layer design with retrieval contracts, handoff records and receipts for multi-agent loops, SOUL.md elicitation interviews, 3x3 compact-vs-full experiments, and context portability audits. Trigger on any complaint that an agent's behavior drifted after a model upgrade or that nobody knows which rule wins.
---

# Agent Harness Engineer

## Purpose

Help the user see, triage, and rebuild the harness around their agent: everything configurable that shapes an answer before the next prompt — custom instructions, AGENTS.md/CLAUDE.md and project files, skills and their descriptions, reference docs, memory and retrieved context, tool schemas, permissions and approval rules, hooks/validators/tests/output formats, model and reasoning settings, carried-forward conversation state. It excludes hidden vendor-side state no user can inspect.

Most harnesses are built accidentally, one correction at a time — each rule fixed a real failure, but nobody can see the accumulated system. Practitioner reports (2026) describe audits finding 66 skills, 172 instruction files, one route loading ~18,400 words before reaching the guide it needed, and one authorship rule duplicated across 15 skills, each copy free to drift. The drag hits at four moments: **finding** the right procedure, **deciding** which rule wins, **finishing** the exact job (binary requirements buried in prose get missed), **maintaining** after model upgrades (every duplicate is another file a human must understand). This skill turns that accumulation into an engineered system: mapped, evidence-labeled, triaged, tested, portable, maintained on a cadence.

## Core model

### The six maintenance rules

1. **Make the map before adding anything.** When a new model lands, ask what the engine inherits, not what to add.
2. **Test compact vs. full instruction sets** (the 3x3 method below) instead of assuming more guidance helps.
3. **One canonical home per rule.** Duplicated ownership means drift; other files invoke the canonical source, never restate it.
4. **Load specialist material at the phase that needs it** — source guides during evidence-gathering, packaging examples during packaging, cadence checks once a draft exists. Not everything at startup.
5. **Judgment in prose, guarantees in machinery.** "Use my point of view" is instruction; "valid JSON under [word limit] words" belongs in a parser and a counter.
6. **Every change is approved, receipted, and reversible.** Read-only first pass; numbered proposals; a plain-language record of what moved, plus rollback.

### The six-outcome decision taxonomy

Every material control gets exactly one verdict:

| Verdict | When |
|---|---|
| **Keep it** | Carries necessary context, product truth, source priority, voice, authority, acceptance criteria, or a proven correction — in the right place. |
| **Give it one home** | Several files own the same rule; designate a canonical owner, others reference it. |
| **Load it later** | Valuable only for a specific task or phase; move behind triggers. |
| **Turn it into a check** | A yes/no guarantee a schema, permission, hook, validator, or test enforces more reliably than prose. |
| **Put it on probation** | May help or hurt; evidence doesn't yet justify a change. Log, retest next cadence. |
| **Retire it safely** | Stale workaround, obsolete process, contradiction, ownerless residue, or a fix for a failure that no longer exists. Only after explicit approval; stays recoverable. |

"Delete it because it's long" is not a verdict — the goal is less negotiation, not less protection.

### The four-part core brief

The compact execution core every job gets:

- **Outcome** — what must be true when the work is finished.
- **Context** — facts, sources, and current state the model cannot safely infer (private facts, which source wins, product requirements).
- **Authority** — what the model may do, what needs approval, what it must never do.
- **Acceptance** — files, checks, evidence, format, and the finish line that proves completion.

This is not an outcome-only prompt: shortening that also drops data, approach, and output expectations produces worse work. Missing information is still missing information.

### Evidence labels

Every audit finding and runtime claim carries explicit epistemic status: **VERIFIED**, **USER_REPORTED**, **INFERRED**, **INACCESSIBLE**, **NOT_APPLICABLE**, **NOT_EXPOSED** (runtime traces the surface doesn't provide). Keep two maps: a **system map** (what is configured to shape work) and an optional **run map** (what provably shaped one specific job). Never convert a configuration file into a runtime fact; name coverage gaps instead of calling unknown settings "clean."

### The 3x3 experiment method

To test whether harness weight helps or hurts a route: run the same job as a compact brief (~750 words: outcome, verified facts, authority boundary, delivery contract) vs. the full method (thousands of words of classifications, checks, scoring plans). Three fresh runs each. Score content **blind**; check the binary delivery contract **separately**. In practitioner reports (2026), the full method scored higher on analysis (19.67/20 vs. 17.5) but passed its binary delivery contract once in three; the compact brief passed 3/3. Lesson: **long context can improve thinking while degrading delivery when enforcement stays prose.** Separate specialist method from exact enforcement; treat selective loading as a recommendation to verify per-setup, not a law.

### The knowledge layer

Production agents fail on **assembly, not retrieval**: the system can't prepare what the agent needs before it acts, so it improvises confidently. The signature anti-pattern is the agent re-deriving the same context every run — retrieval calls before useful work, re-opened sources, token budget burned on raw context, rediscovery across runs. Vector search is one component inside a larger layer: retrieval, document structure, semantic data models, access control, provenance, memory, write-back.

**Seven questions a production knowledge layer must answer:**

1. What is the **work object**? (customer, contract, metric, diff — not an abstract query)
2. What's the right **retrieval unit**? (chunk / section / table / record / graph neighborhood / compiled brief)
3. Which source is **authoritative**? (relevant ≠ controlling)
4. What **permissions** apply — before the model sees content, not cleaned up after?
5. What **provenance** must be preserved?
6. What context should be **precompiled** for repeated workflows?
7. What does the agent **write back** — labeled (observed / inferred / user-confirmed / stale / rejected / authoritative) so guesses never silently become instruction?

Three artifacts operationalize it: a **Retrieval Contract Spec** (the exact bundle the agent must receive — e.g., a refund agent needs plan, region, version, purchase history, policy, threshold, prior exceptions, ticket, approved language, authority level — defined before choosing technology), a **Retrieval Failure Triage** (diagnose breakage from logs via the anti-pattern signals above, plus weak-source citations), a **Retrieval Stack ADR** (change, tradeoffs, rollback). Risks: compiled context goes stale, memory accumulates bad conclusions, overbuilding.

### Handoff records and receipts

Where multiple agents or loops exist, the failure point isn't "can the agent do it" but "can the work survive the trip to the next tool" — otherwise the human is the integration layer. The primitive: a shared task list plus a **seven-part task record** — requester/owner, desired outcome, sources (what not to invent), acceptance criteria, boundaries (ask-first list), blocker rule (one specific question on the same task, never a second task), receipts.

**Receipt vocabulary:** `AGENT CLAIMED` (ownership lock, prevents double work), `AGENT BLOCKED` (paused on a task-level question), `AGENT HUMAN HOLD` (needs owner approval), `AGENT RESUMED` (a paused task, not a dead one), `AGENT DONE` (what changed, where the output is, what was checked, what still needs review), `AGENT FAILED` (last safe step — a retry, not a mess).

**Nine-question loop audit — the pre-build gate.** Before building any recurring loop, answer: what starts it, what sources it reads, the exact outcome, what it never does without asking, what counts as finished vs. reviewable, the stuck-question, where output lands, who continues the work. Any unanswerable row means don't build yet. Rules of thumb: one task per run; smoke-test with a tiny issue; draft-before-send first, never irreversible actions; ending in Agent Review is success. Common failures are boring — wrong assignee/label/status, no working-state lock, BLOCKED treated as terminal.

### SOUL.md elicitation

The bottleneck for personal agents isn't installation — experts can't describe their own work at agent resolution; expertise compiles tacit. So the first agent worth running is an **interviewer**. A ~45-minute elicitation walks five layers in order: (1) **operating rhythms** — what days/weeks/months actually look like, not the calendar version; (2) **recurring decisions** — judgment calls and their inputs; (3) **dependencies** — who you need things from, and when; (4) **institutional knowledge** — what you know that nobody else does; (5) **friction** — recurring annoyances that eat time. **Checkpoint approval after each layer**: nothing saved without confirmation, confirmed facts distinguished from synthesized patterns, resumable mid-interview.

Artifacts: `operating-model.json`, `USER.md` (human profile), `SOUL.md` (agent role, tone, boundaries — when to escalate vs. act, tone per audience, authoritative vs. advisory sources, what "good enough" means per task type), `HEARTBEAT.md` (recurring check cadence), `schedule-recommendations.json`. Treat these as an evolving, version-controlled codebase; multiple narrow agents with clear jurisdictions beat one do-everything bot.

### Context portability

AI working intelligence is professional capital that accrues on platforms the user doesn't own — four compounding layers (domain encoding, workflow calibration, behavioral relationship [deepest, least portable], demonstrated capability), lost at four boundaries (platform switch, enterprise wall — root cause of shadow AI, job change, hiring market). Doctrine: start with a **structured extraction** — ask the AI that knows the user to articulate its model of them into a 30-minute Markdown file; stronger is a personal context server on user-controlled infrastructure speaking MCP; the enterprise pattern is **two filing cabinets** — worker-owned identity store plus employer-owned context store, so the "how I think" / "what I worked on" line lives in architecture, not good intentions.

For skill libraries: a prompt says what you want now, memory says what to remember, a **skill** says how this kind of work should happen again. Copying a SKILL.md between tools fails — loading behavior, triggers, scripts, hooks, MCP configs, and permissions differ. The portable unit is a **work package**: skill file plus install location, trigger behavior, required tools/permissions, dependencies, memory read/write scope, scoping (personal/project/team), sync strategy, evidence of work, tested harnesses — one markdown source generating tool-specific copies. Restraint is the quality bar: session-to-skill extraction should usually conclude "nothing recurring happened." The one-question test: **"If I had to move this skill tomorrow, what would break?" — the answer is the roadmap.**

### Team learning capture

One person's best session vanishing on tab-close is the org-level version of harness loss. Make four things visible: the task, the context loaded, the correction pattern, the review standard — prompt libraries capture the instruction and miss the judgment. Mechanics: declared non-sensitive channels (boundary drawn by workflow, not enthusiasm), senior people posting real work first, metrics of reuse ("the same mistake happening less often"), never token volume.

### Company-rules elicitation (skeleton method)

Organizations run on unwritten rules that past scarcity wrote; agents can only follow written ones. When translating org rules into a harness, separate **four objects** usually blurred together — a value, a rule, a runtime check, a human appeal (different work, different owners). Per resented rule, run the **five-question worksheet**: name the exact behavior; find the scarcity that created it; decide whether it still exists; write a version a person could report as broken; decide who can overrule it. Then place it on the **five-rung enforcement ladder** — value → instruction → reminder → hard block → human-owned decision — evidence required to climb each rung. Prohibitions collapse without replacements. (Method only; derive actual rules from the user's org, not this skill.)

## Workflow

Work through the stages in order; skip any that don't apply, and say so.

1. **Map the current harness.** Inventory every instruction file (CLAUDE.md, AGENTS.md, system prompts, project files), skill, memory store, tool schema, permission, hook/validator, and model setting for [the agent or route being audited]. Read-only. Output a system map: what loads on a typical run, in what order, at what token cost.
2. **Evidence-label every rule** with the six labels above. Name coverage gaps explicitly.
3. **Run the six-outcome triage.** One verdict per material control, as numbered proposals; nothing moves without approval, everything retired stays recoverable.
4. **Rewrite core briefs to the four-part form.** Outcome / Context / Authority / Acceptance per recurring job; move binary requirements out of prose into checks (rule 5).
5. **Design the knowledge layer.** Answer the seven questions for the top recurring workflow; draft a Retrieval Contract Spec before choosing technology. If production logs exist, run the failure triage; record changes in a stack ADR.
6. **Wire handoffs** where multiple agents or loops exist: the seven-part task record and receipt vocabulary, with the nine-question loop audit as the gate before any new loop is built.
7. **Run 3x3 experiments on contested changes** — anywhere triage produced disagreement or probation: three fresh runs per condition, blind content scoring, separate binary delivery check.
8. **Portability audit.** Apply the one-question test to each skill; propose the structured extraction file and, for teams, the two-filing-cabinets split.
9. **Set the maintenance cadence.** Re-run the map-first review at every model upgrade and on a fixed interval (e.g., [monthly]); log probation items for retest. Hand ongoing operation to `agent-ops-governance`.

Greenfield (no harness yet): run stage 4 for the most painful recurring job, add SOUL.md elicitation for a personal agent, then build outward — one loop, draft-before-send, never irreversible actions first.

## Guardrails

- **Read-only first, always.** No moves, deletions, or rewrites in the mapping pass. Every change thereafter is a numbered proposal with receipt and rollback path.
- **Never present configuration as runtime fact.** A rule existing in a file is not evidence it shaped a run. Keep system map and run map separate; use NOT_EXPOSED rather than guessing.
- **Never delete for length.** Retirement requires a taxonomy reason plus explicit approval and recoverability.
- **Judgment stays prose, guarantees become checks.** Voice, priorities, point of view remain instruction; format, limits, permissions, file existence become machinery.
- **Checkpoint approvals in elicitation.** Save nothing without confirmation; distinguish confirmed facts from synthesized patterns.
- **Write-back must be labeled** — model guesses must never silently become instruction.
- **Don't overbuild.** Low-risk assistants don't need the full knowledge layer; most sessions don't deserve a new skill.
- **Attribute honestly.** Benchmarks and counts above are practitioner reports (2026), not laws — verify with the 3x3 method before treating them as binding.
- **Cross-references:** hand the ongoing maintenance loop and token-cost accounting to `agent-ops-governance` (same pack); the checks this harness feeds are audited by `agent-trust-auditor`; treat model fit as a harness input via `model-selection-router` — a harness tuned for one model is inherited, not validated, by the next.

## Suggested effort

- **Quick triage** (one instruction file, "is my CLAUDE.md bloated?"): single session — map, label, six-outcome pass, numbered proposals. Skip experiments unless a verdict is contested.
- **Full harness audit** (multi-file, multi-skill): 2–4 sessions — stages 1–4 first, knowledge layer and handoffs next, experiments and portability last.
- **Greenfield personal agent:** one ~45-minute elicitation producing the SOUL.md artifact set, then one session wiring the first loop through the nine-question audit.
- **Team/production system:** treat as infrastructure — retrieval contracts, handoff records, ADRs before capability work; named owners for each weak control before shipping.
- Default to the smaller scope when unsure; shipping one canonical rule home and three prose-to-check conversions beats an unfinished grand redesign.
