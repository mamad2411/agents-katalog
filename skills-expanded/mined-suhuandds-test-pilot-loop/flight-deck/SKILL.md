# Insider Testing Skill — Test Pilot Loop
## v1.0 — Integrated into Flight Deck

---

## What Is Insider Testing?

Insider testing is not a checklist. It is a **thinking discipline**.

An Insider understands the product's purpose, uses it like someone who cares about the outcome, and evaluates whether the app actually does its job — not just whether buttons click.

| Tier | Reads Spec? | Tests What? | Thinks About? |
|------|------------|-------------|---------------|
| Cold | No | Can I figure this out? | First impressions, discoverability |
| Guided | Partially | Does it match instructions? | Flows, labeling, expected behavior |
| **Insider** | **Full spec** | **Does it achieve its purpose?** | **Outcomes, logic, design, edge cases** |

The Insider is the only tier that asks: **"The app ran successfully — but did it produce the right result?"**

---

## Phase 0: Mandatory Setup — Goal Discovery Q&A

### Where This Fits

This phase is part of the **existing mandatory setup** in AUTOPILOT.md:

```
AUTOPILOT.md Step 1: Read the project spec (CLAUDE.md, PRD.md)
──────────── NEW ────────────
Step 1.5: Goal Discovery Q&A (this skill)
──────────── END ────────────
AUTOPILOT.md Step 2: Set up auto-patrol (fswatch or /loop)
```

**After Claude Code reads the spec but BEFORE patrol starts**, Claude Code conducts a 6-question Q&A with the human. Questions 1-5 are generated from the spec. Question 6 is always the same: "Why are you testing?"

### Why Claude Code Asks (Not Cowork)

Claude Code is the brain. It reads CLAUDE.md and PRD.md — every screen, every button, every state transition. From this, it already knows what the app is supposed to do, what output it produces, and what formats/edge cases exist. But the spec doesn't tell Claude Code what "correct" looks like in the human's specific context, which test data is available, which edge cases have actually failed, or what the human cares about most. The Q&A fills those gaps.

### The 6 Questions

Claude Code generates Q1-Q5 dynamically from the spec. They are NOT generic templates — they reference specific features, formats, and edge cases from CLAUDE.md/PRD.md. Q6 is always asked verbatim.

#### Q1: Goal & Output Verification
> "I've read the spec. The app's goal is [X]. After a test run, where should the tester verify the result, and what does correct output look like?"

#### Q2: Failure Investigation
> "The spec describes [failure mechanism]. When the tester finds items in [failure location], how deep should they investigate?"

#### Q3: Test Data & Known Hard Cases
> "I see the spec handles [formats/features]. What test data is available, and which cases are most likely to break?"

#### Q4: Critical Settings
> "These settings affect the output: [list from spec]. Which ones should the tester change and re-verify?"

#### Q5: Out of Scope
> "I noticed these features in the spec that may not be built yet: [list]. Anything else the tester should skip? Anything that looks like a bug but is intentional?"

#### Q6: Why Are You Testing?
> "Last question — what's your main concern? Why do you want this tested right now?"

This is the most important question. It's asked last because by now the human is in the right headspace. Their answer reveals what they're actually worried about, which sets the tester's priority.

**Example answers and how they change testing priority:**

| Human says... | Tester prioritizes... |
|---------------|----------------------|
| "I'm not confident the OCR catches all name card formats" | Name card detection accuracy — test every format, study every missed card |
| "I just rebuilt the sort pipeline, worried about data loss" | File integrity — count every photo, verify nothing is lost or corrupted |
| "The app is for my dental assistant, she's not technical" | UX clarity — every label, every error message, every empty state |
| "I'm shipping this next week" | Full workflow reliability — happy path must be bulletproof |
| "I added a new feature and want to make sure it didn't break anything" | Regression — test existing features, not just the new one |

### How Claude Code Generates Questions 1-5

After reading CLAUDE.md / PRD.md, Claude Code:

