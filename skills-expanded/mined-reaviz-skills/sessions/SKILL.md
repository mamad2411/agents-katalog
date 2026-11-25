# Sessions

Sessions sidebar — the list of past chats, the new-session trigger, and group-by-date helpers. All read state from `ChatContext`.

## Imports

```tsx
import {
  SessionsList,
  SessionGroups,
  SessionsGroup,
  SessionListItem,
  NewSessionButton
} from 'reachat';
```

## SessionsList

Sidebar wrapper that renders an animated container around its children. Hidden in compact mode while a session is active (so the panel can take over the viewport).

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `templates` | `Template[]` | — | When no session is active, shows clickable template entries that fire `createSession()` |
| `children` | `ReactNode` | — | Usually `<NewSessionButton />` and `<SessionGroups />` |

```tsx
<SessionsList templates={templates}>
  <NewSessionButton />
  <SessionGroups />
</SessionsList>
```

`templates`:

```ts
interface Template {
  id: string;
  title: string;
  message: string;
  icon?: ReactElement;
}
```

## SessionGroups

Groups the context's `sessions` by relative date (Today / Yesterday / This Week / etc.) using the bundled `groupSessionsByDate` utility, and renders `<SessionsGroup>` per heading with `<SessionListItem>` children.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `(groups: GroupedSessions[]) => ReactNode` | — | Render-prop override |

```tsx
<SessionGroups />

// Custom render
<SessionGroups>
  {groups => groups.map(({ heading, sessions }) => (
    <SessionsGroup key={heading} heading={heading}>
      {sessions.map(s => <SessionListItem key={s.id} session={s} />)}
    </SessionsGroup>
  ))}
</SessionGroups>
```

## SessionsGroup

Visual group with a heading. Wraps `SessionListItem`s in a single section.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `heading` | `string` | — | Group heading |
| `children` | `ReactNode` | — | List items |

## SessionListItem

Individual session row. Built on reablocks `ListItem` with start (chat icon) and end (delete icon-button) adornments. Active state is highlighted via theme. Click selects the session; the trash button stops propagation and triggers `deleteSession`.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `session` | `Session` | — | Session data |
| `deletable` | `boolean` | `true` | Show the delete button |
| `deleteIcon` | `ReactElement` | trash icon | Custom delete icon |
| `chatIcon` | `ReactElement` | chat icon | Custom leading icon |
| `limit` | `number` | `100` | Ellipsis cutoff for the title |
| `children` | `ReactNode` | — | Override the entire row content (Radix `Slot`) — title `Ellipsis` is replaced |

```tsx
<SessionListItem session={session} chatIcon={<AppIcon />} />

// Custom item content
<SessionListItem session={session}>
  <div className="flex flex-col">
    <strong>{session.title}</strong>
    <span>{session.conversations.length} messages</span>
  </div>
</SessionListItem>
```

## NewSessionButton

Full-width primary button bound to `createSession()` from context. Shows the plus icon as `start` adornment and respects `disabled` from context.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `newSessionText` | `string \| ReactNode` | `'New Session'` | Default label |
| `children` | `ReactNode` | — | Override the entire button (Radix `Slot`) |

```tsx
<NewSessionButton newSessionText="Start chat" />

// Or wrap a custom trigger
<NewSessionButton>
  <button className="custom-button">+ New chat</button>
</NewSessionButton>
```

## groupSessionsByDate

Exported from `reachat/utils` (re-exported via `reachat`). Buckets sessions by relative date for `SessionGroups`.

```ts
interface GroupedSessions {
  heading: string;
  sessions: Session[];
}

function groupSessionsByDate(sessions: Session[]): GroupedSessions[];
```

## Theme keys

```
theme.sessions.{base, console, companion, group, create}
theme.sessions.session.{base, active, delete}
```
