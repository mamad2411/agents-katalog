---
name: verify
description: Re-execute a demo's verification steps to check for regressions. Compares current results against original evidence and produces a verification report.
argument-hint: '<feature-name>'
disable-model-invocation: true
---

User's request: $ARGUMENTS

# Verify Demo

You are re-running all verification steps from an existing demo document to check that everything still works. This catches regressions.

## Project Discovery

Read and follow `${CLAUDE_PLUGIN_ROOT}/references/project-discovery.md`.

Store the resolved base directory as `$DEMO_BASE`.

## Parse Arguments

Extract the feature name from `$ARGUMENTS`. If missing, list available demos and ask:

```bash
ls "$DEMO_BASE/"*.md 2>/dev/null | grep -v index.md | while read f; do basename "$f" .md; done
```

Use `AskUserQuestion` to ask which demo to verify.

## Read the Demo Document

```bash
cat "$DEMO_BASE/demo.md"
```

If the file doesn't exist, stop and tell the user:

> No demo found for `<feature-name>`. Available demos: <list>
>
> Run `/showboat:demo <feature-name>` to create a demo first.

## Run Verification

Use the showboat CLI to re-execute all code blocks and compare against recorded output:

```bash
showboat verify "$DEMO_BASE/demo.md"
```

The command prints diffs for any blocks whose output has changed and exits with code 1 if there are differences, 0 if everything matches.

If you want to update the document with new outputs without modifying the original:

```bash
showboat verify "$DEMO_BASE/demo.md" --output "$DEMO_BASE/<feature-name>-reverified-<YYYY-MM-DD>.md"
```

## Done

Report the results:

```
Verification complete: <feature-name>

<If showboat verify exited 0:>
  All checks passed — no regressions detected.

<If showboat verify exited 1:>
  Regressions detected — see diff output above.
  Run with --output to produce an updated copy of the document.
```
