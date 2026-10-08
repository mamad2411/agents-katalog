---
description: Colocate React state in the lowest owning component to avoid unnecessary parent and sibling re-renders
globs: chat-app-frontend/**/*.js, chat-app-frontend/**/*.tsx
alwaysApply: false
---

# Colocate React State

When a parent component's state changes, React re-renders that parent and **all of its children by default**, even if a child's props did not change.

Prefer **colocating state** in the lowest component that owns that concern, especially for fast-changing UI state (text inputs, hover, local toggles), to keep expensive siblings stable.

## Default approach

Before adding state to a parent, ask:

1. Who **reads** this state live?
2. Who **writes** this state?
3. Do **siblings** need the live value, or only the final value on an action (submit/send)?

| Situation                                                       | Prefer                                                                           |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Only one child needs live state (e.g. draft text in a composer) | Keep state in that child                                                         |
| Parent only needs the value on submit                           | Child owns state; parent receives callback with final value                      |
| Multiple siblings need the same live state                      | Lift to shared parent, context, or store                                         |
| Parent must reset/clear child state (e.g. on route/chat change) | Pass a `key`, `chatId`, or explicit reset prop — do not lift state up by default |

## Example from this codebase

```jsx
// ❌ BAD — typing re-renders ChatArea and ChatMessageList
function ChatArea() {
  const [messageInput, setMessageInput] = useState("");
  return (
    <>
      <ChatMessageList messages={messages} />
      <ChatMessageComposer messageInput={messageInput} onChange={(e) => setMessageInput(e.target.value)} />
    </>
  );
}

// ✅ GOOD — typing re-renders only the composer
function ChatArea() {
  return (
    <>
      <ChatMessageList messages={messages} />
      <ChatMessageComposer onSendMessage={onSendMessage} />
    </>
  );
}

function ChatMessageComposer({ onSendMessage }) {
  const [messageInput, setMessageInput] = useState("");
  // send via onSendMessage(messageInput.trim()), then clear local state
}
```

## When colocation is not enough

Use these as **secondary** tools, not replacements for colocation:

- `React.memo` on expensive children when props are stable
- `useCallback` / `useMemo` for stable props passed to memoized children
- Split contexts so fast-changing state does not share a provider with slow-changing data

Do not lift state to a parent only for convenience if that causes avoidable re-renders of unrelated siblings.
