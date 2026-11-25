# Portfolio Project — Claude Instructions

## Token Optimisation Rules
- **Read only the targeted section** before editing. Use `offset`+`limit` or `grep -n`.
- **Edit, don't rewrite.** Use the Edit tool for surgical changes.
- **Grep before Read.** Always `grep -n` for a symbol before opening the file.
- **No whole-file dumps.** `index.html` is ~2100+ lines — never read it all.

## Project Facts
- **Live file**: `index.html` (~2100 lines, React/JSX compiled in-browser via local Babel)
- **Backup**: `portfolio.html` — older baseline, not served
- **Server**: `python3 -m http.server 8080` from `/Users/attadeep/Downloads/portfolio/`
- **Local scripts**: `react.min.js`, `react-dom.min.js`, `babel.min.js` (CDN replaced with local files)
- **Edit password**: `portfolio2026`
- **Contact email**: `attadeepgajbhiye@gmail.com` (FormSubmit wired)

## Architecture
- All content in `const PROFILE`, `_PB_PROJECTS`, `_PB_TESTIMONIALS`, `_PB_CLIENTS`, `_PB_POSTS`, `_PB_SERVICES` near lines 556–680
- `_OV` loads from `localStorage['portfolio-autosave']` then falls back to `window.__PORTFOLIO_OVERRIDES`
- `EditorPanel` (line ~1585): password → `prompt()`, opens side panel with Profile/Skills/Deploy tabs
- `StyleInspector` (line ~1860): Claude Design-style right panel — click any element in edit mode → Typography, Size, Box, Shadow, Text, Transform, Position, Display/Flex, Animation sections + Deploy/Save/Download footer
- `useInlineEdit`: click `[data-editable]` elements to edit text inline
- `useMediaUpload`: click `.placeholder` slots to upload image/video (stored in `localStorage['portfolio-media']`)
- Contact form POSTs to `formsubmit.co/ajax/attadeepgajbhiye@gmail.com`, also saves to `localStorage['portfolio-contacts']`
- Leads inbox: EditorPanel → Leads tab shows all contact submissions

## StyleInspector Sections (right panel, 270px wide)
- TYPOGRAPHY: Font, Size, Weight, Color, Align, Line height, Tracking
- SIZE: Width, Height
- BOX: Opacity, Padding (T/R/B/L), Margin (T/R/B/L), Border, Radius, Background
- SHADOW: Box shadow, Text shadow
- TEXT: Transform, Style, Decoration
- TRANSFORM: Rotate, Scale, Translate X/Y
- POSITION: Type, Top/Right/Bottom/Left, Z-index
- DISPLAY/FLEX: Display, Direction, Gap, Align items, Justify
- ANIMATION: Preset (fadeIn/slideUp/slideDown/scaleIn/bounceIn/pulse), Duration, Delay, Easing, Repeat, Transition
- Footer: Save, Copy CSS, Reset, Deploy to GitHub, Download HTML

## localStorage Keys
- `portfolio-autosave` — all content overrides (JSON)
- `portfolio-media` — uploaded images/videos per slot (JSON, keyed by data-editable)
- `portfolio-contacts` — contact form submissions array
- `portfolio_gh_token` — GitHub PAT for deploy

## What NOT to do
- Do NOT add hardcoded `height` or fractional `padding` values to JSX style props.
- Do NOT install packages or create new files unless asked.
- Do NOT read `portfolio.html` — it's a stale backup.
- Do NOT re-read the whole `index.html` — use grep + offset/limit.
