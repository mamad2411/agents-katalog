---
name: quiz-me
description: Use when the user wants to be quizzed or tested on work that was just built for them, or on a pull request by number or URL, including a team mate's. Triggers include "quiz me", "test my understanding", "do I actually get this", "test me on this branch", "quiz me on PR #123". Not for explaining or re-teaching the work — only when they want to be tested on it.
---

# Quiz Me

Give the user a one-question-at-a-time oral exam on the work, centered on **why each decision beat its rejected alternatives**. Grade the answer, never the person; the goal is better calls next time.

**Every run must** make the user reason about at least one rejected alternative (if you can't name one, widen scope; never fall back to pure recall), and grade honestly: mark answers partial or missed when they earn it.

**Short choices** end the message as a numbered plain-text list, after the content; then stop. The user replies with a number or in their own words. Every message here carries content above its choice, so it all stays in the message text: a question-tool popup can hide the text before it.

If the user wants the work *explained*, this is the wrong skill — use the `walkthrough` skill. If the work is trivial (rename, formatting, version bump), say so and offer to quiz the one judgment call, the surrounding code, or skip.

## 1. Gather material silently

If the user named a **PR** (number or URL), that is the scope. Run `gh pr view <n>` for the description **and**, separately, `gh pr view <n> --comments` (it omits the description) for review comments. Then read the diff (`gh pr diff <n>`) and the **full changed files** at the PR head (`git fetch origin pull/<n>/head`, then `git show <sha>:<path>`; outside a clone, `gh api`). The PR need not be checked out.

Else if the user named a topic or file, that is the scope. If it wasn't touched this session, ask whether to quiz the code as-is or the actual changes.

Otherwise, use sources richest-first:
- **A walkthrough earlier in this session** — reuse its checked claims and sourced whys instead of checking them again; keep "my read" items labeled as your own analysis.
- **This session** — the alternatives you rejected and why. The diff only shows what survived.
- **Git** — scope and exact facts. Base: `git merge-base HEAD main`, else `master`, else `git symbolic-ref refs/remotes/origin/HEAD`; then `git diff <base>..HEAD` and `git log <base>..HEAD --oneline`. No base: `git diff HEAD` and `--staged`. No repo: the conversation. Then run `gh pr view --json number,state`: if the branch has an open PR, this is a **PR quiz** too (steps 3 and 7), and its description and comments count as written rationale.
- **Written rationale** — why-comments, ADRs, design docs, linked PRs/issues.

**Someone else's work** (a team mate's PR, a fresh session): you don't know what the author rejected. Use only alternatives stated in the PR, its comments or docs. Alternatives you see yourself are fine, but label them in the question as your own analysis ("one option I'd weigh…"), never as the author's reasoning.

Stop at 5–8 decisions with a known why. If the changes span unrelated areas, drop the mechanical ones and tell the user what you picked and skipped. If conversation and git are both empty, say there's nothing to test and ask what to quiz.

## 2. Build a checked answer key, then announce

Draft one line per decision — it is both the grading key and the question:

> concept/term · choice made · alternatives rejected · deciding tradeoff · what breaks if it's wrong · `[checked: <source>]` or `[unchecked]`

Use 5–8 lines, ordered easy → hard. If this surfaces a likely bug, flag it before starting.
**Check every line that rests on behavior outside the changed code** — library defaults (code that leaves a client's options unset counts: those defaults *are* the behavior) at the pinned version (read the source in the module cache or at that tag), chart values, API specs, the full files around the diff. Tag it with the source you read (file, version, value). Your memory of a default is not a source.

**Never build a question on an unchecked line.** If you can't check it, drop the line, or tell the user it is unchecked and leave it out of the quiz. The same rule holds for claims you make while grading or in a deep dive.

Do these checks before question 1, not on demand. Open with a line saying what you checked (e.g. "Checked: the HTTP client's retry defaults in its source at the pinned version"), then the progress map, then question 1.

## 3. Progress map

Show the quiz as a map of **topics, not questions** (no answers leaked). Show it at the start and again, updated, above every new question. Use exactly these symbols, then the legend, then what follows the quiz:

```
QUIZ ME · rate limiter

 ✓  1. Token bucket vs sliding log     warm-up
 ▶  2. Where the counters live         tradeoff
 ○  3. Behavior under a retry storm    prediction
 ○  4. When Redis goes down            failure mode

 ✓ correct   ◐ partial   ✗ missed   ▶ now   ○ to come
 then: assessment summary → parked questions
```
For a PR quiz (a named PR, or the branch's open PR), add `→ design-review` to the `then:` line. If a deep dive opens a topic worth testing, add it to the map and say so.

## 4. Run the quiz

- Ask **one** question, then wait. Don't leak the answer (no yes/no, no multiple choice). Use the user's language.
- Mostly *"why X over Y"*, plus at least one **transfer** ("same design, now \<new constraint\> — what gives?") and one **prediction** ("where does this break under \<stress\>?"). Recall is for warm-ups only.
- Ask confidence before grading: low / medium / high.
- Aim for ~70% correct: after two weak answers, scaffold down; after two sharp ones, jump to the hardest tradeoff or a transfer.
- "I don't know" / "just tell me" → answer plainly, mark it unanswered. "Stop" → assessment summary. Repeated wipeouts → switch to a guided walkthrough: explain, then ask.

| Type | Example |
|------|---------|
| Tradeoff | "We picked token bucket over a sliding-window log. What does the log buy you, and why wasn't it worth it?" |
| Transfer | "Same limiter, now per-tenant with 10k mostly-idle tenants. What gives first?" |
| Prediction | "What happens under a retry storm — where does it bend, where does it break?" |
| Failure mode | "If Redis goes down, what happens — and was that acceptable?" |

## 5. Grade, reveal, then pause

Each answer gets one message, in this shape:
1. **Verdict:** correct / partial / missed. Don't soften a wrong answer. If incomplete, nudge once before revealing.
2. **Reveal** the rejected alternatives and the deciding tradeoff. Flag confident-and-wrong plainly. Credit different-but-sound answers; if a grade is disputed, re-check the source and own your mistake.
3. **A short choice "What next?", and stop** — do not ask the next question in this message:
   - **Next question**
   - **Dig deeper** — free back-and-forth on this topic. No grading, no limit; the user says when to move on.
   - **Park it** — note the user's question (ask for it if they only picked the option); you answer it after the assessment summary, not now.

## 6. Assessment summary, then parked questions

Give it for whatever was answered, even two questions, in this order: **decisions to remember** (1–3 tradeoffs), **gaps to revisit**, **strengths**, and an optional snapshot score ("solid on the *what*, shakier on failure modes"). Then answer each parked question.

## 7. Hand off to design-review

For a PR quiz, end by offering a short choice:
- **Run `design-review` now (recommended)** — same session; it reads the quiz from the conversation.
- **Write a handoff file** — for `design-review` in a new session.

Outside a git clone you can't write the file: say so, and offer the same-session option only.

The handoff file goes to `<git common dir>/quiz-me/pr-<number>.md` (git common dir: `git rev-parse --path-format=absolute --git-common-dir`). Then tell the user the path and to run `design-review` in a new session. Plain markdown, exactly these headings, in order:

```markdown
## PR
<owner/repo> #<number> · <head SHA> · <title>
## Answer key
- <decision line> [checked: <source>]   (or [unchecked])
## Grades
- <topic>: ✓ / ◐ / ✗ / unanswered
## Gaps
## Parked questions
- <question> — <answer, if given>
## Candidate comments
```
