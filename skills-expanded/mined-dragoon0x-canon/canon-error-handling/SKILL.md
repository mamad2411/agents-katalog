---
name: canon-error-handling
description: Use when designing error states, error messages, recovery flows, fallback UIs, error boundaries, retry logic, or offline handling. Covers the three-part error message anatomy, inline vs toast vs page errors, error boundaries in React, optimistic-UI rollback, and the retry with backoff pattern. Trigger when the user mentions error, error handling, error state, fallback, retry, offline, or error boundary.
---

# CANON · Error Handling

Errors are inevitable. Showing them well is the difference between a product that feels reliable and one that feels broken.

## Error message anatomy

Every error message answers three questions:

1. **What failed?** — Name the thing. "Couldn't save your changes."
2. **Why?** — Give the cause if known. "The server didn't respond."
3. **How to fix?** — Give the action. "Check your connection and try again."

```
Bad:  "Error."
Bad:  "Something went wrong."
Good: "Couldn't save your changes — connection lost. Check your network and retry."
```

## Error display patterns

| Pattern | Use when |
|---|---|
| Inline (below the field) | Field-level validation errors |
| Banner (top of page/section) | Page-level errors affecting multiple things |
| Toast | Non-critical background errors ("Couldn't sync — retrying") |
| Modal | Critical errors requiring explicit acknowledgment |
| Full page (error page) | Route-level failure (404, 500, auth expired) |
| Error boundary | Component crash that shouldn't take down the page |

## Validation timing

From `canon-forms`:
- Validate on blur (when user leaves the field), not on every keystroke.
- Show error after first submission attempt, then live-validate on change.
- Never show errors before the user has interacted with the field.

## Retry logic

| Strategy | Use |
|---|---|
| Immediate retry button | User-triggered (network errors, form submission) |
| Auto-retry with backoff | Background operations (sync, polling) |
| Retry with exponential backoff | API calls: wait 1s, 2s, 4s, 8s, cap at 30s |
| No retry | Permanent errors (404, auth revoked, validation failure) |

Show the retry state: "Retrying in 3s... [Retry now]"

## Optimistic UI rollback

When using optimistic updates (show success instantly, sync in background), the error case is the rollback:

1. Apply the change immediately in the UI.
2. Send the request.
3. On failure: revert the UI, show a toast explaining what happened.
4. "Couldn't delete item — restored. [Try again]"

## Error boundaries (React)

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error, info) { logErrorToService(error, info); }
  render() {
    if (this.state.hasError) {
      return <ErrorFallback onRetry={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}
```

- Wrap at the feature level, not the app level (one broken widget shouldn't blank the page).
- Fallback UI should have a retry action.
- Log the error to your monitoring service.

## Offline handling

- Detect via `navigator.onLine` + `online`/`offline` events (unreliable alone; also check fetch failures).
- Show a persistent banner: "You're offline. Changes will sync when you're back."
- Queue offline actions, replay on reconnect.
- Never show "Something went wrong" for offline — name it.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "Something went wrong" with no detail | Useless |
| "Error code: 0x80004005" | Meaningless to users |
| "Oops!" / "Uh oh!" | Infantilizing in a frustrating moment |
| Red border only (no text) | Unclear what's wrong or how to fix |
| Error toast for form validation | Wrong pattern; validation is inline |
| Auto-retry without telling the user | Silent failure looks like hang |
| No error boundary (entire app crashes) | One bad component blanks the screen |
| Showing stack traces to users | Security risk + useless |

## Audit checklist

- [ ] Every error message says what, why, and how
- [ ] Inline errors for fields, banners for pages, toasts for background
- [ ] Validation on blur, not on keystroke
- [ ] Retry button for recoverable errors
- [ ] Auto-retry uses exponential backoff with visible state
- [ ] Optimistic UI has a rollback + explanation
- [ ] Error boundaries at feature level (React)
- [ ] Offline state shows a banner, not a generic error
- [ ] No "Oops!", no stack traces, no bare error codes

## Sources

- WCAG 2.2 · 3.3.1 Error Identification, 3.3.3 Error Suggestion
- `canon-ux-writing` for message anatomy
- `canon-states` for empty/error/loading patterns
- React docs · Error Boundaries
