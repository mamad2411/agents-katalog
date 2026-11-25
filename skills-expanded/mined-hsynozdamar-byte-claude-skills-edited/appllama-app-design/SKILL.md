---
name: appllama-app-design-skill
description: "Native-feeling mobile app screens in Expo / React Native only, not web. Use when building or improving native app screens with Apple HIG fidelity, Reanimated motion and simulator checks."
license: MIT
metadata:
  author: Appllama (appllama.io)
  version: 1.3.0
---


# Appllama App Design Skill

The screens you build sit next to the best-designed apps on a phone, and the user compares within seconds. This skill sets the bar and the method.

## Study before you draw

Every screen starts from research, not imagination. With the **Appllama MCP** connected, pull real screens for the category and screen type (playbooks in the `appllama-usage` skill) and study 10 to 30 before writing UI. Extract the pattern, not the pixels: layout skeleton, hierarchy, control choices, spacing rhythm, CTA position, what gets illustration versus plain text, how progress shows. Then design your own screen on the proven skeleton in your product's voice. Appllama media carries a small watermark top-left; it is provenance, so ignore it when reading a screen and keep it out of your build.

## Platform baseline

Defaults unless the project differs: Expo + Expo Router, React Native, TypeScript; `react-native-reanimated` + `react-native-gesture-handler`; FlashList for any list that can grow; `expo-image` (SF Symbols via `source="sf:name"`), `expo-video` / `expo-audio` (not `expo-av`); `react-native-safe-area-context` for insets; `process.env.EXPO_OS` over `Platform.OS`.

## Native fidelity laws

A deviation from these is a finding, not a style preference.

1. **Semantic colors, both themes, day one.** System tokens (`Color.ios.label`, `Color.ios.secondarySystemBackground`; Material dynamic colors on Android). A screen is done when light and dark both render right. Resolve semantic colors to strings before they enter Reanimated styles.
2. **Native controls.** Switch, Slider, SegmentedControl, context menus, date pickers use the native control or a faithful wrapper (wiring: `references/native-controls.md`).
3. **SF Symbols / Material Symbols** for icons (`expo-image` `sf:` or `expo-symbols`), one icon family per screen.
4. **Typography is hierarchy.** Platform type ramp (Large Title, Title, Headline, Body, Footnote), one display size per screen, `fontVariant: ['tabular-nums']` for counts, times and prices, `Text selectable` for copyable data.
5. **`borderCurve: 'continuous'`** on every rounded rectangle.
6. **Shadows via CSS `boxShadow`**, one elevation system per app.
7. **Spacing on one base unit (4 or 8)**, flexbox `gap` over margin stacking, ScrollView padding in `contentContainerStyle`.
8. **Safe areas are design.** Check content scrolled under the island and status bar (does the blur or fade hold), the bottom CTA clearing the home indicator, and landscape if supported.
9. **Navigation titles belong to the navigator**: the stack's native title and large-title collapse over a hand-rolled header.
10. **Haptics are punctuation.** Selection tick when a value passes a step, light impact when something snaps home, notification success or error for outcomes; same frame as the visual, one per action, never the only feedback, not on scroll or in loops.
11. **Format numbers like a product**: 1.4M, 38k, $4.99, trailing zeros trimmed, dates localized.
12. **Root scroll**: any screen that can overflow starts with a ScrollView using `contentInsetAdjustmentBehavior="automatic"`. Use `useWindowDimensions`, not `Dimensions.get()`.

## Navigation

Each transition answers: what is the destination, can the user come back, what does back (chevron, iOS edge swipe, Android hardware back) do afterwards.

- Push goes deeper; replace moves on; `router.dismissTo(href)` finishes a flow. Back undoes navigation, never events.
- Presentation is meaning: multi-step task is a `modal` with its own stack; short interruption is a `formSheet` with detents; immersive is `fullScreenModal` with Close; overlay on a visible screen is `transparentModal`; destructive confirm is an action sheet; share, web and photo picking use the system controller.
- One-way doors (sign-in on a wall app, finished onboarding, purchase, finished session) leave the stack via `Stack.Protected` + `replace`, and a feature-triggered sign-in or paywall returns to the feature, unlocked.
- Back is blocked only for an in-flight irreversible request and unsaved modal work (`usePreventRemove`).
- Tabs are peers; full-attention screens live above them; deep links land on a real stack; splash holds until session state resolves.

All six laws with their reasoning: [references/navigation.md](references/navigation.md). Load it before wiring any flow with modals, sheets, auth or paywalls.

## Anti-slop

Defaults unless the brand explicitly asks otherwise and you can say why it fits this product:

1. Palette, materials and layout come from the studied references; purple/indigo glow CTAs, glassmorphism on every card, mesh-gradient heroes, confetti and sparkles are the model's house style.
2. **One accent**, locked across every screen and spent on the primary action, active state and progress; neutrals carry the app.
3. **One grey family** (warm or cool).
4. **Shape lock**: one radius scale stated as a rule ("actions are pills, cards 16, inputs 8").
5. Icons from the symbol set; emoji only in chat-native or playful content, never in chrome.
6. **One label per intent** ("Get started" everywhere or "Start now" everywhere).
7. Emphasis within one typeface family (weight or italic).
8. **Ship full state cycles**: skeletons match the final layout, empty states are composed and say how to fill them, errors are inline and specific.
9. **Mechanical pre-flight** before the simulator pass: accent hues = 1, radii all from the scale, emoji in chrome = 0, gradients without brand reason = 0, duplicate labels = 0. A failed count is a fix.

