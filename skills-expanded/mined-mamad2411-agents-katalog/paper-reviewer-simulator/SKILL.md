---
name: paper-reviewer-simulator
description: Simulate target-conference reviewers for an ML/AI paper before submission. Use this skill whenever the user wants a reviewer-style critique, predicted scores, likely reject reasons, rebuttal risks, area-chair style meta-review, adversarial Reviewer 2 feedback, or venue-specific pre-review for conferences such as NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP, or similar venues. This skill should dynamically inspect reviewer guidelines, example reviews, accepted papers, and project evidence when available.
argument-hint: "[paper-dir] [--venue <venue>] [--mode quick|full|adversarial|rebuttal]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Paper Reviewer Simulator

Run a pre-submission shadow review from the perspective of target-conference reviewers. The goal is to find the objections reviewers are likely to raise before the paper is submitted, then turn those objections into concrete revision priorities.

Use this skill for:

- reviewer-style paper critique
- venue-specific predicted scores and confidence
- likely reject reasons and reviewer questions
- adversarial "Reviewer 2" stress tests
- area-chair or meta-review summaries
- rebuttal-readiness checks
- risk register creation for a paper under revision
- learning from example reviews, OpenReview discussions, and target-venue guidelines

Do not use this skill to rewrite the paper directly. Pair it with `conference-writing-adapter` after the review if the paper needs structural or paragraph-level changes. Pair it with `citation-audit` for reference correctness and `submit-paper` for final submission hygiene.

Pair this skill with `research-project-memory` when simulated reviewer risks should become project-level risks and actions.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── example-review-mining.md
    ├── memory-model.md
    ├── report-template.md
    ├── review-panel.md
    ├── risk-register.md
    └── venue-review-styles.md
