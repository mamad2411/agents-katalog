---
name: apple-hig-ux
description: >-
  Apple-platform design and UX judgment — what a good iOS/iPadOS/macOS/watchOS/visionOS
  app FEELS like. Use whenever designing app screens or flows, answering Human Interface
  Guidelines (HIG) questions, judging "does this feel native", running a UX review of an
  Apple-platform app, choosing navigation patterns (tabs vs hierarchy vs modal), designing
  onboarding, empty states, settings, or paywalls, doing accessibility audits, designing
  app icons or launch screens, handling dark mode, Liquid Glass adoption, typography,
  color, spacing, haptics, or UX copy. Trigger BEFORE writing SwiftUI for any new screen —
  design decisions come first. Complements swiftui-max (implementation) and app-review-max
  (App Store review); this skill owns design/UX judgment only.
---

# Apple HIG & UX Judgment

You are acting as a senior Apple-platform product designer. Give opinions, not menus of
options. Every recommendation must answer: does this make the app feel like it belongs on
the platform? Cite concrete numbers (points, ratios, durations) — vagueness is a bug.

Division of labor: this skill decides *what the screen should be*. `swiftui-max` decides
*how to build it*. `app-review-max` decides *whether Apple will approve it*.

## Non-negotiable principles

1. **Content first, chrome second.** Controls and navigation float above content
   (Liquid Glass layer); content owns the screen. If chrome competes with content, cut chrome.
2. **Deference to the system.** System fonts, semantic colors, standard components, standard
   gestures. Custom is a budget you spend on the one thing that differentiates the app.
3. **Direct manipulation.** Users touch the thing itself, not a proxy. Prefer swipe actions,
   drag, and context menus over edit modes and toolbars full of buttons.
4. **Forgiveness.** Every action is undoable, cancelable, or confirmed only when destructive.
   Never confirm non-destructive actions.
5. **Consistency beats novelty.** A user's muscle memory from Mail, Notes, and Settings is
   free training. Break it only with a measurable payoff.

## Platform idiom decision table

Do not ship the same layout on every platform. The differences below are the product.

| Dimension | iOS | iPadOS | macOS | watchOS | visionOS |
|---|---|---|---|---|---|
| Primary input | One thumb, touch | Touch + Pencil + keyboard/trackpad | Pointer + keyboard | Digital Crown + tap | Eyes + hand pinch |
| Root navigation | Tab bar (2–5 tabs) | Tab bar that adapts to sidebar (`.sidebarAdaptable`) | Sidebar + toolbar; menu bar always | Vertical scroll or page-based; NavigationStack | Tab bar floats left (ornament); sidebar inside window |
| Window model | One full screen | Multiple scenes, Split View, Stage Manager | Many resizable windows | One screen at a time | Windows + volumes + spaces |
| Density | Low; 44pt rows | Medium; multi-column | High; 24–28pt rows, disclosure | Very low; 1–3 items visible | Low; oversized, generous spacing |
| Menus | Context menu (long-press) | Context menu + menu bar (hardware keyboard) | Menu bar is MANDATORY, every command in it | Nearly none | Context menu (pinch-hold) |
| Keyboard shortcuts | Optional | Expected with hardware keyboard | Mandatory for every frequent command | N/A | Optional |
| Settings | In-app screen (gear/tab) | Same | Settings window (⌘,) | Watch app + phone companion | In-app window |
| Session length | Seconds–minutes | Minutes–hours | Hours | 2–10 seconds | Minutes–hours |

Hard rules: an iPad app that is a stretched iPhone app is a defect — use
`NavigationSplitView`, support all Split View widths, add keyboard shortcuts. A macOS app
without a complete menu bar and ⌘-shortcuts is a defect. A watchOS design with more than
one task per screen is a defect — design for the 5-second glance.

## Navigation pattern selection

Pick ONE primary structure; don't mix tab bar + hamburger, ever.

| Pattern | Use when | Don't use when |
|---|---|---|
| **Tab bar** (`TabView`) | 2–5 peer top-level areas users switch between often. Tabs are always visible, state preserved per tab. | You have 6+ areas (cut or merge — a "More" tab is a design failure), or areas are sequential steps. |
| **Hierarchy** (`NavigationStack` push) | Drilling into content: list → detail → sub-detail. User goes deeper into ONE area. | Moving between peer areas (that's tabs) or interrupting for a task (that's modal). |
| **Sheet (modal)** | A self-contained task that starts and ends: compose, edit, filter, add item. Must have explicit Done/Cancel or obvious swipe-dismiss. | Displaying content the user will read/browse — content belongs in the hierarchy. Never stack sheets more than 2 deep. |
| **Full-screen cover** | Immersive interruptions: camera, media playback, onboarding, paywalls. | Anything the user should be able to peek behind. |
| **Popover** (iPad/macOS) | Lightweight options anchored to a control. On iPhone it becomes a sheet — design for both. | Primary content or multi-step tasks. |
| **Confirmation dialog** | Confirming a just-initiated action, esp. destructive. | Presenting new tasks or more than ~4 choices. |
| **Alert** | Something went wrong or data will be lost. Rare by design. | Marketing, ratings begging, non-critical info. |

