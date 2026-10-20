---
name: module-federation-expose-wrapper
description: Six-step pattern for exposing a component from one Module Federation remote and consuming it from another via a shared library — implementation → expose wrapper → MF config → MF name constant → RemoteApp wrapper in shared → consumer import. Prevents direct cross-remote imports and webpack alias collisions.
category: arch
tags: [module-federation, micro-frontend, webpack, react, remote, expose, mfa]
triggers: ["module federation", "MFA", "cross-remote import", "exposes", "RemoteApp", "webpack alias collision"]
source_project: lucida-ui
version: 0.1.0-draft
---

# Module Federation Expose Wrapper Pattern

Short: Never import across sibling remotes. Expose through a shared indirection layer so webpack alias (`@/`) resolution stays local to each remote.

## When to use
- Multi-remote (host + N remotes) webpack Module Federation setup.
- A component implemented in remote A needs to be rendered inside remote B.
- You have a `shared/` package both remotes depend on.

## Pattern
See `content.md`.
