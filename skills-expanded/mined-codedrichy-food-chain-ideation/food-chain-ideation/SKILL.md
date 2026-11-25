---
name: food-chain-ideation
version: 2.1.0
description: >
  10-minute pre-ship stress-test. Run this before you ship, not instead of shipping.
  Dynamically selects animal agents from a behavioral DNA library matched to the specific
  problem, each attacking under strict role-lock with zero shared context. Weakest
  eliminated each round, survivor absorbs the insight and evolves, idea patches itself
  until one apex predator stands. Quick mode (5 animals, 1 round) for fast verdicts.
  Full mode for high-stakes decisions. Works in Claude.ai, Claude Code, Cursor, Windsurf,
  Copilot, and any agent with no dependencies.
when_to_use: >
  "food chain", "pressure test", "stress test", "tear this apart",
  "what kills this", "battle test", "adversarial review", "poke holes in this",
  "what would kill this idea", "attack my idea", "is this idea any good",
  "validate my idea", "should I build this", "red team my idea",
  "devil's advocate", "critique my startup", "is my idea viable",
  "test my business idea", "challenge my idea", "find flaws in my idea"
argument-hint: "[your idea]"
---

# Food Chain Ideation

10-minute pre-ship stress-test. Run this before you build, not instead of building.
Each agent attacks from a distinct angle under strict role-lock. Weak arguments
eliminated each round. Survivors absorb and evolve. The idea patches itself.
One apex predator remains. Output tells you what to change Monday morning.

---

## What This Is

The only adversarial skill built for product decisions, not code review. It produces
insights a single-agent critique cannot — because each attacker has no knowledge of
the other attacks, the elimination mechanic forces real intellectual pressure, and
the idea is stress-tested against its evolved version in every subsequent round.

## What This Is Not

- A debate tool. Agents do not respond to each other — they attack the idea independently.
- A brainstorming tool. Use a brainstorming skill before this one if the idea is not yet defined.
- A validation tool for pre-ideation. Requires a defined idea with a stated ICP and market.
- A code review tool. For code, use an adversarial code review skill.

---

## Prerequisites

Read `references/animal-library.md` before designing any ecosystem.
Use the Quick Selection Guide at the top of that file to identify candidate animals fast.
Never invent behavioral traits from scratch. Never select animals whose DNA overlaps.
Check the Anti-Pattern Combinations section before finalizing the ecosystem.

---

## Pre-Flight Checks

Run these before starting the battle. If any fail, fix them before proceeding.

1. **Input sharp enough?** The idea must contain three things: a defined ICP, a stated geography or market, and a named problem. If any are missing, ask one mandatory question before proceeding. Not optional. Not skippable.

```
Before the battle begins, I need one thing:
Who specifically feels this problem, where are they,
and what are they doing instead of using your product?
```

Do not design the ecosystem until this is answered. Generic input produces generic attacks — this is the single biggest quality lever in the entire skill.

2. **Ecosystem sound?** Verify minimum requirements: one structural hunter, one status quo representative, one resource/incumbent threat. If missing any, reassign.
3. **No overlap?** Check every pair of selected animals against the Anti-Pattern Combinations list.
4. **Roles specific?** Every assigned role must be specific to this exact idea. If any role could describe an attacker in a different industry, rewrite it.
5. **Prior battle log?** If the user pastes a battle log from a previous session, read it. Acknowledge what changed since last time. Select animals that attack the evolved version, not the original. Do not repeat attacks that were already absorbed.
6. **God Agent hypothesis stated?** Before the first attack, state in one sentence what you believe is most likely to kill this idea. This creates accountability and makes the final verdict meaningful.

---

## Step 0 — Agent Count

Analyze the idea. Recommend an agent count. Wait for user confirmation.

```
Complexity: [SIMPLE / MEDIUM / COMPLEX / MAXIMUM]
Reason: [2 sentences]
Hypothesis: [One sentence — what is most likely to kill this idea]
Recommended: [N] agents → [N-1] elimination rounds

How many agents? [3 / 5 / 7 / 9 / custom]
```

**Thresholds:**
- Simple — single feature, clear market, known problem → 3
- Medium — new category, multiple stakeholders, untested assumptions → 5
- Complex — platform business, regulatory exposure, multi-sided market → 7
- Maximum — systemic disruption, novel technology, highly uncertain market → 9

**Environment fallback:** If operating in a context window under 8,000 tokens or a
degraded inference environment, cap at 3 agents automatically and state this explicitly.

---

## Quick Mode

Default entry point for first-time users and fast pre-ship checks. Offer quick mode
before full mode unless the user explicitly requests a full battle.

```
Quick mode: 5 curated animals, 1 round, no elimination.
Full mode:  3–9 animals, elimination rounds, absorption, apex predator.

Which mode? [quick / full]
```

