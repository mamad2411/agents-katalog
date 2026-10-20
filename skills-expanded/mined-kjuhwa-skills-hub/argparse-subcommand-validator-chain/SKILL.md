---
name: argparse-subcommand-validator-chain
description: Structure multi-mode CLI with nested subcommands and a composable chain of pure-function validators
category: cli
version: 1.0.0
tags: [argparse, subcommands, validation, cli, python]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/OpenBMB/VoxCPM.git
source_ref: main
source_commit: 13605c5a0e6b99d6d3527a43bd1a4e0e69c8800e
source_project: VoxCPM
source_paths:
  - src/voxcpm/cli.py
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
---

# Structure multi-mode CLI with nested subcommands and validator chain

## When to use
Use this pattern when a CLI tool needs to support multiple modes (e.g., design, clone, batch) each with different required/forbidden argument combinations. It keeps validation logic testable in isolation and keeps the dispatch path clean — the mode handler receives only already-validated args, never raw input.

Reach for this when `argparse`'s built-in `required` and `mutually_exclusive_group` are insufficient because your validation rules are cross-argument (e.g., "if flag A is set, flag B must not be set AND file C must exist").

## Pattern

### 1. Define validators as pure functions
Each validator takes `args` (the parsed `Namespace`) and a `parser` reference, calls `parser.error()` on failure (which exits with usage), and returns nothing on success.

```python
def validate_file_exists(args, parser):
    if args.input and not Path(args.input).is_file():
        parser.error(f"Input file not found: {args.input}")

def validate_ranges(args, parser):
    if args.cfg_value is not None and not (0.0 <= args.cfg_value <= 10.0):
        parser.error("cfg_value must be between 0.0 and 10.0")

def validate_clone_args(args, parser):
    has_control = args.control is not None
    has_prompt  = args.prompt_audio is not None
    if has_control and has_prompt:
        parser.error("--control and --prompt-audio are mutually exclusive in clone mode")
```

### 2. Compose validators into a chain
```python
CLONE_VALIDATORS = [
    validate_file_exists,
    validate_ranges,
    validate_clone_args,
]

def run_validator_chain(validators, args, parser):
    for v in validators:
        v(args, parser)
```

### 3. Register subparsers with argparse
```python
def build_parser():
    parser = argparse.ArgumentParser(prog="voxcpm")
    sub = parser.add_subparsers(dest="mode", required=True)

    design_p = sub.add_parser("design")
    design_p.add_argument("--text", required=True)
    design_p.add_argument("--control", required=True)

    clone_p = sub.add_parser("clone")
    clone_p.add_argument("--input", required=True)
    clone_p.add_argument("--control")
    clone_p.add_argument("--prompt-audio", dest="prompt_audio")
    clone_p.add_argument("--cfg-value", type=float, dest="cfg_value", default=2.0)

    batch_p = sub.add_parser("batch")
    batch_p.add_argument("--list", required=True)

    return parser
```

### 4. Dispatch after validation
```python
def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.mode == "design":
        run_validator_chain(DESIGN_VALIDATORS, args, parser)
        handle_design(args)
    elif args.mode == "clone":
        run_validator_chain(CLONE_VALIDATORS, args, parser)
        handle_clone(args)
    elif args.mode == "batch":
        run_validator_chain(BATCH_VALIDATORS, args, parser)
        handle_batch(args)
```

## Source reference
- Upstream: `OpenBMB/VoxCPM` @ `main` / `13605c5a`
- Key files:
  - `src/voxcpm/cli.py:1-300` — full subcommand setup, all validator functions, and dispatch logic

## Notes
- `parser.error()` prints usage and exits with code 2 — it's the correct way to surface validation failures in argparse rather than raising exceptions yourself.
- Keep validators pure (no side effects, no I/O beyond file existence checks) so they can be unit-tested without invoking the full CLI.
- Avoid putting mode-specific logic inside validators; validators gate, handlers act.
