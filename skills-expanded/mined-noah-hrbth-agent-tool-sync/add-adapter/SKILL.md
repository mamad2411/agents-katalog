---
name: add-adapter
description: Add a new tool adapter to agentsync — scaffolds internal/tools/<tool>.go (a ToolMeta literal + render func), registers it, extends adopt.go for reverse mapping, adds a roundtrip test, regenerates the metadata golden, and updates README compatibility tables. Use when implementing one of the tools still open in TODO.md (Windsurf, Continue.dev, Roo Code, Crush, Goose, Amazon Q, Kilo Code, Aider, Cody) or any new AI tool.
---

# Add a New Tool Adapter

Goal: define a new `Tool` end-to-end. A `Tool` is a pure value — `Tool{ Meta ToolMeta; Render RenderFunc }`; there is **no `Adapter` interface**. Mirror the conventions in `internal/tools/claude.go` (the reference implementation); the types live in `internal/tools/tool.go`.

## 0. Research the target tool — do not skip

Find primary-source docs for the tool's config layout. Confirm:

- Config dir: `~/.<tool>/` or `~/.config/<tool>/`? (`detectGlobalDir` vs `detectConfigDir`)
- Project layout: `.<tool>/...` at workspace root? Anything special?
- Root memory file (name + format): does it live at workspace root or under the tool dir?
- Per-rule files supported? Subdir layout? File extension (`.md`, `.mdc`, `.toml`)?
- Skills, agents, slash commands: which concepts exist? Frontmatter schema for each?
- User scope: is there an on-disk user config layer? If not, set `Scopes[ScopeUser] = {Supported: false, Reason: "..."}`.
- Deprecations: any concept the tool flags as legacy? (set `Compatibility.Deprecated = true` with a `Replacement`).

Cite the source URL in the tool file as a one-line comment above the `ToolMeta` literal. If docs are ambiguous, prefer WebFetch over guessing.

## 1. Create `internal/tools/<tool>.go`

Use `claude.go` as the template. The file holds two things, co-located:

**`var <tool>Meta = ToolMeta{...}`** — the data descriptor:

- `Key` — stable lowercase id (e.g. `"windsurf"`). `Name` — display name in Title Case (e.g. `"Windsurf"`).
- `Detect` — `detectGlobalDir("<tool>")` or `detectConfigDir("<tool>")` (or a custom `DetectFunc` closure for irregular probes).
- `Concepts` — list **all 4** concepts explicitly: `{Supported: true}` per natively-supported concept; `{Supported: false, Reason: "..."}` for unsupported; mark deprecated concepts with `Deprecated: true, Replacement: "<successor>"`.
- `Scopes` — list **both** scopes explicitly; `{Supported: false, Reason: "..."}` for scopes with no on-disk layer (see `cursor.go`, `zed.go` user scope).
- `Aliases` — only for concepts whose displayed filename differs from the canonical name (e.g. Claude `ConceptRules: "CLAUDE.md"`). Omit otherwise.
- `ConceptInfo` — a specific per-concept help string for the TUI Tools screen (real paths, not generic filler).

**`func render<Tool>(c *canonical.Canonical, scope Scope) ([]FileWrite, error)`** — the only deep, tool-specific code:

- Return `[]FileWrite` with **paths relative to the scope's base dir** (workspace root or `$HOME`). Never emit absolute paths. Build paths from the `paths.go` anchor constants and `filepath.Join` — don't re-type path literals.
- Build all frontmatter via `buildMDFrontmatter` / `buildTOML` from `frontmatter.go` — they skip zero values, so pass every field unconditionally. Do not hand-roll YAML/TOML.
- If the tool has no per-rule directory, append rule bodies as `##`-headed sections to the root memory file via `buildRootMemoryContent` (see `gemini.go`, `opencode.go`, `codex.go`).
- If a canonical field maps to a different key in the target (e.g. Claude `paths:` → Cursor `globs:`), translate **inside this render func only** — don't push translation up the stack.

## 2. Register the tool

Edit `internal/tools/registry.go::All()` and add `{Meta: <tool>Meta, Render: render<Tool>}` to the slice. Ordering is **intentional, not alphabetical** — append new tools at the tail (`TestRegistryTailOrder` pins it) unless there's a reason otherwise.

## 3. Extend `internal/syncer/adopt.go` + `paths.go`

For each path the render func writes that maps reversibly back to a canonical entity:

1. Add the path's dir prefix / root-memory filename to the relevant slice in `internal/tools/paths.go` (the single owner of path vocabulary).
2. Ensure an `adopt.go` matcher recognizes it: root memory → the `isRootMemoryFile` / `case` switch calling `canonical.SaveAgentsMD`; rules → `matchRulePath` (`ruleFilename` strips `.md`/`.mdc`); skills → `matchSkillPath` (update `skillDir` if depth differs); agents → `matchAgentPath` / `matchOpenCodeAgentPath`; commands → `matchCommandPath`; or a dedicated per-tool matcher (see `matchCopilotInstructionPath`, `matchClineWorkflowPath`, `matchPiPromptPath`).
3. Declare the expectation in `tools.ExpectedAdoptOutcome` for each `(tool, concept, path)`: reversible to its own concept (the default), root-memory, cross-mapped, or `OutcomeNonReversible` with a `Reason`.

If the output isn't reversible (e.g. concatenated rule bodies, TOML agents), return `OutcomeNonReversible` with a reason — the render↔adopt contract test (`internal/syncer/contract_test.go`) checks render output against these declarations and fails on drift.

## 4. Add a roundtrip test

Add a per-tool roundtrip test under `internal/syncer/` (mirror `roundtrip_vibe_test.go` / `roundtrip_cline_junie_test.go`): build an in-code probe `canonical.Canonical`, render it for both scopes, `AdoptExternal` each reversible output back, and assert the canonical round-trips. The contract test already guards path-level parity; the roundtrip test guards byte-level fidelity.

## 5. Regenerate the metadata golden

`internal/tools/testdata/metadata_golden.json` + `TestMetadataParity` pin every tool's observable metadata. Regenerate and review the diff:

```bash
UPDATE_GOLDEN=1 go test ./internal/tools/ -run TestMetadataParity
```

The diff must contain only the new tool's entry.

## 6. Update the README

Edit `README.md`:

- "Supported AI tools" table — new row with paths and detection dir.
- "Concept compatibility" table — ✓ / ⚠ / ✗ per concept.
- "Field translation across tools" table — only if the render func renames any canonical field.
- "Tools that don't support user scope" / "user-scope output path differs" lists — add the tool if applicable.

## 7. Verify

Run, in order:

```bash
go vet ./...
go test ./...
make smoke
make sandbox-reset && make build && ./agentsync sync --workspace ./examples/sandbox
```

Then diff `examples/sandbox/.<tool>/` against your expectations.

## 8. Final review

Invoke the `adapter-reviewer` subagent on the new tool file before considering the task done. Apply its findings.
