# ConfirmDialog

Confirmation dialog with accept/reject actions. Built on Dialog. Also exports `useConfirmDialog` hook for imperative usage.

## Import

```tsx
import { ConfirmDialog, useConfirmDialog } from 'reablocks';
```

## ConfirmDialog Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `boolean` | — | Whether the dialog is open |
| `header` | `string \| ReactNode` | — | Dialog header |
| `content` | `string \| ReactNode` | — | Dialog body content |
| `confirmLabel` | `string` | `'Confirm'` | Confirm button text |
| `cancelLabel` | `string` | `'Cancel'` | Cancel button text |
| `variant` | `'default' \| 'destructive'` | `'default'` | Visual variant — `destructive` colors the confirm button as `error` for delete-style actions |
| `onConfirm` | `() => void` | — | Confirm callback |
| `onCancel` | `() => void` | — | Cancel callback (also closes the dialog) |

## Basic Usage

```tsx
const [open, setOpen] = useState(false);

<ConfirmDialog
  open={open}
  header="Save Changes"
  content="Save your changes before continuing?"
  onConfirm={() => { save(); setOpen(false); }}
  onCancel={() => setOpen(false)}
/>
```

## Destructive Variant

Use `variant="destructive"` for dangerous actions (delete, remove, etc.). The confirm button renders with the error color.

```tsx
<ConfirmDialog
  open={open}
  variant="destructive"
  header="Delete Item"
  content="This action cannot be undone."
  confirmLabel="Delete"
  onConfirm={() => { deleteItem(); setOpen(false); }}
  onCancel={() => setOpen(false)}
/>
```

## useConfirmDialog Hook

Imperative API for opening confirm dialogs without managing state:

```tsx
const { openDialog, closeDialog, DialogComponent } = useConfirmDialog();

<Button onClick={() => openDialog({
  header: 'Confirm Action',
  content: 'Are you sure?',
  onConfirm: () => { doAction(); closeDialog(); },
  onCancel: () => closeDialog()
})}>
  Delete
</Button>

<DialogComponent />
```

### Hook Returns

| Property | Type | Description |
|----------|------|-------------|
| `isOpen` | `boolean` | Current open state |
| `openDialog` | `(props: OpenConfirmDialogProps) => void` | Open with props |
| `closeDialog` | `() => void` | Close the dialog |
| `DialogComponent` | `FC` | Render this in your JSX |
