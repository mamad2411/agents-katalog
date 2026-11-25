---
name: campaign-page-one-shot
description: "Use when a campaign needs a landing page and the design-dev cycle would take two weeks you don't have. Give Fable 5 the campaign brief, brand kit, reference screenshots, offer, and proof elements, and get a working single-file HTML landing page rendered live as a claude.ai artifact in one run, plus three suggested hero variants."
---

# Campaign Page One-Shot

## When to use this skill

- A campaign launches soon and the landing page is the bottleneck — design and dev are booked out for weeks
- You want to validate an offer with a real page before committing design/dev resources to the final build
- You have the brief, the brand kit, and the proof elements, and just need someone to assemble a credible page
- You want to show stakeholders a working page instead of a wireframe in the kickoff meeting

## What this skill does **NOT** do

- Production deployment (no hosting, domains, or analytics wiring — you get the HTML file)
- CMS integration or A/B testing infrastructure
- Replace a developer for the final build — this ships the prototype that kills the 2-week design-dev cycle for validation
- Work from a vague brief ("make it pop") — the intake forces the specifics that make one-shots work

## What this skill produces

1. **A working single-file HTML landing page** rendered live as a claude.ai artifact in one run: hero, proof section, offer block, CTA — responsive, brand-faithful, with real copy written from your brief (zero lorem ipsum, zero placeholders)
2. **3 suggested variants** — different hero angles you can request next, each named by the one axis it changes

No Design Handoff section in this skill: Fable IS the builder here — it codes the page directly as an artifact.

## Why Fable 5

Fable 5 is the strongest frontend-coding model available — it one-shots working websites as claude.ai artifacts, which is why people say "Fable is great at design." A smaller model produces a layout that needs five rounds of fixes; Fable holds the brand kit, the reference screenshots, and the full brief together and ships a coherent page in a single pass.

## Corpus checklist

Smaller corpus than the analysis skills — but precision matters more. Vague inputs produce generic pages.

- **Campaign brief** — the offer, the audience (1-2 sentences), the campaign goal, and the single conversion action
- **Brand kit** — HEX color codes (exact, not "our blue"), font names for heading and body, logo description or upload, any spacing/style rules you have
- **Reference screenshots** — 1-3 screenshots of pages whose style you like (upload them; screenshots beat adjectives, per reference.md). Note what specifically you like about each
- **Offer + CTA** — the exact offer wording and the CTA verb you want on the button
- **Proof elements** — 2-3 testimonials with names/titles, customer logos you can name, stats with sources. Real ones; the page is only as credible as its proof
- **Volume guidance:** this all fits on 1-2 pages of pasted text plus the screenshot uploads. Completeness beats length

## Workflow

1. **Gather the inputs** per the checklist — exact HEX codes and real proof elements before you open the chat.
2. Paste this SKILL.md into a new Claude chat with **Fable 5** selected (works in claude.ai, where the artifact renders live, or in Claude Code).
3. Answer the intake questions, one at a time. Upload reference screenshots when asked.
4. Fable builds the page in one run and renders it as an artifact.
5. Review the live render against the quality checklist. Request changes by naming ONE axis at a time (iteration etiquette in reference.md).
6. Pick from the 3 suggested hero variants if the first angle isn't landing, then hand the HTML file to whoever publishes.

## Intake

Ask these questions, **one at a time**.

1. **Offer + audience + goal** (what's offered, to whom, and the one conversion action)
2. **Exact CTA text** (the words on the button)
3. **Brand colors** (HEX codes for primary, secondary, background — exact values)
4. **Fonts** (heading + body font names; Google Fonts names work best in a single file)
5. **Logo** (upload, or describe so a text-based placeholder matches)
6. **Reference screenshots** (upload 1-3, with one line each on what you like about it)
7. **Proof elements** (paste testimonials with attribution, nameable customer logos, stats with sources)
8. **Tone** (e.g., enterprise-calm, founder-direct, playful — one phrase)
9. **Anything forbidden** (competitor look-alikes, banned phrases, colors to avoid)

## Output format: one-shot landing page build

```
Build a complete, working landing page as a single-file HTML artifact.

Campaign: <Q1>. Conversion action: <Q1>. CTA text, exactly: "<Q2>".
Brand: colors <Q3 HEX values>, heading font <Q4>, body font <Q4>,
logo <Q5>. Tone: <Q8>. Forbidden: <Q9>.
Style direction: match the attached reference screenshots —
specifically <what user liked about each, Q6>.

**Page structure (per reference.md anatomy):**
1. Hero — headline that makes the offer clear in 5 seconds, subhead,
   the single CTA button, supporting visual treatment
2. Proof section — within the first scroll: <Q7 proof elements>
3. Offer block — what they get, spelled out
4. Final CTA — same conversion action, restated

**Build rules:**
- Single HTML file, all CSS embedded, responsive at 375px and 1440px
- Real copy written from the brief — zero lorem ipsum, zero
  [PLACEHOLDER] text anywhere
- Exact HEX values from the brand kit; load the named fonts
- One conversion action; every CTA on the page points to it
- No generic AI aesthetics: no purple gradients on dark, no stock-feel
  layouts, no default system fonts (per reference.md)

**After the page renders, list 3 hero variants I can request next,
each changing exactly ONE axis (angle, proof lead, or urgency) with a
one-line description.**

**Self-check before delivering:**
- Headline passes the 5-second offer-clarity test
- Proof appears within the first scroll
- Exact brand HEX values and fonts used, nothing approximated
- Zero placeholder text; every testimonial and stat is from the brief
- Responsive at both breakpoints; one conversion action throughout
- Nothing on the forbidden list (Q9) appears

[UPLOAD REFERENCE SCREENSHOTS WITH THIS MESSAGE]
```

## No Fable access?

Opus can build it, but expect a simpler layout and more iteration rounds to reach brand fidelity. The intake and build rules above still do most of the work.

## Quality checklist

- [ ] All 9 intake questions answered, screenshots uploaded
- [ ] HEX codes exact, fonts named (not described)
- [ ] Artifact renders and is responsive at mobile and desktop widths
- [ ] Headline states the offer clearly in 5 seconds
- [ ] Proof elements visible within the first scroll, all real
- [ ] Zero placeholder or lorem ipsum text anywhere
- [ ] One conversion action; CTA text matches Q2 exactly
- [ ] No generic AI aesthetics (checked against reference.md list)
- [ ] 3 single-axis hero variants suggested

## Related

- `reference.md` — landing page anatomy, one-shot prompt patterns, brand fidelity rules, conversion copy slots, iteration etiquette
- `customer-insight-miner` — mine the objection map first and the proof section writes itself
- `engagement-autopsy` — your winning hook patterns make strong headline candidates

### Related skills in this repo

- **product-marketing-context**: Pull positioning, personas, and objections from here instead of asking from scratch.
- **content-strategy**: Decide the campaign's angle/topic before building the page.
- **frontend-design**: Underlying aesthetic guidance this skill's one-shot build draws on.
- **design-dev-resources**: Source real illustrations/logos for the page instead of hand-drawn SVG.
