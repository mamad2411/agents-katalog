---
name: persona-experiments
description: >
  Designing experiments that validate the buyer persona and value propositions in the
  Ananas-Agency model. Use this skill when the user wants to: validate
  a buyer persona, test value propositions on real customers, check
  whether customers' problems are real, design tests of sales hypotheses,
  create a segment validation plan. Trigger: "experiments", "persona validation",
  "test the persona", "are the problems real", "hypothesis testing", "value
  validation", "check the segment", "test plan", "buyer persona experiments".
---

# Experiments Validating the Buyer Persona and Value Propositions (Ananas-Agency)

## Goal

Starting from the buyer persona and the value propositions, validate the key hypotheses in two waves: run a **first pass of in-session experiments right now** (the assistant tests what it can from public data and persona role-play), then hand the user a **one-week field plan** (5 working days, max 2h per day) to confirm with real customers. Together they confirm or disprove the key hypotheses, before the company invests in prospecting, marketing, and sales.

## Why run experiments

A buyer persona and value propositions are HYPOTHESES. Until you put them in front of real customers, they remain a set of educated guesses. Companies that build their go-to-market on unvalidated hypotheses burn months and budget on messaging that doesn't resonate, segments that don't buy, and value that customers simply don't care about.

## Prerequisites

**Experiments require TWO completed documents:**
1. **Buyer Persona** — without it, you don't know who to test
2. **List of value propositions (PSO (Problem · Solution · Outcome))** — without it, you don't know what to test

If the user is missing one or both, let them know:
> "Experiments require a completed buyer persona and a list of value propositions (PSO (Problem · Solution · Outcome)). Without them I can't design the tests. Which of these documents would you like to create first?"

Do not design experiments unless both documents exist.

## 5 areas of hypotheses to test

Every buyer persona and PSO (Problem · Solution · Outcome) list contains hypotheses across 5 areas. Testing priority runs from the most important down:

### 1. Problems and challenges (HIGHEST PRIORITY)
**Hypothesis:** "Segment X genuinely has problem Y."
If the problems aren't real, the entire persona collapses. We test this ALWAYS and FIRST.

### 2. Value propositions (HIGHEST PRIORITY)
**Hypothesis:** "Segment X genuinely needs and values benefit Z." The value can be referred to by its ID (e.g. "Segment X really needs and appreciates value Z (cite its ID, e.g. PV-03)").
If the value doesn't resonate, the company has nothing to sell. We test this ALWAYS, alongside the problems.

### 3. Segment
**Hypothesis:** "Segment X exists in sufficient numbers and is reachable."
If the segment is too small or unreachable, nothing else matters.

### 4. Decision-making roles
**Hypothesis:** "A person in role Y genuinely takes part in the buying process."
If we're talking to the wrong person, we're wasting time.

### 5. Buying process
**Hypothesis:** "The segment buys the way we've described."
If the actual process differs, our prospecting and marketing will be built on the wrong assumptions.

## The framework for the weekly plan

**Constraints:**
- 5 working days (Monday to Friday)
- Max 2h of effort per day
- Max 10h total across the whole plan
- The experiments must be simple to run: no specialized tools, no budget (or only a minimal one)

**Structure of the week:**
- **Days 1-2:** Prepare materials + run the first experiments (interviews, surveys)
- **Days 3-4:** Run the experiments (calls, test campaign, analysis)
- **Day 5:** Analyze the results + draw conclusions + refine the persona and value propositions

## Conversation flow

> **How to run this session — read before you start.** Treat this as a **discovery conversation**: a guided working session with the user, closer to a strategy call or workshop than a questionnaire. The entire value of the result comes from what you draw out of them, so slow down and dig in. A rushed exchange that jumps straight to a draft produces a generic, forgettable experiment plan; a proper working session produces one grounded in the user's real business.
> - **Open first, then move to choices — keep it balanced.** Make the *first* question on a topic open (*"before I ask specifics, tell me in your own words how you see this"*), then **stop asking everything open**: once you see the shape, switch to targeted questions and fill only genuine gaps with more open follow-ups.
> - **Prefer selectable answers to keep the pace.** Whenever a question has a small, knowable set of likely answers, present them as a **pickable list** (the user selects, and can add their own) rather than another open prompt — an all-open interview drags; balance one open opener with quick pickable questions. Always still push for the specifics behind whatever they pick.
> - **Pace and depth.** Work through the topics as a genuine back-and-forth, asking **2–3 questions at a time** so you never overwhelm the user. Across the whole session expect to ask roughly **6–10 questions** before you have enough to build. If you catch yourself moving to a draft after only two or three answers, you have stopped too early. There is almost always more to uncover, and the difference shows in the output.
> - **Cover the checklist before you build.** Do not move on to choosing the experiment methods (Step 3) or to producing the deliverable until every item in **Required inputs** below has genuinely been captured, or the user has explicitly chosen to skip it, or told you they don't know. A missing item is a gap to close in conversation, not a blank for you to quietly fill on their behalf.
> - **Push past the first answer.** People give you the surface answer first — "we're faster", "better service", "good quality". Treat every vague or general reply as an invitation to go one level deeper: ask for a concrete example, a number, a percentage, an amount in €, a timeframe, or the specific situation that prompted it. Stay on a single point, following up, until the answer is specific enough to actually act on. This is where a good session earns its value.
> - **Ask before you assume.** Never invent a fact the user could have given you. Your default is always to ask them first. If the user genuinely cannot answer, or would rather not, you may fill the gap yourself, but you must label it clearly as **[Assumption]** in the output and flag it so they can confirm or correct it later.

