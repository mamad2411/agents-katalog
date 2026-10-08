---
name: design-mapper-skill
description: >-
  Intelligent design brief router. Takes any design request and emits a structured
  routing plan — which skills to load, in what order, with what focus parameters.
  Always load this skill FIRST when receiving a design brief. It is the entry point
  for the entire modular design system.
  Trigger on: "design a", "create UI for", "branding for", "what should it look like",
  "color scheme for", "design brief", "visual identity", "/design", intent=design_brief.
license: MIT
metadata:
  author: bilioveloso
  version: "1.3.0"
  date: June 2026
  auto_mode: true
trigger_keywords:
  - design a
  - design brief
  - create UI
  - branding for
  - visual identity
  - what should it look like
  - how should it look
  - UI for
  - app design
  - website design
  - /design
  - /mapper
---

# Design Mapper Skill

**Entry point for the modular design system.** Load this first on any design brief.
It reads the brief, detects signals, and emits a routing plan. The agent then loads
each linked skill in the specified order, carrying context forward.

## The Skill Network

```
design-mapper-skill  ← you are here (always load first)
        │
        ├─► color-combo-skill      (palette, mood, roles)
        ├─► design-effects-skill   (morphism, motion, elevation, effects)
        ├─► font-pairing-skill     (typeface, scale, pairing archetype)
        └─► icon-system-skill      (library, weight, style, animated)
```

Skills are independent but the mapper sequences them and passes carryover context
so each skill builds on the choices made before it.

---

## On First Load

When this skill is first loaded in a new session, before processing any design brief:

1. **Announce the system** in one sentence: "I've loaded design-mapper-skill — the entry point for a modular design system."
2. **Offer the companion skills** — ask the user once:

   > "The full system includes 4 companion skills. Want me to install them now?
   > - **color-combo-skill** — 161 palettes, WCAG contrast ratios, CSS custom property templates
   > - **design-effects-skill** — glass morphism, animation, page-type recipes
   > - **font-pairing-skill** — typeface pairing, type scale, loading strategy
   > - **icon-system-skill** — icon library selection, optical sizing, currentColor"

3. **If the user says yes**, run each command:
   ```bash
   npx skills add bilioveloso/color-combo-skill
   npx skills add bilioveloso/design-effects-skill
   npx skills add bilioveloso/font-pairing-skill
   npx skills add bilioveloso/icon-system-skill
   ```
4. **If the user says no**, proceed. The mapper will fetch companion skills from the web when routing — installation is optional.

**Only ask once per session.** Always offer companions and wait for the user's reply before proceeding — even when a design brief was passed at load time alongside the trigger.

---

## Brief Interview

After the companion offer is resolved, **run a targeted interview before routing.**
The goal is to fill any gaps the brief leaves — not to ask what you already know.

**Auto-fill rule:** scan the brief and pre-fill answers you can infer with high
confidence. Show pre-filled answers marked ✓ so the user can correct them.
Only ask questions that are genuinely open.

Ask all open questions in **a single message**. Wait for the reply, then route.

### The 5 questions

| # | Question | Auto-fill when brief contains… |
|---|---|---|
| 1 | **Primary audience** — who will use this? (role, context, sophistication) | any audience / user description |
| 2 | **Three adjectives** describing the feeling (e.g. "premium, calm, technical") | mood words, style descriptors, vibe language |
| 3 | **Existing brand colors or assets** to respect? (paste hex or say none) | specific hex values, "our brand colors are…" |
| 4 | **One or two reference sites you like + one you'd avoid** (URLs or names) | "like X", "inspired by", "not like Y" |
| 5 | **Platform** — web / mobile app / both / print | any platform mention |

**If all 5 are already answered** from the brief, skip the interview entirely.
Say "I have everything I need from your brief — routing now." and proceed immediately.

**If 1–4 are answered**, only ask the open ones. Never re-ask what the brief answered.

### Interview message format

```
Before I route, I have [N] quick question(s):

✓ Platform: web (from your brief)
✓ Feeling: futuristic, personal, premium (from your brief)

❓ Primary audience — who will use this? (role, context, sophistication level)
❓ Any existing brand colors or assets to respect? (paste hex or say "none")
❓ One reference you love the look of + one to avoid
```

