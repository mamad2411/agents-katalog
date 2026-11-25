---
name: food-chain-pitch
version: 1.0.0
description: >
  Investor pitch stress-tester. Spawns adversarial agents from a pitch-specific
  behavioral DNA library. Each attacks the pitch narrative, financial model, or
  due diligence surface under strict role-lock. Elimination rounds harden the pitch.
  Works in Claude.ai, Claude Code, Cursor, Windsurf, Copilot with no dependencies.
when_to_use: >
  "food chain pitch", "stress test my pitch", "tear apart my deck",
  "what would investors ask", "due diligence test", "pitch practice",
  "will this raise", "attack my fundraise"
argument-hint: "[your pitch or deck summary]"
---

# Food Chain Pitch

Investor pitch stress-tester. Each agent attacks the pitch narrative, financial
model, or due diligence surface from a distinct angle under strict role-lock.
Weak arguments eliminated each round. Survivors absorb and evolve. The pitch
patches itself. One apex predator remains. Output tells you what to fix before
you walk into the room.

---

## What This Is

The only adversarial skill built for fundraise preparation, not product validation.
It produces the questions a serious investor will ask and tests whether your pitch
currently answers them — because each attacker operates in isolation with zero
shared context, the elimination mechanic forces genuine diligence pressure, and
the pitch is stress-tested against its evolved version in every subsequent round.

## What This Is Not

- A product stress-tester. For product ideas, use `food-chain-ideation`.
- A deck design tool. This attacks content and claims, not slide layout.
- A financial modeling tool. It pressure-tests assumptions, not spreadsheets.
- A replacement for real investor conversations. It simulates diligence, not relationships.

---

## Prerequisites

Read `references/pitch-animal-library.md` before designing any ecosystem.
Use the Quick Selection Guide at the top of that file to identify candidate animals fast.
Never invent behavioral traits from scratch. Never select animals whose DNA overlaps.
Check the Anti-Pattern Combinations section before finalizing the ecosystem.

---

## Pre-Flight Checks

Run these before starting the battle. If any fail, fix them before proceeding.

1. **Input sharp enough?** The pitch must contain five things: stage (pre-seed / seed / A / B / C), ask amount, key metrics claimed (ARR, growth rate, margins, or proxies if pre-revenue), target investor profile (angels, institutional seed, multi-stage), and a one-sentence thesis (why this company wins). If any are missing, ask before proceeding. Not optional. Not skippable.

```
Before the battle begins, I need:
1. What stage are you raising? (pre-seed / seed / A / B / C)
2. How much are you raising and at what valuation?
3. Key metrics: ARR (or MRR), growth rate, gross margin, burn rate.
   If pre-revenue: users, waitlist, LOIs, or pilot commitments.
4. Who is the target investor? (angels, seed GPs, Series A partners, specific funds)
5. One sentence: why does this company win?
```

Do not design the ecosystem until this is answered. Generic pitch input produces generic attacks — this is the single biggest quality lever in the entire skill.

2. **Ecosystem sound?** Verify minimum requirements: one financial attacker, one narrative attacker, one market/competitive attacker. If missing any, reassign.
3. **No overlap?** Check every pair of selected animals against the Anti-Pattern Combinations list.
4. **Roles specific?** Every assigned role must be specific to this exact pitch. If any role could describe an attacker against a different company's raise, rewrite it.
5. **Prior battle log?** If the user pastes a battle log from a previous session, read it. Acknowledge what changed since last time. Select animals that attack the evolved pitch, not the original. Do not repeat attacks that were already absorbed.
6. **God Agent hypothesis stated?** Before the first attack, state in one sentence what you believe is most likely to kill this pitch. This creates accountability and makes the final verdict meaningful.

---

## Real-Time Data Mode

At battle start, detect whether WebSearch and WebFetch tools are available.

- **Data: LIVE** — agents research current market data, competitor funding rounds, comparable exits, and recent sector-specific investor sentiment before attacking. Each attack cites a real data point where possible.
- **Data: STATIC** — agents attack using only the information provided by the user and general knowledge. No external lookups.

Display the badge in the ecosystem announcement. LIVE mode produces materially stronger attacks — recommend the user run in an environment that supports it if they are in STATIC mode and the pitch is high-stakes.

---

## Step 0 — Agent Count

Analyze the pitch. Recommend an agent count. Wait for user confirmation.

