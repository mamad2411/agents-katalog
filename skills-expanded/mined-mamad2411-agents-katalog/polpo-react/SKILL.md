---
name: polpo-react
description: Build AI agent interfaces with Polpo UI — composable React chat components, CLI tools, and starter templates. Use when the user wants to create a chat app, add chat components, install @polpo-ai/chat, scaffold a Polpo project, configure theming/dark mode, use ChatInput, ChatMessage, ChatSessionList, or any Polpo UI component. Triggers on "polpo ui", "chat UI", "chat component", "@polpo-ai/chat", "@polpo-ai/ui", "create-polpo-app", "chat input", "session list", "agent selector", "chat interface", "polpo chat", "chat widget", "multi-agent".
---

# Polpo UI

Composable React chat components for Polpo AI agents. Three composition levels, three installation methods.

## Install

### New project

```bash
# Interactive
npx create-polpo-app

# Non-interactive (CI / AI agents)
npx create-polpo-app my-app -t chat -y
npx create-polpo-app my-app -t chat-widget -y
npx create-polpo-app my-app -t multi-agent -y
```

### Add to existing project (shadcn-style, copies source)

```bash
# Interactive multi-select
npx @polpo-ai/ui add

# Non-interactive
npx @polpo-ai/ui add --all
npx @polpo-ai/ui add tools hooks --overwrite
```

### npm package (compiled)

```bash
npm install @polpo-ai/chat @polpo-ai/sdk @polpo-ai/react react-virtuoso lucide-react streamdown
```

Consumer adds Tailwind scanning:
```css
/* Tailwind v4 */
@source "../node_modules/@polpo-ai/chat/dist/**/*.js";
```
```js
// Tailwind v3 — tailwind.config.js
content: ["./node_modules/@polpo-ai/chat/dist/**/*.js"]
```

## Provider Setup

```tsx
import { PolpoProvider } from "@polpo-ai/react";

// baseUrl is root URL — SDK appends /v1/ internally. Do NOT add /v1/.
<PolpoProvider baseUrl="https://api.polpo.sh" apiKey={process.env.NEXT_PUBLIC_POLPO_API_KEY} autoConnect={false}>
  {children}
</PolpoProvider>
```

## Composition Levels

### Level 1 — Zero Config
```tsx
<Chat agent="coder" sessionId="session_abc" />
```

### Level 2 — Compose (children replace default input)
```tsx
<Chat agent="coder" avatar={<Avatar />}>
  <MyCustomInput />
</Chat>
```

### Level 3 — Primitives
```tsx
import { ChatMessage, ChatSkeleton } from "@polpo-ai/chat";
import { useChat } from "@polpo-ai/react";
```

## Render Function Pattern

```tsx
<Chat agent="coder" onSessionCreated={(id) => router.replace(`/chat/${id}`)}>
  {({ hasMessages }) => hasMessages ? <ChatInput /> : <LandingPage />}
</Chat>
```

## Session Navigation

Package does NOT handle routing. Use `onSessionCreated` callback:
```tsx
<Chat onSessionCreated={(id) => router.push(`/chat/${id}`)} />
```

## Components

| Component | Purpose |
|---|---|
| `Chat` | Root compound — Provider + Messages + Input |
| `ChatInput` | Textarea + submit + file attach + drag & drop |
| `ChatMessage` | Message dispatcher (user/assistant) |
| `ChatMessages` | Virtuoso list with auto-scroll |
| `ChatProvider` | Context wrapping useChat + useFiles |
| `ChatSessionList` | Flat session list with select/delete |
| `ChatSessionsByAgent` | Sessions grouped by agent |
| `ChatAgentSelector` | Agent picker dropdown |
| `ChatSuggestions` | Suggestion button grid |
| `ChatAskUser` | Ask-user-question wizard |
| `ChatLanding` | Landing + greeting + input + suggestions |
| `ChatScrollButton` | Scroll-to-bottom indicator |
| `ChatSkeleton` | Loading skeleton |
| `ChatTyping` | Typing dots |
| `ToolCallChip` | Auto-dispatching tool renderer |
| `ToolCallShell` | Base tool renderer with expand/collapse |

## Hooks

```tsx
const { messages, sendMessage, isStreaming, abort, uploadFile, pendingToolCall } = useChatContext();
const handleSubmit = useSubmitHandler(sendMessage, uploadFile);
const dragging = useDocumentDrag();
```

## References

- **Component props**: [references/components.md](references/components.md) — full props for every component
- **Composition patterns**: [references/patterns.md](references/patterns.md) — app assembly, ask-user, sessions, custom tools
- **CLI commands**: [references/cli.md](references/cli.md) — create-polpo-app, @polpo-ai/ui, flags
- **Theming**: [references/theming.md](references/theming.md) — colors, dark mode, fonts, Tailwind config
