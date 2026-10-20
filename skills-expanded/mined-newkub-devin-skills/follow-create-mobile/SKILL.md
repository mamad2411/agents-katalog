---
name: follow-create-mobile
description: Create a mobile app — native (Kotlin Multiplatform) or cross-platform (Capacitor)
argument-hint: "[domain]"
related:
  - follow-create-web
  - follow-best-practice
  - follow-tool-maestro
  - implement-to-production
  - ask-me

---

## Goal

Dispatch to the skill matching the mobile target — the parent only routes

## Scope

- The argument is the domain; if omitted → use `/ask-me` to pick a domain

## Execute

### Target Skills

| Domain | Skill |
|---|---|
| `native`, `ios`, `android`, `kmp` | `/follow-create-ios-android-native-by-kotlin-multiplatform` — native iOS+Android with Kotlin Multiplatform |
| `cross-capacitor`, `capacitor` | `/follow-create-mobile-cross-with-capacitor` — web stack + Capacitor |

1. Run `/deep-research` + `/follow-best-practice` for the chosen platform, per the conventions in `/update-devin-global-skills` (done inside the dispatched target skill)
2. Determine the domain from the argument (e.g. `/follow-create-mobile ios`)
3. If the domain is supported → invoke the skill from the table and follow that skill's flow
4. If the domain is missing or unrecognized → use `/ask-me` to pick a domain

## Rules

- The parent only dispatches — never duplicate the target skill's workflow
- Choose native vs cross per the requirements — if unclear, ask the user first

- Use /follow-create-web if needed
- Use /follow-best-practice if needed
- Use /implement-to-production if needed
- Use /deep-test mobile to verify device/emulator flows after scaffolding

## Expected Outcome

- The caller is dispatched to the skill matching the platform and scaffolded via that flow