**Quick mode rules:**
- 5 animals selected from the library, covering the three minimum ecosystem requirements
  (structural hunter + status quo + resource threat) plus two idea-specific threats
- 1 round only. All 5 attack in parallel. Blind scoring ranks them.
- No elimination, no absorption, no patching between rounds.
- Output is a priority-ranked table: top 3 findings ordered by "what changes your
  next action," not by score. Each finding includes a one-sentence "Change Monday"
  action — what the builder should do differently based on this attack.
- Total time: under 10 minutes including ecosystem design.

**Quick mode output:**

```markdown
## Quick Battle — Verdict

| Priority | Threat | Change Monday |
|---|---|---|
| 1 | [most actionable finding — one sentence] | [what to do differently — one sentence] |
| 2 | [second finding] | [action] |
| 3 | [third finding] | [action] |

**Overall:** [SHIP / SHIP WITH CHANGES / PAUSE AND RETHINK]

> Run `full mode` to stress-test with elimination rounds and compound pressure.
```

**When to recommend full mode instead:** Platform businesses, regulated industries,
multi-sided marketplaces, or any idea where the user says "this is high-stakes."
Quick mode is for the 80% case: solo builder validating before shipping.

---

## Step 1 — Ecosystem Design

Select from `references/animal-library.md`. Use the Quick Selection Guide first.

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

### Selection Reasoning

After the ecosystem table, explain 2-3 key selection decisions:
`Selected: [Animal] over [Rejected] — [why this vector is more specific]`
This lets the user challenge selections before the battle starts.

---

## Step 2 — Battle Rounds

Repeat until one animal remains.

### Execution Mode Detection — Auto-detect at battle start. Do not ask the user.

**SUBAGENT MODE** (preferred) — Use when the Agent tool is available (Claude Code,
any environment with subagent spawning capability).

Each animal is spawned as an independent subagent. The subagent receives ONLY:
- The idea description + all patches accumulated to this point
- Its animal's behavioral DNA (copied from animal-library.md)
- Its assigned role specific to this idea
- The attack format template (below)
- For Round 2+: a one-line patch reason (no attribution to which animal caused it),
  e.g., "Idea now uses creator-uploaded content to avoid API dependency." This lets
  animals evolve their angle without breaking role-lock — the obvious attack was
  already patched, forcing a new approach.
- Instruction: "You are [Animal]. Attack this idea from your behavioral DNA.
  You have zero knowledge of any other attacker or any other attack. Produce
  one attack (120–150 words), a 2-sentence summary of the attack, and one
  Kill Shot (one sentence)."

Subagents run in parallel per round. God Agent collects all attacks, scores them,
eliminates the weakest, applies absorption and patching, then spawns the next round.

**Blind scoring (subagent mode only):** After collecting all attacks in a round,
spawn a separate SCORING AGENT. It receives all attacks anonymized as "Attacker A",
"Attacker B", etc. — no animal names, no emoji, no behavioral DNA context. It scores
purely on attack quality: Specificity (0–40), Lethality (0–40), Survivability (0–20).
Returns rankings plus a 1-line justification per dimension (e.g.,
`Specificity: 35/40 — "Names exact API endpoint and rate limit"`), rendered as a
footnote. God Agent maps scores back to animals and eliminates. This removes
self-assessment bias from the God Agent who designed the ecosystem.

**FALLBACK MODE** — Use when subagents are not available (Claude.ai, Cursor,
Windsurf, Copilot, single-context environments). Role-play each animal sequentially.
Before each attack, restate: "I am now [Animal]. I know nothing about any other
attack in this round." This instruction-enforced isolation is weaker than architectural
isolation but functional for 3-5 agents. Degrades above 5 agents in fallback.

**DATA MODE** — Auto-detect alongside execution mode. When WebSearch/WebFetch are
available, subagents search for current competitor data, funding rounds, and pricing
before attacking; kill shots cite current data. `Data: LIVE` or `Data: STATIC` (no
web tools — no degradation of core logic).
**State at battle start:** `Execution: SUBAGENT [or] FALLBACK | Data: LIVE [or] STATIC`

---

### Role-Lock Rule

Each animal has zero awareness of what other animals said. It knows only: the
original idea plus all patches accumulated to that point. This is the mechanism
that produces genuine adversarial pressure.
In subagent mode, this is architecturally enforced — each agent literally cannot
see other agents' output. In fallback mode, this is instruction-enforced. If
role-lock is breaking down (attacks feel aware of each other), restate the active
animal's role explicitly and restart the attack.

### Output Rendering

