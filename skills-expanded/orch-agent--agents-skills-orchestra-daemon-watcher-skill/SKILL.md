---
name: orchestra-daemon-watcher
description: Build Phase 04 daemon workflows with file watching, debounce, launchd integration, and low-latency auto-sync execution.
---

# Objective
Keep agent files continuously synchronized via a resilient background daemon.

# Use This Skill When
- Implementing daemon lifecycle commands.
- Wiring file watching and debounce behavior.
- Adding launchd integration for macOS startup.

# Procedure
1. Start watcher for registry and managed paths.
2. Debounce rapid file events per path bucket.
3. Trigger sync pipeline and record event/log timing.
4. Expose daemon status through socket/CLI command.
5. Support install/start/stop/status with safe shutdown.

# Guardrails
- Prevent deadlocks between sync and status calls.
- Skip self-generated write events where required.
- Keep event-to-sync latency below product targets.

# Done Criteria
- Registry edits auto-sync within target latency.
- Rapid saves collapse into a single effective sync.
- Start/stop/install/status flows are stable and test-covered.
