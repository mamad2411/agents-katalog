# Module: `output` (CLI-specific output concerns)

**Crate:** `shipper-cli`
**Single responsibility:** Format and present output to the user — progress bars, human-readable formatting, structured reporters.

## What lives here

- `output/progress/` — Progress bars and per-crate publish status (was `shipper-progress`, absorbed)
- Future: `output/format/`, `output/reporter/` as the CLI's output concerns split

## Boundary
- These modules know about terminal capabilities (color, TTY width, ANSI). The library `shipper` crate must NOT.
