---
name: lp-optimization
description: "Audits a landing page for conversion — analyzes hero, CTA, social proof, objection handling, and page flow. Produces specific copy and structure change recommendations. Not for A/B testing variants (use experiment) or full site SEO audits (use seo). For brand identity and design tokens, see brand-system. For content strategy, see imc-plan."
argument-hint: "[url or description]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "3.0.0"
  budget: deep
  estimated-cost: "$1-3"
promptSignals:
  phrases:
    - "landing page"
    - "conversion rate optimization"
    - "page optimization"
    - "cro audit"
    - "landing page audit"
    - "optimize the landing page"
  allOf:
    - [landing, page]
    - [conversion, audit]
  anyOf:
    - "landing page"
    - "conversion"
    - "cro"
    - "bounce rate"
    - "above the fold"
  noneOf:
    - "write copy"
    - "brand identity"
  minScore: 6
routing:
  intent-tags:
    - conversion-audit
    - landing-page-audit
    - page-optimization
    - cro
  position: horizontal
  produces:
    - mkt/lp-optimization.md
  consumes:
    - product-context.md
    - mkt/icp-research.md
  requires: []
  defers-to:
    - skill: copywriting
      when: "need to write new copy, not audit existing page"
    - skill: seo
      when: "optimizing for search, not conversion"
  parallel-with:
    - seo
  interactive: false
  estimated-complexity: medium
---

# Landing Page Conversion Optimization — Orchestrator

*Communication — Horizontal. Coordinates specialized audit agents to diagnose conversion blockers and produce prioritized, evidence-based fix recommendations.*

**Core Question:** "What's stopping visitors from converting?"

## Philosophy

The frameworks here (PAS, 4-U, social proof hierarchy) are evidence-backed defaults. They work in most situations. But landing pages serve different audiences, traffic sources, and goals. When your data or testing reveals a different optimal approach, follow the data. The principles matter more than the specific numbers. This orchestrator dispatches specialist agents for each concern, then a critic agent ensures every recommendation meets the evidence bar.

## Critical Gates — Read First

1. **Do NOT recommend fixes without evidence.** Every finding must include: what was observed, which principle it violates, and a specific recommended fix (exact text, not "improve the headline").
2. **Check message match BEFORE optimizing copy.** A perfectly written headline that doesn't match the traffic source will still bounce visitors. Message match is the first conversion gate.
3. **Form fields: every field >5 costs ~10% conversion.** This is an evidence-backed default (Unbounce/HubSpot research). Exceptions exist for high-intent enterprise traffic — but the exception must be justified, not assumed.

## Inputs Required
- Landing page URL or description of the page
- ICP research from `.agents/mkt/icp-research.md` (recommended — VoC language strengthens copy)
- Traffic source context (where visitors come from)

## Output
- Optimization recommendations with specific copy/structure changes
- For new pages: complete page structure with copy

