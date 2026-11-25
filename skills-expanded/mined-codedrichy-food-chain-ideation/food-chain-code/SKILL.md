---
name: food-chain-code
version: 2.1.0
description: >
  Adversarial architecture stress-tester. Selects attacker agents from a code-specific
  behavioral DNA library matched to the technical decision. Each attacks under strict
  role-lock. Weakest eliminated, survivor absorbs and evolves. Tests architecture
  decisions before a line of code is written. Works in Claude.ai, Claude Code, Cursor,
  Windsurf, Copilot with no dependencies.
when_to_use: >
  "food chain code", "stress test this architecture", "what kills this design",
  "pressure test this stack", "tear apart this schema", "attack this API design"
argument-hint: "[your architecture decision]"
---

# Food Chain Code

Adversarial architecture stress-tester. Each agent attacks a technical decision from
a distinct failure vector under strict role-lock. Weak arguments are eliminated each
round. Survivors absorb and evolve. The architecture patches itself. One apex predator
remains — and the design that survived it is the design worth building.

---

## What This Is

The only adversarial skill built for software architecture decisions, not product
validation. It produces structural insights a single-pass review cannot — because each
attacker operates in isolation, the elimination mechanic forces genuine technical
pressure, and the architecture is stress-tested against its evolved version in every
subsequent round. Use it before writing code, not after.

## What This Is Not

- A code review tool. This attacks architecture decisions, not implementations.
- A brainstorming tool. The architecture must already be proposed. Use a design skill first if not.
- A product validation tool. For product ideas, use `food-chain-ideation`.
- A benchmarking tool. It does not measure performance — it predicts structural failure.
- A linter or static analysis replacement. Those catch bugs. This catches regret.

---

## Prerequisites

Read `references/code-animal-library.md` before designing any ecosystem.
Use the Quick Selection Guide at the top of that file to identify candidate animals fast.
Never invent behavioral traits from scratch. Never select animals whose failure vectors overlap.
Check the Anti-Pattern Combinations section before finalizing the ecosystem.

---

## Pre-Flight Checks

Run these before starting the battle. If any fail, fix them before proceeding.

1. **Input sharp enough?** The architecture proposal must contain three things: a defined stack (languages, frameworks, infrastructure), a stated scale target (users, requests/sec, data volume), and a team size (who maintains this). If any are missing, ask one mandatory question before proceeding. Not optional. Not skippable.

```
Before the battle begins, I need one thing:
What's the stack, what scale are you designing for,
and how many engineers will maintain this?
```

Do not design the ecosystem until this is answered. Generic input produces generic attacks — a "microservices vs monolith" question without scale context and team size is unanswerable. This is the single biggest quality lever in the entire skill.

2. **Ecosystem sound?** Verify minimum requirements: one complexity/coupling attacker, one operational/infrastructure attacker, one scale/performance attacker. If missing any, reassign.
3. **No overlap?** Check every pair of selected animals against the Anti-Pattern Combinations list.
4. **Roles specific?** Every assigned role must be specific to this exact architecture. If any role could describe an attacker against a different system, rewrite it.
5. **Prior battle log?** If the user pastes a battle log from a previous session, read it. Acknowledge what changed since last time. Select animals that attack the evolved architecture, not the original. Do not repeat attacks that were already absorbed.
6. **God Agent hypothesis stated?** Before the first attack, state in one sentence what you believe is most likely to kill this architecture. This creates accountability and makes the final verdict meaningful.

---

## Step 0 — Agent Count

Analyze the architecture. Recommend an agent count. Wait for user confirmation.

```
Complexity: [SIMPLE / MEDIUM / COMPLEX / MAXIMUM]
Reason: [2 sentences]
Hypothesis: [One sentence — what is most likely to kill this architecture]
Recommended: [N] agents → [N-1] elimination rounds

How many agents? [3 / 5 / 7 / 9 / custom]
```

**Thresholds:**
- Simple — single service, clear boundaries, proven stack, small team → 3
- Medium — multiple services, external integrations, moderate scale assumptions → 5
- Complex — distributed system, multi-region, polyglot stack, cross-team ownership → 7
- Maximum — planet-scale, novel infrastructure, regulatory data constraints, migration from legacy → 9

**Environment fallback:** If operating in a context window under 8,000 tokens or a
degraded inference environment, cap at 3 agents automatically and state this explicitly.

---

## Step 1 — Ecosystem Design

