---
name: lean-review
description: >
  Review a diff or a repo for over-engineering only. Returns a delete-list, not
  prose: one line per finding with location, what to cut, and what replaces it.
  Use when the user says "review for over-engineering", "what can we delete",
  "is this over-engineered", "find bloat", "audit for complexity", or invokes
  /lean-review. Correctness, security and performance are out of scope — those
  belong to code-reviewer and security-reviewer.
---

# Lean Review

Hunt unnecessary complexity. The best outcome of a diff is that it gets shorter.

Default scope is the working diff (`git diff`, or the staged/branch diff if the
user names one). Say `repo` or `whole codebase` to scan the entire tree instead,
ranked biggest cut first.

## Format

One line per finding. No preamble, no summary paragraph.

`L<line>: <tag> <what>. <replacement>.`

Use `<file>:L<line>: ...` for multi-file diffs and always for repo scans.

## Tags

- `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library already ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Examples

Not this — a suggestion with no decision in it:

> "This EmailValidator class might be more complex than necessary, have you
> considered whether all these validation rules are needed at this stage?"

This:

```
L12-38: stdlib: 27-line validator class. Regex + confirmation mail already covers it, 1 line.
L4: native: moment.js imported for one format call. Intl.DateTimeFormat, 0 deps.
L52-71: delete: retry wrapper around an idempotent local call. Nothing replaces it.
L30-44: shrink: manual loop builds an object. Object.fromEntries(pairs), 1 line.
src/api/client.ts:L88: yagni: options object where no caller passes options. Inline the defaults.
```

End with the only metric that matters:

`net: -<N> lines possible.` — repo scans add `, -<M> deps`.

Nothing to cut: `Lean already. Ship.` and stop.

## Out of scope — never flag these

- **Correctness bugs, security holes, performance.** Route to code-reviewer or
  security-reviewer. This pass only hunts complexity.
- **Tests and coverage.** Test-first is the standing rule; a test is never bloat.
- **File count.** Many small focused files is the house standard. Never propose
  merging files to reduce their number — only propose deleting code that does
  nothing.
- **House patterns.** Repository interfaces, the `ApiResponse<T>` envelope, and
  typed validation schemas are deliberate standards, not speculation. `yagni:`
  applies to abstractions invented for this change, not to the shared conventions.
- **Comments explaining WHY**, and `HACK:` markers naming a ceiling and its
  upgrade trigger.

## Boundaries

Lists findings. Applies nothing — the user decides what to cut. One-shot: report
and stop, do not continue into fixes.
