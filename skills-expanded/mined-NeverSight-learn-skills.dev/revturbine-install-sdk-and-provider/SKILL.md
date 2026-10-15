---
name: revturbine-install-sdk-and-provider
description: >
  Install @revturbine/sdk and mount <RevTurbineProvider> at the app root with a
  user identified. Use when adding RevTurbine to an app for the first time, when
  "the provider isn't set up", or when RevTurbine hooks/components throw because
  no provider is mounted. Writes app code — a provider wrapper and a user
  context. Skip if <RevTurbineProvider> already wraps the app; go straight to
  wiring the Playbook or adding a gate.
license: MIT
metadata:
  author: revturbine
  version: "0.1.0"
  safety_class: writes-app-code
---

# Install the SDK and mount the provider

Get `<RevTurbineProvider>` wrapping the app with a user identified. This is the
prerequisite for every gate, slot, and entitlement check.

Follow **`revturbine-integration-best-practices`** throughout — especially
additive-only: the app must still render if the provider is removed.

## 1. Install the SDK

Use the app's package manager (detect it from the lockfile):

```bash
npm install @revturbine/sdk      # or: pnpm add / yarn add
```

If the app was scaffolded with `npm create revturbine`, the SDK is already a
dependency — skip this step.

## 2. Mount the provider at the app root

Wrap the top of the component tree. Provider options are memoized so the runtime
isn't rebuilt on every render:

```tsx
import { RevTurbineProvider } from '@revturbine/sdk';
import { useMemo } from 'react';

function Root({ children }) {
  const options = useMemo(() => ({
    // Identify the current user and the traits RevTurbine segments/gates on.
    // `plan_handle` matters most — it decides what the user is entitled to.
    user: {
      id: currentUser.id,
      context: { plan_handle: currentUser.planHandle ?? 'free' },
    },
    // Where a CTA should send the user when a placement fires. Wire these to
    // your real routes; a gate's upgrade button is inert without them.
    uiPathResolvers: {
      navigate_to_plans: () => { window.location.href = '/pricing'; },
    },
  }), []);

  return <RevTurbineProvider options={options}>{children}</RevTurbineProvider>;
}
```

Mount it in the framework's root: `app/layout.tsx` (Next.js App Router),
`pages/_app.tsx` (Pages Router), or wherever the tree begins.

> **This step does not yet make RevTurbine resolve anything** — it has no config
> to decide against. That is the next skill (`revturbine-run-local-playbook`),
> which adds `localRuntime` so decisions work with no account.

## 3. Keep it additive

- Do not make any existing component *require* the provider to render. Gating
  is added later, at specific call sites — not by the provider's presence.
- Use the real signed-in user where you have one; a placeholder id is fine only
  for a first local run.

## Verify

The app builds and renders exactly as before — the provider is inert until a
Playbook and a gate are wired. Nothing should look different yet; that is
correct.