## Motion

Decide in this order:

- **Frequency gate.** 100+ per day (tab switch, keyboard, scroll, back): platform default only. Tens per day (press, row select): under 150 ms. Occasional (sheets, modals, toasts): standard motion. Delight only for rare first-time moments. Tabs never slide. When unsure, delete the animation.
- **Name the purpose in one word** (feedback, spatial continuity, state change, explanation, delight) or skip it. Data being read never moves for style.
- **A finger involved means a spring**: start from the live value, pass release velocity in, target the projected momentum so a flick commits, rubber-band at boundaries, stay grabbable mid-flight. Vocabulary: `{ duration: 400, dampingRatio: 1 }` to settle, `{ 300, 0.8 }` for sheets; bounce only with gesture momentum.
- **Everything else is timing under 300 ms with strong ease-out** (`Easing.bezier(0.23, 1, 0.32, 1)`; no ease-in on entrances). Press-in feedback in 100 to 150 ms: scale 0.97 on buttons and cards, background highlight on list rows, opacity on bar buttons. Exits are faster than entrances; enter from `scale(0.95)` + fade; menus grow from their trigger.
- **UI thread only for gestures**: worklets + shared values, `scheduleOnRN` only at gesture end, `transform`/`opacity` only, no `entering` on recycled rows, header height never animates, keyboard tracking via `react-native-keyboard-controller`.
- **Reduce Motion**: spatial motion becomes cross-fades; native transitions stay the system's.
- Bar: 60 fps through the hero flow, measured on a **release build on the slowest supported device** (Expo Go and dev builds hide jank; method in `references/performance.md`).

## State and perceived performance

- Server state in TanStack Query (no `useEffect` + `fetch`); client state in a small atomic store (Zustand/Jotai); ephemeral UI state stays in the component.
- Optimistic by default: reflect taps instantly, reconcile in the background, roll back loudly on failure.
- Uncontrolled `TextInput` for high-frequency typing; MMKV over AsyncStorage when latency shows.
- Skeletons only for content of known shape, never a full-screen spinner for a partial update; FlashList with stable keys; preload next-screen data on press-in; `expo-image` with `recyclingKey` and thumbhash placeholders.
- Cold start and bundle: measure, optimize, re-measure (`references/performance.md`), no blind memoization.

## Image and illustration assets

Generate with the best image model available at its highest quality, then downscale to @1x/@2x/@3x (never upscale). One visual language per app (gradient-mesh, flat-duotone, 3D-clay, hand-drawn, mascot), same palette and lighting for all assets. Prompt for transparent or solid-flat backgrounds matched to the surface; white halos or wrong mattes mean a redo. Pipeline and prompt patterns: [references/image-assets.md](references/image-assets.md).

## Simulator loop

A screen does not exist until you have seen it running.

1. Implement, launch in the iOS Simulator (or Android emulator).
2. Screenshot and look: alignment, optical centering, rhythm, truncation with long content, dark mode, Dynamic Type XL.
3. Run the full-motion pass: screen-record the whole flow (`xcrun simctl io booted recordVideo flow.mov`), watch once at speed and once frame by frame for dropped frames, one-frame flashes of wrong theme or unstyled paint, layout jumps and springs that clip. Screenshots prove layout, not motion. The checklist of what to exercise is in [references/simulator-loop.md](references/simulator-loop.md).
4. Fix, relaunch, re-verify until no defect shows at 100% zoom, then run that checklist once more.

## Definition of done, per screen

- [ ] 10+ real reference screens studied; the adopted pattern is nameable
- [ ] Navigation answered: push / modal / sheet / overlay / replace, back on iOS and Android, no re-entry past a one-way door
- [ ] Light and dark verified in the simulator; safe areas, island and home indicator verified
- [ ] Long-content, empty, loading and error states designed
- [ ] Full flow recorded and scrubbed, zero glitch frames; Reduce Motion respected; 60 fps on a release build
- [ ] Dynamic Type XL holds; tap targets 44pt or more; contrast passes in both themes
- [ ] Assets in one style family, crisp at @3x
- [ ] Lists virtualized, no controlled-input jank, no re-render storms (profiled)

## References

| File | Load when |
|---|---|
| [references/navigation.md](references/navigation.md) | Push/modal/sheet/replace choices, auth and paywall flows, back behavior, tabs, deep links |
| [references/native-controls.md](references/native-controls.md) | Choosing/wiring iOS+Android native controls, menus, pickers, sheets |
| [references/motion.md](references/motion.md) | Any Reanimated work: gestures, transitions, springs, layout animations |
| [references/performance.md](references/performance.md) | Jank, slow TTI, big bundles, memory leaks, profiling method |
| [references/image-assets.md](references/image-assets.md) | Generating illustrations/icons/hero art with image models |
| [references/simulator-loop.md](references/simulator-loop.md) | Final verification checklist, device matrix, full-motion pass |