```
Complexity: [SIMPLE / MEDIUM / COMPLEX / MAXIMUM]
Reason: [2 sentences]
Hypothesis: [One sentence — what is most likely to kill this pitch]
Recommended: [N] agents -> [N-1] elimination rounds

How many agents? [3 / 5 / 7 / custom]
```

**Thresholds:**
- Simple — clear metrics, proven model, single product, known market -> 3
- Medium — early metrics, new category, multi-product, competitive market -> 5
- Complex — pre-revenue, platform play, regulatory exposure, multi-sided -> 7
- Maximum — deep tech, novel market, highly uncertain unit economics -> 7 (cap)

**Environment fallback:** If operating in a context window under 8,000 tokens or a
degraded inference environment, cap at 3 agents automatically and state this explicitly.

---

## Step 1 — Ecosystem Design

Select from `references/pitch-animal-library.md`. Use the Quick Selection Guide first.

**Animal selection reasoning:** For each selected animal, state in one sentence why
it was chosen and name one rejected animal with a one-sentence reason for rejection.
This makes ecosystem design transparent and auditable.

**Announce the ecosystem with attack vectors visible:**

```markdown
## Ecosystem

| | Animal | Role | Attack Vector |
|---|---|---|---|
| [emoji] | [Animal] | [Role] | [one line] |
| [emoji] | [Animal] | [Role] | [one line] |
| ... | ... | ... | ... |

**Selection reasoning:**
- [emoji] [Animal] selected because [one sentence]. Rejected [Animal] because [one sentence].
- [...]

**God Agent hypothesis:** [Restate the kill hypothesis from Step 0]
**Execution:** [SUBAGENT / FALLBACK] — [reason]
**Data:** [LIVE / STATIC]
```

---

## Step 2 — Battle Rounds

Repeat until one animal remains.

### Execution Mode Detection

Auto-detect at battle start. Do not ask the user.

**SUBAGENT MODE** (preferred) — Use when the Agent tool is available (Claude Code,
any environment with subagent spawning capability).

Each animal is spawned as an independent subagent. The subagent receives ONLY:
- The pitch summary + all patches accumulated to this point
- Its animal's behavioral DNA (copied from pitch-animal-library.md)
- Its assigned role specific to this pitch
- The attack format template (below)
- For Round 2+: a one-line patch reason (no attribution to which animal caused it),
  e.g., "Pitch now includes customer-level unit economics with 6-month payback."
- Instruction: "You are [Animal]. Attack this pitch from your behavioral DNA.
  You have zero knowledge of any other attacker or any other attack. Produce
  one attack (120-150 words), a 2-sentence summary of the attack, one Kill Shot
  (one sentence), and a kill shot confidence tag: CONFIRMED (data proves it),
  PROBABLE (strong inference), or SPECULATIVE (plausible but unverified)."

Subagents run in parallel per round. God Agent collects all attacks, scores them,
eliminates the weakest, applies absorption and patching, then spawns the next round
with the patched pitch.

**Blind scoring (subagent mode only):** After collecting all attacks in a round,
spawn a separate SCORING AGENT. It receives all attacks anonymized as "Attacker A",
"Attacker B", etc. — no animal names, no emoji, no behavioral DNA context. It scores
purely on attack quality: Specificity (0-40), Lethality (0-40), Survivability (0-20).
Each score includes a 1-line justification. Returns rankings. God Agent maps anonymous
scores back to animals and applies elimination.

**FALLBACK MODE** — Use when subagents are not available (Claude.ai, Cursor,
Windsurf, Copilot, single-context environments).

Role-play each animal sequentially within the same context. Before each animal's
attack, explicitly restate: "I am now [Animal]. I know nothing about any other
attack in this round. I know only the pitch and its patches." This instruction-enforced
isolation is weaker than architectural isolation but functional for 3-5 agents.

**State which mode is active at battle start:**
```
Execution: SUBAGENT MODE [or] FALLBACK MODE
Reason: [Agent tool available / Not available — single-context environment]
```

---

### Role-Lock Rule

Each animal has zero awareness of what other animals said. It knows only: the
original pitch plus all patches accumulated to that point. This is the mechanism
that produces genuine adversarial pressure.

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

### Founder Defense

After each round's attacks are rendered, the founder gets a defense pass:
- 2-sentence defense per attack (either from the user or AI-generated if the user
  requests auto-defense)
- The scoring agent then scores **residual lethality** (0-10) for each attack
  after hearing the defense. This determines elimination, not the raw score.
