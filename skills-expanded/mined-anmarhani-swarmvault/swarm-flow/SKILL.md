---
name: swarm-flow
description: The SDLC router — figures out where a project stands and runs the right phase. Use at the START of any work in a SwarmVault project: continuing/resuming a project, starting a new one, "what's next", or before writing any feature code, spec, design, or ticket. Also use when unsure which phase (requirements, design, implementation, review) comes next. Resume-from-anywhere on any platform.
---

# swarm-flow — the SDLC router

Thin by design: this skill decides *which* phase runs; all expertise lives in the phase
skills. Load the chosen skill before proceeding.

**Read this before working, not after.** In a SwarmVault-registered project this skill is
the entry point for *any* substantive request — including ones that sound like a direct
order ("add login", "fix the schema", "build the dashboard"). Route first, then work: two
tool calls of routing prevent building the wrong thing, code with no ticket, or two agents
editing the same file. If you are about to write feature code and cannot name the ticket it
belongs to, you skipped this step — come back and route.

**Deciding you can skip the flow is itself a flow decision.** For genuinely trivial or
one-off asks (a typo, a question about existing code, a shell one-liner) say so in one
clause and proceed — but say it, so the user can disagree. Never skip silently.

**The resume promise:** routing needs ONLY vault state — flow-state, ticket statuses, the
question queue, memory. "Continue project X" works from a cold session; never ask the
user what happened last time, and never require a previous transcript. A session that
died mid-work still lands correctly: stale claims surface via TTL, half-done phases
surface via their artifacts.

## Route

1. Resolve the project (`swarmvault.py context .`; `doctor` if that fails).
2. Read `30 Plans/<P>/flow-state.md` — but **artifacts on disk win** over stale state;
   correct the note with a logged line if they disagree.
3. Decide by the first matching row:

| Observed state | Phase → skill |
|---|---|
| No SRS, no specs | requirements → **swarm-spec** |
| SRS/specs `draft` or `mined-draft` | validation pass → **swarm-spec** |
| SRS validated; no design doc | design → offer the **lane choice** below (+ **swarm-design-ui** if the SRS declares any user interface) |
| Designs validated; no tickets | ticket planning → **swarm-implement** |
| Open/claimed tickets | work the next unblocked ticket → **swarm-implement** |
| Milestone's tickets all done, no sweep report | milestone gate → **swarm-review** |
| Sweep findings open | fix tickets → **swarm-implement** |
| All milestones done | maintenance: bugs → **swarm-debug**; new asks → **swarm-spec** (change mgmt) |
| Any request whose deliverable is end-user-facing text | **swarm-write** (README, marketing, posts, UI copy, release notes) |
| User wants SwarmVault out of this project | offboarding → **swarm-eject** |

4. Announce phase + evidence in one line ("SRS validated, 3 open tickets in M2 →
   implementing"), then proceed.

## Design lanes (recorded in flow-state as `design-lane: standard|deep`)

Asked once, when the design phase opens; the answer routes the whole phase. If it is already
recorded, don't re-ask — resume that lane.

- **standard** *(default, recommended)* — **swarm-design**. The agent proposes the
  architecture, the user validates it. Right for most projects.
- **deep** — **swarm-design-deep**. Developer-driven: the user commits to each approach before
  anything is written, down to pseudocode, algorithms and test vectors. Slower and more
  expensive on purpose. Offer it when the user says they want to own or fully understand the
  system, asks for pseudocode/algorithm-level planning, or names "developer mode".

They replace each other — never run both. Switching lanes mid-phase keeps closed work.

## Modes (recorded in flow-state as `mode: gated|auto`)

- **gated** — stop at every phase/milestone boundary for the user's stakeholder
  verification before continuing.
- **auto** — chain phases without stopping; the swarm-review sweep is the milestone gate;
  append non-blocking questions to the question queue; stop only when truly blocked
  (credentials, contradictory requirements, destructive/irreversible actions).

The mode is asked once at SRS validation (swarm-spec) and the user may change it anytime.

## Classify the ask before routing a change

Once an SRS is validated, a request is one of six things, and misreading it is how specs
rot. The test: **does any accepted criterion of an existing FR change?**

| the ask | classification | goes to |
|---|---|---|
| already answered by the SRS | **clarification** | answer, change nothing |
| an existing FR's criterion changes | **amendment** | swarm-spec |
| new criterion inside an existing FR's story | **extension** | swarm-spec |
| a new user goal | **new requirement** | swarm-spec (allocate FR-XX) |
| behavior contradicts an accepted criterion | **defect** | swarm-debug — *never* edit the spec to match the bug |
| an FR goes away | **withdrawal** | swarm-spec (`status: withdrawn`, ID never reused) |

The label isn't the deliverable; the **impact set** is — which FRs, ADRs, open tickets, and
tests this touches. State the read in one line before acting ("amendment to FR-11, impacts
ADR-004 and 2 open tickets"). In gated mode, wait for a nod on *new requirement* and
*withdrawal* only. Log it as a `CR-NNN` entry in the requirements tracker either way.

## Rules

- **Scheduled continuation:** if context shows a `⏳ Scheduled continuation` (or
  `plan-continue show` returns one), you were resumed to push a usage-limited project
  forward — just route to the current phase and continue. When all milestones are done (or
  the plan's `--scope` is reached), clear it: `plan-continue clear --project <P>`. See
  swarm-orchestrate for scheduling one.
- **Safe-state compaction:** on a long task, at a resumable boundary you may `checkpoint`
  (record a safe-state note), compact/clear context to save tokens, and continue — the vault is
  your state. Quality first: never compact mid-work if continuity is carrying the task. Details
  in swarm-orchestrate.
- Never silently skip a user-validated gate; user-requested phase jumps are allowed with
  a one-line warning about what's being skipped.
- On phase completion, the finishing skill updates flow-state
  (`phase:`, `mode:`, `description:` compact status); offer — don't force — the next phase
  in gated mode.
- Monorepos: the nearest `.swarmvault` marker wins.

flow-state format:

```markdown
---
name: flow-state
description: "phase: implement — M2, 3/9 tickets open, next TK-014"
project: MyApp
type: plan
phase: implement
mode: auto
---
```

---
*Influences: Pocock's ask-matt (routing stance) — see CREDITS.md.*