1. **Identifies the primary goal** — what is the app's core job?
2. **Identifies the output** — where does the result go?
3. **Identifies the failure path** — where do rejected/failed items go?
4. **Lists output-affecting settings** — which settings change what the output looks like?
5. **Lists spec features by status** — what's built, what's post-MVP, what's in progress?

Then it formulates Q1-Q5 using this knowledge.

### Saving the Goals

Claude Code compiles the answers into `FLIGHT_DECK/INSIDER_GOALS.md`:

```markdown
# Insider Testing Goals — [Project Name]
## Generated: [date]
## Source: Goal Discovery Q&A (Claude Code + Human Director)

### ⚡ Testing Priority — READ THIS FIRST
[Why the human wants testing — from Q6]
[How this shifts time allocation and focus]

### Final Goal
[What success looks like — from Q1]

### Output Verification Method
[Where to check, what correct looks like — from Q1]
Verification location: [Finder path / URL / tool]
Verification method: [open folder / query database / compare files]

### Failure Investigation Protocol
[Where failures go, how deep to investigate — from Q2]
Failure location: [path]
Investigation depth: [count only / classify each / root-cause each]

### Test Data Inventory
[Available datasets and known hard cases — from Q3]
| Dataset | Path | Photos | Coverage | Notes |
|---------|------|--------|----------|-------|

### Critical Settings to Verify
[Settings that affect output — from Q4]
| Setting | Default | Test Values | How to Verify |
|---------|---------|-------------|---------------|

### Out of Scope
[What to skip — from Q5]

### Goal Verification Checklist
[Auto-generated from all answers]
□ [check 1]
□ [check 2]
□ [check 3]
```

**This file is read by Cowork (the test pilot) before every test flight.**

### When to Re-Run the Q&A

