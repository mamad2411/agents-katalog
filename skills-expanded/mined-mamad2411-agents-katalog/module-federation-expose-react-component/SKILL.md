---
name: module-federation-expose-react-component
description: Canonical 6-step pipeline for exposing a React component from one Module Federation remote and consuming it from another — implementation → expose wrapper (MemoryRouter) → MF config → shared MF-name constants → shared RemoteApp wrapper → consumer import. Prevents direct cross-remote imports and webpack `@/` alias collisions.
category: frontend
tags: [module-federation, micro-frontend, webpack, react, remote, expose, mfa, monorepo]
triggers:
  - "expose a component across module federation remotes"
  - "share React component between MFA remotes"
  - "MFA expose pipeline"
  - "cross-remote import forbidden"
  - "RemoteApp wrapper"
  - "webpack alias collision"
source_project: merged
version: 1.1.0
merged_from:
  - "skill:arch/module-federation-expose-wrapper"
  - "skill:frontend/module-federation-expose-react-component"
supersedes:
  - "skill:arch/module-federation-expose-wrapper"
  - "skill:frontend/module-federation-expose-react-component"
---

# Expose a React component across Module Federation remotes

Use when a component lives in remote A but must render inside remote B (or host), and direct cross-remote import is forbidden (webpack `@/` alias collisions, build isolation, independent deploys).

**Rule**: never import across sibling remotes. Expose through a shared indirection layer so webpack alias resolution stays local to each remote.

## When to use

- Multi-remote (host + N remotes) webpack Module Federation setup.
- A component implemented in remote A needs to be rendered inside remote B.
- You have a `shared/` package that both remotes depend on.

## Steps

1. **Implement in the source remote only.**
   - Path: `remotes/<producer>/src/layout/<Component>.tsx`
   - Rule: use `@<shared-scope>/shared/...` imports only. Do not import from sibling remotes.

2. **Create an expose wrapper that isolates Router + stylesheets.**
   - Path: `remotes/<producer>/src/remote-components/exposes/<Component>.tsx`
   - Wrap the component in `MemoryRouter` (not `BrowserRouter`, not `withRouterWrapper` — see skill: `frontend/mfa-memoryrouter-isolation`).
   - Import the producer's own global stylesheets here so the component renders self-contained.

3. **Register in the producer's `modulefederation.config.js`.**
   ```js
   exposes: { './<Component>': './src/remote-components/exposes/<Component>.tsx' }
   ```

4. **Declare an MF constant in the shared types file.**
   - Path: `shared/types/remoteAppProps.d.ts`
   - `export const <SCOPE>_MF_<PRODUCER>_<COMPONENT> = '<Component>'`

5. **Create a consumer-facing RemoteApp wrapper in `shared/`.**
   - Path: `shared/remote-components/imports/<producer>/<Component>.tsx`
   - Wrap with the project's `RemoteApp` loader, passing `[<PRODUCER_MF_NAME>, <COMPONENT_CONST>]`.

6. **Consume from any other remote.**
   ```ts
   import <Component> from '<scope>/shared/remote-components/imports/<producer>/<Component>'
   ```

## Checklist

- [ ] Producer imports only from `shared/` (no cross-remote `@/`).
- [ ] Expose wrapper uses `MemoryRouter`.
- [ ] Expose wrapper imports the producer's stylesheets.
- [ ] `modulefederation.config.js` `exposes` updated.
- [ ] MF name constant added to `shared/types/remoteAppProps.d.ts`.
- [ ] `RemoteApp` wrapper added under `shared/remote-components/imports/<producer>/`.
- [ ] Consumer uses the shared wrapper, never the producer path directly.

## Why this shape

- `shared/` is the only safe cross-cutting surface; producer and consumer remotes have different webpack aliases for `@/`.
- The **expose wrapper** isolates expose-boundary concerns (styles, Router) from the pure implementation.
- Wrapping the expose with `MemoryRouter` avoids Router context loss when the consumer is served from a different dev-server origin.
- The **shared `RemoteApp` wrapper** means consumers import a normal React component — no knowledge of MF plumbing leaks out, and MF scope/module names cannot drift across config and consumers.

## Related skills

- `frontend/mfa-memoryrouter-isolation` — deep-dive on why `MemoryRouter` is the right choice at the expose boundary.
- `frontend/mfa-plain-html-dropdown-escape-hatch` — common follow-up fix when a DS Dropdown inside the exposed subtree infinite-loops.

## Provenance

- skill:arch/module-federation-expose-wrapper @ 7f01754
- skill:frontend/module-federation-expose-react-component @ 40ea2b2

See `content.md` for code templates and pitfalls.
