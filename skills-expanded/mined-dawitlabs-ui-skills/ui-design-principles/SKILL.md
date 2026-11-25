# UI Design Principles — Everyday Knowledge Base

This skill is Dawit's living UI/UX knowledge base. It contains distilled principles from articles and blogs he has studied. Apply this knowledge automatically when working on any UI, component, color system, or typography task.

---

## COLOR — Variations & Modifications
*Source: learnui.design — Color in UI Design: A Practical Framework*

### The one rule that matters
**Darker = lower brightness + higher saturation**
**Lighter = higher brightness + lower saturation**

Never just darken or lighten. Always move both values together. This mirrors how shadows work in nature and feels instinctively correct to the human eye.

### The hue shift trick
On top of brightness/saturation, shift hue slightly:
- **Darker → shift hue toward luminosity minimums: Red (0°), Green (120°), Blue (240°)**
- **Lighter → shift hue toward luminosity maximums: Yellow (60°), Cyan (180°), Magenta (300°)**

In OKLCH: darker = lower L + higher C + hue toward 0°/120°/240°. Lighter = higher L + lower C + hue toward 60°/180°/300°.

### Practical applications
- Button hover → darker variation (lower L, higher C)
- Button disabled → lighter variation (higher L, lower C)
- Surfaces/backgrounds → same hue, near-zero chroma (~0.005–0.01), not pure neutral gray
- Borders → mid-dark variation of base color
- Don't pick multiple colors — derive everything from one base

### Use HSB/OKLCH not hex
HSB maps directly to what you're doing. In OKLCH: L = lightness, C = chroma (saturation), H = hue.

---

## COLOR — Psychology & Meaning
*Source: UX Magazine — The Psychology of Color in UI/UX Design*

### Color meanings (Western context)
| Color | Communicates | Use for |
|-------|-------------|---------|
| Red | Urgency, excitement, passion | CTAs, alerts, errors |
| Blue | Trust, calm, reliability | Finance, auth, info |
| Green | Safety, growth, success | Success states, health |
| Yellow | Warmth, optimism, energy | Warnings, welcoming |
| Black | Luxury, elegance, premium | High-end branding |
| White | Clarity, simplicity, space | Minimal UI, breathing room |

### Cultural context
- Red = danger in West → luck/celebration in Chinese culture
- Never assume color meaning is universal

### The 60-30-10 rule
- **60%** — dominant (backgrounds, main surfaces)
- **30%** — secondary (cards, sidebars, contrast areas)
- **10%** — accent (CTAs, highlights, key interactions)

### Accessibility
- ~8% of men are color blind
- Red/green and blue/purple are the worst combos
- Never use color as the ONLY signal — always pair with icons, labels, or patterns
- Check contrast ratios against WCAG AA (4.5:1 for normal text, 3:1 for large text)

---

## TYPOGRAPHY
*Source: Supercharge Design — Typography in UX/UI: A Complete Guide*

### Core elements
- **Typeface** = the family (Inter). **Font** = one weight (Inter 600)
- **Tracking** = spacing across all characters in a block
- **Kerning** = spacing between two specific characters
- **Hierarchy** = size + weight + style differences that guide the eye
- **White space** = empty space around text — more = more premium

### Rules
- Max **2 typefaces** per product — more = chaos
- Match typography to demographic (children = bigger, playful)
- Test across iOS, Android, Web — fonts render differently
- Keep copy short and clear

### Type scale baseline
| Role | Size | Weight |
|------|------|--------|
| Hero headline | 48–72px | 700–800 |
| Section heading | 28–36px | 600–700 |
| Card title | 18–22px | 600 |
| Body | 15–16px | 400 |
| Small/label | 12–13px | 500 |
| Code | 13px | mono |

### Hierarchy signals
1. Size (most powerful)
2. Weight (bold vs regular)
3. Color (primary vs muted)
4. Spacing (more space = more important)
5. Case (ALL CAPS for labels/tags)

---

