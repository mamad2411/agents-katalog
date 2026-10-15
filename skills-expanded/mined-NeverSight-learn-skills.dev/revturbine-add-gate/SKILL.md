---
name: revturbine-add-gate
description: >
  Gate one paid action behind an entitlement with <Gate>, showing an upgrade
  surface when denied. Use to "gate a premium feature", "add a paywall", "put an
  upgrade modal on X", or to replace a hard-coded plan check like
  `user.plan === 'pro'`. Writes app code — wraps a call site in <Gate> and keeps
  the existing UI as the granted children. Prerequisite: the provider is mounted
  and a Playbook is loaded (local or hosted). For anything that spends money or
  compute, also add a server re-check (see the Verify section).
license: MIT
metadata:
  author: revturbine
  version: "0.1.0"
  safety_class: writes-app-code
---

# Gate a paid action

Wrap one premium action in `<Gate>`: entitled users see it, everyone else sees an
upgrade surface. This is the first real revenue moment.

Pick **one safe, non-critical action** to start — the export button, an advanced
panel — not a billing-critical or destructive path.

## 1. Confirm the entitlement exists in the Playbook

The gate references an entitlement `handle`. The scaffold's Playbook ships
`advanced_export`, allowed on `pro` and denied on `free`. To gate a *different*
feature, add its entitlement + rule to `revturbine.playbook.json` first (see the
control plane, or author it and `revturbine validate`), then gate it here.

## 2. Replace the hard-coded check with `<Gate>`

Before — a plan check baked into the component:

```tsx
{user.plan === 'pro' ? <ExportControls /> : <UpgradePrompt />}
```

After — RevTurbine decides, and renders the upsell when denied:

```tsx
import { Gate } from '@revturbine/sdk';

<Gate id="editor_export_action" can="advanced_export" surfaceTemplateIds={['modal_overlay']}>
  <ExportControls />
</Gate>
```

- `can` is the entitlement handle to check.
- children (`<ExportControls />`) render **only when granted** — this is your
  existing UI, unchanged.
- when **denied**, the gate resolves the placement and renders the upgrade
  surface named by `surfaceTemplateIds`.

For logic rather than markup, use the hook and keep your own fallback:

```tsx
import { useEntitlement } from '@revturbine/sdk';
const { allowed } = useEntitlement({ handle: 'advanced_export' });
```

## 3. Keep the baseline working (additive-only)

If RevTurbine is absent or the placement resolves to nothing, the call site must
still do something sensible — render the baseline UI, not a blank space or an
error. Never leave a gate that can hide a feature with no way back.

## Verify — this is not optional for revenue-critical gates

`<Gate>` is a **UX hint**. A determined user can edit client state and render the
children anyway. So for any gate protecting real value — an export that costs
compute, a credit spend, a seat — **re-check server-side before delivering the
value**:

```ts
// In the API route / server action that actually performs the action:
const decision = await rtServer.can(userId, 'advanced_export');
if (!decision.allowed) return forbidden();
```

The client gate makes the experience right; the server check is what actually
protects the money. Gating a purely cosmetic feature can skip the server check;
gating anything costly cannot.

## Test it

With `plan_handle: 'free'` you see the upgrade surface; with `'pro'` you see
`ExportControls`. Flip the user context and confirm both paths. Then hand back to
`revturbine-start-here` (or go straight to `revturbine-go-live-hosted-cutover`
when ready to leave local mode).
