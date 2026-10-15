---
name: rebuttal-strategist
description: Plan and write strategic rebuttals after real paper reviews arrive. Use this skill whenever the user has OpenReview reviews, reviewer comments, scores, confidence ratings, meta-reviews, author response windows, or wants to decide which experiments to run, infer reviewer intent, draft point-by-point responses, prepare follow-up discussion replies, or improve wording after reviews for ML/AI venues such as NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP, or similar conferences.
argument-hint: "[paper-dir] [--venue <venue>] [--openreview <forum-url>] [--mode plan|draft|followup]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Rebuttal Strategist

Turn real reviewer feedback into a tactical rebuttal plan, experiment plan, paper revision plan, and response draft. This skill starts after reviews arrive. It is not a pre-submission shadow review.

Use this skill for:

- OpenReview review extraction and thread analysis
- reviewer intent and decision-state analysis
- issue board creation from real comments
- deciding which experiments, analyses, proofs, or clarifications to add during rebuttal
- drafting point-by-point author responses
- preparing concise follow-up replies during discussion
- tracking paper revisions promised in the response
- saving rebuttal memory for future rounds

Pair this skill with:

- `research-project-memory` when real reviews, issue boards, rebuttal experiments, or promised revisions should persist across sessions
- `paper-reviewer-simulator` for pre-submission shadow review or for stress-testing the draft response
- `run-experiment` when the rebuttal plan requires new experiments
- `conference-writing-adapter` when accepted reviewer criticism requires paper restructuring or clearer prose
- `citation-audit` and `citation-coverage-audit` when reviews identify citation problems
- `camera-ready-finalizer` after acceptance to verify promised revisions, final claim/evidence consistency, de-anonymization, and release handoff

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── decision-strategy.md
    ├── experiment-response-planning.md
    ├── issue-board.md
    ├── memory-model.md
    ├── openreview-protocol.md
    ├── rebuttal-writing-style.md
    ├── report-template.md
    └── review-intent-analysis.md
