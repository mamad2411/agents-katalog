---
name: design-grill
description: Design intent grilling session. Interviews the user relentlessly about visual direction — brand personality, audience, references, color, typography, animation level, component style — before any UI work begins. Resolves every ambiguous design decision and writes a DESIGN-BRIEF.md that all other UI skills can reference. Use before starting /uiux, /tokens, /animate, or /landing on a new project, or when the user wants to establish visual direction, says "what should our UI look like", or invokes /design-grill.
---

# /design-grill — Design Intent Interview

Establishes a shared, specific visual direction before any pixels are touched. Asks one question at a time. Challenges vague answers. Outputs a `DESIGN-BRIEF.md` that becomes the north star for every other UI skill.

Full question tree and what to probe for: [QUESTIONS.md](QUESTIONS.md)

---

## How This Works

Ask **one question at a time**. After each answer:
1. If the answer is vague → challenge it. "Clean and modern" is not an answer.
2. If the answer reveals a constraint → note it and probe further.
3. If the answer is specific → affirm it, note it, move to the next question.
4. If the answer contradicts a previous answer → surface the contradiction immediately.

Provide your **recommended answer** with each question. The user can adopt it, reject it, or refine it.

Do not summarise or repeat back what the user said at length. Tight acknowledgement, then the next question.

---

## Phase 0 — Read Existing Context

Before asking anything, read what already exists:

```bash
# Check for existing design brief
ls DESIGN-BRIEF.md 2>/dev/null

# Check for existing tokens
find . -name "globals.css" -o -name "tailwind.config.*" | grep -v node_modules | head -3

# Check for existing brand colors in tokens
grep -rn "primary\|brand\|color" . --include="globals.css" --include="tailwind.config.ts" 2>/dev/null | head -10

# Check for any existing screenshots in /tmp from prior skill runs
ls /tmp/uiux-*.png /tmp/a11y-*.png /tmp/landing-*.png 2>/dev/null | head -5
```

If a `DESIGN-BRIEF.md` already exists: read it, summarise it to the user in two sentences, and ask whether they want to continue from it or start fresh.

If an existing design system is partially in place: read it and use it as grounding. Don't ask questions that are already answered by the codebase.

---

## Phase 1 — The Interview

Work through 12 questions in order. Ask each one, wait for the answer, then challenge or affirm before moving on.

---

### Q1 — Product category

> "What kind of product is this?"

Choose the most specific match:
- **SaaS app** — dashboard, settings, data views, forms
- **Developer tool** — CLI, SDK docs, API reference, playground
- **Consumer app** — social, e-commerce, lifestyle, entertainment
- **Marketing site** — landing page, pricing, blog
- **Internal tool** — admin panel, ops dashboard, back-office
- **Design system / component library** — documentation, playground, showcase

**Why it matters:** SaaS apps follow different visual conventions than consumer apps. Developer tools tolerate density that would kill a consumer app.

**Probe if vague:** "Is the primary surface a dashboard with data, or a flow of pages users move through?"

---

### Q2 — Target user (be specific)

> "Who exactly is using this? Describe one specific person."

**Recommended:** Push for a concrete persona. "Developers" is not an answer.

Good answer: "Senior frontend engineers at mid-size SaaS companies, 5+ years experience, already use Tailwind and shadcn/ui."
Bad answer: "Developers and designers."

**Probe:**
- How technical are they? (Affects density tolerance and jargon level)
- What device/context do they use it on? (Desktop-heavy professional app vs mobile-first consumer)
- Are they using it under time pressure or in a reflective state?

**Why it matters:** A product used by stressed engineers at 2am needs a different visual tone than a lifestyle app used for leisure.

---

### Q3 — Brand personality (5 adjectives)

> "Describe the brand personality in 5 adjectives. Pretend the product is a person — how do they carry themselves?"

**Ban these words immediately:** clean, modern, minimal, professional, simple, sleek, intuitive. These mean nothing — press for something with friction.

**Good adjectives:** authoritative, playful, precise, warm, unapologetic, calm, irreverent, expert, honest, serious, delightful, focused, bold, quiet.

