---
name: roundtrip-check
description: Verify that every adapter's Render output can be adopted back into canonical without drift. Catches mismatches between path conventions in internal/tools/ and reverse matchers in internal/syncer/adopt.go. Run after adding or modifying an adapter, or after editing adopt.go.
---

# Roundtrip Check: Render → Adopt → Compare

Goal: prove that for every adapter where `adopt.go` claims a path is reversible, `Render(canonical) → AdoptExternal(rendered_path) → reload canonical` produces the same canonical entity bytes.

## Procedure

Operate in a temp workspace — do not pollute `examples/sandbox/` or the repo's `.agentsync/`.

### 1. Build a probe canonical

Create `/tmp/agentsync-roundtrip/.agentsync/` with:

- `AGENTS.md` — non-trivial multi-line content with code fences and unicode.
- `rules/sample-rule.md` — frontmatter (`description`, `paths: [src/**/*.ts]`) + body.
- `skills/sample-skill/SKILL.md` — frontmatter with every field set (`name`, `description`, `allowed-tools`, `disable-model-invocation: true`, `paths`).
- `agents/sample-agent.md` — frontmatter (`name`, `description`, `tools`, `model: sonnet`) + body.
- `commands/sample-command.md` — frontmatter (`description`, `argument-hint`, `allowed-tools`, `model`) + body.

The reserved name `general` must not appear — it will fail load.

### 2. Render via every adapter for both scopes

Write a small Go test (or a `go run`-able script under `scripts/`) that:

```go
c, _ := canonical.Load(tmpWorkspace)
for _, a := range tools.All() {
    for _, scope := range []tools.Scope{tools.ScopeProject, tools.ScopeUser} {
        if !a.SupportsScope(scope).Supported { continue }
        writes, _ := a.Render(c, scope)
        for _, fw := range writes {
            // write fw to disk under tmpWorkspace
        }
    }
}
```

### 3. Adopt every written path

For each `fw.Path` written above, call `syncer.AdoptExternal(tmpWorkspace, fw.Path)`. Track which paths return errors — those are paths the adapter emits that `adopt.go` does not handle. Three valid outcomes:

- **Adopted successfully** — proceed to step 4.
- **Adopted with the wrong canonical entity** — bug in `adopt.go` matchers.
- **Returns "no canonical mapping for path"** — either expected (concatenated rule bodies, alias files like `general.mdc` → `AGENTS.md`) or a missing matcher. The adapter file should document which paths are intentionally non-reversible.

### 4. Compare canonical-after vs canonical-before

After adopting each path, reload canonical with `canonical.Load(tmpWorkspace)` and diff the relevant entity (rule/skill/agent/command/AGENTS.md) against the original byte-for-byte. Mismatches indicate frontmatter round-trip loss (e.g. field reordering, dropped fields, escaping changes).

Known acceptable lossy paths:

- `.cursor/rules/general.mdc` round-trips back to `AGENTS.md` with the Cursor frontmatter wrapper stripped. Compare body only, not frontmatter.
- Any tool that emits rules concatenated into the root memory cannot reverse-map individual rules — skip those paths.

### 5. Report

```
# Roundtrip check

## Adapters covered
<list>

## Paths written: N
## Paths adopted cleanly: N
## Paths intentionally skipped: N (with reason)
## Paths with adoption errors: N
## Paths with canonical drift after roundtrip: N

## Failures
- <path> — <reason / diff>
```

If any "adoption errors" or "canonical drift" rows are non-zero and not in the known-lossy list, the check fails. Surface the failures and stop — do not auto-fix.

## When to run

- After adding a new adapter (use the `add-adapter` skill, then this).
- After editing `internal/syncer/adopt.go` matchers.
- After changing a frontmatter field on `Rule`, `Skill`, `Agent`, or `Command` in `internal/canonical/types.go`.

This is not part of `make test` today. If you find yourself running it routinely, consider promoting the probe canonical to `testdata/scenarios/roundtrip/` and adding a `TestRoundtrip` table-driven test.
