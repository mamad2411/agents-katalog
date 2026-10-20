---
name: mermaid-to-svg
description: Use when the user needs Mermaid diagram text rendered to SVG using the local warpdotdev/mermaid-to-svg Rust renderer, or when validating Mermaid-to-SVG output without Node/headless-browser dependencies.
license: MIT
metadata:
  source_repo: https://github.com/warpdotdev/mermaid-to-svg
---

# Mermaid to SVG

Use this skill to convert Mermaid diagram source into SVG with the local
`warpdotdev/mermaid-to-svg` checkout.

## Source

The persistent source clone is:

`/Users/marklindgreen/.skills-repos/mermaid-to-svg`

The repository is a Rust crate. It exposes `render_mermaid_to_svg` as a library
API and includes a CLI binary named `render_mermaid`.

## Workflow

1. Put the Mermaid source in a `.mmd` file or pipe it through stdin.
2. Render with the local checkout:

```bash
cargo run --quiet --manifest-path /Users/marklindgreen/.skills-repos/mermaid-to-svg/Cargo.toml --bin render_mermaid -- diagram.mmd > diagram.svg
```

For stdin:

```bash
printf 'graph TD; A-->B\n' | cargo run --quiet --manifest-path /Users/marklindgreen/.skills-repos/mermaid-to-svg/Cargo.toml --bin render_mermaid -- > diagram.svg
```

3. Inspect the SVG or open it in a browser/image viewer when visual proof is
   required.

## Notes

- Flowcharts are the primary supported diagram type.
- Some other Mermaid diagram types render experimentally and may not match
  Mermaid CLI parity.
- If a command fails, first run the same command without `--quiet` and inspect
  the Rust error instead of guessing.
