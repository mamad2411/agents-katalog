---
name: hissab-cli
description: Use the Hissab calculator CLI to evaluate deterministic math, unit conversions, date/time arithmetic, percentages, statistics, bitwise ops, number-system conversion, and color math from natural-language prompts. Invoke when the user asks for any calculation that should be hallucination-free, when they reference Hissab, or when results need exact precision the model should not compute itself. The skill translates natural-language intent into Hissab expressions, shells out to the local `hissab` binary via Bash, and parses stdout.
---

# Hissab CLI

Offload deterministic computation to the local `hissab` binary instead of computing it yourself. Translate the user's intent into valid Hissab syntax, run the binary, and narrate the result.

## When to invoke

- Any arithmetic, percentage, unit conversion, statistical, date/time, bitwise, number-system, or color calculation.
- Whenever the user mentions Hissab.
- Whenever exact precision matters (financial, scientific, engineering numbers).
- Whenever you would otherwise be tempted to do mental math — let the engine do it.

## Prerequisites

Verify the binary is on `$PATH`:

```bash
command -v hissab
```

If it's missing, fall back to running through the workspace from the repo root:

```bash
pnpm -F cli dev <command> [args]
```

## Workflow

1. **Identify the mathematical intent** in the user's prompt. If there is none, do not invoke this skill.
2. **Skim the base reference** in [`documentation.md`](./documentation.md) for the basics (expressions, brackets, labels, `prev`) and the catalog of categories Hissab supports.
3. **Fetch detailed docs for any unfamiliar category** before writing expressions for it:
   - List available categories: `hissab docs --list`
   - Fetch a specific category: `hissab docs <tag>` (e.g. `hissab docs compound_units`)
   - Full reference for large-context LLMs: `hissab docs --all`

   Skip the fetch for plain arithmetic; pull a chunk for anything else you're not already confident about (units, dates, statistics, color, bitwise, etc.). If your context window can comfortably hold the complete reference, you may run `hissab docs --all` once instead of fetching chunks incrementally.
4. **Formulate Hissab expression(s)** using the syntax. Use parentheses to match the user's intended grouping. Include units inline (e.g. `15 kilometers to miles`).
5. **Run the CLI**:
   - One expression: `hissab eval "<expr>"`
   - Multiple expressions that share labels or use `prev`: write them one-per-line to a temp file and run `hissab run <file>` so they share variable scope.
   - Discovery: `hissab list functions | units | operators`.
6. **Read stdout** for the result. On non-zero exit, read stderr — fix syntax and retry (fetch the relevant docs chunk if you haven't yet), or tell the user this calculation isn't something Hissab can do (cite the limitation, see below).
7. **Render a concise natural-language answer** that directly addresses the original prompt. Answer in the user's language.

Always quote the expression — operators like `*`, `&`, `|`, `<<`, `>>`, `~`, `!`, `^`, parens, and `;` are shell metacharacters.

## Examples

### Single expression
User: *"what's 15% off $240?"*

```bash
hissab eval "240 - 15%"
# 204
```

Reply: "$204."

### Unit conversion
User: *"convert 5'9'' to centimeters."*

```bash
hissab eval "5 feet + 9 inches to centimeters"
# 175.26 centimeters
```

### Shared scope across expressions
User: *"I make $4500/month, spend $1200 on rent and $600 on food. What's my yearly savings?"*

Write `/tmp/calc.hsb`:

```
monthly_savings = 4500 - 1200 - 600
prev yearly
```

Run:

```bash
hissab run /tmp/calc.hsb
```

Use the second line of output as the yearly savings figure in your reply.

### Date math
User: *"I was born on 15 June 1995. How old am I?"*

```bash
hissab eval "today - 15 jun 1995 to years"
```

## Limitations — surface these instead of guessing

- **No currency conversion.** Ask the user for the rate, or fetch one yourself first, then build the expression with the literal rate. Do not hallucinate FX rates.
- **Temperature and Duration units do not support multi-target breakdown.** Use separate expressions per target unit instead of `25 celsius to fahrenheit, kelvin`.
- **`prev` refers only to the immediately previous expression.** For anything further back, use a labelled expression (`my_total = …`) and refer to the label.
- **`m` is a million multiplier**, not meter. When writing compound units, spell out `meter` (e.g. `9.8 meter/second^2`). See `hissab docs compound_units` for details on supported compound unit forms.

## Output format

Plain text on stdout, errors on stderr, non-zero exit code on failure. Pipe-friendly — safe to use in shell pipelines.

## Reference

- Base reference (loaded with this skill): [`documentation.md`](./documentation.md)
- Per-category chunks: `hissab docs <tag>` (e.g. `hissab docs date_time`); `hissab docs --list` for the tag catalog.
- CLI source: `cli/` in the [hissab repo](https://github.com/rawbytess/hissab)
- Engine docs: https://hissab.io/guide/introduction