**Pairs that define a tone:**
- "Expert but approachable" → thinks carefully, explains clearly, no jargon
- "Confident and direct" → bold typography, clear hierarchy, no hedging
- "Calm and focused" → lots of whitespace, muted palette, no visual noise
- "Playful but professional" → fun touches in the details, solid structure overall

**Probe:** "If this product were a magazine, would it be The Economist, Wired, or a design agency's portfolio?"

---

### Q4 — Emotional goal

> "How should the user FEEL when they use this product? Not what they should think — what they should feel."

One or two words. This is the emotional north star.

**Common answers and what they mean:**
- **Confident** → clear hierarchy, no ambiguity, strong CTAs, good empty states
- **Productive** → dense information layout, fast interactions, minimal chrome
- **Delighted** → micro-animations, personality in copy, surprising details
- **Calm** → generous whitespace, muted palette, no urgent visual noise
- **Powerful** → large typography, bold color, expressive UI
- **Trusted** → conservative palette, social proof, polished details

**Probe:** "What's the opposite of that feeling — what would make the user feel the opposite when using a competitor?"

---

### Q5 — Visual references

> "Name 3 products, websites, or apps where you look at them and think 'I want ours to feel like that.' They don't have to be in your industry."

**For each reference, ask:** "What specifically about it? The color? The typography? The whitespace? The animations? The illustration style?"

Vague reference: "I like Linear."
Good reference: "I like Linear's typography — the tight heading scale, the Inter font at high weight, and how much whitespace they use between sections."

**Red flag:** If all three references are in the same industry, the product will look generic. Good references span industries.

**Probe:** "Is there a product you think looks terrible that we should make sure ours never resembles?"

---

### Q6 — Competitors

> "Who are your 3 main competitors? What does their UI look like, and what do you want to consciously avoid?"

**Why it matters:** "We don't want to look like [competitor]" is extremely useful design direction. If all competitors use dark blue and rounded cards, you can immediately differentiate with light surfaces and sharp corners.

**Probe:**
- "Do you want to look adjacent to competitors (reassuringly familiar) or deliberately different?"
- "Is there a reason users would trust us over them based on visual first impression?"

---

### Q7 — Color direction

Ask these as sub-questions:

**7a. Light or dark default?**
> Recommended: light with a dark mode variant. Most SaaS apps default light — dark is a power-user preference.

**7b. Warm, cool, or neutral?**
> Cool (blues, grays) reads as technical, precise, trustworthy.
> Warm (ambers, earth tones) reads as friendly, human, approachable.
> Neutral (pure grays) is the safe choice — add a strong brand accent.

**7c. Single brand color or full palette?**
> Single color + neutral grays = sophisticated, focused (most good SaaS apps).
> Full color palette = consumer app, marketing site, or high-energy brand.

**7d. Saturated or muted?**
> Saturated (vivid, electric) = energetic, loud, startup.
> Muted (desaturated, dusty) = sophisticated, serious, mature.

**Synthesise:** After the four answers, name a specific color direction: "Sounds like: cool blue primary, light mode default, muted saturation, gray neutrals. That maps to something like blue-600 as primary, gray-50 as background."

---

### Q8 — Typography direction

**8a. Geometric sans vs humanist sans vs serif vs mono?**
- **Geometric sans** (Inter, Geist, DM Sans) — neutral, technical, modern. Works everywhere.
- **Humanist sans** (Nunito, Plus Jakarta, Figtree) — friendly, rounded, warmer.
- **Serif** (Playfair Display, Lora, Freight) — editorial, premium, publishing.
- **Mono** (JetBrains Mono, Fira Code, Berkeley Mono) — developer tool, technical purity.

**8b. One font or two?**
> One font = coherent, simpler. Works with weight variation (Regular/Medium/Bold/Black).
> Two fonts = display font for headings, readable font for body. Adds personality but must be paired carefully.

**8c. Information density?**
> Spacious (marketing, landing pages, premium) vs Dense (dashboards, developer tools, data products).

**Synthesise:** "That sounds like Inter for everything, with tight heading scale and body at 15–16px. I'll use 700 for headings, 400/500 for body."

---

### Q9 — Component style

Four axes — ask all four:

