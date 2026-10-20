---
description: Frontend quality bar for components, pages and screens
globs: "**/*.{tsx,jsx,vue,svelte,astro,html,css,scss,dart}"
alwaysApply: false
---

# Frontend Quality

## Components
- One clear responsibility per component or widget. Extract when reused or when it owns state, not before.
- Semantic structure first (web: `header`, `nav`, `main`, `section`, real `button` and `a`; Flutter: `Semantics`, proper button widgets).
- Keep data fetching and business logic out of presentational components. Components receive typed props/params.
- Reuse the project's existing primitives before creating new ones.

## Responsive
- Mobile-first. Check at 360px, 768px, 1024px, 1440px (or phone, tablet, desktop for apps).
- No horizontal scroll at 320px. Responsive images with explicit dimensions.
- Touch targets at least 44x44px (48dp on Android) with spacing between them.

## Interaction states
Every interactive control has: default, hover (pointer devices), focus-visible, active/pressed, disabled. Hover must never be the only way to reveal content.

## Screen states (do not build only the happy path)
For any screen that loads data, submits a form, or calls an API, handle where relevant:
- **Loading**: skeleton or inline indicator sized like the content. No layout shift.
- **Empty**: explain what is missing and the next action.
- **Error**: plain-language message, retry where possible, no raw error text.
- **Success**: confirm the outcome and what happens next.
- **Offline**: detect network failure and say so; queue or retry where sensible.
- **Permission denied / unauthorized**: clear message and path forward, no leaked details.
- Disable submit while pending and prevent double submission (payments especially).

## Consistency
- Same action, same control, same wording everywhere.
- Forms: visible labels, validation on blur, errors next to the field, preserve input on failure.
- Verify every supported theme (light/dark) and locale direction if the project has them.
