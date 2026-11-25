---
name: antigravity-automation
description: Automate recurring, background, event-driven, and multi-agent workflows in Google Antigravity. Crafts scheduled sidecars (~/.gemini/jetski/sidecars/<slug>/sidecar.json), in-session cron/timer automations, lifecycle hooks, autonomous subagent task distribution, and headless agent pipelines.
---

# Antigravity Automation & Scheduled Execution (`/antigravity-automation`, `/automation`)

> **Role**: Principal Automation Engineer & Antigravity Systems Architect  
> **Philosophy**: *Automate deliberately. Never poll in loops. Guard background resources. Respect user timezones. Sleep reactively.*

This skill establishes production discipline for recurring background automations, scheduled sidecars, in-session timers, multi-agent mesh coordination, and lifecycle hooks within **Google Antigravity**.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/sidecar-automation-guide.md](references/sidecar-automation-guide.md) | Antigravity scheduled sidecars, 5-field cron syntax, `CRON_TZ` naming, headless testing. |
| **Reference** | [references/in-session-scheduling.md](references/in-session-scheduling.md) | In-session `schedule` tool, one-shot timers, recurring crons, `manage_task` daemon controls. |
| **Reference** | [references/multi-agent-orchestration.md](references/multi-agent-orchestration.md) | Subagent swarms, dynamic definitions, message bus, shared lease locks, reactive wakeups. |
| **Reference** | [references/antigravity-hooks-reference.md](references/antigravity-hooks-reference.md) | Antigravity lifecycle hooks (`hooks.json`), event handlers, exit codes, safety gates. |
| **Reference** | [references/automation-error-catalog.md](references/automation-error-catalog.md) | Troubleshooting table for cron drift, orphan daemons, hook timeouts, and timezone mismatch. |
| **Utility** | [scripts/generate_sidecar_automation.py](scripts/generate_sidecar_automation.py) | CLI tool to validate, generate, and deploy Antigravity scheduled sidecars. |
| **Utility** | [scripts/verify_antigravity_hooks.py](scripts/verify_antigravity_hooks.py) | CLI validator checking syntax, matchers, timeouts, and paths in `hooks.json`. |
| **Utility** | [scripts/schedule_in_turn_helper.py](scripts/schedule_in_turn_helper.py) | Formats one-shot timers and in-turn cron schedules for the native `schedule` tool. |

---

## 2. Automation Architecture Matrix

```mermaid
flowchart TD
    subgraph TriggerModes["Trigger Modes"]
        A["Scheduled Sidecar<br/>(Cron + CRON_TZ)"]
        B["In-Session Timer<br/>(schedule tool)"]
        C["Lifecycle Hook<br/>(hooks.json)"]
    end

    subgraph ExecutionLayer["Execution Runtime"]
        D["Fresh Agent Context<br/>(agentapi new-conversation)"]
        E["Reactive Turn Resume<br/>(Zero Polling Sleep)"]
        F["Safety Gate Interceptor<br/>(Pre/Post Tool Hook)"]
    end

    subgraph SupervisedTasks["Managed Output"]
        G["Automated PR / Report"]
        H["Subagent Handoff Payload"]
        I["Enforced Code Invariants"]
    end

    A --> D --> G
    B --> E --> H
    C --> F --> I
```

---

## 3. Production Automation Protocols

### 3.1 Scheduled Sidecar Protocol (`sidecar.json`)
Deploy scheduled background automations directly to `~/.gemini/jetski/sidecars/<slug>/sidecar.json`:
1. **Always Prepend Timezone**: Formatted as `CRON_TZ=<IANA_TZ> <5-field-cron>` (e.g. `CRON_TZ=America/New_York 0 9 * * 1-5`). Never use raw offsets (`+02:00`) or non-standard abbreviations (`PST`).
2. **Self-Contained Prompts**: Prompts must contain complete context, target paths, explicit commands to run, and the required output format.
3. **Use Generator Utility**:
   ```bash
   python3 skills/antigravity-automation/scripts/generate_sidecar_automation.py \
       --slug "daily-security-audit" \
       --cron "0 8 * * 1-5" \
       --timezone "America/New_York" \
       --prompt "Run security audit, inspect dependencies, and output findings."
   ```

### 3.2 In-Session Scheduling & Background Tasks
1. **Zero Busy-Waiting**: Never invoke `sleep` in shell commands. Use the `schedule` tool with `DurationSeconds` or `CronExpression`.
2. **Reactive Wakeups**: Call no more tools after scheduling; Antigravity automatically resumes execution when the timer fires or a subagent responds.
3. **Daemon Supervision**: Launch long-running support servers with `IsDaemon: true` and monitor with `manage_task(Action="status")`.

### 3.3 Active Lifecycle Hooks (`hooks.json`)
1. Place `hooks.json` at the root of the customization plugin or project `.agents/hooks.json`.
2. Keep hook scripts lightweight (<2s execution time).
3. Validate hooks configuration with:
   ```bash
   python3 skills/antigravity-automation/scripts/verify_antigravity_hooks.py hooks.json
   ```

---

## 4. Verification & Testing Guardrails

Always verify automation configurations using the automated test suite:
```bash
python3 skills/antigravity-automation/tests/test_antigravity_automation.py
```
