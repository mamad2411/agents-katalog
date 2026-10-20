---
name: committed-ai-configuration-ramp-2026
description: Applies the RAMP (Repository AI Maturity Profile) four-level maturity model (arXiv:2608.25241, ASE 2026) — agents accelerate development at every level but quality degradation concentrates almost entirely in repositories that commit NO AI configuration, with the decisive gap being a few pages of committed rules/standards. Use when planning agent rollout, auditing a repo's AI setup, forecasting quality costs, writing team AI governance, or evaluating whether maturity models apply to AI-assisted development.
---

# Committed AI Configuration & RAMP Maturity 2026

## Overview

Denisov-Blanch, Agarwal, Azaletskiy, He, Schaeffer, Miranda, Vasilescu & Koyejo (Stanford/CMU/Grid Dynamics), ASE '26 (Oct 12–16 2026, Munich; arXiv:2608.25241, DOI 10.1145/3832783.3837546, CC-BY): **RAMP (Repository AI Maturity Profile)**, the first maturity model for AI-assisted development grounded in *version-controlled artifacts* rather than leadership self-assessment. Stratifying Agarwal et al.'s agent-adoption panel (509 treated repos) by RAMP level exposes a clean asymmetry: **agents accelerate commits at every level, but the quality cost (complexity, warnings) falls almost entirely on repositories that commit nothing**.

**Headline numbers** (agent-first stratum, post-adoption):

| Outcome | Level 1 (unconfigured) | Level 2+ (structured) | Ratio |
|---|---|---|---|
| Cognitive complexity | **+52.7%*** | **+26.7%*** | 2.0× |
| Static-analysis warnings | **+24.1%*** | **+14.0%** | 1.7× |
| Commits (velocity) | +37.6% | +27.5% | ~1.4× |
| Lines added | +48.1% | **+68.7%*** | 0.7× |

The four-level gradient is monotonic in the pooled sample: complexity +54.4% (L1) → +39.8% (L2) → ≈0 (L3–L4); warnings +23.0% → +16.7% → n.s. **The decisive gap is between committing nothing and committing a few pages of rules and standards** — L2 is cheap (markdown files), the L2→L3 step adds only smaller reductions.

## When to Use

- Planning an agent rollout: deciding what to commit to the repo BEFORE the first agent PR
- Auditing a portfolio of repos for AI-configuration debt (classifier-style artifact scan)
- Forecasting quality costs of agent adoption for a specific team's maturity level
- Writing team AI governance that lives in version control, not wikis
- Critically evaluating consultancies'/SEI's survey-based AI maturity models
- NOT for: repos where AI governance is enforced entirely by platform tooling outside version control (RAMP would under-score them — see caveats)

## Core Process / Workflow

### 1. Know the Four Levels (Cumulative: context → capabilities → coordination)

| Level | What exists in the repo | What it enables | Effect |
|---|---|---|---|
| **L1 Unconfigured** | No AI-related files committed | Each agent session starts from a blank slate | Baseline quality cost |
| **L2 Grounded Prompting** | Behavioral rules (CLAUDE.md, .cursorrules), tool config, architecture docs, coding standards with examples | AI is *project-aware*; outputs align with team conventions | ~½ the quality degradation |
| **L3 Agent-Augmented** | Named agents with roles/tool restrictions, reusable commands/templates, domain skills | AI performs structured, repeatable tasks via specialized roles | Further reduction (complexity ≈ 0) |
| **L4 Orchestration** | Multi-agent workflows, pipelines with phases/dependencies, session logs | Agents coordinate into end-to-end workflows with handoffs | Complexity ≈ 0; only duplication rises (+31.4% — heaviest users) |

Nine semantic categories map to the levels; a repo's level = highest level with ≥1 artifact. Guttman scalogram validation: CR = 0.997, CS = 0.983; classifier reproduces human repository-level labels 34/35 (97.1%).

### 2. Commit the L2 Package Before (or During) the First Months

Practitioner guidance from the paper:

1. **Commit a rules file** — behavioral directives that constrain every agent contribution ("never use magic numbers", "run eslint before suggesting changes are complete"). Near-universal among structured repos (98.2% of L2).
2. **Commit a coding-standards document** with before/after examples.
3. **Add basic tool configuration** (JSON/YAML/TOML) and optionally an architecture/design doc.
4. Expect this **one-time, set-and-forget** investment: 73.8% of artifacts are committed once and never modified — the initial configuration governs agent behavior for the project's life, so invest deliberately in the first version.
5. Use **starter templates/sensible defaults** tooling to lower the first-commit cost — adopters rarely move up levels later (95.9% enter at L2; 83.1% never add a second level; reversals ≈ 0; median L1→L2 latency ~441–633 days, but L2→L3 median just 154 days once it happens).

### 3. Audit by Artifact Scan (No Surveys Needed)

RAMP's key methodological advance: maturity is measurable from committed artifacts alone (43 file patterns across 12 tools + AGENTS.md/mcp.json cross-tool patterns + semantic classification via nomic-embed-1.5 or a general LLM judge). Point it at a repo portfolio to find thin configuration before rollout. Practical adaptation:

- **Embedding pipeline**: runs locally/air-gapped — use for privacy-sensitive corporate repos; share embedding vectors, not raw files, for cross-org benchmarking.
- **LLM judge**: statistically indistinguishable accuracy (81.1% vs 81.7%), simpler — default for research/practice use.
- **Remember the floor**: wiki/checklist/platform-enforced governance is invisible to a repo scan; a Level 1 label is a *lower bound* on true maturity (this attenuates, not inflates, the gap).

### 4. Interpret Outcomes by Level (Read the Averages Correctly)

Prior work reports +30–41% complexity on average — true of *neither* group once stratified (L1: +52.7%, L2+: +26.7%). For any team:

- Even **L2+ takes a real +26.7% complexity hit** — structure reduces but does not eliminate degradation; pair with review budgets and churn monitoring (see devex-verification-bottleneck-framework).
- Velocity gains appear at every level; quality costs differentiate. Measure both families of outcomes in any internal A/B.
- Honor the caveats: maturity is observational (correlated engineering discipline is a live alternative explanation); only 11% of L2+ repos committed config *before* adoption (reverse causality would *understate* the gap); Level 3–4 strata are small (n=23/40); SonarQube metrics are proxies for maintainability.

## A-Tech Alignment

- **Open source**: artifact-based measurement is itself open (replication package: Zenodo 21406147); RAMP classifiers run locally, no telemetry.
- **Data privacy**: embed-and-share-vectors pattern enables benchmarking without shipping source text; the whole instrument needs no survey and no monitoring of people.
- **Financial freedom**: the highest-ROI investment in agentic AI is *a few pages of committed markdown* — halves the most expensive quality cost. Protects small teams from "agents created slop" budget reversals.
- **Practical implementation**: levels → concrete file checklist → portfolio audit → outcome benchmarks. Directly reusable as a rollout gate: "no L2 package, no agent rollout."

## References

- Primary: Denisov-Blanch et al., "A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption," ASE '26, arXiv:2608.25241.
- Related existing skills: `agentic-coding-prior-ai-exposure-moderation` (the DiD panel this study stratifies; agent-first vs IDE-first), `ai-agent-monotonic-quality-cost` framing in `agent-induced-complexity-debt`, `comprehension-debt-framework`, `devex-verification-bottleneck-framework`, `spec-driven-development-framework` (L2/L3 artifacts are spec-like), `intent-engineering-spec-driven`.