The Q&A runs once during initial setup. Re-run it when:
- New test data is added
- Major features are built that change the output
- Human changes their testing priorities
- First Q&A was too early (app wasn't built enough to answer meaningfully)

Append to INSIDER_GOALS.md rather than overwriting — track how goals evolve.

---

## Oracles — How the Tester Knows Something Is Wrong

An **oracle** is anything the tester compares against to decide if a result is correct or incorrect. Without oracles, the tester can only say "it didn't crash" — not "it did its job."

| Oracle | What It Is | Example |
|--------|-----------|---------|
| **The Spec** | What CLAUDE.md / PRD.md says should happen | "Spec says Format B: 'Patient' on own line, name on next line" |
| **The Output** | The actual files, folders, data produced | Open Finder → check patient folders → are right photos inside? |
| **The Input** | What went in — compare against what came out | 470 photos in → 430 sorted + 35 review + 5 excluded = 470? |
| **Consistency** | Same action should produce same result | Sort twice with same data → same output? |
| **Comparable Product** | How similar apps handle the same case | "Every other photo app handles this name format" |
| **User Expectations** | What a reasonable user would expect | "I'd expect my photos to be there after sorting" |
| **History** | What happened in previous test flights | "This worked last flight — regression?" |

**The most powerful oracle for goal verification is the output itself.**

### When Oracles Conflict

Sometimes the spec says one thing but the output suggests another approach is better. When oracles conflict, the tester notes it and asks the human in Phase 8. Don't silently resolve conflicts — surface them.

---

## The Adaptive Pivot — When to Go Deep

When a tester finds something unexpected, they don't just log it and move on. They **pivot** — immediately exploring related areas to understand the scope.

**The rule: One failure → test 5 related cases before moving on.**

| Tester finds... | Pivot to... |
|-----------------|-------------|
| One name card not detected | Test 5 more cards of the same format. Is it this card or this format? |
| One photo in wrong folder | Check 5 neighboring photos. Is it one mistake or a pattern? |
| Separator not updating in preview | Test date format, name order, tokens. Which settings update and which don't? |
| Slow performance on one dataset | Test same dataset size with different content. Is it size or content? |

**Why this matters for AI testers specifically:** AI agents tend to log an issue and proceed to the next checklist item. Human experts dig in. The pivot rule forces investigation before moving on.

---

## The Five Lenses

Every screen, every feature, every output must pass through all five lenses. The Insider holds all five in mind simultaneously.

### Lens 1: Does It Work?
> "I clicked it. Did something happen?"

The baseline. Buttons click, toggles change state, inputs accept text, navigation works, progress indicators advance. **This lens alone is NOT Insider testing. It's QA 101.**

### Lens 2: Does It Achieve the Goal?
> "The app said 'Done.' But did it actually do its job?"

**This is the most important lens. It is the reason Insider testing exists.**

The app exists to produce a result. After it finishes, leave the app and go verify the result independently. The UI saying "Sort Complete — 37 patients" is a claim. The Insider verifies the claim.

**Verify the output:**
- Open the output location (Finder, database, API, filesystem)
- Spot-check that results are correct, not just present
- Compare output against what you know should be there

**Investigate the failures:**
- Open the failure/review/error location
- For EACH failure item, ask: WHY is this here?
- Classify each failure: correct behavior? Engine limitation? Bug?
- Look for patterns: are all failures the same type?

**Reconcile the numbers:**
- Input count = output count + failure count + excluded count
- Any missing? That's a potential data loss bug — highest severity.

**Check the details:**
- Do filenames match the naming settings?
- Do folder names match expected patterns?
- Are duplicates handled correctly?

### Lens 3: Is It Hard to Use?
> "I got it done, but should it have been that difficult?"

Friction that doesn't cause failure but wastes time or causes confusion: excessive scrolling, multiple clicks where one should suffice, labels that are technically accurate but not intuitive, no visual feedback after an action, settings and their preview not visible at the same time, error messages that describe the error but not the fix.

**Report UX friction even when the feature technically works.**

### Lens 4: Does It Make Sense?
> "This works, but should it exist? Does it contradict something else?"

Requires understanding the product holistically: redundant controls (two UI elements doing the same thing), contradictory settings, orphaned features, missing connections, naming inconsistencies, broken mental models.

**Ask: "If I were explaining this to a new user, would I have to say 'ignore that' or 'that's confusing but...'?"**

### Lens 5: What Else?
> "What hasn't been tested that should be?"

Different datasets, scale (10 items vs 1000), sequence (run twice — duplicates handled?), recovery (interrupt mid-operation), empty states (zero input), adversarial inputs (special characters, extreme lengths, missing metadata).

---

## Insider Testing Protocol — 8 Phases

### Phase 1: Goal Verification — Primary Dataset
**This is the most important phase. Do this first.**

Run the app's complete workflow end-to-end with the primary test dataset. Then:

1. **Leave the app.** Open Finder (or whatever shows the output).
2. **Verify the output** against the Goal Verification Checklist from INSIDER_GOALS.md.
3. **Investigate every failure** — not just count them, understand each one.
4. **Reconcile numbers** — input = output + review + excluded. Any missing = critical.
5. **Document findings** as OUTCOME entries.

```
TIME ALLOCATION: Spend 25% of total testing time on this phase.
This is where the highest-value findings come from.
```

### Phase 2: Failure Deep-Dive
**Do not skip this phase.** Most testers verify success. Insiders investigate failure.

For each item in the failure/review bucket:

| Photo | Why Here? | Correct? | Root Cause | Actionable? |
|-------|-----------|----------|------------|-------------|

For name cards / detection failures:
1. Open the item — what does it look like?
2. Which format is it?
3. Can a human interpret it? If yes → engine should have caught it
4. What text would OCR/processing produce? Is the parsing logic handling it?
5. Screenshot for the bug report

### Phase 3: Goal Verification — Second Dataset
Run the full workflow again with a **different** test dataset. Purpose: surface data-dependent issues that Dataset 1 doesn't trigger. Repeat Phase 1 and Phase 2 against the second dataset's output, then compare.

### Phase 4: Settings Impact Verification
Change key settings (from INSIDER_GOALS.md > Critical Settings) and verify they affect the output correctly.

For each critical setting:
1. Change the setting
2. Run the workflow (or relevant portion)
3. Verify the output reflects the setting change
4. Check the Live Preview if one exists — does it match reality?

**Key principle: the test is in the output, not the UI.** If the Live Preview says one thing but the actual output files say another — that's the real bug.

### Phase 5: Screen-by-Screen Element Audit
Now do the detailed element verification. But augmented with all 5 lenses:

| Element | Works? | Affects output? | Easy to use? | Makes sense? | Notes |
|---------|--------|----------------|--------------|-------------|-------|

For settings and controls, always ask:
- What does changing this actually DO to the final output?
- Can I verify the effect by checking the output?
- Does this duplicate another control?
- Would a user understand this without documentation?

### Phase 6: Edge Cases & Stress
Targeted tests for boundary conditions: re-run with same data (duplicate handling), empty input, only detection items with no data items, only data items with no detection items, change settings between steps, items with no metadata, special characters, very long names.

### Phase 7: Report
Compile findings organized by **lens**, not just by screen.

### Phase 8: Evolve — Post-Flight Q&A With Human

**After delivering the report, the tester asks the human what to test next.**

The tester shares a brief summary, then:

> "Here's what I found this flight: [summary].
>
> Based on what I saw, I think we should also test [suggestion].
>
> Is there anything else you'd like me to focus on next time?"

New testing goals get appended to `INSIDER_GOALS.md`:

```markdown
### Flight [N] Additions — [date]
Source: Post-flight Q&A

New testing goals:
- [what the human asked for]
- [what the tester suggested and human approved]

Updated priority:
- [any shift in focus for next flight]
```

**The skill grows with every flight.** After 3-4 cycles, INSIDER_GOALS.md becomes a rich, project-specific testing playbook.

---

## Reporting Format

### OUTCOME Findings (highest priority)
Results of inspecting actual output.

```
OUTCOME-XXX: Title
  Lens: Goal Verification
  Dataset: which test data
  Location: where in output (Finder path, folder, file)
  Finding: what you observed
  Expected: what should have been there
  Root Cause: why this happened (if determinable)
  Severity: [Correct | Minor Inaccuracy | Wrong Result | Data Loss]
  Evidence: screenshot or file listing
```

### Bug Classification
```
BUG-XXX [Severity]: Title
  Lens: [Works / Outcome / UX / Logic / Edge]
  Screen: where it's triggered
  Steps: how to reproduce
  Expected: what should happen
  Actual: what does happen
  Impact: how this affects the user's goal
  Output verification: did this affect the actual output? (check output)
```

### Notes Classification
```
NOTE-XXX: Title
  Lens: [UX / Logic / Edge]
  Screen: where
  Observation: what you noticed
  Reasoning: why this matters (think it through, don't just report)
  Suggestion: what to consider changing
```

---

## Risk Map — Where to Spend Testing Time

Adapted from James Bach's Heuristic Test Strategy Model (HTSM). Before testing, the Insider builds a risk map: which product elements carry the highest risk, and which quality criteria matter most for each.

**Product Elements × Quality Criteria = Test Priority**

```
Example:
| Product Element        | Accuracy | Data Safety | Performance | Usability | Risk |
|------------------------|----------|-------------|-------------|-----------|------|
| Name card detection    | CRITICAL | -           | Medium      | -         | HIGH |
| Photo grouping (gap)   | HIGH     | -           | Low         | Medium    | HIGH |
| Folder matching (fuzzy)| HIGH     | Medium      | Low         | -         | HIGH |
| File copy + duplicates | Medium   | CRITICAL    | Medium      | -         | HIGH |
| Review assignment UI   | -        | Low         | -           | HIGH      | MED  |
| Settings persistence   | Low      | -           | -           | Medium    | LOW  |
```

**How to use:**
- HIGH risk elements get tested first and deepest (Phases 1-2)
- CRITICAL quality criteria get verified against actual output, not just UI
- LOW risk elements get checked during the element audit (Phase 5), not before

---

## Session Structure — Time-Boxing

Each testing phase is a focused session with a charter, time box, and debrief.

**Why time-boxing matters for AI testers:** Without limits, AI agents can spend 2 hours clicking through Settings tabs while spending 0 minutes checking the output folder. Time-boxing prevents this.

### Phase Timing (approximate):
| Phase | % of Total Time | What |
|-------|-----------------|------|
| Phase 0 | Setup (once) | Goal Discovery Q&A with human |
| Phase 1 | 25% | Goal Verification — Dataset 1 (output in Finder) |
| Phase 2 | 15% | Failure Deep-Dive (review/failure investigation) |
| Phase 3 | 20% | Goal Verification — Dataset 2 |
| Phase 4 | 10% | Settings Impact (change setting → verify output) |
| Phase 5 | 15% | Element Audit (5-lens) |
| Phase 6 | 5% | Edge Cases |
| Phase 7 | 5% | Report |
| Phase 8 | 5% | Evolve — Post-flight Q&A with human |

**Note: 60% of time is on outcome verification (Phases 1-3). Only 15% is on element clicking (Phase 5). This inversion is the whole point of Insider testing.**

---

## Anti-Patterns — What Insider Testing Is NOT

1. **Not a screenshot tour.** Screenshots of every screen saying "looks good" is not testing.
2. **Not element bingo.** Checking "button exists ✓" without evaluating what the button actually does to the output is Cold-tier work wearing an Insider hat.
3. **Not spec compliance only.** The spec can be wrong. The spec can have redundant features. The Insider tests the *product*, not just the spec.
4. **Not UI-only.** If the app produces files — **open the files.** The output is the ground truth.
5. **Not single-dataset.** One test run with one dataset is a demo, not a test.
6. **Not "it didn't crash."** Completing without errors is the bare minimum.
7. **Not "count matches."** 37 patients found and 37 folders exist. Great. But are the RIGHT items in the RIGHT folders?
8. **Not reporting without reasoning.** "Preview doesn't update" is shallow. "Preview doesn't update for separators — but Name Order radio is redundant with token chip ordering, so that's a design issue not a bug" is an Insider finding.
9. **Not log-and-move-on.** (AI-specific trap) One investigated bug that reveals a pattern is worth more than 10 surface-level observations.

---

## Integration Points

### Files this skill creates:
- `FLIGHT_DECK/INSIDER_GOALS.md` — generated during Phase 0, project-specific, evolves each flight

### Files this skill references:
- `CLAUDE.md` / `PRD.md` — full project spec
- `FLIGHT_DECK/FLIGHT_PLAN.md` — current status, prior findings
- `FLIGHT_DECK/PREFLIGHT_CHECK.md` — testing depth config

### Referenced by:
- `AUTOPILOT.md` — Phase 0 Q&A as Step 1.5 in mandatory setup
- `TEST_FLIGHT_PROTOCOL.md` — as the method for Insider tier testing
- `PREFLIGHT_CHECK.md` — as a testing depth option
- `PILOT_HANDBOOK.md` — Insider tier description references this skill

### The Lifecycle

```
Phase 0 (once)          Phase 1-7 (each flight)         Phase 8 (each flight)
┌─────────────┐         ┌─────────────────────┐         ┌──────────────────┐
│ Q&A with    │         │ Test → Verify →     │         │ Report findings  │
│ human       │────────▶│ Investigate →        │────────▶│ Suggest next     │
│ (6 questions)│        │ Report               │         │ Ask human        │
└─────────────┘         └─────────────────────┘         └────────┬─────────┘
      │                          ▲                               │
      │                          │                               │
      ▼                          │                               ▼
┌─────────────┐                  │                      ┌──────────────────┐
│ INSIDER_    │                  │                      │ Update           │
│ GOALS.md   │──────────────────┘                      │ INSIDER_GOALS.md │
│ (created)   │                                         │ (evolved)        │
└─────────────┘                                         └──────────────────┘
```

---

*Insider Testing Skill v1.0 — Test Pilot Loop — Flight Deck*
*Outcome-focused. Logic-driven. The test is in the output, not the UI.*
