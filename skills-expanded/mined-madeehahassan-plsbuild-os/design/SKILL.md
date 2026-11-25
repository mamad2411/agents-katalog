---
name: Design
description: Make UI and visual decisions. Use when choosing layouts, colors, fonts, components, onboarding flows, empty states, or any visual element in a product. Adapts to Claude Code, claude.ai, and Cowork.
---

# /design

Use this when making any visual decision. Layout, colors, fonts, components, onboarding flows, empty states, illustrations, spacing, animations.

When this skill is invoked, your job is to produce **specific, opinionated design that looks like a person made it** — not a template, not a SaaS default, not Material Design, not stock Tailwind.

---

## Which surface are you on?

**Claude Code**
Read the existing CSS, Tailwind config, and relevant components before suggesting anything. If a palette or type scale already exists, respect it. Write design changes directly to files after the user approves. Run the app and verify the result renders the way you described.

**claude.ai chat**
Ask the user to paste the relevant component or CSS. Return proposed changes as copy-ready code blocks. When giving a palette or type scale, include the hex codes and CSS variable names ready to paste.

**Cowork**
Same as Code — read workspace files first, write back after approval. Don't silently overwrite existing design tokens; surface any conflicts with the user's design taste and ask before changing them.

---

## Before you design — ask 1–2 clarifying questions

Before producing any design, stop and ask **one or two** focused clarifying questions. Not five. Not a requirements doc. Just enough to know which direction to commit to.

Pick whichever questions apply to what's missing. If the user's profile already answers one, skip it. Ask in plain language, not as a form:

- *"What's the feeling you want? Three adjectives."*
- *"What's closest to the vibe — jam.dev, Notion, Linear, Stripe, Arc, or Things 3?"*
- *"Is this a full page, a single component, or a flow? Desktop, mobile, or both?"*
- *"Is there an existing palette or brand to stay inside, or are we starting fresh?"*
- *"What's the one action you most want someone to take on this?"*

Ask at most two at a time. If the user gave you enough in the original request, skip this step entirely and go straight to designing.

Do NOT ask:
- Implementation questions ("should I use Tailwind or plain CSS?") — make the call.
- Platform questions ("should it be responsive?") — yes, always, don't ask.
- Open-ended questions ("what do you want?") — that's the user's job to frame, not yours to interrogate.

Once you have the answers, commit. Don't keep asking. Make a decision and implement it.

---

## Fill this in once (add to your profile)

```
My design taste in 3 words: [e.g. "warm, playful, confident"]
Products I love the look of: [e.g. "jam.dev, Notion, Linear, Stripe, Arc, Things 3"]
Products I hate the look of: [e.g. "legacy SaaS, generic dashboards, gradient-heavy landing pages, Material Design admin panels"]
Light or dark mode: [e.g. "light (cream)" or "dark (warm ink, never charcoal)" or "hybrid (cream with dark-warm accent sections, like jam.dev)"]
My brand colors (if decided): [hex codes + names, or "TBD"]
My fonts (if decided): [serif + sans pair + optional display font, or "TBD"]
```

---

## The anti-default rule

The point of this skill is to **avoid the default**. The default is what Claude (or any AI, or any generic Tailwind starter) produces without a strong design voice: blue primary, gray cards, centered hero, stock shadows, Material Design-ish. It's fine. It's forgettable.

Before producing any design, ask: *"Would this look like it could belong to any SaaS product?"* If yes, start over with more specific choices.

---

## Principles (load-bearing, not decorative)

**Warm over cold.**
Backgrounds are cream or warm off-white, never pure white. Never pure black either — use a deep warm brown or ink, not `#000`. Think paper, not screen.

**Opinionated over generic.**
Every decision should feel chosen. If it could be anything, it's wrong. Pick a specific emotion and commit.

**Alive over static.**
Transitions 200–300ms. Things fade or slide in on scroll. Loading states have personality (not a plain spinner — a pulsing dot, a skeleton that matches the real layout, a short phrase).

