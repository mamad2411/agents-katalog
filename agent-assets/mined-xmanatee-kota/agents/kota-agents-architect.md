# Architect Module

Optional two-pass plan-then-edit flow that runs once before the main agent
loop when enabled in config. The architect pass produces a plan; the editor
pass executes it against a narrow tool set with adaptive replanning.

- Opt-in via `modules.architect.enabled` in `.kota/config.json`. The
  `-a` / `--architect` CLI flag sets the same flag for a single invocation.
- When disabled, the module contributes nothing; when removed, the capability
  is gone entirely.
- Plugs into the session loop through the generic pre-send hook registered
  via `ctx.registerPreSendHook`. Core does not reference this module by name.
- The editor advertises its narrow tool set and invokes the session-supplied
  guarded batch executor, which owns tool ordering and concurrency. Planning does not grant additional execution permissions.
