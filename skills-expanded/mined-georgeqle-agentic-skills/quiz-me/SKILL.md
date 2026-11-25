---
name: quiz-me
description: Adversarial one-question-at-a-time questioning to verify deep reading comprehension of alignment pages, specs, or any document
type: review
version: v0.0
argument-hint: "[file-path-or-glob]"
---

# Quiz Me

Invoke as `$quiz-me`.

Adversarial comprehension testing. Reads a document silently, then grills the user one question at a time to verify they actually read it -- not skimmed it, not got the gist, actually read it. Delivers a pass/fail verdict when done.

This is not teaching. This is not alignment-building. This is a test. The user claims they read something; this skill finds out if that's true.

## Process

### Phase 1: Silent Document Ingestion

1. **Resolve input files.**
   - If `$ARGUMENTS` contains a file path or glob, read those files.
   - If `$ARGUMENTS` is empty, find all alignment HTML files (`docs/**/*.html`) and spec documents (`specs/**/*.md`) in the current repo. If multiple files are found, ask the user which document(s) to quiz on.
   - Supported formats: HTML, Markdown, plain text.
   - If no readable document is found, stop and tell the user.

2. **Analyze document structure internally.**
   - Identify major sections, key decisions, trade-offs, cross-section relationships, specific constraints/numbers/names, and non-obvious details.
   - Build an internal question plan that covers every major section, biased toward:
     - Cross-section relationships ("How does X in section 3 affect Y in section 7?")
     - Implications and trade-offs ("What happens if the migration in step 2 fails?")
     - Specific details that skimmers miss (exact constraints, numbers, edge cases)
     - Intent questions ("Why was approach A chosen over approach B?")
     - Synthesis questions ("Summarize the three most important trade-offs.")
   - Do NOT surface any of this analysis to the user.

3. **Open the quiz.** Tell the user which document(s) they're being quizzed on and that you'll ask one question at a time. Nothing else -- no summary, no encouragement, no preview of what's coming.

### Phase 2: Adversarial Questioning

Ask **one question per turn**. Non-negotiable.

Use Codex's available user-input mechanism for every question. When a structured user-input tool is available, present 2-3 plausible multiple-choice options and leave room for the user's free-form "Other" answer. When no structured user-input tool is available, ask exactly one concise question in the conversation, include 2-3 labeled options, explicitly allow a free-form answer, and wait for the user's reply. At least one option should be a trap -- superficially plausible but wrong if the user actually read the document. Vary whether the correct answer is a named option or requires free text.

**Question types** (mix throughout, do not cluster by type):

- **Relationship:** "Section X describes [thing]. How does that interact with [thing from section Y]?"
- **Implication:** "If [condition from the doc] changes, what breaks?"
- **Detail trap:** "What specific [constraint/number/name] does the doc specify for [thing]?"
- **Intent:** "Why does the doc recommend [approach] instead of [alternative]?"
- **Synthesis:** "What are the most important trade-offs the document makes?"

**After each answer, evaluate strictly:**

- **Correct and specific:** Acknowledge in one sentence. Move to next question.
- **Vague or incomplete:** Push back. "That's too vague. What specifically does the doc say about [X]?" Do not accept hand-wavy answers. Re-ask or ask a targeted follow-up.
- **Wrong:** State what's wrong. Give the user one chance to correct. If they fail again, note the gap and move on.
- **Suspiciously perfect verbatim recall:** Ask a follow-up that requires synthesis, not recitation. If they can synthesize, accept it. If they can only parrot, mark the section as weak.

Track per-section comprehension internally. Do not show the user a running score.

### Phase 3: Termination

Continue until one of:

- The user has demonstrated understanding across **all major sections** -- no section left untested.
- The user explicitly gives up or asks to stop.

Do NOT terminate early because the user got a few questions right. Cover the full document. Minimum 5 questions for short documents, more for longer ones.

### Phase 4: Verdict

When the quiz ends, deliver:

1. **Pass or Fail.** Binary. Pass means the user demonstrated deep comprehension across all major sections. Fail means one or more sections had weak or missing comprehension.

2. **Per-section summary:**
   - Sections with strong comprehension
   - Sections with weak or missing comprehension
   - Specific gaps identified

3. **If fail:** List which sections to re-read and why.

## Constraints

- **Read-only.** Do not write, create, modify, or delete any files.
- **No commits, no pushes, no file mutations.**
- **No external requests.** All content is local.
- **One question per turn.** Always.
- **Use Codex-compatible user-input handling for every question.** Do not batch questions, and do not ask multiple independent questions in one response.
- **Adversarial but not hostile.** Push back firmly on bad answers. Do not insult the user. Do not congratulate excessively on correct answers.
- **No teaching.** Do not explain document content during the quiz. If the user gets something wrong, state what's wrong -- do not deliver a lesson.
- **No hints.** Do not help the user arrive at the right answer. This is a test, not a tutorial.

## Differences from taste-calibration

| | quiz-me | taste-calibration |
|---|---|---|
| Purpose | Test comprehension of existing docs | Build alignment for new work |
| Tone | Adversarial examiner | Socratic collaborator |
| Input | Existing document to test against | Rough idea or problem |
| Output | Pass/fail verdict | Shared understanding summary |
| Recommended answers | Never | Always |
| File output | None | None |

## Default Shipping Contract

Read-only — do not create or modify tracked repository files. Follow the shared shipping contract convention in CLAUDE.md for next-step routing only.

