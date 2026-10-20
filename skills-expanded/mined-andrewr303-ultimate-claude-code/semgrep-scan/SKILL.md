---
name: semgrep-scan
description: Semantic static analysis with Semgrep — run registry rulesets for security and correctness, write custom YAML rules with metavariables and taint mode, triage findings, and wire scans into CI. Use when hunting vulnerability patterns, enforcing guardrails across 30+ languages, or when a grep/ast-grep pattern needs semantic awareness (constant propagation, dataflow).
---

# Semgrep Scan

Semgrep is semantic grep for code: rules look like the code they match, and the
engine understands semantics — `grep "2"` matches the string `2`, while Semgrep
matches `x = 1; y = x + 1` when searching for `2` (constant propagation). It
supports 30+ languages and runs entirely locally; code is never uploaded by default.

## When to Use This Skill

| Scenario | Use this skill | Alternative |
|----------|---------------|-------------|
| Scanning for known vulnerability patterns (injection, secrets, crypto misuse) | Yes | N/A |
| Enforcing project guardrails ("never call X without Y") | Yes | `ast-grep-search` for pure structural match/rewrite |
| Dataflow questions (does user input reach this sink?) | Yes — taint mode | N/A |
| One codebase-wide structural rewrite | No — use `ast-grep-search` | `openrewrite-recipes` for type-aware JVM refactors |
| Broad anti-pattern sweep with bundled rules | `/ult-engineer:code-antipatterns` first | This skill for deeper security passes |
| Dependency CVE audit | No — use `/ult-engineer:code-dep-audit` | Semgrep Supply Chain (platform) |

Scope note: the open-source Community Edition analyzes within a single function/file
boundary. Cross-file and cross-function dataflow require the commercial platform —
report intra-file findings honestly and do not claim whole-program guarantees.

## Setup

Check availability: `semgrep --version`. Install (ask/notify the user first):

```bash
pip install semgrep        # or: pipx install semgrep
brew install semgrep       # macOS
docker run --rm -v "${PWD}:/src" semgrep/semgrep semgrep scan --config auto /src
```

## Running Scans

```bash
semgrep scan --config auto .                     # auto-select registry rules for the repo
semgrep scan --config p/security-audit .         # curated security ruleset
semgrep scan --config p/owasp-top-ten .          # OWASP Top 10 patterns
semgrep scan --config p/secrets .                # hardcoded credentials
semgrep scan --config ./semgrep-rules/ src/      # local custom rules only
semgrep scan --config auto --severity ERROR .    # highest-severity only
semgrep scan --config auto --json > findings.json
semgrep scan --config auto --sarif > findings.sarif
semgrep scan --config ./rules/ --autofix .       # apply `fix:` transformations
```

`--config auto` contacts the Semgrep registry to pick rules (and sends scan
metrics); use pinned `p/<ruleset>` or local `--config ./rules/` for offline or
metrics-free runs.

## Writing Custom Rules

One YAML file per concern. Validate with `semgrep --validate --config rule.yml`.

```yaml
rules:
  - id: no-dynamic-sql
    languages: [python]
    severity: ERROR
    message: SQL built via f-string/concat — use parameterized queries.
    patterns:
      - pattern-either:
          - pattern: cursor.execute(f"...")
          - pattern: cursor.execute("..." + $X)
          - pattern: cursor.execute("...".format(...))
      - pattern-not-inside: |
          def test_...(...):
              ...
```

Key operators: `pattern`, `pattern-either` (OR), `patterns` (AND),
`pattern-not` (exclude), `pattern-inside` / `pattern-not-inside` (context),
`metavariable-pattern` and `metavariable-comparison` (constrain `$X`),
`fix:` (autofix template). `...` matches any sequence; `$X` binds and must
match consistently within a rule.

### Taint Mode

Track untrusted data from sources to sinks, minus sanitizers:

```yaml
rules:
  - id: request-to-subprocess
    languages: [python]
    severity: ERROR
    message: User-controlled input reaches a shell command.
    mode: taint
    pattern-sources:
      - pattern: flask.request.args.get(...)
    pattern-sinks:
      - pattern: subprocess.run($CMD, ..., shell=True)
    pattern-sanitizers:
      - pattern: shlex.quote(...)
```

### Testing Rules

Put annotated fixtures next to the rule and run `semgrep --test rules/`:
`# ruleid: no-dynamic-sql` above a line that must match,
`# ok: no-dynamic-sql` above one that must not.

## Workflow

1. **Baseline** — run the broad config for the repo's stack, capture `--json`.
2. **Triage** — group findings by `check_id`; classify each rule's hits as
   true positive, false positive, or accepted risk. Never bulk-suppress.
3. **Narrow** — for confirmed classes, write a precise custom rule (with `fix:`
   where mechanical) instead of hand-fixing occurrences one by one.
4. **Fix** — apply autofixes or edit; re-run the same config to verify zero
   findings for the addressed rule ids.
5. **Guard** — add `semgrep ci` (or `semgrep scan --error --config <pinned>`)
   to CI so the class stays fixed; `--error` makes findings fail the build.
6. Inline suppressions (`# nosemgrep: <rule-id>`) require a justification
   comment — flag bare `nosemgrep` in review (they are exactly the silent
   suppression `/ult-engineer:code-hidden-failures` hunts).

## Related Skills

- `ast-grep-search` — structural search/replace; faster for syntax-shape queries and rewrites
- `/ult-engineer:code-antipatterns` — bundled ast-grep anti-pattern sweep
- `/ult-engineer:code-hidden-failures` — swallowed-error and silent-degradation detection
- `openrewrite-recipes` — type-aware, build-integrated remediation for JVM codebases
- `/ult-engineer:code-dep-audit` — dependency CVE / license audit