## TYPOGRAPHY — The Power of Type in UI
*Source: Medium/@nasir-ahmed03 — Typography in UX/UI: A Complete Guide — The Absolute Power*

### The 7 powers of typography
1. **Readability & accessibility** — good type makes content effortless to find and consume
2. **Tone and mood** — cartoon font + warm colors = fun. Plain simple font = serious/professional
3. **Differentiation** — typography is what makes apps memorable and recognizable
4. **Boosts sales** — longer engagement, less distraction, faster information discovery
5. **Communication** — guides attention, conveys meaning, creates intuitive interfaces
6. **Visual hierarchy** — font size/style/color tells users what to read first and what to do next
7. **Brand identity** — bold/modern = tech. Sophisticated serif = luxury. Type IS the brand voice

### Brand personality through type
- **Technology brands** → bold, geometric, modern sans-serif
- **Luxury brands** → sophisticated serif (think editorial magazines)
- **Playful/consumer** → rounded, soft, warm typefaces
- **Serious/finance** → plain, clean, minimal

### Hierarchy done right
"Well-structured hierarchy means the job of conveying the message is half done."
- Headers: larger + bolder
- Subheaders: medium size + medium weight
- Body: comfortable reading size + regular weight
- Labels/captions: smaller + often uppercase or muted color
- The eye should flow naturally without effort

### Consistency is non-negotiable
- Same typeface family for same element type everywhere
- Same weight for same hierarchy level everywhere
- No random font switching — if it looks different it must mean something

### Color in typography
- Balance text color with background AND surrounding graphics
- Don't just check contrast — check harmony with the full palette
- Excessive color contrast experimentation = lower readability
- Subtle color shifts (muted vs primary text) create hierarchy without size changes

### White space as a power tool
- More white space = more premium, more breathing room, more focus
- Increase white space to draw attention to essential sections
- Margins are the foundation — logos, headers, body must all align to them

---

## TYPOGRAPHY — Choosing the Right Typeface
*Source: Designlab — What is Typography & How is it Important to UX/UI Design*

### The 4 functions of typography in UI
1. **Captures attention** — the right typeface draws users in before they read a word
2. **Influences behavior** — bad fonts cause abandonment; good fonts create longer engagement
3. **Supports brand recognition** — typeface + logo together build subliminal brand association
4. **Creates visual hierarchy** — directs time-poor users to what matters most instantly

### 5 questions to ask when choosing a typeface
1. **Brand identity** — is this brand serious/hard-hitting or fun/creative? Pick a typeface that answers that
2. **Tone** — informal fonts suit relaxed cultures; wrong for serious organizations
3. **Legibility** — decorative fonts look impressive but fail in body text; users abandon it
4. **Consistency** — switching fonts between pages creates confusion and breaks trust
5. **SEO** — choose browser-friendly fonts so search engines can crawl and index the text

### Typeface categories
- **Serif** — traditional, trustworthy, editorial, luxury
- **Sans-serif** — modern, clean, digital-first, tech
- **Decorative** — personality-driven, use sparingly (headlines only, never body)

### White space is an active design element, not emptiness
- Small spacing adjustments have dramatic impact on legibility
- White space signals quality — cramped = low-end, spacious = premium
- Margins, padding, and line spacing all control it

### Typography is structural, not just aesthetic
- It's not decoration — it's the skeleton of how information is organized
- Language + typography work together to create impressions
- How type works with OTHER design elements (color, layout, imagery) matters as much as the type itself

### The SEO angle (unique to this source)
- Browser-unfriendly fonts block search engine indexing
- Always use web-safe or properly loaded web fonts (Google Fonts, system fonts, or self-hosted)
- For ParticleUI: use `font-display: swap` to avoid invisible text during load

---

---

## TYPOGRAPHY — Emotions Behind Typefaces
*Source: UX Planet — UI Design: Typography and Emotions Behind It*

### The core design philosophy
"You either design for your users or you create for yourself. There is nothing in between."

Every typeface choice is an emotional choice. Users feel the font before they read the words.