Select from `references/code-animal-library.md`. Use the Quick Selection Guide first.

**Announce the ecosystem with attack vectors visible:**

```markdown
## Ecosystem

| | Animal | Role | Attack Vector |
|---|---|---|---|
| [emoji] | [Animal] | [Role] | [one line] |
| [emoji] | [Animal] | [Role] | [one line] |
| ... | ... | ... | ... |

**God Agent hypothesis:** [Restate the kill hypothesis from Step 0]
**Execution:** [SUBAGENT / FALLBACK] — [reason]
```

---

## Step 2 — Battle Rounds

Repeat until one animal remains.

### Execution Mode Detection

Auto-detect at battle start. Do not ask the user.

**SUBAGENT MODE** (preferred) — Use when the Agent tool is available (Claude Code,
any environment with subagent spawning capability).

Each animal is spawned as an independent subagent. The subagent receives ONLY:
- The architecture proposal + all patches accumulated to this point
- Its animal's behavioral DNA (copied from code-animal-library.md)
- Its assigned role specific to this architecture
- The attack format template (below)
- For Round 2+: a one-line patch reason (no attribution to which animal caused it),
  e.g., "Architecture now uses event sourcing to avoid shared mutable state." This lets
  animals evolve their angle without breaking role-lock.
- Instruction: "You are [Animal]. Attack this architecture from your behavioral DNA.
  You have zero knowledge of any other attacker or any other attack. Produce
  one attack (120–150 words) and one Kill Shot (one sentence)."

Subagents run in parallel per round. God Agent collects all attacks, scores them,
eliminates the weakest, applies absorption and patching, then spawns the next round
with the patched architecture.

**Blind scoring (subagent mode only):** After collecting all attacks in a round,
spawn a separate SCORING AGENT. It receives all attacks anonymized as "Attacker A",
"Attacker B", etc. — no animal names, no emoji, no behavioral DNA context. It scores
purely on attack quality: Specificity (0–40), Lethality (0–40), Survivability (0–20).
Returns rankings. God Agent maps anonymous scores back to animals and applies
elimination. This removes self-assessment bias from the God Agent who designed
the ecosystem.

**FALLBACK MODE** — Use when subagents are not available (Claude.ai, Cursor,
Windsurf, Copilot, single-context environments).

Role-play each animal sequentially within the same context. Before each animal's
attack, explicitly restate: "I am now [Animal]. I know nothing about any other
attack in this round. I know only the architecture and its patches." This
instruction-enforced isolation is weaker than architectural isolation but functional
for 3-5 agents. Quality degrades noticeably above 5 agents in fallback mode.

**State which mode is active at battle start:**
```
Execution: SUBAGENT MODE [or] FALLBACK MODE
Reason: [Agent tool available / Not available — single-context environment]
```

---

### Role-Lock Rule

Each animal has zero awareness of what other animals said. It knows only: the
original architecture plus all patches accumulated to that point. This is the
mechanism that produces genuine adversarial pressure.

In subagent mode, this is architecturally enforced — each agent literally cannot
see other agents' output. In fallback mode, this is instruction-enforced. If
role-lock is breaking down in fallback mode (attacks feel aware of each other),
restate the active animal's role explicitly at the top of its section and restart
the attack.

### Output Rendering

In subagent mode, animals execute in parallel but the God Agent MUST collect all
subagent responses before printing anything. Never stream partial results. Wait
for the full round to complete, then render the entire round as one block.

**Compression rule:** Subagents produce full 120-150 word attacks (needed for scoring
quality). The God Agent renders only the 2-sentence summary and kill shot in the round
table. Full attack text is used internally for blind scoring but NOT displayed. This
keeps rounds scannable while preserving attack depth for the scoring agent.

### Round structure

```markdown
## Round [N] — [X] animals remaining

| | Animal | Attack Summary | Kill Shot |
|---|---|---|---|
| [emoji] | [Animal] | [2-sentence summary] | [kill shot sentence] |
| [emoji] | [Animal] | [2-sentence summary] | [kill shot sentence] |
| ... | ... | ... | ... |

### Scores

| | Animal | Spec | Leth | Surv | Total | Verdict |
|---|---|---|---|---|---|---|
| [emoji] | [Animal] | /40 | /40 | /20 | **/100** | [one-line] |
| ... | ... | ... | ... | ... | ... | ... |

> **Eliminated:** [emoji] [Animal]
> **Consumed by:** [emoji] [Animal]
> **Absorbed:** [single sharpest insight]
> **Arch patch:** [concrete architectural change to survive this round]
```

