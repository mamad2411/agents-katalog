---
name: core-peripheral-developer-agent-usage
description: Applies empirical evidence on how core and peripheral developers differ in their use of coding agents across the PR lifecycle. Use when [designing agent rollout strategies, understanding experience-based adoption patterns, optimizing agent-assisted code review workflows].
---

# Core vs. Peripheral Developer Agent Usage Across the PR Lifecycle

## Overview

Coding agents do not flatten the social structure of open-source development. This skill captures the findings of Cynthia, Das & Roy (MSR '26), a large-scale empirical study of how **core** and **peripheral** developers differ in their use of coding agents across the full pull-request lifecycle — from the tasks they delegate, to how their work is reviewed, to whether it passes CI before merging. The headline finding is that contributor reputation and reviewer rigor persist even when both groups delegate implementation to agents, and that agents are primarily absorbing "toil" tasks (documentation, testing) rather than displacing core engineering judgment.

The study analyzes **9,427 agentic PRs** from **1,701 developers** across **1,391 public GitHub repositories**, examining four research questions spanning usage frequency/purpose, review dynamics, modifications, and CI verification. For the detailed evidence behind every number cited below, see `references/evidence-base.md`.

## Study Scope

- **9,427 agentic pull requests** (PRs created with AI coding agent involvement)
- **1,701 developers** classified as core or peripheral based on repository contribution history
- **1,391 public GitHub repositories** (open-source projects)
- **Source:** Cynthia, Das & Roy, "Core vs. Peripheral Developers: How Do They Use AI Coding Agents Differently?" (MSR '26, arXiv:2601.20106)
- **Classification:** Core developers are maintainers or high-frequency contributors with merge privileges and sustained commit history; peripheral developers are occasional/external contributors without maintainer status
- **Methodology:** Quantitative analysis of PR metadata, review comments, modification patterns, and CI outcomes across the four RQs (see references for full methodology)

## When to Use

- Designing agent rollout strategies that account for contributor experience levels (core vs. peripheral)
- Understanding experience-based adoption patterns and why a subset of peripheral developers become agent "power-users"
- Optimizing agent-assisted code review workflows (who reviews, what they flag, how rigor differs)
- Evaluating whether coding agents flatten or reinforce existing contributor hierarchies in OSS projects
- Planning CI/verification policies for agent-generated contributions
- Assessing the long-term skill-formation risks of agent delegation for less-experienced contributors

## When NOT to Use

- Evaluating IDE-only autocomplete assistants (Copilot inline completion) — this study covers agentic, multi-step PR-level work
- Making claims about proprietary/closed-source development contexts — the data is from public GitHub OSS projects
- Benchmarking individual agent models or comparing agent quality — this is about developer behavior, not model performance
- Evaluating non-coding AI agent use (e.g., research, writing, design agents)

## Core Findings

### RQ1 — Usage Frequency and Purpose

Both groups adopt agents at comparable baseline rates, but the *distribution* differs significantly:

| Metric | Core Developers | Peripheral Developers |
|---|---|---|
| Median agentic PRs per dev | 2.0 | 2.0 |
| Mean agentic PRs per dev | 3.73 | 6.08 |
| Agentic PRs merged to main/master | 85.8% | 77.8% |

**The mean/median divergence reveals a power-user subset.** A subset of peripheral developers uses agents disproportionately more often (mean 6.08 vs. median 2.0), pulling the mean well above the core developer mean (3.73). These peripheral "power-users" may be compensating for skill gaps through agent delegation — a pattern with both short-term productivity benefits and long-term learning risks.

**Task delegation patterns diverge by group:**

- **Peripheral developers** delegate evenly across task types — bug fixing (~19.8%), feature addition (~19.3%), documentation (~18.7%), testing (~18.9%). Their agent use is broad and undifferentiated.
- **Core developers** concentrate agent use on **documentation (20.9%)** and **testing (21.8%)** — the "toil" tasks that developers view as low-satisfaction but necessary. They reserve their own effort for higher-judgment work (bug fixing, feature design).

**Interpretation:** Agents are absorbing the tedious, low-satisfaction work that core developers would rather not do manually. Peripheral developers, by contrast, use agents across the board — including for tasks where core developers prefer to maintain direct control.

### RQ2 — Review Dynamics

| Metric | Core Developers | Peripheral Developers |
|---|---|---|
| Median review comments per PR | 3.6 | 2.0 |
| Primary review focus | Alternative solution approaches | Code organization |
| Evolvability issues raised | 52.8% | 59.3% |

**Core developers engage more rigorously in review discussions** — nearly twice the median comment count per PR (3.6 vs. 2.0). This persists even for agent-generated PRs, meaning core developers do not relax their review standards when an agent produced the code.

**Both groups primarily raise evolvability concerns** (maintainability, future-change-ability), but the focus differs:
- **Peripheral developers** flag code organization issues (structure, modularity, where things should live)
- **Core developers** flag alternative solution approaches (whether the chosen approach is the right one — a higher-level architectural judgment)

**Core developers function as quality gatekeepers.** Their higher engagement, focus on solution approach rather than surface organization, and greater CI rigor (see RQ4) collectively indicate that they apply more rigorous standards to agent-generated code — and to all code. The agent does not displace this role.

### RQ3 — Modifications to Agentic PRs

| Metric | Core Developers | Peripheral Developers |
|---|---|---|
| Agentic PRs accepted without modification | ~74.1% (both groups) | ~74.1% (both groups) |
| Mean added lines (when modified) | 55.4% | lower |
| Mean deleted lines (when modified) | 38.2% | lower |

**Most agent-generated PRs are accepted as-is** — 74.1% across both groups, indicating that agents produce work that is generally "good enough" to merge without further human editing.

**When modifications do occur, both groups commonly refactor.** Beyond that common ground, the modification types diverge:
- **Peripheral developers** also fix bugs in agent-generated code
- **Core developers** also improve documentation — extending the agent's output with better explanations

**Core developers make larger modifications** when they do intervene — higher mean added (55.4%) and deleted (38.2%) lines. This is consistent with their role as quality gatekeepers: when they touch agent output, they make more substantial changes, often restructuring or expanding the contribution.

### RQ4 — CI Verification

| Metric | Core Developers | Peripheral Developers |
|---|---|---|
| CI success rate on agentic PRs | 51.2% | 43.1% |
| Merged without running any checks | 11.2% | 19.1% |

**Core developers follow the "all checks must pass" principle more consistently.** They require passing CI more often (51.2% success rate vs. 43.1%) and are far less likely to merge agent-generated PRs without running any checks at all (11.2% vs. 19.1% — peripheral developers are nearly twice as likely to skip verification).

**Interpretation:** The CI gap is one of the most actionable findings. Peripheral developers — who are also more likely to be the agent "power-users" — are the group most likely to merge unverified agent output. This creates a compounding risk: less-experienced contributors, using agents more heavily, with less verification rigor. Projects relying on peripheral agent contributions should consider mandatory CI gates for agent-generated PRs.

## Key Implications

1. **Socio-technical factors persist under agentic workflows.** Contributor reputation continues to matter: core developers' agentic PRs merge at 85.8% vs. peripheral's 77.8%. Agents do not democratize access to merge decisions — the reputation effect holds even when the code is agent-generated.

2. **Agents absorb "toil," not judgment.** Core developers delegate documentation and testing — tasks with low creative satisfaction but high necessity. They retain direct control over bug fixing and feature work. This suggests agents are best understood as toil-absorbers within expert workflows, not as replacement engineers.

3. **The peripheral power-user risk is real.** A subset of peripheral developers uses agents at high rates (mean 6.08 PRs) across all task types, including bug fixing and feature work. If agents become a crutch that substitutes for skill development, these contributors may plateau — productive in the short term but blocked from becoming core developers because they never build the underlying judgment.

4. **Core developers remain essential quality gatekeepers.** Higher review engagement, focus on solution approach, larger modifications when intervening, and stronger CI adherence all point to the same conclusion: in agentic workflows, the core developer's role shifts toward review and verification, but does not diminish in importance.

5. **CI policy is the highest-leverage intervention.** The 19.1% no-checks merge rate for peripheral developers is the clearest actionable risk in the data. Projects should require CI passage on all agent-generated PRs regardless of contributor status, and should especially not relax CI requirements for peripheral agent contributions.

## A-Tech Alignment

- **Open source (OSS focus):** The study uses public GitHub data from 1,391 OSS repositories. Findings directly inform how open-source projects should structure agent contribution policies, review workflows, and CI gates — core A-Tech territory.
- **Data privacy:** Analysis uses PR metadata (commits, comments, CI status) — publicly visible repository artifacts — not developer surveillance or private telemetry. No individual developer monitoring.
- **Financial freedom:** Understanding adoption patterns by contributor type enables better product strategy for open-source tooling — knowing who your power-users are and what risks they face informs tool design and go-to-market.
- **Practical implementation:** 9,427 PRs and 1,701 developers yield specific, per-group recommendations (not vague generalizations). The findings translate directly into actionable CI policies, review guidelines, and onboarding strategies.

## Recommended Actions by Developer Group

### For Core Developers
- Continue delegating toil (documentation, testing) to agents; reserve judgment work for yourself
- Maintain review rigor on agent-generated PRs — do not relax standards for agent output
- When modifying agent PRs, focus on solution-approach critique and architectural improvements
- Enforce "all checks must pass" on your own agent-generated PRs as a modeling behavior

### For Peripheral Developers
- Be cautious of over-reliance on agents for bug fixing and feature work — these build the judgment needed to become a core contributor
- Use agents for toil and scaffolding, but manually review and understand the generated code before merging
- Always run CI before merging agent-generated PRs — do not skip verification
- Treat agent output as a draft, not a finished product, especially for tasks outside your expertise

### For Project Maintainers
- Require CI passage on all agent-generated PRs regardless of contributor status
- Do not relax review standards for agent-generated PRs — the 74.1% no-modification rate means most agent PRs pass, but the 25.9% that need changes need *rigorous* review
- Watch for peripheral "power-users" who submit many agent-generated PRs — provide mentorship to ensure they are building underlying skills, not just generating volume
- Consider labeling agent-generated PRs (e.g., `agent-assisted` label) so reviewers can calibrate their review approach

## Cross-References

- `cli-agentic-coding-adoption-impact` — How CLI coding agents spread through social networks; the +24% PR lift finding complements this skill's core/peripheral usage analysis
- `agentic-coding-returns-to-expertise` — Domain expertise (not coding proficiency) drives agentic coding success; explains why core developers get more value from agents even when both groups delegate
- `ai-engineering-culture-amplifier` — How AI tools amplify existing engineering culture rather than flattening it; this study's reputation-persistence finding is a concrete instance
- `botsitting-botshitting-cycle` — The cycle of over-trusting then over-policing agents; the CI verification gap (19.1% no-checks) is a botshitting risk vector
- `human-oversight-agentic-systems-practice` — Four forms of oversight work; core developers' review behavior maps to post hoc review and the "quality gatekeeper" pattern

## Source Provenance

- **Primary:** Cynthia, Das & Roy, "Core vs. Peripheral Developers: How Do They Use AI Coding Agents Differently?" MSR '26, arXiv:2601.20106
- **Scale:** 9,427 agentic PRs, 1,701 developers, 1,391 repositories (public GitHub)
- **Methodology details:** `references/evidence-base.md`