In subagent mode, the God Agent MUST collect all subagent responses before printing
anything. Never stream partial results. Render the entire round as one block.
**Compression rule:** Subagents produce full 120-150 word attacks (needed for scoring
quality). The God Agent renders only the 2-sentence summary and kill shot in the round
table. Full attack text is used internally for blind scoring but NOT displayed.

### Round structure

```markdown
## Round [N] — [X] animals remaining

| | Animal | Attack Summary | Kill Shot |
|---|---|---|---|
| [emoji] | [Animal] | [2-sentence summary] | [kill shot sentence] |
| [emoji] | [Animal] | [2-sentence summary] | [kill shot sentence] |
| ... | ... | ... | ... |

**Kill shot confidence tags:** **CONFIRMED** (verifiable data) | **PROBABLE** (strong structural signal) | **SPECULATIVE** (plausible, needs validation). Format: `Kill Shot [CONFIRMED]: "..."`

### Scores

| | Animal | Spec | Leth | Surv | Total | Verdict |
|---|---|---|---|---|---|---|
| [emoji] | [Animal] | /40 | /40 | /20 | **/100** | [one-line] |
| ... | ... | ... | ... | ... | ... | ... |

> **Eliminated:** [emoji] [Animal]
> **Consumed by:** [emoji] [Animal]
> **Absorbed:** [single sharpest insight]
> **Idea patch:** [concrete change to survive this round]
```

### Founder Defense (Optional)

After collecting attacks but before scoring, spawn a **Founder Agent** that receives ALL
attacks (breaks role-lock intentionally), produces 1 defense per attack (2 sentences max).
Scoring agent scores **residual lethality after defense**. Strong defense = manageable;
weak defense = full lethality stands. Active in subagent mode; skipped in fallback.

**Early termination rule:** If an idea survives two consecutive rounds with only
cosmetic patches, declare it structurally sound early. Do not manufacture rounds.
State: "This idea has survived structural pressure. Remaining attacks are unlikely
to find fatal flaws." Then proceed to the apex output.

---

## Audience Agent

After the final round and before the apex output, spawn one final subagent (or role-play
in fallback mode) — the ICP itself.

### Persona Construction

Build the persona from the sharpened input in pre-flight check #1. The persona must include:
- **Role:** job title or life situation (e.g., "solo founder, 6 months in, first SaaS")
- **Context:** what they're doing today to solve this problem (the status quo)
- **Constraints:** budget, time, team size, technical ability
- **Motivation:** why they'd look for a solution right now (trigger event)
- **Skepticism profile:** what makes them say no to new tools in general

If the pre-flight input is too thin to construct all five, fill gaps with the most
conservative plausible defaults (lowest budget, least time, most skeptical).

### What It Receives

In subagent mode, the audience agent receives ONLY:
- The evolved idea (final patched version)
- The unfair advantage statement
- The constructed ICP persona

Zero battle context. Zero knowledge of which animals attacked or what was eliminated.
It reacts to the final product, not the process.

### What It Answers

The audience agent answers five questions, not three:

1. **Would you pay for this?** (or invest time if free) — yes/maybe/no with one sentence why
2. **What would make you say yes immediately?** — the single trigger
3. **What would make you say no?** — the single dealbreaker
4. **What's confusing?** — the part of the pitch that doesn't land on first read
5. **Who else would you tell about this?** — zero people (bad sign), or specific
   role/community (distribution signal)

### Audience Panel (3 ICPs)

Spawn 3 audience agents (or 3 sequential in fallback): **Early Adopter** (tech-forward,
low price sensitivity, high churn risk) | **Mainstream Buyer** (needs proof, references,
case studies) | **Skeptical Enterprise** (procurement, security review, legal approval).
Each answers the same 5 questions. Divergence is signal: all agree = strong positioning;
adopter yes / others no = distribution problem; enterprise no = not enterprise-ready.
Subagent: parallel. Fallback: sequential.

### Confidence Calibration

After answering, the audience agent rates its own confidence:
- **HIGH** — "I know exactly what this is and whether I want it"
- **MEDIUM** — "I get the concept but need to see it working"
- **LOW** — "I'm not sure this is for me or what it replaces"

LOW confidence is a signal the evolved idea's positioning is unclear — the battle
hardened the product but not the pitch. Flag this in the apex output.

### Failure Modes

- Audience agent sounds like a cheerleader → persona is too generic. Tighten constraints.
- Audience agent rejects everything → skepticism profile is too aggressive. Match to real ICP.
- Answers feel detached from the idea → persona wasn't built from the pre-flight input.
  Reconstruct from the actual ICP stated in check #1, not a generic buyer.

---

## Pivot Engine

Activates ONLY when the God Agent determines the idea has been fundamentally killed —
not restructured, not patched, but killed. If every round's patches accumulated to the
point where the final version is unrecognizable from the original AND the unfair advantage
statement cannot be written without forcing it, the idea is dead.

