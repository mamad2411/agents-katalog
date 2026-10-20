# Expo HAS CHANGED

Read the exact versioned docs at https://docs.expo.dev/versions/v57.0.0/ before writing any code.

# RTL and LTR

The app runs Hebrew (RTL) and English (LTR), on a phone set to either language. Write every
screen once, in start/end terms, and let React Native mirror it:

- Direction is decided in ONE place: `src/i18n/direction.ts` (`applyLayoutDirection`, called by the
  preferences provider). It pins both `allowRTL` and `forceRTL` to the app language and restarts
  when the running layout disagrees. Never call `I18nManager.forceRTL`/`allowRTL` anywhere else, and
  never set expo-localization's `supportsRTL`/`forcesRTL` in app.json -- on iOS that rewrites the
  flag from the DEVICE language on every launch.
- `flexDirection: 'row'` already runs right-to-left in Hebrew. Never pick `row-reverse` by language.
- Use `marginStart`/`marginEnd`, `paddingStart`/`paddingEnd`, `start`/`end`, `borderStartWidth`.
  Physical `left`/`right` are only for things that are physical (a point on a map) or symmetric.
- Text alignment: `ThemedText` already starts text at the line's start. For a raw `<Text>` use
  `TEXT_ALIGN_START`, for `<TextInput>` use `INPUT_ALIGN_START`. Never `isRTL ? 'right' : 'left'` --
  React Native already treats `left` as start on `<Text>`, so that mirrors twice.
- Arrows and chevrons come from `src/components/directional-icon.tsx`, never a `scaleX: -1` flip.
- A lint rule (`eslint.config.js`) enforces the above; check new screens in both languages.

# Inline rows, no cards, no shadows

The visual language is flat and card-less: a white page, content sitting directly on it as
inline rows, and `Hairline` (`src/components/hairline.tsx`) between rows in a list. Do not
wrap a list item in a filled, rounded container to set it apart -- that is the card pattern
this app deliberately does not use. Whitespace and a section heading separate SECTIONS;
hairlines separate ROWS within one.

Three colour roles, and reaching for the wrong one is the usual mistake:

- `background` -- the page. Also every panel docked over a map (a map is its own background,
  so nothing over it can be card-less), every bottom sheet, and the ink drawn on a
  `text`-coloured fill, which is why it inverts with the theme.
- `surface` -- all but retired. The controls that used to wear this tint are outlined now
  (below); what is left is the grey stand-in a web build shows where a map would be.
- `borderMuted` -- hairlines between rows, and the outline of a panel.
- `borderControl` -- the edge of a CONTROL, a full step stronger than `borderMuted`. A
  divider should not shout; an edge has to hold its shape against a white page.

Every control -- search field, chip, filter, segmented track, icon circle, departure pill,
the map button -- is `background` with an outline, never a fill: spread `useControlOutline()`
(`hooks/use-theme`) into its style array, which pairs `borderControl` with
`ControlBorderWidth`. Call it at the top of the component, not inline in the style array:
several of these render after an early return, and a hook below one breaks the rules of
hooks. A control that is SELECTED inverts to a `text` fill and drops the outline -- a filled
chip with an edge reads as two states at once.

The one rounded block in the app is the smart-suggestion hero, and only because it holds a
map, which has to be clipped to an edge.

The vertical rhythm, loosest to tightest -- with no card edges, this spacing IS the
structure, so use these three and nothing in between:

- `SectionGap` (48, from `constants/theme`) between two top-level sections of a page.
- `Spacing.four` (24) inside a cluster of controls (a title over its field over its
  filters), and as the page's horizontal inset on EVERY screen.
- `Spacing.three` (16) from a section heading to the rows under it.

Two exceptions, both deliberate. A long list you scan (lines, stations, the pickers) keeps
`Spacing.three` row padding where the short home lists use `Spacing.four` -- at 24 a
catalogue becomes one row per thumb-scroll. And a bottom sheet over a map is not a page:
its peek is all the rider sees at rest, so its blocks sit `Spacing.four` apart, never
`SectionGap`.

When a section's rows live inside a `gap`-ed column, wrap the rows in their own plain
`View`. The column's gap otherwise lands between every row AND every hairline, which
silently doubles the row padding.

No shadows anywhere. Never add `shadowColor`/`shadowOffset`/`shadowOpacity`/`shadowRadius`,
`elevation`, or web `boxShadow`/`box-shadow`/`filter: drop-shadow(...)` to any component or
style. A surface reads from its background color and border alone, not elevation.

# Haptics

Every haptic goes through `src/lib/haptics.ts`, whose functions are named for what just
happened (`hapticGestureRecognised`, `hapticSettled`, `hapticSelected`, `hapticSucceeded`,
`hapticWarned`) rather than for the waveform. Never import `expo-haptics` at a call site --
the vocabulary is what lets the whole app be re-tuned from one file.

Add one only for a moment with NO immediate visual, or one the rider may not be looking at:
a long press before its sheet appears, the map pin landing, a selection changing, the
get-off alarm. Ordinary taps -- a chip, a row, a result, a tab -- answer themselves on
screen, and an app where everything buzzes is one where nothing means anything. For a
toggle, fire only on a real change: re-picking the option already chosen is a no-op, and
buzzing there teaches that the tap means nothing.

`alertSettings.vibrate` gates exactly ONE of them, the get-off alert, because that switch is
the rider's answer about the alarm and not about interface feedback. iOS already honours the
system-level haptics setting, so there is no app-level one.

Every call is fire-and-forget and swallows its error: a device with no Taptic Engine, or a
binary without the native module, must fall through to the action itself in silence.
`expo-haptics` is NATIVE -- adding or changing it needs a new EAS build and cannot ship over
the air.