- An attack that scores 35/40 on lethality but drops to 2/10 residual after
  defense is weaker than an attack scoring 25/40 that stays at 8/10 residual.

### Round structure

```markdown
## Round [N] — [X] animals remaining

| | Animal | Attack Summary | Kill Shot | Confidence |
|---|---|---|---|---|
| [emoji] | [Animal] | [2-sentence summary] | [kill shot sentence] | [CONFIRMED / PROBABLE / SPECULATIVE] |
| ... | ... | ... | ... | ... |

### Founder Defense

| | Animal | Defense | Residual Lethality |
|---|---|---|---|
| [emoji] | [Animal] | [2-sentence defense] | [0-10] — [1-line justification] |
| ... | ... | ... | ... |

### Scores

| | Animal | Spec | Leth | Surv | Total | Residual | Verdict |
|---|---|---|---|---|---|---|---|
| [emoji] | [Animal] | /40 [1-line] | /40 [1-line] | /20 [1-line] | **/100** | /10 | [one-line] |
| ... | ... | ... | ... | ... | ... | ... | ... |

> **Eliminated:** [emoji] [Animal]
> **Consumed by:** [emoji] [Animal]
> **Absorbed:** [single sharpest insight]
> **Pitch patch:** [concrete change to survive this round]
```

**Early termination rule:** If a pitch survives two consecutive rounds with only
cosmetic patches (word changes, minor reframing, slide reordering), declare it
structurally sound early. Do not manufacture rounds. State: "This pitch has
survived structural diligence pressure. Remaining attacks are unlikely to surface
fatal questions." Then proceed to the apex output.

---

## Investor Simulation

After the final round and before the apex output, spawn the INVESTOR SIMULATION —
three independent investor personas who each evaluate the evolved pitch.

### Panel Construction

Build each persona from the stage and target investor profile provided in pre-flight:

1. **Angel investor** — writes $25K-$100K checks. Evaluates: founder conviction,
   market intuition, personal thesis alignment. Forgives missing metrics. Punishes
   vague vision.
2. **Seed GP** — leads $1M-$4M rounds from a $50M-$150M fund. Evaluates: market
   size methodology, early traction signals, founder-market fit, capital efficiency.
   Needs a thesis match to their fund's stated focus.
3. **Series A partner** — leads $8M-$20M rounds from a $300M+ fund. Evaluates:
   repeatable growth engine, unit economics at scale, competitive moat, path to
   $100M ARR. Needs proof, not promise.

Adjust personas to match the actual stage being raised. If raising Series B, shift
the panel: seed GP becomes Series A partner, Series A partner becomes growth equity
investor, angel becomes seed GP looking at follow-on signal.

### What Each Investor Receives

In subagent mode, each investor persona receives ONLY:
- The evolved pitch (final patched version)
- The stage, ask amount, and claimed metrics
- Their investor persona profile

Zero battle context. Zero knowledge of which animals attacked or what was eliminated.
They react to the final pitch, not the process.

### What Each Investor Answers

Each investor answers independently:

| Question | Format |
|---|---|
| **Would you take the meeting?** | YES / MAYBE / NO + one sentence |
| **Would you invest?** | YES / MAYBE / NO + one sentence |
| **What's the single biggest concern?** | One sentence |
| **What data point would change your mind?** | One sentence |

### Output Format

```markdown
### Investor Panel

| | Investor | Meeting? | Invest? | Biggest Concern | Mind-Changer |
|---|---|---|---|---|---|
| 1 | Angel ($25-100K) | [Y/M/N] | [Y/M/N] | [one sentence] | [one sentence] |
| 2 | Seed GP ($1-4M) | [Y/M/N] | [Y/M/N] | [one sentence] | [one sentence] |
| 3 | Series A ($8-20M) | [Y/M/N] | [Y/M/N] | [one sentence] | [one sentence] |
```

---

## Dead Pitch Handling

NO pivot engine. If the pitch is killed — every round's patches accumulated to
the point where the narrative is unrecognizable and the core thesis cannot be
defended — redirect:

```
This pitch did not survive diligence pressure. The idea may still be valid,
but the pitch narrative and financial model need fundamental rework.

Recommended next step:
- Run `food-chain-ideation` on the underlying product idea to validate
  whether the problem and solution survive before rebuilding the pitch.
```

Do not generate pivots. Do not attempt to salvage the pitch inline. A dead pitch
needs product-level rethinking, not slide-level fixes.

---

## Step 3 — Apex Output

