---
name: oss-public-knowledge-erosion
description: Applies the 2026 counterfactual simulation finding that coding agents in open-source communities shift work into private human-agent loops — direct human-to-human task completion falls from 32.4% to 11.6%, and agent-era public records cover only 22.3% of future tasks vs 81.1% for human-era records — to design agent-era OSS contribution norms, documentation policy, and maintainer defense. Use when planning open-source project AI policy, designing contribution guidelines for the agentic era, evaluating community health, or building knowledge-preservation tooling for repositories.
---

# OSS Public-Knowledge Erosion

## Overview

Zhou, Yin & Chen (Shanghai U Finance & Economics / Fudan, arXiv:2608.03585, 2026) built an LLM multi-agent simulation initialized with real GitHub data from 1,084 active developers, then branched the same community into with-agent and without-agent conditions. Coding agents boosted production (+34% planned, +39% completed tasks; median completion 45→20 min) — but at a hidden cost. Only 26% of developers adopted agents, yet agent-assisted commits reached 65% of all commits; **direct human-to-human task completion collapsed from 32.4% to 11.6%**, with 40.3% of tasks finished in private developer-agent self-loops. Worst of all: when agents queried public records to solve future tasks, agent-era corpora achieved **22.3% knowledge coverage vs 81.1%** for human-era corpora, needing 3× more retrieval steps with far lower success. The mechanism: agent-assisted work happens privately, so the explanation, debugging narrative, and design rationale that used to live in public issues/PRs/reviews never get written down. **The productivity gain is real, but the public knowledge that OSS runs on is thinning.**

## When to Use

- Writing AI/agent contribution policies for open-source projects (yours or ones you depend on)
- Designing contribution guidelines, PR templates, and review standards for agentic workflows
- Evaluating community health beyond commit counts (knowledge preservation, newcomer pathways)
- Building tooling that captures rationale into public artifacts (decision records, enriched commit messages)
- Advising foundations/companies funding OSS on what "healthy in the agentic era" means
- NOT for: private-company internal repos (different incentive structure), or as a claim that agents harm individual productivity — they demonstrably help; the issue is public-goods depletion

## Core Process / Workflow

### 1. Understand the Erosion Mechanism

```
Old path:  Dev A hits problem → asks in issue/discussion → Dev B explains
           → explanation is PUBLIC → future devs (and agents) retrieve it

Agent path: Dev A hits problem → asks agent privately → agent solves it
           → fix is committed, reasoning is PRIVATE → future devs retrieve nothing
```

The commit still lands. The **why** doesn't. OSS "social coding" — visible interaction that teaches norms, spreads expertise, and builds the reusable record — is precisely what agent loops bypass.

### 2. The Public-Knowledge Health Audit (Project Scorecard)

Score each 0–2 (healthy / partial / eroding):

| Dimension | Signal |
|---|---|
| **Rationale visibility** | Do PRs/issues contain *why* explanations, or only *what* diffs? |
| **Interaction mix** | % of tasks with visible cross-developer discussion (the 32.4%→11.6% warning) |
| **Newcomer pathway** | Can a newcomer reconstruct decisions from public artifacts alone? Test: pick a recent nontrivial PR; can someone outside the team explain its rationale from public record? |
| **Agent disclosure** | Is agent use disclosed in commits/PRs? Undisclosed agent work = invisible rationale debt |
| **Knowledge retrievability** | Search your repo for a solved-but-obscure problem from 6 months ago; how many hops to find the explanation? (Simulated analog: 2.63 → 8.02 steps) |
| **Review depth** | Are agent-generated PRs getting substantive human review, or rubber stamps? |

Any dimension scoring 0 is where erosion is live. This extends `open-source-maintainer-ai-burden` from *maintainer load* to *commons depletion*.

### 3. Countermeasure Playbook (Project-Level Norms)

1. **Rationale-in-public rule**: agent-assisted PRs must include a short human-authored rationale block (design choice, alternatives rejected, gotchas). The agent can draft it; a human must own it.
2. **Decision records as first-class artifacts**: significant changes land with an ADR-style note, regardless of who (or what) wrote the code. Cheap, greppable, survives agent loops.
3. **Enriched commit conventions**: commit message templates that prompt for context beyond the diff ("what problem, why this approach, what was ruled out").
4. **Disclose-and-review policy**: agent contribution disclosure + mandatory human review on agent-generated PRs (ties to existing `code-health-mcp-integration` and review-quality skills).
5. **Discussion-to-artifact pipeline**: valuable issue threads get distilled into docs/FAQ by maintainers or bots — convert ephemeral chat into durable public knowledge before it evaporates.
6. **Newcomer shadow-audit** (quarterly): a newcomer (or agent simulating one) attempts onboarding purely from public records; failures map the erosion.

### 4. For Consumers of OSS (Dependency Defense)

- When evaluating dependencies, check knowledge-health signals, not just stars/recency: issue-thread depth, PR discussion quality, maintainer response norms.
- Prefer projects with explicit AI contribution policies — they've at least thought about the commons problem.
- Mirror and pin critical dependencies (see `open-commons-acquisition-neutrality-2026` for the broader infrastructure-concentration argument).

### 5. Measure What Matters (Beyond Commits)

The study's deepest lesson for OSS metrics: **production ≠ health**. Track knowledge-preservation indicators alongside throughput:
- Ratio of issues/PRs containing explanatory content vs bare diffs
- Median retrieval hops for common task types (simulate: can docs+history answer X?)
- Cross-developer interaction rate per completed task
- Newcomer time-to-first-meaningful-contribution trend

## A-Tech Alignment

- **Open-source**: Direct defense of the commons — the skill exists to keep OSS's knowledge-generating interaction alive as agents industrialize contribution.
- **Practical implementation**: Scorecard + playbook + measurement are immediately adoptable by any project.
- **Community**: Aligns with `ai-agents-make-free-software-matter-again` and `community-led-growth-for-open-source-ai` — this skill adds the *knowledge-erosion* dimension those lack.
- **Privacy note**: No personal data handling; all recommendations operate on public artifacts.

## References

- Zhou, M., Yin, Y., & Chen, Y. (2026). From Social Coding to Agentic Coding: Productivity and Relational Reconfiguration in Open-Source Communities. arXiv:2608.03585. (Counterfactual branch design: 4-week warm-up on real commits, then parallel No-CA/CA simulation runs ×3 per condition; robustness across DeepSeek-V4, GLM-5.2, Qwen3.7 backbones; Public Knowledge Coverage benchmark on 8,822 held-out future commits; TF-IDF cosine similarity threshold 0.3, 10-round retrieval protocol.)
- Related existing skills: `open-source-maintainer-ai-burden`, `ai-agents-make-free-software-matter-again`, `open-source-community-flywheel`, `agent-friendly-documentation-behavior`, `comprehension-debt-framework`, `open-source-funding-crisis-defense`.
