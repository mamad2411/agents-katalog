---
name: chatbox-layout-patterns
description: CSS and React patterns for building WhatsApp-style chat interfaces with pinned input, bottom-anchored messages, scroll management, and streaming support. Covers the CSSence double-reverse pattern, min-h-0 grid/flex fixes, h-dvh viewport locking, and mobile adaptations.
triggers:
  - chat layout
  - chatbox
  - chat scroll
  - WhatsApp chat
  - messages scroll bottom
  - input pinned bottom
  - column-reverse
  - scroll anchor
  - chat streaming
  - typing indicator
---

# Chatbox Layout Patterns

CSS and React patterns for building WhatsApp-style chat interfaces with pinned input, bottom-anchored messages, and streaming support.

## The Core Problem

A chat UI needs five behaviors simultaneously:
1. Messages start at the **bottom** when few (like WhatsApp's first messages)
2. Messages **scroll up** as they accumulate, with the scrollbar tracking
3. The input box is **always pinned** at the bottom of the viewport
4. New messages and streaming content keep the scrollbar **stuck at the bottom**
5. On mobile, the viewport height adapts to the **virtual keyboard**

## Architecture: The Three-Layer Stack

### Layer 1: Viewport Lock

```
h-dvh flex flex-col
```

- `h-dvh` (not `h-screen` or `h-full`) locks to the **dynamic viewport height**
- On mobile, `dvh` shrinks when the virtual keyboard appears, keeping input visible
- `h-screen` includes the browser chrome height, causing overflow on mobile
- `h-full` depends on parent height, which often isn't set in Next.js App Router

### Layer 2: Flex Column Chat Container

```
h-full min-h-0 flex flex-col overflow-hidden
```

- `flex flex-col` creates the header / messages / input stack
- **`min-h-0`** is critical: overrides CSS Grid/Flexbox default `min-height: auto`
  - Without it, flex/grid children refuse to shrink below their content size
  - This single property was the root cause of the "input pushed off screen" bug
- `overflow-hidden` clips content to the container bounds

### Layer 3: Scrollable Messages (CSSence Double-Reverse Pattern)

```html
<!-- Outer: column-reverse for native bottom anchoring -->
<div class="flex-1 min-h-0 overflow-y-auto flex flex-col-reverse p-4">
  <!-- Inner: un-reverses content for natural reading order -->
  <div class="flex flex-col gap-4">
    {messages}
    {typingIndicator}
    <div ref={scrollAnchorRef} class="h-px" />  <!-- sentinel -->
  </div>
</div>
```

**Why double-reverse works:**
- Outer `flex-col-reverse`: scroll position 0 = bottom. Browser naturally anchors here.
- Inner `flex-col`: un-reverses content so messages read top-to-bottom. No `.reverse()` on the array.
- The CSS reverses cancel out, but scroll anchoring behavior is preserved.

**Why a single `flex-col-reverse` isn't enough:**
- Text selection breaks (selection direction is reversed)
- You must `.reverse()` the array, which is fragile with React keys
- No natural place for the typing indicator (it needs to be first in DOM)

## Critical CSS Properties

### `min-h-0` (The Flex/Grid Shrink Override)

Both CSS Grid and Flexbox set `min-height: auto` on children by default. This means a child's minimum height equals its content height, preventing shrinking. The fix:

```css
/* On grid items */
.grid-item { min-height: 0; }

/* On flex children that need to shrink */
.flex-child { min-height: 0; }
```

You often need it **twice** in a chat layout:
1. On the grid item containing the chat panel (grid context)
2. On the messages div inside the flex column (flex context)

### `overflow-hidden` vs `overflow-auto`

- **Container div** (the chat panel): `overflow-hidden` — clips everything, prevents double scrollbars
- **Messages div**: `overflow-y-auto` — allows message scrolling within the constrained area

### `h-dvh` vs `h-screen` vs `h-full`

| Property | Behavior | Mobile keyboard | Use case |
|----------|----------|-----------------|----------|
| `h-dvh` | Dynamic viewport height | Adapts | Chat containers |
| `h-screen` | Static viewport height (100vh) | Overflows | Full-page layouts without keyboard |
| `h-full` | 100% of parent | Depends on parent | Nested elements |

## Scroll Anchoring

### CSS Native: `overflow-anchor`

```css
.scroll-container { overflow-anchor: auto; }  /* default */
.message-item { overflow-anchor: none; }       /* opt out individual items */
```

- `auto` (default): browser tries to keep visible content stable when DOM changes above
- In `column-reverse`, this can **fight** with bottom-pinning during streaming
- Safari support is incomplete as of 2026
- Not reliable enough alone for production chat UIs

### JS Safety Net: Scroll Sentinel

```tsx
const scrollAnchorRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  scrollAnchorRef.current?.scrollIntoView({ behavior: "smooth" });
}, [messages]);

// In JSX, at the very end of the inner wrapper:
<div ref={scrollAnchorRef} className="h-px" />
```

- `scrollIntoView({ behavior: "smooth" })` for polished animation
- Fires on every `messages` change (new message or streaming token update)
- The sentinel is a 1px div at the bottom of the inner wrapper
- Combined with `column-reverse`, this ensures the scrollbar thumb stays at the bottom

### WhatsApp-Style Scroll Behavior

WhatsApp's actual behavior:
- **At bottom + new message**: auto-scroll to show it
- **Scrolled up + new message**: stay where you are, show "scroll to bottom" button
- **User sends message**: always scroll to bottom

To implement the "respect user scroll position" pattern:

```tsx
const scrollContainerRef = useRef<HTMLDivElement>(null);
const shouldAutoScroll = useRef(true);

const handleScroll = () => {
  const el = scrollContainerRef.current;
  if (!el) return;
  // In column-reverse, scrollTop=0 is bottom
  shouldAutoScroll.current = el.scrollTop < 50;
};

useEffect(() => {
  if (shouldAutoScroll.current) {
    scrollAnchorRef.current?.scrollIntoView({ behavior: "smooth" });
  }
}, [messages]);
```

## Message Bubbles

### Alignment

```tsx
<div className={cn("flex", role === "user" ? "justify-end" : "justify-start")}>
  <div className="max-w-[85%] rounded-2xl px-4 py-2">
    <p className="whitespace-pre-wrap">{content}</p>
  </div>
</div>
```

- Outer div: full width, `flex` with `justify-end`/`justify-start`
- Inner div: `max-w-[85%]` prevents bubbles from spanning full width
- `rounded-2xl` for the WhatsApp bubble shape
- `whitespace-pre-wrap` preserves line breaks in messages

### Typing Indicator

```tsx
{isLoading && !messages[messages.length - 1]?.displayContent && (
  <div className="flex justify-start">
    <div className="bg-muted rounded-2xl px-4 py-2">
      <div className="flex gap-1">
        <span className="w-2 h-2 bg-muted-foreground/50 rounded-full animate-bounce" />
        <span className="w-2 h-2 ... animate-bounce" style={{ animationDelay: "150ms" }} />
        <span className="w-2 h-2 ... animate-bounce" style={{ animationDelay: "300ms" }} />
      </div>
    </div>
  </div>
)}
```

- Show dots **only** before text arrives, hide once streaming text is visible
- Staggered `animationDelay` creates the wave effect
- Placed after messages but before the scroll sentinel in DOM order

## Input Pinning

```tsx
<form className="p-4 border-t">
  <div className="flex gap-2">
    <Textarea
      className="min-h-[44px] max-h-32 resize-none"
      onKeyDown={(e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          handleSubmit(e);
        }
      }}
    />
    <Button type="submit" size="icon" />
  </div>
</form>
```

- Natural flex child at the bottom of the chat column — no `position: fixed` needed
- `min-h-[44px]` meets touch target guidelines (44px)
- `max-h-32` prevents the textarea from growing unbounded
- `resize-none` prevents manual resize (height is auto-managed)
- Enter submits, Shift+Enter adds newline

## Full Hierarchy Reference

```
h-dvh flex flex-col pt-16                              // viewport lock + navbar offset
  flex-1 w-full px-4 pb-4 overflow-hidden              // main content area
    h-full lg:grid lg:grid-cols-[1fr_420px]            // desktop: sidebar + chat
    lg:grid-rows-[1fr] lg:gap-6
      // Left: sidebar panel
      hidden lg:block h-full overflow-auto space-y-6   // independent scroll

      // Right: chat panel
      h-full min-h-0 flex flex-col overflow-hidden     // THE CHAT CONTAINER
        p-4 border-b                                    // header (fixed height)
        flex-1 min-h-0 overflow-y-auto                 // messages (scrollable)
        flex flex-col-reverse p-4                      //   column-reverse outer
          flex flex-col gap-4                           //   normal inner wrapper
            {messages}                                  //     chronological order
            {typingDots}                                //     after messages
            div.h-px ref={scrollAnchor}                //     sentinel at end
        p-4 border-t                                    // input (pinned at bottom)
```

## Mobile Considerations

### Bottom Sheet / Drawer Pattern

For companion panels on mobile (like a Lean Canvas sidebar):

```tsx
// Toggle button: fixed position above the input
<button className="lg:hidden fixed bottom-20 left-4 z-50 rounded-full bg-primary shadow-lg p-3">

// Drawer: overlay from bottom
<div className="lg:hidden fixed inset-0 z-40 bg-black/50">
  <div className="absolute inset-x-0 bottom-0 max-h-[70vh] overflow-auto rounded-t-2xl bg-background p-4">
```

- `max-h-[70vh]` prevents drawer from covering the full screen
- `rounded-t-2xl` gives the iOS-style sheet appearance
- Separate scroll context from the chat messages

## Common Pitfalls

| Pitfall | Cause | Fix |
|---------|-------|-----|
| Input pushed off screen | Grid/flex `min-height: auto` default | Add `min-h-0` to grid item AND flex child |
| Can't scroll to oldest messages | `justify-content: flex-end` on scroll container | Use inner wrapper or `margin-top: auto` instead |
| Text selection reversed | `column-reverse` on content container | Double-reverse with inner wrapper |
| Scroll jumps during streaming | Browser `overflow-anchor` fighting layout | Add JS `scrollIntoView` safety net |
| `h-screen` overflows on mobile | Static viewport includes browser chrome | Use `h-dvh` (dynamic viewport height) |
| `space-y-4` reversed in column-reverse | Margins are direction-dependent | Use `gap-4` instead (direction-agnostic) |
| Firefox scroll broken with column-reverse | Bug 1042151 (open since 2015) | Inner wrapper pattern works around it |

## Sources

- [CSSence: Bottom-Anchored Scrolling Area](https://cssence.com/2024/bottom-anchored-scrolling-area/) - The double-reverse pattern
- [Saurus Chronicles: Reverse Scrolling for Chat Boxes](https://seo-saurus.com/saurus-chronicles/reverse-scrolling-for-chat-boxes) - CSS-only approach
- [CSS-Tricks: overflow-anchor](https://css-tricks.com/almanac/properties/o/overflow-anchor/) - Scroll anchoring API
- [Firefox Bug 1042151](https://bugzilla.mozilla.org/show_bug.cgi?id=1042151) - column-reverse overflow issues
- [React Docs: getSnapshotBeforeUpdate](https://react.dev/reference/react/Component) - Scroll position preservation
- [Chen Hui Jing: Box Alignment and Overflow](https://chenhuijing.com/blog/box-alignment-and-overflow/) - Flexbox overflow edge cases
