---
name: ios-design-system
description: Use when styling any SwiftUI view or changing the look and feel of the iOS app (AgenticApp). Covers Theme tokens, DS components and how to restyle the whole app.
---

# iOS design system

All styling comes from `AgenticApp/DesignSystem/Theme.swift`, read through `@Environment(\.theme)`. Its colours and spacing come from `DesignTokens.swift`, generated from `design/tokens.json`: the same palette as the web app, back office and website.

## Tokens

- `theme.colors` – primary, onPrimary, background, surface, border, textPrimary, textSecondary, success, error (light and dark mode)
- `theme.typography` – title, headline, body, caption
- `theme.spacing` – xs 4, s 8, m 16, l 24, xl 32
- `theme.radius` – s, m, l

## Components

- `Button("…") {}.buttonStyle(.ds(.primary))` or `.ds(.secondary)`
- `DSCard { … }` for grouped content
- `DSLoadingView()` and `DSErrorView(message:retry:)` for loading and error states
- `DSTextField(label:text:isSecure:error:identifier:)` for form fields

## Rules

- Never hard-code colors (`Color.blue`, hex), font sizes or paddings in features. Use tokens.
- Need something new? Add a token or a `DS*` component first, then use it.
- To change the palette for every app: edit `design/tokens.json` and run `node design/build.mjs`. Never edit `DesignTokens.swift` by hand.
- To restyle only iOS: create another `Theme` and inject it in `AppContainer`.
- Keep Dynamic Type working: build fonts from text styles (`.body`, `.headline`), not fixed sizes.