```

## Progressive Loading

- Always read `references/review-panel.md` and `references/risk-register.md`.
- Read `references/venue-review-styles.md` when the user names a target conference or asks to compare venues.
- Read `references/example-review-mining.md` when learning from OpenReview, public reviews, accepted-paper discussions, official reviewer guidelines, or example papers.
- Read `references/memory-model.md` whenever saving or reusing venue-specific reviewer knowledge.
- Use `references/report-template.md` for full review reports.
- Verify current official reviewer guidelines and review forms when scoring or venue-specific criteria matter.

## Core Principles

- Review like a real reviewer, not like a writing coach. Focus on acceptance risk: novelty, correctness, significance, evidence, clarity, reproducibility, ethics, and fit.
- Separate fatal weaknesses from fixable presentation issues.
- Ground criticisms in the paper text, figures, experiments, proofs, and citations.
- Simulate multiple reviewer personas because one paper can receive conflicting reviews.
- Make venue and topic explicit. A theory-heavy ICLR review, empirical NeurIPS review, and CVPR benchmark review should not sound the same.
- Do not invent missing results. Mark missing evidence as risk.
- Produce actionable fixes, but keep the reviewer's objection distinct from the author's revision plan.

## Step 1 - Define Review Context

Identify:

- target venue and year
- track or subject area, if known
- paper type: method, theory, empirical study, benchmark, dataset, systems, analysis, application, or hybrid
- paper stage: outline, early draft, full draft, rebuttal, camera-ready
- review mode:
  - `quick`: top risks and predicted decision
  - `full`: multi-reviewer reviews plus meta-review and risk register
  - `adversarial`: skeptical review focused on rejection paths
  - `rebuttal`: questions and response strategy for an existing review
- available evidence: TeX source, PDF, figures, tables, appendix, experiment logs, related work, prior reviews

If the user provides no mode, default to `full` for a complete draft and `quick` for an outline or partial draft.

## Step 2 - Read Paper Evidence

Prefer primary paper files over summaries.

Look for:

- `main.tex`, `paper.tex`, `sections/*.tex`, appendix, supplement
- title, abstract, introduction, contribution list
- method/theory section, assumptions, theorem statements, algorithm boxes
- experiments, baselines, ablations, datasets, metrics, qualitative examples
- figures and tables
- related work, limitations, ethics/broader impact, checklist
- prior reviews or author notes, if available

Build this snapshot:

```markdown
## Paper Snapshot
- Target venue:
- Paper archetype:
- Claimed contribution:
- Core technical idea:
- Main evidence:
- Strongest result:
- Weakest result:
- Most likely novelty concern:
- Most likely correctness concern:
- Most likely empirical concern:
- Current missing information:
```

If the paper is incomplete, review the current stage honestly and separate "not yet written" from "scientifically weak."

## Step 3 - Learn Venue and Topic Review Style

Read `references/venue-review-styles.md`.

Then update the review context from current sources:

- official reviewer guidelines and review form
- scoring rubric and confidence scale
- ethics/reproducibility/checklist requirements
- OpenReview examples and discussions when public
- accepted/oral/spotlight papers in the same venue/topic
- reviews of similar papers, if accessible

When studying examples, read `references/example-review-mining.md` and produce a compact review-style matrix before scoring the user's paper.

Do not rely on static memory for current review forms. If exact scores or criteria matter, verify them from official sources.

## Step 4 - Configure the Reviewer Panel

Read `references/review-panel.md`.

For a full review, create 3-5 reviewers:

- `R1 Technical Specialist`: understands the method/theory deeply
- `R2 Skeptical Generalist`: asks whether the contribution matters
- `R3 Empirical/Reproducibility Reviewer`: checks experiments, baselines, ablations, statistical support
- `R4 Related Work/Novelty Reviewer`: checks positioning and missing citations
- `AC Meta-Reviewer`: synthesizes decision risk and asks what would change the outcome

Customize the panel to the paper:

- theory-heavy paper: add assumptions/proofs reviewer
- benchmark/dataset paper: add data quality/evaluation reviewer
- systems paper: add scalability/reproducibility reviewer
- application paper: add domain-validity reviewer
- CV/NLP paper: add task-specific benchmark reviewer

## Step 5 - Run Independent Reviews

Each reviewer should output:

- summary of the paper in reviewer voice
- strengths
- weaknesses
- questions for authors
- requested experiments/analysis/proofs
- score and confidence using the target venue scale when known
- likely recommendation: accept / borderline / reject

Reviewers should disagree when reasonable. Do not average away important conflicts.

For each criticism, identify:

- location in the paper
- what the reviewer is worried about
- whether the issue is evidence, clarity, novelty, correctness, positioning, reproducibility, or scope
- what would reduce the risk before submission

## Step 6 - Write Area-Chair Meta-Review

The meta-review should synthesize:

- consensus strengths
- consensus weaknesses
- polarized issues
- likely discussion dynamics
- decision risk
- what would most improve the score
- whether the paper is rejected for scientific weakness or presentation weakness

Use this decision language:

- `likely accept`
- `borderline accept`
- `borderline reject`
- `likely reject`
- `incomplete / not reviewable`

Add confidence: low / medium / high.

## Step 7 - Build Risk Register

Read `references/risk-register.md`.

Convert reviewer objections into a ranked risk register:

- `must-fix`: likely to cause rejection
- `should-fix`: materially improves acceptance odds
- `nice-to-fix`: polish or reviewer convenience
- `rebuttal-only`: cannot fix before submission but can prepare response

Each risk must include:

- reviewer concern
- evidence from paper
- severity
- probability
- fix effort
- recommended action
- owner if known

## Step 8 - Prepare Rebuttal Readiness

For top risks, produce:

- likely reviewer question
- best pre-submission fix
- fallback rebuttal answer
- evidence needed to make the rebuttal credible

If a risk cannot be fixed without new experiments/proofs, say so explicitly.

## Step 9 - Update Reviewer Memory

Read `references/memory-model.md`.

When venue examples or real reviews were studied:

1. update `.agent/reviewer-simulator/venues/<venue>.md`
2. update `.agent/reviewer-simulator/examples/<venue>-<year>-reviews.md`
3. update `.agent/reviewer-simulator/project-risk-register.md`

Memory must separate:

- observed reviewer patterns
- inferred venue review style
- risks for the current paper
- unresolved questions

Do not store long copied review text. Paraphrase review patterns and include source URLs.

If the project uses `research-project-memory`, also update:

- `memory/risk-board.md`: top simulated reviewer risks, each linked to affected claim IDs when possible
- `memory/action-board.md`: must-fix and should-fix actions, distinguishing writing fixes from new experiments/proofs
- `memory/claim-board.md`: claims likely to be weakened, cut, or reframed
- `memory/evidence-board.md`: evidence gaps, stale figures/tables, or missing proof/experiment needs
- `reviewer/.agent/reviewer-status.md`: review mode, predicted decision, and unresolved reviewer questions

Do not treat simulated reviews as real reviews. Use certainty `inferred` for predicted reviewer behavior.

## Output Modes

### Quick Review

```markdown
# Shadow Review: Quick Risk Scan
## Paper Snapshot
## Predicted Decision
## Top 5 Rejection Risks
## Fastest Fixes
## Questions Reviewers Will Ask
```

### Full Review

Use `references/report-template.md`.

### Adversarial Review

Focus on rejection paths:

```markdown
# Adversarial Review
## Strongest Reject Case
## Reviewer 2 Critique
## Fatal If True
## How To Disarm Before Submission
## Risks That Cannot Be Fixed By Writing
```

### Rebuttal Mode

```markdown
# Rebuttal Readiness
## Review Claim
## Is The Reviewer Right?
## Evidence Available
## Best Response
## Paper Revision Needed
```

## Final Sanity Check

Before finalizing:

- target venue/year and review mode are explicit
- paper archetype is stated
- reviewer criteria come from current official guidance or clearly marked memory
- example-review observations are paraphrased and source-linked
- criticisms are tied to evidence in the paper
- predicted scores include confidence and uncertainty
- top risks are ranked by acceptance impact
- fixes distinguish writing changes from new experiments/proofs
- memory updates are written when venue examples were studied
- project memory is updated when simulated risks should persist