### Typeface → emotion map
| Typeface | Emotion / Personality |
|----------|----------------------|
| Patrick Hand | Friendly, helpful, handwritten warmth |
| Bebas Neue | Bold, strong, confident — great for headlines |
| ABeeZee | Educational, open, welcoming — learning contexts |
| McLaren | Fun, bouncy, comic — approachable for all ages |
| Cinzel Decorative | Heritage, classical, Roman — premium/legacy brands |
| Cabin Sketch | Teenage, sketchy, modern humanist |
| Creepster | Frightening, grisly — Halloween/horror only |
| Wallpoet | Graffiti, stencil, political, street culture |
| Stint Ultra Condensed | Information-dense, compact — data-heavy UIs |
| Delius Swash Caps | Comic marker style — titles, logos, illustration |

### The mismatched font problem
"You can't use a Creepster typeface in a child-friendly website and expect users to use it."
- Wrong typeface = emotional disconnect = users leave
- The font must match the product's purpose AND the user's expectations
- Test your typeface against real-world context, not just in isolation

### Practical rules
- Use Google Fonts for free, legal, web-safe typefaces
- Never use pirated premium fonts for commercial products
- Always test by applying the font to an actual page — not just a style preview
- The best way to judge a font: put it on the real UI and feel what it communicates

---

---

## UI — 7 Rules for Creating Gorgeous UI (Part 1)
*Source: learnui.design/blog — 7 Rules for Creating Gorgeous UI*