---

## Auto Mode (default on)

After emitting the DESIGN ROUTE block, **automatically load and apply each non-skipped skill in order.** Do not wait for the user to trigger each one manually.

**Source priority for each skill:**
1. Installed locally → read from `~/.claude/skills/<skill-name>/SKILL.md`
2. Not installed → fetch from the raw URL below

| Skill | Raw URL |
|---|---|
| color-combo-skill | `https://raw.githubusercontent.com/bilioveloso/color-combo-skill/main/SKILL.md` |
| design-effects-skill | `https://raw.githubusercontent.com/bilioveloso/design-effects-skill/main/SKILL.md` |
| font-pairing-skill | `https://raw.githubusercontent.com/bilioveloso/font-pairing-skill/main/SKILL.md` |
| icon-system-skill | `https://raw.githubusercontent.com/bilioveloso/icon-system-skill/main/SKILL.md` |

Pass the carryover context from the route when applying each skill (see Carryover Context Rules below).

**To disable auto mode:** If the user says "just route, don't apply" or "route only" — emit the DESIGN ROUTE block and stop. The user can then trigger each skill manually.

---

## How to Use This Skill

When you receive a design brief:

1. **Companion offer** — offer companion skills (see On First Load above). Wait for reply.
2. **Brief Interview** — run the targeted interview (see Brief Interview above). Wait for reply. If brief already answers all 5 questions, skip and proceed immediately.
3. **Detect signals** from the brief + interview answers using the Signal Detectors below.
4. **Resolve the route** using the Routing Table.
5. **Emit the Design Route block** (template at the end).
6. **Auto mode:** load each non-skipped skill in order, reading the carryover notes before each one.
7. **Skip any skill** that has a skip condition (listed per skill below).

---

## Signal Detectors

Read the brief for these signals. Multiple signals compound — use the strongest match.

### Industry / Product Signals

