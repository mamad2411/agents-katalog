# Error Boundary Implementation

## Purpose
Implements React error boundaries at appropriate levels to handle runtime failures gracefully.

## Role
Frontend Developer

## Phase
Development

## Triggered By
Any new page, module, or complex component created.

## Inputs
- App/module/component structure

## Process

### Error Boundary Levels
- App level: catches catastrophic errors (shows generic "something went wrong")
- Module level: catches module-specific errors (module fails, rest of app works)
- Component level: catches component errors (component fails gracefully)

Logging: all caught errors logged to Loki via `logging-implementation`.

### Pattern
```typescript
// shared/components/ErrorBoundary.tsx
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    // Log to Loki via logging helper
    logger.error('React error boundary caught', { error, info })
  }

  render() {
    if (this.state.hasError) return <this.props.fallback error={this.state.error} />
    return this.props.children
  }
}
```

Apollo errors: handle in hooks using `error` from `useQuery`/`useMutation`. Don't let Apollo errors bubble to error boundaries — handle explicitly.

## Outputs
App, module, and component-level error boundaries with fallback UI.

## Quality Gates
- [ ] App-level error boundary wraps the entire app
- [ ] Module-level boundaries on all feature modules
- [ ] Errors logged to Loki
- [ ] Fallback UI at each boundary level

## References
- `.claude/skills/frontend-developer/logging-implementation/SKILL.md`