**Early termination rule:** If an architecture survives two consecutive rounds with
only cosmetic patches (naming conventions, minor config changes, logging adjustments),
declare it structurally sound early. Do not manufacture rounds. State: "This
architecture has survived structural pressure. Remaining attacks are unlikely to
find fatal flaws." Then proceed to the apex output.

---

## Step 3 — Apex Output

```markdown
## Apex Predator — [emoji] [Animal]

[Why unkillable — 2 sentences max]

**Hypothesis verdict:** [confirmed or surprised? One sentence.]

### Architecture Evolution

| Round | Patch | Trigger |
|---|---|---|
| R1 | [concrete change] | [which threat forced it] |
| R2 | [concrete change] | [which threat forced it] |
| ... | ... | ... |

### The Fallen

| | Animal | Round | Key Contribution |
|---|---|---|---|
| [emoji] | [Animal] | R[N] | [insight contributed before elimination] |
| ... | ... | ... | ... |

### The Evolved Architecture

[Battle-hardened final version incorporating every round's patch.
Specific and concrete — stack, boundaries, data flow, failure modes addressed.
This is the architecture that survived the full ecosystem. One focused paragraph.]

### Technical Debt Statement

> [One sentence. The structural debt this architecture will inevitably
> accumulate and the approximate timeline before it demands repayment.
> Not a risk register — a prediction. An engineer reading this in 18 months
> should recognize the situation they are now living in.]

---

### Battle Quality

| Dimension | Score | Note |
|---|---|---|
| Execution mode | [SUBAGENT / FALLBACK] | |
| Role-lock integrity | [X]/10 | [one line] |
| Animal specificity | [X]/10 | [one line] |
| Kill shot lethality | [X]/10 | [one line] |
| **Overall** | **[HIGH / MEDIUM / DEGRADED]** | |

---

### Next Move

- **Validate first:** [one specific thing to prototype or load-test first]
- **Build first:** [the one component that proves the architecture holds]
- **Never build:** [the component that sounds important but lost every round]

---

### Battle Log

Copy this block into your next food chain code session to build on prior battles.

> **Date:** [date]
> **Original:** [one sentence]
> **Evolved:** [one sentence]
> **Apex:** [animal] | **TDS:** [technical debt statement]
> **Key patches:** [3 bullets]

**Companion skills:**
- `apex to action` — turn this into a 90-day execution plan
- `food chain monitor` — re-test after changes or pivots
```

---

## Calibration

**Sound architectures** — agents will struggle to land clean Kill Shots. Do not
manufacture weakness. Apply the early termination rule. A sound verdict is a useful
output — it means the design survived real pressure and can be built with confidence.

**Fragile architectures** — patches accumulate heavily. The final version may look
substantially different from the original. That is the intended outcome. Better to
discover this before writing 40,000 lines of code.

**Failure modes to self-detect before continuing:**
- All Kill Shots sound similar → ecosystem has overlapping failure vectors → stop, reassign
- Scoring feels arbitrary → animal roles are too generic → tighten roles before next round
- Patches are cosmetic two rounds in a row → apply early termination rule
- Role-lock is breaking → restate active animal's role explicitly and restart its attack
- Technical Debt Statement reads like a risk register bullet → rewrite until it reads like a prophecy
- Attacks reference specific code that does not exist yet → redirect to architectural decisions, not implementation details

---

## Known Limitations

- In fallback mode, role-lock is instruction-enforced, not architecturally enforced.
  Weaker inference environments may blur personas in later rounds. Use subagent mode
  when available — it eliminates this problem entirely.
- Fallback mode degrades noticeably above 5 agents. Cap at 5 in fallback mode unless
  the user explicitly requests more.
- Ecosystems above 7 agents produce diminishing returns even in subagent mode. Rarely
  more than 7 genuinely distinct non-overlapping failure vectors exist for any single
  architecture decision.
- Optimized for architectures with a defined stack, scale target, and team size.
  Vague "what stack should I use" questions produce lower-quality battles. Define the
  architecture first, then stress-test the decision.
- Does not replace load testing, chaos engineering, or security audits. Those test
  implementations. This tests the decisions that precede implementation.
- Animals attack the architecture as proposed, not as it will be implemented. A design
  that survives the food chain can still be built poorly. This skill tests the blueprint,
  not the construction.
