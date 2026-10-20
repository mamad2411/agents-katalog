---
name: rust-maintainers-in-residence-2026
description: Applies the Rust Foundation Maintainers in Residence (MiR) program (RFC 3931; announced Aug 26 2026; $350,000 from Google, AWS, OpenAI, and the Rust Project Leadership Council funding six maintainers at full/half/one-day-per-week rates) as the first production-grade EMPLOYMENT model for critical open-source maintenance — a Project-controlled Funding Team hires maintainers who must be existing team members, with flat published pay, 50/50 team-priority vs self-directed time, and sponsor-undirected funding. Use when [designing funding programs for critical open-source infrastructure, comparing sponsorship vs employment vs endowment models for maintainers, writing a maintainer-fund RFC or governance charter, or evaluating whether a language/eco-system foundation can sustain paid maintenance]. NOT for [one-off bounties or project-scoped contracts, corporate open-source-program-office sponsorship with strategic messaging, or small projects with no team structure to integrate a paid maintainer into].
---

# Maintainers in Residence: The Employment Model for Critical OSS Maintenance

## Overview
The Rust Foundation Maintainers Fund (RFMF) reached $350,000 in August 2026 (Google, AWS, OpenAI, and the Rust Project Leadership Council) and its first cohort funds six maintainers at three commitment tiers: Gen Li (full-time, Rustup), Alejandra González (half-time, Clippy), Chris Denton (half-time, stdlib/compiler/Rustup/Windows), León Liehr (half-time, rustdoc/compiler), plus Maintainer Grants to Jonas Böttiger (std) and Jason Newcomb (Clippy). The structural insight: RFC 3931 routes funds into the Leadership Council's Project Priorities budget but *restricts* them to programs that pay individual maintainers — the fund's value proposition to sponsors is that every dollar goes into a maintainer's pocket. This completes the library's OSS-funding series (endowment → co-ops → MiR employment) with the first long-term salaried role at scale, and the RFC is explicit that *sustained presence* — not grant-style scoped work — is the core value proposition, because review backlogs and cross-team refactors need deep context, not project-scoped interventions.

## The Evidence Base
- **Rust RFC 3931** (`rust_foundation_maintainer_fund`, Feb 23 2026; PR rust-lang/rfcs#3931): defines the RFMF–Project relationship, the Funding Team charter, the MiR role, sponsor benefits and forbidden benefits.
- **Rust Foundation announcement (Aug 26 2026)**: $350K raised; six funded maintainers; contracts for ≥12 months.
- **Motivating evidence from team interviews:** rust-analyzer's PR backlog was ~10 when a funded reviewer was working on it, then climbed to **over 110** when that person changed jobs. Clippy's 6-month Foundation grant showed short-term funding enables but doesn't sustain long-term plans ("hard to make long-term plans"). The Clippy team also cites a ~300-PR backlog target.
- **Prior art cited in the RFC:** PSF Developer-in-Residence (2021; 3 funded maintainers by 2026; the "self-directed time made all the difference" lesson after ~5 years), Django Fellowship (weekly reports; running since 2014 — the longest track record), Zig Software Foundation (92% of spend directly to contributors), Scala Center (pool-funded with sponsor Advisory Board).

## Core Findings (the four design rules)
1. **Fund sustained presence, not scoped projects.** The maintenance problems teams report (review backlogs, cross-team blocking, multi-month refactors) require people with deep context who stay. Short grants keep the lights on but stall strategic work.
2. **Dedicate the fund; publish the rate.** "Dedicated to maintainers" is the pitch; flat published pay avoids negotiation asymmetry and the perception of unequal valuation for equivalent work.
3. **50/50 split between team priorities and self-selected work.** The PSF's 5-year lesson: pure-maintenance-only roles burn out ("not much joy in that"); allowing feature work alongside maintenance is what makes the role sustainable.
4. **Sponsors fund, projects select.** Sponsors get impact reports, sponsor meetings, and priority review — never the ability to unilaterally direct a maintainer's work or pick who joins a team. That governance rule is what keeps the fund's neutrality credible.

## When to Use
- Designing funding for a critical project with an existing team structure (compiler, framework, database, language runtime).
- Comparing employment vs sponsorship vs endowment for maintainer sustainability.
- Building the sponsor pitch: the restriction to maintainer-pay is the value proposition.
- Evaluating whether a language ecosystem can sustain salaried maintenance.

## NOT For
- Bounties for specific features (that's the Project Goals Funding program's job, per the RFC).
- Projects with no team structure (a MiR must be a team member with permissions — this is a hard requirement).
- Companies who want to hire maintainers directly for feature work (companies are explicitly told RFMF is for maintenance, not features).

## Core Process / Workflow
1. **Diagnose the maintenance gap.** Interview team leads: what's the maintenance baseline (minimum healthy maintainer count) per team, and how far are you from it? Which teams are critically underfunded AND high-impact?
2. **Establish the fund.** Foundation (legal entity, bank account) + Project (knowledge of team health, member vetting). Neither can operate the program alone — it's a partnership.
3. **Define the Funding Team.** Members appointed by top-level teams; affiliation limits (no more than 1 rep from any one company if ≤5 members; 2 if ≥6) prevent capture.
4. **Set the employment structure.** Full-time / half-time / ~1-day tiers; flat rates published with the open call; termination period or severance required.
5. **Run the open call.** Applications require (1) project background, (2) availability, (3) proposed work. Selection criteria: technical depth in the area, community trust, sustained-work orientation (track record for review/mentorship/deep-context work).
6. **Contract with a termination period.** Funded maintainers are existing team members (or approved for membership upon starting). No separate contributor class — they're team members who now have capacity.
7. **Split time 50/50.** Team priorities (reviews, mentoring, triage, refactors) + self-selected passion projects. The PSF evidence says the self-directed half is what prevents burnout.
8. **Report and renew.** Impact reports to sponsors; funding decisions stay with the Funding Team; sponsors never direct work.

## A-Tech Alignment
- **Open source:** the third leg of the OSS-sustainability tripod after `oss-endowment-and-coop-funding-2026` (perpetual grants) and `agentic-oss-economics-2026` (economic mechanism analysis) — this is the employment model.
- **Privacy:** N/A — funding governance, not a data architecture.
- **Financial freedom:** direct precedent for "get paid to maintain the tool you already maintain" — the model Hamish's content repeatedly advocates for maintainers seeking financial freedom from their passion project.
- **Practical:** the RFC's day-to-day Funding Team responsibilities, affiliation limits, sponsor-benefit tiers, and the PSF's 50/50 time-split lesson are directly actionable for any ecosystem.

## References
- Pairs with: `oss-endowment-and-coop-funding-2026` (endowment + co-op — the structural complement), `agentic-oss-economics-2026` (why engagement compensation matters), `open-source-maintainer-ai-burden` (the workload context), `community-monetization-ladder` (funding-stage taxonomy), `sovereign-tech-fund-causal-impact` (money raises velocity but not contributor counts — MiR addresses that).