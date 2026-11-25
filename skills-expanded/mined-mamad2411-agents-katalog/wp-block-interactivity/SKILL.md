---
name: wp-block-interactivity
description: Implements and reviews WordPress Interactivity API blocks with server-rendered directives, Script Modules, state and context boundaries, permissions, progressive enhancement, and client-side navigation compatibility.
---

# WordPress Block Interactivity

Use this skill for front-end interactions built with the Core Interactivity API.

## Compatibility Gate

The Interactivity API and Script Modules entered Core in WordPress 6.5. For lower Core versions, require an explicit compatible Gutenberg dependency or choose another architecture.

## Procedure

1. Confirm minimum WordPress version and whether Interactivity API is allowed.
2. Keep meaningful initial HTML server-rendered.
3. Add `supports.interactivity` and `viewScriptModule` deliberately.
4. Namespace stores and distinguish global state, local context, derived state, config, actions, and callbacks.
5. Keep protected data and authorization on the server.
6. Validate directive values and escape server-rendered attributes.
7. Design a useful no-JavaScript baseline.
8. Test hydration, repeated instances, client-side navigation, failure states, and accessibility.

## Workflow

Use `workflows/implement-interactive-block-workflow.md`.

## Resource

- `resources/interactivity-safety-checklist.md`

## Example

- `examples/progressive-enhancement-example.md`
