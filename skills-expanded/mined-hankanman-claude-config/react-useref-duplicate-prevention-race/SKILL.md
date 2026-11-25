---
name: react-useref-duplicate-prevention-race
description: |
  Fix React duplicate detection race conditions using useRef for synchronous checks.
  Use when: (1) Rapid successive function calls bypass duplicate/spam detection despite
  state-based checking logic, (2) Rate limiting or cooldown logic fails when triggered
  multiple times quickly, (3) Duplicate items appear in lists despite deduplication code,
  (4) State-based guards don't prevent re-entry in event handlers. Solves race condition
  where multiple calls read the same stale state value before any setState completes.
  Covers React hooks patterns with useRef, useState, useCallback for duplicate prevention,
  spam protection, rate limiting, and synchronous guard checks.
author: Claude Code
version: 1.0.0
date: 2026-02-02
---

# React useRef for Duplicate Prevention Race Conditions

## Problem

When implementing duplicate detection, spam prevention, or rate limiting in React using state, rapid successive function calls can bypass the checks due to React's asynchronous state updates. All calls read the same stale state value before any `setState` completes, allowing duplicates through.

**Common Scenario**: Alert/notification system where rapid form validation errors trigger multiple identical alerts despite duplicate detection logic.

## Context / Trigger Conditions

Use this pattern when you encounter:

1. **Duplicate Detection Failures**:
   - Multiple identical alerts/notifications appear despite deduplication logic
   - Spam prevention allows duplicates when triggered rapidly
   - List deduplication fails for items added in quick succession

2. **State-Based Checks Failing**:
   - Code like `if (recentItems.has(item)) return;` doesn't prevent duplicates
   - Cooldown/rate limiting logic bypassed by rapid clicks
   - Guard clauses using state don't prevent re-entry

3. **Symptoms**:
   - Problem only appears with rapid successive calls (< 100ms apart)
   - Single slow calls work correctly
   - Adding `console.log` shows all calls see the same state value
   - Problem worse in production (React batches updates more aggressively)

4. **Code Patterns That Fail**:
   ```javascript
   // ❌ Race condition: all calls read same stale state
   const [recentItems, setRecentItems] = useState(new Map());

   const addItem = useCallback((item) => {
     if (recentItems.has(item.id)) return; // All calls see same stale Map

     setRecentItems(prev => {
       const next = new Map(prev);
       next.set(item.id, Date.now());
       return next;
     });
   }, [recentItems]); // Recreates callback on every state change!
   ```

## Solution

Use `useRef` for synchronous duplicate checking while keeping state for rendering needs:

### Step 1: Add ref for synchronous tracking

```javascript
import { useRef, useState, useCallback } from 'react';

const [items, setItems] = useState([]);
const recentItemsRef = useRef(new Map()); // Synchronous duplicate tracker
```

### Step 2: Check and update ref synchronously

```javascript
const addItem = useCallback((item) => {
  const now = Date.now();

  // Check ref (synchronous read)
  const lastSeen = recentItemsRef.current.get(item.id);
  if (lastSeen && now - lastSeen < 5000) {
    return; // Duplicate within 5 second window
  }

  // Update ref immediately (synchronous write, prevents race)
  recentItemsRef.current.set(item.id, now);

  // Clean up old entries
  for (const [id, timestamp] of recentItemsRef.current.entries()) {
    if (now - timestamp > 5000) {
      recentItemsRef.current.delete(id);
    }
  }

  // Update state for rendering
  setItems(prev => [...prev, item]);
}, []); // No dependencies - ref is stable!
```

### Step 3: Remove state dependency from useCallback

The key insight: refs don't need to be in the dependency array because they're always the same object reference. This prevents recreating the callback on every state change.

## Complete Example

```javascript
import React, { useRef, useState, useCallback } from 'react';

const DUPLICATE_WINDOW_MS = 5000;

function AlertProvider({ children }) {
  const [alerts, setAlerts] = useState([]);

  // Ref for synchronous duplicate checking
  const recentAlertsRef = useRef(new Map());

  const addAlert = useCallback((alert) => {
    const normalized = `${alert.title}:${alert.message}`.toLowerCase().trim();
    const now = Date.now();

    // Synchronous duplicate check via ref
    const lastShown = recentAlertsRef.current.get(normalized);
    if (lastShown && now - lastShown < DUPLICATE_WINDOW_MS) {
      return ''; // Duplicate detected
    }

    const id = `alert-${now}-${Math.random().toString(36).substr(2, 9)}`;

    // Update ref immediately (synchronous, prevents race)
    recentAlertsRef.current.set(normalized, now);

    // Cleanup old entries from ref
    for (const [key, timestamp] of recentAlertsRef.current.entries()) {
      if (now - timestamp > DUPLICATE_WINDOW_MS) {
        recentAlertsRef.current.delete(key);
      }
    }

    // Update state for rendering
    setAlerts(prev => [...prev, { ...alert, id, timestamp: now }]);

    return id;
  }, []); // No dependencies!

  return (
    <AlertContext.Provider value={{ alerts, addAlert }}>
      {children}
    </AlertContext.Provider>
  );
}
```

## Verification

### Test the fix:

1. **Rapid Click Test**:
   ```javascript
   // Should only create one alert despite 10 rapid calls
   for (let i = 0; i < 10; i++) {
     addAlert({ title: 'Test', message: 'Same message' });
   }
   ```

2. **Console Verification**:
   ```javascript
   const addItem = useCallback((item) => {
     console.log('Ref check:', recentItemsRef.current.has(item.id));
     // Should print: false, true, true, true... for rapid duplicates

     if (recentItemsRef.current.has(item.id)) return;
     recentItemsRef.current.set(item.id, Date.now());
   }, []);
   ```