### Required inputs — capture before drafting
Check each off (or mark "skip") before Step 3 (choosing methods):
- [ ] Buyer Persona + PSO (Problem · Solution · Outcome) list received
- [ ] Hypotheses extracted across all 5 areas — problems, value, segment, roles, process
- [ ] Each hypothesis tagged — certain / probable / risky
- [ ] Riskiest hypotheses identified together with the user
- [ ] User's real constraints known (customer base? ad budget? time?) so the methods actually fit

### Step 1: Collect the input documents

Ask the user for the buyer persona and the PSO (Problem · Solution · Outcome) list. If they're missing, stop the process.

### Step 2: Extract the hypotheses to test

From the buyer persona and the PSO (Problem · Solution · Outcome), pull out a list of specific hypotheses, one set per area — see the 5 areas above.

Assign each hypothesis a sequential ID as you extract it: **`H1`, `H2`, `H3`… (H = Hypothesis)**. These IDs label the hypotheses everywhere in the plan (the schedule, the success criteria, the in-session findings, and the results table), so the user can always tell which hypothesis a row refers to.

**Show the user the complete list first — never jump straight to prioritizing.** Present every hypothesis you extracted as a visible, grouped list, each line carrying its **ID *and* its full statement** (grouped by the 5 areas), so the user can see exactly what each `H#` means. For example:

> **Problems & challenges**
> - **H1** — [full hypothesis statement]
> - **H2** — [full hypothesis statement]
>
> **Value propositions**
> - **H3** — [full hypothesis statement]
> …

Then ask the user to **add, edit, or remove** any hypotheses before going further. Only once the list is agreed do you ask them to prioritize: *"Which of these are you least sure of? Point to them by what they say (or the H-number) — those get tested hardest."* **Never present the prioritization choice as bare `H1 / H5` labels with no statement attached** — always repeat the full hypothesis text alongside each ID.

Tag each hypothesis as:
- **Certain** — the user is confident (e.g. backed by CRM data)
- **Probable** — the user believes it but has no hard evidence
- **Risky** — the user isn't sure themselves

Focus the experiments on the **probable and risky** hypotheses. Don't test the certain ones (unless the user wants to).

### Step 3: Choose experiment methods

Based on the hypotheses to test, select the methods. For the method catalog, see [references/rules-experiments.md](references/rules-experiments.md).

Selection rules:
- The catalog has two kinds of method: **field** methods the user runs over the week (1–8), and **in-session** methods the assistant runs now (9–13). For each key hypothesis (problems, value), pick **at least one of each**: an in-session method for a read *today*, and a field method for real validation.
- Label every chosen method **[in-session]** or **[field]** in the plan, so the user knows what happens now versus what's homework.
- Every experiment must have a clear success criterion
- Prefer methods that give DIRECT feedback (a conversation > a survey > data analysis)
- Match the field methods to what the user can realistically do (not everyone has a customer base, not everyone has an ad budget)

### Step 4: Spread across 5 days

Lay the experiments out into a weekly plan. Rules:
- Day 1 covers preparation (writing questions, creating materials)
- The hardest experiments (phone calls) fall on days 2-4
- Day 5 = analysis and conclusions
- No day exceeds 2h
- Give an estimated time per task

### Step 5: Define success criteria

For each experiment, specify:
- What we measure
- What result = hypothesis confirmed
- What result = hypothesis refuted
- What result = ambiguous (more data needed)

For the thresholds, see [references/rules-experiments.md](references/rules-experiments.md), section "Validation thresholds".

### Step 6: Run the in-session experiments now

