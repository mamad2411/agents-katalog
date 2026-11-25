---
name: research-brief
description: Produces a one-page research brief on a topic, person, or company — what they do, what matters, what's changed recently, sources. Use when the user asks to research, look into, brief me on, or get context on a specific topic, company, competitor, or person. Pulls from the web, any project context, and recent emails involving the subject.
---

# Research Brief

Turn "I need to know about X before my 2pm call" into a one-page brief the user can skim in three minutes and feel prepared.

## Before starting

1. Ask the user what they want a brief on if it's not clear. A company? A person? A topic? A competitor?
2. Ask what they need the brief *for.* A sales call? A strategic decision? A blog post? Same subject, different briefs.
3. Read `context/preferences.md` — source citation style, confidence level tagging if relevant
4. Check the project folder — have you researched this subject before? Build on it, don't redo it.

## What to produce

A markdown file saved to `/output/research-brief-{subject}-{YYYY-MM-DD}.md` with four sections:

1. **The 30-second version** — three to five sentences. If the user only reads this section, what do they need to know?
2. **What they do / what it is** — core facts. Company: product, size, customers, how they make money. Person: role, background, what they're known for. Topic: the basics.
3. **What matters right now** — recent news, strategic shifts, public statements, anything timely. What's changed in the last 90 days.
4. **Sources & confidence** — what you drew from, and where you're guessing vs. citing. Label each claim with a confidence marker if the user asked for it in `preferences.md`.

## Inputs

- Web search (required)
- The user's prior research on this subject in the project folder (if exists)
- Recent emails mentioning the subject (optional — useful for competitive briefs)
- Any docs the user uploaded with the request

## How it works

1. Understand the subject and the purpose (ask if unclear)
2. Search the web — company site, news, LinkedIn if it's a person, press releases, recent podcast/video appearances for public figures
3. Cross-reference with any existing project context
4. Draft the four sections. Short. Dense with information. No padding.
5. Flag anything uncertain or contested — never smooth over ambiguity
6. Save the file, tell the user one-line what stood out ("Strong product, weak financials — the gap is interesting if you're pitching to them")

## What not to do

- Do not regurgitate their "About" page. Synthesize, don't copy-paste.
- Do not invent specifics. If you can't find revenue numbers, don't estimate them. Say "not publicly disclosed."
- Do not include information that's more than 18 months old unless it's foundational (company history, product roadmap). Prioritize recent.
- Do not produce a 10-page report. A one-page brief is the format. Respect the format.

## Example output structure

```markdown
# Research Brief — Northwind Inc. — 2026-04-18

## The 30-second version
Northwind is a 200-person B2B workflow SaaS targeting mid-market ops teams, about $18M ARR, series B last year ($24M led by Accel). They're pivoting from horizontal workflow to vertical (finance ops first). New CRO joined in January. Growth was strong through 2024 but has slowed visibly in the last two quarters — this is likely why they're engaging on our pricing conversation now.

## What they do
- **Product:** workflow automation for ops teams — think Zapier but with more structured primitives
- **Customers:** ~600 SMB and mid-market, mostly US, growing international presence
- **Pricing:** $500–$3,000/month per team, custom for enterprise
- **Team:** 200 FTEs, HQ in Austin, 60% eng/product

## What matters right now
- **Vertical pivot.** Announced in March — finance ops as the beachhead vertical. Hiring finance-ops-specific AEs.
- **Slower growth.** Q4 2025 growth rate was 8% QoQ, down from 14% in Q2. Public hiring slowdown in engineering.
- **New CRO.** Marcus Alvarez, ex-Greenhouse, joined January. Known for aggressive deal closing.
- **Competitive pressure.** Retool and Zapier both pushed into their mid-market segment in Q1.

## Sources & confidence
- Company site, March 2026 press release (high confidence — primary source)
- Crunchbase funding data (high confidence — primary source)
- LinkedIn for headcount and CRO details (high confidence)
- ARR estimate from The Information's March coverage (medium confidence — reported, not disclosed)
- Growth rate QoQ from their annual all-hands leak on Blind (low confidence — unverified)
- Vertical pivot and competitive context from recent Latent Space podcast interview with their CEO (high confidence — on the record)
```

## Customization notes

- **For a sales brief.** Add a section: "Likely objections" — based on their stage, budget, existing stack.
- **For a competitive brief.** Add a section: "Where they win, where they lose" — honest assessment.
- **For a prospect brief (person).** Focus sections 2 and 3 on the individual — background, what they've said publicly, any connection to the user's network.
- **For a market brief (topic).** Replace sections 2 and 3 with "The landscape" and "What's shifting" — same structure, broader scope.
