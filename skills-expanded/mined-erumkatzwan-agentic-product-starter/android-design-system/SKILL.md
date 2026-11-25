---
name: android-design-system
description: Use when styling any composable or changing the look and feel of the Android app (AgenticApp). Covers AppTheme tokens, DS components and how to restyle the whole app.
---

# Android design system

All styling comes from `designsystem/Theme.kt`, read through `AppTheme` (`AppTheme.colors.primary`, `AppTheme.spacing.m`). Its colours and spacing come from `DesignTokens.kt`, generated from `design/tokens.json`: the same palette as the iOS app, web app, back office and website. `AppTheme { }` also maps the tokens onto Material 3, so Material components follow the palette.

## Tokens

- `AppTheme.colors` – primary, onPrimary, background, surface, border, textPrimary, textSecondary, success, error (light and dark mode follow the system)
- `AppTheme.typography` – title, headline, body, caption
- `AppTheme.spacing` – xs 4, s 8, m 16, l 24, xl 32
- `AppTheme.radius` – s, m, l

## Components

- `DSScreen(title, onBack, actions) { padding -> … }` for every screen: top bar, back arrow (`nav.back`), edge-to-edge insets
- `DSButton(text, onClick, kind = DSButtonKind.PRIMARY | SECONDARY)`
- `DSCard { … }` for grouped content
- `DSLoadingView()` and `DSErrorView(message, onRetry)` for loading and error states
- `DSTextField(label, value, onValueChange, tag, isSecure, error)` for form fields

## Rules

- Never hard-code colours (`Color.Blue`, hex), font sizes or paddings in features. Use tokens.
- Need something new? Add a token or a `DS*` component first, then use it.
- To change the palette for every app: edit `design/tokens.json` and run `node design/build.mjs`. Never edit `DesignTokens.kt` by hand.
- To restyle only Android: create another `Theme` and provide it in `AppTheme`.
- Use `sp` for text so system font scaling works, and keep touch targets at least 48dp.
