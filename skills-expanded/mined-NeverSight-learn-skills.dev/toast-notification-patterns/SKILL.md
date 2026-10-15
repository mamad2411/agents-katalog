---
name: toast-notification-patterns
description: Toast notifications, snackbars, alerts, and system feedback patterns
license: MIT
---

# Toast & Notification Patterns

## 1. Toast Types

**Success** - Confirmation of completed actions
**Error** - Critical failures requiring attention
**Warning** - Important non-critical issues
**Info** - Neutral system messages
**Loading** - In-progress operations with optional progress indicator

## 2. Toast Anatomy

```tsx
interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info' | 'loading';
  message: string;
  description?: string;
  icon?: React.ReactNode;
  action?: { label: string; onClick: () => void };
  dismissible?: boolean;
  duration?: number;
  progress?: number; // 0-100 for loading toasts
}
```

**Core Elements:**
- Icon (type-specific, 16-20px)
- Message (bold, 14px)
- Description (optional, muted, 13px)
- Action button (optional, primary action)
- Dismiss button (X icon, always visible for errors)
- Progress bar (bottom edge, for timed auto-dismiss)

## 3. Positioning & Stacking

**Preferred positions:**
- `top-right` - Default, least intrusive
- `bottom-center` - Mobile-friendly, undo actions
- `top-center` - Critical system alerts

**Stacking behavior:**
```tsx
// Max 3 visible, newest on top
const MAX_VISIBLE = 3;
const STACK_OFFSET = 8; // px between toasts
const STACK_DIRECTION = 'down'; // or 'up' for bottom positioning
```

Toasts stack vertically with 8px gap. When exceeding max, oldest dismissed first (FIFO).

## 4. Timing Rules

```tsx
const DURATIONS = {
  success: 3000,   // 3s - Quick confirmation
  info: 4000,      // 4s - More reading time
  warning: 6000,   // 6s - Important message
  error: Infinity, // Persist until user dismisses
  loading: Infinity // Persist until operation completes
};
```

**Auto-dismiss logic:**
- Pause timer on hover/focus
- Resume on mouse leave
- Reset on content update
- Manual dismiss always available (except loading)

## 5. Accessibility

```tsx
<div
  role="alert"
  aria-live="polite" // 'assertive' for errors
  aria-atomic="true"
  className="toast"
>
  <svg aria-hidden="true">{icon}</svg>
  <div>
    <p className="font-semibold">{message}</p>
    {description && <p className="text-sm text-muted">{description}</p>}
  </div>
  <button aria-label="Dismiss notification">{dismissIcon}</button>
</div>
```

**Focus management:**
- Errors: Move focus to toast on appear (if user not typing)
- Actions: Button must be keyboard accessible
- Dismiss: ESC key dismisses focused toast

## 6. Code Examples

```tsx
// Toast Provider
export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((toast: Omit<Toast, 'id'>) => {
    const id = crypto.randomUUID();
    setToasts(prev => [{ ...toast, id }, ...prev].slice(0, MAX_VISIBLE));
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ addToast, removeToast }}>
      {children}
      <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
        {toasts.map((toast, idx) => (
          <ToastItem key={toast.id} toast={toast} onDismiss={removeToast} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

// Hook
export const useToast = () => useContext(ToastContext);
```

## 7. Toast Queue Management

**Deduplication strategy:**
```tsx
const addToast = (toast: Omit<Toast, 'id'>) => {
  setToasts(prev => {
    // Remove duplicate messages within 5s window
    const isDuplicate = prev.some(t => 
      t.message === toast.message && 
      Date.now() - t.createdAt < 5000
    );
    if (isDuplicate) return prev;
    
    return [{ ...toast, id: uuid(), createdAt: Date.now() }, ...prev]
      .slice(0, MAX_VISIBLE);
  });
};
```

**Priority system:**
Errors > Warnings > Loading > Success > Info

## 8. Action Toasts

**Undo pattern:**
```tsx
toast.success('Item deleted', {
  action: { 
    label: 'Undo', 
    onClick: () => restoreItem(id) 
  },
  duration: 8000 // Longer for user to react
});
```

**Retry pattern:**
```tsx
toast.error('Upload failed', {
  action: { 
    label: 'Retry', 
    onClick: () => retryUpload() 
  },
  duration: Infinity
});
```

## 9. Persistent vs Transient

**Use persistent (no auto-dismiss) for:**
- Errors requiring user action
- Loading states
- Toasts with action buttons (undo, retry)
- Form validation summaries

**Use transient (auto-dismiss) for:**
- Success confirmations
- Informational updates
- Non-critical warnings
- Progress milestones

## 10. Audit Checklist

- [ ] **[CRITICAL]** Errors persist until manually dismissed
- [ ] **[CRITICAL]** All interactive elements keyboard accessible (Tab, Enter, ESC)
- [ ] **[CRITICAL]** role="alert" and aria-live present
- [ ] **[MAJOR]** Icons have aria-hidden="true"
- [ ] **[MAJOR]** Dismiss buttons have aria-label
- [ ] **[MAJOR]** Auto-dismiss pauses on hover/focus
- [ ] **[MAJOR]** Maximum 3 toasts visible simultaneously
- [ ] **[MAJOR]** Toast width constrained (max 400px)
- [ ] **[MINOR]** Success toasts auto-dismiss in 3-4s
- [ ] **[MINOR]** Toast animates in/out smoothly (200-300ms)
- [ ] **[MINOR]** Duplicate messages within 5s deduplicated
- [ ] **[MINOR]** Loading toasts show progress indicator
- [ ] **[MINOR]** Action toasts have 6-8s duration minimum
- [ ] **[MINOR]** Mobile: Bottom positioning preferred
- [ ] **[MINOR]** Color contrast meets WCAG AA (4.5:1)
