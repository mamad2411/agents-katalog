---
name: agentic-coding-returns-to-expertise
description: Analyzes how domain expertise (not coding proficiency) drives successful agentic coding outcomes, and how the division of labor between humans and AI agents works in practice. Use when studying agentic coding adoption, designing developer training for AI collaboration, evaluating coding agent effectiveness across skill levels, or planning team structures for agentic development. NOT for evaluating model benchmarks or IDE-only coding assistants.
---

# Agentic Coding and Returns to Expertise

## Overview

This skill captures the findings of Anthropic's large-scale empirical study of agentic coding in the wild — how developers actually use Claude Code, what predicts success, and how the human/AI division of labor shakes out across hundreds of thousands of real sessions. The headline finding challenges the intuition that better coders get more out of coding agents. Instead, **domain expertise** — knowing what to build and how to judge it — is the scarce resource that agentic coding rewards. Coding proficiency, in the traditional sense, matters far less.

The analysis draws on two primary sources:
- Hitzig et al., "Agentic Coding and Persistent Returns to Expertise" (Anthropic, June 2026)
- Wu et al., "How Do Developers Interact with AI?" (arXiv:2604.16393) — the S-IASE model and modes-of-work classification

For the detailed methodology behind the numbers cited below, see `references/expertise-returns-evidence-base.md`.

## Study Scope

- **~400,000 Claude Code sessions** analyzed
- **~235,000 unique people** (anonymized, opt-in)
- **Time window:** October 2025 – April 2026 (7 months)
- **Surfaces:** Claude Code CLI, Claude.ai, and the Claude Code desktop app. Third-party IDEs, SDKs, and headless mode (`claude -p`) are excluded — so the figures undercount total agentic coding activity.
- **Approach:** Privacy-preserving observational telemetry plus model-based classifiers (validated against telemetry) for work mode, decisions, expertise, success, and occupation. No researcher reads individual transcripts; occupation labels are never linked to identifiable users.

## The Division of Labor: What vs. How

The central structural finding is a clean split between planning and execution:

- **Humans make ~70% of planning decisions** — deciding *what* to do, scoping the task, setting constraints, and course-correcting direction.
- **Claude makes ~80% of execution decisions** — deciding *how* to implement: which files to touch, what code to write, which commands to run, how to structure the change.

This is not a 50/50 collaboration. It is a delegation pattern: the human acts as a product owner / technical director; the agent acts as an implementer. The implication for training and team design is significant — the valuable human skill is specifying intent and evaluating output, not writing the implementation.

## Expertise Amplification

Expertise shows up dramatically in how much leverage a person gets from each prompt:

| Metric | Novice | Expert | Ratio |
|---|---|---|---|
| Actions triggered per prompt | ~5 | ~12 | 2.4x |
| Output words generated per prompt | ~600 | ~3,200 | ~5x |

Experts don't prompt more often. They prompt *better* — each instruction unpacks into far more autonomous work. The multiplier compounds: a well-scoped expert prompt can trigger a long chain of file edits, tests, and command runs, while a novice prompt may only produce a small isolated edit.

Critically, the study isolates **domain expertise** (knowing the problem space) from **coding proficiency** (knowing the language/tooling). Domain expertise is what predicts the amplification effect. A domain expert who is a mediocre coder gets more out of Claude Code than a strong coder who lacks domain context. Note that expertise here is **task-specific**: a senior engineer asking their first Rust question is a beginner at that task; an accountant specifying reconciliation rules and catching edge cases is an expert at that task.

## Returns to Expertise: The Competence Threshold

The returns-to-expertise curve is concave, not linear:

- **Novice → Intermediate** gap is *larger* than the **Intermediate → Expert** gap.
- Most of the benefit of expertise is captured by reaching *competence*, not *mastery*.
- Going from "I barely know this domain" to "I can navigate it reliably" yields a big jump in agentic coding success. Going from "reliable" to "world-class" yields a much smaller marginal gain.

This has a practical implication: the investment payoff is in getting people over the competence bar, not in chasing elite expertise. Training and onboarding for agentic coding should target domain fluency, not advanced coding techniques.

## Success Rates

The study measured two outcomes:
- **Judged success:** the session appeared to accomplish what the user asked (broader, includes cases where verification was not possible).
- **Verified success:** the session produced concrete evidence of completion — passing tests, working build, demonstrable artifact.

Verified success rates by expertise tier:

| Tier | Verified Success |
|---|---|
| Novice | ~15% |
| Intermediate | ~28–33% |
| Expert | ~28–33% |

Note the flat top: intermediate and expert land in the same band. This reinforces the concave returns finding — competence buys you the success rate; extra mastery does not materially raise it.

## Occupation Matters Less Than Expertise

