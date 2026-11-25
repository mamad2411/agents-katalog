---
name: jevaluate-report
description: "Turns a Jevaluate rating a team agrees with into one Markdown report its coding agents can work from before a pull request: the verdict, a ranked fix table and one section per fix with the line it rests on, the TypeSafe docs behind it, a change to try and a test to run on the team's own eval. Use after rating a project with jevaluate-private (or jevaluate-publish) and agreeing with the result, when a team wants a file its agents can work through, or on \"/jevaluate-report\" with a repo, rating or folder."
---

# Jevaluate Report

The workflow this skill fits: build with Jev Sources open, rate the work with `jevaluate-private`, and once you agree with the rating, run this skill. It writes one Markdown file that you point your coding agents at to work through the fixes before you open a pull request. The rating is a pair-programming check, not a score to publish, and this skill never posts anything.

`<skill>` below is this skill's folder.

## Contents

- The framing rule
- Intake
- Steps
- After the fixes
- In Codex
- Files
- Enforced by

## The framing rule

Jevaluate checks a design against TypeSafe's documented practice. That practice isn't shown to matter for this product until the team tests it on their own eval, and the people who built the project know it far better; what looks like a departure may be how they made something work. So every fix is advice to test: a change to try, and a test with a bar set before the run. The report says so in plain words in its opening, for the person and for their agent.

Every fix section has five labels (`scripts/report_check.py` checks them), in this order: **What we saw.**, **Why it matters.**, **Source.**, **Suggested change.**, **How to check it.** In them:
- **Suggested change** starts with "Try" or "Consider".
- No promise, outside quotes, in Suggested change, Why it matters, the opening, the Rating section or the title: "this fixes", "will fix", "will reduce", "solves", "must", "rates 4" and the like. `scripts/report_check.py` holds the full list.
- **How to check it** names the test, the measure or pass-or-fail outcome, and the bar.

`scripts/report_check.py` checks the labels, the rules above and that the opening says the fixes are to be tested. The two below are for the writer and the review agent:
- A fix that would move the verdict is a test on held-out data, never a promise.
- When the project already tried a version of a fix, the section says what it tried and found, and proposes a different version with the current design as the control.

## Intake

The input is the rating the user just agreed with: in this session, or a rating file they name. With no rating, ask them to run `jevaluate-private` first; never rate inside this skill. Ask only what the rating doesn't settle, in one batch, with a default for each:

1. **Where to save the report.** Default: `jevaluate-report.md` at the repo root, left uncommitted. Whether it goes in the pull request is the user's call.
2. **Published numbers:** does the project publish eval or benchmark results? Default: read the README and any `evals/` folder and say what you found.

## Steps

