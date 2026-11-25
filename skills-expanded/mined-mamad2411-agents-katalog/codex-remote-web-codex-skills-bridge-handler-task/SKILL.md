# Bridge Handler Task

Use this skill when adding or refactoring relay/control-plane behavior, bridge-managed RPCs, or desktop-agent forwarding behavior in the standalone remote stack.

## Goal

Implement backend/runtime changes without destabilizing the browser contract or the bridge session lifecycle.

## Workflow

1. Read `.codex/rules/bridge-and-relay.md`.
2. Confirm whether the change belongs in the control-plane, bridge, or desktop relay agent.
3. Preserve `/api/mobile/*` and `/v1/sessions/*` compatibility unless the task explicitly changes them.
4. Normalize structured errors instead of leaking raw process failures where possible.
5. Keep desktop-side assumptions clear: bridge is local, relay agent connects out, control-plane routes requests.
