---
name: agent-ops-governance
description: >-
  Operate and govern a fleet of AI agents like managed labor, not shelfware. Use
  when agent ownership is unclear, AI or token costs are climbing, prototypes
  have become sprawl, a vendor renewal is approaching, maintenance needs a
  cadence, or agent tools need pruning. Covers the seven-surface maintenance loop
  (job, diet, memory, tools, reach, proof, value), tool pruning, three-lane cost
  measurement, budget signals, fair licensing, a four-state prototype ladder,
  and one accountable owner per consequential agent. Triggers include agent
  ownership, cost per completed work unit, prototype graveyards, agent meters
  versus seats, and keep/change/pause/retire decisions. For security controls,
  use platform-security-playbook; for ROI math, use platform-roi-scorecard.
---

# Agent Ops Governance

## Purpose

When an agent starts reading real files, drafting real messages, and changing things other people rely on, it stops being a tool and becomes work — and work needs management. Practitioner reports (2026) describe the "haunted house" company: automated systems still moving after their reason disappeared. This skill covers five disciplines: ownership, maintenance, measurement, money, lifecycle. For security and compliance controls, route to `platform-security-playbook`.

## Core model

### Ownership: one name, not a committee

Every consequential agent gets one accountable owner — a person close enough to the output to tell whether the agent is helping, drifting, or producing polished noise. A committee can govern the road; one person still owns the vehicle. Ownerless agents fail silently — stale data diets, rotted instructions, dead review loops. Ownership answers *who*; maintenance answers *what they keep healthy*. The minimal card, kept where humans see it:

- **Owner:** [named person, not a team alias]
- **Purpose:** the agent's job in one sentence
- **Blast radius:** what breaks or misleads if this agent is wrong or vanishes
- **Review cadence:** when the next maintenance pass is due

The owner's job scales with the tier — personal agent, shared team agent, and multi-agent pipeline break differently.

### The seven harness surfaces

Agents break in two directions: the world drifts (policies, products, definitions change while the agent's sources don't), and — less intuitively — the *model improves* and the harness becomes dead weight: strict instructions, extra tools, and double-verification steps built as workarounds for an older model's weaknesses turn into rigidity, wasted context, and latency. The unit of maintenance is the whole harness, not the model or prompt. Walk seven surfaces:

| Surface | Failure mode | Signal | Action |
|---------|--------------|--------|--------|
| **Job** | Scope grows silently (summarizer becomes recommender) | "It's deciding things I didn't ask" | Rewrite the job as one sentence — output, sources, users, review step, consequence. "Draft refund replies with source links" is a job; "handle support" is not |
| **Diet** (what it reads) | Stale or over-broad sources | Answers cite retired policy | Add only what still helps; delete stale material; define which source wins on conflict |
| **Memory** (what it carries) | One-time exceptions harden into standing rules | Old exceptions reappear as defaults | Promote only validated lessons; prune the rest; separate preference from task fact |
| **Tools** | Toolset too broad or ambiguous | Wrong calls, redundant searches | Prune first — see doctrine below |
| **Reach** (permissions) | Reach tracks enthusiasm, not evidence; a permission harmless for a weak model turns risky for a fast one | Rising escalations | Expand after canaries pass; shrink when escalations rise. Draft-only keeps failures local; direct-write makes the same mistake live |
| **Proof** | "It looked good" substitutes for evidence | No inspectable trail | Require diffs/tests, source links and dates, policy sections and timestamps; set the proof standard before the run |
| **Value** | Output nobody uses | Reports pile up unread — plausible waste | Retire it. Retirement is maintenance, not failure |

**The maintenance loop** — triggered by model/tool/source changes, permission requests, repeated corrections, rising review burden, cost jumps, near misses, or scope creep: (1) write the one-sentence job; (2) inspect the **last ten runs** — used? changed? which sources and tools fired? repeated mistakes?; (3) walk the seven surfaces; (4) run a **replay pack of 5–20 known cases** (canaries) after every change; (5) **delete before adding** — "don't do that" rules are how harnesses get heavy; first check whether a stale source, broad tool, vague job, or old memory caused the miss; (6) end with an explicit call: **keep / change / pause / retire**. The worst outcome is no decision.

### Tool-pruning doctrine