The study inferred users' occupations via SOC taxonomy mapping (see references) and compared verified success across occupational categories:

- **Every major occupation group is within ~7 percentage points of software engineers.**
- **Management occupations scored slightly *above* software engineers** on verified success — likely because managers bring strong domain context and clear intent specification, even if they write less code day-to-day.

This is a striking result for a coding tool. It suggests the bottleneck is not "can you code?" but "do you know what to build and can you tell if the result is right?" — exactly the skills that domain experts and managers tend to have.

## Work Composition Shift (Oct 2025 → Apr 2026)

As the user base grew and matured, the mix of work changed substantially:

| Work Mode | Oct 2025 | Apr 2026 | Trend |
|---|---|---|---|
| Debugging | 33% | 19% | ↓ sharp decline |
| Operating software | 14% | 21% | ↑ growth |
| Writing / analysis | 10% | 20% | ↑ doubled |

Interpretation: early usage was dominated by fixing broken things (debugging-heavy). Over time, users shifted toward *operating* existing software (running, configuring, extending) and *writing/analysis* (generating docs, exploring data, drafting). The tool's role moved from "fix my code" toward "help me work with software."

## Task Value

- **Average task value rose ~27% over the 7-month window.**

"Task value" reflects the judged worth of what was accomplished in a session (see references for the measurement approach). The rise suggests users are either tackling more ambitious tasks or getting better at steering the agent toward higher-value outcomes — consistent with the composition shift away from debugging and toward generative work.

## Implications

1. **Coding agents substitute for implementation work, but reward domain understanding.** The code-writing part is increasingly commoditized; the scarce skill is knowing what to build and judging whether the AI's output is correct and good.

2. **The scarce skill is judging AI output, not writing code.** Verification — reading diffs, running tests, assessing whether the result actually solves the problem — is where human value concentrates. This is a review/evaluation skill, not a production skill.

3. **Competence, not mastery, is the threshold.** Organizations get outsized returns from bringing people up to domain competence. Chasing expert-level coders yields diminishing returns under agentic workflows.

4. **Non-developers are surprisingly effective.** Management and other non-SWE occupations succeed at rates comparable to software engineers. The tool broadens who can do technical work.

5. **Team structure implications.** Teams may benefit from "domain expert + agent" pods rather than traditional "senior coder + junior implementer" hierarchies. The senior role shifts toward specification and review.

## A-Tech Alignment

For the A-Tech ethos (open source AI tools + accessible technical work):

- **Domain expertise + open-source AI tools = accessible technical work for non-developers.** If the bottleneck is domain knowledge and judgment rather than coding fluency, then open, accessible AI coding agents lower the barrier to technical contribution. A subject-matter expert with an open-weight coding agent can build, modify, and operate software without a traditional engineering background.
- **Verification as the key skill** maps well to open-source culture — code review, testing, and reproducibility are already valued practices. The agentic-coding world makes them *central* rather than peripheral.
- **The competence threshold** is encouraging for broadening participation: people don't need to become elite engineers to get real value. Reaching domain competence is enough.
- **Open-weight / open-source coding agents** (e.g., self-hosted or local models with agentic tooling) extend this accessibility to contexts where proprietary tools are unavailable or undesirable — aligning with open-source-first development.

## Related Topics / Extensions

- **Training developers for AI collaboration:** designing curricula around intent specification and output verification rather than syntax.
- **Team structures for agentic development:** how to compose pods, divide review responsibilities, and onboard non-developers into technical work.
- **Open-source coding agent landscape:** comparing open-weight agentic tools (e.g., Aider, OpenHands,Continue, local-model setups) against the proprietary baseline measured here.
- **Verification tooling:** the emerging stack for judging AI-generated code (test generation, diff review aids, automated sanity checks).

## When to Use This Skill

- Studying real-world agentic coding adoption and outcomes
- Designing developer training or onboarding for AI-collaboration workflows
- Evaluating coding agent effectiveness across skill levels or occupations
- Planning team structures for agentic development
- Arguing for domain-expise investment over raw coding proficiency
- Contextualizing open-source coding agent value propositions

## When NOT to Use This Skill

- Evaluating model benchmarks or leaderboards (use a benchmarking skill instead)
- Reviewing IDE-only autocomplete assistants (e.g., Copilot inline completion) — this study covers agentic, multi-step CLI coding, not single-line suggestions
- Making claims about closed-source vs. open-source model quality — the data here is Claude Code-specific; generalize carefully

## Source Provenance

- **Primary:** Hitzig et al., "Agentic Coding and Persistent Returns to Expertise," Anthropic, June 2026.
- **Supporting:** Wu et al., "How Do Developers Interact with AI?" arXiv:2604.16393 (S-IASE model, modes-of-work classification).
- **Methodology details:** `references/expertise-returns-evidence-base.md`