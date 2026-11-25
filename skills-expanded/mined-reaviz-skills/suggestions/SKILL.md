# ChatSuggestions

Clickable suggestion chips (typically rendered above or below `ChatInput` to surface starter prompts). Reads `theme.suggestions` and `disabled` / `isLoading` from `ChatContext`.

## Imports

```tsx
import { ChatSuggestions, ChatSuggestion } from 'reachat';
import type { Suggestion } from 'reachat';
```

## ChatSuggestions

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `suggestions` | `Suggestion[]` | — | Array of `{ id, content }` items |
| `onSuggestionClick` | `(content: string) => void` | — | Fires with the clicked suggestion's content |
| `className` | `string` | — | Container class |
| `children` | `ReactElement` | — | Single child template — clones it per suggestion with `{ ...suggestion, onClick }` props |

`Suggestion`:

```ts
interface Suggestion {
  id: string;
  content: string;
}
```

Returns `null` when `suggestions` is empty.

## ChatSuggestion

The default chip rendered by `ChatSuggestions`. Built on reablocks `Button` (`variant="outline"`).

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `string` | — | Required |
| `content` | `string` | — | Display text |
| `onClick` | `(content: string) => void` | — | Click handler |

Honors `disabled` and `isLoading` from `ChatContext` (the chip becomes non-interactive).

## Default usage

```tsx
const suggestions = [
  { id: '1', content: 'Summarize this document' },
  { id: '2', content: 'Translate to French' },
  { id: '3', content: 'Explain like I\'m five' }
];

<ChatSuggestions
  suggestions={suggestions}
  onSuggestionClick={text => sendMessage(text)}
/>
```

## Custom chip rendering

Pass a single child element — `ChatSuggestions` clones it per suggestion, spreading the suggestion plus the click handler:

```tsx
<ChatSuggestions
  suggestions={suggestions}
  onSuggestionClick={sendMessage}
>
  <button className="my-chip" />
</ChatSuggestions>
```

## Theme keys

```
theme.suggestions.base
theme.suggestions.item.{base, icon, text}
```