**9a. Corner radius?**
- Sharp (0px) — serious, precise, technical
- Slightly rounded (4px) — the default, nothing to say
- Rounded (8–12px) — friendly, approachable
- Very rounded (full / pill) — playful, consumer-facing

**9b. Elevation (shadows)?**
- Flat (no shadows, borders only) — modern, minimal, 2022+
- Subtle (very soft shadows) — professional, the safe choice
- Elevated (clear shadow on cards) — traditional SaaS, legacy feel
- Very elevated (dramatic shadows) — landing pages, marketing

**9c. Density?**
- Spacious (marketing, premium)
- Balanced (the default)
- Dense (dashboards, data tools)

**9d. Border style?**
- Heavy borders (1-2px everywhere) — structured, clear hierarchy
- Light borders (1px, subtle color) — the standard choice
- Borderless (shadows only) — modern, minimal

**Synthesise:** Turn the four answers into a concrete component style: "Sharp corners, flat (border only), dense, light borders — that's a developer tool aesthetic. Think VS Code or Linear."

---

### Q10 — Animation level

> "How animated should this product feel?"

- **Minimal** — nearly static. Only essential feedback (button active state, form error). No enter/exit animations.
- **Subtle** — 100–200ms transitions everywhere. Modal fades. Hover states. Nothing distracting.
- **Expressive** — staggered list animations, scroll reveals, modal springs. Polished and deliberate.
- **Very animated** — parallax, hero timelines, scroll-driven storytelling. Only for marketing sites.

**Recommended:** Subtle for SaaS apps, Expressive for landing pages, Minimal for developer tools.

**Probe:** "Is there a specific interaction that should feel especially good? (Opening a modal, completing a form, loading data)"

---

### Q11 — Dark mode

> "Is dark mode required from day one, a nice-to-have, or not needed?"

- **Required now** — token system must account for it from the start. Both modes ship together.
- **Later** — build with tokens so dark mode can be added, but don't implement it yet.
- **Not needed** — simplifies the token system. Light only.

**Probe:** "Is your audience the type to have their OS in dark mode? (Developers: usually yes. Consumers: depends on product.)"

---

### Q12 — The defining screen

> "If there's one screen that should feel absolutely perfect — the one that defines the product's visual identity — which one is it?"

This is the screen `/uiux` should tackle first. It's usually:
- The hero/landing page (first impression)
- The main dashboard (where users spend 80% of time)
- The product's signature interaction (the thing that makes the product unique)

**Probe:** "Why that screen? What does 'perfect' look like there — specifically?"

---

## Phase 2 — Surface Contradictions

Before writing the brief, check for contradictions in the answers:

| Contradiction | Surface it |
|--------------|------------|
| "Dense layout" + "lots of whitespace" | "Dense and spacious are opposites — which wins in tables and forms?" |
| "Minimal animation" + "very expressive landing page" | "Should the marketing site animate more than the app?" |
| "Very rounded corners" + "serious, authoritative" | "Rounded corners skew friendly — is that intentional, or should we pull back to 8px?" |
| "Single brand color" + "multiple competing accent colors in references" | "Your references use color boldly — is a single accent enough, or do you want a second color?" |
| "Light mode default" + "competitor analysis: all competitors use light mode" | "Everyone in your space uses light mode — is dark default a differentiation opportunity?" |

Resolve each contradiction before writing the brief. When a direction is explicitly rejected (not just deprioritised), note it for the **Ruled Out** section — future sessions must not re-propose it without a reason.

---

## Phase 3 — Write the Design Brief

Write `DESIGN-BRIEF.md` to the **project root**. This is a permanent project artifact, not a temp file.

