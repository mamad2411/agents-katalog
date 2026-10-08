# Agent Basics

## Purpose
Teach agents the operational baseline for using Chronos safely: launchers, direct CLI invocation, argument passing, and `.chs` scripting workflows.

## When To Use
- New agent session setup.
- User asks "how do I run Chronos commands/scripts?"
- Agent needs a quick operational reset before domain skills.

## Scope
- Startup and execution mechanics only.
- Not a replacement for domain skills (Scheduling, Goals, Projects, etc.).

## Entrypoints

### Launchers (Windows)
- `console_launcher.bat` - open Chronos console.
- `listener_launcher.bat` - run listener service.
- `dashboard_launcher.bat` - run dashboard server + open UI.
- `ADUC_launcher.bat` - run ADUC familiar interface in Chronos mode.

### Direct CLI Invocation
- `python modules/console.py`
- `python modules/console.py <command> <args...>`

Examples:
- `python modules/console.py today`
- `python modules/console.py today reschedule`
- `python modules/console.py status energy:low focus:medium`

## Command Argument Basics

Chronos syntax is token-first, property-second:
- positional args: command targets (`today`, `task`, `"Deep Work"`)
- property tokens: `key:value`

Examples:
- `new task "Deep Work" priority:high duration:60m`
- `set task "Deep Work" status:pending category:focus`
- `today kairos breaks:timer quickwins:10`

If syntax is uncertain:
- `help`
- `help <command>`

## `.chs` Scripting Basics

### Create script
- Save file in `scripts/` (or any reachable path), extension `.chs`.

Example `scripts/daily_reset.chs`:
```chs
status energy:medium focus:high
today reschedule
quickwins limit:5
```

### Run script
- `run scripts/daily_reset.chs`

### Common script primitives
- variables: `set var ...`, `vars`, `unset`
- conditionals: `if ... then ...`
- loops: `repeat`, `for`, `while`

Reference:
- `docs/dev/chs_scripting.md`
- `docs/guides/conditions_cookbook.md`

## Operational Workflow (Recommended)
1. Start console (`console_launcher.bat` or direct Python invocation).
2. Validate command with `help` if needed.
3. Execute command or script.
4. Inspect output/state (`today`, `status`, `view`, `list`).
5. Escalate to domain skill if request is specialized.

## Guardrails
- Prefer read-only checks before mutation when state is unclear.
- Ask confirmation before destructive operations unless explicitly requested.
- Keep scripts small and composable; avoid giant monolithic `.chs` files.

## References
- `docs/readme.md`
- `docs/reference/cli_commands.md`
- `docs/dev/chs_scripting.md`
- `docs/guides/conditions_cookbook.md`
- `docs/agents/skills/skills_index.md`

