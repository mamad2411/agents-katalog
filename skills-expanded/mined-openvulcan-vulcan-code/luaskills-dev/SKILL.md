---
name: luaskills-dev
description: Use when the user wants to design, create, modify, debug, test, package, or publish their own LuaSkill (a skill directory with skill.yaml, dependencies.yaml and Lua entries that LuaSkills and Vulcan Code load as tools). Installs and drives luaskills-debug, the standalone LuaSkills developer tool.
---

# LuaSkills Development

A LuaSkill is a directory whose name is the `skill_id`. It holds `skill.yaml` (entries, help, config), optional
`dependencies.yaml` (tools, Lua packages, native libraries, managed Node/Python), Lua entry files under `runtime/`,
and help files. LuaSkills loads it and exposes each entry as a tool named `{skill_id}-{entry_name}`.

Develop every LuaSkill with **luaskills-debug**. It embeds the same LuaSkills runtime a host uses, so `call` runs
the real load and call path, `validate` applies the real packaging rules, and `package` builds the exact release
assets LuaSkills installs. Never hand-build zips, guess manifest fields, or test by installing into the user's
Vulcan Code skills.

## 1. Get luaskills-debug

1. Call the `luaskills_debug` tool with `{"action":"status"}`.
2. If it reports `installed: false` or `compatible: false`, call `{"action":"install"}` and wait for the result.
   The install downloads the release that matches the LuaSkills series Vulcan Code embeds and verifies its
   checksum. Do not download luaskills-debug yourself with shell commands.
3. Use the returned `executable` path in every command below (quote it; it may contain spaces). `package_root`
   is the extracted tool folder and `runtime_root` is its private debug runtime.
4. If `runtime_ready` is `false`, run the setup script once before the first `call`, with `shell_command`:
   - Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File "<package_root>\setup_runtime.ps1" -Target lua`
   - Linux/macOS: `bash "<package_root>/setup_runtime.sh" lua`

`validate`, `package` and `new` work without the runtime setup.

## 2. Start or open the skill

- **New skill**: `luaskills-debug new <dir>`. The final directory name becomes the `skill_id`
  (`^[a-z]([a-z0-9-]*[a-z0-9])?$`). Use the default standard layout. Pass `--layout platform` only when the skill
  will bundle native libraries for several systems. The template includes a release workflow.
- **Existing skill**: work in its directory. Read `skill.yaml`, `dependencies.yaml` and the entry files before
  changing anything.
- Ask the user where the skill should live when it is unclear. Do not create skills inside Vulcan Code's own
  skill directories.

## 3. Edit, validate, call — in a loop

1. Change `skill.yaml`, `dependencies.yaml`, Lua entries, schemas or help. Follow
   [references/skill-format.md](references/skill-format.md); read the full manual it links when a field or API is
   not covered there. Never invent manifest fields: LuaSkills rejects unknown fields.
2. After every change run `luaskills-debug validate --skill-path <dir> --output json`. Fix each issue by its
   `code` and `path`, then validate again until it reports no issues.
3. Exercise the changed entries with the real runtime:
   `luaskills-debug call --runtime-root <runtime_root> --skill-path <dir> --tool <entry> --args-json '<json>' --output json`
   Prefer `--args-file` for non-trivial JSON. Check `result.content`, errors and logs; use `list-tools` and
   `inspect` to see the registered names and the loading result.
4. Repeat until every entry behaves as intended. See [references/cli.md](references/cli.md) for host context,
   SQLite, mirrors and managed runtime options.

Running a skill executes its code: every luaskills-debug command goes through `shell_command` and its normal
permission checks.

## 4. Package and publish

1. `luaskills-debug package --skill-path <dir> --out-dir <dir>/dist --output json`, with `--layout platform` for a
   platform release and `--include <name>` for extra top-level entries the skill ships.
2. Check the report: every asset, its size, and any warning about the LuaSkills Hub limits (100 MiB per package,
   600 MiB per version, 1 GiB expanded).
3. Explain the release path from [references/release.md](references/release.md): push to GitHub, tag `v<version>`
   matching `skill.yaml`, let the workflow publish the release, then submit the repository on LuaSkills Hub.
   Do not push, tag or publish for the user unless they ask.

## Rules

- Facts come from the skill source, validate/call output and the referenced manuals, never from memory of older
  LuaSkills versions.
- Keep the user's files: change only what the task needs, and show what changed.
- Report validation issues and failing calls as they are; do not hide them or work around them with fallbacks.