## Quality Gate
Before delivering, the **critic agent** verifies:
- [ ] Headline scores >=3 out of 4 on the U's (Useful, Unique, Urgent, Ultra-specific)
- [ ] Message matches the traffic source (headline echoes the ad/link that brought them)
- [ ] One primary CTA per page (secondary CTAs don't compete)
- [ ] Trust signals appear within scroll-distance of every CTA
- [ ] Form has <=5 fields (or justified why more are needed)
- [ ] Social proof is from the last 12 months (older proof replaced or removed)
- [ ] Every audit finding includes: what was observed, which principle it violates, and a specific recommended fix
- [ ] Prioritized fix list has ICE scores with documented reasoning
- [ ] No vague recommendations ("improve the headline" — must be specific replacement text)

## Chain Position
Horizontal — works with `icp-research` (audience data), `content-create` (content assets), `copywriting` (copy craft), `experiment` (test design)
**Re-run triggers:** After major page redesigns, when conversion drops >10%, when traffic source mix changes significantly, or quarterly.

### Skill Deference
- **Need to write copy from scratch (not optimize existing)?** → Use `content-create` — this skill optimizes existing pages, not blank-page writing.
- **Need craft-quality headline rewrites or CTA copy?** → Run `copywriting` for variation workflow and evaluation rubric.
- **AI pattern cleanup needed?** → Use `humanize` — this skill focuses on conversion mechanics, not voice/pattern editing.

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Hero Audit | 1 (parallel) | `agents/hero-audit-agent.md` | Headline, subheadline, hero CTA, above-the-fold assessment |
| Trust Audit | 1 (parallel) | `agents/trust-audit-agent.md` | Social proof, testimonials, credibility signals, trust hierarchy |
| CTA Audit | 1 (parallel) | `agents/cta-audit-agent.md` | All CTAs, risk reversal, form fields, conversion friction |
| UX Audit | 1 (parallel) | `agents/ux-audit-agent.md` | Navigation, mobile, load speed, cognitive load, visual hierarchy |
| Message Match | 2 (sequential) | `agents/message-match-agent.md` | Ad/email/search-to-LP message continuity |
| Prioritization | 2 (sequential) | `agents/prioritization-agent.md` | Ranks findings by conversion impact, ICE scoring |
| Critic | 2 (final) | `agents/critic-agent.md` | Quality gate — PASS/FAIL with rewrite routing |

### Shared References (read by multiple agents)
- `references/core-principles.md` — Headlines, value props, CTAs, forms, message match, PAS
- `references/social-proof-trust.md` — Social proof hierarchy, biases, trust signals
- `references/ux-design.md` — Visual hierarchy, mobile optimization
- `references/advanced-psychology.md` — Headline formulas, close sequences, pricing, urgency
- `references/testing-optimization.md` — A/B testing, tracking, ICE framework
- `references/implementation-checklist.md` — Pre-launch checklists

---

## Routing Logic

Classify the task, then follow the matching route.

### Route A: Quick Audit
**When:** User wants a fast assessment of a specific concern (headline, CTA, or form) — not a full-page audit.

```
1. Pre-dispatch: Gather context (Step 0 below)
2. Dispatch 1-2 relevant agents:
   - Headline concern → hero-audit-agent
   - CTA/form concern → cta-audit-agent
   - Both → hero-audit-agent + cta-audit-agent in parallel
3. Dispatch: prioritization-agent (on selected agent outputs)
4. Dispatch: critic-agent
5. If critic returns FAIL → re-dispatch named agent(s) with feedback (max 2 cycles)
6. Deliver prioritized fix list
```

### Route B: Full Audit
**When:** User wants a comprehensive landing page conversion audit.

```
1. Pre-dispatch: Gather context (Step 0 below)
2. LAYER 1 — Dispatch IN PARALLEL:
   - hero-audit-agent
   - trust-audit-agent
   - cta-audit-agent
   - ux-audit-agent
3. MERGE: Combine all Layer 1 outputs into unified audit findings
4. LAYER 2 — Dispatch SEQUENTIALLY:
   - message-match-agent (receives merged L1 output)
   - prioritization-agent (receives message-match output)
   - critic-agent (receives prioritization output)
5. If critic returns FAIL → re-dispatch named agent(s) with feedback (max 2 cycles)
6. Deliver final audit artifact
```

### Route C: New Landing Page (Write Mode)
**When:** User wants to create a new landing page, not audit an existing one.

This is a write workflow, not an audit workflow. The agents are repurposed as planning advisors.

```
1. Pre-dispatch: Gather context (Step 0 below)
2. Read ICP research (if available) for VoC language and pain points
3. Define primary conversion goal (one per page)
4. Generate headline using hero-audit-agent's 4-U framework:
   - Generate 10+ headline variations using formula library
   - Score each with 4-U formula
   - Select top 3 for presentation
5. Structure body with PAS framework (from core-principles reference)
6. Plan social proof using trust-audit-agent's hierarchy:
   - Identify strongest proof available
   - Place above fold
7. Design form using cta-audit-agent's form rules:
   - Minimal fields (start with email only)
   - First-person CTA formula
   - Risk reversal placement
8. Plan UX using ux-audit-agent's checklist:
   - Remove navigation
   - Mobile-first layout
   - Trust signals near every CTA
9. Verify message match with traffic source(s)
10. Run through quality gate checklist
11. Deliver page structure with copy recommendations
```

**Note:** Route C uses the agent frameworks and reference files as planning tools but follows the sequential workflow rather than parallel dispatch, since the page doesn't exist yet to audit in parallel.

---

## Step 0: Pre-Dispatch Context Gathering

Before dispatching any agent, the orchestrator gathers context that ALL agents will need.

### Product Context Check
Check for `.agents/product-context.md`. If available, read for product details and accuracy. If missing, strongly recommend running `icp-research` first — this skill works without it but produces significantly better output with it.
If `.agents/product-context.md` or `.agents/mkt/icp-research.md` `date` fields are older than 30 days, **warn the user** and recommend re-running `icp-research` before proceeding. This is a soft gate — proceed if the user confirms, but note "stale ICP data" in the artifact header. Tip: `/navigate status` (from meta-skills) gives a single-pass freshness report across all upstream artifacts.

### Required Artifacts
None — can audit any page standalone.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `icp-research.md` | icp-research | VoC data for persuasion |
| `product-context.md` | icp-research | Product details for accuracy |
| `experiment-*.md` | experiment | Test design context |

### Pre-Writing Framework
Answer these questions before dispatching. Pass the answers to every agent as the `pre-writing` input:

1. **What is the primary conversion goal?** (signup, purchase, demo request, download)
2. **Who is the target audience?** What do they currently believe? What language do they use?
3. **Where is the traffic coming from?** (Ad, search, email, social, direct) — determines message match requirements.
4. **What traffic source copy exists?** (ad headlines, email subject lines, search meta descriptions) — needed for message-match verification.

If `.agents/mkt/icp-research.md` exists, pull VoC quotes and pain language for all agents.

---

## Dispatch Protocol

### How to spawn a sub-agent

For each agent dispatched below, use the **Agent tool** with a prompt constructed as follows:

1. **Read** the agent instruction file (e.g., `agents/hero-audit-agent.md`) — include its FULL content in the Agent prompt
2. **Append** the brief and pre-writing context after the instructions
3. **Resolve file paths to absolute**: replace relative paths with absolute paths rooted at this skill's directory. Example: if this skill is at `/Users/you/skills/lp-optimization/`, then `references/core-principles.md` becomes `/Users/you/skills/lp-optimization/references/core-principles.md`. Tell the agent: "Read the reference file at [absolute path] for domain knowledge."
4. **Pass upstream artifacts by content, not path**: the orchestrator reads `.agents/product-context.md` and `.agents/mkt/icp-research.md` FIRST, then includes relevant excerpts (VoC quotes, pain language, product details) in the pre-writing object. Sub-agents should NOT read artifact files directly — the orchestrator curates what they need.
5. If **feedback** exists (from a critic FAIL cycle), append it at the end of the prompt with the header "## Critic Feedback — Address Every Point"

### Single-agent fallback

If multi-agent dispatch is unavailable (no Agent tool, single-agent runtime, or context constraints), execute each agent's instructions sequentially in-context:
- Layer 1: run each agent's domain instructions one at a time, writing each section
- Layer 2: apply each refinement pass to the full document in order
- Critic: self-evaluate using the critic-agent's rubric and quality gate

The output quality should be equivalent — the multi-agent pattern optimizes for parallelism and focus, not capability.

---

## Layer 1: Parallel Audit Agents

Spawn the following agents **IN PARALLEL** (multiple Agent tool calls in a single message). For each agent, follow the Dispatch Protocol above.

| Agent | Instruction File | Pass These Inputs | Reference Files to Resolve |
|-------|-----------------|-------------------|---------------------------|
| Hero Audit | `agents/hero-audit-agent.md` | brief + pre-writing | `references/core-principles.md`, `references/advanced-psychology.md` |
| Trust Audit | `agents/trust-audit-agent.md` | brief + pre-writing | `references/social-proof-trust.md` |
| CTA Audit | `agents/cta-audit-agent.md` | brief + pre-writing | `references/core-principles.md` |
| UX Audit | `agents/ux-audit-agent.md` | brief + pre-writing | `references/ux-design.md` |

**For quick audit tasks (Route A):** Dispatch only the relevant agent(s), not all four.

---

## Merge Step

After all Layer 1 agents return, assemble their outputs into a unified audit document.

### Section Order (full audit)
1. **Hero Assessment** — hero-audit-agent's headline, subheadline, and hero CTA evaluation
2. **Trust & Social Proof Assessment** — trust-audit-agent's proof inventory, gaps, and recommendations
3. **CTA & Conversion Assessment** — cta-audit-agent's CTA inventory, form audit, risk reversal, friction analysis
4. **UX & Page Experience Assessment** — ux-audit-agent's navigation, mobile, speed, cognitive load findings

### Assembly Rules
The merge is deterministic assembly, not creative synthesis. Slot each agent's output into the unified document by ownership:

| Section | Owner Agent |
|---------|-----------|
| Headline Assessment | Hero Audit |
| Subheadline Assessment | Hero Audit |
| Hero CTA Assessment | Hero Audit |
| Above-the-Fold Verdict | Hero Audit |
| Social Proof Inventory | Trust Audit |
| Recency Assessment | Trust Audit |
| Cognitive Bias Utilization | Trust Audit |
| Trust Signal Clustering | Trust Audit |
| CTA Inventory | CTA Audit |
| Form Audit | CTA Audit |
| Risk Reversal Audit | CTA Audit |
| Conversion Friction Analysis | CTA Audit |
| Navigation Assessment | UX Audit |
| Visual Hierarchy | UX Audit |
| Mobile Experience | UX Audit |
| Page Speed | UX Audit |
| Cognitive Load | UX Audit |

### Conflict Resolution
- Each agent owns specific sections (table above). If two agents mention the same element (e.g., both hero-audit and cta-audit reference the hero CTA), keep the version from the section owner.
- If hero-audit's headline assessment contradicts ux-audit's visual hierarchy assessment, note both perspectives and let the prioritization agent resolve via ICE scoring.

---

## Layer 2: Sequential Analysis

Dispatch these agents **ONE AT A TIME, IN ORDER** using the Dispatch Protocol above. Each receives the previous agent's full output as the `upstream` field.

```
message-match-agent → prioritization-agent → critic-agent
```

| Step | Agent | Instruction File | Receives |
|------|-------|-----------------|----------|
| 1 | Message Match | `agents/message-match-agent.md` | Merged Layer 1 output + traffic source data |
| 2 | Prioritization | `agents/prioritization-agent.md` | Message match output (includes all findings) |
| 3 | Critic | `agents/critic-agent.md` | Prioritization output (final document) |

Each agent returns the full document with their analysis added + a change log.

---

## Critic Gate

The critic agent returns one of two verdicts:

### PASS
The audit meets all quality standards. Deliver the critic's approved output as the final artifact.

### FAIL
The critic returns specific failures with:
- Which sections failed and why
- Specific fix instructions
- Which agent to re-dispatch

**Rewrite loop:**
1. Read the critic's failure report
2. Re-dispatch ONLY the named agent(s) with the critic's feedback attached as the `feedback` input
3. Run the modified output back through the critic
4. **Maximum 2 rewrite cycles.** After 2 failures, deliver the audit with the critic's annotations and flag to the user: "Audit scored [X] — manual review recommended on [specific sections]."

---

## Artifact Template

When saving optimization artifacts, use this frontmatter:

```yaml
---
skill: lp-optimization
version: 1
date: [today's date]
status: draft
---
```

> On re-run: rename existing artifact to `[name].v[N].md` and create new with incremented version.

## Next Step

Run `copywriting` to rewrite specific sections. Run `seo` for technical search optimization. Run `experiment` to set up A/B tests for recommended changes.

---

## Worked Example — Full Audit (Route B)

**Brief:** Audit the Acme Analytics free trial page for conversion optimization.
**Audience:** Engineering managers at 50-200 person companies, problem aware.
**Traffic:** Google Ads ("real-time analytics dashboard"), LinkedIn ads (cold), and organic search.

### Step 0: Pre-Dispatch
1. Conversion goal: Free trial signup
2. Audience: EMs who need real-time visibility but feel buried in tool sprawl
3. Traffic: Google Ads (warm, searched for solution), LinkedIn (cold, interrupted), organic
4. Traffic source copy: Google Ad headline: "Real-time analytics dashboard — 14-day free trial"

### Layer 1: Parallel Dispatch
--> **Hero audit agent** returns: Headline "The Best Analytics Platform for Modern Teams" scores 1/4 on 4-U. Recommends: "See every metric your team tracks — one screen, updated every 5 minutes." (4/4). 5 variations provided.
--> **Trust audit agent** returns: No testimonials above fold. Customer logos present but below fold. No recency dates on testimonials. Tier 1 proof missing entirely. Recommends: add strongest result quote near hero CTA, move 3 logos above fold, date-stamp all testimonials.
--> **CTA audit agent** returns: Hero CTA "Get Started" (no first-person, no specificity). Form has 7 fields (name, email, company, role, size, phone, referral source). No risk reversal near any CTA. Recommends: "Start My Free Trial" + cut to 3 fields + "14-day free trial. No credit card."
--> **UX audit agent** returns: Full site nav present (7 links). Mobile CTA below fold. Page load 3.8s due to uncompressed hero image. No sticky CTA on mobile.

### Merge (orchestrator assembles)
Slots all Layer 1 outputs into unified audit: Hero Assessment -> Trust Assessment -> CTA Assessment -> UX Assessment.

### Layer 2: Sequential Dispatch
--> **Message match agent** receives merged output + traffic source data. Finds: Google Ad promises "real-time" and "dashboard" — headline mentions neither. Ad says "14-day free trial" — page says "Get Started" with no trial mention. LinkedIn ad not checked (`[BLOCKED: no ad copy provided]`). Organic meta title partially matches. Scores: Google Ads = Mismatch, Organic = Partial Match.
--> **Prioritization agent** receives message-match output. Consolidates all findings. Ranks by ICE:
  1. Rewrite headline for message match (ICE: 9.3)
  2. Cut form from 7 to 3 fields (ICE: 8.7)
  3. Add risk reversal near hero CTA (ICE: 8.0)
  4. Move testimonial above fold (ICE: 7.0)
  5. Remove navigation links (ICE: 6.7)
  6. Compress hero image for speed (ICE: 6.3)
  7. Add sticky CTA on mobile (ICE: 6.0)

### Dispatch: Critic Agent --> PASS
Scores: Completeness 5, Specificity 5, Evidence 4, Prioritization 5, Actionability 5. Average: 4.8/5. All quality gate items checked. Approved.

### Final Artifact

```markdown
---
skill: lp-optimization
version: 1
date: 2026-03-17
status: draft
---

# LP Audit — Acme Analytics Free Trial Page

## Headline Assessment

Current: "The Best Analytics Platform for Modern Teams"
4-U Score: 1/4 (Useful only — not Unique, not Urgent, not Ultra-specific)

Recommended: "See every metric your team tracks — one screen, updated every 5 minutes."
4-U Score: 4/4

## Message Match
Traffic source: Google Ads — "real-time analytics dashboard"
Current headline mentions neither "real-time" nor "dashboard" → broken match.
Fix: Echo "real-time dashboard" in headline.

## Social Proof Audit
- No testimonials above fold → add strongest result quote near hero CTA
- Customer logos present but below fold → move 3 logos above fold

## Form Audit
Current: 7 fields (name, email, company, role, size, phone, referral source)
Recommended: 3 fields (name, email, company) — collect rest via progressive profiling after signup
Expected impact: ~40% form completion improvement

## Priority Action Items
| # | Fix | Expected Impact | Effort | ICE |
|---|-----|----------------|--------|-----|
| 1 | Rewrite headline for message match | High | Low | 9.3 |
| 2 | Cut form to 3 fields | High | Low | 8.7 |
| 3 | Add risk reversal near hero CTA | High | Low | 8.0 |
| 4 | Move testimonial above fold | Medium | Low | 7.0 |
| 5 | Remove navigation links | Medium | Low | 6.7 |
| 6 | Compress hero image | Medium | Low | 6.3 |
| 7 | Add sticky CTA on mobile | Medium | Medium | 6.0 |
```

---

## Anti-Patterns

**Redesign without diagnosis** — Jumping to "make it look better" without identifying what's actually blocking conversion. Diagnose before prescribing. **INSTEAD:** Run the full audit (Route B) to identify specific blockers, then fix in priority order.

**Testing design before copy** — A/B testing button colors or layouts when the headline doesn't pass the 4-U test. Copy is responsible for 80%+ of conversion impact. **INSTEAD:** Fix the words before the visuals. Follow the testing priority order: headlines > offers > CTAs > layout > forms.

**Ignoring mobile experience** — Optimizing for desktop when 60%+ of traffic is mobile. **INSTEAD:** Check thumb zone placement for CTAs, ensure forms are completable one-handed, verify load time on mobile networks, add sticky CTA for long pages.

**Social proof without specificity** — "Trusted by thousands of companies" is weaker than "Used by 3,247 teams including Stripe and Notion." **INSTEAD:** Every social proof element must include specific numbers, named companies, or measurable results.

**Multiple competing CTAs** — Primary CTA, secondary CTA, sidebar CTA, and exit-intent popup all fighting for attention. **INSTEAD:** One primary CTA per page — secondary CTAs must not visually compete. Audit the CTA hierarchy.

**Vague audit recommendations** — "Improve the headline" or "Add social proof" without specifics. **INSTEAD:** Every recommendation must include: what was observed, which principle it violates, and exact replacement text or action.

**Skipping message match** — Optimizing page copy without checking if it matches the traffic source. **INSTEAD:** Always verify message match first. A perfectly written headline that doesn't match the ad will still bounce visitors.

---

## Agent Files

### Sub-Agent Instructions (agents/)
- [agents/hero-audit-agent.md](agents/hero-audit-agent.md) — Headline, subheadline, hero CTA, above-the-fold
- [agents/trust-audit-agent.md](agents/trust-audit-agent.md) — Social proof, testimonials, credibility signals
- [agents/cta-audit-agent.md](agents/cta-audit-agent.md) — CTAs, risk reversal, form fields, conversion friction
- [agents/ux-audit-agent.md](agents/ux-audit-agent.md) — Navigation, mobile, speed, cognitive load
- [agents/message-match-agent.md](agents/message-match-agent.md) — Traffic source message continuity
- [agents/prioritization-agent.md](agents/prioritization-agent.md) — ICE scoring, testing roadmap
- [agents/critic-agent.md](agents/critic-agent.md) — Quality gate, PASS/FAIL, rewrite routing
- [agents/_template.md](agents/_template.md) — Reusable template for creating new agent files

### Shared References (references/)
- [references/core-principles.md](references/core-principles.md) — Headlines, value props, CTAs, forms, message match, PAS
- [references/social-proof-trust.md](references/social-proof-trust.md) — Social proof hierarchy, biases, trust signals
- [references/ux-design.md](references/ux-design.md) — Visual hierarchy, mobile optimization
- [references/advanced-psychology.md](references/advanced-psychology.md) — Headline formulas, close sequences, pricing, urgency
- [references/testing-optimization.md](references/testing-optimization.md) — A/B testing, tracking
- [references/implementation-checklist.md](references/implementation-checklist.md) — Pre-launch checklists

**Sources:** [CopyHackers](https://copyhackers.com), [CXL](https://cxl.com), [Unbounce](https://unbounce.com/landing-page-articles/)
