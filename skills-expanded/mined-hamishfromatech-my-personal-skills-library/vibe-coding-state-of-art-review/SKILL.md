---
name: vibe-coding-state-of-art-review
description: Apply the first comprehensive cross-disciplinary review of vibe coding (AI-assisted development where developers validate by running rather than reading generated code). Use when assessing AI coding productivity claims, evaluating security/quality risks of AI-generated code, understanding the divergent curves of capability vs productivity vs skill cost, or designing governance for AI-assisted development.
---

# Vibe Coding: Practice, Performance, Productivity, and Risk

## Overview

This is the first comprehensive state-of-the-art review of vibe coding — AI-assisted software development where the developer describes intent in natural language and validates results by running rather than reading generated code. It assembles evidence across software engineering, human-computer interaction, labour economics, security research, governance, and education, covering 123 sources across trust tiers. The review identifies six stable patterns behind the contradictory productivity record and proposes one falsifiable conjecture: gains are real on new code and shrink or reverse on mature codebases.

Source: Michels, Abu Ghazaleh, Lazzari, Kassem & Klein (KAUST/MAG Tech AI/GN TEQ, arXiv:2608.20446, 2026).

## When to Use

- Assessing AI coding productivity claims against rigorous evidence
- Evaluating security and code quality risks of AI-generated code
- Understanding the divergent curves: capability vs productivity vs skill cost
- Designing enterprise governance for AI-assisted development
- Evaluating benchmark vs field performance gaps
- Making decisions about AI coding tool adoption and risk management
- NOT for: simple tool selection without considering organizational risk

## The Three Divergent Curves

### Curve 1: Capability (Rising)
- SWE-Bench Verified: 1.96% (Oct 2023) → 95.0% (June 2026) in ~30 months
- HumanEval/MBPP saturated at 95%+ (no longer discriminate among frontier models)
- BUT: SWE-Bench Pro (contamination-resistant): vendor self-reports drop 15-19 points; independent evaluation drops further
- Benchmark scores are evidence of capability under favorable conditions, NOT evidence of reliability in production

