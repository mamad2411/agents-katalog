---
name: mfa-memoryrouter-isolation
description: Wrap Module Federation-exposed React components in `MemoryRouter` so they own a private router context instead of inheriting the host's — avoids cross-origin router errors in dev and keeps the remote's routes from leaking into the host URL bar.
category: frontend
tags: [module-federation, react-router, memoryrouter, micro-frontend, cross-origin]
triggers: ["MemoryRouter", "Router context", "cross-origin", "useNavigate outside Router", "MFA expose router"]
source_project: lucida-ui
version: 0.1.0-draft
---

# MFA MemoryRouter Isolation

Wrap the inside of each MF expose with `MemoryRouter` so the remote gets a working Router even when the host isn't routing, and doesn't hijack the host's URL.

See `content.md`.