**Template:**
```markdown
# Design Brief — [Product Name]

_Generated by /design-grill on [date]. Update this file when design decisions change._

## Product Context
- **Category:** [SaaS app / developer tool / consumer app / etc.]
- **Target user:** [Specific persona, one sentence]
- **Primary device/context:** [Desktop, mobile, both — and usage context]
- **Defining screen:** [The one screen that must feel perfect]

## Brand Personality
**5 adjectives:** [word], [word], [word], [word], [word]
**Emotional goal:** [One word — how the user should feel]
**Tone:** [Two-sentence description of the brand voice and visual attitude]

## Visual References
- **[Reference 1]** — [What specifically to borrow]
- **[Reference 2]** — [What specifically to borrow]
- **[Reference 3]** — [What specifically to borrow]

## What to Avoid
- Looks like: [competitor 1] — [what specifically]
- Looks like: [competitor 2] — [what specifically]

## Color System
- **Default mode:** Light / Dark / Both
- **Temperature:** Warm / Cool / Neutral
- **Primary color direction:** [e.g., "cool blue — blue-600 range"]
- **Palette approach:** Single accent + neutrals / Full palette
- **Saturation:** Saturated / Muted
- **Specific starting point:** primary: #[hex], background: #[hex], text: #[hex]

## Typography
- **Typeface:** [Font name] — [why it fits]
- **Scale approach:** Spacious editorial / Balanced / Dense information
- **Heading/body:** Same font / Display + text pair
- **Suggested pair:** [Font 1] (headings at 700–800) + [Font 2] (body at 400–500)

## Component Style
- **Corner radius:** Sharp (0) / 4px / 8px / 12px / Full (pill)
- **Elevation:** Flat / Subtle shadow / Elevated cards / Dramatic
- **Density:** Spacious / Balanced / Dense
- **Borders:** Heavy / Light / Borderless
- **Overall:** [One sentence summary — e.g., "Sharp, flat, dense, light borders — developer tool register"]

## Animation
- **Level:** Minimal / Subtle / Expressive / Very animated
- **Key interaction to make feel great:** [Specific interaction]
- **Easing preference:** [e.g., "ease-out entrances, no bouncing"]

## Dark Mode
- Required now / Add later / Not needed

## Decisions Made
| Decision | What was decided | Why |
|----------|-----------------|-----|
| [Topic]  | [Decision]      | [Reason given] |

## Ruled Out
_Directions explicitly rejected during this session. Do not re-propose these without reopening the decision._

| Direction | Why it was rejected |
|-----------|-------------------|
| [e.g., Dark mode default] | [e.g., Primary audience is non-technical — dark mode adoption is low] |
| [e.g., Serif headings] | [e.g., Too editorial — conflicts with the "precise and technical" personality] |
| [e.g., Full color palette] | [e.g., Single accent is intentional — prevents visual noise in a dense dashboard] |

## Open Questions
- [Any decisions deferred or not resolved]
```

**When to update this file:**
- Add to **Ruled Out** any time a direction is explicitly rejected during a future session
- Update **Decisions Made** when a decision changes — don't delete the old row, mark it superseded
- Future skill runs (`/uiux`, `/tokens`, `/animate`) read this file — keep it accurate

---

## Phase 4 — Recommend Next Steps

After writing the brief, tell the user:

1. Which skill to run next (based on the defining screen and the biggest gap):
   - New project with no UI yet → `/uiux` on the defining screen
   - Existing product needing consistency → `/tokens` to establish the token system
   - Landing page that's not converting → `/landing`
   - App with no animation → `/animate`

2. Which token values to set first (based on color + typography decisions):
   ```bash
   # Suggested starting token values from the brief:
   # Primary: [hex]
   # Background: [hex]
   # Text: [hex]
   # Font: [font name]
   ```

3. One thing to prototype before committing to the direction: "Before running `/uiux` on everything, build one card and one button with these values and screenshot it."

---

## Rules

1. **One question at a time.** Never combine two questions into one message.
2. **Challenge vague answers.** "Clean and modern" → "What does clean mean here — few colors, or few elements, or minimal decoration?"
3. **Give a recommended answer with every question.** The user can redirect — they should never face a blank question.
4. **Surface contradictions immediately.** Don't let incompatible answers coexist in the brief.
5. **Read the codebase first.** Don't ask about things already decided in `globals.css` or `tailwind.config`.
6. **The brief is a living document.** It belongs in the project root. It gets updated when decisions change.
7. **No implementation during the interview.** This is discovery only — code comes after the brief.
8. **If the user says "just use your judgment"** — do so, but explain the choice and give them a chance to override.
