# Copilot instructions for this repository

## Project shape
- This is a Vite + React 18 single-page marketing site (no backend, no API layer, no routing flow in use).
- Entry point: `src/main.tsx` renders `src/app/App.tsx`.
- `App.tsx` composes sections in a fixed order: `Navigation → Hero → Benefits → Difference → Process → Guarantee → FAQ → Pricing → Footer`.
- The top scroll progress bar in `App.tsx` is driven by `useScrollProgress()` from `src/app/components/hooks/useAnimations.tsx`.

## Section and navigation conventions
- Navigation links are in-page anchors (`#miks?`, `#protsess`, `#garantii`, `#kkk`, `#hinnad`) defined in `src/app/components/Navigation.tsx`.
- Matching section IDs must exist on section root elements (example: `Pricing` uses `id="hinnad"`).
- If you add/rename a section, update both the section `id` and `navItems` to keep smooth scrolling functional.

## Animation patterns used here
- Animations are handled with `motion/react` (`motion.div`, `motion.button`) plus small custom hooks.
- Reuse hooks from `src/app/components/hooks/useAnimations.tsx`:
  - `useInView()` for one-time reveal animations.
  - `useMagnetic()` for CTA cursor-follow interactions.
  - `useCountUp()` where numeric counters are needed.
- Existing sections rely on simple, local animation state; do not introduce global animation/state libraries.

## Styling and UI conventions
- Tailwind CSS v4 is enabled via `@tailwindcss/vite` and `src/styles/tailwind.css`.
- Theme tokens and base styles live in `src/styles/theme.css`; prefer these tokens for reusable UI primitives.
- This codebase intentionally mixes Tailwind utility classes with inline styles for exact typography sizing and branding.
- Keep brand typography consistent with current usage (`Poppins`, `Inter`, `Cormorant Garamond`) from `src/styles/fonts.css`.
- Use existing UI primitives from `src/app/components/ui/*` when building generic controls; section components are mostly custom.

## Imports and file organization
- Use the `@` alias for `src` when it improves readability (configured in `vite.config.ts`).
- Keep page sections under `src/app/components/`; keep shared hooks under `src/app/components/hooks/`.
- Keep utility class merging through `cn()` from `src/app/components/ui/utils.ts` for reusable components.

## Dev workflow
- Install: `npm i`
- Run dev server: `npm run dev`
- Production build: `npm run build`
- There are currently no test or lint scripts in `package.json`; verify changes with a Vite build and manual browser check.

## Content constraints in this project
- Marketing copy is in Estonian; preserve language and tone unless explicitly asked to rewrite content.
- This repository appears generated from Figma Make (`README.md`, `vite.config.ts` comments); preserve required plugin setup and structure.