| Signal words in brief | → Route |
|---|---|
| dashboard, analytics, metrics, data viz, admin panel | → Corporate / Slate Command → design-effects: flat |
| SaaS, B2B, enterprise, platform, workspace | → Corporate / Slate Command or Steel Platform |
| fintech, banking, finance, investment, wealth | → Corporate / Finance Trust |
| legal, compliance, regulatory, law firm | → Corporate / Legal Anchor |
| devops, infrastructure, monitoring, ops, uptime | → Corporate / Ops Green |
| healthcare, medical, clinical, hospital, pharma | → Healthcare / Clinical Trust |
| wellness, mental health, meditation, therapy | → Healthcare / Wellness Sage |
| gaming, esports, competitive, streaming, twitch | → Gaming / Cyber Arena or Shadow Protocol |
| fashion, luxury brand, jewelry, watch | → Luxury / Golden Obsession or Emerald Dynasty |
| startup, product launch, consumer app | → Luxury Facade / Caramel Air or Blue Horizon |
| e-commerce, retail, shop, marketplace | → Luxury Facade / Citrus Royal or Coastal Contrast |
| restaurant, food, beverage, café, bakery | → Rustic / Amber Workshop |
| craft brewery, spirits, wine, bar | → Rustic / Smoked Oak OR Gothic / Bone & Wine |
| travel, resort, hotel, hospitality | → Warm Tropical / Palm & Sand or Mango Shore |
| eco, sustainable, green, organic, botanical | → Nature / Forest Floor or Deep Canopy |
| music, event, concert, festival | → Acid Contemporary / Ink Volt or Crimson Grid |
| photography, portfolio, creative studio | → Minimalist / Grey Scale Plus or Bone & Carbon |
| science fiction, tech startup, futuristic | → Otherworldly / Vulcanico or Silver Pulse |
| vintage brand, retro revival, heritage | → Retro / Mustard Record or Rust & Cream |
| beauty, cosmetics, skincare, perfume | → Luxury Facade / Soft Prestige OR Gothic / Midnight Bloom |
| kids, education, learning, playful | → Warm Tropical / Mango Shore (high energy) |
| AI platform, chatbot, copilot, LLM, assistant | → AI-Native UI / minimal chrome, streaming text, dark preferred |
| NFT, web3, blockchain, crypto, DeFi, wallet | → Cyberpunk / dark OLED, neon accent, trust chain visibility |
| mental health, therapy, anxiety, depression, mindfulness app | → Healthcare / Wellness Sage, calm blue, NO motion overload |
| smart home, IoT, home automation, connected devices | → Corporate / Ops Green (dark), real-time status pulse |
| dating, match, swipe, relationship | → Warm Tropical / Mango Shore, card-swipe mobile, high-energy |
| knowledge base, documentation, wiki, help center, docs | → Minimalist / Bone & Carbon, search-first, flat |
| music streaming, playlist, audio player | → Dark OLED / Otherworldly, waveform viz, motion-driven |
| video streaming, OTT, watch, movies, series | → Dark OLED, content carousel, cinematic |
| podcast, episodes, audio show | → Minimalist dark, waveform player, clean |
| food delivery, on-demand, order food | → Warm Tropical / high-energy, image-heavy, Vibrant & Block |
| fitness, gym, workout, training, exercise | → Gaming / energetic, progress rings, gamification |
| job board, recruitment, hiring, career, jobs | → Corporate / Steel Platform, flat, search-filter focused |
| medical clinic, doctor, appointment, patient portal | → Healthcare / Clinical Trust, accessible, booking-forward |
| developer tool, IDE, CLI, terminal, devtool, code editor | → Dark OLED / Otherworldly, monospace, minimal chrome |
| cybersecurity, security, threat, vulnerability, SIEM | → Dark OLED / Otherworldly, threat viz, trust signals |
| news, media, journalism, breaking news | → Editorial / Minimalist, content-dense, fast-loading |
| marketing agency, growth agency, performance marketing | → Acid Contemporary / bold portfolio, results-forward |
| personal finance, budget, expense tracker, net worth | → Corporate / Finance Trust, glass morphism, number animations |
| remote work, collaboration, team, workspace, async | → Corporate / Steel Platform, presence indicators, real-time |
| creator economy, creator, influencer, monetize audience | → Luxury Facade / motion-driven, profile reveals, engagement |
| photography studio, photographer | → Minimalist / Bone & Carbon, full-bleed gallery, minimal text |
| coworking, shared office, desk booking | → Corporate / Slate Command, amenity reveal, space tour |
| e-learning, online course, LMS, learning platform | → Corporate / clean, progress gamification, certificate reveals |
| legal tech, contract, compliance tool | → Corporate / Legal Anchor, flat, no decoration |
| real estate, property listings, home buying | → Luxury / Premium, 3D tour, map-forward |

### Mood / Aesthetic Signals (override or confirm industry route)

| Signal words in brief | → Override |
|---|---|
| premium, exclusive, expensive, luxury, opulent | → confirm or upgrade to Luxury |
| minimal, clean, whitespace, editorial | → override to Minimalist |
| dark, moody, dramatic, night, noir | → override to Gothic / Dark Romance |
| cyber, neon, futuristic, digital, tech | → override to Otherworldly |
| warm, cozy, artisan, handmade | → override to Rustic / Craft |
| bold, disruptive, street, urban, aggressive | → override to Acid Contemporary |
| soft, calm, airy, gentle, wellness | → override to Soft Gradients or Luxury Facade / Soft Prestige |
| nostalgic, vintage, retro, aged | → override to Retro / Vintage |
| natural, earthy, organic, botanical | → override to Nature / Organic |

### Platform / Context Signals

| Signal | → Effect on route |
|---|---|
| mobile app, iOS, Android | → design-effects: suppress heavy glass, prefer subtle elevation; font-pairing: prefer Dynamic Type–friendly scales |
| web app, SaaS, dashboard | → design-effects: glass OK, elevation-heavy layouts OK |
| landing page, marketing site | → design-effects: hero gradient + scroll motion focus |
| print, poster, packaging | → skip design-effects (motion irrelevant); font-pairing: display-weight emphasis |
| dark mode required | → apply dark variant of chosen palette; design-effects: glass morphism preferred |
| accessibility priority | → override accent choices that fail WCAG AAA; flag in route |
| already has brand colors | → skip color-combo; start at design-effects |
| already has fonts chosen | → skip font-pairing |
| icon-free context (text content, doc) | → skip icon-system |

