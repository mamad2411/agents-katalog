---
name: analyze
description: Conduct structured analysis on any problem using CIA/IC analytic techniques — assess competing hypotheses, challenge assumptions, stress-test judgments, and produce defensible evidence-based assessments with full citations. Supports 18 techniques including ACH, Key Assumptions Check, What-If, Premortem, Cross-Impact Matrix, Contrasting Narratives, Devil's Advocacy, Red Hat Analysis, Alternative Futures, and Deception Detection.
argument-hint: "[technique or flags, e.g. ach, --guided, --no-osint]"
allowed-tools: Task, Read, Write, Glob, Grep, Bash, WebSearch, WebFetch, mcp__firecrawl__firecrawl_search, mcp__firecrawl__firecrawl_scrape
---

# Structured Analysis Skill

Apply CIA/IC Structured Analytic Techniques to produce defensible, evidence-based analytical assessments. Every claim must be cited. Every judgment must trace to technique outputs.

## Invocation

```
/structured-analysis:analyze                          → Adaptive mode (auto-select techniques)
/structured-analysis:analyze <technique>              → Direct mode (run one technique)
/structured-analysis:analyze --guided                 → Guided mode (walk through all phases)
/structured-analysis:analyze --resume <analysis-id>   → Resume or update existing analysis
/structured-analysis:analyze --iterate <analysis-id>                → Re-run full analysis with new evidence
/structured-analysis:analyze --iterate <analysis-id> <technique>    → Re-run specific technique(s)
/structured-analysis:analyze --lean                   → Lean mode (abbreviated technique set)
/structured-analysis:analyze --comprehensive          → Comprehensive mode (full rubric, adversarial + deception checks)
/structured-analysis:analyze --no-osint               → Disable web research
```

> Commands use the plugin (namespaced) form `/structured-analysis:analyze`. If the skill is loaded un-namespaced, drop the prefix and use the bare `/analyze`.

Techniques: `customer-checklist`, `issue-redefinition`, `restatement`, `brainstorm`, `kac`, `ach`, `inconsistencies`, `cross-impact`, `what-if`, `premortem`, `counterfactual`, `narratives`, `bowtie`, `opportunities`, `devils-advocacy`, `red-hat`, `alt-futures`, `deception`

Flags combine: `/structured-analysis:analyze --guided --no-osint` is valid.

## Execution

**You MUST read the orchestrator protocol before proceeding.** It contains mode routing, technique selection logic, and the technique routing table.

### Step 0 — Context Inference

Before parsing explicit arguments, scan the conversation history for implicit inputs. Users often invoke `/structured-analysis:analyze` mid-conversation after discussing a problem, providing data, or sharing links.

Extract from conversation context:
- **Problem statement**: What is the user trying to analyze? Look for questions, concerns, scenarios, or decisions under discussion.
- **Implicit technique hints**: Did the user mention assumptions, hypotheses, competing explanations, risks, or scenarios? Map these to techniques (e.g., "I'm not sure which explanation is right" → ACH, "what could go wrong" → Premortem).
- **Implicit flags**: Did the user indicate they want something quick (→ `--lean`), don't want web research (→ `--no-osint`), or want to walk through everything (→ `--guided`)?
- **Prior analysis**: Are there existing analyses in `analyses/` for the same topic? (→ suggest `--resume` or `--iterate`)
- **Evidence already provided**: Files shared, URLs pasted, data discussed — these become Tier 1/2 evidence.

### Step 0.1 — Validate Assumptions

If context inference produced any results, present them to the user for confirmation before proceeding:

```
Based on our conversation, here's what I'm picking up:

**Problem**: [inferred problem statement]
**Mode**: [inferred mode + rationale]
**Techniques**: [inferred techniques, if any]
**Flags**: [inferred flags, if any]
**Prior context**: [files, data, or evidence already in conversation]

Does this look right? Adjust anything before I proceed.
```

If the user provided explicit arguments, those always take precedence — but still surface any useful context (e.g., "You asked for ACH. I also noticed you shared [file] earlier — I'll include that as evidence.").

If no conversation context exists and no arguments were provided, proceed directly to Adaptive mode (the orchestrator will prompt for a problem statement).

### Steps 1–6 — Main Execution

1. Read `protocols/orchestrator.md` (relative to this skill's directory)
2. Parse explicit arguments → determine mode and flags (merge with Step 0 inferences, explicit args win)
3. Follow the orchestrator's instructions for the detected mode
4. For technique execution, follow the orchestrator's Technique Execution Contract:
   - **1 technique** (Direct mode): Execute in-context — read protocol, read template, execute SETUP → PRIME → EXECUTE → ARTIFACT → FINDINGS → HANDOFF, write artifact to `analyses/<id>/working/`
   - **2+ techniques**: Dispatch to background subagents in dependency-aware tiers — each subagent reads protocol/template, executes the technique, writes the artifact, and returns only a compact findings summary. Main context accumulates summaries and file paths, not full technique work.
5. For evidence gathering: read and execute `protocols/evidence-collector.md`
6. For report synthesis: dispatch per `protocols/report-generator.md` Phase A/B architecture

## Self-Correction (3 Layers)

- **Layer 1** (after each technique, silent): Protocol compliance check — all steps completed? All template sections filled? No unfilled `{{PLACEHOLDER}}` tokens?
- **Layer 2** (before report, silent): Analytical self-critique — 8 checks:
  - 3a. Assumption audit
  - 3b. Evidence balance
  - 3c. Confidence calibration
  - 3d. Alternative check
  - 3e. Missing voices
  - 3f. Internal consistency audit (cross-artifact validation)
  - 3g. Analytical bias scan (sycophancy, anchoring, vividness, completion, authority)
  - 3h. Quality score (quantitative 1-5 with pass/fail threshold)
- **Layer 3** (before finalization): Human review gate — present summary (including quality score), incorporate feedback
- **Auto-Remediation Gate** (between Phase A and Phase B): HIGH-severity Layer 2 flags (evidence imbalance >2:1, unstated critical premises, strong counter-arguments, sycophancy/anchoring bias, quality score < 3.0) trigger automatic remediation — the orchestrator invokes the iteration handler to collect targeted evidence, re-run flagged techniques (max 3), and regenerate the report before the user sees it. Capped at 1 cycle. Zero overhead when no HIGH flags exist.
- **Critique-to-Iteration Bridge** (after results): Remaining MEDIUM/LOW flags from Layer 1 and Layer 2 are mapped to specific technique re-runs and evidence collection focuses, presented as ready-to-run `/structured-analysis:analyze --iterate` commands. Only fires when actionable flags exist beyond what auto-remediation already addressed. All flags and their statuses are written to `next-steps.md` in the analysis root — a standalone ledger tracking OPEN, REMEDIATED, RESOLVED, and DEFERRED items across iterations. The `--iterate` handler reads this file as its primary input.

## Citation Requirement

Every claim in every artifact must be cited. No exceptions. Citation methods:
- **OSINT**: `[Source](URL)` — Retrieved: YYYY-MM-DD
- **FILE**: `[filename:line_range]`
- **USER**: `[User-provided, session context]`
- **ANALYSIS**: `[Derived via technique_name]`
- **PRIOR-ITERATION**: `[PRIOR-v{N}: technique_name]`

OSINT is never presented as fact — always "according to [source]".

## Reference Library

For deep background on any technique, read `docs/library/00-prime.md` and the specific library files referenced in each protocol. The library contains the full theoretical foundation, axioms, selection matrices, and empirical critiques underlying this skill.
