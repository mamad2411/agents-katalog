---
name: pitch
description: "Go-to-market launch engine. Use when converting a validated offer spec into ready-to-execute landing page copy, launch posts, GitHub README, email sequence, launch checklist, A/B test spec, and kill criteria."
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F680"
---

# Pitch

Transform an offer-scope build spec into a complete go-to-market launch kit. Produces ready-to-execute landing page copy, platform-specific launch posts, a GitHub product README (with product structure sketch for technical domains), a post-purchase email sequence, an hour-by-hour launch checklist, an A/B test spec, and refined kill criteria -- all grounded in persona data, SWOT findings, and offer-scope positioning.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Pipeline Position

```
signal-scan -> decision-log -> persona-extract -> swot-analysis -> offer-scope -> positioning -> **pitch** -> hunter-log
```

This skill consumes the output of `offer-scope`, `persona-extract`, `swot-analysis`, `decision-log`, and `signal-scan`, and feeds into `hunter-log` for execution tracking. The pitch output is the complete "go live" package -- everything needed to launch the product.

## When to Use

- Converting a validated offer spec into ready-to-execute launch materials
- Generating landing page copy grounded in persona language and offer-scope positioning
- Creating platform-specific launch posts that follow the 80/20 value-first rule
- Building a GitHub product README that serves as both documentation and conversion engine
- Drafting a post-purchase email sequence for nurturing and community building
- Planning a day-by-day launch execution sequence with specific times and platforms
- Defining what to test (headlines, prices, channels) once traffic is flowing
- Sharpening kill criteria inherited from offer-scope with pitch-level specifics

## Trigger Phrases

- "Build the launch kit for [product]"
- "Create pitch materials from this offer spec"
- "I need landing page copy for [product]"
- "Generate the go-to-market package"
- "Turn this offer scope into launch-ready materials"
- "/pitch [offer-scope output]"
- "Deploy artifacts from [pitch doc]"
- "Split the pitch into deployable files"
- "/pitch --deploy-only [pitch-slug or path]"

---

## Deploy-Only Mode

Reads an existing pitch document from the vault and splits/deploys its artifacts without re-generating content. Use when:
- A pitch was generated before the deployment extensions existed
- You want to re-deploy artifacts after editing the pitch document
- Testing the deployment pipeline against an existing pitch

### Deploy-Only Input

One of:
- **Pitch slug**: e.g., `devops-decision-kit-pitch-2026-02-08` (searches `Admin/Product-Discovery/Pitches/`)
- **Full vault path**: e.g., `Admin/Product-Discovery/Pitches/devops-decision-kit-pitch-2026-02-08.md`
- **Absolute path**: the full filesystem path to the pitch markdown

Optional:
- **Launch date**: ISO date for kanban task dates. If omitted, uses relative dates (`T-7`, `T+0`, `T+1`, etc.)
- **Skip list**: Deployment phases to skip (e.g., `--skip emails,kanban` if those are already deployed)

### Deploy-Only Workflow

```
Existing pitch markdown (from vault)
    |
Step 1: Parse pitch document into sections
    |
Step 2: Check what is already deployed (launchpad branch? seeds exist? kanban exists?)
    |
Step 3: Deploy missing artifacts only
    |    ├── Phase 2.4: Launch posts → Obsidian content seeds
    |    ├── Phase 3e: Landing page copy → index.html on launchpad branch
    |    ├── Phase 4.6: Email sequence → individual files on launchpad branch
    |    ├── Phase 5.6: Launch checklist → Obsidian kanban
    |    └── Phase 7.6: Kill criteria → Obsidian Tasks on pitch doc
    |
Step 4: Update Pipeline tracker
    |
Output: Report of what was deployed and where
```

### Parsing Contract

The deploy-only mode reads the pitch markdown and locates content by H2 section headers. The pitch doc may use either short headers (`## Launch Posts`) or phase-numbered headers (`## Phase 2: Launch Posts`). Match on the section name, ignoring any `Phase N:` prefix.

