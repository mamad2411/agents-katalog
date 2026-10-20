---
name: registry-royalty-mandate-2026
description: Applies Laurie Voss's "Nobody pays for open source. We can force them to." (seldo.com, Sept 13, 2026) as the REGISTRY-ROYALTY-MANDATE pattern — companies already pay >$1B/yr for open-source supply (JFrog $532M, Snyk ~$326M, Docker $207M, Chainguard $40M→$100M target) but the money is captured by mirror/security vendors, not maintainers; the proposal is for the dozen package registries to meter corporate use, charge for supply, and pass a fixed royalty slice pro-rata to every package in paying customers' dependency trees, automatically. Use when designing OSS sustainability mechanisms, evaluating funding-model proposals, or writing about the open-source supply chain economy. NOT for [license-level monetization (every attempt has been forked), corporate-pledge or endowment design (use open-source-pledge-sustainability / oss-endowment-and-coop-funding-2026), or per-download tip economics].
---

# The Registry Royalty Mandate: Pay the People Who Run the Meter

## Overview
Laurie Voss (npm co-founder, five years running npm) argues that 30 years of voluntary open-source funding have failed because they ask ten thousand companies to give; the fix is an instruction to the ~12 suppliers who own the chokepoint. The REGISTRY-ROYALTY-MANDATE: registries already meter corporate usage (rate limits, auth, enterprise tiers) — add a corporate-supply subscription (individuals, small teams, students, FOSS pay nothing and notice nothing), then route a fixed revenue slice as an automatic royalty to every package in the paying customers' dependency trees, weighted by paying-customer dependence, no application, no ceremony. The insight that changes the debate: companies DO pay for open source — just not to the people who write it.

