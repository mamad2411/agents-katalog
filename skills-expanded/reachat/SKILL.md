---
name: reachat
description: Use when building chat / LLM UIs in React with the reachat component library (Chat, ChatInput, SessionsList, SessionMessages, ChatBubble, AppBar, Markdown rendering with code highlighting, RichTextInput with @mentions and /commands, MessageStatus, ComponentCatalog for LLM-driven dynamic components, useAgUi for ag-ui protocol). Covers the slot-based Chat layout, ChatContext, theme system (ChatTheme, PartialChatTheme), file uploads, multi-file support, autoScroll, and viewType (console / companion / chat).
---

# Reachat

Reachat is a React UI library for building chat / LLM experiences. It provides a slot-based component system, markdown rendering, rich-text input with mentions and slash commands, file uploads, session management, and a typed Tailwind theme system.

Built on **reablocks** (UI primitives), **Tiptap v3** (rich text editor), **react-markdown**, **Floating UI** (popups), and **motion** (animations).

## Installation

```bash
npm install reachat reablocks
```

The library is distributed as ESM with a separate CSS file. Import the styles once:

```tsx
import 'reachat/dist/index.css';
```

## Three-tier Composition

The main `Chat` component is a **provider + layout shell**. It exposes context (`ChatContext`) consumed by `SessionsList`, `SessionMessagePanel`, `SessionMessages`, `ChatInput`, etc. Slot composition lets you swap layouts without rewriting state plumbing.

```tsx
import {
  Chat,
  SessionsList,
  SessionGroups,
  NewSessionButton,
  SessionMessagePanel,
  SessionMessagesHeader,
  SessionMessages,
  SessionMessage,
  ChatInput
} from 'reachat';

<Chat
  viewType="console"
  sessions={sessions}
  activeSessionId={activeId}
  isLoading={isStreaming}
  onSelectSession={setActiveId}
  onDeleteSession={handleDelete}
  onNewSession={handleNew}
  onSendMessage={handleSend}
  onStopMessage={handleStop}
  onFileUpload={handleUpload}
>
  <SessionsList>
    <NewSessionButton />
    <SessionGroups />
  </SessionsList>
  <SessionMessagePanel>
    <SessionMessagesHeader />
    <SessionMessages>
      {convos => convos.map(c => <SessionMessage key={c.id} conversation={c} />)}
    </SessionMessages>
    <ChatInput />
  </SessionMessagePanel>
</Chat>
```

## viewType

`Chat` adapts layout based on `viewType` and viewport width:

| viewType | Description |
|----------|-------------|
| `'console'` | Full screen with sessions sidebar (default) |
| `'companion'` | Compact / mobile view, sessions and panel toggle in place |
| `'chat'` | Chat only — no sessions list rendered |

`Chat` measures its own container; if width drops below 767px the `companion` layout is automatically forced (`isCompact = true` in context).

## Core Data Types

```typescript
import type { Session, Conversation, ConversationFile, ConversationSource, Template, Suggestion } from 'reachat';

interface Session {
  id: string;
  title?: string;
  createdAt?: Date;
  updatedAt?: Date;
  conversations: Conversation[];
}

interface Conversation {
  id: string;
  createdAt: Date;
  updatedAt?: Date;
  question: string;
  response?: string;
  sources?: ConversationSource[];
  files?: ConversationFile[];
}

interface ConversationFile { name: string; type?: string; size?: number; url?: string; }
interface ConversationSource { url?: string; title?: string; image?: string; }

interface Template { id: string; title: string; message: string; icon?: ReactElement; }
interface Suggestion { id: string; content: string; }
```

## Chat Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `sessions` | `Session[]` | — | Session list to display (required) |
| `activeSessionId` | `string` | — | Currently selected session id (controlled) |
| `viewType` | `'console' \| 'companion' \| 'chat'` | `'console'` | Layout variant |
| `theme` | `ChatTheme` | `chatTheme` | Custom theme |
| `remarkPlugins` | `Plugin[]` | `[remarkGfm, remarkYoutube, remarkMath]` | Remark plugins for the markdown pipeline |
| `markdownComponents` | `react-markdown` `Components` | — | Custom markdown component overrides |
| `components` | `ComponentCatalog` | — | A catalog created by `componentCatalog()` for dynamic LLM-driven components |
| `isLoading` | `boolean` | — | Show loading state (cursor on the streaming response, disabled send) |
| `disabled` | `boolean` | — | Disable interactions globally |
| `style` / `className` | — | — | Root element styling |
| `onSelectSession` | `(id: string) => void` | — | Session selected |
| `onDeleteSession` | `(id: string) => void` | — | Session deleted |
| `onNewSession` | `() => void` | — | Hotkey or button triggered new session |
| `onSendMessage` | `(message: string) => void` | — | Send button or Enter |
| `onStopMessage` | `() => void` | — | Stop streaming |
| `onFileUpload` | `(file: File \| File[]) => void` | — | File(s) attached via `ChatInput` |

