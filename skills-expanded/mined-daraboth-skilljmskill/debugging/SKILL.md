---
name: debugging
description: Systematic 5-step workflow (Reproduce → Isolate → Identify → Fix → Verify) for finding and fixing bugs in code. Use when the user reports a crash, error, stack trace, unexpected output, regression ("used to work"), flaky behavior, or performance issue — in JavaScript, Java, or any language. Also trigger when the user says "debug this", "why is X broken", or pastes an error message. Forbids guessing fixes without reproducing the bug first.
---

# Skill: Debugging

> **Purpose**: Find and fix bugs systematically. Never guess.

## When to Use
- App crashes or throws errors
- Wrong output from code
- Something "used to work" but doesn't
- Performance issues

---

## 5-Step Workflow

### 1. REPRODUCE
Trigger the bug reliably. Write exact steps.
```javascript
fetchUser(undefined); // → TypeError
```

### 2. ISOLATE
Find the smallest code that fails. Use binary search — comment out half, test, repeat.

### 3. IDENTIFY
Ask: What did I expect? What happened? Why?
```
Expected: fetchUser(1) → { id: 1, name: "John" }
Actual:   fetchUser(undefined) → SyntaxError
Root cause: No input validation. undefined becomes "/api/users/undefined"
```

### 4. FIX
Apply the minimal correct fix. Don't refactor during debugging.
```javascript
async function fetchUser(id) {
  if (!id) throw new Error('fetchUser requires a valid ID');
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
```

### 5. VERIFY
Test: the failing case, the normal case, and edge cases.

---

## Logging Strategy

```javascript
// ❌ Bad
console.log("here");

// ✅ Good — tagged, structured
console.log('[fetchUser] Input:', { id, type: typeof id });
console.error('[fetchUser] Failed:', error.message);
```

```java
System.out.println("[UserService] findById id=" + id);
System.err.println("[UserService] ERROR: " + e.getMessage());
```

---

## Real-World Examples

### NullPointerException (Java)
```java
// Bug: user.getFirstName().toUpperCase() crashes when firstName is null
// Fix: null check
String name = user.getFirstName();
return (name != null) ? name.toUpperCase() : user.getEmail();
```

### Async Bug (JavaScript)
```javascript
// Bug: users is always empty
function loadDashboard() {
  let users = [];
  fetchUsers().then(data => { users = data; });
  renderDashboard(users); // Runs BEFORE fetch completes!
}
// Fix: use await
async function loadDashboard() {
  const users = await fetchUsers();
  renderDashboard(users);
}
```

### Silent Crash
```javascript
// Bug: empty catch swallows errors
try { JSON.parse(input); } catch (e) {} // ← never do this

// Fix: log and handle
try {
  JSON.parse(input);
} catch (error) {
  console.error('[Parser] Invalid input:', error.message);
}
```

---

## Best Practices
1. **Read the full error message** — 80% of bugs are explained by the stack trace
2. **Check recent changes** — `git diff` or `git log -5`
3. **Use breakpoints** — faster than console.log for complex state
4. **One change at a time** — otherwise you can't tell what fixed it
5. **Take a break at 30 min** — fresh eyes find bugs faster

## Common Mistakes
| Mistake | Do This Instead |
|---------|----------------|
| Changing multiple things at once | One change, test, repeat |
| Fixing symptoms not causes | Find root cause |
| No reproduction steps | Write steps before fixing |
| Empty catch blocks | Always log errors |
| Not testing after fixing | Verify with multiple cases |
