---
name: write-luau-code
description: "Luau code style and idioms for flipbook-labs: type discipline, table formatting, naming, stdlib-first idioms, enums, error shape, module organization, and when not to abstract. Use when: writing or editing any Luau source in a flipbook-labs repo (library, plugin, CLI, or a .lute/ script), or reviewing a diff for style. This is the vendor-neutral house style; a repo's own skill owns its framework idioms and exemplars."
type: process
---

# Write Luau Code

The house style for Luau you write or edit anywhere in the org. These are the corrections Marin makes most often in review, collected so you make the change before being asked. Match the surrounding file when it already establishes a local convention. This skill owns _how the code reads_, not what it does or whether it is tested (see the cross-links at the end).

## Types

- **Prefer `unknown` over `any`.** Reach for `unknown` by default at boundaries (untrusted input, cross-module generics). `any` disables the checker and needs an explicit reason. Marin: _"Use `unknown` before `any`. Explicit approval is needed for using `any`."_
- **Type the public contract.** Give function signatures and exported data structures explicit types rather than leaning on inference. A missing type is a review comment waiting to happen.
- **Name a reusable type instead of repeating an inline union.** `export type BumpKind = "major" | "minor" | "patch"` once, then annotate with it (`local kind: BumpKind = ...`), rather than writing the union at each site.
- **Keep generics sound for every instantiation.** Do not assume a generic `T` has a property just because it is not some other type. Marin: _"we can't assume that any generic value `T` will be a StoryControlValue only because it's not a StoryControl."_
- **Name the arguments in function types.** Write `getStoryModuleRecords: (storyModule: ModuleScript) -> StoryModuleRecord?`, not `getStoryModuleRecords: (ModuleScript) -> StoryModuleRecord?`. The names carry meaning a bare type list loses, so the type reads as a signature.

## Table formatting

**Expand tables by default, one field per line.** Only a trivial one- or two-field table belongs on a single line. Wide inline tables hurt readability and produce noisy diffs. This one recurs constantly in review, so do it up front: multi-key tables and multi-key `return` statements each get a line per entry.

## Naming

- **Functions read as verb phrases; variables as nouns.** A function that reads or computes state is named with a verb prefix: `getRepoSlug`, `fetchManifest`, `resolvePath`, `hasUnreleasedChanges`. Do not name a function the way you would name the value it returns (`manifest` for a getter).
- **Booleans take an `is`/`has` prefix:** `isActive`, `hasChanges`, not `active` or `changed`.
- **Pick one term for a concept and apply it everywhere.** When you rename, sweep the whole change so the vocabulary stays consistent across modules. Consistency beats a marginally better name used in only one place.
- **Do not pluralize gratuitously**, and prefer a descriptive name over a generic one (`entry`, `data`, `value`) wherever the specific meaning is not obvious from context.

## Idioms: reach for the standard library first

- **Use stdlib utilities instead of hand-rolling.** `string.split`, `path.join`, `fs.readFileToString`, `fs.writeStringToFile` exist so you do not open/read/close by hand or reinvent a path join. In a `.lute/` script, parse arguments with the CLI battery, not by pulling apart `...`.
- **Trust the language and stdlib to throw.** Drop redundant `assert()` around a call that already errors on failure (file reads, a parser with a required argument), and drop casts the language already implies. Marin: _"Error is implicit for file reading, remove the asserts."_
- **Colon notation for methods:** `content:gsub(pattern, next)`, `message:find("409 ", 1, true)`, not the `string.` free-function form.
- **Backtick strings call `tostring` for you:** write `` `got {value}` ``, not `` `got {tostring(value)}` ``.
- **Index directly rather than binding an eager intermediate** you use once (`request.method`), but _do_ introduce a local to capture a multiple-return value rather than wrapping the call in parentheses to discard the rest.
- **Alias a hot import once at the top of the file** (`local run = FlipbookBatteries.run`) and use the alias throughout instead of re-indexing it at every call site.
- **Order requires: packages first, then local modules.** Keep third-party imports (`@std`, `@pkg`, batteries) grouped as the vendor block, local modules after. Put all requires at the top; a mid-file require is only for a deliberate dynamic-loading case.

