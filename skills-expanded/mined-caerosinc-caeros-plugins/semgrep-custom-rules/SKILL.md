---
name: semgrep-custom-rules
description: Write custom Semgrep rules, pattern syntax, metavariables, taint mode, autofix, and rule testing. Use when the user wants to encode a security invariant or ban a dangerous pattern in their own codebase.
---

# Semgrep custom rules

Rules are YAML. Minimum viable rule:

```yaml
rules:
  - id: no-string-built-sql
    languages: [python]
    severity: ERROR
    message: >
      SQL built by string interpolation. Use parameterized queries
      (cursor.execute(sql, params)) to prevent injection.
    patterns:
      - pattern: cursor.execute(f"...")
```

Run it: `semgrep scan --config rules/no-string-built-sql.yaml src/`.

## Pattern syntax essentials

- `...` matches any sequence of args/statements: `open(...)`.
- `$X` metavariable matches one expression and can be reused:
  `foo($X, $X)` finds calls with a repeated argument.
- `"..."` matches any string literal; `f"..."` any f-string.
- Patterns are semantic, not textual: `requests.get(...)` also matches
  `import requests as r; r.get(...)`.

## Combining patterns

```yaml
patterns:                      # AND semantics
  - pattern: subprocess.run(...)
  - pattern-not: subprocess.run(..., shell=False)
  - pattern-inside: |
      def $FUNC(..., request, ...):
          ...
```

- `pattern-either`: OR list of alternatives.
- `pattern-not` / `pattern-not-inside`: carve out safe usages.
- `pattern-regex`: raw regex when semantics do not help (config files).
- `metavariable-pattern` / `metavariable-regex`: constrain what a
  metavariable may match, e.g. only when `$X` matches `flask.request.*`.

## Taint mode (source to sink)

```yaml
rules:
  - id: request-to-query
    languages: [python]
    severity: ERROR
    message: Untrusted request data reaches a SQL sink unescaped.
    mode: taint
    pattern-sources:
      - pattern: flask.request.args.get(...)
    pattern-sinks:
      - pattern: cursor.execute($SINK, ...)
    pattern-sanitizers:
      - pattern: sqlescape(...)
```

Taint mode follows data flow through assignments and calls inside a file,
which kills most false positives that plain patterns produce for injection
classes.

## Autofix

```yaml
    pattern: requests.get($URL, verify=False)
    fix: requests.get($URL, verify=True)
```

Apply with `semgrep scan --config rule.yaml --autofix` (add `--dry-run` first).
Metavariables carry over from pattern to fix. Keep fixes strictly equivalent
plus safe; anything judgment-based should stay a message, not a fix.

## Testing rules

Create a test file next to the rule with annotated lines:

```python
# ruleid: no-string-built-sql
cursor.execute(f"SELECT * FROM t WHERE id = {uid}")
# ok: no-string-built-sql
cursor.execute("SELECT * FROM t WHERE id = %s", (uid,))
```

Run `semgrep --test rules/`. CI should run rule tests like unit tests. The
interactive editor at https://semgrep.dev/playground is the fastest way to
iterate on a pattern before committing it.

## Rule hygiene

- One invariant per rule id; stable ids (they appear in `nosemgrep` comments).
- `message` must say why it is dangerous and what to do instead.
- Set `metadata` (cwe, owasp, references) so triage tooling can rank findings.