### Rule 1: Light comes from the sky
- Shadows are cast downward — top surfaces catch light, bottom surfaces are shaded
- **Inset elements** (inputs, pressed buttons, wells): top edge is dark, bottom edge is lighter (light can't reach the top, bounces up from bottom)
- **Raised elements** (cards, buttons): top edge is lighter, bottom edge is darker
- Apply to: borders, box-shadows, background gradients on elements

### Rule 2: Black & white first
- Design in grayscale before adding color — forces you to solve contrast and hierarchy correctly
- Color is an enhancement, not a crutch for hierarchy
- If it looks bad in black & white, color won't fix it
- After grayscale works: add color sparingly, only to guide attention

### Rule 3: Double your whitespace
- Every element needs more breathing room than feels comfortable
- **Practical starting values**: if font-size is 12px, padding is at least 12px; space between groups ~25px
- Whitespace between unrelated groups must be visually larger than whitespace within a group
- When in doubt: add more. The common mistake is too little, never too much.
- Margins and padding are the foundation — every element must align to them

---

## UI — 7 Rules for Creating Gorgeous UI (Part 2)
*Source: learnui.design/blog — 7 Rules for Creating Gorgeous UI (Part 2)*

### Rule 4: Learn the methods for text on images
Four techniques — use them, don't just slap text over a photo:
1. **Overlay** — add a dark (or colored) overlay on the image, then put text on top. Simple and reliable.
2. **Text in a box** — put the text in a semi-opaque box. Works when the image is busy.
3. **Blur** — blur the background behind the text. Blurred area creates visual separation.
4. **Floor fade** — gradient from transparent at top to dark at bottom, text sits at the bottom. Classic hero pattern.
5. **Scrim** — subtle diagonal or radial gradient, softer than floor fade

### Rule 5: Make text pop — and unpop
Two dimensions for text emphasis:
- **Size** — larger = more important
- **Color** — darker/more saturated = foreground; lighter/more muted = background
- Use both together: hero text = large + dark. Captions = small + muted. Don't use large + muted or small + dark.
- "Unpopping" text (making it less prominent) is as important as popping it — most designers only know how to make things stand out

### Rule 6: Only use good fonts
Recommended for clean modern UI:
- **Satoshi** — modern geometric, great for headings + body
- **Metropolis** — geometric sans, strong hierarchy
- **Source Sans** — humanist sans, excellent legibility at body sizes
- **Figtree** — friendly, geometric, all-purpose
- Avoid: novelty fonts in body text, fonts with inconsistent weights
- Use Google Fonts or self-hosted; always set `font-display: swap`

### Rule 7: Steal like an artist
Learn by cloning excellent work:
- **Dribbble** — find UI inspiration, identify design patterns
- **Layers.to** — curated product screenshots
- **Mobbin** — mobile and web UI library, searchable by element type
- Process: find something great → ask "why does this work?" → extract the principle → apply it yourself

---

## UX — 4 Rules for Intuitive UX
*Source: learnui.design/blog — 4 Rules for Intuitive UX*

### Rule 1: Law of locality
- Controls must be near the thing they affect. Users look next to an object for its controls, not across the screen.
- **Bad**: settings gear icon in the top nav when it controls a card
- **Good**: edit icon inline with the element it edits
- Applies to: delete buttons, edit controls, toggles, filter selectors — all should be spatially adjacent to the content they control

### Rule 2: ABD — Anything But Dropdowns
Dropdowns are the worst UX control for most use cases. Replace them:
| Situation | Replace dropdown with |
|-----------|----------------------|
| 2–4 options | Radio buttons or segmented control |
| Toggle | Toggle switch |
| Date | Date picker |
| Multiple select | Checkbox list |
| Search + select | Autocomplete input |
- Dropdowns are acceptable only when: options > ~7, or options are very dynamic, or space is severely constrained

### Rule 3: Squint test (MIT — Most Important Thing)
- Squint your eyes until the screen blurs — what do you see first?
- That blurry focal point = your MIT (most important thing)
- If the wrong thing is the MIT, fix the hierarchy: increase contrast, size, or color weight of the real priority
- Every screen must have exactly one MIT. If everything shouts, nothing is heard.

### Rule 4: Teach by example, not by explanation
- Don't explain with text when you can show with a placeholder or example
- Placeholder text in inputs should show a real example, not just the label (`john@example.com` not `Email`)
- Empty states should show what a filled state looks like
- Onboarding should demonstrate, not just describe
- "Show, don't tell" — the user's mental model comes from seeing, not reading

---

## UI — Font Sizes in UI Design
*Source: learnui.design/blog — Font Sizes in UI Design*

### The baseline scale
Never go below 12px for any readable text. Practical scale:
| Context | Min size | Comfortable size |
|---------|----------|-----------------|
| Body text | 15px | 16–18px |
| Secondary/supporting | 13px | 14px |
| Labels/captions | 11px | 12–13px |
| Navigation | 14px | 15–16px |
| Headings | 20px | 24–48px depending on level |

### Line height matters as much as size
- Body text: line-height 1.4–1.6× the font size
- Headings: line-height 1.1–1.25 (tighter than body — they don't have multi-line rhythm problems)
- Captions/labels: line-height 1.3–1.4

### Hierarchy through size contrast
- The difference between heading and body must be immediately obvious — not just 2px apart
- Use ratios: H1 ~2.5× body, H2 ~1.75× body, H3 ~1.25× body
- Don't create 6 heading levels — most UIs only need H1, H2, and body

---

## COLOR — HSB Color System Deep Dive
*Source: learnui.design/blog — The HSB Color System: A Practitioner's Primer*

### HSB component definitions
- **Hue (0–360°)** — position on the color wheel. Red = 0°/360°, Green = 120°, Blue = 240°
- **Saturation (0–100%)** — 100% = richest color; 0% = gray. Amount of color injected into the gray.
- **Brightness (0–100%)** — 0% always = black regardless of H or S. 100% B + 0% S = white. 100% B + any S = very bright color.

### The tint/shade technique (critical)
- **Lighter (tint):** Decrease S + Increase B simultaneously → moves toward upper-left corner of color picker
- **Darker (shade):** Increase S + Decrease B simultaneously → produces rich dark shades ← **THIS is the right way**
- **Wrong approach:** Only decrease B → produces dull, muddy darker shades 95% of the time
- Key insight: "removing white" (decreasing B + increasing S) is correct. "Adding black" (only decreasing B) is wrong.

### Hue shifting for palette personality
- Blue (240°) → shift down 30° to 210° = lighter, more casual/fun (aqua/teal)
- Blue (240°) → shift up 20° to 260° = cooler, more premium (indigo)
- Red (0°) → shift down 10° = friendlier, pinker
- Rule: don't restrict palettes to kindergarten colors — hue shifting creates personality

### HSB vs. HSL
- CSS doesn't accept HSB — convert to hex/HSL/OKLCH for code
- HSB is the design tool for manipulation. Use it in Figma, design tools.

---

## COLOR — Data Visualization Palettes
*Source: learnui.design/blog — Picking Colors for Data Visualizations*

### Three palette types
1. **Multi-hue** — for categorical data (pie charts, multi-series line charts, maps)
2. **Single-hue** — for one numeric variable's magnitude (heat maps, choropleth)
3. **Divergent (two-hue)** — for transitions from one extreme → neutral → opposite extreme

### Multi-hue rules
- **Visual equidistance is mandatory** — any two adjacent palette colors must appear equally different to the eye
- Span both warm and cool hues across dark and light values
- Use HCL color space (not RGB or HSB) — it models human perception, not computer rendering
- Bad palettes: two colors too similar → users can't distinguish categories

### Divergent scale rules
- Structure: color A → neutral midpoint → color B
- Neutral midpoint: bright + low saturation
- **Hue angle rule:** if endpoint hues are ≤120° apart, use the hue between them as neutral (e.g., green 120° + red 0° → yellow 60° as neutral)
- If endpoints >120° apart: flat gray works as neutral
- Both halves must be visually equidistant from the midpoint

---

## UI — Shadows, Borders, Typography Deep Dive
*Source: learnui.design/blog — The King vs. Pawn Game of UI Design*

### Shadows: two types
- **Photorealistic** — behave like real-world light sources
- **Cartoon/idealized** — show elevation without full realism

### Shadow CSS values (specific)
- Light button on light background: `0 1px 2px rgba(0,0,0,0.30)`
- Dark/bold button: `0 2px 4px rgba(0,0,0,0.50)`
- Dark background context: `0 2px 3px rgba(0,0,0,0.40)` (vs 0.20 on light backgrounds)

### Shadow luminosity rule
- Higher luminosity background → lower shadow opacity needed
- Lower luminosity background → higher shadow opacity needed
- Test: convert button to grayscale — diagnose whether shadow darkness is matched to background
- Alternative to drop shadow: **30% black opacity border on bottom edge only** = softer depth effect

### Border opacity calibration
- 20% black opacity → visible on high-luminosity (light/teal) backgrounds
- 50% black opacity → needed on lower-luminosity (standard blue) backgrounds

### Typography: font-shape pairing
- Rounded fonts → rounded border-radius (e.g. Satoshi → 6–8px radius)
- Squared/geometric fonts → sharp corners (0px radius)
- **Uppercase letter-spacing rule:** always add letter-spacing to uppercase text — fonts designed for sentence case appear cramped in all-caps
- Source Sans: apply **−1% letter-spacing** on heavier weights/titles

### Icon drawing consistency
- Match icon stroke weight to text weight
- Apply same corner radius to icons as the typeface uses
- Icons should appear "drawn with the same pen" as the typeface
- Avoid thick bubbly icon sets for precise/minimal UIs

### Base button specs (starting reference)
- Height: 40px | Horizontal padding: 20px each side | Font size: 16px
- iOS tap target minimum: 44×44pt | Android: 48×48dp

---

## UX — The 3 Laws of Locality (Extended)
*Source: learnui.design/blog — The 3 Laws of Locality*

### Law 1: Put controls where they effect change
- Actions appear on or directly adjacent to the specific object they modify
- Use hover states to keep clean — reveal actions only on hover for list items
- Example: delete/edit buttons on individual email threads, not in a distant toolbar

### Law 2: Controls affecting an entire area go above that area
- Recursive: areas nest within areas; app-wide controls sit higher than page-wide controls
- Group-level controls → top of the group. Page-level controls → top of page. App-level → app bar.

### Law 3: Farther control = more visual pop
- If a control must be displaced (e.g., floating action button for thumb reach on mobile), compensate with extra visual prominence
- iOS upper-right primary action button violates this: user filled form at center-bottom, must reach all the way to top-right

---

## UI — Alignment
*Source: learnui.design/blog — 3 Pro Tips on Alignment*

### Core insight
Alignment is the single highest-ROI cleanliness technique. Sloppy-looking designs almost always have alignment problems.

### 3 rules
1. **Left-aligned text has a strong left edge, weak right edge** — don't assume left-alignment is solving your problem; trace where your invisible alignment lines actually fall
2. **Centering is valid alignment** — vertical or horizontal centering between two elements is a legitimate deliberate choice, not laziness
3. **Hanging alignment** — punctuation, icons, bullets, and decorative shapes with less visual weight should hang *outside* the main alignment grid to keep strong text edges clean (used in print typography since Gutenberg)

---

## UI — Animation & Transition Timing
*Source: learnui.design + NN/g standards*

### Timing values
| Animation type | Duration |
|---------------|---------|
| Simple feedback (checkbox, toggle) | ~100ms |
| Hover state transitions | 100–250ms |
| Modals / substantial changes | 200–300ms |
| Large screen transitions | up to 400ms |
| Annoyance threshold | 500ms+ (avoid) |
| Dropdown open | 200–300ms |
| Tooltip appear | ~125ms |

### Easing rules
- **Entering elements:** ease-out (decelerates into position)
- **Exiting elements:** ease-in (accelerates away)
- Entry slightly slower than exit (e.g., open 300ms / close 200–250ms)
- Button press scale: 0.97 (subtle physical feel)

### Performance rule
- Only animate `transform` and `opacity` — GPU composited, no layout recalculation
- Never animate `width`, `height`, `padding`, `margin` — causes layout thrash
- Always implement `prefers-reduced-motion` media query

---

## UI — Font Sizes Reference
*Source: learnui.design/blog — Ultimate Guide to Font Sizes in UI Design*

### Platform units
- **iOS/macOS:** points (pt) — "the number you type in design software"
- **Android layout:** dp (density-independent pixels)
- **Android fonts:** sp (scaleable pixels, respects user accessibility setting)
- **Web:** CSS px (CSS pixels, not device pixels)
- **Critical:** Always design at @1x — guidelines only apply at 1x scale

### Minimum sizes (never go below these)
| Context | Min | Comfortable |
|---------|-----|-------------|
| Body text | 15px | 16–18px |
| Secondary/supporting | 13px | 14px |
| Labels/captions | 11px | 12–13px |
| Navigation | 14px | 15–16px |
| Small headings | 20px | 22–24px |
| Large headings | 28px | 32–48px |

### Line height
- Body: 1.4–1.6× font size
- Headings: 1.1–1.25 (tighter)
- Captions/labels: 1.3–1.4

### Hierarchy ratios (use contrast, not just 2px differences)
- H1 ≈ 2.5× body | H2 ≈ 1.75× body | H3 ≈ 1.25× body
- Most UIs need 3 heading levels maximum

---

---

## UX — Signup & Login UX Patterns
*Source: learnui.design/blog — 15 Tips for Better Signup/Login UX*

Core rule: **Remove interaction. Remove clicks, remove reading, remove waiting, remove thinking.**

### Specific rules
- **Autofocus** the first input field — eliminates the extra tap/click to begin
- **Specialized keyboards** — use `type=email`, `type=tel`, `type=number` for mobile keyboard correctness
- **Validate on blur** (when leaving a field), never only on submit
- **Make labels clickable** — wrap inputs in `<label>` or use `aria-labelledby`
- **Show password requirements only while creating** — hide them once the field is valid
- **Password visibility toggle** — better than confirm-password field
- **Descriptive button text** — "Start My Free Trial" not "Continue"
- **SSO options** — offer Google login unless there's a specific reason not to
- **Magic links** — set validity to **30–60 minutes**
- **ToS notification** — notify on signup rather than requiring a checkbox (where legally permitted; EU requires explicit consent)
- **Distinct terminology** — "Register" vs. "Sign In" (differ by more than 2 letters; never "Sign Up" vs. "Sign In")
- **Link to toggle** — always provide sign-in ↔ register switch at the bottom of the form
- **Email over username** — users remember email, not usernames
- **Specific error messages** — "Password must be at least 8 characters" not "Incorrect password"
- **Retain typed values** after failed login — do not clear email field
- **Pre-fill email** on reset-password screen if the user already entered it within ~30 seconds

---

## UI — Visual Spice Techniques
*Source: learnui.design/blog — 37 Ways to Spice Up Your UI Designs*

"Pro-level designs = solid foundations + a few well-chosen techniques"

### Background techniques
- **Angled transitions** — diagonal instead of horizontal = more dynamic
- **Curved transitions** — suit soft/organic design systems
- **Tilted highlight shape** — colored shape behind element, slightly rotated; gradient fills amplify effect
- **Background highlight shape** — geometric shape behind a card/section to distinguish without a border
- **Subtle patterns** — low-contrast repeating texture that doesn't distract
- **XL background text** — large, low-contrast words behind content (size and contrast trade off)

### Border techniques
- **Dotted borders** — lighter, more textured than solid; dotted dividers suggest connection not separation
- **Double borders** — add an extra white ring for emphasis
- **Gradient borders** — vibrant gradient signals excitement/importance
- **Bevelled borders** — mimics light catching a metal edge
- **Fading borders** — duplicate border at increasing sizes + decreasing opacity = depth/pulse effect
- **Thick transparent borders** — structure without visual weight

### Shadow techniques
- **Floating shadow** — shadow below and separated from element (appears to hover)
- **Solid shadow** — offset unblurred shape matching container (cartoon depth)
- **Outline shadow** — offset outline as shadow substitute
- **Pattern shadow** — textured shadow grabs attention while highlighting

### Typography techniques
- **Layered text** — interweave type with imagery; best for large titles
- **Inline imagery** — icons/illustrations embedded within a sentence
- **Thick underlines** — substantial underlines in brand color (not the thin default)
- **Font-change emphasis** — switch typeface or italicize specific words for editorial character
- **Width variation** — condensed or extended variants for emphasis beyond bold/italic

### Structural techniques
- **Break the frame** — content spills beyond container edges = energy/playfulness
- **Offset background** — border or background separated from element edge by a gap
- **Pocket cut-off** — images cropped at edge to imply they continue behind
- **Repeated shapes at decreasing sizes** — creates illusion of distance

---

## TYPOGRAPHY — Font Pairing
*Source: learnui.design/blog — The Step-by-Step Guide for Pairing Fonts*

### Core rules
- 95% of good font pairings: **one serif + one sans-serif**
- Max 2 typefaces (except highly stylized editorial work)
- Body font criteria: high x-height, open counters, never calls attention to itself

### 6-step pairing process
1. Determine brand identity (adjectives: clean, classy, friendly, quirky, techie)
2. Brainstorm fonts matching brand subtly
3. Select body font for legibility
4. Add secondary font to fill brand gaps
5. Define per-font usage rules (headings, labels, body, nav, forms, footer)
6. Repeat steps 4–5 until system is complete

### Brand-to-font mapping
| Brand personality | Typeface direction |
|------------------|--------------------|
| Clean/Simple | Geometric sans, neutral |
| Classy/Luxury | High-contrast serif (Didone) |
| Friendly | Rounded humanist sans |
| Quirky | Distinct personality font (headlines only) |
| Techie | Bold geometric sans |

---

## UI/UX — Key Reference Numbers
*Source: learnui.design/blog — 100 Things a UX/UI Designer Should Know*

### Typography numbers
| Value | Rule |
|-------|------|
| 50–75 chars | Optimal body text line length |
| <3 lines | Only time to center-align text |
| 16px | Web + Material Design default body size |
| 17pt | iOS default body size |
| 1.4–1.6× | Line height multiplier for body text |
| 1.1–1.25× | Line height multiplier for headings |
| −1% | Letter spacing for Source Sans on heavier weights |

### Touch targets
| Platform | Minimum |
|----------|---------|
| iOS | 44×44pt |
| Android | 48×48dp |
| Most common iPhone width | 375pt |
| Most common Android width | 360pt |

### Timing
| Interaction | Duration |
|-------------|---------|
| Hover state | 100–250ms |
| Modals / screen transitions | 200–300ms |
| Annoyance threshold | 500ms+ |

### Layout
| Context | Value |
|---------|-------|
| Desktop main content width | ~620px reference |
| Nav bar: text/icon height | ~20% of bar height |
| Menu item padding (12px font) | 12px per side |
| List title gap to underline | 15px |
| Gap between list groups | 25px |
| Standard button height | 40px |
| Standard button H padding | 20px per side |
| Standard button font size | 16px |

### Contrast (WCAG AA)
| Text size | Ratio |
|-----------|-------|
| Body text | 4.5:1 |
| Large text / headlines | 3:1 |

### Color
| Shadow context | Opacity |
|----------------|---------|
| Light background | ~20–30% black |
| Dark background | ~40–50% black |

### UX mental models (apply automatically)
- **Jakob's Law** — users prefer sites that work like sites they already know
- **Satisficing** — users take the first "good enough" option; bad design forces bad choices
- **Poisson distribution** — scheduling dates and small counts cluster near low values; design controls (steppers, calendars) to reflect this
- **80/20 rule** — 20% of pages = 80% of traffic; 20% of features = 80% of usage; prioritize accordingly
- **Zero price effect** — "free" generates dramatically more interest than even a tiny cost
- **Desire paths** — user-created workarounds reveal true mental models; study them

---

## HOW TO APPLY THIS KNOWLEDGE

When working on any UI task:

1. **Colors** — derive hover/active/disabled states by moving S+B in opposite directions (never just opacity)
2. **Tints/shades** — tint = decrease S + increase B. Shade = increase S + decrease B. Never just reduce brightness.
3. **Surfaces** — give neutral backgrounds a whisper of brand hue chroma (~0.005), never pure gray
4. **Palette** — follow 60-30-10: one dominant, one secondary, one accent
5. **Accessibility** — check contrast, never rely on color alone; WCAG AA = 4.5:1 (text), 3:1 (large)
6. **Type** — max 2 fonts, clear scale with ratio contrast (H1 ≈ 2.5× body), let hierarchy do the work
7. **White space** — double what feels right. Font-size-equivalent padding minimum. Treat space as default state.
8. **Brand voice** — match typeface to brand personality; match font shape to border-radius
9. **Consistency** — same element type looks identical everywhere
10. **Shadows** — light from sky: raised = lighter top, inset = darker top. Match shadow opacity to background luminosity.
11. **Controls** — place controls next to what they control (Law of Locality). ABD: replace dropdowns with segmented controls, toggles, steppers.
12. **Hierarchy** — squint test: one MIT per screen. Up-pop = large + dark + bold. Down-pop = small + muted.
13. **Text on images** — always use overlay (35% opacity), text-box, blur, or floor fade (0%→20% gradient)
14. **Alignment** — left text has strong left edge only. Center deliberately. Hang punctuation/icons outside the grid.
15. **Animation** — 100–300ms for most transitions. ease-out enter, ease-in exit. Only animate transform + opacity.
16. **Icons** — same stroke weight and corner radius as the typeface. Drawn with the same pen.
17. **Font sizes** — 16px body minimum for web. Never below 12px for any readable text. Line height 1.4–1.6× for body.

## SOURCES TO ADD MORE
When Dawit shares new blogs or articles, extract the principles and add them to this file under a new section. Keep growing this as a living knowledge base.
