---
name: iterative-refinement
description: >
  Rapid iterative refinement skill. Runs 4–6 structured improvement cycles on
  any output — writing, code, strategy, design — without losing coherence, regressing
  previous improvements, or drifting from the original intent. Each cycle targets
  a specific refinement dimension, tracks deltas explicitly, and terminates when
  the output reaches a defined quality threshold. Prevents the common failure where
  "make it better" produces sidewise movement instead of genuine improvement.
  Use when user says: refine this, iterate, make it better, run refinement cycles,
  improve this over multiple passes, keep improving, cycle through this, refine
  until good, multiple passes, polish this, iterate until done, run the loop,
  keep going until it's great, another pass, refine again.
  Do NOT activate for: first-draft generation, simple one-shot edits, structural
  rewrites that require rethinking from scratch.
  First response: "Iterative Refinement active. Paste the output to refine and
  describe what 'done' looks like — quality bar, intended use, audience. I'll
  run targeted cycles and track deltas."
license: Apache 2.0
---

# Iterative Refinement Loops

"Make it better" produces one of two failure modes: circular iteration (the output
changes but doesn't improve, just moves sideways) or regression (fixing one dimension
breaks another).

The solution is structured refinement: each cycle has a specific target dimension,
an explicit delta from the previous version, and a quality gate. The model knows what
it's optimizing for, knows what it changed, and knows when to stop.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/refine <output>` | Start a refinement loop with auto-selected dimensions |
| `/cycle <dimension>` | Run one targeted refinement cycle on a specific dimension |
| `/delta` | Show exactly what changed in the last cycle and why |
| `/score` | Score the current output against the quality target |
| `/target <description>` | Define or update the quality target |
| `/dimensions` | Show the active refinement queue and completed cycles |
| `/undo` | Revert to the previous cycle's output |
| `/lock <element>` | Lock a specific element — do not change this in future cycles |
| `/focus <dimension>` | Prioritize one dimension for the next N cycles |
| `/auto <n>` | Run n cycles automatically, picking the highest-value dimension each time |
| `/history` | Show all cycle deltas in sequence — full refinement log |
| `/done` | Declare the output final and output the refinement summary |

---

## HIGH-LEVEL WORKFLOW

```text
User provides output and quality target
    │
    ├─ Phase 1: Baseline Assessment
    │     Score the input across all refinement dimensions
    │
    ├─ Phase 2: Dimension Prioritization
    │     Rank dimensions by gap from target and impact
    │
    ├─ Phase 3: Targeted Cycles
    │     Apply one cycle per dimension; track every delta
    │
    ├─ Phase 4: Regression Check
    │     Confirm each cycle didn't regress a previously-improved dimension
    │
    ├─ Phase 5: Quality Gate
    │     Score after each cycle; stop when target is met
    │
    └─ Phase 6: Refinement Summary
          Report what changed, what improved, and what was locked
```

---

## PHASE 1 — REFINEMENT DIMENSIONS

Every output type has a set of refinement dimensions. Score each 1–5 before starting.

### Writing dimensions

| Dimension | Score 1 | Score 5 |
| --- | --- | --- |
| **Clarity** | Reader must re-read to understand | First read is enough; meaning is immediate |
| **Concision** | Words don't earn their place | Every word is necessary |
| **Impact** | Opening and close are weak | First and last sentences are strongest |
| **Specificity** | Vague; could apply to anything | Concrete, specific, tied to this context |
| **Flow** | Sentence-to-sentence movement is rough | Transitions are invisible; reading is effortless |
| **Tone** | Doesn't match the target audience | Exactly right for the audience and purpose |
| **Structure** | Organization is unclear or wrong | Structure serves the reader's needs |

### Code dimensions

| Dimension | Score 1 | Score 5 |
| --- | --- | --- |
| **Correctness** | Has bugs | Handles all cases correctly |
| **Readability** | Hard to follow | Intent is obvious on first read |
| **Robustness** | Crashes on edge cases | Handles unexpected inputs gracefully |
| **Performance** | Obvious inefficiencies | Appropriate for the use case |
| **Testability** | Hard to test in isolation | Clean interfaces; easy to mock |
| **Security** | Obvious vulnerabilities | Input validated; no injection points |

### Strategy / plan dimensions

| Dimension | Score 1 | Score 5 |
| --- | --- | --- |
| **Clarity of goal** | Ambiguous success criteria | Concrete, measurable outcomes |
| **Completeness** | Missing key steps | Every necessary step is present |
| **Risk coverage** | Major risks unaddressed | Key risks named with mitigations |
| **Feasibility** | Resources or timeline unrealistic | Grounded in real constraints |
| **Prioritization** | All steps treated equally | Critical path is clear |

