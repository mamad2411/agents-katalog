---
name: react-hooks-patterns
description: Writes custom React hooks with honest dependency arrays, proper cleanup and no stale closures, and fixes effects that misuse useEffect.
---

# React hooks patterns

Most effects should not exist. Write the ones that do so they are safe to run twice.

## Steps

1. For every `useEffect` ask what it synchronizes with. If the answer is "state with other state", delete it and compute the value during render, or use `useMemo` if it is costly. If the answer is "a user action", move it into the event handler.
2. For real synchronization (subscription, timer, network, DOM API) write setup and cleanup as a pair. Unsubscribe, clear timers, abort fetches with `AbortController`, and ignore results of outdated requests.
3. Make the dependency array complete. Never silence `react-hooks/exhaustive-deps`. If a dependency causes unwanted reruns, fix its source: move the object or function inside the effect, memoize it at the owner, or read the latest value through a ref (`useRef` updated in an effect) or `useEffectEvent` where available.
4. Prevent stale closures: use the functional form `setCount(c => c + 1)` when new state depends on old state, and do not capture props in long-lived callbacks without listing them.
5. Extract a custom hook only when logic repeats or hides a lifecycle. Name it `useThing`, return a stable shape (object for many values, tuple for two), and keep it free of JSX.
6. Verify in Strict Mode: mount, unmount, remount must leave no duplicate listeners or requests.

## Rules

- Hooks are called at the top level, never in conditions or loops.
- Do not fetch in effects if the project has a data library; use it.
- Add a test with `renderHook` for each new hook.

## Report

Effects removed, hooks extracted, bugs fixed and tests added.
