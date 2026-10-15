---
name: review-ocaml
description: "Two-phase review of an OCaml project. Use when the user asks to review an OCaml codebase, audit its module interfaces, restructure or redocument .mli files, or hunt for redundancy, dead code and optimisation opportunities across implementations. Phase one reads only dune and .mli files to judge the public interfaces; phase two dispatches a subagent per module to review the implementation."
---

# OCaml Project Review

A review in two phases. The interfaces are judged first, on their own, as a
user of the library sees them. Only then are the implementations read, one
module at a time, by a dedicated subagent each.

Never merge the phases. Reading an implementation before judging its interface
is how a bad interface gets rationalised.

## Phase 1: Interfaces

### What to read

Read **only** these files.

- `dune-project`
- every `dune`
- every `.mli`
- every `.mld`
- `*.opam` if present

Do **not** open a `.ml` in this phase. A module with no `.mli` is itself a
finding. Note the module, record what `dune` says about it, and move on.

### Build the map

From the `dune` files alone, record:

- Every library and executable, its `public_name`, and its `libraries`.
- Which modules are `(modules ...)` of which stanza, and which are private.
- Whether libraries are `wrapped` and what the wrapper module re-exports.
- `(flags ...)`, disabled warnings, `preprocess` stanzas.
- Dependency direction between the project's own libraries, and any cycle
  pressure or layering violation.

State the map back as a short dependency listing before reviewing anything.

### Judge each interface

For every `.mli`, check the following.

**Shape**
- Does the module do one thing? A module that would need two synopsis
  sentences is two modules.
- Is there a central `type t`, and is it abstract? Exposed records that carry
  invariants are a finding.
- Are the values ordered sensibly, with constructors first, then accessors,
  then predicates and comparisons, then converters and printers?
- Are `pp`, `equal` and `compare` present where the type warrants them?
- Are the generic names gone? `Util`, `Helpers`, `Common` and `Misc` are
  findings.

**API quality**
- Unlabelled booleans and unlabelled same-typed adjacent arguments.
- `find_*` returning `option` and `get_*` returning a value directly, or the
  convention broken.
- Error handling. Recoverable failure is a `result`. An exception in a public
  signature must be documented and justified.
- Values exported only because a test or a sibling module needs them. These
  belong behind a private module or an `_intf` split.
- Leaked internals. Types from a dependency in the signature that the caller
  should not have to depend on.

**Documentation**
- Judge every doc comment against the `doc-style` skill. That skill is the
  standard, so load it before reviewing prose.
- Missing synopsis, missing value docs, `[f x y] is` violations, colons and
  em dashes, prose about implementation, banned words.

### Deliverable

Produce an interface report with, in order:

1. The library and module map.
2. Findings, grouped by module, each as `file:line` plus one sentence.
3. A restructuring plan, if one is warranted. Say which modules split, merge,
   move library, or gain an `.mli`, and what the API break costs.
4. A redocumentation plan, if one is warranted. List the files whose
   documentation is to be rewritten under `doc-style`.

Present this and **stop**. Restructuring is the user's call. Do not edit an
interface, and do not start Phase 2, until the user has responded.

## Phase 2: Implementations

Once the user has accepted or amended the plan, review the implementations.

### Dispatch

One subagent per implementation module. Group only trivially small modules,
never more than three per subagent, and never modules from different
libraries.

Launch subagents in parallel, in a single message, up to six at a time. Wait
for a batch to return before launching the next.

Give each subagent the module's `.ml`, its `.mli`, and the Phase 1 findings
for that module. Use this prompt. The comment rules are spelled out in it
rather than delegated, because a subagent may not have this plugin's skills
available.

```
Review the implementation of <module> in <path>.ml against its interface in
<path>.mli. Read both files in full, plus any module it calls that you need
in order to judge a finding.

Report only defects you can point at. For each one give file:line, one
sentence of what is wrong, and one sentence of evidence. Do not edit any
file. Do not report style preferences that ocamlformat settles.

Look for, in this order:

1. Logic errors. Wrong base case, off-by-one, a partial match that will
   raise, an ignored result, an error path that loses information, a
   comparison that disagrees with equal, integer overflow, resource leaked on
   an exception path.
2. Dead code. Values never used inside the module and not in the .mli.
   Unreachable branches. Parameters never consulted. Types with no inhabitant
   constructed. Say for each whether it is safe to delete.
3. Redundancy. Two functions that compute the same thing. A hand-written loop
   that is a Stdlib or List function. A reimplementation of something already
   in this project's own libraries, which you should check for by name.
4. Optimisation. Quadratic behaviour on a path that takes user-sized input.
   Repeated work that could be hoisted. String concatenation in a loop where
   a Buffer belongs. An avoidable allocation on a hot path. Say what input
   size makes it matter, and skip it if none does.
5. Comments. Any comment inside the implementation that the code already
   says, which is to be deleted. Section banners and commented-out code, also
   deleted. Any doc comment in the .ml when an .mli exists, since the
   documentation belongs in the interface. A comment survives only if it
   cites a spec, states an invariant a reader cannot check locally, explains
   a deliberate workaround, or justifies an unsafe operation.
6. Interface drift. Behaviour that contradicts what the .mli documents.

Rank your findings by severity, most severe first. If a category is clean,
say so in one line rather than inventing a finding.
```

### Aggregate

When every batch has returned:

- Drop duplicates and anything a subagent could not support with evidence.
- Add the cross-module findings no single subagent could see. The same helper
  written in three modules. A layering violation. A type converted back and
  forth across a boundary.
- Rank everything by severity. Correctness first, then dead code, then
  redundancy, then optimisation, then comments.
- Present the ranked list with `file:line`. Apply fixes only when the user
  asks, and apply them in that order.

## Rules

- Phase 1 reads no `.ml`. Phase 2 starts only after the user responds.
- Every finding cites `file:line`.
- Subagents review and report. They never edit.
- An optimisation finding without a stated input size is noise. Drop it.
- Do not report anything `ocamlformat` or `dune fmt` already handles.
- Warnings that a `dune` stanza disables are findings in themselves.
- A proposed change that breaks the public API is labelled as such, with the
  callers it affects.
