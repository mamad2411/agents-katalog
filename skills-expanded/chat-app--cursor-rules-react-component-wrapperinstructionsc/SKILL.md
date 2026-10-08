---
description: Use when creating or editing React components (.js/.tsx) under chat-app-frontend. Every component return must wrap JSX in a single kebab-case `-wrapper` root div — even if nearby files omit it
globs: chat-app-frontend/**/*.js, chat-app-frontend/**/*.tsx
alwaysApply: false
---

# React Component Wrapper

Every React component's returned JSX must have a single root `<div>` with `className="{kebab-case-name}-wrapper"`.

- Derive the class from the component name: `ChatArea` → `chat-area-wrapper`, `ChatPage` → `chat-page-wrapper`.
- Put all component markup inside this wrapper.

```jsx
function ChatArea() {
  return (
    <div className="chat-area-wrapper">
      {/* component content */}
    </div>
  );
}
```
