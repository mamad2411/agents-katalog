---
description: Dialog action button patterns for mobile-friendly UX and consistent styling.
globs: "app/**/*.tsx, components/**/*.tsx"
alwaysApply: false
---

## Dialog action buttons (mandatory)

### Mobile spacing
- Use `gap-3` for vertical stacking on mobile, `sm:gap-2` for horizontal on desktop.
- Pattern: `className="flex flex-col gap-3 pt-4 sm:flex-row sm:gap-2"`

### Destructive actions require confirmation
- **Reset** and **delete** actions must show a confirmation dialog before executing.
- Use a state variable (e.g., `showResetConfirm`) to control the confirmation dialog.
- Confirmation dialog should have Cancel and Confirm buttons.

### Primary/CTA buttons use `brand` variant
- The primary action button (Save, Confirm, Submit) must use `variant="brand"`.
- Secondary actions (Cancel, Reset) use `variant="outline"` or `variant="destructive"`.

### Confirmation dialog button order
- Cancel button comes first (left on desktop, top on mobile).
- Destructive/confirm action comes last (right on desktop, bottom on mobile).
- Use `sm:justify-end` to align buttons to the right on desktop.

### Example:

```tsx
{/* Actions in main dialog */}
<div className="flex flex-col gap-3 pt-4 sm:flex-row sm:gap-2">
  <Button
    variant="outline"
    onClick={() => setShowResetConfirm(true)}
    className="flex-1 gap-2"
  >
    <RotateCcw size={16} />
    Reset to Defaults
  </Button>
  <Button
    variant="brand"
    onClick={handleSave}
    className="flex-1 gap-2"
  >
    <Save size={16} />
    Save
  </Button>
</div>

{/* Confirmation dialog */}
{showResetConfirm && (
  <Dialog open={true} onOpenChange={() => setShowResetConfirm(false)}>
    <DialogContent title="Reset to defaults?">
      <p>This will reset all preferences to their default values.</p>
      <div className="flex flex-col gap-3 pt-4 sm:flex-row sm:justify-end sm:gap-2">
        <Button
          variant="outline"
          onClick={() => setShowResetConfirm(false)}
          className="gap-2"
        >
          <X size={16} />
          Cancel
        </Button>
        <Button
          variant="destructive"
          onClick={() => {
            handleReset();
            setShowResetConfirm(false);
          }}
          className="gap-2"
        >
          <RotateCcw size={16} />
          Reset
        </Button>
      </div>
    </DialogContent>
  </Dialog>
)}
```