---

## Skip Conditions

| Skill | Skip when |
|---|---|
| color-combo-skill | Brief already specifies exact brand colors |
| design-effects-skill | Platform is print/poster/packaging; or brief is purely typographic |
| font-pairing-skill | Brief already specifies exact typefaces |
| icon-system-skill | No UI components involved (branding only, editorial, print) |

---

## Carryover Context Rules

### color-combo → design-effects
- **Warm palette** (Rustic, Tropical, Retro) → prefer soft elevation, warm shadows, no cold glass
- **Dark palette** (Gothic, Gaming, Otherworldly) → glass morphism strongly preferred; high-contrast borders
- **Corporate palette** → flat or subtle elevation only; no glass; clean dividers
- **Minimalist palette** → zero decoration; solid fills only; no gradients in components

### color-combo → font-pairing
- **Luxury palette** → serif display or high-contrast didone pairing
- **Minimalist palette** → geometric sans, mono optionally for accents
- **Rustic / Craft palette** → slab serif or humanist serif
- **Corporate palette** → humanist sans (Inter, Source Sans), no decorative
- **Gothic palette** → high-contrast serif or editorial condensed
- **Otherworldly / Gaming** → geometric sans or display mono; avoid humanist

### design-effects → icon-system
- **Glass morphism active** → icons need heavier weight (stroke 2px+) to show through blur
- **Flat design** → icons should be stroke-only, light (1.5px), consistent weight
- **Dark background** → prefer filled or outlined icons with high contrast; avoid 1px strokes
- **Animated effects active** → consider animated icons (Lordicon / Lottie) for key interactive moments

---

## Routing Table (Full)

| Brief type | color-combo | design-effects | font-pairing | icon-system |
|---|---|---|---|---|
| B2B SaaS dashboard | Corporate / Slate Command | flat, subtle elevation | humanist sans | stroke, medium weight |
| Fintech / banking | Corporate / Finance Trust | flat, no glass | humanist sans, tabular nums | stroke, minimal |
| Healthcare app | Healthcare / Clinical Trust | flat, clean dividers | humanist sans (Inter) | stroke, accessible |
| Wellness / mental health | Healthcare / Wellness Sage | soft elevation, no motion | rounded humanist | soft filled icons |
| Esports team | Gaming / Cyber Arena | glass, neon glow | geometric display | animated, bold filled |
| Luxury brand site | Luxury / Golden Obsession | subtle glass, editorial | didone or high-contrast serif | none or minimal |
| Fashion startup | Luxury Facade / Caramel Air | soft glass, warm shadows | modern humanist serif | minimal stroke |
| Eco / organic brand | Nature / Forest Floor | soft elevation, no glass | slab serif or humanist | nature-themed stroke |
| Coffee / craft brand | Rustic / Amber Workshop | textured, warm shadows | slab serif | hand-drawn or bold stroke |
| Music / event | Acid Contemporary / Ink Volt | flat, bold color blocks | condensed display | minimal or animated |
| Dark editorial / niche | Gothic / Velvet Crypt | glass, dark shadows | editorial serif | none or minimal |
| Resort / travel | Warm Tropical / Mango Shore | warm glass, blur OK | rounded humanist | filled, playful |
| Mobile consumer app | Luxury Facade / Blue Horizon | subtle elevation, no heavy glass | rounded humanist | filled icons, 24px |
| Portfolio / studio | Minimalist / Bone & Carbon | flat, zero decoration | geometric sans + mono | stroke, ultra-light |
| Retro brand | Retro / Mustard Record | flat, textured optionally | slab serif or vintage display | hand-drawn or none |

---

## Industry Anti-Patterns

Specific things that kill credibility or trust in each context. These override general taste — they are non-negotiable.

