---
name: agent-terms-define
description: 'Authoritative dictionary of standard developer abbreviations for variables, functions, classes, CSS classes and terse technical writing, injected at session start. Use when naming identifiers or abbreviating. RU: сокращения, аббревиатуры, именование переменных.'
disable-model-invocation: true
---

# abbreviations — naming & terse-writing dictionary

Single source of truth for standard abbreviations in names (vars / fns / classes
/ CSS classes / tokens) and terse text (comments, commit msgs, logs).

Resolve the canonical dictionary and any optional local capture buffer through
the available runtime or plugin interface. Some runtimes can inject these inputs
at session start; verify the actual hook registration and supplied context before
assuming they are present. Otherwise read the available dictionary through its
supported interface when needed. Do not duplicate the canonical dictionary.

## Policy

- **Only mainstream, at-a-glance abbrs.** Ones any dev recognizes on sight. No
  private / project / company jargon in the canonical dict (shared across all
  projects, no personal data). Dubious / local / stack-specific → spell the word
  out in full, don't add it.
- **Names self-explain.** A var / fn / class / CSS class / token must be clear
  from its name alone; if you must comment what a name means, rename it.
- **Comments explain "why", not "what".** Minimal comments — only a nontrivial
  edge case, a bug workaround, a hidden invariant. A good name needs no "what".

## Disambiguation

The 2-col data file can't resolve ambiguity — pick the explicit form, don't guess:

- `res` — if a module already uses `res`=resource, use `resp` for response.
- `acc` — accumulator vs account: on any risk of confusion, spell it out.
- `tx` — transaction (the default); in net/radio code spell out transmit/text.
- `mux` — mutex vs multiplexer (HTTP router): qualify by context.
- `ns` — namespace vs nanosecond: pick the explicit name.
- `ref` vs `ptr` — `ref` = logical reference/key, `ptr` = pointer.

## Growing the dictionary

Coined or hit a genuinely mainstream abbr missing from both files → append it to
the capture buffer, and periodically promote buffer rows into canonical. Full
flow (buffer format, append snippet, promotion steps) → [growing.md](growing.md).