| Pitch Section | Header (either format) | Parser | Deploy Phase |
|---|---|---|---|
| Landing Page Copy | `## Landing Page Copy` or `## Phase 1: Landing Page Copy` | Read all subsections (### Headline through ### Call to Action) and pass to Phase 3e HTML generator | 3e (index.html on launchpad branch) |
| Launch Posts | `## Launch Posts` or `## Phase 2: Launch Posts` | Split by `### {Platform}: {Title}`, `### Reddit r/{sub} Post`, or `### Twitter/X Thread` | 2.4 (Obsidian seeds) |
| Email Sequence | `## Email Sequence` or `## Phase 4: Email Sequence` | Split by `### Email {N}: {Subject} (Day {N})` | 4.6 (individual files) |
| Launch Checklist | `## Launch Checklist` or `## Phase 5: Launch Checklist` | Split by `### Pre-Launch`, `### Launch Day`, `### Week 1`, `### Ongoing Cadence`, `### Month 2-3 Growth` | 5.6 (Obsidian kanban) |
| Kill Criteria | `## Kill Criteria` or `## Phase 7: Kill Criteria` | Read `### 7.1 Week 1 Threshold`, `### 7.2 Month 1 Threshold`, `### 7.3 Month 3 Threshold` (also accepts unnumbered `### Week 1`, etc.) | 7.6 (Obsidian Tasks) |

**If a section is missing or cannot be parsed, skip that deployment phase and warn the operator.** Do not fail the entire deploy because one section is malformed.

### Deploy-Only Checks

Before deploying each artifact:

1. **Content seeds** (Phase 2.4): Check if `{vault}/Writing/Content-Briefs/{product-slug}-{platform}-seed-*.md` already exists. If yes, skip and warn (or append under `## Update: {timestamp}` per conventions).
2. **Landing page HTML** (Phase 3e): Check if `index.html` exists on the launchpad branch root. If yes, skip and warn. If the branch does not exist, warn that Phase 3d (launchpad branch creation) should run first.
3. **Email files** (Phase 4.6): Check if `emails/` directory exists on the launchpad branch. If yes, skip and warn. If the branch does not exist, warn that Phase 3d (launchpad branch creation) should run first.
4. **Kanban** (Phase 5.6): Check if `{vault}/Admin/Product-Discovery/Pitches/{product-slug}-launch-checklist.kanban.md` exists. If yes, skip and warn.
5. **Review reminders** (Phase 7.6): Check if the pitch markdown already has a `## Review Reminders` section. If yes, skip and warn.

### Deploy-Only Output

Returns a deployment report:

```json
{
  "pitch_ref": "devops-decision-kit-pitch-2026-02-08",
  "deployed": {
    "landing_page_html": "index.html (on {product-slug} branch)",
    "content_seeds": ["path/to/seed-1.md", "path/to/seed-2.md"],
    "email_files": ["emails/email-1-welcome.md", ...],
    "kanban": "path/to/launch-checklist.kanban.md",
    "review_reminders": "appended to pitch markdown"
  },
  "skipped": {
    "kanban": "already exists at path/to/..."
  },
  "warnings": ["No launch date specified; using relative dates"]
}
```

---

## Prerequisites

Before starting, the following must be available:

1. **Offer-scope output** -- A completed offer-scope result containing: product name, format, price, value equation, build spec, positioning (headline, subheadline, bullet points, objection handlers, social proof angle, guarantee), distribution plan, revenue model, and kill criteria
2. **Persona extraction output** -- The persona used by offer-scope, containing: pain stories (with situation/pain/workaround/emotional state/evidence), decision triggers, objections, willingness-to-pay data, and channel behavior
3. **SWOT analysis data** -- The SWOT for this hypothesis, containing: validated strengths, key weaknesses, opportunities, threats, risk registry, and moat assessment
4. **Positioning data** (optional, recommended) -- If a positioning skill run exists, its output becomes the PRIMARY source for: landing page headline (from messaging hierarchy lead message), problem section (from competitive alternatives), copy anti-rules (from anti-messaging). When positioning output is available, use it instead of offer-scope Phase 5 positioning. If no positioning output exists, fall back to offer-scope positioning as before.
5. **Decision log entry** -- The decision record for the chosen opportunity
6. **Signal scan data** -- The original signal scan with PAIN, SPEND, COMPETITIVE, and AUDIENCE signals

If any of these are missing, prompt the user to run the upstream skill first or provide the data manually. The pitch skill is a synthesis layer -- it assembles and refines upstream outputs into execution-ready materials, not a research layer.

---

## Input

The skill expects the following input structure (assembled from upstream skill outputs):

```typescript
interface PitchInput {
  offer: {
    product_name: string
    format: string
    price_point: string
    ship_time: string
    value_equation: {
      dream_outcome: string
      perceived_likelihood: string
      time_delay: string
      effort_sacrifice: string
    }
    build_spec: {
      deliverable: string
      transformation: string
      sections: { title: string, estimated_time: string, content_type: string }[]
    }
    positioning: {
      headline: string
      subheadline: string
      bullet_points: string[]
      objection_handlers: { objection: string, counter: string }[]
      social_proof_angle: string
      guarantee: string
    }
    distribution_plan: {
      launch_channel: string
      launch_strategy: string
      ongoing_channels: string[]
      email_capture: boolean
    }
    revenue_model: {
      unit_price: number
      first_week_target: { units: number, revenue: number }
      first_month_target: { units: number, revenue: number }
      assumptions: string[]
    }
    kill_criteria: string[]
  }
  persona: {
    persona_name: string
    pain_stories: {
      situation: string
      pain: string
      current_workaround: string
      emotional_state: string
      evidence: string
    }[]
    decision_triggers: { trigger: string, urgency: string, channel: string }[]
    objections: { objection: string, counter: string }[]
    willingness_to_pay: { range: string, evidence: string, anchor_products: string[] }
    channels: { platform: string, behavior: string }[]
  }
  swot: {
    verdict: string
    validated_strengths: string[]
    key_risks: string[]
    modifications: string[]
    moat_assessment: { current_strength: string, timeline: object }
  }
  positioning?: {
    lead_message: string                // headline source (overrides offer.positioning.headline)
    category_frame: string              // subheadline / positioning line
    primary_hook: string                // above-the-fold emotional hook
    anti_messaging: { phrase: string, use_instead: string }[]  // copy rules
    competitive_alternatives: string[]  // problem section source
    icp_title: string                   // copy targeting
    first_conversation_moats: string[]  // credibility claims
    positioning_canvas_ref: string      // artifact slug for cross-reference
  }
  domain: string
  opportunity: string
  offer_ref: string
  persona_ref: string
  swot_ref: string
  positioning_ref?: string  // slug of the positioning-canvas artifact
  decision_ref: string
  signal_scan_ref: string
}
```

---

## Workflow

```
Offer Spec + Persona + SWOT + Decision + Signal Scan (from upstream)
    |
Phase 1: Landing Page Copy (complete, ready to paste)
    |
Phase 2: Launch Posts (platform-specific, ready to publish)
    |
Phase 3: GitHub Product Repo (3a: structure + 3b: README + 3c: hero + 3d: branch/PR + 3e: landing page HTML)
    |
Phase 4: Email Sequence (3-5 emails, post-purchase nurture)
    |
Phase 5: Launch Checklist (hour-by-hour execution plan)
    |
Phase 6: A/B Test Spec (what to test once traffic flows)
    |
Phase 7: Kill Criteria Refinement (time-bounded, measurable)
    |
Phase 8: Slide Deck (Slidev presentation with extracted SVG diagrams)
    |
Output: JSON spec + Markdown summary -> vault
```

---

## Phase 1: Landing Page Copy

Generate complete, paste-ready landing page copy with headline, subheadline, above-the-fold hook, problem section (minimum 3 persona pain story references), solution section, what's inside breakdown, social proof strategy, pricing with value stack and guarantee, FAQ mapped to persona objections (minimum 5), and primary/secondary CTAs. Every line must trace to persona data or offer-scope positioning.

```
Read ${SKILLS_DIR}/pitch/references/landing-page-template.md
```

---

## Phase 2: Launch Posts

Generate 2-3 platform-specific posts following the 80/20 value-first rule. Includes primary channel post, LinkedIn version, and Twitter/X thread. Each post is ready to publish and provides genuine standalone value. Also writes Obsidian content seeds for the content-planner pipeline and integrates with the `::linkedin` convention for LinWheel scheduling.

```
Read ${SKILLS_DIR}/pitch/references/launch-posts-templates.md
```

### 2.5 LinkedIn Launch Post Convention (`::linkedin`)

For LinkedIn launch posts, write them to Obsidian with the `::linkedin` prefix in the note body (before the post content). This triggers the OpenClaw ambient pipeline:

1. OpenClaw detects the `::linkedin` prefix in the Obsidian note
2. Pipes the note content to LinWheel (the LinkedIn content generator + scheduler)
3. The operator reviews and approves the post in LinWheel
4. LinWheel schedules and publishes to LinkedIn

**Format**: Write the LinkedIn seed to `{vault}/Writing/Content-Briefs/{product-slug}-linkedin-seed-{YYYY-MM-DD}.md` with `::linkedin` as the **very first line of the file** (line 1, before frontmatter). NOT after frontmatter — BEFORE it. The `::linkedin` trigger must be byte 0 of the file or the OpenClaw pipeline won't fire. Frontmatter follows on line 2+. This makes it a live launch post that can be approved and scheduled, not just a draft.

The full pipeline: pitch skill → Obsidian seed → OpenClaw → LinWheel → LinkedIn publication.

---

## Phase 3: GitHub Product README

Multi-sub-phase: 3a produces product structure sketch (technical domains only, enriched with buildlog data), 3b produces README conversion copy, 3c generates hero image via ComfyUI (or writes image intent comment), 3d deploys to launchpad repo branch with PR, and 3e generates a single-file dark-theme landing page HTML from Phase 1 copy with full design system, OG tags, and mobile responsiveness.

```
Read ${SKILLS_DIR}/pitch/references/github-readme-template.md
```

---

## Phase 4: Email Sequence

Generate 5 post-purchase emails: welcome/delivery (Day 0), quick win (Day 2), story/credibility (Day 4), objection handler (Day 6), and community invite (Day 7). Each email has one job, specific subject lines, and practitioner-to-practitioner tone. Outputs individual email files to the launchpad branch `emails/` directory.

```
Read ${SKILLS_DIR}/pitch/references/email-sequence-template.md
```

---

## Phase 5: Launch Checklist

Step-by-step execution plan: pre-launch setup (Days -7 to -1) with specific tools and time estimates, hour-by-hour launch day sequence, daily Week 1 follow-up actions, ongoing cadence (Weeks 2-4), and Month 2-3 growth actions. Outputs an Obsidian Kanban board with dated tasks.

```
Read ${SKILLS_DIR}/pitch/references/launch-checklist-template.md
```

---

## Phase 6: A/B Test Spec

Define testable variables for solo operators with 100-500 visitors: 2-3 headline variants with rationale, 2-3 price variants cross-referenced with SPEND data, ranked channel priority, metrics with targets and measurement methods, and decision thresholds defined before testing. Sequential testing approach -- one variable at a time.

```
Read ${SKILLS_DIR}/pitch/references/ab-test-spec.md
```

---

## Phase 7: Kill Criteria Refinement

Sharpen kill criteria from offer-scope and SWOT with pitch-level specifics: Week 1, Month 1, and Month 3 thresholds with exact numbers and actions. Includes qualitative signal interpretation (iterate vs pivot vs kill), pivot triggers with direction, and Obsidian Tasks output with review reminder dates queryable by Dataview.

```
Read ${SKILLS_DIR}/pitch/references/kill-criteria-template.md
```

---

## Phase 8: Slide Deck (Slidev)

Generate a Slidev presentation summarizing the validation pipeline output. The deck lives in `launchpad/deck/` and deploys alongside the landing page.

### 8.1 Structure

The deck is a single `slides.md` file using Slidev's markdown syntax. Global config in frontmatter, per-slide frontmatter between `---` separators. Speaker notes go in `<!-- -->` comments at the bottom of each slide.

Required slides (in order):
1. **Cover** — product name + validation date (use `layout: cover` in global frontmatter)
2. **Opportunity** — the gap diagram
3. **Evidence Wall** — signal count + key stats
4. **Reddit Voices** — 3 direct quotes with source citations
5. **SDP Scoring** — bar chart of opportunity ranking
6. **Personas** — persona cards with WTP
7. **Four Forces** — push/pull/inertia/anxiety
8. **Two Offers** — offer tiers side by side
9. **Curriculum Stack** — week-by-week breakdown
10. **Revenue Model** — bar chart of revenue streams
11. **Revenue Breakdown** — table with unit economics (Stream / Unit Economics / Annual Estimate)
12. **Competitive Map** — price vs depth scatter plot
13. **Execution Calendar** — timeline with milestones and kill gate
14. **Kill Criteria** — gate cards with thresholds
15. **Bias Check** — status indicators per bias type
16. **Next Steps** — table with Milestone / Deadline / Kill Condition columns
17. **Appendix** — asset map linking to all pipeline artifacts
18. **Closing** — pipeline attribution

### 8.2 SVG Conventions

All diagrams are extracted SVG files in `deck/public/`. Reference them with `<img src="/filename.svg">` tags. NEVER inline complex SVGs in the markdown — Vue's template compiler will mangle them.

SVG style rules:
- **Font**: `font-family="'Inter', sans-serif"` on all text elements. Never use Caveat, cursive, or handwriting fonts.
- **Displacement filter**: `feDisplacementMap scale="0.4"` max. Subtle texture, not wobbly hand-drawn.
- **Color palette**: background `#0d1117`, text `#eee0cc`, muted `#8b949e`, coral `#e88072`, red `#f87171`, green `#4ade80`, yellow `#facc15`
- **XML safety**: Always escape `<` as `&lt;` in SVG text content. Unescaped `<` breaks the SVG parser.
- **Sizing**: Use `viewBox` for dimensions. Set `style="width:100%;max-width:NNNpx;"` on the root `<svg>` element.
- **Text overflow**: Ensure text fits inside containing boxes. For label text inside bounded shapes, measure the text width against the shape width and reduce font-size or widen the shape if needed.
- **Overlap**: Maintain minimum 50px center-to-center spacing between elements with labels. Check that label text from one element doesn't collide with the heading of the next.

SVG animation rules:
- Use CSS `@keyframes` inside `<style>` blocks within the SVG for auto-playing animations (pulse, blink, breathe). These work in `<img>` tags.
- For hover interactivity, use `<object data="..." type="image/svg+xml">` instead of `<img>`. Add `:hover` CSS rules inside the SVG's `<style>` block.
- Good candidates for animation: alert indicators (blink), kill/flag states (pulse), highlighted elements (breathe/glow).

### 8.3 Slidev Config

```yaml
theme: default
fonts:
  sans: Inter
  mono: Fira Code
  provider: google
transition: slide-left
css: unocss
drawings:
  persist: false
```

Use `style.css` for global styles (background, heading colors, v-click animation overrides). Do not use scoped `<style>` blocks in slides.

### 8.4 Speaker Notes

Every slide gets presenter notes in `<!-- -->` comments. Notes must:
- State what the slide shows and why it matters
- Reference specific numbers, sources, or upstream pipeline data
- Be written in direct, conversational tone — not LLM summary voice
- Avoid em-dash chains, tricolons, performative honesty, or "landscape/tapestry/crucible" vocabulary

### 8.5 Content Seed Trigger

If generating a LinkedIn content seed, the `::linkedin` trigger tag MUST be byte 0, line 1 of the file — BEFORE frontmatter. This triggers the OpenClaw → LinWheel → LinkedIn pipeline.

```markdown
::linkedin

---
type: content-brief
...
```

---

## Output

The pitch produces multiple output artifacts across the vault and launchpad repo.

**Vault path:** `${VAULT}/`

For the complete output markdown structure (frontmatter, all sections, deployment outputs):

```
Read ${SKILLS_DIR}/pitch/references/output-template.md
```

### Primary Outputs (Vault)

#### 1. JSON Spec: `{vault}/Admin/Product-Discovery/Pitches/{product-slug}-pitch-{YYYY-MM-DD}.json`

Structured data following the schema in [references/output-schema.json](references/output-schema.json). Must validate against that schema.

#### 2. Markdown Summary: `{vault}/Admin/Product-Discovery/Pitches/{product-slug}-pitch-{YYYY-MM-DD}.md`

Human-readable launch kit containing all phase outputs in the structure defined by the output template.

### Deployment Outputs (Launchpad Repo + Vault)

#### 3. Launchpad Product Branch: `github.com/Peleke/launchpad` branch `{product-slug}`
- Full product directory structure from Phase 3a
- Product README from Phase 3b
- Hero image from Phase 3c (or HTML comment with image intent)
- `emails/` directory with individual email files from Phase 4.6
- PR opened against `main` for operator review (Phase 3d)

#### 3b. Landing Page HTML: `index.html` on launchpad branch root
- Single-file HTML landing page generated from Phase 1 copy (Phase 3e)
- Dark theme, mobile responsive, zero dependencies
- Open Graph meta tags for social sharing
- Immediately deployable via Vercel branch preview
- Preview URL: `https://launchpad-git-{product-slug}-northwind-labs.vercel.app`

#### 4. Content Seeds: `{vault}/Writing/Content-Briefs/{product-slug}-{platform}-seed-{YYYY-MM-DD}.md`
- One file per launch post (Phase 2.4)
- Frontmatter: `type: content-brief`, `status: backlog`, platform tag
- Picked up by content-planner for full brief generation after operator review

#### 5. Launch Checklist Kanban: `{vault}/Admin/Product-Discovery/Pitches/{product-slug}-launch-checklist.kanban.md`
- Obsidian Kanban board with Pre-Launch, Launch Day, Week 1, Ongoing columns (Phase 5.6)
- Tasks have dates, checkable on mobile via iCloud sync

#### 6. Review Reminders: Appended to pitch markdown in vault
- Obsidian Tasks format with dates and `#hunter/review` tags (Phase 7.6)
- Week 1, Month 1, Month 3 review dates
- Queryable by Obsidian Tasks and Dataview plugins

#### 7. Pipeline Tracker: `{vault}/Admin/Product-Discovery/Pipeline.md`
- Table of all products with branch links, preview URLs, status
- Updated by pitch skill when creating a new product
- Format:

```markdown
| Product | Branch | Preview URL | Price | Status | Pitch Date |
|---------|--------|-------------|-------|--------|------------|
| {name} | [{slug}](https://github.com/Peleke/launchpad/tree/{slug}) | [Preview]({vercel-url}) | ${price} | spec | {date} |
```

---

## Vault Output Contract

All vault output files are written to the Obsidian vault (iCloud-synced):

```
${VAULT}/
```

**Pitch files:** `Admin/Product-Discovery/Pitches/`
- Filename format: `{product-slug}-pitch-{YYYY-MM-DD}.md` and `{product-slug}-pitch-{YYYY-MM-DD}.json`

**Content seeds:** `Writing/Content-Briefs/`
- Filename format: `{product-slug}-{platform}-seed-{YYYY-MM-DD}.md`

**Launch kanban:** `Admin/Product-Discovery/Pitches/`
- Filename format: `{product-slug}-launch-checklist.kanban.md`

**Pipeline tracker:** `Admin/Product-Discovery/Pipeline.md`

**Rules:**
- If a file already exists at the target path: APPEND under `## Update: {ISO timestamp}`, do NOT overwrite
- Frontmatter MUST include: `type: pitch`, `date`, `status: draft`, `tags` (minimum: `hunter/pitch`, `hunter/domain/{slug}`)

---

## Resources

### references/

- `output-schema.json` -- JSON Schema for the structured pitch output. Load when producing the JSON file to validate against.
- `landing-page-template.md` -- Phase 1: landing page copy structure, section breakdown, copy rules
- `launch-posts-templates.md` -- Phase 2: platform-specific post templates, 80/20 rule, Obsidian seed output, `::linkedin` convention
- `github-readme-template.md` -- Phase 3: product structure sketch, README copy, hero image, launchpad branch, landing page HTML design system
- `email-sequence-template.md` -- Phase 4: 5-email post-purchase sequence, tone rules, file output format
- `launch-checklist-template.md` -- Phase 5: pre-launch through Month 2-3 execution plan, Obsidian Kanban output
- `ab-test-spec.md` -- Phase 6: headline/price variants, channel priority, metrics, decision thresholds
- `kill-criteria-template.md` -- Phase 7: time-bounded thresholds, qualitative signals, pivot triggers, Obsidian Tasks output
- `output-template.md` -- Full markdown output structure and deployment output inventory

### README.md

- The full Launch Architecture framework reference, including intellectual lineage (Ogilvy, Schwartz, Halbert, Godin, Dunford, Fitzpatrick, Lavingia, Hoy, McKenzie), detailed methodology, anti-patterns, and calibration examples. Consult for deep framework questions during a pitch session.

---

## Quality Checklist

Run this checklist before delivering the pitch:

- [ ] Landing page copy is complete and standalone -- someone could build a page from it
- [ ] Every line of landing page copy traces to persona data or offer-scope positioning
- [ ] Headline stops the scroll -- uses persona's exact pain language, not generic marketing
- [ ] Problem section uses minimum 3 persona pain story references with specific language
- [ ] FAQ section maps each Q to a specific persona objection
- [ ] Launch posts follow 80/20 value-first rule -- genuine value even without buying
- [ ] Launch posts follow platform norms (no self-promo spam, platform-specific formatting)
- [ ] Each launch post is ready to publish, not an outline or draft
- [ ] GitHub README is excellent technical documentation first, marketing second (if technical domain)
- [ ] Product structure sketch covers directory layout, file manifest, learning path (if technical domain)
- [ ] Free preview in README is genuinely useful -- not a teaser but real, usable content
- [ ] Email sequence has specific subject lines -- not "Hey!" but specific to the content
- [ ] Each email has ONE job -- no multiple CTAs crammed into a single email
- [ ] Email tone is practitioner-to-practitioner, not marketer-to-mark
- [ ] Launch checklist has specific dates, times, and platforms -- not "post on social media"
- [ ] Launch day plan is hour-by-hour with specific actions
- [ ] A/B test spec has measurable metrics with decision thresholds defined before testing
- [ ] Price variants are grounded in SPEND data, not guesses
- [ ] Kill criteria are time-bounded and measurable -- "sell 10 units in 14 days" not "get traction"
- [ ] Kill criteria distinguish between iterate, pivot, and kill signals
- [ ] All upstream refs linked (offer_ref, persona_ref, swot_ref, decision_ref, signal_scan_ref)
- [ ] JSON output validates against `references/output-schema.json`
- [ ] Markdown output has correct frontmatter (type: pitch, date, status: draft, tags, all refs)
- [ ] Both files are saved to vault `Admin/Product-Discovery/Pitches/`
- [ ] Launchpad branch created with product structure, README, hero image, and emails/
- [ ] Landing page index.html generated from Phase 1 copy and committed to launchpad branch
- [ ] Landing page renders at mobile (640px) and desktop, no horizontal scroll
- [ ] Landing page has zero external dependencies (no CDN, no JS, no external CSS)
- [ ] Open Graph meta tags present with product name, description, and hero image URL (if hero exists)
- [ ] PR opened against launchpad main with review checklist
- [ ] Content seeds written to `Writing/Content-Briefs/` with correct frontmatter
- [ ] Launch checklist written as Obsidian kanban with dated tasks
- [ ] Kill criteria review reminders appended with Obsidian Tasks format (dates, #hunter/review)
- [ ] Pipeline tracker updated with new product row
- [ ] All prose content reviewed by buildlog_gauntlet Bragi persona (all rules)
- [ ] Deploy-only mode: all deployment phases either succeeded or were skipped with warnings (no silent failures)
