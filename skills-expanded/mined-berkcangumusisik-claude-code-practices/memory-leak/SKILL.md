---
name: memory-leak
description: Finds potential memory leaks - uncleaned listeners, unclosed connections, growing caches
argument-hint: [file-path]
user-invocable: true
allowed-tools: Read Grep Glob
effort: medium
---

## Memory Leak Analysis

Target: **$1** (or `src/` if not specified)

### Pattern 1: Event Listeners Without Cleanup
```ts
// ❌ Listener added but never removed
useEffect(() => {
  window.addEventListener('resize', handler)
}, []) // Missing: return () => window.removeEventListener('resize', handler)
```

### Pattern 2: Timers Not Cleared
```ts
// ❌ Interval runs forever
setInterval(syncData, 5000)

// ✅ Store ref and clear on unmount
const id = setInterval(syncData, 5000)
return () => clearInterval(id)
```

### Pattern 3: Unbounded Caches
```ts
// ❌ Cache grows indefinitely
const cache = new Map()
cache.set(key, value) // never evicted
```

### Pattern 4: Unclosed DB/File Connections
Look for `db.connect()` without corresponding `db.close()` in error paths.

---

For each finding:
1. Show the leaking code
2. Explain what accumulates and why it matters
3. Provide the fix

Rate by severity: **Critical** (crashes in production under load) / **Warning** (gradual degradation) / **Minor** (theoretical).
