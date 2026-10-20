---
name: sovereign-tech-standards-network-2026
description: Applies the Sovereign Tech Standards network pilot (STA + DIN; cohort announced July 27 2026; €4,800–5,200/month for ~10 h/week of standards work at IETF/W3C/ISO) as the operational playbook for getting open-source maintainers into standards development — the fifth structural OSS-funding leg and a governance-capture defense. Use when [evaluating OSS funding mechanisms, advising maintainers on funded standards participation, writing about standards governance or digital sovereignty, or designing a national/regional open-infrastructure funding program]. NOT for [individual project grants, bounty-style bug funding, or corporate sponsorship negotiation].
---

# Sovereign Tech Standards: Funding Maintainers Where the Rules Are Written

## Overview
Open standards are developed through open processes — but open does not mean accessible. Participation in the IETF, W3C, and ISO takes time, expertise, and sustained engagement that independent open-source maintainers (the people who *implement* these standards) usually cannot afford; large companies participate as strategic investment. The Sovereign Tech Standards network (Sovereign Tech Agency + German national standards body DIN) closes that gap: ten maintainers, funded at €4,800–5,200/month for ~10 hours/week, embedded in IETF/W3C/ISO standards work with training, mentoring, travel, and fee support. It is simultaneously **a fifth OSS-funding leg** (after endowments, co-ops, employment, patronage) and **a governance-capture defense**: implementation experience enters the room where rules are written, or the rules get written without it.

## When to Use
- Mapping the OSS-funding landscape (this completes the five-leg picture)
- Advising a maintainer on whether/how to pursue funded standards work
- Explaining why standards bodies matter for open-source strategy (procurement, interoperability, sovereignty)
- Designing a public program to fix a structural participation gap (the program-design template below)
- NOT for: one-off grants; bug bounties; sponsorship deals with strings

## The Program Mechanics (the template)