3. **Success Criteria**:
   - Rapid successive calls with same data create only one item
   - Different data creates multiple items correctly
   - No console warnings about stale closures
   - useCallback has no or minimal dependencies

## Why This Works

**The Race Condition Explained**:
```javascript
// Time 0ms: Call 1 reads state (empty Map)
// Time 1ms: Call 2 reads state (still empty - setState hasn't completed)
// Time 2ms: Call 3 reads state (still empty)
// Time 5ms: Call 1's setState completes
// Time 6ms: Call 2's setState completes (overwrites Call 1)
// Time 7ms: Call 3's setState completes (overwrites Call 2)
// Result: All three calls passed the duplicate check!
```

**With useRef**:
```javascript
// Time 0ms: Call 1 reads ref (empty), writes to ref (has entry)
// Time 1ms: Call 2 reads ref (has entry), returns early
// Time 2ms: Call 3 reads ref (has entry), returns early
// Result: Only Call 1 proceeds. Race condition prevented!
```

**Key Differences**:
- `useState`: Asynchronous updates, batched by React
- `useRef`: Synchronous read/write, immediate mutation
- Refs bypass React's render cycle entirely for the duplicate check
- State still used for rendering (separation of concerns)

## Notes

### When to Use This Pattern

✅ **Good use cases**:
- Duplicate detection (alerts, notifications, toasts)
- Rate limiting (API calls, button clicks)
- Spam prevention (form submissions)
- Cooldown timers (game actions, animations)
- Request deduplication (cache keys, fetch guards)

❌ **Don't use for**:
- Values that affect rendering (use state instead)
- Complex business logic (use state + proper async handling)
- Data that needs to persist across component unmounts (use external storage)

### Performance Considerations

- Refs don't trigger re-renders when mutated (good for frequent updates)
- Map/Set cleanup during each call is O(n) - for large Maps, consider periodic cleanup:
  ```javascript
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      for (const [key, timestamp] of recentItemsRef.current.entries()) {
        if (now - timestamp > DUPLICATE_WINDOW_MS) {
          recentItemsRef.current.delete(key);
        }
      }
    }, 10000); // Clean every 10 seconds

    return () => clearInterval(interval);
  }, []);
  ```

### Related Patterns

1. **AbortController Pattern** (for fetch requests):
   ```javascript
   const abortRef = useRef(null);

   useEffect(() => {
     abortRef.current?.abort();
     abortRef.current = new AbortController();

     fetch('/api', { signal: abortRef.current.signal })
       .then(handleResponse);
   }, [dependency]);
   ```

2. **Boolean Flag Pattern** (for component unmount):
   ```javascript
   const isMountedRef = useRef(true);

   useEffect(() => {
     return () => { isMountedRef.current = false; };
   }, []);

   const fetchData = async () => {
     const data = await fetch('/api');
     if (isMountedRef.current) {
       setData(data); // Only update if still mounted
     }
   };
   ```

3. **Debounce/Throttle with useRef**:
   ```javascript
   const lastCallRef = useRef(0);

   const throttledFunction = useCallback((arg) => {
     const now = Date.now();
     if (now - lastCallRef.current < 1000) return; // Throttle to 1s
     lastCallRef.current = now;

     actualFunction(arg);
   }, []);
   ```

### Common Pitfalls

1. **Forgetting to remove state from dependencies**:
   ```javascript
   // ❌ Bad: recreates callback on state change
   const addItem = useCallback((item) => {
     if (recentItemsRef.current.has(item)) return;
     recentItemsRef.current.set(item, Date.now());
     setItems(prev => [...prev, item]);
   }, [recentItems]); // ← Remove this!

   // ✅ Good: stable callback
   const addItem = useCallback((item) => {
     if (recentItemsRef.current.has(item)) return;
     recentItemsRef.current.set(item, Date.now());
     setItems(prev => [...prev, item]);
   }, []); // No dependencies
   ```

2. **Using state for the check instead of ref**:
   ```javascript
   // ❌ Race condition still exists
   const [recentItems, setRecentItems] = useState(new Set());

   const addItem = useCallback((item) => {
     if (recentItems.has(item)) return; // Reads stale state
     setRecentItems(prev => new Set(prev).add(item));
   }, [recentItems]);
   ```

3. **Not cleaning up old entries**:
   ```javascript
   // ❌ Memory leak: ref grows unbounded
   recentItemsRef.current.set(item.id, Date.now());
   // Missing cleanup!

   // ✅ Cleanup old entries
   for (const [id, timestamp] of recentItemsRef.current.entries()) {
     if (now - timestamp > WINDOW_MS) {
       recentItemsRef.current.delete(id);
     }
   }
   ```

## References

- [Fixing Race Conditions in React with useEffect - Max Rozen](https://maxrozen.com/race-conditions-fetching-data-react-with-useeffect)
- [Avoiding Race Conditions when Fetching Data with React Hooks - DEV](https://dev.to/nas5w/avoiding-race-conditions-when-fetching-data-with-react-hooks-4pi9)
- [Don't Misuse useRef in React: The Practical Guide - DEV](https://dev.to/a1guy/dont-misuse-useref-in-react-the-practical-guide-you-actually-need-5aj6)
- [How to debounce and throttle in React - Developer Way](https://www.developerway.com/posts/debouncing-in-react)
- [Mastering State Updates: Avoiding SetState Race Conditions - InfiniteJS](https://infinitejs.com/posts/mastering-setstate-race-conditions/)