---

## PHASE 2 — CYCLE EXECUTION

### Cycle structure

Each refinement cycle:
1. **Identify the target dimension** (highest gap × highest impact)
2. **Describe the specific improvement** before making it
3. **Apply the improvement**
4. **Write the delta note** — what changed and why
5. **Run regression check** — did this break anything previously improved?
6. **Score the dimension** — did it improve?

### Cycle output format

```text
CYCLE [N]: [dimension]
Target: [what this cycle is improving]
Gap before: [score]/5 → Target: [target score]/5

Changes made:
  · [specific change 1] — [why]
  · [specific change 2] — [why]

Delta:
  BEFORE: "[exact quote of changed section]"
  AFTER:  "[exact quote of new version]"

Regression check:
  [dimension previously improved]: [still holds / regressed — describe]

[Dimension] score: [before] → [after]
```

### Cycle targeting rules

1. **Never optimize two dimensions simultaneously in one cycle.** Clarity + Tone in one cycle produces mediocre improvement in both.
2. **Impact and opening/close first.** For writing, the opening and closing sentences deliver the most return per cycle.
3. **Correctness before readability.** For code, never polish what might be wrong.
4. **Lock wins.** Once a dimension scores 5, mark it locked unless the user explicitly unlocks it.
5. **Diminishing returns threshold.** If two consecutive cycles on the same dimension produce less than 0.5 score improvement, move to the next dimension.

---

## PHASE 3 — QUALITY GATE

After each cycle, calculate the overall quality score:

```text
QUALITY GATE — CYCLE [N]

Scores:
  [Dimension 1]:  [N]/5  [LOCKED / ACTIVE / REGRESSED]
  [Dimension 2]:  [N]/5  [LOCKED / ACTIVE / REGRESSED]
  ...

Overall: [avg]/5
Target:  [user-defined threshold]/5

Status: CONTINUE | DONE | REGRESSION DETECTED
```

### Stop conditions

- **Done:** Overall score ≥ target threshold (default: 4.2/5)
- **Done:** All active dimensions locked (all scored ≥ 4.5)
- **Stop and review:** Any dimension regressed after being locked
- **Stop and reframe:** 3+ consecutive cycles with < 0.3 total improvement

### Regression handling

If a cycle causes a regression:
1. Immediately revert to previous cycle's output
2. Re-run the cycle with a tighter constraint: "Improve [dimension] without touching [locked dimensions]"
3. If regression persists after 2 attempts, surface the tension explicitly: "Improving [A] conflicts with [B] because [reason]. Which takes priority?"

---

## PHASE 4 — DIMENSION-SPECIFIC TECHNIQUES

### Clarity cycles
- Replace abstract nouns with concrete verbs: "the implementation" → "the function that..."
- Split sentences that contain more than one idea
- Move the main clause first; subordinate clauses after
- Replace "this," "it," "they" with the actual noun when the referent is more than 2 sentences back

### Concision cycles
- Remove every word that does not change meaning if deleted
- Remove softeners: "somewhat," "quite," "rather," "a bit"
- Remove throat-clearing openers: "It is important to note that," "As we can see,"
- Replace prepositional phrases with a single word: "in the event that" → "if"
- Merge two sentences that make the same point

### Impact cycles
- Move the most important sentence first in every paragraph
- End the piece with the highest-stakes sentence, not a summary
- Find the most generic sentence and make it the most specific
- Find the most passive sentence and make it active

### Specificity cycles
- Replace every adjective that could apply to anything with one that couldn't
- Add a number where an amount is described: "many users" → "72% of users"
- Name the specific mechanism: "it improves performance" → "it reduces round trips by eliminating..."
- Ground the abstract: "a better experience" → "opens in under 200ms"

---

## PHASE 5 — REFINEMENT SUMMARY

When the loop completes:

```text
REFINEMENT COMPLETE

Cycles run: [N]
Total iterations: [N]

Quality progression:
  Cycle 0 (baseline): [N]/5
  Cycle 1: [N]/5 (+[delta]) — [dimension improved]
  Cycle 2: [N]/5 (+[delta]) — [dimension improved]
  ...
  Final: [N]/5

Dimensions locked: [list with final scores]
Dimensions not reached: [list with current scores — why not improved]

Most impactful change: [which cycle, which dimension, what changed]
What held back further improvement: [honest assessment of ceiling]
```
