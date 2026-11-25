---
name: ui-ios
description: Generate slop-free SwiftUI UI for iOS 17+ (iPhone and iPad). Use whenever the user asks to build, design, scaffold, restyle, or improve a SwiftUI screen, View, sheet, NavigationStack, tab, or any iOS interface. Greenfield mobile coverage — does not replace any existing skill. Two phases — tokens first (with approval gate), then UI — both gated by a self-audit checklist that the model MUST run before claiming done.
---

# ui-ios — Slop-Free SwiftUI Skill

You are generating production-grade iOS UI in SwiftUI (iOS 17+) and Swift 5.9+. This skill exists because untouched LLMs produce **AI slop**: purple→pink LinearGradients, default centered VStack heros, three-card LazyVGrid features, magic numbers everywhere (`.padding(13)`, `.cornerRadius(7)`), Inter on iOS, glassmorphism on every card, "Get Started" buttons, and the median of every SwiftUI tutorial scraped from GitHub. This skill replaces guesses with **constraints**.

The non-negotiable rule: **NEVER use a buzzword in place of a token.** Words like *clean*, *modern*, *professional*, *sleek*, *premium* are banned from your reasoning. Every aesthetic choice must trace back to a named anchor recipe in `anchors.md` and a value in `Theme/Tokens.swift`.

iOS adds a second non-negotiable: **HIG mechanics are strict.** 44pt minimum touch targets. SF Symbols only for system icons. Dynamic Type mandatory. Safe area respected. NavigationStack for navigation. `.sheet` / `.fullScreenCover` for modal presentation. Swipe-back gesture preserved. Brand has freedom over color, custom typography (with declared system fallback), accent, motion personality, and shape — not over the platform mechanics above.

---

## Workflow (follow in order)

### Step 0 — Project scan (decides bootstrap vs extend mode)

Before any other action, check for:

```
DESIGN_RULES.md                      # at repo root → if exists, you are in EXTEND mode
*/Theme/Tokens.swift                 # → if exists, you are in EXTEND mode
*/Theme/ThemeModifier.swift
.swiftlint.yml                       # check for custom slop rules
```

- **If `DESIGN_RULES.md` exists**: read it. Read the existing `Tokens.swift`. Skip to **Step 3 (Phase 2: UI)**. Use only existing tokens. NEVER add new colors/spacing/radii without asking.
- **If `Tokens.swift` exists but no `DESIGN_RULES.md`**: read tokens, infer the closest matching anchor, ask the user to confirm the inferred anchor, then write `DESIGN_RULES.md` and proceed to Phase 2.
- **If neither exists**: you are in **bootstrap mode**. Continue to Step 1.

### Step 1 — Intake (interactive, bootstrap only)

Use AskUserQuestion to gather, in this order:

1. **Anchor pick** — show the 8 recipes from `anchors.md` (one-line summary each). Note that **Apple Music / Podcasts** is the most native to iOS and the safest default. Let the user pick 1–3. If 2–3, ask which is primary and which contributes type vs color vs motion.
2. **Ban menu** — show the 8 ban patterns from `ban-patterns.md` with the 3 default-on items pre-checked. Confirm.
3. **Project context**:
   - Content density: airy / balanced / dense
   - Primary surface: app / utility / reader / media / form-heavy / game-shell
   - Dark mode: required (default on iOS) / optional / none
   - iPad support: yes / no
   - Brand color (if any): hex value or "derive from anchor"
   - Custom typography: yes (must declare a system font fallback) / no (use SF Pro)

Do NOT ask vibe questions ("how should it feel?"). Ask only the questions above.

### Step 2 — Phase 1: tokens (gated)

Generate, in this order:

1. **`<App>/Theme/Tokens.swift`** — enum-based tokens. Use the template at `templates/Tokens.swift.tmpl`. Required enums: `Theme.Color`, `Theme.Spacing`, `Theme.Radius`, `Theme.Font`, `Theme.Shadow`, `Theme.Motion`.
2. **`<App>/Theme/ThemeModifier.swift`** — `EnvironmentKey`-driven theme injection so views never reach into `Tokens` through string literals or hardcoded paths.
3. **Color assets** — `Background`, `Surface`, `Accent`, `TextPrimary`, `TextSecondary`, semantic (`Success`, `Warning`, `Danger`) — each with `Any Appearance` and `Dark Appearance` variants in `Assets.xcassets`. List the assets the user must add; do not invent hex values without anchor justification.
4. **`.swiftlint.yml`** patch — enable the slop-blocking custom rules from `templates/swiftlint.yml.tmpl`.
5. **`DESIGN_RULES.md`** at repo root — fill `templates/DESIGN_RULES.md.tmpl` with the chosen anchors, active bans, token file paths, and verification command.
6. **`CLAUDE.md` patch** — append (do not overwrite): `Before any UI/UX work, read and follow DESIGN_RULES.md.`

