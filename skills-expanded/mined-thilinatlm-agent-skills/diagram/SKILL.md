---
name: diagram
description: This skill should be used when the user asks to "render a diagram", "draw a diagram", "create a diagram from text", "convert PlantUML to SVG", "render Mermaid", "render PlantUML", "render GraphViz", "render D2", "render DBML", "render BPMN", "convert .puml to png", "convert .mmd to svg", "make a flowchart", "make a sequence diagram", "make an ERD", "draw a UML diagram", "diagram as code", "Kroki", "C4 diagram", or otherwise needs to convert textual diagram source (PlantUML, Mermaid, GraphViz/dot, D2, DBML, BPMN, Excalidraw, Erd, Ditaa, Nomnoml, Pikchr, Structurizr, SvgBob, TikZ, Vega/Vega-Lite, WaveDrom, WireViz, BlockDiag family) into SVG, PNG, PDF, or JPEG. Backed by the Kroki HTTP service — no local diagram toolchain required.
---

# diagram

CLI for rendering text-based diagrams (PlantUML, Mermaid, GraphViz, D2, DBML, BPMN, C4, Erd, Ditaa, Nomnoml, Pikchr, Structurizr, SvgBob, TikZ, Vega, Vega-Lite, WaveDrom, WireViz, BlockDiag / SeqDiag / ActDiag / NwDiag / PacketDiag / RackDiag, Excalidraw, Bytefield, Symbolator, UMlet) to SVG / PNG / PDF / JPEG / TXT / Base64 via the [Kroki](https://kroki.io) HTTP API. JSON output.

## CLI

- Path: `./diagram-cli/diagram` (relative to this SKILL.md). On Windows use `diagram.cmd` or `diagram.ps1`.
- Requires `uv` ([install](https://docs.astral.sh/uv/)). First call provisions the Python environment automatically.
- Subcommands: `render` (primary), `types` (capability discovery).
- Run `diagram render --help` for current flags.

## Endpoint resolution

The CLI picks the Kroki endpoint in this order:

1. `--endpoint <url>` flag
2. `KROKI_URL` environment variable
3. `.kroki-url` file (one URL, no quotes) walked up from the current working directory — useful for pinning a project to a self-hosted Kroki without touching shell config
4. `https://kroki.io` (default, free public instance)

Add `.kroki-url` to `.gitignore` if it points to an internal hostname.

## Subcommands

### `diagram render`

Renders one diagram and writes the output to a file. Always pass `--output <path>` — the JSON envelope is the only thing on stdout; the rendered bytes go to the file. After a successful call, use the Read tool on the produced `file` path to confirm the output looks right.

| Flag                 | Description                                                                                                |
| -------------------- | ---------------------------------------------------------------------------------------------------------- |
| `--input <path>`     | Read diagram source from a file. Extension drives type auto-detect (see table below).                      |
| `--source "<text>"`  | Inline diagram source (alternative to `--input`).                                                          |
| stdin                | Used when neither `--input` nor `--source` is given and stdin is piped.                                    |
| `--type <name>`      | Diagram type (e.g. `plantuml`, `mermaid`, `graphviz`, `d2`). Required if not derivable from the extension. |
| `--format <name>`    | Output format. Default `svg`. Support varies by type — see `diagram types`.                                |
| `--output <path>`    | **Required.** Output file. Parent directories are created.                                                 |
| `--endpoint <url>`   | Override Kroki endpoint (also `KROKI_URL`, `.kroki-url`).                                                  |
| `--timeout <secs>`   | HTTP timeout. Default `30`.                                                                                |

Examples:

```bash
# Auto-detect type from extension (.mmd → mermaid), default SVG
./diagram-cli/diagram render --input docs/flow.mmd --output docs/flow.svg

# PlantUML to PNG with explicit type/format
./diagram-cli/diagram render --input arch.puml --type plantuml --format png --output assets/arch.png

# Inline GraphViz
./diagram-cli/diagram render \
  --type graphviz \
  --source 'digraph G { Hello -> World }' \
  --output /tmp/hello.svg

# Stdin
cat diagram.d2 | ./diagram-cli/diagram render --type d2 --output diagram.svg

# Self-hosted Kroki
KROKI_URL=http://kroki.internal:8000 ./diagram-cli/diagram render \
  --input flow.puml --output flow.svg
```

Success output:

```json
{"ok":true,"file":"/abs/path/flow.svg","type":"plantuml","format":"svg","bytes":12345,"endpoint":"https://kroki.io","sourceOrigin":"file"}
```

### `diagram types`

Lists supported diagram types and their formats. No network call — the table is baked into the CLI. Use this to discover what `--type` / `--format` combinations are valid before calling `render`.

```bash
./diagram-cli/diagram types            # all types
./diagram-cli/diagram types mermaid    # one type
```

## Supported diagram types (summary)

| Type          | File extensions                | Output formats              |
| ------------- | ------------------------------ | --------------------------- |
| `plantuml`    | `.puml`, `.plantuml`, `.iuml`  | svg, png, pdf, txt, base64  |
| `mermaid`     | `.mmd`, `.mermaid`             | svg, png                    |
| `graphviz`    | `.dot`, `.gv`                  | svg, png, jpeg, pdf         |
| `d2`          | `.d2`                          | svg                         |
| `dbml`        | `.dbml`                        | svg                         |
| `bpmn`        | `.bpmn`                        | svg                         |
| `c4plantuml`  | `.c4`, `.c4puml`               | svg, png, pdf, txt, base64  |
| `erd`         | `.erd`                         | svg, png, jpeg, pdf         |
| `ditaa`       | `.ditaa`                       | svg, png                    |
| `excalidraw`  | `.excalidraw`                  | svg                         |
| `nomnoml`     | `.nomnoml`                     | svg                         |
| `pikchr`      | `.pikchr`                      | svg                         |
| `structurizr` | `.structurizr`, `.dsl`         | svg, png, pdf, txt, base64  |
| `svgbob`      | `.svgbob`                      | svg                         |
| `tikz`        | `.tikz`                        | svg, png, jpeg, pdf         |
| `vega`        | `.vega`                        | svg, png, pdf               |
| `vegalite`    | `.vl`, `.vegalite`             | svg, png, pdf               |
| `wavedrom`    | `.wavedrom`                    | svg                         |
| `wireviz`     | `.wireviz`                     | svg, png                    |
| `bytefield`   | `.bytefield`                   | svg                         |
| `symbolator`  | —                              | svg                         |
| `umlet`       | —                              | svg, png, jpeg              |
| `blockdiag` family (`blockdiag`, `seqdiag`, `actdiag`, `nwdiag`, `packetdiag`, `rackdiag`) | matching `.*diag` extension | svg, png, pdf |

Run `diagram types` for the machine-readable, always-current list.

## Workflow guidance

- Default to SVG. It scales, embeds cleanly in HTML/Markdown, and every diagram type supports it. Switch to PNG only when the consumer can't render SVG (image-only chat, certain markdown renderers).
- Prefer writing the diagram source to a file with an unambiguous extension (`.puml`, `.mmd`, `.dot`, etc.). The CLI then auto-detects `--type` and you keep the source under version control alongside the rendered output.
- When `RENDER_FAILED` comes back, the `hint` field contains Kroki's syntax-error message — surface it verbatim to the user and to your reasoning. Most of the time it includes a line number.
- For very large diagrams, raise `--timeout`. The default 30 s is generous for Kroki's free instance but a self-hosted one rendering complex PlantUML or TikZ may need more.

## Error codes

| Code                 | Meaning                                                                          |
| -------------------- | -------------------------------------------------------------------------------- |
| `PREREQ_MISSING`     | `uv` is not installed.                                                           |
| `INPUT_CONFLICT`     | More than one of `--input` / `--source` / stdin was provided.                    |
| `INPUT_MISSING`      | No diagram source was provided.                                                  |
| `INPUT_NOT_FOUND`    | `--input` path does not exist, is not a file, or could not be decoded as UTF-8.  |
| `OUTPUT_MISSING`     | `--output` was not provided.                                                     |
| `TYPE_MISSING`       | Type was not given and could not be inferred from the input file extension.      |
| `TYPE_UNKNOWN`       | Type name is not in the supported list — run `diagram types`.                    |
| `FORMAT_UNSUPPORTED` | The `(type, format)` combination is not supported by Kroki for that type.        |
| `RENDER_FAILED`      | Kroki returned 4xx. Usually a syntax error in the source; details in `hint`.     |
| `KROKI_UNAVAILABLE`  | Network failure, timeout, or Kroki returned 5xx.                                 |
| `IO_ERROR`           | Could not write the `--output` file.                                             |
| `INTERNAL_ERROR`     | Unexpected CLI failure — file a bug if you see this.                             |
