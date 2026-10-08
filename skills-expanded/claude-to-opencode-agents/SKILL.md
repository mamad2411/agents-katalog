# AGENTS.md

## Project

CLI tool (`claude-to-opencode`) that migrates Claude Code projects to OpenCode format.
TypeScript, compiled to `dist/`, no test suite, no linter configured.

## Commands

```bash
npm run build   # tsc → dist/  (only build step; required before running)
npm run dev     # ts-node src/index.ts (run from source without build)
node dist/index.js --input <path> --output <path>
```

There is no `test`, `lint`, or `typecheck` script beyond `tsc` (which is `npm run build`).
Always run `npm run build` after editing source before testing changes via `node dist/index.js`.

## Source layout

```
src/
  index.ts              # CLI entry (commander), orchestrates all converters
  types.ts              # All shared interfaces — single source of truth for data shapes
  scanner/scanner.ts    # Scans input project, returns ScanResult
  frontmatter/
    transformer.ts      # All frontmatter conversion logic (model map, tool→permission, etc.)
  converters/
    agents.ts           # .claude/agents/*.md → .opencode/agents/*.md
    commands.ts         # .claude/commands/*.md → .opencode/commands/*.md
    skills.ts           # .claude/skills/*/SKILL.md → .opencode/skills/*/SKILL.md
    claude-md.ts        # CLAUDE.md @include inlining
    mcp.ts              # .mcp.json + .claude/settings.json → opencode.json
    rules.ts            # path-scoped rules → _unsupported/rules/
    hooks.ts            # hooks → _unsupported/hooks/
  report/reporter.ts    # Generates MIGRATION-REPORT.md
  utils/
    fs.ts               # Async file helpers (exists, readFile, listFiles, listDirs)
    logger.ts           # Logger factory (verbose/dry-run aware)
```

## Key conventions

- `frontmatter/transformer.ts` is the central logic file — model alias maps, tool-to-permission
  mappings, and all frontmatter conversion functions live there. Add new mappings here first.
- `TOOL_KEY_MAP` in `transformer.ts` maps Claude tool names (e.g. `Write`, `Bash`) to OpenCode
  permission keys (e.g. `edit`, `bash`). Update this when adding new tool support.
- `MODEL_MAP` in `transformer.ts` maps Claude model aliases per provider. Currently covers
  `anthropic`, `openai`, `google`.
- Converters receive `(scan, options, result, log?)` — they mutate `result` in place (counts,
  warnings, errors, unsupportedFiles).
- Dry-run: all file writes must go through the logger/fs utilities that check `options.dryRun`.
  Never call `fs.writeFile` directly in a converter.
- Skills have a non-obvious structure: each skill is a subdirectory with a `SKILL.md` inside,
  not a flat `.md` file. Subdirectory name becomes the skill name.

## OpenCode format constraints (verified against docs)

### Skill frontmatter
OpenCode skills only accept these frontmatter fields: `name`, `description`, `license`,
`compatibility`, `metadata`. There is **no** `tools` or `permission` field in skill frontmatter.
The `convertSkillFrontmatter` function in `transformer.ts` correctly drops `allowed-tools` with
a warning instead of mapping it.

### Agent frontmatter
The `tools` field in agent config is deprecated in OpenCode — use `permission` instead. The
converter already emits `permission: { edit: "deny", bash: "deny" }` style output. Agent mode
defaults to `all` if omitted, but the converter always sets it explicitly.

### Permission format
Permissions use `"allow"` / `"deny"` / `"ask"` strings. For bash sub-patterns:
`{ bash: { "git *": "allow" } }`. Last matching rule wins.

### MCP format
`.mcp.json` `mcpServers[name].command` + `args` → OpenCode `mcp[name].command` (single array).
`env` → `environment`. Remote servers need `type: "remote"` + `url`.

### CLAUDE.md includes
OpenCode does not natively parse `@filepath` includes — converter inlines them directly into
the output file. This is intentional: OpenCode uses `opencode.json` `instructions` array for
multi-file instructions instead.

## Unsupported content handling

- Hooks and path-scoped rules cannot be converted; they are copied to `_unsupported/` (or just
  reported) depending on `--unsupported` flag (`copy-and-report` default, `report-only`).
- `UnsupportedFile` entries are pushed to `result.unsupportedFiles` and appear in the generated
  `MIGRATION-REPORT.md`.

## Binary / entry point

- `package.json` `bin` points to `dist/index.js` — file must be compiled before `npm link` or
  direct invocation works.
- `npm link` makes `claude-to-opencode` available globally from the compiled output.