**Confident over cluttered.**
One CTA per screen. Generous vertical whitespace (5rem+ between sections). One idea per section. If two things compete for attention, the page is wrong.

**Playful, not silly.**
Personality lives in the details. A badge with unusual letterspacing. An icon in a softly tinted square. A button that says "Run it" instead of "Submit." An empty state that makes the user smile. Not emoji explosions. Not comic sans.

**Tactile where it counts.**
Interactive elements can have a hard drop shadow (`0 4px 0 var(--dark)`) to feel stamp-like and clickable. Default cards use soft shadows (`0 20px 60px rgba(0, 0, 0, 0.08)`).

---

## Concrete defaults (use these unless the user's profile overrides)

### Palette — light mode (default)

```css
--cream: #F8F8F8;         /* primary background, never pure white */
--warm-white: #FFFFFF;    /* cards, modals, input fields */
--sand: #F2F2F2;          /* secondary background, dividers */
--yellow: #FFE48B;        /* playful accents, badges, highlights */
--yellow-soft: #FFF3C4;   /* callouts, soft backgrounds */
--mint: #C8F0DC;          /* positive actions, fresh accents */
--peach: #FFD9C8;         /* warm accents, alerts */
--dark: #1A1612;          /* primary text and buttons, never pure black */
--mid: #5C5C5C;           /* secondary text */
--light-text: #9E9E9E;    /* tertiary text, metadata */
--border: #E5E5E5;        /* subtle borders */
```

### Palette — dark mode (warm ink, NOT charcoal)

When the user's profile says dark mode, or the product context calls for it, use **warm dark** — not generic dark-UI charcoal. Think jam.dev's dark sections, or a warm espresso tone. Never pure black, never cool-gray.

```css
--bg: #1A1612;             /* primary background — deep warm ink */
--bg-card: #2A241F;        /* cards, elevated surfaces */
--bg-elevated: #35302A;    /* modals, dropdowns, highest layer */
--text: #F5EFE6;           /* primary text — warm off-white, NOT #FFF */
--text-mid: #B5ACA0;       /* secondary text — warm gray */
--text-dim: #7A7066;       /* tertiary text, metadata */
--border: rgba(245, 239, 230, 0.08);  /* subtle warm border */
--yellow: #FFE48B;         /* accents stay the same — pop against dark */
--yellow-soft: rgba(255, 228, 139, 0.15);  /* softened for dark bg */
--mint: #C8F0DC;
--mint-soft: rgba(200, 240, 220, 0.15);
--peach: #FFD9C8;
--peach-soft: rgba(255, 217, 200, 0.15);
```

**Dark mode rules:**
- Background is warm-ink (`#1A1612`), not charcoal (`#1E1E1E`) or true-dark (`#0A0A0A`).
- Cards are slightly lifted — `#2A241F` — so they look layered without needing heavy shadows.
- Text is warm off-white (`#F5EFE6`), never `#FFFFFF`. Pure white on dark backgrounds feels clinical.
- Accent colors (yellow, mint, peach) keep their hex. They pop beautifully against warm dark.
- Softened backgrounds for callouts use the accent hex with `0.15` alpha instead of the solid soft variant.

### Hybrid palette (cream main with dark-warm accent sections — jam.dev style)

Some of the best sites (jam.dev especially) use **light as the default** but punctuate with **warm dark sections** for emphasis — a "here's the serious part" or "here's the proof" moment. If the product's profile says "hybrid," alternate sections between cream and warm-dark-ink. Never abrupt — transitions should feel like turning a page.

Tune these to the product, but keep the warm/confident/playful shape. **Never use bright blue as a primary color.** Never use gray as the background of the whole page — cream, tinted white, or warm ink only.

### Typography

Pair a serif with a sans-serif. Not two serifs. Not two sans. Optionally add a **display font** for oversized numbers and hero stats so they feel editorial instead of dashboard-y.

