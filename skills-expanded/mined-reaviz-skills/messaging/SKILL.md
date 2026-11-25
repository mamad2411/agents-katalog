# Messaging

Components that render the active session: panel layout, header, messages list, individual message, plus the per-message slots (question, response, files, sources, action footer). All read state from `ChatContext`, so they only function inside `<Chat>`.

## Imports

```tsx
import {
  SessionMessagePanel,
  SessionMessagesHeader,
  SessionMessages,
  SessionMessage,
  SessionEmpty,
  MessageQuestion,
  MessageResponse,
  MessageFiles,
  MessageSources,
  MessageActions
} from 'reachat';
```

## SessionMessagePanel

Outer wrapper for the message column. Animates in/out, handles compact-mode "back to sessions" button, and slots in its children.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `allowBack` | `boolean` | `true` | Render the back button in compact view (hidden when `viewType === 'chat'`) |
| `children` | `ReactNode` | — | Header / messages / input slots |

```tsx
<SessionMessagePanel>
  <SessionMessagesHeader />
  <SessionMessages />
  <ChatInput />
</SessionMessagePanel>
```

The panel only renders when there is something to show: in companion mode, only when an `activeSessionId` is set; in console / chat mode, always.

## SessionMessagesHeader

Header for the active session — renders the title (with `Ellipsis`) and creation date (`DateFormat`). Hidden when no session is active. Accepts children to override the default content (Radix `Slot`):

```tsx
<SessionMessagesHeader>
  <div className="flex items-center justify-between gap-2">
    <h2>{activeSession?.title}</h2>
    <Button>Share</Button>
  </div>
</SessionMessagesHeader>
```

## SessionMessages

Renders the conversations of the `activeSession`. Handles client-side pagination via `reablocks` `useInfinityList`, optional auto-scroll to bottom, and a "scroll to bottom" floating button.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `limit` | `number \| null` | `10` | Client-side page size; `null` disables paging and renders the full list |
| `showMoreText` | `string` | `'Show more'` | Label for the load-more button |
| `autoScroll` | `boolean` | `true` | Scroll to bottom when the active session changes or animation finishes |
| `showScrollBottomButton` | `boolean` | — | Show floating "scroll to bottom" button when not at bottom |
| `showLoadMoreButton` | `boolean` | `false` | Force-show the "show more" button (otherwise shown only when `hasMore`) |
| `loadMoreButtonDisabled` | `boolean` | — | Disable the load-more button |
| `newSessionContent` | `string \| ReactNode` | — | Forwarded to `SessionEmpty` when no session is active |
| `onScroll` | `UIEventHandler<HTMLDivElement>` | — | Captures scroll on the scroll container |
| `onLoadMore` | `() => void` | — | Replace built-in pagination — fires when load-more is clicked |
| `children` | `(conversations: Conversation[]) => ReactNode` | — | Render-prop override; if omitted, renders `<SessionMessage />` per conversation |

```tsx
<SessionMessages
  limit={20}
  autoScroll
  showScrollBottomButton
  onLoadMore={fetchOlderConversations}
>
  {convos => convos.map(c => <SessionMessage key={c.id} conversation={c} />)}
</SessionMessages>
```

When no session is active, `SessionMessages` falls back to `<SessionEmpty>{newSessionContent}</SessionEmpty>` (renders `theme.empty`).

## SessionMessage

Renders a single conversation as a card with the four sub-components (question, response, sources, actions). Uses Framer Motion for staggered entry animation (configured by the parent `SessionMessages` container).

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `conversation` | `Conversation` | — | Conversation data |
| `isLast` | `boolean` | — | Marks the streaming message — controls the loading cursor on `MessageResponse` |
| `className` | `string` | — | Class for the inner Card |
| `children` | `ReactNode` | — | Override the default sub-component layout |

```tsx
<SessionMessage conversation={conv} isLast={isStreaming}>
  <MessageQuestion question={conv.question} files={conv.files} />
  <MessageResponse response={conv.response} isLoading={isStreaming} />
  <MessageSources sources={conv.sources} />
  <MessageActions question={conv.question} response={conv.response} onUpvote={...} />
</SessionMessage>
```

The default body checks `isLast && isLoading` from context to show the typing cursor on `MessageResponse`.

## MessageQuestion

Question block: renders `Markdown` with the chat's `remarkPlugins`, plus attached files and a "Show more" button when the question is long (>500 chars).

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `question` | `string` | — | Markdown question string |
| `files` | `ConversationFile[]` | — | File attachments rendered above the text |
| `children` | `ReactNode` | — | Override (Radix `Slot`) |

## MessageResponse

Response markdown with an animated streaming cursor when `isLoading` is true. Renders inside a `data-compact` wrapper for compact-mode targeting.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `response` | `string` | — | Markdown response string |
| `isLoading` | `boolean` | — | Show the blinking cursor |

## MessageFiles

Renders `Conversation.files`. Image files (`type` starts with `image/`) and other files are grouped separately. When more than 3 image files, the rest collapse behind a `+N` overlay that expands on click.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `files` | `ConversationFile[]` | — | Files to render |
| `children` | `ReactNode` | — | Override (default `MessageFile`) |

## MessageSources

Renders `Conversation.sources` as cards using the default `MessageSource` component. Hidden when sources is empty.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `sources` | `ConversationSource[]` | — | Sources to render |
| `children` | `ReactNode` | — | Override slot for custom source rendering |

## MessageActions

Footer with copy / upvote / downvote / refresh icon buttons. Renders only when at least one icon prop is provided. Defaults copy the question + response to the clipboard.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `question` | `string` | — | Used by the default copy handler |
| `response` | `string` | — | Used by the default copy handler |
| `copyIcon` / `thumbsUpIcon` / `thumbsDownIcon` / `refreshIcon` | `ReactElement \| null` | reachat icons | Pass `null` to hide a button |
| `onCopy` / `onUpvote` / `onDownvote` / `onRefresh` | `() => void` | — | Handlers (default `onCopy` writes `question\nresponse` to the clipboard) |
| `children` | `ReactNode` | — | Override the entire footer |

## SessionEmpty

Empty-state shown by `SessionMessages` when no session is active. Renders `newSessionContent` inside `theme.empty`.

```tsx
<SessionEmpty>Start a new conversation</SessionEmpty>
```

## Theme keys

```
theme.messages.{base, console, companion, back, inner, title, date, content, header, showMore}
theme.messages.message.{base, question, response, cursor, overlay, expand, scrollToBottom: { container, button }}
theme.messages.message.files.{base, file: { base, name }}
theme.messages.message.sources.{base, source: { base, companion, image, title, url }}
theme.messages.message.markdown.{hr, p, a, table, th, td, code, inlineCode, toolbar, li, ul, ol, copy, h1..h6}
theme.messages.message.footer.{base, copy, upvote, downvote, refresh}
```
