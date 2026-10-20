---
description: Mobile-first UI — design for phones first; handle soft keyboard covering content
alwaysApply: true
---

# Mobile-first UI

This app is **mobile-first**. Design and build for a phone viewport first; desktop is a secondary stretch, not the default.

## Defaults

- Assume ~390px width, thumb reach, and one-handed use.
- Prefer full-width controls, large tap targets (~44px+), and bottom sheets over desktop modals/side panels.
- Stack vertically; avoid multi-column layouts unless they clearly degrade well on small screens.
- Use `text-base` (16px+) on inputs so iOS does not zoom on focus.
- Test mentally: one hand, portrait, notch/safe areas (`env(safe-area-inset-*)`).

## Soft keyboard (critical)

A focused input must never sit under the software keyboard — web or iOS.

### Web / PWA (Safari)

On iOS Safari/PWA the keyboard often covers fixed sheets, footers, and focused inputs. **Never ship overlays that trap content under the keyboard.**

When building sheets, dialogs, or any fixed bottom chrome with inputs:

1. Use [`useVisualViewportFrame`](src/hooks/use-visual-viewport-frame.ts) so the overlay tracks the _visual_ viewport, not `100dvh`.
2. Keep the primary action (Generate / Save / Submit) visible above the keyboard — shrink or hide secondary chrome when `keyboardOpen`.
3. Make the middle section scroll (`min-h-0 flex-1 overflow-y-auto`); pin header/footer.
4. Prefer `preventScroll` on focus when you manage viewport yourself.

```tsx
// ✅ Sheet pinned to visual viewport (see AiTemplateButton / AiSessionButton)
const { style, keyboardOpen } = useVisualViewportFrame(open);

<SheetContent style={style} className="flex flex-col …">
  <header className="shrink-0">…</header>
  <div className="min-h-0 flex-1 overflow-y-auto">…input…</div>
  <footer className="shrink-0">…primary CTA…</footer>
</SheetContent>;
```

```tsx
// ❌ Fixed sheet using only h-dvh / bottom-0 — keyboard covers the CTA
<SheetContent className="h-dvh">…</SheetContent>
```

### Expo / iOS app

`KeyboardProvider` is already at the root. Do not use RN's `KeyboardAvoidingView`
or `automaticallyAdjustKeyboardInsets` for new input screens.

- **Scrolling screens** — `Screen` uses `KeyboardAwareScroll`, which scrolls the
  caret into view (including multiline).
- **Sticky Finish/Save/Generate footers** — `KeyboardAwareFooterLayout` +
  `KeyboardStickyFooter`. The layout measures the footer and passes it as
  `bottomOffset` / `extraKeyboardSpace` so the caret clears both keyboard and
  footer.
- **Composer-style inputs** (comments) — put the field in `KeyboardStickyFooter`
  via `Screen`'s `footer` prop and set `keyboardMode="composer"`. This scrolls
  the content with the keyboard even though the focused input is outside the
  scroll view. Keep a height-limited composer internally scrollable.
- **Multiline notes** — keep `scrollEnabled={false}` on the `TextInput` so the
  parent scroll view follows the caret as the note grows.
- **Inputs in page sheets** — same primitives; a `Modal` still sits under the
  root `KeyboardProvider`.

```tsx
// ✅ Note / sheet with sticky CTA
<KeyboardAwareFooterLayout
  footer={<KeyboardStickyFooter>…Finish…</KeyboardStickyFooter>}
>
  {/* Multiline TextInput with scrollEnabled={false} so the parent follows the caret */}
  <WorkoutNoteField />
</KeyboardAwareFooterLayout>
```

```tsx
// ❌ ScrollView + fixed footer — keyboard covers the caret
<ScrollView automaticallyAdjustKeyboardInsets>…input…</ScrollView>
<View style={{ position: "absolute", bottom: 0 }}>Finish</View>
```

## Checklist before finishing UI

- [ ] Usable at ~390px without horizontal scroll
- [ ] Tap targets and spacing work with thumbs
- [ ] Focused inputs / sheet CTAs stay above the soft keyboard
- [ ] Safe-area padding on bottom bars and full-screen sheets
