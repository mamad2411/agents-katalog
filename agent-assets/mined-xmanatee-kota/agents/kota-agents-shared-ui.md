# Android Shared UI Renderer

This directory owns the native React Native presentation of the daemon-generated
`ui.surface.v1` graph used by the Android product path.

- Keep rendering exhaustive over generated unions. Unknown protocol arms fail in
  the generated decoder and renderer switches use `assertNever`.
- Derive navigation, availability, forms, confirmations, effects, and action
  semantics from the graph. Presentation and device affordances remain local.
- Execute every action through the central daemon context and
  `/ui/actions/execute`; do not call capability-specific routes from components.
- Key specialization to typed node or link kinds, never module names or surface
  ids. Native iOS operator behavior remains in `clients/apple/`.