`Chat` also registers a `meta+shift+s` hotkey (via `reakeys`) for "Create new session" — wired to `onNewSession`.

## ChatContext

Slot components consume context via `useContext(ChatContext)`:

```typescript
interface ChatContextProps {
  sessions: Session[];
  activeSession?: Session | null;
  activeSessionId: string | null;
  viewType?: 'chat' | 'companion' | 'console';
  isCompact?: boolean;          // true when companion or width < 767px
  isLoading?: boolean;
  disabled?: boolean;
  theme?: ChatTheme;
  remarkPlugins?: Plugin[];
  markdownComponents?: Components;
  selectSession?: (id: string) => void;
  deleteSession?: (id: string) => void;
  createSession?: () => void;
  sendMessage?: (message: string) => void;
  stopMessage?: () => void;
  fileUpload?: (file: File | File[]) => void;
}
```

You can build custom slot components by reading `ChatContext` directly.

## Theme System

The `ChatTheme` interface holds Tailwind class strings for every region of the UI: container, sessions, messages, message bubble, markdown, footer actions, input editor, suggestion popup, mention/command tags, suggestions, charts, dynamic component frame, and message status.

```tsx
import { Chat, chatTheme, type ChatTheme, type PartialChatTheme } from 'reachat';

// Per-instance override — use PartialChatTheme to type partial overrides
const myTheme: PartialChatTheme = {
  input: {
    actions: { send: 'bg-emerald-500 hover:bg-emerald-600 text-white' }
  }
};

<Chat theme={{ ...chatTheme, ...myTheme as ChatTheme }} sessions={...}>...</Chat>
```

`PartialChatTheme` is `DeepPartial<ChatTheme>` — convenient for typing overrides.

Top-level theme keys (each is a nested map of class strings):

- `base`, `console`, `companion`, `empty`, `appbar`
- `sessions` — list, group, session, console/companion shell
- `messages` — content, header, message bubble, markdown, footer (copy / upvote / downvote / refresh), files, sources, scrollToBottom
- `input` — base, upload, input, actions (send / stop), `popup` (mention/command popup), `tag` (mention/command pill in editor), `editor` (Tiptap container)
- `suggestions` — chips below or above the input
- `status` — MessageStatus (icon, text, multi-step)
- `chart` — ChartRenderer wrapper / error / warning
- `component` — ComponentCatalog render frame

`Chat` resolves the theme via `useComponentTheme<ChatTheme>('chat', customTheme)` from reablocks, so you can also extend it via reablocks' `extendTheme`.

## Hotkeys

`Chat` registers global shortcuts via `reakeys`:

- `meta+shift+s` — Create new session

## Component Index

| Category | Components |
|----------|------------|
| **Root** | `Chat`, `ChatContext`, `chatTheme`, `ChatTheme`, `PartialChatTheme` |
| **Sessions** | `SessionsList`, `SessionGroups`, `SessionsGroup`, `SessionListItem`, `NewSessionButton` |
| **Messages** | `SessionMessagePanel`, `SessionMessagesHeader`, `SessionMessages`, `SessionMessage`, `MessageQuestion`, `MessageResponse`, `MessageSources`, `MessageActions`, `MessageFiles`, `SessionEmpty` |
| **Input** | `ChatInput`, `RichTextInput`, `MentionList`, `FileInput` |
| **AppBar** | `AppBar` |
| **Bubble** | `ChatBubble` |
| **Suggestions** | `ChatSuggestions`, `ChatSuggestion` |
| **Markdown** | `Markdown`, `CodeHighlighter`, `Table`, themes |
| **Status** | `MessageStatus`, `MessageStatusItem`, `StatusIcon` |
| **Catalog** | `componentCatalog`, `ComponentRenderer`, `ComponentPre`, `ComponentError`, `chartComponentDef`, `validateSpec`, `generatePrompt` |
| **AG-UI** | `useAgUi` |
| **Types** | `Session`, `Conversation`, `ConversationFile`, `ConversationSource`, `Template`, `Suggestion`, `SuggestionItem`, `MentionItem`, `SlashCommandItem`, `SuggestionConfig` |

See per-component skills under `messaging/`, `input/`, `sessions/`, `markdown/`, `chat-bubble/`, `app-bar/`, `suggestions/`, `status/`, `catalog/`, `ag-ui/`.
