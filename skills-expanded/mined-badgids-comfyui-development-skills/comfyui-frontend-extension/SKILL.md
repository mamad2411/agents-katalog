---
name: comfyui-frontend-extension
description: Use for ComfyUI JavaScript or TypeScript frontend extensions, custom widgets, node UI behavior, menus, settings, dialogs, extension hooks, client-server UI integration, frontend build issues, or code that depends on ComfyUI_frontend internals.
metadata:
  version: "00.01.11"
---
# ComfyUI Frontend Extension

Frontend APIs move. Search current target/current `Comfy-Org/ComfyUI_frontend` before using any hook, service, type, or internal module path.

## Sources

- target/current `Comfy-Org/ComfyUI_frontend`;
- `Comfy-Org/ComfyUI-React-Extension-Template` when React/TypeScript extension scaffolding is relevant;
- frontend/custom-node docs in `Comfy-Org/docs`;
- current core frontend extensions as implementation examples;
- the target custom-node pack's existing web assets;
- frontend tests/build configuration.

## Procedure

1. Establish target frontend version/commit where possible.
2. Decide whether a frontend extension is actually necessary.
3. Search current frontend source for the needed extension lifecycle or service.
4. Prefer public/typed extension surfaces over private implementation details.
5. If private internals are unavoidable, isolate them and document the compatibility risk.
6. Preserve API-mode compatibility where possible. Direct client-server coupling should be intentional, not accidental.
7. Avoid relying on widget index/order when a current named/type-safe mechanism exists; verify the target behavior either way.
8. Run formatting/lint/type/build checks defined by the target project.
9. Test the behavior in the actual frontend and check browser console errors.
10. Verify backend/frontend version assumptions if the extension exchanges custom data.

## Do not

- copy an old `app.registerExtension` example without checking current hooks/types;
- monkey-patch global prototypes when a supported extension hook exists;
- assume LiteGraph internals are stable public API;
- duplicate backend state in the frontend unless necessary;
- create frontend-only behavior that silently breaks API execution when API compatibility is expected.

## Acceptance gate

Before calling the frontend change complete:

- verify the hook or extension API from the target/current frontend source;
- pass the relevant build, type, lint, or focused test command when available;
- confirm the extension registers or loads in a compatible frontend when practical;
- test any client-server contract from both sides when the feature is connected;
- state clearly when browser/runtime verification could not be run.