- **Headlines:** Lora (Google Fonts) — weight 500, letter-spacing -0.01em to -0.015em. Line-height 1.1. *Lora has personality but leans "thoughtful essay" — if you want less serious, swap to **Fraunces** (rounder, more playful) or **DM Serif Display** (bolder, stamp-like).*
- **Body:** DM Sans (Google Fonts) — weight 400, line-height 1.55. 16px minimum.
- **Display (large numbers, stats, hero moments):** **Fraunces** at weight 600 with `font-variation-settings: 'SOFT' 100, 'WONK' 1` for extra character — or **DM Serif Display** for a cleaner but still confident look. Reserve for big display moments only. Lora is too restrained for a "21" that should feel celebratory.
- **Code / monospace:** Menlo or SF Mono, 0.78rem, background `var(--sand)` (light) or `rgba(255,255,255,0.06)` (dark), 4px border-radius.

Max three hierarchy levels: headline, subhead, body. Anything more is clutter.

**When to use the display font:** Hero numbers on dashboards ("21 best streak"), giant percentages, anything meant to make the user feel a win. Don't use it for UI labels or body — it'll feel carnival.

### Component patterns

**Cards.**
- Background: `var(--warm-white)`
- Border: 1px solid `var(--border)`
- Border-radius: 14–20px (20 for hero cards, 14 for inline)
- Padding: 2–3rem for major cards, 1.2rem for inline
- Shadow (default): `0 20px 60px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04)`
- Shadow (interactive/tactile): `0 4px 0 var(--dark)` — use sparingly for playful elements

**Buttons.**
- Primary: `var(--dark)` background, `var(--cream)` text, 10px border-radius (not rounded pill), 14px vertical padding, 22px horizontal. Font weight 600.
- Secondary: `var(--warm-white)` background, `var(--dark)` text, 1px solid `var(--dark)` border, same padding.
- Hover: lift 1px (`transform: translateY(-1px)`), background darkens by ~10%.
- Never: gradient fills, pill shapes for primary CTAs, icon-only with no label except in clearly obvious contexts.

**Inputs.**
- Background: `var(--warm-white)` or `var(--cream)`
- Border: 1.5px solid `var(--border)`
- Border-radius: 8–10px
- Padding: 10–12px
- Focus: border becomes `var(--dark)`, no harsh blue focus ring.

**Badges / tags.**
- Border-radius: 999px (pill shape)
- Text: uppercase, font-size 0.56–0.72rem, letter-spacing 0.08em–0.14em
- Background: `var(--dark)` with `var(--cream)` text, or soft colored backgrounds (`var(--yellow-soft)`, `var(--mint)`) with `var(--dark)` text.

**Icons.**
- Use Iconify (iconex set for warm, rounded feel) or Lucide (for sharper utility icons).
- When icons live in containers, use softly tinted square backgrounds: 40×40px, 10px border-radius, background one of the accent soft colors (`#FFF0B8`, `#C8F0DC`, `#FFD9C8`, `#E8E0FA`). Different tint per semantic group — don't use the same tint for everything.

### Layout

- **Text max-width:** 620–820px for body copy. Never full-width paragraphs.
- **Page max-width:** 1080–1280px for most content.
- **Vertical rhythm:** 5rem between major sections, 2.5rem between sub-sections, 1.2rem between related elements.
- **One CTA per section.** If there are two buttons, one is primary and one is a quiet text link.
- **Asymmetry is fine.** Not everything needs to be a centered grid. A 1fr / 1.15fr split reads more intentional than 1fr / 1fr.

### Motion

- **Transitions:** 200–300ms for hover and state changes, with `cubic-bezier(0.22, 1, 0.36, 1)` for things that should feel springy.
- **Entrance:** fade + 16px translate-up, 0.7s duration. Stagger by 100–200ms when multiple elements enter together.
- **Never:** 0ms transitions (feels jarring), 1000ms+ transitions (feels slow), sliding from outside the viewport (feels heavy).

