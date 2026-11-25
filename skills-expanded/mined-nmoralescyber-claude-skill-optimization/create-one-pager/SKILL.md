---
name: create-one-pager
description: Generates single-page sales/marketing collateral — leave-behinds, datasheets, executive summaries, pricing sheets, capability briefs. Make sure to use this skill whenever the user says create a one-pager, write a datasheet, build a leave-behind for [prospect/event], make a capability brief, exec summary for [meeting], one-page summary of [product/feature/proposal], or describes any single-page persuasive document. Optimized for printable / shareable / scannable. For cybersecurity products, includes trust signals, compliance certifications, and ROI quantification. Do NOT use for: multi-slide presentations (use create-deck), interactive prospect landing pages (use create-landing-page), screencast scripts (use create-workflow-demo), or marketing blog/social content (use marketing:draft-content). Defining characteristic: "fits on one page, designed to be skimmed in 60 seconds, often printed."
---

# Create One-Pager

Single-page persuasive collateral — datasheets, leave-behinds, capability briefs, exec summaries.

## When to use vs. adjacent asset skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Output must fit one printed page | Multi-slide presentation → `create-deck` |
| Designed to be skimmed in 60 seconds | Interactive prospect landing page → `create-landing-page` |
| Often printed and physically left behind | Walkthrough or screencast → `create-workflow-demo` |
| Persuasive sales/marketing intent | Blog or social content → `marketing:draft-content` |

## One-pager types this skill handles

### Product datasheet (technical buyer)
For technical evaluators (engineering, security, IT). Dense with specifics.

Layout:
- Header: product name + 1-line value prop + version/date
- "What it does" — 2-3 sentences, no buzzwords
- "How it works" — 3-step diagram or flow
- Capabilities — bulleted list, technical specifics
- Integrations — supported systems
- Specifications — performance numbers, scale, latency, deployment options
- Security/compliance — certifications, encryption, data residency
- Pricing model — high-level, with link to detailed pricing
- Footer: contact + URL + legal

### Sales leave-behind (business buyer)
For decision-makers after a meeting. Reinforces the conversation; not a substitute for it.

Layout:
- Header: customer-facing tagline + your logo
- The problem they have (mirror of what was discussed)
- The 3 outcomes you deliver (quantified)
- 2-3 customer proof points with logos and metrics
- Trust row: SOC 2 / ISO / known customers / known investors
- Suggested next step (specific, low-friction)
- Contact info for the salesperson who left it

### Executive summary (decision-grade)
For exec / board / procurement deciding on go/no-go.

Layout:
- Decision required
- Recommendation with confidence
- 3 reasons (quantified)
- 3 risks + mitigations
- Cost / timeline / dependencies
- Decision owner + deadline

### Capability brief / feature one-sheet
For sales enablement or partner enablement. Internal-facing usually.

Layout:
- Capability name + 1-line summary
- The problem it solves (customer language)
- How it works (technical, but brief)
- Use cases (2-3 named)
- Pricing / packaging / availability
- Talk track (3 lines a salesperson can say verbatim)
- Common objections + responses
- Where to learn more

## Cybersecurity overlay

For security products, every one-pager type benefits from these elements:

- **Compliance row** — list of certifications and standards (SOC 2 Type II, ISO 27001, HIPAA-ready, PCI-DSS, FedRAMP if applicable)
- **Threat coverage statement** — what attack surface or threat type this addresses, named specifically (e.g., "Detects credential stuffing across web auth endpoints" not "improves security")
- **Deployment time** — how fast they can be live (in days, not "varies")
- **Pen test attestation** — most recent date + scope
- **Customer ICP fit** — "Used by 12 of the top 50 fintechs" beats "trusted by enterprises"

## Design / format constraints

- **One page genuinely.** A one-pager that runs to 1.5 pages is a failure. Cut or restructure.
- **Scannable hierarchy.** F-pattern reading: top-left to top-right, then down. Most important content top-third.
- **High contrast, large type.** Will be printed, scanned, photocopied, faxed (yes, in some industries still).
- **Visuals where possible.** A diagram beats a paragraph. A chart beats a sentence.
- **Brand-consistent.** If a brand guide exists, follow it; if not, default to clean / clear / unfussy.
- **Contact info present.** Always. People do find one-pagers months later.

## Anti-patterns

- **Hype words** — "revolutionary," "next-generation," "best-in-class" — read as filler by everyone
- **Wall of bullets** — 30 bullets across 6 columns. Pick 3-5 strongest.
- **Buzzword bingo** — AI-powered, blockchain-enabled, cloud-native, zero-trust — okay in moderation, deadly when stacked
- **Generic stock imagery** — handshakes, locks, network diagrams. Either show your actual product or use abstract typography
- **Fine print obscured** — if it's important enough to disclose, it's important enough to read
- **Out-of-date stats** — "trusted by 500+ customers" without a date stamp; verify before publishing
- **Multi-page disguised as one-page** — header on every "page" doesn't make it one page

## Output

Produces:
1. The one-pager content in markdown
2. Layout intent (which sections go where, what's a column vs. full-width, what gets visual emphasis)
3. Optional: HTML version for printing or PDF export
4. Optional: .docx version (chains to anthropic-skills:docx)
5. Suggested distribution (sales rep leave-behind / partner deck attachment / website resource page / direct email)
