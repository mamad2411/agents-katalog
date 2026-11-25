---
name: codex-controller
description: Use FAST for optional G → Manager/Factory → X delegation through an existing designated controller. Use for coordinated work across one or more approved Codex workers where a Manager improves sequencing or acceptance. Reuse verified workers, normal message_send/read chat, native Codex queue behind the controller, and tracked execution safeguards only when needed.
---

# FAST — Manager G → M → X (optional)

This is a **delegation workflow**, not a new control plane. The selected controller's current Issue/SPEC and repository adapter own the routing, provider restrictions, worker bindings and acceptance. No skill grants extra permission.

1. Resolve the **existing designated controller** and its exact connected workspace. Do not create an F/Manager or confuse connector identities. Check the owning Issue/PR and current delegated objective only as needed.
2. G talks to that controller with one compact `message_send` containing the active Issue/PR and current delta; use `message_read` to check a fresh response (cursor when available). No mission IDs, file packets, broad context reload or status ceremony just to talk.
3. The **controller**, not G, chooses verified bound workers, sequences their implementation and checks one writer per conflicting checkout or provider operation. The controller sends one small worker delta through its existing supported native queue; a queue receipt proves **admission only**.
4. The controller reads the worker's terminal result and required GitHub/provider evidence, records material decisions in the owning Issue/PR, and continues the next **already-authorized** phase without asking for routine permission.
5. Stop at real identity, write-conflict, unknown-previous-action, approval, security or production gates. Retain required provider evidence even when the message path is deliberately fast. Do not blind-resend an uncertain execution.

## Direct advisory side channel (allowed)

G can ask any verified X a **read-only question directly** via `codex-direct-chat`, including a controller-managed worker. This is advice only: it may not redirect ongoing work, change worker priority, start a new goal, or take over the controller's acceptance. Share material findings with the controller and Issue/PR before acting on them.

## Factory is a concrete adapter, not the generic contract

For an already selected **Factory F** lane, read [Factory AGENTS](https://github.com/amitkarpe/work/blob/main/docs/factory/AGENTS.md) and, only when applicable, [FAST](https://github.com/amitkarpe/work/blob/main/docs/factory/FAST_PROTOCOL.md). Established F-to-gg practice uses a short native `codex queue` instruction and one useful completion, not routine old Direct missions or duplicate goal/result artifacts. Factory's worker identity and endpoint remain controller-specific; the shared FAST send/reply practice also applies to other verified Managers without copying Factory's binding.

Dot-managed tracked execution keeps its own adapter's `mission_start/status` semantics unless that adapter changes explicitly; normal chat does not erase its execution guards.

References when needed:
- [Agent OS controller/worker collaboration](https://github.com/amitkarpe/agent-os/blob/main/kb/playbooks/integrations/chatgpt-codex-collaboration-protocol.md)
- [Agent OS native queue contract](https://github.com/amitkarpe/agent-os/blob/main/kb/playbooks/delegation/codex-native-controller-worker-protocol.md)