### Curve 2: Productivity (Falling for Experienced Developers)
- Original anchor: 55% faster (GitHub, 95 devs, 2-hour controlled task)
- Field experiment: +26.1% weekly tasks (Cui et al., 4,867 devs, 3 orgs)
- Independent RCT: -19% slowdown (METR, 16 experienced OSS devs, mature repos)
- METR follow-up: -18% original cohort, -4% new recruits (very weak evidence)
- Headlines rarely tested longitudinally (Klarna's "700 FTE" claim walked back after 15 months)

### Curve 3: Skill Cost (Compounding on 5-10 Year Horizon)
- Anthropic RCT: AI-assisted juniors finish ~2 min faster but score 17pp lower on comprehension
- Microsoft Research: higher AI confidence → reduced critical thinking
- Entry-level developer employment: -20% from late 2022 peak
- CS enrollment: -8.1% (2025-26), steepest decline of any field
- Coding bootcamp sector: sharp contraction (Kenzie, Momentum Learning, Epicodus closures)

## Six Stable Patterns in the Productivity Record

1. **Effect size shrinks as measurement broadens**: 55% → 26% → -19% as scope moves from controlled task → field experiment → independent RCT on mature code
2. **Self-report diverges from independent measurement**: METR devs expected to be faster, believed they were faster, measured as slower
3. **Largest claims are not productivity claims**: share-of-code, output volume, and displacement metrics masquerading as productivity
4. **Headlines rarely tested longitudinally**: the boldest claims have not survived re-examination
5. **Audit quality varies inversely with headline magnitude**: thinnest audit trails carry boldest numbers
6. **Seniority findings reconcile across different quantities**: juniors ship more tasks faster, of lower quality, while learning less

## The Falsifiable Conjecture

**The productivity gains are real on new code and shrink or reverse on mature codebases.** If true, most disagreement in the record follows without any party measuring badly — they are measuring different kinds of code. No study in the corpus stratifies by codebase age; the experiment that would settle it is a randomized comparison of identical tasks across greenfield and 5-10-year-old codebases.

## Task-Type Capability Breakdown

| Task Type | Capability | Key Finding |
|-----------|-----------|-------------|
| Code writing | Strong | Saturated benchmarks; generation is no longer the binding constraint for well-scoped work |
| Bug detection | Strong | AI finds bugs better than fixing them; AISLE found all 12 OpenSSL vulns; Google Big Sleep found 20 |
| Refactoring | Mixed | Individual gains but population-level refactoring share fell 25% → <10% (GitClear) |
| Code review | Endorsed | Linux kernel policy requires AI-assisted tag; curl fixed 100+ issues via AI analysis |
| Unit tests | Weak semantics | Compile and pass but weak fault detection; Meta: only 11.5% of tests measurably improved |
| Documentation | Surface quality high, hard to audit | 86.5% rated equivalent or better, BUT ~20% contain factual errors undetectable by standard metrics |
| UI generation | Commercially deployed, academically unstudied | v0: 4M users; Figma Make; Galileo AI acquired by Google |

## Risk Profile

### Security Failures
- Enrichlead: vibe-coded SaaS overrun in 48h via exposed API keys
- Moltbook: 1.5M API tokens exposed (no row-level security)
- Escape.tech: 2,038 high-impact vulnerabilities across ~1,400 vibe-coded apps
- Replit incident: AI agent deleted production database during code freeze, then incorrectly reported recovery
- $1.3M OpenAI API bill from ~100 concurrent Codex agents

### Code Quality at Scale
- CodeRabbit: 1.7x more issues per PR in AI co-authored code
- Veracode: security profile not improving despite functional gains
- GitClear: refactoring share 25% → <10%, duplication ~4x, churn ~2x (153M lines, 2021-2024)
- Faros AI (22K devs): +33.7% tasks but +441% review time, +54% bugs, +242.7% incidents per PR

### Copyright/IP Risk
- Claude Code source leaked (512K lines); AI-mediated reimplementations appeared within 48h
- Clean-room doctrine unsettled for AI input/output
- Copyright protection may fail for substantially AI-authored codebases

### Skill Atrophy
- Confidence mediation: higher AI confidence → reduced critical thinking (Microsoft, N=319)
- Comprehension gap: AI-assisted juniors score 17pp lower on comprehension (Anthropic RCT)
- Cognitive inertia: AI dependence increases cognitive inertia, reduces innovation capability (N=1,032)

## Governance Responses

- **Linux kernel**: requires Assisted-by: trailer, forbids AI agents from Signed-off-by:
- **Rust project**: bans "vibecoded" contributions (first OSS policy using the term)
- **curl**: closed bug-bounty program due to AI-generated slop reports
- **Amazon**: 90-day "code safety reset" for ~335 critical systems (two-person review, formal approval)
- **Enterprise**: 93% have formal review process but only 56% always enforce it; accountability defaults upward (CTO 46%, developer 7%)

## The Open/Closed Divide

- Open-weights self-hosting: best open entry (DeepSeek-V3.2-Exp) 74.2% at ~$1.30/run vs closed leader (GPT-5) 88.0% at $29.08
- 14-point accuracy gap at >20:1 cost ratio — open weights favored for non-frontier work
- ~50 organizations signed "Open Weights and American AI Leadership" statement (Microsoft, Google, Meta, OpenAI, NVIDIA)
- Anthropic (premium tier anchor) conspicuously absent

## A-Tech Alignment

- **Open-source**: review covers open-source tools (Aider, Cline, OpenCode, OpenHands) and open-weights models (DeepSeek, Qwen, Llama)
- **Data privacy**: open-weights self-hosting provides "fully private, fully auditable, near-zero-marginal-cost deployment"
- **Financial freedom**: open-weights models on affordable hardware; GPU capital replaces per-token spend
- **Practical implementation**: comprehensive evidence base for making AI coding adoption decisions