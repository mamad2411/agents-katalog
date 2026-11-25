---
name: react-stable-keys-state-persistence
description: |
  Fix React component state resetting on page reload when using identifiers that change between
  renders (like messageId from Zustand hydration vs server). Use when: (1) component state shows
  correctly then reverts on reload, (2) localStorage/server state uses unstable keys, (3) Zustand
  hydrates from localStorage before server data arrives causing ID mismatch, (4) state persists
  in one layer but not another due to key differences. Solution: create content-based stable keys
  from immutable component parameters.
author: Claude Code
version: 1.0.0
date: 2026-02-03
---

# React Stable Keys for State Persistence

## Problem

Component state resets on page reload even though data exists in localStorage or server.
The component briefly shows correct state, then reverts to initial state.

## Context / Trigger Conditions

- Component displays correct persisted state momentarily, then resets
- Console shows multiple loads with different IDs for the same component
- Using Zustand with localStorage persistence + server-side state
- State key depends on an identifier (messageId, sessionId) that can differ between:
  - Initial Zustand hydration (from localStorage, happens synchronously)
  - Server-provided data (arrives asynchronously)
- Different state layers (localStorage vs server) use different keys

## Root Cause

When using Zustand with `persist` middleware:

1. **Synchronous hydration**: Zustand hydrates from localStorage immediately on load
2. **Async server data**: Server messages arrive later with potentially different IDs
3. **Key mismatch**: Component mounts with localStorage messageId, then remounts with server messageId
4. **State loss**: Second mount uses different key, finds no persisted state

Example timeline:
```
T0: Page loads
T1: Zustand hydrates from localStorage (messageId: "abc-123")
T2: Component mounts, loads state for "abc-123" ✓ (finds data)
T3: Server messages arrive (messageId: "xyz-789")
T4: Component remounts with new messageId
T5: Component loads state for "xyz-789" ✗ (no data)
T6: Component shows initial state (regression)
```

## Solution

Create a **content-based stable key** from immutable component parameters instead of
using potentially unstable identifiers:

```typescript
/**
 * Create a stable key from component content (not messageId which can change on reload)
 */
function createStableKey(
  action: string,
  parameters: string,
  chatId?: string
): string {
  // Extract a unique identifier from parameters
  let uniqueContent = ''
  try {
    const params = JSON.parse(parameters)
    uniqueContent = params.projectUri || params.id || ''
  } catch {
    uniqueContent = parameters
  }

  // Create a simple hash from stable content
  const input = `${chatId || 'nochat'}:${action}:${uniqueContent}`
  let hash = 0
  for (let i = 0; i < input.length; i++) {
    const char = input.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // Convert to 32bit integer
  }
  return `key-${Math.abs(hash).toString(36)}`
}

// Usage in component
const stableKey = useMemo(
  () => createStableKey(action, parameters, chatId),
  [action, parameters, chatId]
)

// Use stableKey instead of messageId for state persistence
const { data, saveData } = usePersistentState({
  key: stableKey,  // Not messageId!
  // ...
})
```

## Two-Layer Deduplication Pattern

For side effects (like sending follow-up messages), use both:

1. **Refs** for same-session deduplication (prevents double-fires within render cycle)
2. **localStorage** for cross-reload deduplication (survives page refresh)

```typescript
// Ref for same-session
const hasTriggeredRef = useRef(false)

// localStorage key using stable key
const flagsKey = `app:flags:${stableKey}`

const getFlags = useCallback(() => {
  try {
    const stored = localStorage.getItem(flagsKey)
    return stored ? JSON.parse(stored) : {}
  } catch { return {} }
}, [flagsKey])

const setFlag = useCallback((flag: string) => {
  try {
    const current = getFlags()
    localStorage.setItem(flagsKey, JSON.stringify({ ...current, [flag]: true }))
  } catch {}
}, [flagsKey, getFlags])

// In effect
useEffect(() => {
  if (hasTriggeredRef.current) return  // Same-session guard

  const flags = getFlags()
  if (flags.hasTriggered) {  // Cross-reload guard
    hasTriggeredRef.current = true
    return
  }

  hasTriggeredRef.current = true
  setFlag('hasTriggered')

  // Trigger side effect...
}, [dependencies])
```

## Verification

After implementing:
1. Complete the action (e.g., deploy a project)
2. Verify state shows correctly
3. Refresh the page
4. State should persist without briefly reverting

Console should NOT show multiple different IDs loading state for the same component.

## Example

Before (broken):
```typescript
// messageId changes between localStorage hydration and server
const { state } = useComponentState({
  key: messageId,  // Unstable!
})
```

After (fixed):
```typescript
// stableKey is content-based and never changes
const stableKey = useMemo(
  () => createStableKey(action, parameters),
  [action, parameters]
)

const { state } = useComponentState({
  key: stableKey,  // Stable!
})
```

## Notes

- This pattern applies whenever you have multiple sources of truth for identifiers
- The stable key should be derived from CONTENT that doesn't change, not from IDs
- For Juicebox deployments, `projectUri` (IPFS hash) is ideal - it's unique per deployment
- Keep server-persisted state as a secondary layer; localStorage with stable keys is primary
- Consider cleaning up localStorage entries periodically to prevent bloat

## Related Patterns

- Zustand persist middleware hydration timing
- React strict mode double-mount behavior
- Server-client state synchronization
- Content-addressable storage (similar concept)
