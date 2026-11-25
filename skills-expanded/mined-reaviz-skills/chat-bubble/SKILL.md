# ChatBubble

Floating chat bubble launcher — renders a clickable trigger and toggles a popover containing the chat UI. Built on reablocks `ConnectedOverlay` (Floating UI under the hood).

## Import

```tsx
import { ChatBubble } from 'reachat';
import type { Placement, Modifiers } from 'reablocks';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `bubbleContent` | `ReactNode` | — | Content rendered inside the trigger element (the always-visible bubble) |
| `children` | `ReactNode` | — | Content rendered inside the floating popover when open |
| `position` | `Placement` | `'right-end'` | Floating UI placement (e.g. `'top'`, `'bottom-start'`, `'left-end'`) |
| `modifiers` | `Modifiers` | `[offset({ mainAxis: 0, crossAxis: -40 })]` | Floating UI middleware overrides |
| `className` | `string` | — | Class for the trigger wrapper |

Click the trigger to open / close. The component manages its own `isOpen` state.

## Usage

```tsx
<ChatBubble
  bubbleContent={
    <button className="rounded-full p-3 bg-primary text-white shadow-lg">
      <ChatIcon />
    </button>
  }
  position="top-end"
>
  <Chat
    sessions={sessions}
    activeSessionId={activeId}
    viewType="companion"
    onSendMessage={handleSend}
  >
    <SessionMessagePanel>
      <SessionMessages />
      <ChatInput />
    </SessionMessagePanel>
  </Chat>
</ChatBubble>
```

For a floating chat bubble experience, pair `ChatBubble` with `viewType="companion"` so the chat surface fits within the popover.
