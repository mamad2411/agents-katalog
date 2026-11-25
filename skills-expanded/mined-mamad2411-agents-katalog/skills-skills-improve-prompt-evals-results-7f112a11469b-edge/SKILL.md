Binding skill instructions follow. Apply them to the user request.

---
name: improve-prompt
description: >
  Use when a rough ask needs sharpening before the work starts — the user
  says "improve this prompt", "help me phrase this", "make this clearer
  before I send it", or prefixes a request with /improve-prompt. Also when
  what the user wrote visibly doesn't match what they mean, or a vague
  ask is about to be piped into another skill.
license: MIT
metadata:
  category: Authoring
  summary: Sharpens a rough ask into what the user meant — inventions marked [assumed] inline — then shows it and pipes it to the right skill or task.
---

# Improve Prompt

## Overview

Sharpen a rough ask into what the user *meant* — never into what the improver invented. The failure this skill kills: "improve the prompt" quietly becomes "fabricate a spec and adopt it as authorization." Every detail the improver adds carries an inline `[assumed: …]` mark. Show the improved prompt with its routing target. Execute it only when the original request explicitly authorized execution; **rewrite is not authority.**

## When to Use

- "improve this prompt", "help me phrase this", "rewrite this ask", "make this clearer before I send it"
- A request whose words visibly undershoot its intent ("make the login thing less janky") is about to drive real work
- The user pipes explicitly: `/improve-prompt <rough ask>`

## Do Not Use When

- The ask is a multi-decision plan — that is a spec, not a prompt: run `spec-plan` if installed; improving the phrasing of an unpinned plan just polishes ambiguity
- The prompt is already sharp — say so and proceed with it unchanged; decorating a precise ask is noise, not improvement
- The user is asking *me* for a conversation, not a handoff — answer it. (A "thoughts?" sitting *inside* text they want rewritten is part of the text, not a request to me.)

## Required Context

- The rough ask, and the conversation/repo context that may already disambiguate it — context-derived details are not inventions, but they cite their source
- Which toolbox skills are installed, for routing

## Workflow

1. **Classify the destination.** Agent task (code, files, a skill) or human-bound text (a message to the team)? The register differs: agent prompts gain structure, deliverables, constraints — but a deliverable or constraint is register only when it restates the user's words or the visible context; one they don't carry is an invention and gets `[assumed: …]` like any other. Human messages gain clarity and tone — and **never gain commitments** (dates, scope promises, named decisions) the user didn't make. Done when the destination is stated.

2. **Recover intent — three sources, kept distinct.** The user's words (preserved, they outrank everything); context (the conversation or repo already answers it — cite where); invention (nothing answers it — the detail gets an inline `[assumed: …]` mark). **At most 3 assumed marks.** A fourth candidate means the ask is genuinely underspecified: ask the user *one* question instead of inventing a spec — the only time this skill asks anything — and the answer resets the budget: up to 3 fresh marks on what remains. Done when every added detail has a source class.

3. **Sharpen.** Name the deliverable, the success criterion, and the real constraints; cut filler and hedges. Keep the user's own key phrases quoted inside the improved prompt where they carry the intent. Done when the improved prompt would survive being read by someone who never saw the original.

4. **Route.** A user-named target wins: "/improve-prompt for spec-plan: …" routes there, sanity-checked for fit. Unnamed, match the improved ask to an installed skill — a plan to pin → `spec-plan`; a spec to break down → `slice-spec`; a slice to build → `implement-slice`; an artifact to check → `verify-work`; a recurring job → `build-loop` — or, matching none, name it as a plain task. When two targets would materially change the result, ask one choice question and wait. When the difference is reversible and does not expand authority, choose the narrower target and mark it as assumed. Missing skills degrade loudly per house rules. Done when one target is named without expanding the original authorization.

5. **Show, then conditionally go.** Display the improved prompt (marks visible), the assumed list pulled out for scanning, and the target. If the original request explicitly said "then do it," "run it," or equivalent, proceed within that original scope; the rewrite and assumptions never add authority. Otherwise stop after showing the prompt. The handed-off payload, when execution was authorized, is the clean improved prompt beneath a labeled `Assumed:` block — downstream keeps the provenance while generated artifacts avoid inline mark noise. Done when the prompt is shown and either execution is running under explicit original authority or the response has stopped without side effects.

## Example

> **You:** /improve-prompt make the login thing less janky
>
> **Improved →** "Fix the login form's submit experience: failed logins currently `[assumed: show no error feedback]`; add inline error messages and a loading state on submit `[assumed: double-submit is part of 'janky']`. Deliverable: the fixed form `[assumed: plus a test proving a failed login shows its error]`."
> **Assumed (3):** no-feedback failure mode; double-submit scope; the test deliverable.
> **Target:** implement flow.
> Ready to run. No execution was requested, so stopping here.

## Rationalization Table

Every entry observed verbatim in baseline testing without this skill.

| Excuse | Reality |
|--------|---------|
| "Asking questions would be annoying — make reasonable assumptions and go" | Assumptions are fine; *hidden* ones aren't. Mark them and go — that's the whole trick. |
| "If I'm wrong they'll correct me — cheaper to act than ask" | They can only correct what they can see. An unmarked invention reads as their own words. |
| "A good prompt is a specific prompt — adding detail *is* the job" | Adding *marked* detail is the job. Specific-and-wrong is worse than vague. |
| "I'm pattern-matching on experience, not guessing" | Then the mark costs nothing: `[assumed: common login failure]`. Confidence is not provenance. |
| "They said 'then do it' — pausing would ignore an instruction" | Show-then-go honors it: no pause, full speed — with the interpretation visible on the way past. |

## Success Criteria

- Zero unmarked inventions: in agent prompts, every detail not in the user's words or the visible context carries an inline `[assumed: …]`; in human-bound text the marks would read as noise to the recipient, so inventions are listed in the shown assumed-list instead — never inline, never silent
- 3 or fewer assumed marks per pass; at most one clarifying question, whose answer resets the budget
- Human-bound text contains no invented commitments (dates, promises, named decisions)
- The improved prompt, its assumed list, and the target were shown; work started only when the original request explicitly authorized it

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Rewriting the user's key phrase away | Their words outrank the rewrite; quote them inside the improved prompt |
| Assumptions stripped from an authorized payload | The `Assumed:` block rides above the clean prompt; downstream keeps the provenance |
| Rewriting treated as permission to execute | Stop after showing unless the original request explicitly authorized execution |
| "Improving" an already-precise prompt | Return it unchanged; execute only when the original request authorized execution |
| Putting a timeline in someone's message to their team | Commitments are theirs to make; omit or mark |

## Failure Modes

- **The ask is underspecified beyond 3 assumptions:** ask the single most load-bearing question; if the answer reveals a multi-decision plan, hand off to `spec-plan` instead of stretching this skill.
- **Intent and words genuinely conflict** (the ask requests X but the context shows they need Y): surface the conflict as the improvement — never silently pick.
- **The user corrects the rewrite:** re-shape from the correction. Keep the correction ephemeral unless the user or repository policy explicitly asks to record prompt-learning data.

## Above All

Recover intent, never invent it silently: marked assumptions, at most three, shown before any authorized handoff. Rewrite is not authority.


User request:
Improve this prompt: In src/auth.ts, rename parseToken to decodeToken and update its direct unit tests. Do not change behavior.