Before delivering the plan, actually **run the [in-session] methods you selected (9–13)**. This is the part that doesn't wait for the week. For the top hypotheses (problems and value):
- Run the chosen methods — offer/website teardown, desk market-sizing, search & language scan, competitor desk research, and/or a persona role-play.
- Report each result against its success criterion and tag it a **directional (in-session) signal**.
- Apply the provisional write-back from [references/rules-experiments.md](references/rules-experiments.md), section "Results intake & write-back": an in-session confirmation stays `Source: hypothesis (in-session signal: positive)`; it is NOT yet `validated`; an in-session negative flags the value to sharpen or re-test.

Then tell the user plainly what you already learned now, and what still needs the field plan to confirm.

### Step 7: Deliver the plan as files

Generate TWO files (`.md` and a styled, self-contained `.html`), including the **in-session findings** from Step 6 and the field plan for the week. For the format, see [references/rules-experiments.md](references/rules-experiments.md), section "Output file format". The `.html` must follow the shared navigation rules: cross-links to the other deliverables, hover hints on short terms, and the **Next** button to the next file in the sequence (see the reference's Output file format).

Save both files and share them with the user for download.

### Step 8: Capture results and close the loop

The plan is only half the value; the other half is feeding the results back into the strategy. Results arrive in two waves: the **in-session** signals from Step 6 (now), and the **field** results when the user returns after the week. Capture both with the structured intake in [references/rules-experiments.md](references/rules-experiments.md), section "Results intake & write-back": ask the user to report each hypothesis as `H# | method | evidence | confirmed/refuted/unclear`, interpret it against the validation thresholds, then apply the write-back:

- **Update the persona and PSO list** with what the experiments revealed (sharper problems, corrected segment, new objections, roles that don't actually decide).
- **Re-score any value whose evidence changed** — recompute Score = Problem weight + Outcome magnitude (max 20). Keep each value's `PV-/SV-/AV-` ID **unchanged** even if the new score would re-order it; the IDs are stable anchors that Skills 3, 5, 6, and 7 reference. IDs identify a value, they are **not a live ranking**, so after re-scoring, rank by Score, not by the ID number.
- **Update each value's `Source` tag**: `validated` **only** if a **field** experiment (methods 1–8) confirmed it; an **in-session** confirmation stays `hypothesis` with an `(in-session signal: positive)` note; `hypothesis` if it was refuted or untested. This is what later skills read to know whether they're building on tested ground.
- **Write the changes back into the value list itself** — apply the re-scores and `Source` flips to the **Value Proposition** deliverable (`value-propositions.md` and the dossier's Value Propositions section), not only to this experiments output. Later skills read `Source` and Score from the value list, not from the experiment log, so the value list must be the current source of truth after validation.

This closes the "living document" loop the Buyer Persona skill promises, and is what lets the Buying Process (Skill 5) and Missing Value Propositions (Skill 6) skills build on validated inputs rather than guesses.

## Add to the Strategy Dossier

This suite runs as one continuous session. **Deliver only your own two files now** — the **Strategy Dossier** is an **internal running document**, not delivered until the end, so don't create or hand over a dossier file mid-session. Update that internal dossier in **two** places:
1. Add or refresh the **Validation results** section — what was tested and the `validated` / `hypothesis` status of each key input.
2. **Refresh the Value Propositions section** — apply the `Source` flips and re-scores from Step 8 there too, so the value list in the dossier reflects the validated state (not just the Validation section).

Full format: [dossier-format.md](../dossier-format.md).

## Critical rules

1. **No buyer persona and PSO (Problem · Solution · Outcome), no experiments.** Don't design anything without both documents.
2. **Always test problems and value.** They're the highest priority; everything else is secondary.
3. **Min. 2 methods per key hypothesis.** One method isn't enough to be confident.
4. **The plan must be realistic.** 5 days × 2h = 10h. Don't plan beyond that. The user has other responsibilities too.
5. **A success criterion with EVERY experiment.** Without one, you can't tell whether the test succeeded.
6. **A direct conversation beats everything else.** The most valuable experiment is a conversation with a real customer from the segment.
7. **Keep the methods simple.** The experiments must be doable without specialized tools and without a budget.
8. **A discovery conversation, not a form.** Follow the session guidance at the top of the conversation flow: cover the Required-inputs checklist before you build, push every vague answer toward a specific, and label any gap you fill yourself **[Assumption]**.
9. **Run an in-session first pass — but don't over-claim it.** Always run the in-session methods (9–13) during the session for a read today, and label every method **[in-session]** or **[field]** in the plan. A value is only `validated` after a **field** experiment confirms it, never on in-session signal or role-play alone.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
