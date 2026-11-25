---
name: rtl-bidirectional-ui
description: Build UX-correct bidirectional (LTR/RTL) interfaces in React Native — Arabic-first apps, mirrored layouts, horizontal carousels, directional icons, and text alignment.
---

<!-- Reference: React Native docs, Arabic UX conventions, production app patterns -->

# RTL & Bidirectional UI

Apply when building any screen, component, or scroll list in an app that supports both Arabic (RTL) and English (LTR). For apps where Arabic is the primary language, treat RTL as the default and verify LTR as the secondary case.

## When to apply

- Any horizontal layout with left/right positioning
- Horizontal scroll lists, carousels, or peek effects
- Icons that communicate direction (arrows, chevrons, progress)
- Text alignment, padding, margin, or absolute positioning
- Any hardcoded `"left"` or `"right"` value in styles

---

## Core Principles

### 1. Arabic-first mental model

If your app's main language is Arabic, design the RTL layout first and verify LTR second. Do not design for LTR and try to mirror it — the RTL layout will feel like an afterthought.

---

### 2. Use logical (direction-aware) style properties

Always prefer logical properties over physical ones. Physical properties (`left`, `right`, `marginLeft`, `paddingRight`) never flip — logical ones do.

| Physical (avoid) | Logical (prefer) |
|---|---|
| `marginLeft` | `marginStart` |
| `marginRight` | `marginEnd` |
| `paddingLeft` | `paddingStart` |
| `paddingRight` | `paddingEnd` |
| `left: 0` (absolute) | `start: 0` |
| `right: 0` (absolute) | `end: 0` |
| `textAlign: "left"` | `textAlign: align` from `getTextAlign()` |

---

### 3. Direction cascading — understand what you set

In React Native, setting `direction: "rtl"` on a parent **cascades to all children**. This means:
- A child `View` with `flexDirection: "row"` will lay out right-to-left.
- A child `View` with `flexDirection: "row-reverse"` will lay out left-to-right (double reversal — wrong).

**The trap**: setting `direction: "rtl"` on a FlatList and then `flexDirection: "row-reverse"` on a child card produces LTR order. Double reversal cancels out.

**The fix**: if you set `direction` on a parent, add `direction: "ltr"` on child components that control their own layout via `flexDirection`. This isolates them from the cascade.

```tsx
// FlatList has direction: "rtl"
<FlatList style={{ direction: "rtl" }} ... />

// Card must isolate itself — otherwise it inherits parent direction
// and flexDirection: "row-reverse" double-reverses back to LTR (wrong)
<TouchableOpacity style={{ direction: "ltr", flexDirection: isRTL ? "row-reverse" : "row" }}>
  <LogoBox />  {/* logo on right in RTL, left in LTR */}
  <InfoText />
</TouchableOpacity>
```

---

### 4. Horizontal carousels in RTL — use the `scaleX: -1` mirror trick

Setting `direction: "rtl"` on a horizontal `FlatList` changes item layout order but does **not** reliably flip scroll physics on all platforms. The safe, cross-platform approach is the **mirror flip**:

1. Apply `transform: [{ scaleX: -1 }]` to the `FlatList`.
2. Apply `transform: [{ scaleX: -1 }]` to each card/item.

**Why it works:**
- The FlatList stays physically LTR. All offset math, `snapToInterval`, `getItemLayout`, and `scrollToIndex` work unchanged.
- Visually the list is mirrored: item 0 appears on the right, higher indices extend to the left. Correct RTL carousel order.
- Touch/swipe events are mirrored too: physically swiping left = visually swiping right → "next" in the underlying LTR scroll = "next in Arabic" visually. ✓
- The two `scaleX: -1` transforms cancel out inside each card — text, images, and logos render normally.

```tsx
// FlatList: mirror the scroll area in RTL, no direction prop needed
<FlatList
  style={isRTL ? { transform: [{ scaleX: -1 }] } : undefined}
  snapToInterval={ITEM_STRIDE}
  snapToAlignment="start"
/>

// Card: counter-mirror so content is not rendered backwards
<TouchableOpacity
  style={[
    styles.card,
    { direction: "ltr" },
    isRTL ? { transform: [{ scaleX: -1 }] } : null,
  ]}
>
  {/* flexDirection: "row-reverse" → logo on right in RTL after double-flip cancels */}
  <LogoBox />
  <InfoText />
</TouchableOpacity>
```

| Mode | Logo position | Peek side | Scroll direction |
|---|---|---|---|
| LTR | Left | Right | Left → Right |
| RTL | Right | Left | Right → Left |

---

