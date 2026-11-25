---

name: add-adapter
description: Teach the Gateweave Agents scanner a new coding agent or a new file format of one it already reads - an adapter in packages/adapters with its docs links, redaction, wants/detect and tests. Use when a vendor adds a file type (skills, commands, MCP config) or when adding an agent such as Windsurf or Copilot.
---

# Add or change an adapter

`packages/adapters` turns a repository's files into a scan. One module per coding agent; the
contract it produces lives in `packages/model/src/inputs.ts` (`DetectedAgent`, `DetectedAsset`,
`ScanProblem`, `scanResult`).

## 1. Read the vendor's current docs

Formats change often. Fetch the official documentation (not memory, not a blog), and note:

- which files are committed to a repository, and at what depth they are read (root only, or any
  folder, as nested `CLAUDE.md` and `AGENTS.md` are);
- each file's format and the fields worth showing (front matter, JSON keys, TOML tables);
- which files are personal and gitignored (`CLAUDE.local.md`, `settings.local.json`): skip them;
- which other agents' files it also reads (Cursor reads `AGENTS.md` and `.claude/skills`).

Put the URLs and the date you checked in the comment at the top of the adapter. Say what the docs
contradicted from what you expected; that is what future readers need.

## 2. Write the adapter

Create `packages/adapters/src/<agent>.ts` exporting an `Adapter` (`src/types.ts`) and add it to
`ADAPTERS` in `src/detect.ts`. If the agent is new, its runtime must exist in
`REPOSITORY_RUNTIMES` in `packages/model/src/vocabulary.ts` first; that is a model change.

- `wants(path)` is true for every path whose text you need, and only those. The scanner downloads
  nothing else. It cannot depend on file contents, so a file that is only needed when a setting
  names it (a custom Gemini `context.fileName`) is given by blob and size instead.
- `detect(tree)` returns agents, assets and problems. Detect an agent only from its own files.
  Link the assets it reads in the agent's `assets`.
- Reuse the shared builders: `instructionsAsset` for a file stored byte for byte, `skillAssets` for
  any `SKILL.md` folder, `markdownAsset` for Markdown with front matter, `readConfig`,
  `settingsAsset` and `mcpServerAssets` for configuration. Two adapters that read the same file
  must produce identical assets, because `detect` keeps one asset per key. Using the builders
  guarantees it.
- File paths inside an asset are relative to the asset's directory. A part of a file (one MCP
  server) is one file named after its parent file, holding the part's own text.
- Metadata is flat (text, numbers, booleans, lists of text; at most 50 fields). Truncate, never
  fail, when text is over a limit.
- Never throw on bad input. Missing text, invalid JSON, YAML or TOML becomes
  `addProblem(problems, path, message)` and the piece is skipped.
- Do not hand-write a YAML or TOML parser; `frontmatter.ts` and `config.ts` already wrap `yaml` and
  `smol-toml`.

## 3. Keep secrets out

Everything stored from a configuration file goes through `redact` (`src/redaction.ts`): every
value under `env`, `headers` or `http_headers` is replaced, as are credentials in arguments, URLs
and keys named like `clientSecret`. Store `redactedText(...)`, never the original, and put only
names (`namesIn`) in metadata. If the format keeps credentials under another key, add it to
`redact` and to `test/redaction.test.ts`.

## 4. Test

One `test/<agent>.test.ts` with small inline fixtures modeled on the vendor's documented examples:

- the agent from its main file, and from `AGENTS.md` alone only if the vendor reads it as its own;
- every asset kind, with its metadata;
- secrets: assert that no secret value appears anywhere in `JSON.stringify(detection)`;
- problems for broken files, binary files by blob and size, and the `wants` yes and no lists;
- `expectValid(detection)` (`test/support.ts`) in every test that checks output.

Add the agent to the mixed repository in `test/detect.test.ts`.

## 5. Docs and verify

Update the supported-agents list in `docs/spec.md` and the "Format adapters" section of
`docs/architecture.md`. Run `pnpm verify`, then follow `open-pull-request`. Cite the vendor docs
in the pull request body.