## The Evidence Base
- **The voluntary-failure ledger:** GitHub Sponsors passed $100M total payouts (July 2026) vs the $8.8T replacement value (Harvard estimate; 5% of developers produce 96% of value); only 3% of maintainers got foundation money, 1% government; Open Source Pledge ~$1.3M committed at $2K/dev/yr; OpenSSF Alpha-Omega $5–6M/yr; Germany's Sovereign Tech Fund ~€20M/yr; OpenAI's Dan Lorenc: OpenSSF had "more money than they could give away" without fixing the problem.
- **The captured-money insight:** JFrog $532M rev (+24%, 2025), Snyk ~$326M, Docker $207M (>1M paid seats; $12M→$207M 2020–2024 after rate-limiting free pulls), Chainguard $40M→$100M target, Sonatype (86% of Maven Central traffic from cloud providers), plus Sonar/Socket — the supply-chain market sells "dependable supply of free code" at a layer above the maintainer, who is the one person who can actually make the code more secure.
- **Two games:** the code game (the resource is software; free always wins — React 2017, Elastic/OpenSearch, HashiCorp/OpenTofu, Redis/Valkey every lost the fork war) and the supply game (the resource is not having to think; won by whoever is the default — Red Hat $34B to IBM, Docker's 15× revenue). Registries are where the two games touch: infrastructure you don't route around.
- **Why now:** LLMs collapse software cost → longer tails; agents are the fastest-growing OSS consumers and consume exclusively through registries (RubyGems May 2026: OpenAI agent swarm published 2,000+ packages in two days, exploited the registry API, forced a 4-day registration shutdown); curl killed its $90K/7-year bug bounty as AI garbage pushed real-bug share from 15% to <5%. Code gets cheaper; supply gets more expensive — the supply layer becomes worth paying for.
- **Prior art:** Feross 2019 npm terminal ads (banned; npm shipped `npm fund` — a hyperlink); Flossbank 2020–22 (pro-rata payout half worked, died of opt-in); Ruby Together 2015–22 (voluntary, one big donor → 2025 RubyGems governance crisis); Docker (not voluntary) worked and kept the money for itself.

## Core Findings (the mandate pattern)
1. **The money exists; it's captured at the wrong layer.** Companies pay enthusiastically for supply when it shows up as a boring procurement line item ("supply chain") — the constraint was never the supply of money.
2. **Move the toll booth from the license to the registry.** License-level charging gets forked; registry-level charging gets JFrog's revenue. The registry is a legal-free, infrastructure-locked chokepoint.
3. **Docker's rule is the template:** bill the company, not the download; individuals and open source pay nothing and notice nothing.
4. **The royalty is automatic and pro-rata.** Presence in paying customers' dependency trees is the weight — thanks.dev runs this distribution today; nobody has connected it to the collection half. No application form, no grants committee, no becoming-a-brand requirement.
5. **Pay the long tail.** Tips pay celebrities, foundations pay staff, government funds pay ~20 critical projects; dependency-tree royalties are the first mechanism that pays `is-odd`.

## When to Use
- Evaluating or building OSS funding mechanisms (the first proposal that doesn't ask the equilibrium to change — no license change, no charity, no mandate).
- Modeling agentic-consumption economics: agents consume OSS through registries, making metered supply the natural agentic-era funding surface.
- Writing or debating OSS-sustainability content: the "two games" frame and the captured-money table are the citable reframe.

## NOT For
- License-level or "fair source" monetization (structurally forked every time — see the four case histories).
- Corporate pledges and endowments (held by open-source-pledge-sustainability, oss-endowment-and-coop-funding-2026) — those are the voluntary tracks this proposal argues will never scale.
- Per-download tip economics (the power-law critique is exactly what this proposal is designed to bypass).

## Core Process / Workflow
1. **Identify the chokepoint.** For any OSS-sustainability proposal, name the layer that owns the domain everybody downloads from — that's the only layer where charging survives routing-around.
2. **Split collection from distribution.** Collection = enterprise meters already in production; distribution = pro-rata royalty over paying customers' dependency trees (thanks.dev mechanics), automatic and unceremonious.
3. **Weight against gaming.** Pay per paying-customer-dependence, not raw downloads; accept a fraud rate (junk-package farming) as the cost of having no grants committee — "the current fraud rate of paying maintainers is 100%, because we don't do it."
4. **Name the twelve.** The rule: "the people who run the meter pay the people who make the thing worth metering." It needs ~a dozen registry operators to add a line to invoices companies already pay, plus a cron job.
5. **Watch the agentic trigger.** Agent-driven registry load (the RubyGems swarm pattern) is the forcing function that makes the supply layer worth paying for before 2027.

## A-Tech Alignment
- **Open source:** the strongest single mechanism proposal for maintainer funding this cycle — and it is compatible with A-Tech's open-weights revenue lanes (hosted inference as the metered supply surface above the free weights).
- **Financial freedom:** pays the long tail for being useful, not for being good at asking — the exact inversion of the "maintainers should learn business skills" narrative.
- **Practical:** the two-games frame and the captured-money table are directly reusable in A-Tech's open-source-business-model narrative and content.

## Honesty Caveats
- A proposal, not a deployment: no registry has adopted it; GitHub/JFrog/Sonatype responses unknown.
- Dependency-tree weighting still permits lockfile-gaming at the margins; the weighting scheme is asserted, not simulated.
- JFrog/Docker/Snyk revenue figures are company-reported or trade-press figures, unaudited.
- The Spotify-model fraud analogy is the author's own; registry operators may prefer grants-committee governance for legal reasons (EU vendor-status, platform liability).

## Pairs-with
`open-source-pledge-sustainability` (the voluntary corporate track this argues against), `oss-endowment-and-coop-funding-2026` (the perpetual-income track), `temporal-durable-execution-open-source` (open-core supply contrast), `china-open-source-llm-arr-tracker` (agent-consumption growth lane), `agentic-oss-economics-2026` (agent-maintainer burden), `rust-maintainers-in-residence-2026` (the foundation stipend contrast).

## References
- seldo.com, "Nobody pays for open source. We can force them to," Sept 13, 2026 (ESS frame, captured-money table, registry-royalty proposal, RubyGems swarm).
- Tidelift 2024 maintainer survey (60% unpaid; stable since 2021); Linux Foundation Census II; Harvard $8.8T study.
- Docker pricing history (Nov 2020 rate limits → Aug 2021 Desktop paywall → $207M/2024).

*Created: 2026-09-17 (Cycle 28, Run 3) — A-Tech Research Division*