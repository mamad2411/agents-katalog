---
name: setup-codex
description: >-
  Review, reconcile, and tidy ~/.codex/config.toml from this agent-workbench
  repository. Use only when the user explicitly asks to run setup-codex,
  reconcile Codex settings, clean up config layout, or migrate the former
  script-managed Codex config.
---

# Setup Codex

Reconcile the user's Codex config with `references/config.toml`, and normalize
its layout, while preserving unrelated settings and comments.

Feature flags control capability availability; they do not uninstall plugin
bundles, disconnect accounts, or remove plugin skills from an existing session.
Handle plugin installation and account connections through the supported plugin
manager as a separate workflow. Never infer installation state from cache files.

When the user explicitly asks to isolate local Codex from account/workspace
plugins while preserving ChatGPT connections, use
`scripts/remote_plugin_policy.py`. It gets installed state and skills from the
Codex app-server, uninstalls only removable remote plugins through
`plugin/uninstall`, and keeps a name-based local denylist as a fallback. It does
not operate ChatGPT connectors and does not delete plugin caches.

## Workflow

1. Confirm the current Git root contains this skill at
   `.agents/skills/setup-codex/SKILL.md`. Stop if it does not; this workflow is
   intentionally limited to the agent-workbench repository.
2. Read the repository `AGENTS.md`, this file, and `references/config.toml`.
3. Resolve the reference placeholders:
   - `{{HOME}}`: the user's home directory.
   - `{{AGENT_WORKBENCH_DIR}}`: the physical agent-workbench repository root.
   - `{{DOTFILES_DIR}}`: `$ILYASYOY_DOTFILES_DIR`, or the `dotfiles` sibling
     of the agent-workbench repository when it is unset.
   - `{{NVIM_WORKBENCH_DIR}}`: `$ILYASYOY_NVIM_WORKBENCH_DIR`, or the
     `nvim-workbench` sibling when it is unset.
   - `{{PERSONAL_PROJECTS_DIR}}`: the parent directory of the
     agent-workbench root.
4. Resolve the target as `$CODEX_HOME/config.toml`, defaulting `CODEX_HOME` to
   `~/.codex`. Inspect the target and its symlink status without writing.
5. Parse the target as TOML. Treat a missing target as an empty config. If it
   is unreadable, invalid, or a symlink to an unexpected location, report the
   problem and ask the user what to do; never replace it automatically.
6. Detect legacy lines matching
   `## start ilyasyoy codex ... ##` or `## end ilyasyoy codex ... ##`.
   Propose removing only those comment lines. Never delete a marker span,
   because unrelated settings may have been inserted inside it.
7. Compare every leaf in the rendered reference with the target. Treat arrays
   as single values and group differences as `root`, `tui`, `notice`,
   `sandbox`, `features`, `memories`, `skills`, `mcp`, and `projects`. Preserve every
   target key not present in the reference, except when an MCP server changes
   transport between a local `command` and a remote `url`: compare and replace
   that server table atomically so fields from the old transport are removed.
8. Detect obsolete configuration as an independent `obsolete` change group:
   - Remove `features.js_repl` when present. The feature was removed; a separate
     `mcp_servers.node_repl` entry is not affected.
   - Remove `mcp_servers.computer-use` only when
     `plugins."computer-use@openai-bundled".enabled = true`; the bundled plugin
     owns Computer Use in that configuration.
   - Remove an `[apps.<id>]` override only after the user explicitly confirmed
     that the corresponding external plugin was uninstalled. Do not use cache
     presence or absence as evidence.
9. Run the layout checker with
   `uv run .agents/skills/setup-codex/scripts/normalize_codex_config.py --check <target>`.
   Treat a
   nonzero status of `1` as an independent `layout` change group; status `2`
   is an error. The canonical top-level order is Core, Safety, Features and
   memory, Interface, Tools and plugins, Trusted projects, Other settings, and
   Generated application state. Generated `desktop`, `marketplaces`, and
   `apps` tables stay at the bottom. The normalizer preserves TOML data,
   comments, nested-table adjacency, and array order; it sorts repeated tables
   by identifier with `_default` first. `[skills]` belongs to Features and
   memory. The normalizer does not reorder `skills.config`; only the remote
   policy synchronizer sorts its comment-marked entries.
10. Show a concise redacted summary containing missing, differing, obsolete,
    legacy marker, and layout changes. Never print unknown values or values
    whose key or content looks like a token, password, key, credential,
    authorization header, or secret.
11. Ask the user to choose one of: apply all groups, select groups, or cancel.
    `Apply all` includes `obsolete` and `layout`; selective apply may include or
    exclude either. Offer layout-only cleanup even when semantic settings
    already match. Do not write before a choice is explicit.
12. Before the first write, request approval for writing under `CODEX_HOME`.
    Create `config.toml.YYYYMMDDHHMMSS.bak` with metadata preserved. If the
    target is missing, state that no backup is possible.
13. Apply only the confirmed groups and marker-line cleanup. Replace a
    confirmed MCP server table atomically when its transport changes; otherwise
    preserve target keys absent from the reference. Keep root keys before TOML
    tables and preserve all unrelated tables and runtime-generated settings. If
    `obsolete` is selected, first run
    `uv run .agents/skills/setup-codex/scripts/prune_obsolete_codex_config.py --output <pruned> <temporary>`;
    add one `--remove-app <id>` for each explicitly confirmed uninstalled app.
    If `layout` is selected, run the normalizer on the semantic or pruned
    temporary file:
    `uv run .agents/skills/setup-codex/scripts/normalize_codex_config.py --output <candidate> <temporary>`.
    Verify the candidate is semantically equal to the temporary file, then
    install the candidate atomically. Never pass the target as both input and
    output. Do not use the old dotfiles setup helpers.
    For an explicitly approved remote-isolation change, first run
    `uv run .agents/skills/setup-codex/scripts/remote_plugin_policy.py prepare --config <temporary> --output <policy-candidate>`.
    This probes current Codex support for exact
    name-based overrides and stops before writing when unsupported. Normalize
    the policy candidate, install it atomically with the other approved groups,
    and only then run the same script's `uninstall` command. Existing unrelated
    skill overrides and prior managed denials are preserved; newly discovered
    remote names are added, while bundled/runtime names are excluded.
14. Parse the result again, then run
    `codex doctor --summary --no-color --ascii`. If validation fails, stop,
    show the failure, and offer to restore the backup; do not restore or make
    further edits without confirmation.
15. When features, plugins, apps, or MCP entries changed, also run
    `codex features list`, `codex plugin list`, and `codex mcp list`. Treat the
    plugin list as local CLI state only; account-level plugin removal requires
    confirmation from the supported plugin manager. Plugin skills in the
    current session remain stale until a new session starts.
    For remote isolation, run the same script's `verify` command twice so each
    result comes from an independent app-server process. Require zero enabled
    remote skills and at least one enabled bundled/runtime skill in both runs.
16. Report changed groups, the backup path, validation result, and that a new
    Codex session is required to verify its skill inventory. If there is no
    diff, report that without creating a backup.

## Safety

- Configure only `config.toml`; do not alter auth, sessions, plugin caches,
  skill files, memories, rules, or other files under `CODEX_HOME`.
- Do not delete or rename plugin caches. Plugin and connector removal is a
  separate, explicitly authorized operation through the supported manager.
- App-server audit, uninstall, and denylist synchronization require explicit
  user authorization. Never substitute `codex plugin remove` for remote
  `plugin/uninstall`, and never touch ChatGPT connector state in this workflow.
- Never request or expose secret values. MCP entries contain environment
  variable names only.
- Do not commit repository changes.
