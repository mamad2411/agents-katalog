# AppBar

Top header bar for the chat. Reads the `theme.appbar` class string and renders arbitrary content.

## Import

```tsx
import { AppBar } from 'reachat';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `ReactNode` | — | Content to display |
| `theme` | `ChatTheme` | `chatTheme` | Per-instance theme override |

## Usage

```tsx
<AppBar
  content={
    <div className="flex w-full items-center justify-between">
      <Logo />
      <UserMenu />
    </div>
  }
/>
```

`AppBar` resolves its theme via `useComponentTheme<ChatTheme>('chat', customTheme)` from reablocks, so it picks up the same theme provider as the rest of the chat.

Render it outside `<Chat>` (as a sibling header) or inside the panel — it has no context dependency.

## Theme key

```
theme.appbar
```
