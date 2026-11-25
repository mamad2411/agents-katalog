# MessageStatus

Status banner with optional sub-steps — typically used to show tool / agent progress inside a streaming response (similar to "Searching the web…" / "Reading file…" patterns). Reads `theme.status` from `ChatContext` (or falls back to default).

## Imports

```tsx
import { MessageStatus, MessageStatusItem, StatusIcon } from 'reachat';
import type { MessageStatusState, MessageStatusStep } from 'reachat';
```

## Types

```ts
type MessageStatusState = 'loading' | 'complete' | 'error';

interface MessageStatusStep {
  id: string;
  text: string;
  status?: MessageStatusState;  // default 'loading'
}
```

## MessageStatus Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `string` | — | Main status text (required) |
| `status` | `MessageStatusState` | `'loading'` | Drives the icon and text color |
| `steps` | `MessageStatusStep[]` | — | Optional ordered sub-steps |
| `icon` | `ReactNode` | derived | Custom icon — overrides the default `StatusIcon` |
| `className` | `string` | — | Class for the container |
| `children` | `ReactNode` | — | Override the entire body (Radix `Slot`) |

Animations: enter / exit fade + 10px slide via Framer Motion.

## Default usage

```tsx
<MessageStatus
  status="loading"
  text="Searching the web"
  steps={[
    { id: '1', text: 'Querying index', status: 'complete' },
    { id: '2', text: 'Reading top results', status: 'loading' },
    { id: '3', text: 'Drafting summary' }
  ]}
/>
```

When the run completes:

```tsx
<MessageStatus
  status="complete"
  text="Found 12 results"
  steps={steps.map(s => ({ ...s, status: 'complete' }))}
/>
```

## MessageStatusItem

Renders one row of `steps` — used internally by `MessageStatus`. Exposed for custom layouts.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `step` | `MessageStatusStep` | — | The step to render |

## StatusIcon

Status-aware icon. Renders different SVGs for `loading` (spinner), `complete` (check), `error` (cross).

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `state` | `MessageStatusState` | — | Which icon to render |
| `className` | `string` | — | Outer class (e.g. for size) |
| `colorClassName` | `string` | — | Color classes (typically `theme.status.icon[state]`) |

## Theme keys

```
theme.status.{base, header}
theme.status.icon.{base, loading, complete, error}
theme.status.text.{base, loading, complete, error}
theme.status.steps.base
theme.status.steps.step.{base, icon, text, loading, complete, error}
```
