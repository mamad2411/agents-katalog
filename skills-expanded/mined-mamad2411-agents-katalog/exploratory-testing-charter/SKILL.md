---
name: exploratory-testing-charter
description: Plan and execute time-boxed exploratory testing sessions using SBTM (Session-Based Test Management) charters with goals, areas, oracles, and debrief. Use to find bugs systematic scripts miss.
source: self
date_added: 2026-05-01
---

# Exploratory Testing Charter

Exploratory testing is **simultaneous learning, design, and execution**, made accountable by Session-Based Test Management. Charters give exploration shape; debriefs convert findings into tests, risks, and patterns.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Method | SBTM (Bach/Bolton), Heuristic Test Strategy Model (HTSM) |
| Time-box | 60–120 min sessions, 1 charter per session |
| Capture | Markdown notes, Loom/OBS recording, Polarion / Xray / TestRail "exploratory session" |
| Oracles | Spec, comparable products, prior version, internal consistency, claims, statutes |
| Heuristics | SFDIPOT, CRUSSPIC STMPL, FEW HICCUPPS, RIMGEA |
| AI assistance (2026) | LLM-driven test idea generation (Bach's *Rapid Software Testing*-style prompts), AI bug triage/classification |

## When to Use

- New feature reaching beta.
- After a refactor with broad blast radius.
- When automated suite is green but stakeholders feel risk.
- Onboarding — fastest way for a tester to learn an area.
- Preparing risk-based test plans by surfacing unknown unknowns.

## Charter Template (paste-ready)

```
Title:        Explore <feature> for <risk>
Charter ID:   EX-2026-04-22-checkout-resilience
Mission:      Find bugs that affect <user/business outcome>
Areas:        <pages/components/APIs in scope>
Test ideas:   <specific seeds; not exhaustive — invent in-session>
Oracles:      <spec doc / prior version / sibling product / domain rule>
Risks:        <what if we miss something here>
Time-box:     90 min
Tester(s):    <names>
Setup data:   <seeded users / test orders>
Out of scope: <areas to avoid>
```

## Heuristics — SFDIPOT (San Francisco Depot)

Mnemonic for areas to probe:

- **S**tructure: code, files, data structures
- **F**unction: features and capabilities
- **D**ata: input/output, format, persistence
- **I**nterfaces: APIs, UIs, files, protocols
- **P**latform: OS, browser, device, locale
- **O**perations: how users actually use it
- **T**ime: timing, sequence, concurrency

## Session Flow

1. **Charter (5 min)** — agree mission, areas, oracles, time-box.
2. **Setup (5–10 min)** — environment, accounts, seed data, recording.
3. **Explore (60–90 min)** — alternate **survey** (broad), **deep-dive** (narrow), **regression** (re-check earlier paths).
4. **Note** observations, questions, bugs, ideas — separately.
5. **Debrief (15 min)** — PROOF: Past, Results, Outlook, Obstacles, Feelings.
6. **Convert** — file bugs; promote interesting paths to automated regression; update risk register.

## Output (session report)

```
Charter:      EX-2026-04-22-checkout-resilience
Tester:       Sam
Duration:     90 min (T:50  B:25  S:15  setup/charter:10  bug investig:20  test design:20)
Coverage:     Areas — payment, address, tax fallback; Platforms — Chrome, Safari iOS
Oracles:      spec v3.4, prior release, Stripe docs
Bugs (4):
  1. CRITICAL Address autocomplete throws on Cyrillic input
  2. HIGH Tax service 504 silently sets tax=0
  3. MED  Double-tap "Place order" creates two orders on slow 3G
  4. LOW  Currency symbol misaligned in JPY
Issues (3): 1 spec ambiguity, 2 unclear UX
Ideas (5): focus-trap audit; offline mode; refund concurrency
Risks updated: tax-fallback path elevated to High
```

## Heuristics Library to Run In-Session

- **FEW HICCUPPS** consistency oracles: Familiar, Explainable, World, History, Image, Comparable, Claims, Users, Product, Purpose, Statutes
- **CRUSSPIC STMPL** quality criteria: Capability, Reliability, Usability, Security, Scalability, Performance, Installability, Compatibility, Supportability, Testability, Maintainability, Portability, Localizability
- **RIMGEA** bug investigation: Replicate, Isolate, Maximize, Generalize, Externalize, And-also (other side-effects)

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Open-ended "have a poke" with no charter | Always write a charter before starting |
| Skipping the debrief | Debrief is where insight becomes asset |
| Treating ET as "manual = inferior" | ET excels where automation lags (UX, locale, AT, edge) |
| Not capturing recordings/notes | Loom + Markdown — bug repro becomes trivial |
| Promoting every finding to automation | Only promote enduring risk paths; not one-offs |
| Doing ET only before release | Schedule sessions inside iterations, not after |

## Charter Patterns You Can Reuse

- **Tour**: feature, claims, history, intellectual ("is this consistent with X?"), money, risk, scenario.
- **Survey + deep-dive**: 30 min wide, 60 min narrow on the riskiest finding.
- **Comparable product tour**: how does Stripe handle this? Apple Pay? Last release?
- **Regression mosaic**: walk an old bug list and confirm none returned.

## References

- J. Bach & M. Bolton — *Rapid Software Testing*: <https://www.satisfice.com/rst-appendices>
- HTSM (Heuristic Test Strategy Model): <https://www.satisfice.com/download/htsm>
- SBTM paper (Bach, 2000): <https://www.satisfice.com/download/sbtm>
- E. Hendrickson — *Explore It!*
- ISTQB CTFL 4.0 — Experience-based testing