```

## Progressive Loading

- Always read `references/review-intent-analysis.md`, `references/issue-board.md`, and `references/rebuttal-writing-style.md`.
- Read `references/openreview-protocol.md` when the user provides an OpenReview URL, forum ID, review thread, or asks to fetch review information.
- Read `references/decision-strategy.md` when scores, confidence, reviewer stances, or AC/meta-review dynamics matter.
- Read `references/experiment-response-planning.md` when reviews request more experiments, baselines, ablations, proofs, analyses, or details.
- Read `references/memory-model.md` when saving or reusing project rebuttal state.
- Use `references/report-template.md` for substantial plans or saved reports.
- Verify current venue rebuttal rules, response length, deadline, anonymity constraints, and discussion policy from official sources when they affect the response.

## Core Principles

- Rebuttal is strategic, not just polite. The goal is to change the decision path.
- The audience is reviewers and the area chair. Write responses that help the AC see an accept path.
- Prioritize persuadable reviewers and high-impact misunderstandings. Do not spend most of the budget arguing with an unmovable reject unless their objection can dominate the meta-review.
- Separate real scientific weaknesses from presentation misunderstandings.
- Lead with evidence. Every response should cite a result, table, figure, theorem, appendix detail, new experiment, or concrete planned revision.
- Concede correct criticism cleanly. Defensive tone loses credibility.
- Never promise experiments, revisions, code, or analyses that the authors cannot deliver.
- Preserve anonymity and venue policy during rebuttal.

## Step 1 - Define Rebuttal Context

Identify:

- venue, year, and track
- response deadline and response length or format limit
- whether discussion is per-review, unified, or both
- whether follow-up comments are allowed
- current scores, confidence, and any meta-review/AC note
- paper source files and appendix
- review source: OpenReview URL, exported JSON, copied review text, PDF, or screenshots transcribed by the user
- mode:
  - `plan`: strategy, issue board, experiment plan
  - `draft`: write rebuttal text
  - `followup`: answer new reviewer questions during discussion
  - `post-mortem`: update memory after final decision

Default to `plan` before drafting if no issue board exists.

## Step 2 - Collect Reviews and Paper Evidence

Read or fetch:

- all reviews
- scores and confidence
- reviewer questions
- strengths and weaknesses
- official comments and follow-up threads
- any meta-review or AC comment
- paper abstract, introduction, method, experiments, appendix, figures, tables, and related work
- experiment logs or notes that may answer reviewer concerns

If using OpenReview, follow `references/openreview-protocol.md`. If fetching is blocked or login is needed, ask the user for exported review text or pasted comments.

## Step 3 - Atomic Review Parsing

Break every review into atomic issues.

Each issue should have:

- reviewer ID
- exact local concern
- category: novelty, correctness, theory, experiment, baseline, ablation, related work, clarity, reproducibility, ethics, limitation, formatting, question, praise
- severity
- whether the reviewer is factually correct
- whether the issue is answerable with existing evidence
- response posture

Do not answer broad review paragraphs as a blob. One paragraph may contain several independent issues.

## Step 4 - Infer Reviewer Intent and Decision State

Read `references/review-intent-analysis.md` and `references/decision-strategy.md`.

For each reviewer, infer:

- stance: champion, likely accept, borderline persuadable, skeptical but fixable, likely reject, unmovable reject
- whether the reviewer likes the core idea
- whether requested changes are small, medium, or fatal
- whether the reviewer is asking for clarification or building a reject case
- what evidence would move them

Then infer the paper-level decision path:

- current decision state
- main accept path
- main reject path
- which reviewer or issue is pivotal
- what the AC is likely to care about

## Step 5 - Build Issue Board

Read `references/issue-board.md`.

Rank issues:

- `must-win`: could decide acceptance if answered well
- `must-answer`: direct reviewer question or serious concern
- `quick-win`: easy clarification with high value
- `experiment-needed`: requires new experiment/analysis/proof
- `paper-revision`: can be fixed by promised text change
- `do-not-overinvest`: low impact or unmovable objection

The issue board should decide what gets response budget.

## Step 6 - Plan Experiments and Evidence

Read `references/experiment-response-planning.md`.

For each issue requiring evidence:

- define the smallest credible experiment, ablation, proof sketch, analysis, or table
- estimate feasibility before deadline
- identify required data, code, compute, metric, and owner
- define success, partial success, and failure response wording
- decide whether it belongs in rebuttal text, appendix, or future revision

Prefer targeted experiments that directly answer reviewer objections over broad new result hunting.

## Step 7 - Choose Response Posture

For every issue choose one posture:

- `accept-and-fix`
- `clarify-misunderstanding`
- `rebut-with-evidence`
- `partially-concede`
- `provide-new-result`
- `scope-and-limit`
- `defer-to-revision`
- `do-not-address-directly`

Read `references/rebuttal-writing-style.md` for wording guidance.

## Step 8 - Draft Rebuttal

Draft in the required format:

- per-reviewer response
- unified response
- short OpenReview author comment
- follow-up reply
- camera-ready response summary, if relevant

Default structure:

1. one-sentence appreciation and thesis
2. answer pivotal concerns first
3. group repeated concerns across reviewers
4. provide new results and concrete evidence
5. state paper revisions promised
6. answer remaining reviewer-specific questions

Use concise, non-defensive language. Do not waste budget thanking every reviewer separately unless format requires it.

## Step 9 - Stress-Test the Draft

Before finalizing, check:

- Does the draft answer the strongest reject path?
- Does it give the AC an accept path?
- Are promised revisions feasible?
- Are new results stated with enough detail?
- Are reviewer misunderstandings corrected without sounding combative?
- Are correct criticisms acknowledged?
- Are repeated issues consolidated?
- Are venue length and anonymity constraints respected?

If the draft fails, revise once and report remaining risks.

## Step 10 - Update Memory

Read `references/memory-model.md`.

When reviews were parsed or a strategy was created, update project-local memory under:

```text
.agent/rebuttal-strategy/
```

Track:

- original reviews and parsed issues
- reviewer intent map
- experiment plan
- response drafts
- promised paper revisions
- follow-up discussion state
- final decision, if known

If the project uses `research-project-memory`, also update:

- `memory/risk-board.md`: real reviewer risks and issue severity, using certainty `observed` for review text and `inferred` for intent
- `memory/action-board.md`: rebuttal experiments, response drafting tasks, promised revisions, and post-rebuttal follow-ups
- `memory/evidence-board.md`: new rebuttal experiments, proof sketches, analyses, or tables
- `memory/claim-board.md`: claims reviewers challenged, weakened, clarified, or supported
- `rebuttal/.agent/rebuttal-status.md`: issue board, reviewer intent map, response plan, promised revisions, and discussion state

Never mark a promised revision as done until the paper/code change exists. Link promises to actions.

## Output Modes

### Strategy Plan

```markdown
# Rebuttal Strategy
## Situation Summary
## Reviewer Intent Map
## Decision Path
## Issue Board
## Experiment / Evidence Plan
## Response Posture
## Draft Outline
## Follow-up Strategy
```

### Draft Response

```markdown
# Rebuttal Draft
## Response Strategy Notes
## Draft
## Claims Requiring Verification
## Promised Paper Revisions
## Remaining Risks
```

### Follow-Up Reply

```markdown
# Follow-Up Reply
## New Reviewer Comment
## Intent Assessment
## Recommended Reply
## Risk If Ignored
```

## Final Sanity Check

Before finalizing:

- real reviews are separated from inferred intent
- all scores/confidence are recorded when available
- the pivotal reviewer/issue is identified
- every must-win issue has evidence or a clear fallback
- response text follows venue limits and policy
- no impossible promises are made
- experiment plan has feasible deadlines
- paper revision promises are tracked
- memory updates are written if the user is working in a project repo
