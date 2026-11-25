---
name: "Component Lifecycle Manager"
version: "1.0.0"
description: "Manages component lifecycle from creation to destruction. Handles initialization, mounting, updating, and cleanup patterns across React, Vue, and vanilla JS."
author: "workspace"
activated: false
---

# Component Lifecycle Manager

Manages component lifecycle from creation to destruction. Handles initialization, mounting, updating, and cleanup patterns across React, Vue, and vanilla JS.

## Decision Framework

### When to Apply
Use when: Complex components with side effects, subscriptions, timers, or external resources requiring cleanup

### When NOT to Apply
Don't use when: Simple stateless presentational components

## Anti-Patterns

### 1. Memory Leaks
```javascript
// BAD: No cleanup
componentDidMount() {
  window.addEventListener('resize', this.handleResize);
}
// GOOD: Always clean up
componentWillUnmount() {
  window.removeEventListener('resize', this.handleResize);
}
```

### 2. Unnecessary Re-renders
```javascript
// BAD: New object every render
<Component style={{ color: 'red' }} onClick={() => doSomething()} />

// GOOD: Memoize
const style = useMemo(() => ({ color: 'red' }), []);
const handleClick = useCallback(() => doSomething(), []);
```


## Trigger Phrases

- "Component lifecycle"
- "Mount/unmount"
- "useEffect cleanup"
- "Memory leak"
- "Re-render optimization"

## Patterns

### Effect Lifecycle (React)
```javascript
useEffect(() => {
  const controller = new AbortController();
  fetchData(controller.signal);
  return () => controller.abort(); // cleanup
}, [dependency]);
```

### Mount/Unmount Hooks
```javascript
function useMountUnmount(onMount, onUnmount) {
  useEffect(() => {
    onMount?.();
    return () => onUnmount?.();
  }, []);
}
```

## Integration
- Works with: state-machine-designer, performance-budget-enforcer

