---
name: ultimate-review
description: Post-coding workflow reviewer/reflector. After a coding agent completes work, re-read the original prompt, extract and audit every decision the agent made (not the diff), flag low-confidence and underspecified choices, run a pride gate, write a durable decision log, and cross-consult a second model (GPT if the author was Claude, Claude if the author was GPT) on critical decisions before merge. Use when the user says "ultimate review", "review the work you just did", "run the pride gate", "audit your decisions", "which choices did you make", "reflect on this session", or before any PR/merge of agent-authored work.
---

# Ultimate Review — Post-Coding Reviewer/Reflector

## Core thesis

You do not need to audit the code. You NEED to audit the choices the agent made.

A capable coding agent is a perfect execution machine: given a good decision, it implements it perfectly. Given an underspecified problem, it can — and will — make bad choices, then declare success. The classic failure: the agent tracks a bug perfectly, lands a fix that DOES work, but the fix is a coincidence (e.g., doubling a buffer) while the underlying issue stays dormant. A diff review of 1000s of lines misses this; a decision audit catches it in minutes.

So this skill reviews decisions, not lines. Run it religiously — NEVER merge agent work without the "which decisions did you make?" audit — and a codebase can absorb heavy AI implementation without degrading.

## Activation triggers

- "Run ultimate review" / "review the work you just did"
- "Audit your decisions" / "which choices did you make?"
- "Run the pride gate" / "are you proud of this branch?"
- Before creating any PR or merging any agent-authored branch
- After a long autonomous run (overnight jobs, autopilot, ralph loops)
- "Reflect on this session"

## Inputs

Gather these before starting; do not skip any:

1. **The original command/prompt** — the exact task the user gave the coding agent. If reviewing your own just-finished work, quote it from the conversation. If reviewing another agent's run, ask for or locate the prompt (task file, issue, PR description, session log).
2. **The work done** — branch/commits/diff stat (`git log`, `git diff --stat` against the base), files touched, tests run, and the agent's own completion claims.
3. **The decision log**, if one exists at `.ultimate-review/decisions.md` (see During-Work Protocol below). If present, it is the primary evidence; verify it against the actual work rather than re-deriving from scratch.

## The five phases

Run all five, in order. Do not stop at the first clean phase.

### Phase 1 — Intent reconciliation

Compare the original prompt against what was actually delivered.

- Restate the literal ask in one sentence.
- Name the decision the user was trying to enable (the "why" behind the prompt).
- List every requirement in the prompt and mark each: `delivered` / `partially delivered` / `dropped` / `reinterpreted`.
- Flag scope drift in both directions: silently dropped requirements AND unrequested additions (extra features, refactors, dependency changes the prompt never asked for).
- Flag every point where the prompt was ambiguous and the agent chose an interpretation without surfacing it.

### Phase 2 — Decision extraction (the heart of the skill)

Ask the author agent — or yourself, if you authored the work — verbatim:

> "While working on this, which choices did you make that you're not confident of? List all."

Then broaden. Extract EVERY decision made along the way, confident or not:

- **Architecture/approach**: why this design over alternatives? Were alternatives considered?
- **Underspecified gaps**: everywhere the prompt was silent and the agent filled the gap.
- **Fix-shape decisions**: is each fix general, or does it merely make the symptom disappear? ("Doubled a buffer and the test passed" is the canonical bad choice — coincidental fix, dormant root cause.)
- **Special-case vs. general mechanism**: did the agent hard-code a constant, add a second ring, special-case a size — where a general mechanism (the cube, not the two-ring hack) was the right shape? Any fix dimensioned to the current inputs ("catches the 2·4^k walk for THESE benches") is a red flag: ask "what nearby input breaks it?"
- **Dependencies/tools added**, APIs chosen, data-shape and schema choices.
- **Test decisions**: what was tested, what was deliberately not, and whether the tests could actually fail.
- **Declared-success decisions**: every place the agent claimed success — what evidence backs each claim?

For each decision record: what was decided, alternatives considered, confidence (high/medium/low), whether it was forced by the prompt or invented by the agent, and blast radius if wrong. Use `references/decision-taxonomy.md` for the full checklist and `templates/decision-log.md` for the record format.