| Industry / Context | Avoid |
|---|---|
| SaaS (General) | Excessive animation · Dark mode by default |
| B2B / Enterprise | AI purple/pink gradients · Playful design · Hidden credentials |
| Healthcare / Medical | Bright neon · Motion-heavy animations · AI purple/pink gradients |
| Banking / Traditional Finance | Playful design · Poor security UX · AI purple/pink gradients |
| Fintech / Crypto | Playful design · Unclear fees · AI purple/pink gradients |
| Legal Services | AI purple/pink gradients · Outdated design · Hidden credentials |
| Insurance | AI purple/pink gradients · No trust signals · Confusing pricing |
| Government / Public Service | Ornate design · Low contrast · Motion effects · AI purple/pink gradients |
| E-commerce Luxury | Vibrant & Block-based · Playful colors · Fast animations |
| Mental Health App | Bright neon · Motion overload |
| Beauty / Spa / Wellness | Bright neon · Dark mode · Harsh animations |
| Gaming / Esports | Minimalist design · Static assets |
| Kids / Education | Dark modes · Complex jargon · Muted colors |
| Senior Care / Elderly | Small text · Complex navigation · AI purple/pink gradients |
| Developer Tool / IDE | Light mode by default · Slow performance |
| AI / Chatbot Platform | Heavy chrome · Slow response feedback |
| Logistics / Delivery | Static tracking · No map integration · AI purple/pink gradients |
| Restaurant / Cafe | Low-quality imagery · Outdated hours |
| Photography Studio | Heavy text · Poor image showcase |
| Medical Clinic / Pharma | Confusing booking · Privacy concerns · AI purple/pink gradients |
| NFT / Web3 | Light mode default · No transaction status feedback |
| Podcast Platform | Poor audio player · Cluttered layout |
| Dating App | Generic profiles · No safety features visible |
| News / Media | Cluttered layout · Slow loading |
| Food Delivery | Muted colors · Low energy |
| Fitness / Gym | Static design · No gamification |

**"AI purple/pink gradients"** — the gradient style from AI branding (purple→pink mesh) is now associated with generic AI products. Avoid it in finance, healthcare, legal, government, and enterprise contexts where it signals "not serious."

---

## Output Format

Emit this block after routing:

```
╔══════════════════════════════════════╗
║         DESIGN ROUTE                 ║
╚══════════════════════════════════════╝
Brief:    [one-line brief summary]
Platform: [web / mobile / print / unknown]

Step 1 → color-combo-skill
  Category:  [category name]
  Palette:   [palette name, or "agent selects"]
  Note:      [carryover note for next skill]

Step 2 → design-effects-skill
  Focus:     [effect family or "flat"]
  Suppress:  [what to avoid]
  Note:      [carryover note for next skill]

Step 3 → font-pairing-skill
  Archetype: [pairing archetype name]
  Priority:  [display / body / mono emphasis]
  Note:      [carryover note for next skill]

Step 4 → icon-system-skill   [or: SKIP — reason]
  Library:   [preferred library]
  Weight:    [stroke px or filled]
  Style:     [animated / static]

Confidence: [HIGH / MEDIUM / LOW — how well signals matched]
Adjustments: [anything ambiguous that the user should confirm]
```

Then emit this pre-delivery checklist:

```
PRE-DELIVERY:
  [ ] SVG icons only — no emojis as icons (use Heroicons/Lucide)
  [ ] cursor-pointer on all clickable elements
  [ ] Hover states: 150–300ms transition
  [ ] Text contrast ≥4.5:1 minimum (WCAG AA)
  [ ] Focus states visible for keyboard nav
  [ ] prefers-reduced-motion respected
  [ ] Responsive: 375px / 768px / 1024px / 1440px
  [ ] No AI purple/pink gradients in finance, healthcare, legal, or government contexts
```

---

## Example Runs

### Example 1: B2B logistics dashboard

**Brief:** "We need a dashboard for our logistics operations team — tracking shipments, delays, driver status. B2B product, used daily."

```
╔══════════════════════════════════════╗
║         DESIGN ROUTE                 ║
╚══════════════════════════════════════╝
Brief:    B2B logistics ops dashboard — shipments, delays, driver status
Platform: web app

Step 1 → color-combo-skill
  Category:  Corporate
  Palette:   Ops Green or Slate Command
  Note:      Dark accent preferred; real-time status needs distinct alert colors (red/amber/green)

Step 2 → design-effects-skill
  Focus:     flat, data-dense layout, subtle row elevation
  Suppress:  no glass, no heavy animation, no gradients in data cells
  Note:      Flat palette → stroke-only icons at consistent weight

Step 3 → font-pairing-skill
  Archetype: humanist sans + tabular mono for numerics
  Priority:  body (data legibility first)
  Note:      Tabular nums required for shipment counts and timestamps

Step 4 → icon-system-skill
  Library:   Heroicons or Lucide
  Weight:    stroke 1.5–2px
  Style:     static

Confidence: HIGH
Adjustments: Confirm whether dark mode is required for ops environments (night shift use case)
```

