---
name: react-error-boundaries
description: Use when a React subtree should fail gracefully instead of blanking the whole app on a render/lifecycle error — class-based ErrorBoundary component with a retry action.
metadata:
  origin: ECC (decomposed from frontend-patterns)
allowed-tools: Read, Edit, Grep, Glob
---

# Error boundary pattern

Error boundaries must be class components (no hook equivalent exists) — `getDerivedStateFromError`
for the fallback render, `componentDidCatch` for logging.

```tsx
interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<{ children: React.ReactNode }, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error boundary caught:', error, errorInfo);
    // also report to your error tracker here
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false })}>Try again</button>
        </div>
      );
    }
    return this.props.children;
  }
}

// <ErrorBoundary><App /></ErrorBoundary>
```

## Placement

- One boundary at the app root as a last-resort catch-all is not enough by itself — wrap
  independent feature sections (a chart, a widget, a routed page) in their own boundary so one
  broken feature doesn't blank the whole screen.
- Error boundaries do **not** catch errors in event handlers, async code, SSR, or the boundary's
  own render — wrap those with regular `try/catch` and set error state normally.
- The "Try again" reset only clears the boundary's own state; if the error came from bad data
  still in a parent store, retrying will immediately re-throw. Pair retry with actually refetching
  or clearing the bad state, not just flipping `hasError` back to false.
