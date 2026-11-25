---
name: upskill
description: Use as the canonical way to create AND continuously improve skills. Triggers when turning a proven/repeated workflow into a skill, creating a skill from scratch, "make this a skill", "skillify this", "/upskill <name>"; and when capturing what a skill learned after a run, onboarding a skill to the documentation + improvement standard, setting up a learnings wiki, or deciding whether a skill's recurring decision should be retrained by optimise-skill. Prefer this over hand-rolling a skill so logging and improvement are wired in from day one.
---

# upskill

## Overview

upskill is the canonical way to both **create** a skill and **keep improving** it. A skill is born already wired to record what it does and learn from it, and every run after that compounds what it learned. (Karpathy's framing: *stop re-deriving, start compiling.*)

upskill owns the **memory, the routing, and the safety rules**. It does not reimplement authoring, evaluation, or retraining — it delegates:
- **`superpowers:writing-skills`** — the write-the-failing-test-first authoring discipline.
- **`skill-creator`** — the eval harness and `description:` triggering optimisation.
- **`optimise-skill`** — retrains a skill's judgment against labelled examples, behind a held-out test.
- **Autonomy governance** — reuses proven patterns (revertibility as the line, allow-list not danger-list) rather than inventing its own. See Autonomy section.

What's genuinely upskill's own: (1) the **staging contract** for creating skills, and (2) the **learnings wiki + the end-of-session retrospective** that turn experience into a permanent reflex.

## Four modes — create, onboard, improve, or retro

(This is *what* it does. *How autonomously* it acts is a separate choice — ask-me-first vs just-do-it — see Autonomy.)

| | **Create** | **Onboard** | **Improve** | **Retro** |
|---|---|---|---|---|
| Trigger | "make this a skill", no skill exists | `/upskill <skill>` where skill exists but has no `references/learnings.md` | `/upskill <skill>` where skill already has wiring | `/upskill retro` at end of session |
| Does | author + stage/test/approve + wire in logging | create improvement infrastructure + run first retrospective | sense → reflect → improve | retrospective for ALL onboarded skills used this session |
| Ends at | a committed skill that's already instrumented | skill wired for improvement, first journal entry written | updated journal + lessons, or a graduated SKILL.md edit / retrain handoff | journal entries + lessons for every skill that ran |

**Detection is automatic.** When you run `/upskill`:
- `/upskill retro` (no skill name) → **Retro** — scans session, finds which onboarded skills ran, does a retrospective for each
- `/upskill <skill>` where skill doesn't exist → **Create**
- `/upskill <skill>` where skill exists, no `references/learnings.md` → **Onboard** (then Improve if there's a session to reflect on)
- `/upskill <skill>` where skill exists with wiring → **Improve**

All four end the same way: every skill touched is set up to keep improving.

---

## Retro — end-of-session retrospective for all skills

Run `/upskill retro` at the end of any session. It does not target a single skill; it finds every onboarded skill that ran.

1. **Detect which skills ran.** Scan the session for skill invocations (loaded via the Skill tool, or invoked by name in slash commands). Build a list of skill names.
2. **Filter to onboarded skills.** For each skill that ran, check if `<skill>/references/learnings.md` exists. Skip skills without the improvement wiring (they need `/upskill <skill>` to onboard first). Surface any un-onboarded skills that ran: "These skills ran but aren't onboarded yet: X, Y. Run `/upskill <skill>` to set them up."
3. **Run the retrospective for each onboarded skill.** For each skill, walk the structured checklist (section 2: corrections, successes, outputs, procedure, skill-specific checks from `retrospective-checklist.md`). Independently review the session trace for that skill's portion of the work. Do not rely on a summary; read what actually happened.
4. **Write artifacts per skill.** For each skill:
   - Append a run-journal entry to `<skill>/references/run-journal.md`
   - Write new learnings to `<skill>/references/learnings.md` as `proposed`
   - Flag retrain candidates if a judgment recurred
5. **Cross-skill patterns.** After all per-skill retros, check: did the same correction apply across multiple skills? If so, put the learning in EVERY relevant skill's `learnings.md` (duplication is fine; each skill reads its own file at run start). Use `Related:` wikilinks to connect the entries across skills so they can be maintained together. Project-wide learnings (`<project-config>/learnings.md`) are only for patterns genuinely outside any skill's scope: general session workflow, tool conventions, cross-cutting process rules for ad-hoc work that no skill covers.
6. **Present a summary.** One block per skill: what was captured, how many learnings, any retrain flags, any un-onboarded skills that should be set up.

---

## Onboard a skill — wire the improvement infrastructure

For skills that exist but were built before upskill (or without the improvement wiring). Onboard creates the infrastructure, then hands off to Improve if there's a session to reflect on.

1. **Read the skill's SKILL.md.** Understand what the skill does: what domain it operates in, what decisions it makes, what outputs it produces, what data sources it uses, what its phases/steps are. This understanding drives step 4.
2. **Create `references/learnings.md`.** Empty wiki with the standard header. Will be populated by the first retrospective.
3. **Create `references/run-journal.md`.** Empty journal with the standard header.
4. **Create `references/retrospective-checklist.md`.** This is skill-specific and requires understanding the skill's domain. Read SKILL.md and ask:
   - What are the skill's **key decisions**? (e.g. a triage skill: bug-vs-working-as-designed diagnosis. a ticket-implementing skill: root cause identification. a drafting skill: tone and accuracy.)
   - What **data sources** should verify those decisions? (e.g. a triage skill: analytics + database + screenshots. a ticket-implementing skill: test output + code trace. a drafting skill: a QA reference + the customer's actual message.)
   - What are the skill's **outputs** that could be wrong? (e.g. a triage skill: drafts, tickets, diagnoses. a ticket-implementing skill: code changes, test coverage. a drafting skill: email text.)
   - What **ordering constraints** does the skill have? (e.g. a triage skill: investigate before drafting. a ticket-implementing skill: failing test before fix.)

   Write 3-6 yes/no check questions that a retrospective can walk. Each check should catch a specific failure mode. Example for an investigation skill: "Was each diagnosis verified against user data before being proposed?" Example for a coding skill: "Was a failing test written before the fix?"
5. **Add "read learnings" instructions to SKILL.md.** In the skill's preflight or startup phase, add two reads:
   - `references/learnings.md` for per-skill process learnings from prior runs
   - `<project-config>/learnings.md` for project-wide process patterns and safety constraints (domain-specific rules that apply across all skills in this project)
   
   Both use the same entry format. Per-skill learnings are about how to run THAT skill better. Project-wide learnings are about how to work in THIS project (safety constraints, tool conventions, domain rules). Both are read at run start so corrections take effect immediately.
6. **Run the first retrospective** if there's a current session to reflect on. Otherwise, the infrastructure is ready for the next run.

---

## Create a skill — the staging contract

**Never write a half-broken skill to disk.** A broken skill in the list is worse than none — agents reach for the wrong tool. So everything stages first, tests gate, you approve, the commit is atomic; a failed test or a "no" throws the staging copy away.

1. **Name it.** Pull the workflow from the conversation/proven run. Propose a name (verb-first, hyphens, ≤32 chars), 3–5 trigger phrases a real user would say, and where it lives (global vs project). Check for a name collision first.
2. **Author via `writing-skills` (failing test first).** Watch it fail without the skill, write the minimal skill that fixes those exact failures, close loopholes. Don't skip the baseline — "clear to you ≠ clear to another agent."
3. **Stage, don't commit.** Write the draft to a temporary folder, never the final path.
4. **Test the staged copy.** Tests must check substance, not just "it didn't crash." Two fix-retries max, then discard.
5. **You approve.** Show the staged skill; offer commit / review-first / discard. No silent promotion, ever.
6. **Atomic commit or clean discard.** Yes → move to the final path in one step. No/fail → delete the staging folder; nothing partial lands.
7. **Wire in logging** (the improvement loop, below) before calling it done.

(The lineage of this contract is gstack's `/skillify`; upskill generalises it to any skill.)

---

## Improve a skill — sense, reflect, improve

Three jobs, each different. Two of them improve the skill; the first one just watches.

### 1. Sense (automatic, every run — the eyes)
As a skill runs, it quietly records what happened: the decisions it made, where you corrected it, and plain health counts (how often it had to retry, what failed, how often you overrode it). This **doesn't change anything** — it's the gauge. Its value is that it sees *patterns across many runs* that no single decision shows: slow drift, a creeping override-rate, one case-type quietly mishandled. It's also what the safety net reads to pull a runaway task back (see Autonomy). It lives in the skill's existing run records — no new files.

### 2. Reflect (end of every session — the retrospective)

When a session ends, the retrospective reviews the session and produces learnings. **It must independently review the session trace, not just process arguments passed to it.** A summary of "here's what went wrong" biases toward what the summariser noticed; the full trace catches what they missed.

**The retrospective checklist (walk each in order):**

1. **Walk the corrections.** For each time the operator pushed back, asked for a redo, or corrected an output: what was wrong, why, and what's the durable rule? → `operator-correction` entry.
2. **Walk the successes.** What worked on first attempt, was praised, or was accepted without changes? What's non-obvious about why it worked? → consider `positive-pattern` entry. (Don't skip this. Correction-only retrospectives drift toward caution and lose what works.)
3. **Walk the outputs.** For each deliverable the skill produced (draft, ticket, diagnosis, plan, fix): was the first version correct? If it was revised, what specifically changed and why? Each revision is a candidate learning.
4. **Check procedure adherence.** Did the skill follow its own phases/steps in order? Where did it skip, shortcut, or reorder? A skipped step that caused a correction is a strong signal.
5. **Skill-specific checks.** Read `<skill>/references/retrospective-checklist.md` if it exists. Each skill adds its own domain-specific checks during upskill setup (e.g. investigation skills check "was each diagnosis verified against user data?", drafting skills check "was the customer's actual message read before composing?"). Generic upskill does not prescribe these; it delegates to the skill's own checklist.

**Do NOT rely solely on arguments passed to `/upskill`.** The arguments are a starting point. Re-scan the session for corrections the summary missed, especially quiet acceptances ("yes that's fine" after a non-obvious choice) and patterns across multiple items.

The retrospective produces four things:
- **A run-journal entry** → appended to `references/run-journal.md`. A short dated section (~10-15 lines): what went well, what didn't, corrections made, health counts, and which lessons were distilled. This is the evidence trail — NOT read at every run start, but read when investigating patterns or deciding whether to retrain. Format: `references/run-journal-format.md`.
- **Durable lessons** → written to `references/learnings.md` as `proposed` (see the convention below). Be **selective**: only generalisable lessons become entries; one-off noise is dropped so the wiki stays sharp. Lessons can come from corrections (`operator-correction`), the agent's own observation (`skill-inferred`), or something that consistently works well (`positive-pattern`) — see source types below.
- **Retrain flags** → when the same *judgment* keeps going wrong, it flags that decision-type as a candidate to retrain (handed to optimise-skill in step 3).
- **Staleness check** → scan `learnings.md` for `active` entries where `updated:` is older than 30 days. Surface them: "These rules haven't been confirmed in a while — still relevant?" The operator either re-confirms (bump `updated:`) or retires them. Freshness is a trust signal: old + never seen again = probably stale; old + recently confirmed = durable, candidate for graduation.

Lessons it writes are the agent's own guesses (`skill-inferred`), so they're advisory until you ratify them — they can't silently become reflexes (see Safety).

### 3. Improve (three levels, fast to durable)

`learnings.md` is a staging area, not the final destination. Lessons land there fast but are fragile (context read 100k tokens ago is easy to forget under pressure). The real improvement is when a lesson gets folded into the skill itself.

- **Lessons (fast, every run)** — notes in `learnings.md`, read at the start of every run, so a fix sticks without re-deriving. Cheap, continuous. A lesson enforces only once it's ratified (by you) or proven (by a real outcome). This is the Karpathy wiki: stop re-deriving, start compiling.

- **Graduation into SKILL.md (durable, periodic)** — when a lesson proves itself (recurs at `seen: 2`, or you ratify it early), it becomes a candidate to fold into the skill's own SKILL.md — into the procedure, the common-mistakes section, the checks. This is gated by the `writing-skills` TDD cycle:
  1. **RED:** Write a pressure test (a subagent scenario) that demonstrates the failure mode the lesson addresses. Run it against the current SKILL.md. Watch it fail. If it does NOT fail, don't conclude "no procedure gap" yet — first check whether the failure is vigilance-under-load. A calm single-task agent self-corrects on lapses that only surface mid-batch under pressure. Re-run as a *load-faithful* variant: bury the trap as one item in a batch of distractor tasks, under a "move fast, keep it tight" framing. Only if the load-faithful RED also passes is the lesson better kept as an `active` run-start reminder than folded into SKILL.md.
  2. **GREEN:** Edit SKILL.md to address the failure (add the check to the procedure, add it to common mistakes, etc.). Run the test. Watch it pass.
  3. **REFACTOR:** Check for loopholes (does the agent find a new way around it?).
  4. Mark the lesson `retired` in `learnings.md`. The test joins `<skill>/tests/` as a permanent regression check.

  The growing test suite IS the score: each graduated lesson leaves a test behind. Run the suite any time to check for regressions.

- **Retraining (for judgment skills)** — when a skill keeps making the *same scorable call* and getting it wrong (ticket-or-not, skip-or-fix, severity), that judgment gets retrained by **optimise-skill** against the collected examples, behind a held-out test (accept only if it scores better and still catches known past failures). Heavier, occasional, triggered when enough corrected examples have piled up.

**A lesson that keeps recurring graduates — but where depends on what it is.** A recurring *procedure* ("always check X before doing Y") goes into SKILL.md via pressure tests. A recurring *judgment* ("this type of call keeps being wrong") goes to optimise-skill for rubric tuning. See `references/learnings-format.md` for the routing rule.

### The learnings.md convention
Per-skill, append-only, PII-free wiki at `<skill>/references/learnings.md`, **read at the start of every run**. One canonical entry format (every skill identical — a scannable header line, like a corpus row, plus Karpathy-style freshness, recurrence count, and optional links):
```markdown
### <id-kebab> · status: proposed · source: operator-correction · seen: 1 · updated: 2026-06-02 · tags: #pii-boundary
**What happened:** <PII-free, 1–2 sentences>
**Rule:** <the durable behaviour>
**Check:** <a yes/no question to ask on a future run>
**Related:** [[my-skill/related-entry-id]] — brief reason for the link
```
- `status: proposed → active → retired` — new entries land `proposed` (surfaced, not enforced); you flip to `active` to bind it; graduated entries become `retired`; revert by flipping, never deleting.
- `source: operator-correction | skill-inferred | positive-pattern` — only `operator-correction` + `active` enforce; `skill-inferred` stays advisory until ratified; `positive-pattern` captures what consistently works (the critic surfaces it as "protect this" rather than "fix this").
- `tags:` *(optional, in header)* — `#kebab-tags` for cross-cutting concerns that span skills. Enables grep-based discovery across the whole wiki.
- `Related:` — path-qualified wikilinks with inline summaries: `[[skill-name/entry-id]] — reason`. The summary makes links self-describing to an LLM. Use `[[project/entry-id]]` for project-wide learnings. Keep to 3-5 links max.
- `seen:` — bump it when the lesson recurs (don't duplicate the entry); **at `seen: 2` (or when you ratify it), the lesson graduates** — a recurring judgment goes to optimise-skill for retraining; a recurring procedure goes to SKILL.md via the writing-skills TDD cycle (see Improve above). Mark the entry `retired` once graduated.
- `updated:` — last touched; a stale `active` entry the code has outgrown gets re-checked, not trusted forever.

Full format + lifecycle: `references/learnings-format.md`.

### What a skill produces (the full artifact set)

| Artifact | Location | Read when | Purpose |
|---|---|---|---|
| **SKILL.md** | `<skill>/SKILL.md` | Every run (core instruction) | The skill itself — procedure, rules, common mistakes. The durable home for graduated lessons. |
| **learnings.md** | `<skill>/references/learnings.md` | Every run (supplement) | Staging area for corrections. Fast to add, read at run start, but fragile. Lessons graduate out of here into SKILL.md or optimise-skill. |
| **run-journal.md** | `<skill>/references/run-journal.md` | When reflecting or investigating | Retrospective log. What happened, what worked/didn't, health counts. The evidence trail. |
| **Pressure tests** | `<skill>/tests/` | On demand, or as a regression suite | Graduated lessons as subagent scenarios. The score (pass count / total). |
| **Decision corpus** | `<project>/.claude/<skill>-corpus/` | By optimise-skill | Machine-readable decisions for rubric tuning. PII-bearing, project-local, gitignored. |
| **Project-wide learnings** | `<project-config>/learnings.md` | Session start | Cross-cutting process patterns that span skills. Same entry format. Referenced with `[[project/entry-id]]`. |

The cycle: run-journal captures the raw signal. `learnings.md` stages corrections. Pressure tests gate the promotion to SKILL.md. SKILL.md is the durable skill. The corpus feeds the rubric tuner for judgment skills. Project-wide learnings capture cross-cutting patterns that don't belong to any single skill.

---

## Autonomy — ask-me-first or just-do-it

One choice per *kind of decision* (not per whole skill — so a skill can act on its own for some calls and still check with you on others).

- **Ask-me-first** (default; everything starts here). It proposes, you approve.
- **Just-do-it.** It acts on its own.

**The one rule for what can ever be just-do-it: can a mistake be undone?**
- **Undoable** (a draft, a code edit, filing a ticket, a learnings note) → can become just-do-it.
- **Can't be undone** → **always ask-me-first, forever.** No review makes an un-undoable action safe.

This doesn't drift because it's an **allow-list, not a danger-list**: only things confirmed undoable are eligible; anything new or unclear stays ask-me-first by default. The principle: revertibility is the line, non-negotiable.

**Domain-specific safety constraints** (moving money, sending real messages, deleting data, irreversible infrastructure changes) belong in `<project-config>/learnings.md`, not here. Each project defines its own never-autonomous list. upskill reads that file at run start and enforces it.

**How a decision-type earns just-do-it (graduation).** Not an approval streak (too fragile, too easy to game). It earns it when all of:
1. it's **undoable** (else it never qualifies);
2. its **track record** shows you've been agreeing with it;
3. the **review provably catches that decision-type's known past mistakes** — keep a few real examples of times this kind of call went wrong, and the reviewer must flag them; and
4. **you flip it on** with one command. It never flips itself.

**The flip** (to build): `/upskill <skill>` shows a plain readout —
```
Ready to turn on (undoable, track record good, catches the known traps):
  • drafting how-to replies        [turn on?]
Not ready (stays ask-me-first):
  • bug vs working-as-designed — review doesn't yet catch the
    "looks like confusion, actually a bug" trap
Never (can't be undone):
  • see project-wide learnings for domain-specific list
```
You say yes; it records the setting; reversible any time.

**While a decision-type is on just-do-it,** before it acts it gets a quick adversarial review from a few different angles; a checker then decides *resolved / needs replanning / escalate*. On an objection it revises and re-checks; it escalates to you the moment it stops making progress, with a hard cap as a backstop. The review's job is to find a reason *not* to act, not to vote.

**Safety net:** if a just-do-it action turns out wrong (it gets reverted/redone), that decision-type automatically drops back to ask-me-first.

---

## Safety rails (why these exist)

`learnings.md` is read every run, seeds behaviour, and syncs across machines, and creating skills makes new tools others trust — so:
1. **Staging contract (create):** nothing lands until tests pass + you approve; failure/rejection discards it.
2. **Proposed-by-default:** the only path to an *enforced* lesson runs through you (or a proven outcome).
3. **Provenance:** the retrospective's own (`skill-inferred`) lessons stay advisory until ratified — the skill can't launder its guesses into policy.
4. **Undoable-only + project safety list:** un-undoable actions never go just-do-it; the eligibility set is an allow-list. Domain-specific constraints live in `<project-config>/learnings.md`.
5. **Self-targeting block:** upskill must NOT autonomously improve itself or its trust chain (the skills that govern how it runs and evaluates). Editing the rules that govern your own runs needs explicit human invocation + a reviewed diff. (Creating a *new* skill is fine.)
6. **No PII in synced files:** learnings.md is generalised; anything with customer IDs stays project-local and gitignored.

## Common mistakes
- **Committing a skill before tests pass** — staging discards on failure; no half-broken skills on disk.
- **Letting the retrospective bloat learnings.md** — only durable, generalisable lessons; drop one-off noise.
- **Writing a lesson straight to `active`** — new entries are `proposed`; you flip them.
- **Folding a lesson into SKILL.md without a pressure test** — TDD applies to improvements, not just creation. RED first, then GREEN.
- **Concluding "no procedure gap" from an isolated RED that passed** — vigilance-under-load lapses don't reproduce in a calm single-task agent. Run a load-faithful RED (trap buried mid-batch under speed/correction pressure) before downgrading a lesson to an `active`-only reminder.
- **Sending a procedural lesson to optimise-skill** — "always check X before Y" is a SKILL.md change, not a rubric tune. Route by what it is: judgments to optimise-skill, procedures to SKILL.md via TDD.
- **Skipping the run-journal entry** — the journal is how patterns become visible across runs. No journal = no evidence for graduation decisions.
- **Treating "just-do-it" as all-or-nothing** — it's per decision-type, undoable-only, and you flip each one on.

## Dogfood

upskill uses its own improvement infrastructure. `references/learnings.md` captures corrections from upskill's own runs. `references/run-journal.md` logs each retrospective. The seed checks in `references/critic-pass.md` came from the first production run where upskill missed a shipped feature and the operator had to challenge its ticket calibration. See the README for worked examples.
