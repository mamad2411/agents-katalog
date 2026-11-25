---
name: update-foundation-models-apis
description: Audits Apple FoundationModels documentation through apple-doc-mcp, refreshes symbol-index.md, records OS-version deltas, and verifies deprecations and changed guidance. Use after an OS/Xcode release or when asked to verify new Foundation Models symbols. Network access and apple-doc-mcp required.
---

# Update Foundation Models API reference

Regenerate the local symbol catalog and OS-version guidance for this repository's `apple-foundation-models-skill/references/`.

## Prerequisites

- A configured `apple-doc-mcp` / `apple-doc-mcp-server`
- Write access to this repo

## Workflow

### 1. Select Foundation Models

Use `discover_technologies`, then `choose_technology` with `doc://com.apple.documentation/documentation/FoundationModels`. Record the MCP server version.

### 2. Breadth-first documentation traversal

Seed the queue with `documentation/FoundationModels` and retrieve it through `get_documentation`.

For each retrieved page:

- Parse `references` object.
- Enqueue every unseen path whose URL starts `/documentation/foundationmodels`.
- Retrieve every queued category, article, sample, type, protocol, property, initializer, method, enum case, nested type, and relationship page through `get_documentation`.
- Record failed fragment URLs separately; do not treat anchors as symbols.
- Retrieve directly linked cross-framework pages needed to validate Foundation Models guidance, such as the PCC entitlement, Vision tools, and Evaluations integration.

### 3. Rebuild `symbol-index.md`

Emit a markdown table:

- Columns: Path, Kind (`symbolKind` / article kind), Min platform (prefer iOS `introducedAt`, otherwise the first documented platform), Title.

Sort paths lexicographically.

### 4. Fetch release notes

**Required URL:** `https://developer.apple.com/documentation/Updates/FoundationModels`

Update the applicable OS delta reference with every documented release-note bullet and migration.

### 5. Delta and quality audit

- Filter metadata by the target OS `introducedAt`, `deprecatedAt`, `renamed`, and availability fields.
- Group member-level additions under their owning type so the skill remains an operating manual rather than an API dump.
- Compare every group and release-note topic with the existing references.
- Remove APIs or behaviors that the current Apple documentation does not establish. Never infer signatures.
- Keep examples compilable and aligned with current declarations.

### 6. Spot-check high-traffic types

Manually re-fetch markdown or JSON for:

- `LanguageModelSession`
- `SystemLanguageModel`
- `Generable`
- `Tool`
- `Transcript`
- `ContextOptions`
- `LanguageModelError`
- `LanguageModel`
- `PrivateCloudComputeLanguageModel`
- `LanguageModelSession/GenerationError`

Verify no signature drift against man-pages; update reference files if fragments changed.

### 7. Required second pass

- Re-read every module-root category and compare its members with the first-pass manifest.
- Re-run the references-closure check; unresolved unseen Foundation Models paths must be zero.
- Re-check the release notes, deprecation/rename set, and all high-traffic types.
- Run repository validation and scan for stale names, unsupported claims, broken relative links, and unindexed reference files.

### 8. Delivery

- Report traversal count, target-OS path count, deprecations/renames, failures, changed files, and validation evidence.
- Commit, branch, push, or open a PR only when explicitly requested.

## apple-doc-mcp tools

| Tool | Use |
|------|-----|
| `discover_technologies` | Resolve the Foundation Models technology identifier |
| `choose_technology` | Scope subsequent symbol operations |
| `get_documentation` | Retrieve a known category, article, symbol, or member path |
| `search_symbols` | Cross-check wildcard, exact-name, and keyword discovery |
| `get_version` | Record the source tool version |

If apple-doc-mcp is unavailable, stop and report the blocker; do not silently substitute prior knowledge or another documentation mirror.
