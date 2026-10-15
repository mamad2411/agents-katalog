---
name: api-client-integration
category: frontend
description: Use when a component talks to the backend - go through the typed api client, type every response, and handle loading, success, and error states explicitly
tech_stack: React
---
# API Client Integration

## Overview

Every remote call is three states, not one. The recurring defects are raw `fetch` scattered in components, untyped responses, and errors swallowed into `console.log` while the UI half-updates.

**Core principle:** One typed client, three states (loading/success/error), no swallowed errors.

## Rules

- **Go through `web/src/api.ts`** helpers — never raw `fetch` in components.
- **Type every response** with an interface matching the backend JSON. A contract change starts by updating the interface so the compiler finds every affected usage.
- **Handle all three states:** loading (visible feedback), success, and error (toast with an actionable message).
- **Never swallow errors** into `console.log` — surface them to the user and keep the UI consistent (no half-updated state on failure).
- **Debounce** user-driven queries; cancel or ignore stale responses when inputs change quickly.

## Worked Example

```tsx
// ✅ typed client call, three states, no half-update on failure
const [state, setState] = useState<Loadable<Task[]>>({ status: "loading" });

useEffect(() => {
  let active = true;
  api.listTasks(projectId)                       // typed helper from api.ts
    .then(tasks => active && setState({ status: "ok", data: tasks }))
    .catch(err => active && setState({ status: "error", message: err.message }));
  return () => { active = false; };              // ignore stale response
}, [projectId]);

if (state.status === "loading") return <Spinner />;
if (state.status === "error") return <ErrorView message={state.message} />;
return <TaskList tasks={state.data} />;          // success only
```

The `active` flag drops a stale response when `projectId` changes; the error branch shows a real message instead of leaving a spinner or a half-list.

## Common Mistakes

- Raw `fetch` in a component.
- Untyped/`any` response.
- Only rendering the success path — no loading/error.
- `catch(e => console.log(e))` with the UI left inconsistent.
- No stale-response guard on fast-changing inputs.

## Red Flags

- `fetch(` inside a component file.
- A remote call with no error UI.
- A toast that says "error" with no actionable message.