### 5. `getItemLayout` must include the content's leading padding

For `scrollToIndex` to land at the correct pixel, `getItemLayout.offset` must include the content's leading padding (`paddingHorizontal` in `contentContainerStyle`). Without it, every programmatic scroll arrives `paddingHorizontal` pixels short.

```tsx
const SIDE_PAD = theme.spacing.lg; // must match contentContainerStyle.paddingHorizontal
const ITEM_STRIDE = cardWidth + CARD_GAP;

const getItemLayout = useCallback(
  (_: unknown, index: number) => ({
    length: ITEM_STRIDE,
    offset: SIDE_PAD + ITEM_STRIDE * index, // include leading padding
    index,
  }),
  [ITEM_STRIDE],
);
```

---

### 6. Peek carousel sizing

For a "peek" carousel that shows the next card edge to invite scrolling:
- **LTR**: card starts at left edge (side padding), next card peeks on the **right**.
- **RTL**: card starts at right edge (side padding), next card peeks on the **left**.

Card width at **62–68% of screen width** gives a satisfying ~30–38% peek. Wider than 78% = too little peek; narrower than 55% = feels unstable.

---

### 7. Directional icons must flip

Icons that communicate direction must mirror in RTL. Icons with no directional meaning must not.

```tsx
// Back arrow, forward chevron — flip in RTL
const backStyle = isRTL ? { transform: [{ scaleX: -1 }] } : {};
const forwardStyle = isRTL ? { transform: [{ scaleX: -1 }] } : {};

// Shopping cart, star, avatar, logo — do NOT flip
```

---

### 8. Text alignment and writing direction

Never hardcode `textAlign: "left"` or `"right"`. Always use direction helpers:

```tsx
import { getTextAlign, getWritingDirection } from "@/utils/rtl";

<Text style={{ textAlign: getTextAlign(), writingDirection: getWritingDirection() }}>
  {content}
</Text>
```

---

### 9. RTL-aware absolute positioning

Physical `left`/`right` never flips. Use logical helpers:

```tsx
// Notification badge on the trailing corner of an avatar
<View style={[styles.badge, getPositionEnd(4)]} />
// LTR → { right: 4 }   RTL → { left: 4 }
```

---

### 10. Hooks cannot be called inside FlatList renderItem

`renderItem` is a callback, not a component. Calling `useState`, `useRef`, or any hook inside it violates the Rules of Hooks and causes a crash. Extract each card into a named `React.FC` so it can own its own state.

```tsx
// ❌ Crashes
const renderItem = ({ item }) => {
  const [failed, setFailed] = useState(false); // hook in a callback
  ...
};

// ✅ Correct
const StoreCard: React.FC<{ item: Store }> = ({ item }) => {
  const [failed, setFailed] = useState(false); // hook in a component
  ...
};
const renderItem = ({ item }) => <StoreCard item={item} />;
```

---

## Checklist

- [ ] No hardcoded `marginLeft` / `marginRight` / `paddingLeft` / `paddingRight` — use `Start`/`End` variants
- [ ] No hardcoded `textAlign: "left"` or `"right"` — use `getTextAlign()`
- [ ] `direction: "ltr"` added to child components that are isolated from a parent RTL direction
- [ ] Horizontal `FlatList` carousels in RTL use `scaleX: -1` on both the list and each item
- [ ] `getItemLayout.offset` includes the content's leading padding
- [ ] Directional icons (arrows, chevrons) flip in RTL; decorative icons do not
- [ ] Absolute-positioned elements use `getPositionEnd` / `getPositionStart`, not physical `left`/`right`
- [ ] Both `ar/` and `en/` locale files are updated together — never one without the other
- [ ] Tested visually in both RTL and LTR modes

---

## Anti-Patterns

- **Designing LTR first** when Arabic is the primary language — RTL will feel bolted on.
- **`direction: "rtl"` on parent + `flexDirection: "row-reverse"` on child** — double reversal produces LTR (wrong).
- **`direction: "rtl"` on a horizontal FlatList** — scroll physics do not reliably flip on Android; use `scaleX: -1`.
- **`getItemLayout` offset without leading padding** — `scrollToIndex` lands at the wrong position, animation appears misaligned with snapping.
- **Hardcoded physical `left`/`right`/`marginLeft`/`paddingRight`** — breaks when language switches.
- **Flipping symmetric or decorative icons** (carts, stars, avatars) — looks broken.
- **Separate LTR/RTL code branches** — diverge over time and introduce inconsistencies. One layout that adapts via helpers is always better.
- **`useState` inside `renderItem`** — causes "Invalid hook call" crash; always extract to a named component.
