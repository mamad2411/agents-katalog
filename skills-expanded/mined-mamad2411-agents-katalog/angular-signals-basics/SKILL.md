---
name: angular-signals-basics
description: >
  Angular Signals basics for owned apps: signal/computed/effect, OnPush interoperability,
  migrating from RxJS-heavy patterns where appropriate, and avoiding effect anti-patterns.
  Use when adopting Signals for local state and performance-friendly reactivity — not as a
  replacement for Angular security review.
---

# Angular Signals Basics

## Scope And Authorization

- **In scope:** Angular codebases you maintain.
- **Out of scope:** Blind rewrites of production without tests; using this skill for XSS (see security skill).
- Prefer incremental migration with feature flags.
- Pair with `code-quality-standards` and `typescript-style-and-eslint`.

## When To Use

- Introducing `signal`, `computed`, `effect` in components/services.
- Replacing simple `BehaviorSubject` local state with Signals.
- Improving change detection with Signals + OnPush.
- Debugging infinite `effect` loops or impure effects.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Angular XSS/CSRF/auth | `angular-security-basics` |
| SSR hydration | `angular-ssr-hydration` |
| Global state architecture debates | `state-management-guidelines` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| API | Role |
| --- | --- |
| `signal(v)` | Writable reactive value |
| `computed(() => …)` | Derived pure value |
| `effect(() => …)` | Side effects (use sparingly) |
| `update` / `set` / `mutate` | Write patterns (API evolves) |
| RxJS interop | `toSignal` / `toObservable` when needed |
| Inputs as signals | `input()` signal inputs (modern Angular) |

## Workflow

### 1. Confirm version and success criteria

1. Record Angular version (Signals maturity differs).
2. Success: clearer local state; fewer manual subscriptions; tests green; no effect-driven spaghetti.
3. Choose pilot component (non-critical).

### 2. Local state with signals

```typescript
import { signal, computed } from '@angular/core';

const count = signal(0);
const double = computed(() => count() * 2);

count.set(1);
count.update(v => v + 1);
// template: {{ count() }} {{ double() }}
```

### 3. Effects — disciplined use

```typescript
import { effect } from '@angular/core';

// OK: sync to logging/analytics/localStorage with care
effect(() => {
  const v = count();
  console.debug('count', v);
});

// Bad: fetch in effect without coordination → loops/races
// Prefer explicit event handlers / rx resource patterns for async
```

| Rule | Why |
| --- | --- |
| Keep effects pure-ish | Avoid writing multiple signals that re-trigger unboundedly |
| Don’t replace all RxJS | Streams, cancellation, complex async still RxJS-friendly |
| Prefer computed | Derived state should not be effect+set |

### 4. Interop with RxJS

```typescript
import { toSignal } from '@angular/core/rxjs-interop';
const data = toSignal(this.api.getItems(), { initialValue: [] });
```

1. Specify `initialValue` / `requireSync` carefully.
2. Unsubscribe concerns handled by interop when used correctly — still avoid leaks in manual subs.

### 5. Migration strategy

1. New code: signals for component-local UI state.
2. Shared async domain state: keep established store/Rx patterns until ready.
3. Convert one service at a time; keep public API stable.
4. Enable strict templates; fix `count` vs `count()` mistakes.

### 6. Verify

```bash
ng test
ng build --configuration production
# Manual: UI updates on signal set; no CD thrash; no infinite loops
```

### 7. Hand off

1. Team convention doc: when signal vs RxJS.
2. Lint for excessive effects if available.
3. Security still via `angular-security-basics`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Derived state | `computed` | `effect` that `set`s derived |
| Async | Explicit load methods / rx | Unbounded fetch in effect |
| Migration | Incremental pilot | Big-bang rewrite |
| Templates | Call signals as functions | Forget `()` and wonder |

## Output Checklist

- [ ] Angular version supports planned Signals features
- [ ] Pilot component migrated with tests
- [ ] computed used for derived values
- [ ] effects limited and reviewed
- [ ] RxJS interop boundaries clear
- [ ] Build/test green
- [ ] Team conventions documented
- [ ] `code-quality-standards` applied

## Rules

- Owned codebases only.
- Prefer computed over effect for derived state.
- Do not treat Signals as a security control.
- Migrate incrementally with tests.
- Keep async cancellation and error handling explicit.