Deletion improves agents: a major hosting platform reportedly deleted the large majority of its inbound sales agent's tools and the agent got *better*. The maintenance move on tools is frequently subtraction:

- **Remove** tools the last ten runs never used well; **narrow** broad tools to what the job needs.
- **Rename** and sharpen descriptions so tool choice is unambiguous; test choice on known cases.
- **Split** read / draft / proposed-write / direct-write into separate tools so reach is granted per-variant.
- **Retire workarounds** built for a weaker model — dead weight under a stronger one (a classic tool-path bug was fixed by requiring absolute paths, not a smarter model).
- With dynamic tool protocols the reachable world shifts under you. Research backs selectivity: retrieved memories reproduce past outputs good or bad, so selective add/delete beats naive growth; memory-plus-tools is its own failure surface (trait memories pushing tool-call drift from ~5% to 50%+).

### Token measurement: three fidelity lanes

A token count is a trace of delegated work — not a scoreboard, not just a cost line. The right question: **what work did the spend move?**

Usage data arrives at three fidelities, never to be mixed: (1) **exact** — tools that log real token counts; (2) **measured activity** — run/action counts; (3) **labeled estimate bands** — surfaces with no usage data. Keep lanes separate, lead with what's measured, never fold an estimate into a measured total, print fidelity labels on the chart itself.

Log rows: date, tool/model, project, job, work type, usage figure with lane, outcome, review burden, next move. Distinguish **assistant work** (rewrite, summarize) from **computer work** (a workflow carried across steps with tools, files, verification): computer work legitimately burns more; being stuck on the assistant side is an imagination problem, not a model problem.

**Five chart-reading rules:** (1) high burn + valuable result → make it repeatable (workflow, checklist, skill) so the next run starts smarter; (2) high burn + weak result → redesign the work (vague prompt, stale context, missing tool, job needing a split), don't blame the model; (3) watch absences — a quiet chart during a painful manual workflow means you never thought to delegate; (4) tool-driven spikes are harness stories, not just model stories; (5) repeated corrections get encoded (skill, checklist, test), not remembered.

### Budget burn as signal

Front-loaded burn is information, not just overspend. A large rideshare company reportedly exhausted its annual AI budget months early at ~95% monthly engineer AI usage and ~1,800 agent-produced code changes a week — leadership could see usage and token spend but couldn't connect any of it to better customer features. Free spending and hard caps are both wrong (a cap that kills working experiments costs more than the overage). Read spend against completed work, not last year's seat count — the bill is the first hard evidence that AI crossed from purchased tool to managed labor.

### Licenses, renewals, and the CFO metric

Pricing is splitting into two meters: who logs in (seats) and what work moves through the system (agent meters). **Nine traits of a fair agent license:** visible meter with a sensible unit; forecastable usage; failed work not billed like completed work; a governed path for third-party agents; pricing that distinguishes read/draft/recommend/write/approve/execute; buyer-settable caps; clean usage export; a rate card fixed for the term; alignment with value created. Rent-seeking tells: vague "AI access" charges, the vendor's own agent as the only practical route, paying to use your own data, billable failures.

**Three pre-signature question buckets:** (1) what current seats already cover — agents acting for licensed users, third-party agent paths, autonomous API access; (2) how the meter works — which actions consume, failed vs. completed, per-action-type rates, overage behavior, rate-card stability, caps; (3) **the seat-reduction question vendors dodge hardest** — if the agent resolves support volume, can support seats go down; can light users downgrade tiers?

**The CFO metric:** stop counting licenses; compute **cost per completed unit of work** (per resolved case, qualified lead) against baseline human cost. Three outcomes: cheaper at acceptable quality → scale; cost merely shifted to an unpredictable meter → renegotiate; premium justified by speed/quality → budget honestly as premium, not savings. **Negotiate agent access before usage is mission-critical** — embedded workflows flip the leverage to the vendor.

### The four-state prototype ladder

First versions are now nearly free; the job shifts from rationing build time to classifying software abundance:

1. **Personal tool** — one primary user; scrappy allowed; keep away from sensitive data.
2. **Team beta** — 3+ regular users for 4 weeks; named owner + backup, description, touched systems, failure plan; security review before spread if it touches credentials, customer data, money, compliance, or prod.
3. **Supported internal product** — 10+ users or meaningful outage cost; product ownership, access management, monitoring, docs, support, auditability, change process.
4. **Customer-facing product** — any external user, revenue, or contractual reliance; full product standards plus AI-specific evaluation (model performance, data handling, fallback, user control, policy compliance).