---

### Example 2: Boutique gin distillery

**Brief:** "Branding and website for a small-batch gin distillery. Very craft, botanical, a little dark and mysterious."

```
╔══════════════════════════════════════╗
║         DESIGN ROUTE                 ║
╚══════════════════════════════════════╝
Brief:    Small-batch gin distillery — craft, botanical, dark/mysterious
Platform: web (marketing site)

Step 1 → color-combo-skill
  Category:  Rustic / Gothic hybrid
  Palette:   Smoked Oak OR Bone & Wine
  Note:      Dark background with botanical accent (deep green or aged gold); warm shadows forward

Step 2 → design-effects-skill
  Focus:     hero gradient, textured overlays, warm shadow elevation
  Suppress:  no cold glass, no neon glow, no flat corporate layout
  Note:      Dark palette → glass morphism optional on hero only; prefer texture

Step 3 → font-pairing-skill
  Archetype: editorial serif display + humanist body
  Priority:  display (brand identity weight)
  Note:      Slab or transitional serif for headings; legible humanist for body copy

Step 4 → icon-system-skill
  Library:   hand-drawn stroke set or Phosphor (thin weight)
  Weight:    stroke 1.5px
  Style:     static

Confidence: HIGH
Adjustments: Confirm if e-commerce (bottle shop) is in scope — would add card layout requirements
```

---

### Example 3: Gaming peripheral brand

**Brief:** "Website for a gaming peripherals brand — keyboards, mice, headsets. Target audience: competitive PC gamers."

```
╔══════════════════════════════════════╗
║         DESIGN ROUTE                 ║
╚══════════════════════════════════════╝
Brief:    Gaming peripheral brand website — keyboards, mice, headsets; competitive PC audience
Platform: web (product/marketing site)

Step 1 → color-combo-skill
  Category:  Gaming
  Palette:   Cyber Arena or Shadow Protocol
  Note:      Dark OLED base; neon accent (cyan or electric lime); RGB-suggest color roles

Step 2 → design-effects-skill
  Focus:     glass morphism on product cards, neon glow on CTA, scroll-driven motion
  Suppress:  no warm shadows, no soft pastels, no flat corporate layout
  Note:      Animated effects active → animated icons or Lottie for key interactive moments

Step 3 → font-pairing-skill
  Archetype: geometric display + geometric sans body
  Priority:  display (product names, hero headlines)
  Note:      Avoid humanist; geometric or condensed display only

Step 4 → icon-system-skill
  Library:   Lordicon or Lucide (dark-optimized)
  Weight:    filled, bold stroke (2px+)
  Style:     animated on hover for hero icons

Confidence: HIGH
Adjustments: Confirm whether product configurator (RGB customizer) is in scope — affects motion budget
```

---

## Anti-Slop Gate

**Always apply `design-anti-slop` as the final step of every design route.**

After the skill chain (color → effects → fonts → icons) produces output, check it
against the 7 cardinal sins before delivering. This is not optional — it is the
quality gate that separates a designed artifact from a generated template.

Load: `design-anti-slop` skill.  
Run: the 10-item checklist at the bottom of that file.  
Block: any P0 violation (indigo default, trust gradient, emoji icons, AI dashboard tile,
invented metrics, filler copy, wrong display font).

---

## Maintained by

[@bilioveloso](https://github.com/bilioveloso) — part of the modular design skill system.

**System repos:**
- [color-combo-skill](https://github.com/bilioveloso/color-combo-skill)
- [design-effects-skill](https://github.com/bilioveloso/design-effects-skill)
- [font-pairing-skill](https://github.com/bilioveloso/font-pairing-skill)
- [icon-system-skill](https://github.com/bilioveloso/icon-system-skill)