**Funding shape:** fixed monthly €4,800–5,200 (not negotiated per-person — mirrors Rust MiR's flat-rate transparency rule) for ~10 h/week; SDO participation fees reimbursed; travel supported. Paid in euros by invoice to Sovereign Tech Agency GmbH; worldwide eligibility.

**Design rules worth copying:**
1. **Fund the *function*, not the project** — the deliverable is sustained standards participation (spec review, WG contributions, meeting attendance), not a code milestone. Complements the Sovereign Tech Fund (scoped contracts) and Fellowship (longer-term individual contracts) rather than duplicating either.
2. **Institutional partnership to lower the barrier** — DIN (Germany's ISO representative) joins selection and accompanies participants; ISO navigation "requires institutional knowledge and relationships that take years to build." Pair a funder with a standards body; neither alone suffices.
3. **Cohort + peer learning** — up to ten maintainers across three SDOs simultaneously, onboarding together, mentoring throughout. Networks beat isolated grants.
4. **First-meeting onboarding** — the cohort's first IETF (IETF 126 Vienna, July 2026) and TPAC attendance done *together*. The first meeting is the highest-friction step; design for it.
5. **Pilot-then-evaluate** — both the Fund and the Fellowship began as pilots; an evaluation follows the pilot (ends June 2027) before permanence.
6. **DPIA-grade anti-capture rules** — strong preference for individual contracts; entities "which do not require public support for this work are likely to be excluded"; relationship with an organization ends if the individual leaves.

**Scoring rubric (four criteria, two independent reviewers):**
- **Public-interest relevance** — how foundational/widely used the standard is; is the process at a stage where maintainer input can still shape the outcome?
- **Proposed work** — which WG, which draft, which gap; realistic outputs in the timeframe
- **Representation gap** — is the implementer perspective currently missing or underrepresented?
- **Expertise** — maintainer track record and technical authority in the domain

## The Pilot Cohort (proof of breadth)
Ten maintainers spanning: internet routing security (Job Snijders, RPKI), QUIC/HTTP-3 (Marten Seemann, quic-go; MASQUE WG co-chair), IoT encrypted DNS (Martine Lenders, RIOT; RFC 9953 DNS-over-CoAP), OpenPGP (Heiko Schäfer, rPGP), GNU Taler payments (Antoine d'Aligny), EV charging (Kacper Dalach, EVerest; ISO 15118), ActivityPub/fediverse (Daniel Supernault, Pixelfed), accessibility (Lola Odelola, W3C TAG co-chair; Mike Pennisi, AT Driver), digital identity/post-quantum (Stephen Curran, did:webvh, ACA-Py, AnonCreds).

**The survey that justified it:** of maintainers STA works with, three-quarters actively rely on standards yet very few can afford long-term participation. Maintainers bring what's missing — direct implementation experience; they "encounter in practice what looks clean on paper."

## Strategic Context
- **The funding-quad becomes a quintet.** Endowment (Open Source Endowment, perpetual ~5% income) · Co-op (3–7 maintainers, shared ownership) · Employment (Rust MiR, $350K fund, flat $10K/mo full-time tier) · Patron (Omacom, $12.6M, founder-controlled, upstream deployment) · **Standards participation (STA Standards, €4,800–5,200/mo, function-funded)**. Each targets a different failure mode; a healthy ecosystem deploys several.
- **Digital sovereignty pressure is the accelerant.** Erik Möller (STA Director of Programs, Open Source Security podcast, Aug 2026): government awareness of dependency risk is spiking — Anthropic model access restricted through export controls made every government ask "what if what we rely on can be cut off?" Germany funds critical open-source infrastructure *on behalf of the taxpayer* as roads-and-bridges investment; criteria = criticality, "what happens when it breaks," whether a funder ecosystem already exists.
- **International scaling vehicle exists:** the EU **Digital Commons EDIC** (France, Netherlands, Germany, Luxembourg, Italy) pooling resources; a pilot **EU Sovereign Tech Fund** instruments multilateral investment.
- **Adjacent STA programs:** Sovereign Tech Resilience (security audits, memory safety, post-quantum readiness, CRA compliance — relaunching late 2026); the **Standards Network's own rationale** ("standards make interoperability and portability; they avoid vendor lock-in") maps directly onto AI-governance concerns (Möller: open weights are "blobs you cannot reproduce"; "until you have reproducibility, you do not have" openness).
- **IGF Policy Network on Open Digital Infrastructure** — STA + German Federal Ministry proposal accepted; open to maintainers, researchers, policymakers.

## Honest Caveats
- Pilot, not permanent: evaluation publishes after June 2027; success criteria still being tested against reality.
- The survey is self-selected (maintainers already in STA's orbit); the representation-gap claim is plausible but not independently measured.
- €4,800–5,200/mo is a stipend, not a salary (participants invoice; no employment benefits) — the program is explicit that it's "not a good fit for people who live in expensive areas or who are looking for a higher salary."
- STA's own framing of AI ("open weights are not open source until reproducible") is advocacy-adjacent; pair with library skills holding the neutral evidence base.

## Playbook: Deploying a Standards-Participation Program (any region/body)
1. **Survey first** — quantify the reliance-vs-participation gap in your maintainer population (the "three-quarters rely, few can afford" statistic is the entire funding case).
2. **Partner with the standards body** — selection credibility + institutional navigation (the DIN move).
3. **Fund the function** — flat monthly rate for ~10 h/week sustained participation, not scoped deliverables.
4. **Cohort of ~10, three SDOs, first-meeting onboarding together** — peer network is the retention mechanism.
5. **Score on the four criteria** — public-interest relevance / proposed work / representation gap / expertise; two independent reviewers.
6. **Anti-capture rules in the contract** — individual contracts preferred; exclude entities that don't need public support.
7. **Pilot → evaluate → scale** — publish the evaluation even if the numbers disappoint.
8. **Watch the maintenance-not-code rule** — if the program drifts toward feature funding, it duplicates existing grants; the value is in review/triage/representation work with "no natural corporate sponsor."

## A-Tech Alignment
- **Open source:** a fifth funding leg; direct precedent for "get paid to represent implementers where rules are written" — and a governance-capture defense for the standards layer AI payments and identity increasingly depend on.
- **Privacy:** identity, encryption, and post-quantum standards seats (Cohort members did:webvh, OpenPGP) are exactly where privacy-respecting infrastructure gets shaped.
- **Financial freedom:** €4,800–5,200/month for 10 h/week ≈ €110–125/hour equivalent for maintenance-adjacent public work — a new, realistic income path for maintainers.
- **Practical:** the 8-step playbook and four-criterion rubric are directly reusable for funders, foundations, and governments.

## References
- See [references/sovereign-tech-standards-evidence-base.md](references/sovereign-tech-standards-evidence-base.md) for program-details extraction, the full cohort list, the DIN memorandum, the IGF policy network, and the funding-quad comparison.

## Related Skills
- `rust-maintainers-in-residence-2026` — the employment leg (flat rates, sponsor-funds-projects-select)
- `oss-endowment-and-coop-funding-2026` — endowment + co-op legs
- `omacom-patron-funding-model` — the patron leg (and its governance-concentration caveat — STA is the structural opposite)
- `sovereign-tech-fund-causal-impact` — the STA instrument this standards network extends
- `open-source-funding-platformization-2026` — platform-side funding counterweight