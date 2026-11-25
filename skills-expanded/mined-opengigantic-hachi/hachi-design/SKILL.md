---
name: hachi-design
description: Use this skill to generate well-branded interfaces and assets for Hachi (a local-first personal AI agent by Open Gigantic), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.
If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.
If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Hachi in one breath
A local-first personal AI agent you can trust — it runs long, autonomous tasks on your machine, but only ever within the permissions and budget you set. **You hold the leash.** Endorse as "Hachi by Open Gigantic". Warm, premium, flat. Calm Torii-red Shiba mascot.

## The non-negotiables
- **One accent.** Torii red `#D64933` — mark + primary actions only, never body text or large fills. Cream `#F3E9D2` / bone `#FBF7EF` carry the warmth.
- **Flat.** No gradients, glows, or shadows beyond a functional focus ring. Hairline 0.5px borders, radius 16 cards.
- **Two weights only** (400/500). General Sans (display), Inter (body), JetBrains Mono (terminal/code). **Sentence case everywhere; never ALL CAPS.** Wordmark is lowercase `hachi`.
- **Voice:** calm, loyal, plainspoken. Address the user as *you*; Hachi speaks of itself in third person ("Hachi is resting"). No emoji.
- **Cost & permissions are always visible.** Budget reads "spent $X of $Y". The leash prompt is the signature surface — calm and clear, never an error.
- **Never recolour the mascot.**

## Where things are
- `styles.css` — global entry (link this). Tokens in `tokens/`.
- `components/` — React primitives (namespace `window.HachiDesignSystem_46e488`): Button, StatusPill, Input, Switch, Badge, Card, Toast, LoyalLoop, HachiMark, **LeashPrompt**, RunCard, Terminal. See each `.prompt.md`.
- `ui_kits/` — full screens for the three surfaces: `webapp/`, `tui/`, `cli/`.
- `assets/` — mascot mark + variants, the loyal-loop ∞ spinner.
- `guidelines/` — foundation specimen cards (Type, Colors, Spacing, Brand).
