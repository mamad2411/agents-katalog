# Input

Composer area: rich-text input (Tiptap), send / stop / file-attach actions, and `@mention` / `/command` suggestion popups.

## Imports

```tsx
import {
  ChatInput,
  RichTextInput,
  MentionList,
  type ChatInputRef,
  type RichTextInputRef,
  type SuggestionConfig,
  type SuggestionItem,
  type MentionItem,
  type SlashCommandItem
} from 'reachat';
```

## ChatInput

Main composer used inside `<Chat>`. Wraps `RichTextInput` and adds: file attachment (`FileInput`), send button, stop button (during streaming). Reads `isLoading`, `disabled`, `sendMessage`, `stopMessage`, `fileUpload`, `activeSessionId` from `ChatContext`.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `placeholder` | `string` | `'Type a message...'` | Editor placeholder |
| `defaultValue` | `string` | — | Initial editor value |
| `allowedFiles` | `string[]` | — | File extensions/MIME types — when set, the attach button is shown |
| `allowMultipleFiles` | `boolean` | `false` | Allow selecting multiple files |
| `attachIcon` | `ReactElement` | paperclip | Icon for the file button |
| `sendIcon` | `ReactElement` | send | Icon for the send button |
| `stopIcon` | `ReactElement` | stop | Icon for the stop button |
| `mentions` | `SuggestionConfig<MentionItem>` | — | Configures `@`-trigger suggestions |
| `commands` | `SuggestionConfig<SlashCommandItem>` | — | Configures `/`-trigger suggestions |
| `minHeight` | `number` | `24` | Editor min height in px |
| `maxHeight` | `number` | `200` | Editor max height in px (auto-expand) |
| `autoFocus` | `boolean` | `true` | Auto-focus on mount and when `activeSessionId` changes |
| `onMessageChange` | `(value: string) => void` | — | Fires on every keystroke with the current value |
| `className` | `string` | — | Container class |

The send/stop buttons swap based on `isLoading`. Attach button only renders when `allowedFiles?.length > 0`.

```tsx
const inputRef = useRef<ChatInputRef>(null);

<ChatInput
  ref={inputRef}
  placeholder="Ask anything..."
  allowedFiles={['image/*', '.pdf']}
  allowMultipleFiles
  mentions={{
    items: [
      { id: '1', label: 'John Doe', description: 'Engineer', icon: <Avatar /> }
    ]
  }}
  commands={{
    items: [
      { id: 'help', label: 'Help', shortcut: 'Ctrl+H' },
      { id: 'search', label: 'Search', type: 'insert', value: 'search:' }
    ]
  }}
  onMessageChange={handleDraftChange}
/>
```

### ChatInputRef

```ts
interface ChatInputRef {
  focus: () => void;
  getValue: () => string;
  setValue: (value: string) => void;
  insertText: (text: string) => void;
}
```

## RichTextInput

Standalone Tiptap-based editor used internally by `ChatInput`. Useful when building a custom composer.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `string` | — | Editor content |
| `placeholder` | `string` | — | Placeholder text |
| `disabled` | `boolean` | — | Disable editing |
| `autoFocus` | `boolean` | `true` | Focus on mount |
| `minHeight` | `number` | `24` | Min editor height |
| `maxHeight` | `number` | `200` | Max editor height |
| `mentions` | `SuggestionConfig` | — | `@` trigger config |
| `commands` | `SuggestionConfig` | — | `/` trigger config |
| `className` | `string` | — | Editor class |
| `onChange` | `(value: string) => void` | — | Value changed |
| `onSubmit` | `(value: string) => void` | — | `Enter` pressed (Shift+Enter inserts a newline) |

`RichTextInputRef` exposes the same methods as `ChatInputRef`.

Built on Tiptap v3 with `Document`, `Paragraph`, `Text`, `HardBreak`, `Placeholder`, and `Mention` extensions; suggestion popups positioned via Floating UI's `flip`/`shift` middleware.

## SuggestionConfig

```ts
interface SuggestionItem {
  id: string;
  label: string;
  description?: string;
  icon?: ReactElement;
  metadata?: Record<string, unknown>;
}

interface MentionItem extends SuggestionItem {
  /** Custom value to insert; defaults to label. */
  value?: string;
}

interface SlashCommandItem extends SuggestionItem {
  shortcut?: string;
  type?: 'insert' | 'action';
  value?: string;
}

interface SuggestionConfig<T extends SuggestionItem = SuggestionItem> {
  /** Trigger character (default: '@' for mentions, '/' for commands) */
  trigger?: string;
  /** Static items */
  items?: T[];
  /** Async search — return filtered items for the current query */
  onSearch?: (query: string) => Promise<T[]> | T[];
  /** Custom selection handler — receives the chosen item and an insertText callback */
  onSelect?: (item: T, insertText: (text: string) => void) => void;
  /** Cap on visible items (default: 10) */
  maxResults?: number;
  /** Custom row renderer */
  renderItem?: (item: T, isHighlighted: boolean) => ReactNode;
  /** Custom empty-state renderer */
  renderEmpty?: (query: string) => ReactNode;
}
```

### Static items

```tsx
mentions={{
  items: [
    { id: '1', label: 'Alice', description: 'PM' },
    { id: '2', label: 'Bob', description: 'Eng' }
  ]
}}
```

### Async search

```tsx
commands={{
  onSearch: async query => {
    const results = await api.searchCommands(query);
    return results.map(r => ({ id: r.id, label: r.name, shortcut: r.hotkey }));
  },
  maxResults: 8
}}
```

### Custom render & insert

```tsx
mentions={{
  items: people,
  renderItem: (item, isHighlighted) => (
    <div className={isHighlighted ? 'bg-blue-100' : ''}>
      <strong>@{item.label}</strong>
      <small>{item.description}</small>
    </div>
  ),
  onSelect: (item, insertText) => insertText(`@[${item.label}](user:${item.id})`)
}}
```

## MentionList

The popup component the editor renders for suggestions. Exposed for advanced users — most code only needs `SuggestionConfig`.

```ts
interface MentionListRef {
  onKeyDown: (props: { event: KeyboardEvent }) => boolean;
}

interface MentionListProps {
  items: SuggestionItem[];
  command: (item: { id: string; label: string }) => void;
  triggerChar: string;
  config: SuggestionConfig;
  query?: string;
}
```

Keyboard: ↑/↓ moves selection, Enter/Tab inserts, Escape dismisses.

## Theme keys

```
theme.input.{base, upload, input}
theme.input.actions.{base, send, stop}
theme.input.popup.{base, content, item, itemHighlighted, itemIcon, itemContent, itemLabel, itemDescription, itemShortcut, empty, loading}
theme.input.tag.{base, mention, command}    // Inline pill styling for inserted mentions/commands
theme.input.editor.{base, container, placeholder}
```

## Deprecated aliases

The following type aliases exist for backwards compatibility and will be removed in a future major:

- `MentionPluginConfig` → use `SuggestionConfig<MentionItem>`
- `SlashCommandPluginConfig` → use `SuggestionConfig<SlashCommandItem>`
- `InputPluginItem` → use `SuggestionItem`
- `InputTrigger<T>` → use `SuggestionConfig<T>`
