---
name: create-plugin
description: |
  Creates oh-my-claude statusline plugins from scratch. Use when the user asks to build, create, make, or scaffold a new statusline plugin, segment, or widget for oh-my-claude or Claude Code's statusbar. Handles both JS plugins and script plugins (Python, Bash). Generates the plugin file, tests it, wires it into the statusline, and verifies it renders.
argument-hint: "[what the plugin should show]"
user-invocable: true
---

# Create Plugin

Build an oh-my-claude statusline plugin — from idea to working output in one pass.

## Workflow

1. **Clarify the plugin's purpose** — ask what it should display, when to hide, and any config the user wants. See [PATTERNS.md](PATTERNS.md) for data fields and common patterns.

2. **Choose plugin type** — JS plugin (default, in-process, fast) or script plugin (any language, runs as subprocess). Use JS unless the user specifies a language or the task needs external tools. See [PATTERNS.md](PATTERNS.md).

3. **Scaffold the plugin** — run `omc create <name>` (or `omc create <name> --script --lang=python|bash`). This creates the directory structure at `~/.claude/oh-my-claude/plugins/<name>/`.

4. **Implement render logic** — edit the generated `plugin.js` (or `plugin` script). Follow the contract in [PATTERNS.md](PATTERNS.md). Always use optional chaining. Always return null when data is missing.

5. **Set default config** — add any configurable values to `meta.defaultConfig` (JS) or `plugin.json` (script). Use concrete defaults, not empty strings.

6. **Test the plugin** — run `omc test <name>`. Verify it returns `{ text, style }` with mock data and returns `null` with empty data.

7. **Wire it up** — run `omc add <name>` (with `--line N` and `--left` if needed). Run `omc show` to verify placement.

8. **Verify end-to-end** — run `omc doctor` to confirm no errors. Run `omc show` to see the live preview.

## Self-review checklist

Before delivering, verify ALL:

- [ ] `meta.name` matches the directory name
- [ ] `meta.description` is a single clear sentence
- [ ] `render()` uses optional chaining for every data access (`data?.field?.subfield`)
- [ ] `render()` returns `null` when required data is missing (never crashes)
- [ ] `omc test <name>` succeeds — shows text with mock data, returns null with empty data
- [ ] `omc doctor` reports no errors for this plugin
- [ ] Shell commands (if any) use `cachedExec` from `src/cache.js`, never raw `execSync`
- [ ] Config keys have sensible defaults in `defaultConfig` (no empty strings or nulls for required values)
- [ ] Plugin text is short — fits in a statusline segment (under ~30 chars typical)
- [ ] `omc show` confirms the plugin appears where the user wants it

## Golden rules

Hard rules. Never violate these.

1. **Never crash the statusline.** Every data access uses optional chaining. Every render returns `{ text, style }` or `null`. No exceptions, no throws. A plugin that crashes breaks the entire statusbar for the user.
2. **Null means hide.** Return `null` when data is unavailable. Never return empty strings, placeholder text, or fallback values that clutter the bar.
3. **Cache all shell commands.** Use `cachedExec(key, command, ttlMs)` from `src/cache.js`. Raw `execSync` in render blocks the entire statusline pipeline.
4. **Test before wiring.** Always run `omc test <name>` before `omc add <name>`. A broken plugin silently disappears — testing catches errors the statusline would swallow.
5. **Keep text short.** Statusline segments share a single terminal line. Aim for under 30 characters. Use abbreviations, symbols, and rounding (e.g. `42%` not `42.53%`, `$2.41` not `$2.4100`).
6. **Config has real defaults.** Every key in `defaultConfig` must have a usable value. Users override config — they don't fill in required blanks.
7. **Match name to directory.** `meta.name` must exactly match the plugin directory name. Mismatches cause the plugin to silently not load.

## Reference files

| File | Contents |
|------|----------|
| [PATTERNS.md](PATTERNS.md) | Data fields, plugin templates, cachedExec usage, script plugin format, style tokens, common patterns |
