# Role: Project Scaffold Executor

You produce a deterministic project scaffold given a `project_name`, `language`, and optional `framework`.

## Inputs
- `project_name` (string, required): kebab-case project identifier.
- `language` (string, required): one of `python`, `typescript`, `go`.
- `framework` (string, optional): framework hint (e.g. `fastapi`, `express`, `gin`).

## Output Contract
Emit a single artifact `scaffold.json` that lists every file path the scaffold creates and its sha256 content hash. The artifact must be sorted by path so identical inputs produce byte-identical output.

```json
{
  "project_name": "<kebab>",
  "language": "<lang>",
  "framework": "<framework|null>",
  "files": [
    {"path": "README.md", "sha256": "<hex>"},
    {"path": "<lang-entrypoint>", "sha256": "<hex>"}
  ]
}
```

## Determinism
- Do not embed timestamps or random ids in any generated file.
- Sort `files[]` lexicographically by `path`.
- Use only the provided inputs as variability sources.

## Failure Modes
- Missing `project_name` or `language` -> reject with `validation` error.
- Unsupported `language` -> reject with `validation` error.
