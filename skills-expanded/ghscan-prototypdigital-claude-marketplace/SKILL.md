---
name: docs-upkeep
description: Updates affected docs in the same task as code or workflow changes — README, API docs, CLI --help, config, wiki. Use when renaming endpoints, adding flags/config, or fixing stale references.
---

# docs-upkeep

Use this skill when code or workflow changes affect documented behavior.

## Triggers

- Code change that alters documented behavior or public API
- New feature, endpoint, or configuration option that needs documentation
- Workflow, CI, or deployment process change

## Does this change need docs?

```text
Does the change alter a documented surface
(endpoint, flag, config key, public API)?
  YES → update docs in THIS task (see Protocol)
  NO  → skip (internal refactor, test-only, private helper)
```

## Protocol

Formatting, prose style, and lint are out of scope here — they belong to the
formatting/lint rules. This skill only ensures docs stay in sync with the surface.

### Step 1 — Find every doc that references the changed surface

Grep the old name across all doc surfaces before touching anything.

```bash
grep -rn "GET /v1/orders" README.md docs/ wiki/ examples/
grep -rn "\-\-old-flag" README.md docs/ wiki/
grep -rn "old_config_key" docs/ examples/ *.example.yaml
```

### Step 2 — Update each hit in the same commit

Apply the new endpoint/flag/key/path to every file the grep returned. Do not
defer any to a follow-up commit — the doc change ships with the code change.

### Step 3 — Hunt stale references

Look beyond the renamed surface for collateral rot.

```bash
grep -rn "old-feature-name" docs/ wiki/        # removed features
grep -rn "](.*\.md)" docs/ | grep -v http      # then verify each link target exists
```

Fix dead links, renamed-file references, and mentions of removed features.

### Step 4 — Re-run doc code examples

Recompile or execute every code block you touched so examples stay valid.

```bash
ts-node docs/examples/usage.ts
bash docs/examples/quickstart.sh
```

### Step 5 — Note doc changes in the commit / handoff

Call out which docs moved in the commit message or handoff summary so reviewers
can confirm the surface and its docs landed together.

## Example

```text
BAD:  Rename GET /v1/orders → GET /v1/purchases in the handler,
      leave README curl examples pointing at /v1/orders.

GOOD: grep -rn "/v1/orders" README.md docs/ examples/
      → update README + API docs + curl examples in the SAME commit.
```

## Completion checklist

- [ ] Grepped the old endpoint/flag/key/path across README, docs/, wiki/, examples/
- [ ] Updated every hit in the same commit as the code change
- [ ] Fixed stale references — dead links, renamed files, removed features
- [ ] Re-ran or recompiled every doc code example that was touched
- [ ] Noted the doc changes in the commit message or handoff summary

## When NOT to use

- Internal refactors that don't change external behavior or API surface
- Changes to test files only
