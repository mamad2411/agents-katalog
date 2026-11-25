---
name: recording-studio-imagegen-mobile
description: Generate premium mobile app screen images and flows. Use when a Recording Studio host needs iOS, Android, or cross-platform comps. This is an image-only job. Flatpack applies only if a later step builds related web screens.
---

# Recording Studio imagegen mobile

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/imagegen-frontend-mobile` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

This skill generates mobile screen images only. Do not write SwiftUI, React Native, Flutter, HTML, Tailwind, or Flatpack here. Related web screens later: `recording-studio-image-to-code` and `recording-studio-flatpack`. Taste: `recording-studio-taste`. Brand: `recording-studio-brandkit`. Web comps: `recording-studio-imagegen-web`. Direction packs (for web themes, not these images): `recording-studio-soft`, `recording-studio-minimalist`, `recording-studio-brutalist`.

## When to use

- Onboarding, auth, home, profile, settings, chat, commerce, health, or productivity app comps
- A multi-screen flow that must feel like one product
- The user asked for mobile images, not implementation

Not for websites, landing pages, or coding. Use `recording-studio-imagegen-web` or `recording-studio-image-to-code` for those.

## Output

Generate the screens. Do not answer with description only.

- 1 screen → 1 image
- 5 screens → 5 images
- Onboarding → several distinct screens, not one slide
- App concept → a meaningful set, not a single hero

Do not crop details from a collage. Generate a fresh screen. Do not collapse a flow into one board.

Show screens in a clean phone frame by default. The content stays the hero. Even margins, consistent device scale, soft shadow. Omit the frame only if the user asks for raw screens.

## Platform

Pick one and keep it: iOS-native premium, Android-native premium, or cross-platform premium. Do not mix tab bars and Material app bars at random.

## Design bible

Lock before a multi-screen set: platform, device frame, palette, type mood, radius, icons, imagery, texture, navigation, cards, buttons, shadows.

Screens 3 and 5 must still be the same app. Variation is composition and job, not identity.

Flows must be logical: onboarding → auth → home, browse → detail → cart, profile → settings. Not a random gallery.

## First screen

Calm, readable, one focal point, short headline, one next action. No widget pile, no website-hero-inside-a-phone.

Respect safe areas, status bar, tab bar, and home indicator. These should feel like app screens, not posters.

## Layout and type

Fewer containers. No card-in-card-in-card. Generous spacing. Text never feels small. If type is tiny, simplify or split a screen.

Copy is short and real. No Elevate / Unlock your potential / NovaCore.

Icons should feel brand-specific, not a generic developer pack.

## Art direction

Imagery, grain, and fades are allowed when they help and text stays readable. Texture supports mood; it does not fight the UI.

Not every app must be ultra-minimal. Clean is required. Simple is optional.

Pick one theme paradigm, one type character, one structure bias, one image bias, one texture, one palette logic. Choose four signature modules and two motion-implied cues (image energy only, not code).

## Category bias

- Fintech: trust, clear numbers, almost no fake charts
- Health: calm metrics, airy spacing
- Productivity: list discipline, task hierarchy
- Social: feed vs create, stronger media
- Commerce: browse / detail / checkout, stable product frames

## Quality check

Real app, not a website in a phone. Safe areas. Enough screens. Logical flow. Readable type. Controlled palette. Consistent mockups. No purple-blue fintech default, no Lucide-template icons, no nested-box clutter.

Regenerate weak screens. Do not settle.

## If web screens come next

Extract palette, type, and radius into a named Flatpack theme. Dummy / gem / Admin stay rounded unless opted in. Do not treat these mobile images as a mandate to add a native kit to the gem.
