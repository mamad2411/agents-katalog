---
name: interview-me
description: >-
  Interview the user one question at a time to turn ambiguities into explicit
  decisions before implementation, prioritizing architecture-changing
  questions. Use when the user says "interview me", "访谈我",
  "开工前把需求问清楚", "帮我把这个需求里的模糊点理清楚",
  "ask me clarifying questions" before starting, complains the requirements
  are too vague to start ("需求太模糊没法干"), or wants pre-task Q&A.
  Not when the user merely permits
  questions while working ("有不确定的可以问我", "ask me if unclear") —
  permission for later is not an interview now. Not for interview practice
  (面试题) or researching pitfalls (use blindspot-pass; run it first when
  both apply).
---

# Interview Me

Resolve the user's known unknowns by interviewing them, one question at a
time, before any implementation.

## Workflow

1. **Build the question list silently.** From the conversation, any
   blindspot-pass findings if that ran first, plus a quick scan of relevant
   code (for greenfield work with no code yet, the conversation alone), list
   the ambiguities in the task. For each, note
   which layer the answer would change: architecture/data model >
   scope/behavior > UX details > cosmetics. Sort by that impact; when one
   answer gates other questions, ask the gating question first. If the list
   holds 10+ architecture-level ambiguities, propose splitting the task
   instead of interviewing through it. Open by telling the user how many
   questions you plan to ask, architecture first.
2. **Ask one question at a time.** Use the structured question tool when
   available (in Cursor, the AskQuestion option card; in Claude Code, the
   AskUserQuestion tool). Never ask a bare open-ended "what do you want?".
   For decision questions:
   - Present 2-4 concrete options, recommended option first, marked
     "(recommended)" in its label.
   - Say why the answer matters (what it would change) and the trade-offs in
     the question body; keep option labels short.
   - Treat a free-text answer outside the listed options as a first-class
     answer.
   For fact questions (who the users are, how much data), ask openly —
   options, if offered, are "e.g." examples, never a forced choice.
3. **Re-plan after every answer.** The question list is a living document:
   drop questions the answer resolved, rewrite options it invalidated, add
   ambiguities it exposed. If an answer does not address the question,
   restate it once — that is not re-asking. If it introduces a new
   requirement, do not expand it that turn: batch-ask which of the new items
   are in or out of scope; after three consecutive turns of new
   requirements, pause the interview and re-scope the task. If the user
   changes a requirement mid-interview, say which earlier decisions it
   affects, update those, and rebuild the remaining list.
4. **Stop early.** End the interview once remaining unknowns would not change
   the approach — typically 3-7 questions. At question 7, if
   approach-changing unknowns still remain, stop asking one-by-one: lay out
   the remaining list in a single message, let the user pick what to settle
   now, and record the rest as assumptions. Never pad with questions you
   could answer yourself from the code; go read the code instead.
5. **Deliver the decision record.** Summarize in chat, in the language of the
   conversation, as a compact decision record ("known knowns") with three
   parts: decisions made; assumptions (defaults chosen in place of an
   answer); deliberately deferred unknowns, each with the assumption chosen
   for it. Classify by who chose: the user explicitly picked = decision; the
   user explicitly postponed = deferred; the agent defaulted = assumption.
   Write each decision on one line: chosen — why it matters — alternatives
   shown — depends on (which earlier decisions, if any). Before delivering,
   re-read the record for contradictions; the record reflects the latest
   state — when the user reverses a decision, rewrite its entry in place,
   never append a conflicting one. Keep it ready to paste into an
   implementation prompt or plan. If planning or implementation will happen
   in a later session (or the user asks), also write it to
   `interview-decisions.md` in the project root. Do not commit it unless the
   user asks; in a git repo, exclude it locally:
   `n=interview-decisions.md; p="$(git rev-parse --git-path info/exclude 2>/dev/null)" && { mkdir -p "$(dirname "$p")" && { grep -qxF "$n" "$p" || echo "$n" >> "$p"; }; } 2>/dev/null || echo "note: could not exclude $n — leaving it untracked, never staging it"`
   If planning comes next, hand this decision record to implementation-plan
   as its input.

## Rules

- This skill requires a human respondent. If no interactive channel exists
  (headless/CI run, no one to answer), do not start the interview: say so,
  record explicit assumptions instead, and proceed.
- One question per turn — a single structured-question call, then wait for
  the answer. Do not batch (the step 3 in/out-of-scope check, the step 4
  wrap-up, and the bundled-defaults confirmation below are each one
  message, not a batch).
- If the user answers "I don't know" — or delegates the choice ("随便",
  "你定", "you decide") — offer to prototype (the design-directions skill exists
  for this) or default to the recommended option and record it as an
  assumption; do not re-ask that question. After two consecutive such
  answers, stop asking one-by-one and bundle the remaining recommended
  defaults into one yes/no confirmation.
- The interview's deliverable is the decision record. Do not start
  implementing during the interview or right after it — wait for the user's
  go.