Rules of thumb: navigation depth ≤ 3 taps to any content; swipe-back must always work
(don't hijack the left screen edge); modality means the user *chose* to be interrupted —
the app never self-interrupts except for data loss. Search: give it its own tab with
`Tab(role: .search)` when search is a primary behavior; otherwise `.searchable` on the
relevant list.

## Liquid Glass (current design language)

Baseline: iOS/iPadOS/macOS/tvOS/watchOS 26 (shipped 2025). Verified against the HIG
Materials page (updated Sept 2025) and June 2026 guidance.

- **Two layers, strictly.** Liquid Glass is the *functional* layer — tab bars, toolbars,
  sidebars, buttons — floating above the *content* layer. Never apply Liquid Glass inside
  the content layer (app backgrounds, cells, cards). Content uses standard materials
  (`ultraThin`/`thin`/`regular`/`thick`).
- **Use effects sparingly.** System components adopt glass automatically. Custom
  `glassEffect` is reserved for the few most important custom controls; glassy everything
  reads as a theme-park skin, not native.
- **Regular vs clear variant.** Regular (default) blurs and adapts luminosity — use for
  anything text-heavy (sidebars, alerts, popovers). Clear is highly translucent — ONLY over
  visually rich media (photo/video). Over bright media, add a ~35 %-opacity dark dimming
  layer behind clear glass for legibility.
- **Let content flow under bars.** Scroll edge effects handle legibility at bar boundaries;
  don't paint opaque rectangles behind toolbars.
- **Concentric geometry.** Corner radii of nested elements share a center with the
  container/device bezel. Misaligned radii are one of the fastest "off" tells.
- **It adapts without you.** Glass responds to Reduce Transparency, Increase Contrast, and
  (beta, iOS 27) a user-facing transparency slider. Never hand-tune colors to look right at
  one transparency level.
- **Beta (iOS/iPadOS/macOS 27, announced WWDC26, ships fall 2026):** reduced default
  transparency; user opacity slider ("ultra clear" → fully tinted); sharper icon rendering
  with per-layer refraction; search button re-integrated into the tab bar (reverses the
  iOS 26 separate bottom-corner placement); adjusted sidebar corner radii on iPadOS/macOS.
  Design so the layout survives both iOS 26 and 27 rendering.

## Typography

- **System fonts only** unless brand display type is the product: SF Pro (iOS/iPadOS/macOS),
  SF Compact (watchOS), New York for editorial serif. Custom body fonts must support
  Dynamic Type or don't ship.
- **Use text styles, never fixed sizes.** iOS defaults (Large setting):

| Style | Size/Leading (pt) | Use for |
|---|---|---|
| Large Title | 34/41 | Screen title at scroll top |
| Title 1 / 2 / 3 | 28 / 22 / 20 | Section-level headers |
| Headline | 17/22 semibold | Cell titles, emphasis |
| Body | 17/22 | Default reading text |
| Callout | 16/21 | Secondary content |
| Subheadline | 15/20 | Cell subtitles |
| Footnote | 13/18 | Attributions, metadata |
| Caption 1 / 2 | 12 / 11 | Labels, timestamps |

- macOS body is 13pt; watchOS body 14–16pt by device; tvOS body 29pt (10-foot viewing).
  Don't port point sizes across platforms — use each platform's text styles.
- Minimum text size 11pt on iOS; nothing under Caption 2. Line length: aim 45–75 characters;
  use readable content margins on iPad/Mac.
- Hierarchy via weight and size, not color alone. Two weights per screen is usually enough.

## Color, materials, dark mode

- **Semantic colors only:** `.primary`, `.secondary`, `Color(.systemBackground)`,
  `.secondarySystemBackground`, system accent colors. Hardcoded hex breaks dark mode,
  Increase Contrast, and vibrancy — automatically un-native.
- **One accent color.** Interactive elements share the app tint; color = "you can tap me."
  Never use the tint color on non-interactive text.
- **Dark mode is a distinct palette, not inverted.** Base/elevated background pairs create
  depth (pure black `#000` base on OLED is fine; elevated surfaces lighten). Desaturate
  brand colors slightly in dark; test both modes at every design review, not at the end.
- **Vibrant colors on materials.** On any material/glass, use system vibrancy label styles,
  never fixed grays (contrast collapses).
- Never encode meaning in color alone (add icon/label — 8 % of men are color-blind).
- Contrast: ≥ 4.5:1 body text, ≥ 3:1 for text ≥ 17pt bold / ≥ 18pt regular and for
  essential UI shapes. Details in `references/accessibility.md`.

## Touch targets & spacing

| Number | Rule |
|---|---|
| **44×44pt** | Minimum hit region, iOS/iPadOS/watchOS — even if the glyph is smaller |
| **60×60pt** | Minimum hit region in visionOS (eye targeting); center glyphs in it |
| **28pt** | Typical macOS control height; pointer allows density, don't import 44pt rows |
| **8pt grid** | All spacing in multiples of 8 (4 for fine detail) |
| **≥ 8pt** | Minimum gap between adjacent tappable elements |
| **16pt / 20pt** | Standard layout margins, compact / regular width |
| **44pt** | Minimum list row height |
| Bottom third | Primary actions on iPhone live in thumb reach; top corners are expensive |

Respect safe areas always; content scrolls under bars but controls never hide behind the
home indicator or Dynamic Island.

## Haptics vocabulary (iOS)

Haptics confirm *meaning*, not taps. The system already plays haptics for standard controls
— add your own only for app-specific moments, synced to the animation frame.

| Feedback | Meaning | Example |
|---|---|---|
| `.success` | Task completed | Order placed, upload done |
| `.warning` | Attention, not failure | Approaching a limit |
| `.error` | Action failed | Invalid card, sync failed |
| `.selection` | Value ticked | Picker wheel, segmented drag |
| `.impact` light→heavy / soft / rigid | Physical collision | Drag snap, pull-to-refresh threshold |

Rules: never fire haptics on every scroll tick or button (fatigue → users disable them);
one haptic per event; pair with sound/animation. SwiftUI: `.sensoryFeedback(_:trigger:)`.

## UX writing

- **Buttons are verbs stating the outcome:** "Delete Draft", "Start Trial", "Save Changes" —
  never "OK", "Yes", "Submit", "Continue" on a destructive or ambiguous choice.
- Title Case for buttons/titles/nav; sentence case for body, descriptions, options.
- **Alert anatomy:** title = what happened (no "Error", no "Oops"); message = why + what to
  do; buttons = the actual choices. Cancel on the left/bottom, preferred action bold,
  destructive red and never the default.
- **Error messages:** state what failed, whose fault it isn't, and the next step.
  "Couldn't save your note. Check your connection and try again." Not "An unexpected error
  occurred (code -34)."
- No "please", no "sorry", no exclamation marks, no blaming ("invalid input"). Second
  person ("your notes"), present tense, front-load the key word.
- Empty states sell the action, not the emptiness: "Scan your first receipt" beats
  "No data found."
- Numerals over words ("3 items"); avoid truncation at largest Dynamic Type before cutting copy.

## Un-native smells checklist

Run this list during any UX review; each hit is a "web/Android port" tell:

- [ ] Hamburger menu on iOS instead of tabs; FAB; Material ripple; snackbars/toasts
- [ ] Custom back button, or edge-swipe-back broken/hijacked
- [ ] Fixed font sizes — layout explodes (or ignores) larger Dynamic Type
- [ ] Hardcoded colors; dark mode inverted or missing; text on images with no scrim
- [ ] "Submit"/"OK"/"Yes/No" buttons; alert used for marketing or rating begging
- [ ] Login/signup wall before showing any value; forced onboarding carousel > 3 screens
- [ ] Splash screen with logo animation or spinner (launch screen must mirror first screen)
- [ ] No pull-to-refresh on feeds; no swipe actions on list rows; no context menus
- [ ] Custom alert/dialog lookalikes; custom share icon instead of the system share sheet
- [ ] Opaque rectangles behind bars; content doesn't scroll under toolbars; ignored safe areas
- [ ] Buttons without pressed/disabled states; no haptics where system apps would have them
- [ ] iPad = stretched iPhone; macOS = ported iPad app with no menu bar or shortcuts
- [ ] Settings screen re-implements a website account page; in-app browser for core flows
- [ ] Loading spinners where skeletons/`redacted` or cached content should appear
- [ ] Everything animated, or nothing — no restraint hierarchy (see haptics rules: same logic)

## Reference files

| File | Read when |
|---|---|
| `references/accessibility.md` | VoiceOver semantics, Dynamic Type discipline, contrast, Reduce Motion, audit workflow, Assistive Access |
| `references/patterns-by-screen.md` | Designing onboarding, settings, paywalls, empty/error/offline states, search, lists vs grids |
| `references/app-icons-and-branding.md` | App icons (layered/Icon Composer, dark/clear/tinted variants), launch screens, branding restraint |

## Companions & orchestration

Part of the swift-tothemax plugin — `apple-dev-conductor` routes multi-facet tasks. Siblings: `swiftui-max` implements what this skill specifies; `app-review-max` covers design-related rejections (guideline 4.x) — flag apps that fail the un-native smells checklist to it before submission.
Ecosystem companion: `apple-hig` (nexu-io) for supplementary HIG lookups if installed. This skill's iOS 27/Liquid Glass guidance is newer; prefer it on conflicts.
