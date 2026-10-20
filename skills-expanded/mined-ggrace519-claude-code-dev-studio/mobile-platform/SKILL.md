---
name: mobile-platform
description: Platform conventions and native integration specialist. Auto-invoked when platform-specific UI, navigation, permissions, or OS-integration code is written — HIG/Material adherence, share sheets, widgets, intents, App Clips, Siri/App Shortcuts.
---

# Mobile Platform Conventions

Platform-idiomatic behavior — navigation, permissions, OS integrations — is
what makes an app feel native instead of ported. Users can't name the
convention being violated, but they uninstall over it anyway.

## When to reach for this

- Building platform-specific UI/navigation and deciding how far cross-platform
  code should bend toward each OS's conventions (HIG vs Material 3)
- Adding a runtime permission request, or recovering from permission denials
- Wiring OS integrations: share sheet, widgets, shortcuts, Live Activities,
  App Clips / Instant Apps, deep links
- Dark mode, Dynamic Type / font scaling, and system-theme adherence work

## Principles

1. **Feel native on both.** Shared UI is fine; shared *navigation and gesture
   language* is not. Back gesture and predictive back on Android, edge-swipe
   pop and large titles on iOS — respect each platform's spine even in
   Flutter/React Native.
2. **Ask for permissions in context, never at cold start.** Request when the
   user taps the feature that needs it, after a one-line explanation. On iOS
   the system prompt is effectively one-shot — a denial means a trip to
   Settings — so a pre-prompt that gauges intent before burning the real prompt
   pays for itself. On Android, show rationale when
   `shouldShowRequestPermissionRationale` says so; after repeated denials the
   dialog stops appearing and Settings is the only path.
3. **Request the narrowest permission that works.** Photo picker instead of
   gallery access, approximate before fine location, `When In Use` before
   `Always` — narrower scopes get higher grant rates and easier store review.
4. **Deep links are an attack surface.** Every inbound URL/intent is untrusted
   input: validate the route, authenticate before acting, never execute
   side effects from query params. Verify ownership properly — Universal Links
   via `apple-app-site-association`, Android App Links via `assetlinks.json` —
   or another app can claim your scheme.
5. **Dynamic Type to the accessibility sizes.** Layouts must survive the large
   accessibility text sizes (truncation ≠ surviving) and Android font scale —
   test at the extremes, not at 100%.
6. **Theme honesty.** Supporting dark mode means every screen, web view, splash,
   and notification icon — a half-dark app reads as broken, not partial.

## Permission-request checklist

- [ ] Triggered by a user action that obviously needs it (map tap → location)
- [ ] Pre-prompt or inline rationale states the *user benefit*, not "we need access"
- [ ] Narrowest scope requested (picker / approximate / when-in-use)
- [ ] Denied path is functional: feature degrades gracefully + a "enable in Settings" deep link
- [ ] Permanently-denied state detected and handled (no re-prompt loop)
- [ ] Usage-description strings (`Info.plist`) / manifest declarations match what the code does
- [ ] New permission flagged for store privacy declarations (see `mobile-release`)

## Pitfalls

- The permission "double prompt" anti-pattern done badly: a pre-prompt that
  *replaces* context instead of adding it, trained users to tap "no"
- Hardcoded colors that break dark mode (use semantic/dynamic colors)
- Fixed-height text containers that clip at accessibility font sizes
- Deep link handlers that navigate before auth state is restored, dumping users
  on a login screen and losing the destination
- iOS-style back chevrons and modals on Android (or system-back ignored) —
  the single most-reported "feels off" issue in cross-platform apps
- Widgets/Live Activities that fetch on their own schedule and blow the
  process's background budget

---
*Related: `mobile-release` (privacy declarations for new permissions),
`common-notifications` (notification permission timing and UX), `mobile-perf`
(integration cost on startup) · domain agent: `mobile-architect` · output/ADR
format: `playbook-conventions`*