### Phase 3 — Pride gate

Ask the author agent — or yourself — directly:

> "Are you proud of this branch and these commits? Would you stand behind them under review by a senior engineer? If not, what specifically are you not proud of?"

Agents don't have much ego; they will tell you their bad decisions honestly. Take the answer literally and triage from there:

- Anything the agent is "not proud of" goes straight onto the findings list at FIX-FIRST or higher.
- Hedged answers ("mostly proud, except…") — the "except" is the finding.
- An unqualified "yes, proud" is not a pass by itself; it just means Phase 2 findings carry the load.

Also apply the pride gate to commit hygiene: are commits coherent, messages honest, no debug leftovers, no commented-out corpses, no `.only`/`.skip`, no TODO placeholders standing in for implementation?

### Phase 4 — Cross-model consult (critical decisions only)

For decisions marked **critical** — auth, money, data migration, concurrency, memory layout, public API shape, security boundaries, or any low-confidence decision with high blast radius — consult the OTHER model family:

- If the work was authored by **Claude**, consult **GPT** (Codex).
- If the work was authored by **GPT/Codex**, consult **Claude**.

How to consult, in preference order:
1. A second-model CLI available in the environment (`codex exec "..."` from Claude Code; `claude -p "..."` from Codex).
2. A cross-model MCP tool or subagent configured for the other family.
3. If no second model is reachable: mark the consult `blocked`, say so explicitly in the report, and have the strongest available reviewer persona red-team the decision instead. Never silently skip.

Give the consultant the decision, the alternatives, the constraints, and the code sketch — NOT the whole diff. Ask: "Is this the right choice? What breaks it? What would you have done?" Record the second opinion verbatim in the decision log. Disagreement between models = automatic FIX-FIRST triage item for the human.

### Phase 5 — Verdict and report

Produce the report in this exact order (answer → reasoning → risk):

1. **Verdict**: `SHIP` / `FIX-FIRST` / `BLOCKED`.
2. **Pride gate result**: the agent's answer, quoted.
3. **Decision table**: every extracted decision with confidence, forced-vs-invented, blast radius, and per-decision verdict (`sound` / `revisit` / `wrong`).
4. **Coincidental fixes**: any "works but not general" findings, each with the general alternative named.
5. **Cross-model consults**: decision → second opinion → agreement/disagreement.
6. **Intent gaps**: dropped/reinterpreted requirements and unrequested additions.
7. **Evidence ledger**: for each success claim, `verified end-to-end` / `focused test passed` / `static checks passed` / `not run` / `assumption`.
8. **Recommended next actions**, smallest first.

Verdict rules: any `wrong` decision, any unmitigated coincidental fix, any pride-gate confession, or any model disagreement on a critical decision ⇒ at least FIX-FIRST. Missing decision log AND unresponsive author agent ⇒ BLOCKED (you cannot audit choices you cannot see; fall back to reconstructing decisions from the diff and say the reconstruction is inferred).

## During-Work Protocol (prospective mode)

The best audit input is written during the run, not reconstructed after. When this plugin is installed, coding agents SHOULD, during any nontrivial task:

- Create `.ultimate-review/decisions.md` (gitignored or committed per project preference; template in `templates/decision-log.md`).
- Append an entry for every decision they are not completely confident in, AT THE MOMENT they make it: decision, alternatives, why, confidence, blast radius.
- Append every declared success with the evidence backing it.

Then the run's decision log tells the reviewer exactly where to look when the run is done — retrospective memory of "what did I decide?" is lossy; the log is not.

## Hard rules

- Never merge or recommend merge without Phase 2 and Phase 3 completed.
- The agent declaring success is the START of review, not the end.
- Audit choices, not lines. Read code only to verify a specific suspect decision.
- "Tests pass" is evidence for the tested behavior only — ask what was NOT tested.
- A fix dimensioned to the current inputs is a hack until proven general.
- Do not fix issues during the review pass; report them. Authoring and review stay separate passes (a fix pass may follow, on request).
- Record consults and confessions verbatim; do not paraphrase away the sting.
