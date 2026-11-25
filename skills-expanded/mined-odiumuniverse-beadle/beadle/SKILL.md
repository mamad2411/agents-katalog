---
name: beadle
description: Work with beadle, the agent-config sync tool. Use when the user mentions beadle, the vault (~/.beadle), syncing agent configuration, `beadle doctor`, `beadle sync`, plugin hooks approval, bundles, or when rules, MCP servers, skills or permissions drift between agents. For open sync conflicts use the beadle-conflicts skill.
---

# beadle

beadle keeps every AI coding agent's configuration in one vault (`~/.beadle`,
`$BEADLE_HOME`) and syncs it both ways with a 3-way merge. This skill is the
quick map; the full machine-facing guide is `beadle guide`.

<important>
- **Hooks never travel by themselves.** Plugin command hooks are only reported
  by `beadle doctor`; ask the human, then run
  `beadle hooks approve --plugin <marketplace>/<name>`. beadle never executes
  hooks itself.
- **Defaults (U-14):** the `permissions` kind and the shared
  `~/.agents/skills` surface are on; `beadle init` enables detected agents,
  installs the watcher daemon, enables the project files already present in a
  git checkout and attempts the native bundles. Escape hatches:
  `beadle kinds disable <kind>`, `beadle agents disable <agent>`,
  `beadle bundles disable <host>`, `beadle project disable <file>`.
- **Secrets:** never print or copy values; the canon keeps `{secret:NAME}`
  references and values live in `mcp/secrets.json` (0600). A sync materializes
  them into the host configs; `beadle export` keeps references unexpanded.
- **`beadle doctor` is read-only** and safe to run any time.
</important>

<workflow>
1. `beadle status` → `beadle diff` (read-only) → `beadle sync`.
2. A conflict is not an error: `beadle conflicts --json` → decide → `beadle resolve`
   with the three expected hashes (see the beadle-conflicts skill).
3. Plugins: `beadle doctor` reports the plugin farm findings (collisions,
   quarantines); hooks need a personal approve.
4. `beadle guide` prints the full rules for agents; `beadle guide --humans` the
   human guide.
</workflow>

<command>
- `beadle status` · `beadle diff` · `beadle sync [--dry-run]` · `beadle pull` · `beadle push`
- `beadle doctor`                          read-only diagnosis, farm findings and hooks awaiting approval
- `beadle conflicts` · `beadle resolve`    the conflict loop (beadle-conflicts skill)
- `beadle agents` / `beadle kinds`         enable, disable, change a mode
- `beadle plugins pins` · `pin` · `unpin`  per-agent plugin version pins
- `beadle hooks list|add|rm|approve|revoke`; `approve --plugin <marketplace>/<name>`
- `beadle bundles status|enable|disable`   native host bundles
- `beadle skills seed|adopt|unadopt`       the built-in skills
- `beadle export` · `beadle explain` · `beadle history` · `beadle restore`
- `beadle secrets list|set|rm|prune|migrate`
- `beadle project status|enable|disable|forget`
- `beadle guide` · `beadle guide --humans`
</command>

<never>
- Never edit the vault and an agent file for the same item and then sync: one
  side becomes a conflict.
- Never approve a hook (or a plugin) without reading what it runs.
- Never copy a secret value out of a config file into the vault, a note or a
  chat.
- Never hand-edit `<vault>/state.json`, the conflict files, the CAS objects or
  anything under the plugin farm.
- Never commit, push or publish the vault unless the human asked.
</never>