When activated:
1. Generate 3 pivots from the wreckage — each a one-paragraph idea informed by what
   the battle revealed about the market, the ICP, and the threat landscape
2. Run a MINI-BATTLE on each pivot: 3 animals, 1 round, no elimination, just attacks
3. Score and rank the pivots by survivability
4. Present the best pivot as the recommended next direction

```markdown
## Pivot Engine — original idea did not survive

| # | Pivot | Survivability | Verdict |
|---|---|---|---|
| 1 | [one-paragraph description] | **HIGH / MEDIUM / LOW** | [one sentence] |
| 2 | [one-paragraph description] | **HIGH / MEDIUM / LOW** | [one sentence] |
| 3 | [one-paragraph description] | **HIGH / MEDIUM / LOW** | [one sentence] |

**Recommended:** Pivot [N] — [one sentence why]
```

In subagent mode, run all 3 mini-battles in parallel (9 subagents total — 3 per pivot).
In fallback mode, run sequentially.

---

## Step 3 — Apex Output

```markdown
## Apex Predator — [emoji] [Animal]

[Why unkillable — 2 sentences max]

**Hypothesis verdict:** [confirmed or surprised? One sentence.]

### Idea Evolution

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

### The Evolved Idea

[Battle-hardened final version. Specific, concrete. This is the idea
that survived the full ecosystem. One focused paragraph.]

### Unfair Advantage

> [One sentence. Structural compounding advantage. A competitor
> reading this should pause. Not marketing copy.]

---

### Audience Check

| Persona | Verdict | Pay? | Yes trigger | No trigger | Confusing | Tell who? | Confidence |
|---|---|---|---|---|---|---|---|
| Early Adopter | [Y/M/N] | [1 line] | [1 line] | [1 line] | [1 line] | [1 line] | [H/M/L] |
| Mainstream Buyer | [Y/M/N] | [1 line] | [1 line] | [1 line] | [1 line] | [1 line] | [H/M/L] |
| Skeptical Enterprise | [Y/M/N] | [1 line] | [1 line] | [1 line] | [1 line] | [1 line] | [H/M/L] |

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

### Change Monday

Top 3 findings ranked by what changes the builder's next action. Not scored by
attack quality — scored by "does this alter what you do tomorrow?"

| Priority | Finding | Action |
|---|---|---|
| 1 | [most actionable finding — one sentence] | [specific thing to change or test — one sentence] |
| 2 | [second finding] | [action] |
| 3 | [third finding] | [action] |

### Next Move

- **Validate first:** [one specific real-world test]
- **Build first:** [one feature that proves the unfair advantage]
- **Never build:** [feature that sounds important but lost every round]

---

### Battle Log

Copy this block into your next food chain session to build on prior battles.

> **Date:** [date]
> **Original:** [one sentence]
> **Evolved:** [one sentence]
> **Apex:** [animal] | **UAS:** [unfair advantage statement]
> **Key patches:** [3 bullets]

**Companion skills:**
- `apex to action` — turn this into a 90-day execution plan
- `food chain monitor` — re-test after changes or pivots
```

---

## Calibration

**Strong ideas** — agents will struggle to land clean Kill Shots. Do not manufacture
weakness. Apply the early termination rule. A strong verdict is a useful output.

**Weak ideas** — patches accumulate heavily. The final version may look substantially
different from the original. That is the intended outcome.

**Failure modes to self-detect before continuing:**
- All Kill Shots sound similar → ecosystem has overlapping attack vectors → stop, reassign
- Scoring feels arbitrary → animal roles are too generic → tighten roles before next round
- Patches are cosmetic two rounds in a row → apply early termination rule
- Role-lock is breaking → restate active animal's role explicitly and restart its attack
- Unfair Advantage Statement reads like a tagline → rewrite until it reads like a threat assessment

**Known limitations:**
- In fallback mode, role-lock is instruction-enforced, not architecturally enforced.
  Weaker inference environments may blur personas in later rounds. Use subagent mode
  when available — it eliminates this problem entirely.
- Fallback mode degrades noticeably above 5 agents. Cap at 5 in fallback mode unless
  the user explicitly requests more.
- Ecosystems above 7 agents produce diminishing returns even in subagent mode. Rarely
  more than 7 genuinely distinct non-overlapping attack vectors exist for any single problem.
- Optimized for ideas with a defined ICP and market. Pre-ideation brainstorming
  produces lower-quality battles. Define the idea first.

---

## Validated Output

See [`references/validated-output.md`](references/validated-output.md) for three tests
across different domains (B2B SaaS restructured, consumer marketplace killed, developer
tool validated) with benchmark methodology notes.
