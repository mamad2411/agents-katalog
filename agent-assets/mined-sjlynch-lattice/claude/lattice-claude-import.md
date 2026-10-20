# backend/src/mcp/import

"Import from existing tools": read the user's OTHER agent configs, normalize the
MCP servers they already declare into Lattice's `McpServerEntry` shape, and
classify their secrets. The orchestrator (`scanImportableServers` / `applyImport`
+ dedupe) and the public re-exports live in `../importConfigs.ts`; this directory
holds the concerns it composes. Where secrets live and how they reach a server
is `../CLAUDE.md` → Policies — don't duplicate it here.

The orchestrator renames an import whose id is a retired built-in
(`../retiredServers.ts`) to `<id>-imported`: the settings layer strips those
ids from every toggle map, so under the old id it could never be switched on.

## Modules

- `normalize.ts` — `normalizeServer` + the `Normalized` / `RawServer` types: the
  shape-normalization assembly that turns a raw per-tool entry into an
  `McpServerEntry`, consuming `secretDetection.ts` to route each env/header value.
  A LITERAL secret-looking value (by var NAME *or* VALUE SHAPE) is captured for
  `~/.lattice/mcpSecrets.json` and kept OFF the entry; a REFERENCE
  (`${input:…}`/`${env:…}`/`$VAR`/Codex `bearer_token_env_var`) is recorded as a
  `secretEnvVars` / `secretHeaders` name with no value.
- `secretDetection.ts` — the secret-**classification** core, split out of
  `normalize.ts` so the security surface is auditable in isolation:
  `looksSecret(name)`, `looksSecretValue(value)`, `isReference(value)` and the
  regex/entropy internals. **Test-pinned** through `normalizeServer`.

  **Security invariants.** A value is treated as a literal secret when its NAME
  trips the name regex *or* its VALUE SHAPE matches any of four detection methods:
  1. **Name regex** — `key|token|secret|password|passwd|auth|credential|apikey`.
  2. **Vendor value prefixes** — known issuer token prefixes (`sk-`, `ghp_`,
     `xox…-`, `AKIA`, `AIza`, `glpat-`, `npm_`, `hf_`, …), case-sensitive.
  3. **Credentialed URIs** — a `scheme://userinfo@host` connection string
     (`postgres://u:p@host`); the userinfo run forbids `/`, so a plain URL never
     matches.
  4. **High-entropy tokens** — a ≥24-char single-token `[A-Za-z0-9_-]` string with
     both letters and digits and Shannon entropy ≥ 3.5 bits/char (opaque keys with
     no recognizable prefix).

  **Bias toward "secret".** When in doubt we classify as a secret: a false
  positive only routes plain config into the `0600` secrets file (still injected
  at resolve time), whereas a false negative leaks a key inline into the
  world-readable `globalSettings.json`.

  **Secrets embedded in `url` / `args`** (`?api_key=…`, `https://user:tok@host`,
  a secret-shaped path segment, `--api-key sk-…`, `--api-key=…`, `KEY=…`,
  mcp-remote `--header Authorization:Bearer …`) have no env/header slot to move
  into, so `scanUrlForSecrets` / `scanArgsForSecrets` return a **redacted** copy
  plus name-only findings. `normalizeServer` keeps only the redacted url/args and
  sets `Normalized.embeddedSecrets`; the scan surfaces it (the UI disables the
  row) and `applyImport` **refuses** the server (`refused: [{id, reason}]`) —
  never writes it to `globalSettings.json`. Secret-named flags/params ending in
  `file|path|dir|mode|url|…` (`--token-file`) are not treated as secrets.
- `codexToml.ts` — `parseCodexMcpServers`: a minimal hand-rolled reader for
  Codex's `[mcp_servers.*]` TOML tables only (no TOML dep added; best-effort).
- `sources.ts` — the five per-tool `collect*` readers (Claude Code, Cursor,
  Codex, VS Code, Windsurf) + the `readJson` / `serversFromMap` helpers. All
  read-only; a missing/unparseable file is silently skipped.

`normalize.ts` (with `secretDetection.ts` behind it) and `codexToml.ts` are
test-pinned via the `../importConfigs.js` re-export path
(`__tests__/mcp.import.test.ts`).