## Enums

Model a closed set of values as a frozen table of named constants, not a bare string-union type:

```luau
local Surface = table.freeze({
	Agent = "agent",
	Plugin = "plugin",
})
```

Callers then reference `Surface.Agent`, which is greppable and typo-proof, instead of repeating the raw string. Follow the pattern already used elsewhere in the org rather than inventing a new enum shape.

## Errors

Name an error field `err` or `problem`, not `error` (which shadows the global and reads as generic). Keep error handling light: let a clear base error surface rather than wrapping it in bespoke handling. Marin: _"The base error is pretty clear, and if anyone ever hits this they'll either find the escape hatch themselves or ask about it."_

## Module organization

- **One responsibility per module, and that is usually one function.** A module earns its own file by carrying a single job, not by collecting several jobs that share a topic. Two functions living together because they are both "about the publish lock" is still a bundle, so split them. The tell is a module named for a theme (`statusHelpers`, `lockUtils`) that exports a handful of functions. Topical relatedness is not a license to bundle: it is what a _folder_ is for, one function per file inside it.
- **Fold a trivial, single-use helper into its caller.** A helper that is a couple of lines and called from one place has not earned a module or even an export. Inline it where it runs. When a themed module has only one function worth reusing, keep that one as the module and fold the rest back into their call sites rather than keeping them company.
- **Extract an inline helper into its own module** once it is reused or non-trivial, instead of leaving it defined in the middle of an unrelated file.
- **Hoist shared types to a `types.luau`** rather than re-declaring them across the files that use them.

## Do not abstract ahead of need

- **Build the direct thing until it actually fails.** Do not add a cross-platform wrapper, a config knob, or an indirection for a problem you have only imagined. Marin: _"Did spawning a `cp` process actually fail or were you overeager to create this? We'll use `cp` until we actually hit an issue."_
- **Do not add validation the system already guarantees elsewhere.** A downgrade guard is redundant when the PR review is the real gate; a required CLI argument does not need a runtime nil-check on top of the parser.
- **Reuse the org's battle-tested logic** before writing your own for a solved problem (path resolution, type narrowing). Check Flipbook and sibling repos first.

## When not to use

This skill is code style only. For whether a test is any good, see [`org/write-luau-tests`](../write-luau-tests/SKILL.md). For when a comment earns its place, see [`org/code-comments`](../code-comments/SKILL.md). For repo setup, `.luaurc` strictness, and the `@std`-over-`@lute` policy, see [`org/repo-conventions`](../repo-conventions/SKILL.md). For deciding a change is too large or exposes too much, see [`org/reviewable-changes`](../reviewable-changes/SKILL.md).

---

## Provenance and Maintenance

**Date stamped:** 2026-07-07. Distilled from Marin's inline review comments across storyteller, agent-gateway, changewrite, flipbook, and flipbook-cli, where the same Luau-style corrections recur (type discipline, expanded tables, verb-and-`is` naming, colon notation, stdlib-first, frozen-table enums, one-thing-per-module, no premature abstraction). Quotes are frozen illustrations, not live pointers into any repo's source. Updated 2026-07-09: the module-organization section was sharpened after a changewrite review where a themed module bundled several related pure helpers and the earlier "unrelated exports" wording read as permission, so it now says relatedness is not a license to bundle and a trivial single-use helper folds into its caller. Updated 2026-07-20: the function-type rule was reversed after a Storyteller review asked for parameter names in function types and to apply that generally across the PR's type changes. Earlier versions of this skill said the opposite.

**Re-verify these claims when this skill next loads:** nothing mechanical. This is `org/` doctrine with no single-repo anchors. The quotes above are frozen snapshots quoted for illustration. If the org's Luau conventions shift (a new formatter changes table style, a stdlib rename), update the relevant section and add a `.changes/` entry.