```markdown
## Apex Predator — [emoji] [Animal]

[Why unkillable — 2 sentences max]

**Hypothesis verdict:** [confirmed or surprised? One sentence.]

### Pitch Evolution

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

### The Evolved Pitch

[Battle-hardened final version. Specific, concrete. This is the pitch
narrative that survived full diligence pressure. One focused paragraph.]

### Due Diligence Survival

The top 3 questions a serious investor at this stage would ask in diligence,
with whether the pitch currently answers them.

| # | Question | Currently Answered? | Gap |
|---|---|---|---|
| 1 | [specific diligence question] | YES / PARTIAL / NO | [what's missing] |
| 2 | [specific diligence question] | YES / PARTIAL / NO | [what's missing] |
| 3 | [specific diligence question] | YES / PARTIAL / NO | [what's missing] |

---

### Investor Panel

[Rendered from Investor Simulation above]

---

### Battle Quality

| Dimension | Score | Note |
|---|---|---|
| Execution mode | [SUBAGENT / FALLBACK] | |
| Data mode | [LIVE / STATIC] | |
| Role-lock integrity | [X]/10 | [one line] |
| Animal specificity | [X]/10 | [one line] |
| Kill shot lethality | [X]/10 | [one line] |
| Founder defense quality | [X]/10 | [one line] |
| **Overall** | **[HIGH / MEDIUM / DEGRADED]** | |

---

### Fix Before the Room

Top 3 findings ranked by what changes the pitch's outcome in a real meeting.
Not scored by attack quality — scored by "does this change whether you get a term sheet?"

| Priority | Finding | Fix |
|---|---|---|
| 1 | [most critical pitch gap — one sentence] | [specific change to make — one sentence] |
| 2 | [second finding] | [fix] |
| 3 | [third finding] | [fix] |

### Next Move

- **Answer first:** [the single diligence question you must have a bulletproof answer for]
- **Add to deck:** [one slide or data point that is currently missing]
- **Remove from deck:** [one claim or slide that weakened under pressure every round]

---

### Battle Log

Copy this block into your next food chain session to build on prior battles.

> **Date:** [date]
> **Stage:** [stage] | **Ask:** [amount]
> **Original pitch:** [one sentence]
> **Evolved pitch:** [one sentence]
> **Apex:** [animal] | **Top diligence gap:** [one sentence]
> **Key patches:** [3 bullets]

**Companion skills:**
- `apex to action` — turn the evolved idea into a 90-day execution plan
- `food chain monitor` — re-test after pitch changes or new metrics
- `food-chain-ideation` — if the pitch died, stress-test the underlying idea
```

---

## Calibration

**Strong pitches** — agents will struggle to land clean kill shots. Do not manufacture
weakness. Apply the early termination rule. A strong verdict is a useful output — it
means the pitch survived real diligence pressure and the founder can walk in confident.

**Weak pitches** — patches accumulate heavily. The final version may look substantially
different from the original. That is the intended outcome. Better to discover this
in a simulation than in front of a partner meeting.

**Failure modes to self-detect before continuing:**
- All kill shots sound similar -> ecosystem has overlapping attack vectors -> stop, reassign
- Scoring feels arbitrary -> animal roles are too generic -> tighten roles before next round
- Patches are cosmetic two rounds in a row -> apply early termination rule
- Role-lock is breaking -> restate active animal's role explicitly and restart its attack
- Founder defenses are too easy -> attacks are not specific enough -> sharpen animal roles
- Investor panel is unanimously positive -> personas are too generic -> tighten constraints
- All confidence tags are SPECULATIVE -> attacks lack grounding -> use LIVE data mode or sharpen claims

**Known limitations:**
- In fallback mode, role-lock is instruction-enforced, not architecturally enforced.
  Weaker inference environments may blur personas in later rounds. Use subagent mode
  when available.
- Fallback mode degrades noticeably above 5 agents. Cap at 5 in fallback mode unless
  the user explicitly requests more.
- STATIC data mode cannot verify market claims, competitor funding, or comparable exits.
  For high-stakes pitches (Series A+), strongly recommend running in a LIVE data environment.
- Optimized for pitches with defined metrics and a stated ask. "Should I raise?" is a
  different question — this skill tests the pitch, not the decision to fundraise.
- Does not replace real investor conversations. Simulated diligence catches structural
  gaps but cannot replicate relationship dynamics, fund-specific thesis matching, or
  partner meeting politics.