Then **run the Token Audit** from `verification.md` and print the PASS/FAIL table to the user. **Do not proceed to Phase 2 until the user approves.**

### Step 3 — Phase 2: UI

Generate the requested screen/View using **only values from `Theme.*`**. Follow:

- **`component-anatomy.md`** — exact rules for Button, TextField, List/Form rows, NavigationStack, sheets, ConfirmationDialog, Alert, TabView, ProgressView, ContentUnavailableView, form fields.
- **`motion.md`** — easing curves and durations.
- **`copy-voice.md`** — every string is real, contextual copy. No lorem ipsum, no filler. Honor iOS button conventions (Cancel left, primary right; "Done" capitalized in nav bars).
- **`icons-imagery.md`** — SF Symbols ONLY for system icons. Never Lucide / Phosphor / custom inline SVG when SF Symbols has the glyph.

Then **run the UI Audit** from `verification.md` AND `swiftlint`. Print the audit table. Fix every FAIL before claiming done.

---

## Files in this skill

| File | When to read |
|---|---|
| `anchors.md` | Step 1, before showing the user choices. ALWAYS read fully — never quote from memory. |
| `ban-patterns.md` | Step 1, when showing ban menu. Step 2 and 3, when verifying. |
| `component-anatomy.md` | Step 3, before writing any View. |
| `motion.md` | Step 3, when adding any `.animation` or `withAnimation`. |
| `copy-voice.md` | Step 3, before writing any user-facing string. |
| `icons-imagery.md` | Step 3, when choosing SF Symbols or images. |
| `verification.md` | After Step 2 (Token Audit) and after Step 3 (UI Audit). MANDATORY — do not skip. |
| `templates/*` | Use as the basis for the generated files; fill placeholders, never ship as-is. |

## Hard rules (the model must obey these always)

1. **No magic numbers.** Forbidden: `.padding(13)`, `.frame(width: 372)`, `.cornerRadius(7)`, `Color(red: 0.2, green: 0.4, blue: 0.6)`, `Color(hex: "#3a4f6b")`. Every value must come from `Theme.Spacing`, `Theme.Radius`, `Theme.Color`, `Theme.Font`, or `Theme.Motion`. If you need a value that does not exist, ask the user to add it.
2. **No buzzwords in code or comments.** Banned strings in your output: *clean*, *modern*, *professional*, *sleek*, *premium*, *beautiful*, *elegant* (except in copy if the user explicitly asked for those words).
3. **No default-style-tells unless the chosen anchor explicitly allows them.** Specifically: no `LinearGradient(colors: [.purple, .pink], ...)`, no `[.indigo, .purple]`, no `.ultraThinMaterial` on cards (only on chrome — toolbar, sheets — where iOS uses it natively).
4. **No filler copy.** No lorem ipsum. No "Lightning fast", "Built for iOS", "Powered by AI", "Get Started", "Beautiful and intuitive".
5. **Touch targets ≥ 44pt** on every interactive element. Verify with `.frame(minHeight: 44)` or `.contentShape`.
6. **Dynamic Type support is mandatory.** Use `.font(.body)`, `.font(.headline)`, `Theme.Font.body()` — never fixed `.system(size: 14)` outside `Theme.Font`. Test at `xxxLarge`.
7. **Safe area is respected.** No `.ignoresSafeArea` unless intentional and documented inline with a `// SAFE-AREA-IGNORE: <reason>` comment.
8. **VoiceOver labels** on every icon-only Button (`.accessibilityLabel("...")`).
9. **Dark mode parity.** Every Color comes from an asset with both Any/Dark variants OR from `Theme.Color`. Verify by toggling preview.
10. **SF Symbols only** for system iconography. `Image(systemName:)` always. Custom `Image("name")` only for brand artwork.
11. **You must run the verification checklist** before responding "done". Print the audit table to the user.

## What this skill is NOT

- Not a magic-aesthetic generator. You still have to pick an anchor and follow it.
- Not a copy generator. Phase 2 stops and asks for real copy when needed.
- Not a brand-design tool. Logo and brand identity are the user's call.
- Not a replacement for design review with humans. The audit table is a floor, not a ceiling.
- Not for AppKit, Catalyst, or visionOS — pure SwiftUI on iOS 17+ only. For iPad-specific patterns (Sidebar, three-column), follow the same anchors but defer column layout to user request.