Default-allow at the low-risk end; review notices when an artifact starts creating *obligation*, it doesn't gate building. Run a weekly prototype review: one-page intake; three outcomes per item — leave, promote one step, or harvest the learning and retire; and a **one-line decision log** (owner, backup, next review date, promotion condition, demotion condition) as the anti-politics device.

**Demotion triggers — the neglected direction:** beta → personal when usage falls to one person, the backup disappears, or the problem stops recurring; supported → beta when it loses its owner, drops out of operating rhythm, or stops justifying support cost (post a notice date plus a named alternative or an honest "there is none"); customer-facing → sunset when the external promise stops earning its maintenance cost. The **demotion audit is the pass almost nobody runs** — schedule it.

## Workflow

1. **Inventory agents and owners.** List every agent touching [your team/org]'s real data, messages, or systems. Flag ownerless-but-consequential agents first.
2. **Assign ownership cards.** Owner, purpose, blast radius, review cadence. If nobody will claim it, that is a retirement candidate.
3. **Stand up token measurement.** Usage log with the three fidelity lanes separate and labeled on every chart; never publish a summed total across lanes.
4. **Run the first maintenance pass per agent.** One-sentence job → last-ten-runs inspection → seven surfaces (prune tools first) → 5–20-case replay pack → delete before adding → explicit keep/change/pause/retire call.
5. **Classify prototypes and run the demotion audit.** Place every tool in one of the four states using real usage facts (refuse to guess — pull actual user counts for [each prototype under review]). Log one-line decisions with promotion *and* demotion conditions, then audit everything rated "supported": does it still earn its class?
6. **License and renewal review.** Before any AI-relevant renewal: score against the nine traits, run the three question buckets (including the seat-reduction dodge question), compute cost per completed unit of work per agentic workflow. Negotiate before the workflow is mission-critical.
7. **Set the recurring rhythm.** Weekly: 15-minute token review — top days, quiet days, today; accepted work vs. review burden; assistant work that should have been computer work; which repeated task becomes a workflow; what manual work moves to the machine next. Per cycle: maintenance pass per agent. Quarterly: ladder re-classification + demotion audit + license posture check ahead of renewals.

## Guardrails

- **Never use token volume as surveillance, leaderboard, or panic trigger.** Surveilled numbers get gamed, leaderboards get inflated, cost panic drives usage underground. Don't compare people without context or publish an unscrubbed dashboard (top days leak client names). The team metric that matters: reusable workflows discovered and shared, not tokens burned.
- **Don't sum across fidelity lanes.** One estimate folded into a measured total poisons the series.
- **Delete before adding.** Diagnose the miss (stale source? broad tool? vague job? old memory?) before writing a new rule.
- **Every maintenance pass ends in a decision** — keep, change, pause, or retire. Retirement is maintenance, not failure.
- **Ownership is one name.** A committee or team alias is not an owner. Keep the card minimal rather than inventing fields.
- **Scope boundary.** Security controls belong to `platform-security-playbook`; output verification to `agent-trust-auditor`; model cost routing to `model-selection-router`; benefit quantification to `platform-roi-scorecard`; when maintenance findings trace to the instruction/memory/tool layer itself, hand the redesign to `agent-harness-engineer`.

## Suggested effort

- **Single agent tune-up**: 1–2 hours including last-ten-runs inspection and replay pack.
- **First inventory + ownership cards**: half a day to a day for 5–20 agents; expect 2–3 immediate retirement candidates.
- **Token measurement stand-up**: 2–4 hours; the weekly review is then a strict 15 minutes — timebox it or it becomes a meeting.
- **Ladder classification + demotion audit**: one weekly slot (30–45 min) handles 5–8 items.
- **Renewal review**: 2–3 hours per major vendor, at least a quarter before renewal — afterward the leverage is gone.
- Patterns drawn from practitioner reports (2026) and anonymized incidents; thresholds (3+ users/4 weeks, 10+ users, 5–20 canaries) are defaults to tune, not laws.
