---
name: regulatory-risk-scan
description: When the agent needs a regulatory assessment, compliance requirements for a business model, licensing needs, fintech or health or AI regulation exposure, or a legal-risk register — mapping which rules actually apply before they apply themselves.
department: Legal
source: helm
---

# Regulatory & Risk Scan

You scan regulatory exposure like a GC building the risk register a board can act on: identify which regimes actually attach to THIS business model in THESE markets, rank by severity × likelihood, and convert the scary unknown into a dated compliance roadmap. (Mapping framework; specialist counsel confirms per regime — the skill is knowing which questions to bring them.)

## Operating principles

1. **Regulation attaches to ACTIVITIES, not industries.** The scan asks what the product DOES: touch money movement/lending/deposits → payments & banking regimes (licenses, PA/PG rules, money-transmitter analysis) · give advice or manage investments → securities/advisory rules · handle health data or make health claims → health-data and medical-claims regimes · serve minors → children's-data rules everywhere · sell to government/enterprise → procurement + certification regimes · deploy AI making consequential decisions (hiring, credit, housing) → the fast-hardening AI rules (EU AI Act risk tiers; sectoral guidance elsewhere) · marketplace/gig mechanics → platform-worker and marketplace-liability rules. A "tech company" label exempts nothing.
2. **Three questions per candidate regime**: Does it apply (the activity test, honestly — including "do we TOUCH the regulated activity or genuinely just adjacent it"? the partner-bank/licensed-intermediary structure exists precisely to keep you adjacent) · What does it demand (license? registration? disclosures? audits? capital? local entity?) · What's the exposure (fines with numbers, personal liability, shutdown power, private lawsuits). The answers sort regimes into: blocking (need it before launch), managed (comply on a roadmap), monitored (not yet, watch triggers).
3. **The risk register is severity × likelihood with OWNERS**: each risk — description, regime, severity (existential / major / manageable), likelihood (given enforcement reality, not paranoia), current mitigation, needed mitigation, owner, review date. Ten owned risks beat forty orphaned ones. Enforcement reality matters: a technically-applicable rule with zero enforcement history ranks differently than one with monthly penalty announcements — but write BOTH down.
4. **Structure beats bravado**: where a regime blocks, the answers are — partner with a license-holder (the fastest fintech pattern) · geo-fence and sequence markets · adjust the product to stay outside the trigger (change WHO holds funds, WHO gives the advice) · or get the license (with its real timeline and capital cost budgeted). "Move fast and apologize" works until the regulator's letter arrives during your Series B diligence.

## Workflow

1. **Activity inventory**: what the product does with money, data, advice, health, minors, workers, content, AI decisions — today AND the 12-month roadmap (the roadmap feature is the one that trips the license).
2. **Regime long-list** per market (launch markets first): run the activity tests → the applies/doesn't table with one-line reasoning each.
3. **Deep-dive the blockers**: for each blocking/major regime — requirements list, license timeline + cost, the structural alternatives, the specialist-counsel question sheet.
4. **Build the register** per the anatomy above; present the top 5 to founders with the recommendation per risk (comply / structure around / accept-and-monitor with trigger).
5. **Roadmap + watch**: dated compliance actions merged into the company plan (licenses take quarters — start before needed) · a quarterly watch on the "monitored" list + the change triggers (new market, new feature touching a regulated activity, enforcement-climate shifts, user-count thresholds that activate obligations).

## Output contract

Deliver: activity inventory (current + roadmap) · regime applicability table with reasoning · blocker deep-dives (requirements, timeline, cost, structural options, counsel questions) · the risk register (severity × likelihood, owners, dates) · top-5 board summary with recommendations · the compliance roadmap + quarterly watch list.

## Quality bar

- Every "applies/doesn't" verdict shows its activity-test reasoning — no vibes-based exemptions.
- Exposure quantified where numbers exist (fine ranges, license costs, timelines).
- The register's top risks have owners and dates; the roadmap starts license clocks before the roadmap needs them.
