---
name: reference-hunt
description: >-
  Port the semantics of a reference implementation by reading its actual
  source, not screenshots or docs. Use when the user says "reference hunt",
  "照着这个实现", "像这个一样", "要做成像 X 那样", "抄作业" while pointing at
  a concrete product, library, or code, says "find me a reference implementation"
  or "steal X's logic", asks "how does <product> do that? I want that here" —
  the question is the trigger — or struggles to articulate a behavior they
  can recognize. If the user has no reference — or has one but wants several
  divergent directions to react to — use design-directions (a reference hunt
  can feed it one direction's semantics). Not for finding documentation or
  tutorials, and not for merely matching the project's existing code style.
---

# Reference Hunt

Sometimes the user cannot describe what they want in words — showing beats
telling. The best reference is source code.

## Workflow

1. **Get a pointer.** If the user already named a reference (a library, a
   vendored crate, a folder, a component on a website), start there. If not,
   propose 2-3 candidate references yourself — from the codebase, vendored
   dependencies, or well-known open-source implementations — and let the user
   pick. One short message, not an interview.
2. **Read the real implementation.** Locate the source in this order:
   `node_modules`/vendored copies inside the project → the package's
   repository at the installed version (`npm view <pkg> repository` or the
   ecosystem's equivalent, then fetch the tagged file) → GitHub code search
   (needs auth; anonymous fallback: shallow-clone the repo or fetch raw
   files by path from raw.githubusercontent.com). For a website module,
   read the underlying markup and code. Read the source, not its README,
   docs, or a screenshot. **Also skim its test file** — edge-case semantics
   (ordering, error paths, boundary values) live in tests more reliably
   than in the implementation body. A different language from the target
   is fine; semantics transfer, syntax does not. When the reference's
   framework differs from the target's, list which behaviors are carried
   by framework scheduling (pre-paint effects, batched updates,
   subscription timing) — re-create those deliberately; they neither
   transfer for free nor count as mere syntax.
3. **Write down what you are taking.** Before implementing, give the user a
   short list, in the language of the conversation: the semantics being
   ported and what is deliberately *not* being ported. Cover five dimensions:
   inputs/API shape, outputs and return values, state transitions, edge
   cases, failure behavior. The list must outlive the chat:
   - if implementation starts now, record the ported semantics under
     Context and your own deliberate deviations under Decisions in
     `implementation-notes.md` (per the implementation-notes skill);
   - otherwise write it to `porting-checklist.md` in the project root,
     headed by the reference name+version, then the five dimensions; if
     planning comes next, hand that file to implementation-plan as an
     input. Do not commit it unless the user asks; in a git repo, exclude
     it locally:
     `n=porting-checklist.md; p="$(git rev-parse --git-path info/exclude 2>/dev/null)" && { mkdir -p "$(dirname "$p")" && { grep -qxF "$n" "$p" || echo "$n" >> "$p"; }; } 2>/dev/null || echo "note: could not exclude — leaving it untracked, never staging it"`
4. **Reimplement, don't transplant.** Port the behavior into the target
   stack following the project's existing conventions and idioms. Cite the
   reference file paths — with version or commit for remote references
   (e.g. `lodash@4.17.21 debounce.js`) — in your summary so claims are
   checkable.

## When source is not readable

- Website with minified JS: check for sourcemaps first (look for a
  sourceMappingURL directive at the file tail, then confirm the .map
  actually loads); otherwise use the minified code only to confirm
  structure, and find an open-source implementation of the same pattern
  to read for semantics.
- Closed-source SaaS or nothing readable: first look for a well-known
  open-source implementation of the same pattern and read that as the
  semantic reference. Only when none exists, tell the user you are
  downgrading to black-box observation (drive the UI/API, record behavior
  as a table of input → output/state; if the behavior sits behind a login,
  ask the user for access or a screen recording), and mark ported
  semantics as "observed, not read".
- Reference too large to read fully: find the file that owns the core
  behavior (search for the distinctive algorithm/state names first), read
  it plus its direct tests — budget roughly 3-5 files; follow at most one
  import hop when the behavior clearly spans modules, and name what you
  skipped as "assumed standard".

## Rules

- Never copy code verbatim from an external reference — port semantics and
  match the project's style. Check the reference's license first (LICENSE
  file, package.json, or `npm view <pkg> license`): permissive
  (MIT/Apache/BSD) is fine to port from with attribution in your summary.
  For GPL/AGPL, warn that reading the source then reimplementing risks a
  derivative work; if the user proceeds, extract semantics into the taking
  list first, implement only from the list without re-opening the source,
  and say so in the summary. For no license, warn that the default is
  all-rights-reserved and prefer a permissive alternative; black-box
  observation is the license-safe fallback.
- If the reference's behavior conflicts with something the user stated,
  surface the conflict instead of silently picking one.
- If the reference turns out to be a poor fit, say so and propose another.
