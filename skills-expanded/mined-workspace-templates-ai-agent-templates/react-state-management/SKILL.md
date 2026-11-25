---
name: react-state-management
description: Chooses local state, context, a reducer or a store for each piece of React state and removes prop drilling without adding a library by habit.
---

# React state management

Put state in the lowest place that works. Add machinery only when that fails.

## Steps

1. Inventory the state. List each piece with its owner, readers and source. Classify it: server data (from an API), URL state (filters, page, tab), form state, UI state (open, hover), or true app state (session, theme, cart).
2. Choose the home for each kind:
   - Server data goes to a query library such as TanStack Query or SWR, not to a store. Cache, refetch and invalidate there.
   - URL state lives in the router or search params so links and the back button work.
   - Form state stays in the form, or a form library for large forms.
   - UI state stays local with `useState`, lifted only to the nearest common parent.
   - Complex transitions with several related values use `useReducer` with a typed action union.
   - App state shared by distant components goes to context for rarely changing values, or a small store (Zustand, Jotai, Redux Toolkit) when many components read changing values.
3. Remove prop drilling by composition first: pass components or `children` instead of data through layers. Add context after that.
4. Split contexts by concern and by update rate. Memoize the provider value. Expose a custom hook that throws outside the provider.
5. Do not store derived data; compute it. Keep state normalized and minimal.
6. Migrate one slice per commit and run the tests after each.

## Rules

- No new dependency without saying what it replaces.
- Never mirror props into state.

## Report

A table of state, old home, new home and reason, plus what was left alone.
