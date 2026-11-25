---
name: accessibility
description: Use when building or changing any screen, component or colour, when an accessibility check is red, before a release, or on request ("is this accessible", "add VoiceOver labels", "fix contrast"). Keeps every app at WCAG 2.2 AA.
---

# Accessibility

The standard is **WCAG 2.2 AA** in every app ([ADR-0011](../../../docs/adr/0011-accessibility.md)). Checks enforce most of it; this skill covers how to build so they pass and what to check by hand.

## 1. While building a screen

* **Colours** come only from semantic tokens (`textPrimary`, `controlBorder`, …). If you change `design/tokens.json`, `node design/build.mjs` fails when a pair drops below 4.5:1 (text) or 3:1 (control borders) in light or dark mode. Fix the token, never the check.
* **Names:** every control has a visible label or an accessible name. Icon-only buttons: `aria-label` (web), `.accessibilityLabel` (iOS), `contentDescription` (Android).
* **Structure:** one `h1` per web page, headings in order, landmarks (`main`, `nav`). On iOS mark titles with `.accessibilityAddTraits(.isHeader)`; on Android `Modifier.semantics { heading() }`.
* **Touch targets:** at least 44×44 pt on iOS, 48×48 dp on Android, 24×24 CSS px on the web.
* **Text size:** use the design system fonts, which scale with Dynamic Type and Android font size. Never fix a height that clips text.
* **State is not colour only:** errors have text, not just a red border. Link errors to fields (`aria-describedby` on the web).
* **Keyboard and focus (web):** everything works with Tab, Enter and Space, focus is visible, dialogs trap and return focus.
* **Motion:** respect reduced motion settings.

## 2. Test it

* **Web app / back office:** add the new screen to `src/accessibility.test.tsx` and to `e2e/accessibility.spec.ts`.
* **Website:** add new pages to `apps/website/e2e/accessibility.spec.ts`.
* **iOS:** visit the new screen in `AgenticAppUITests/AccessibilityUITests.swift` and call `audit("screen")`.
* **Android:** visit it in `AccessibilityUiTest.kt` and call `showsThenCheck("tag")`.

All of these run unless the repository variable `ACCESSIBILITY_CHECKS` is `off`. Never turn it off to make a pull request green; only the product owner decides that, for the whole product.

A failing check prints the rule and the element. Fix the app; only skip a rule for a known platform false positive, with a comment saying why.

## 3. By hand, before a release

Automated tools catch about a third to a half of issues. Once per release, on one real device each:

1. VoiceOver (iOS) and TalkBack (Android): sign in, sign up and the main flow, eyes closed. Is every element announced with a sensible name, in a sensible order?
2. Largest text size: nothing clipped or overlapping.
3. Web with only a keyboard: complete the main flow; focus is always visible.
4. Dark mode and increased contrast settings.

Record each finding as an issue.
