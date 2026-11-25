---
name: add-loading-states
description: Adds loading, empty and error states to a view that fetches data, using the spinners, skeletons and messages the app already has.
disable-model-invocation: true
---

Add loading, empty and error states to the view: $ARGUMENTS

1. Read the view and trace where its data comes from (hook, loader, store, fetch call). Note what the code currently does while pending, on an empty result and on failure.
2. Search the codebase for existing patterns: skeleton or spinner components, empty-state illustrations, error banners, toast helpers. Reuse them; create a new component only if none exists.
3. Implement: a loading state that matches the final layout size to avoid jumps; an empty state with a short message and the next action; an error state with the reason in plain words and a retry button that calls the same fetch.
4. Mark loading regions with `aria-busy` and announce errors with `role="alert"`. Do not show a spinner for requests under about 300 ms if the app has a delay helper.
5. Add or update tests for the three states using the project's mocking approach.

Run the tests and type check. Report which states were missing, what was reused, and anything in the data layer you did not change.
