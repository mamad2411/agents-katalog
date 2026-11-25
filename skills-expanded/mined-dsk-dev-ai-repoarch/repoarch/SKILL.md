# repoarch

Turn a codebase or a natural-language description into a clean architecture
diagram — as Mermaid source or a self-contained HTML file. No AI model, no
server, no dependencies. Works offline on any laptop.

## When to use

Use repoarch when the user wants to **see how a codebase is structured**:
dependency maps, module / component relationships, folder-level architecture,
or a high-level system overview. It is ideal for:

- Documenting a project before writing docs
- Onboarding onto an unfamiliar repository
- Reviewing the shape of a PR / module before reviewing code
- Generating a shareable `architecture.html` for READMEs or presentations

## Install

```bash
# CLI (recommended)
pip install repoarch
```

If the CLI is not installed but the skill lives inside a checkout or skill
bundle, you can run it in place:

```bash
python -m repoarch <path> -o <out_dir>
```

## Usage

```bash
# generate diagrams for any folder (default output: current dir)
repoarch /path/to/codebase -o out/

# pipe / wrap for the user
repoarch <path> -o <out_dir> [--name TITLE] [--min-degree N]
```

### Parameters

| Argument | Description |
|---|---|
| `path` | Codebase path (default: current directory) |
| `-o, --output` | Output directory for `architecture.html` and `architecture.mmd` |
| `--name` | Custom diagram title (default: folder name) |
| `--min-degree N` | Drop low-importance (low-degree) components to declutter large projects |

### Output

- `architecture.html` — a single, self-contained, interactive diagram
  (dark/light theme, zoom) that opens in any browser. Ideal for sharing.
- `architecture.mmd` — raw Mermaid `flowchart LR` source.

## Detectable languages

Python · Go · JavaScript · TypeScript · Java · Rust · Ruby · PHP · C · C++ · C#

## Notes

- Requires Python 3.8+.
- Pure standard library — no network, no API keys, no telemetry.
- For a quick visual demo, run against this repository's `sample/` folder.