1. **Pin the commit** the rating read. For a GitHub repo, every repo link in the report is a permalink at that commit; the quote check reads code from a checkout that holds it (the user's own clone, or `git -C <clone> fetch origin <commit>`). If the code has moved since the rating, re-check the lines the new commits touch. For a local folder with no remote, use `target: <folder>` in place of `repo` and `commit`, and name files as `file:line` in code spans.
2. **Take the verdict and scores from the rating.** Take each verdict's name (2 "Rework it", 3 "Use with a fix") and each score's meaning from `../jevaluate/rubric.md`, sections 3 (scores) and 5 (verdicts). The target verdict in the opening comes from the rating's own reasoning about what moves it.
3. **Read the docs behind each fix** with `jev-sources`, and keep each source's label. A fix whose docs claim you can't quote is dropped and named when you hand back.
4. **Check the numbers, only when the project publishes some.** For each headline figure: what it decides, on what unit, at what n, against what baseline, with what interval. Compute intervals with a script and quote its output. Use a statistics skill such as `stats-ml-eval` when one is installed. With no published numbers, skip this step and add no statistics section.
5. **Build the fix list.** Read `lessons.md` first. Every failing fact in the rating, every figure the check found overstated or unsupported, merged. Re-derive each at the commit: the file line and the docs quote. A fix you can't re-derive is dropped and named, with why, when you hand back. Read the project's own experiments and issues for earlier tries. Rank: Jev question and model, then eval method, then reporting, then minor.
6. **Draft from `template.md`.** Write the opening, summary table, Rating, What already works and every fix section. The opening is for a person and their agent at once: what the report is and that each fix is advice to test on their own eval, then the verdict and its one cause pointing to the Rating section, the top fixes as bullets, and the paragraph telling the agent how to work through them.
7. **Check the draft:** `python3 <skill>/scripts/report_check.py <file> --private-terms <file of terms that must never appear, one per line>`. With no terms file it says so and checks only paths, internal IDs and the built-in words. Then `python3 <skill>/scripts/trace_check.py <file> --checkout <clone>`: every docs quote must be on the Jev Sources page it links, and every quoted line of code in the linked file and lines at the commit; quotes from other sources are listed for you to check by hand. Fix every finding. Then remove AI-writing tells (with a scanner, when one is installed).
8. **One review agent.** Give a fresh agent the file, the rating and the framing rule, never this session's summary. It checks each fix's docs claim with `jev-sources` and its line at the commit, and each figure when step 4 ran, and reads the opening as someone new to the project: can they say what to do first, and that each fix is a test? Before dispatch, tell the user its token estimate (from an estimating tool if you have one, else a rough count). The agent proposes; you apply. Before applying an edit, trace each fact it adds to the rating, the code at the commit or a docs quote you read in step 3, and drop any you can't trace.
9. **Rerun both checks** on the file as saved, after the review edits and after any later edit by you or the user: an edit can break a label or add a bare fix number.
10. **Hand back** the file's path, the fixes dropped with why, and one line to give their agent, naming the file where it was saved: "Work through `<file>`, one fix at a time, as its opening says." This skill never commits, posts or opens anything; the user decides what goes in the pull request.

## After the fixes

Once the agents have worked through the fixes, re-rate the new commit with `jevaluate-private`. If the rating still has fixes, run this skill again for a new report; keep the old one as it was. What the team's tests showed belongs in their own notes; to share a lesson with every user of the skill, propose it to `lessons.md` by pull request.

## In Codex

Ask for it by name: `jevaluate-report <repo>`. Codex's default sandbox blocks the network, so fetching the commit and the Jev Sources refresh need your approval, or a run with network access. Step 8's review agent runs as a Codex subagent.

## Files

- `template.md`: the report's layout and the rules for filling it.
- `lessons.md`: what past reports taught, with the first one (skimmer) as the example.
- `scripts/report_check.py`, `scripts/trace_check.py`, `tests/`.

## Enforced by

| Rule | Enforced by |
|---|---|
| Front matter has title, date, method, verdict, scores, fixes, and a repo with a 40-character commit or a target | `scripts/report_check.py` (front-matter) |
| Five fix labels, exact text, in order, in every fix section | `scripts/report_check.py` (labels) |
| Repo links pinned to the front-matter commit | `scripts/report_check.py` (pinned-links) |
| Every link is a web address or a #section, never a local file | `scripts/report_check.py` (local-link) |
| Summary table, fix sections and front-matter list agree | `scripts/report_check.py` (table-match) |
| Cross-references by section name, no bare fix number in the body | `scripts/report_check.py` (bare-ref) |
| Order: title, opening, table, Rating, What already works, fixes | `scripts/report_check.py` (order) |
| No local paths (link targets included), internal IDs or private terms in the front matter or body | `scripts/report_check.py` (private) |
| No em-dashes or emojis; `--` at most once a paragraph | `scripts/report_check.py` (dashes) |
| Under 60,000 characters | `scripts/report_check.py` (size) |
| No promise in Suggested change, Why it matters, the opening, the Rating section or the title | `scripts/report_check.py` (certainty) |
| Suggested change starts with Try or Consider | `scripts/report_check.py` (advice) |
| How to check it names a measure or outcome | `scripts/report_check.py` (test-named) |
| Opening links the Rating section and lists the top fixes as bullets; Rating has all four scores | `scripts/report_check.py` (opening) |
| Opening says the fixes are to be tested | `scripts/report_check.py` (opening-test) |
| Every docs quote is on the Jev Sources page it links; every quoted line of code is in the linked file and lines at the commit | `scripts/trace_check.py` |
| A real report in the current template (skimmer's, rebuilt) passes both checks | `tests/test_report_check.py`, `tests/test_trace_check.py` (`fixtures/skimmer-report.md`) |
| The checks behave as stated, on three fixed blind probe sets | `tests/test_report_check.py` (`fixtures/probes.json`, `fixtures/whole-probes.json`), `tests/test_trace_check.py` (`fixtures/trace-probes.json`) |
| A rating the user agreed with as the input, praise and claims no wider than the rating, target verdict traced, review edits traced before they are applied, quotes from sources other than the docs and the repo, numbers check, fix ranking, an opening a newcomer can act on | the session running the skill, then the review agent |