---

## Reference products — the feel we want

These are the sites and products whose aesthetic should inform designs produced by this skill. When in doubt, ask yourself: *"Would this feel at home next to jam.dev or Notion?"*

- **[jam.dev](https://jam.dev)** — the gold standard for inviting-but-confident SaaS design. Warm cream backgrounds, cards that tilt toward the cursor, generous whitespace, product screenshots framed with personality, hand-drawn-feeling accents. Watch how their hero, picker, and section transitions feel alive without being distracting.
- **[Notion](https://notion.so)** — clean warm-white, friendly illustrations, type-led hierarchy, blocks that feel tactile. Their whole site feels like a product designed by someone who cared.
- **[Linear](https://linear.app)** — sharp typography, confident dark sections paired with warm light sections, crisp pill buttons, subtle but deliberate animations. Shows that "confident" doesn't have to mean "cold."
- **[Stripe](https://stripe.com)** — editorial-quality typography, graceful product integrations, section transitions that feel like turning a page.
- **[Arc browser](https://arc.net)** — playful sticker-style badges, tactile card shadows, friendly copy everywhere, motion that makes the product feel alive.
- **[Things 3](https://culturedcode.com/things/)** — restraint as a design choice. Proof that "inviting" can also be quiet.

When building a product's site or app, **pick one of these as your north star** for the section you're working on. Don't copy — channel.

---

## Modern animation patterns (the inviting + playful layer)

Static pages feel dead. The difference between "looks fine" and "feels alive" is usually a handful of small motion patterns applied with intent.

### 1. Cards that tilt toward the cursor (jam.dev pattern)

When hovering over a card, tilt it slightly toward the mouse position. Feels like the card is leaning in to listen.

```css
.card {
  transform-style: preserve-3d;
  transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1);
  will-change: transform;
}
```

```js
card.addEventListener('mousemove', (e) => {
  const rect = card.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  const cx = rect.width / 2;
  const cy = rect.height / 2;
  const rx = ((y - cy) / cy) * -8;  // max 8deg tilt
  const ry = ((x - cx) / cx) * 8;
  card.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg) scale(1.02)`;
});
card.addEventListener('mouseleave', () => { card.style.transform = ''; });
```

Use for: picker cards, product feature cards, interactive showcase tiles. Don't use on every card — reserve for the ones the user is meant to choose.

### 2. Scroll reveal (Stripe / Notion pattern)

Elements fade and slide up as they enter the viewport. Makes the page feel like it's unfolding.

```css
.reveal {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

```js
const obs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      obs.unobserve(e.target);
    }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
```

### 3. Staggered page entrance (Arc / Linear pattern)

When the page loads, elements cascade in. Eyebrow → headline → subhead → CTA. Each delayed by 200ms.

```css
@keyframes entrance {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.page-entrance { animation: entrance 0.9s ease forwards; opacity: 0; }
.page-entrance-1 { animation-delay: 0ms; }
.page-entrance-2 { animation-delay: 180ms; }
.page-entrance-3 { animation-delay: 380ms; }
.page-entrance-4 { animation-delay: 580ms; }
```

### 4. Playful glyph hover (jam.dev + Arc pattern)

Small icon inside a colored square that scales + rotates on parent hover. Tactile, friendly.

```css
.card-glyph {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--yellow-soft);
  transition: transform 0.55s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.35s ease;
}
.card:hover .card-glyph {
  transform: scale(1.18) rotate(-6deg) translateY(-2px);
  background: var(--yellow);
}
```

The `cubic-bezier(0.34, 1.56, 0.64, 1)` gives a slight overshoot that feels bouncy, not robotic.

### 5. Parallax drift for background accents

Warm color blobs that drift slowly across the page as the user scrolls. Subtle depth without heaviness.

```css
.parallax-bg {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  pointer-events: none;
}
.blob-1 { top: 10%; left: 5%; width: 400px; height: 400px; background: var(--yellow-soft); }
.blob-2 { top: 60%; right: 5%; width: 500px; height: 500px; background: var(--peach); }
```

```js
window.addEventListener('scroll', () => {
  const y = window.scrollY;
  document.querySelectorAll('.parallax-bg').forEach((el, i) => {
    const speed = 0.2 + i * 0.1;
    el.style.transform = `translateY(${y * speed * -1}px)`;
  });
});
```

### 6. Pulse on "needs you" indicators

A soft pulse on elements that are waiting for user input. Draws attention without being annoying.

```css
@keyframes needs-you-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(255, 228, 139, 0.6); }
  50%      { box-shadow: 0 0 0 8px rgba(255, 228, 139, 0); }
}
.needs-you { animation: needs-you-pulse 2.4s ease-in-out infinite; }
```

### 7. Button micro-interactions

Buttons should feel tactile. Lift on hover, gentle letterspacing change on transition, disabled state goes quiet but not invisible.

```css
.btn {
  transition: background 0.25s ease, transform 0.25s ease,
              letter-spacing 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.btn:hover:not(:disabled) {
  background: #2a2a2a;
  transform: translateY(-1px);
  letter-spacing: 0.04em;
}
.btn:disabled { opacity: 0.6; cursor: wait; }
```

### 8. Coral squiggle underline (hand-drawn accent)

A wavy coral line drawn underneath a word or phrase to mark it as important without the shouty feel of a full highlight or bold. Feels handcrafted and warm. Looks like someone underlined the word with a coral marker.

**When to use it:**
- Under a key verb in a headline ("Now Claude *knows* me.")
- Under a proof word in body copy
- Under product names or sticker-style tags when you want a softer alternative to pill badges
- As a punctuation-free way to say "this word matters"

**Don't use it:**
- More than once or twice per section. It loses weight if overused.
- On long phrases. Keep it to 1–3 words max so the squiggle reads as a deliberate underline, not a decoration running across the page.
- In UI that needs to feel clinical. It's warm and playful. Wrong for dashboards.

**SVG path (inline):**

```html
<svg viewBox="0 0 120 12" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M2 7 Q 12 2, 22 7 T 42 7 T 62 7 T 82 7 T 102 7 T 118 6"
        stroke="#E66158" stroke-width="2.2" stroke-linecap="round" fill="none"/>
</svg>
```

**As a reusable CSS utility:**

```css
.squiggle {
  position: relative;
  display: inline-block;
  white-space: nowrap;
}
.squiggle::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -0.25em;
  height: 0.3em;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 12' preserveAspectRatio='none'><path d='M2 7 Q 12 2, 22 7 T 42 7 T 62 7 T 82 7 T 102 7 T 118 6' stroke='%23E66158' stroke-width='2.2' stroke-linecap='round' fill='none'/></svg>");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  pointer-events: none;
}
```

Then anywhere: `<span class="squiggle">important</span>`.

**Tuning notes:**
- `stroke-width` controls thickness. 2.2 is the sweet spot for body text. Bump to 3 for headlines.
- `stroke-color` is coral (`#E66158`) but can swap to any accent. Yellow for a warmer feel, peach for softer.
- The path has 5 bumps across 120 units. For shorter words (2–4 characters), the bumps read too dense. Either narrow the viewBox or shorten the path.
- `bottom: -0.25em` places it just below the baseline. Tune up/down depending on font and weight.

### 9. Success confirmations

When a user clicks "copy" or completes an action, the button morphs to a success state with a checkmark and a short phrase. Confirms without a modal.

```js
btn.addEventListener('click', async () => {
  await navigator.clipboard.writeText(text);
  btn.textContent = 'Copied ✓';
  btn.classList.add('copied');
  setTimeout(() => {
    btn.textContent = 'Copy';
    btn.classList.remove('copied');
  }, 2000);
});
```

```css
.btn.copied { background: #2d7a4a; }
```

### When to use animations (and when not to)

**Use when:**
- The page feels "dead" on first load — add entrance + reveal
- A card is meant to be chosen — add tilt + glyph hover
- A button is meant to be clicked right now — add pulse
- A section explains a product feature — add scroll reveal

**Don't use when:**
- Motion would distract from reading (no animations on body copy)
- The user is doing a focused task (no decorative motion in editors, forms, settings)
- Accessibility matters — respect `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Playful details checklist (required before calling a design done)

A design without these will feel competent-but-dead. Run through this checklist on every UI. If you can't check a box, add the missing detail before shipping.

### Icons
- [ ] **Icons are representational, not abstract shapes.** A runner for Morning Run, a book for Read, a water drop for Drink Water, a moon for Meditate. Use **Iconify** (`iconex` set — warm, rounded) or **Lucide** (sharper utility). Never replace a meaningful icon with an arrow, square, or circle just because it's "minimal."
- [ ] **Icons sit in softly tinted square containers** (40×40px, 10px border-radius) using different tints per semantic group — mint for movement, yellow for reading/learning, peach for mindfulness, sand for neutral. Not all-the-same-tint.

### Rewards and achievements
- [ ] **Streaks and progress have warmth indicators.** A 🔥 flame next to streaks over 7 days. A subtle color shift or badge at 30-day milestones. Stats aren't just numbers — they're small wins, celebrated.
- [ ] **Completed states feel like completions.** Checked-off items get a soft mint background tint and a line-through or dimmed text. Don't just remove them.

### Current-state indicators
- [ ] **"You are here" markers use warm yellow fill,** not hard black. The current day in a week view is a yellow-filled circle with dark text — not an inverted-color shock.
- [ ] **Selected states get a soft color wash,** not a harsh border or outline.

### Microcopy warmth
- [ ] **At least one human touch per screen.** A greeting that includes progress (*"Good morning, Alex. Three down today."*). An empty state that encourages (*"Nothing here yet. Drop something in."*). A CTA that invites (*"Track something new"* vs *"Add Item"*).
- [ ] **Numbers get context.** "3 of 5 done" is a dashboard. "Three down today" is a person.

### CTAs
- [ ] **Primary CTAs are FILLED, not outlined.** An outline CTA is a whisper. If you want someone to tap it, fill it.
- [ ] **Secondary CTAs are quiet text links or outline buttons.** Never two filled CTAs competing.

### Tactile moments
- [ ] **At least one tactile element per screen.** A card that tilts toward the cursor. A button that lifts on hover. A glyph that scales playfully when its parent is hovered. If the page is fully static on hover, it's dead.
- [ ] **Interactive elements respond within 100ms.** Delay feels broken.

### Typography variety
- [ ] **Hero numbers use the display font,** not the headline font. A "21" at 3rem in Lora feels like an essay. In Fraunces or DM Serif Display, it feels like a trophy.
- [ ] **Letter-spacing is tuned per context.** Tight (`-0.015em`) for big display. Normal for body. Wide (`0.12em+`, uppercase) for eyebrows and badges.

### When in doubt
Ask: *"Would jam.dev ship this?"* If the answer is "they'd add more personality," do that.

---

## Channeling jam.dev specifically

jam.dev is the north star for "inviting + playful + confident." If the user's profile points to jam.dev, channel these specific moves:

1. **Hero-first, with a warm dark section right after.** Cream hero, bold serif headline, then immediately a warm-ink-dark section with a product screenshot that feels like proof.
2. **Cards that tilt toward the cursor.** Every picker card, every option. Not subtle — up to 8 degrees of tilt. Feels like the card is listening.
3. **Sticker-style badges.** Small pills with uppercase letter-spacing, dropped on cards as "new" / "recommended" / "most popular" markers. They should feel applied, not integrated — like actual stickers.
4. **Hand-drawn-feeling arrows.** Annotations that point to features or screenshots. Slightly wobbly curves, not perfect SVG arcs. Conveys "a person drew this."
5. **Section transitions that feel like page turns.** Not hard cuts between sections. Softer — use subtle color shifts in the background, scroll-reveal animations, sometimes a playful divider.
6. **Typography that goes oversized with confidence.** H1s at 4–6rem on desktop. Hero numbers even bigger. No fear of scale.
7. **Product screenshots framed with personality.** Not just a raw screenshot — floating inside a warm rounded container, with a soft shadow, maybe a fake browser chrome around it. Makes the product feel like a character on the page.
8. **Copy that's slightly wry.** Not jokes. Just a knowing voice. "The bug-reporting tool that doesn't make you want to quit." That kind of thing.
9. **Motion that rewards interaction.** Hover a card → it tilts. Click a button → it lifts and confirms. Scroll past a section → elements reveal staggered. Nothing is static.
10. **No stock photos. Ever.** Illustrations should feel hand-made or bespoke. Even product screenshots get framed with care.

If the user's profile says "jam.dev" — these are the moves. Don't half-ass them.

---

## Anti-patterns (what NOT to produce)

If you find yourself generating any of these, stop and reconsider:

- **Blue primary buttons.** Too Silicon Valley default.
- **Gradient fills on buttons or cards.** Feels 2015 SaaS.
- **Material Design floating action buttons.** Not this aesthetic.
- **Shadows that look like box-shadow: 0 4px 6px rgba(0,0,0,0.1).** That's the Bootstrap default.
- **Stock illustrations (Undraw, Storyset).** They all look the same now.
- **Three-column feature grid with identical cards.** Lazy layout.
- **"Transform your life with..."** copy in headlines. Use the /voice skill.
- **Emoji as visual hierarchy.** Use tinted icon squares instead.
- **Dark mode as default.** Warm light themes first. If dark mode matters, make it warm-dark (ink, not charcoal).
- **Rounded-pill primary buttons.** Feels consumer-app, undermines confidence.

---

## By context

**Onboarding.** One step per screen. One idea per step. One CTA. No walls of text. Progress indicator if more than 3 steps.

**Empty states.** Tell the user what's going to be there and how to start. "Nothing here yet. Add your first [thing] to get started." Or warmer: "It's quiet in here. Drop something in." Include a visible CTA button, not just a text link.

**Errors.** Calm and specific. What happened, what to do. "Couldn't load your data. Try again, or refresh the page if it keeps happening." Never a raw error message. Never a generic "Something went wrong."

**Loading states.** Use skeletons that match the actual layout shape — not just a spinner. Button loading states keep the button in place but show a subtle pulse or dot animation.

**Mobile.** Design at 375px first. 44×44px minimum tap targets. Test before calling it done.

**Data display.** Numbers get generous size and weight. Use Lora for display numbers if the rest of the page uses it for headlines — makes stats feel editorial, not dashboard-ish.

---

## Process

1. **Read the existing direction.** If the product has a profile, palette, or existing components, start there.
2. **Name the feeling.** Three adjectives. If you don't know, ask.
3. **Pick the palette.** Two accent colors plus cream + dark. Not more.
4. **Pick the type pair.** Serif + sans. Commit.
5. **Build one component at a time.** Card first, then button, then input, then layout. Not all at once.
6. **Check against anti-patterns.** Would this look like any SaaS? If yes, rework.
7. **Test at mobile 375px.** Before calling it done.

---

## Output shape

When producing a full design (e.g., a landing page, an app screen, a component set):

- Lead with the **feeling** in one line.
- Follow with the **palette** as hex codes.
- Follow with the **type scale**.
- Then the **components** in working code.
- End with **one note** on what would break the feel if changed (the load-bearing decision).

Don't present three options. Make a decision and implement it. If the user wants alternatives, they'll ask.
