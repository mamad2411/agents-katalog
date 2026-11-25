---
name: specforge-authoring
description: "Orchestrator for writing .spec files that the SpecForge compiler turns into a typed, validated graph -- for any domain the project's extensions declare (software specs, product plans, marketing, pharma/GxP procedures, operations). Checks first which extensions the project loads and which entity kinds they declare, writes only those kinds, prefers typed edits (specforge new/set/link), and delegates to the per-kind child skills when a builtin extension is loaded. Use when writing new .spec files, adding or changing entities, auditing .spec completeness, or converting Markdown, spreadsheets or documents into .spec."
---

# SpecForge Authoring (Orchestrator)

SpecForge is a domain-free engine. Its grammar knows five structural keywords and nothing else:

| Keyword | What it is |
|---------|-----------|
| `spec` | the project's root entity (configures nothing: configuration is `specforge.json`) |
| `ref` | a typed link to an outside resource (`ref gh.issue:42 "..."`) |
| `use` | an import of another `.spec` file (optional: references resolve project-wide) |
| `define` | reserved; registers nothing (W143) |
| `defaults` | file-level default values for one kind's fields |

**Every other kind** -- `behavior`, `feature`, `persona`, `decision`, a GSD `phase`, a pharma `procedure` -- exists only
because an extension the project loads declares it, with its fields, edges, rules and commands. The builtin
extensions (`@specforge/software`, `product`, `governance`, `formal`, `testing`, ...) are a starter set, not the base.

## Step 1: find out what this project can say

Never assume a kind exists. Before writing anything:

```bash
specforge extensions                 # which extensions are enabled and loaded
specforge infer-guide                # every declared kind, its extension and its fields (* = required)
specforge infer-guide <kind>         # one kind: each field's type and enum values, a guide and an example
specforge schema --kind <kind>       # the exact fields and edge types, as JSON (a field may be computed, harness, immutable or append_only: never write a computed or harness value by hand)
specforge model --fields all         # every kind and relationship, grouped by extension
```

Over MCP the same answers come from `specforge.extensions`, `specforge.schema` and `specforge.model`.

Then:

- **Write only kinds those extensions declare.** An unknown kind is E024; an undeclared field is W020.
- **Use each field the way it is declared** -- required fields (E006), enum values (E061), the target kind of a
  reference (E022), the verify kinds a kind allows (W009) or whether it takes `verify` at all (W158).
- **A custom domain follows its own extension.** If the project loads `@acme/clinical` or `@gsd/core`, its
  declarations are the reference: the child skills below describe the builtins only and do not apply to it.
- **A kind the project needs but no extension declares** is not something to improvise in `.spec`: add the extension
  that declares it (`specforge add <name>`), or write one (`specforge extension init`, then `build`, `validate`).

## Step 2: write through typed edits

Prefer the typed edits to hand-written text. They write each value in the form its field declares, lay the block out
canonically, and refuse (E080) an edit that would leave the project with an error it does not have now:

```bash
specforge new behavior archive_task "Archive a Task" --in spec/behaviors/task.spec --contract "…" --types Task --category command
specforge set archive_task category query          # specforge set <id> --title "…" changes the title
specforge link archive_task invariants task_id_uniqueness    # unlink removes; unset removes a field
specforge link archive_task --verify unit:"archiving an unknown task fails"
specforge delete archive_task --unlink-references
```

A write is checked against the file as you last read it. `specforge set/unset/link/unlink/delete/new` take `--revision <sha256:..|absent>` (MCP: a `revision` on each edit; `specforge.inspect` returns an entity's `file` and `revision`), and when the file has changed since, the write is refused `stale_revision` and nothing is written: read the entity again, then retry. A kind or field declared `writer: human` is refused `human_only` to an agent: tell the person instead of working around it.

A member of a typed block or block list is addressed by its path: `specforge set <id> 'requires[0].phase' 03`, `specforge unset <id> completion.audit`; a whole block list is JSON (`specforge set <id> requires '[{"phase":"02","provides":"x"}]'`), and the MCP `specforge.edit` tool adds an item with `append` and drops one with `remove` (a list of words changes by `link`/`unlink`).

`--in` is relative to the project root and must be inside the spec root. `specforge new <kind> --help` lists that
kind's field flags, read from the loaded extensions -- so the same commands work for any domain's kinds.

Over MCP, `specforge.edit` takes a list of edits (`create`, `set`, `unset`, `retitle`, `link`, `unlink`, `add_verify`,
`remove_verify`, `delete`) applied all or nothing, so an entity and the link to it go in one call. Add `--dry-run`
(`dry_run: true`) to see the diff first. A union type takes only `set --title` and `delete`, and ports with `method`
lines are not covered by typed edits yet: write those by hand, then run `specforge check`.

A `verdict <rule> <outcome> { ... }` member of a block is a judged rule's record: never write one by hand (E083),
and never write a field a verdict sets (E082). Read what the judge reads with `specforge query <id> --inputs <rule>`
(MCP `specforge.verdict_inputs`); a verdict goes stale when an input changes ([judged rules](../../../docs/guides/judged-rules.md)).

## Step 3: check

```bash
specforge check                      # parse, resolve, validate; exit code 1 on errors
specforge check --strict             # warnings count as errors
specforge explain <code>             # what a diagnostic means and how to fix it
```

When `@specforge/checks` is loaded, a field's values can be held to a standard too: the field's `checks`, or
`specforge.json`'s `checks.fields` for a field you do not declare, attaches a checker such as `json`, `pointer`,
`markdown_anchor`, `image` or `package`
(`"checks": {"fields": {"feature.refs": [{"checker": "@specforge/checks:pointer"}]}}`). A check that needs the network
asks for approval first (W170); one not performed is not an error. The checkers, their arguments and codes are in
[the inventory](../../../docs/extension-inventory.md).

## Builtin kinds: delegation table

Use a child skill only when `specforge extensions` lists its extension.

| Kind | Child skill | Declared by |
|------|-------------|-------------|
| `spec` | **specforge-spec-block** | core (structural) |
| `ref` | **specforge-refs-dsl** | core (structural) |
| `behavior` | **specforge-behaviors-dsl** | `@specforge/software` |
| `invariant` | **specforge-invariants-dsl** | `@specforge/governance` |
| `event` | **specforge-events-dsl** | `@specforge/software` |
| `type` | **specforge-types-dsl** | `@specforge/software` |
| `port` | **specforge-ports-dsl** | `@specforge/software` |
| `feature` | **specforge-features-dsl** | `@specforge/product` |
| `journey` (+ `persona`, `channel`) | **specforge-journeys-dsl** | `@specforge/product` |
| `deliverable` | **specforge-deliverables-dsl** | `@specforge/product` |
| `milestone` | **specforge-milestones-dsl** | `@specforge/product` |
| `module` | **specforge-modules-dsl** | `@specforge/product` |
| `term` | **specforge-terms-dsl** | `@specforge/product` |
| `decision` | **specforge-decisions-dsl** | `@specforge/governance` |
| `constraint` | **specforge-constraints-dsl** | `@specforge/governance` |
| `failure_mode` | **specforge-failure-modes-dsl** | `@specforge/governance` |

`@specforge/product` also declares `release`; `@specforge/formal` declares `property`, `axiom`, `protocol`,
`refinement`, `process` and adds `requires`/`ensures`/`maintains`/`abstract`/`refines` to behaviors;
`@specforge/testing` decides which kinds take `verify` and with which kinds. No child skill covers those: read
`specforge infer-guide <kind>`.

## The structural syntax (same in every domain)

### A block

```spec
feature order_tracking "Order Tracking" {
  status   accepted
  priority high
  problem  "Customers cannot see where their order is."
  acceptance [
    "The order page shows the current carrier status",
    "A status change is visible within 5 minutes",
  ]
}
```

`<kind> <id> "<title>" { <field> <value> ... }`.

- **ID** -- words of letters, digits and underscores joined by single `-` or `.` (`AUTH-01`, `v1.0`), 2-60 characters (E014), unique within its scope and kind (E002; a name is also W060 against another kind in its scope) and best unique
  across kinds (W060). A kind keyword or structural keyword cannot be an ID (E013).
- **Title** -- required (E076). `specforge migrate` adds one to blocks that lack it.
- **One field, one line** -- a block writes each field once (E081): give a list all its items in one `[...]`.

### Value forms (W159 when a value is not written in its field's form)

| Field type | Written as |
|------------|-----------|
| string | `"quoted"`, or `"""triple-quoted"""` for several lines |
| enum, identifier | bare word: `status accepted` |
| reference | bare ID: `persona patient` |
| reference list | `[a, b]` |
| string list | `["one", "two"]` |
| date | bare day: `target_date 2026-06-30` |
| integer / bool | `42` / `true` |

### References

A reference names an entity by ID and resolves across the whole project -- no import needed. A name that does not
exist is E003; one that names the wrong kind is E022. Each relation is written on one side only: the field its
extension declares (writing the other side is E079). `[some_id]` inside prose is text for readers, not an edge.

### `use` imports (optional)

```spec
use "types/user"                            // records that this file builds on types/user.spec
use { User, UserRole } from "types/user"    // the same, naming the entities it uses
```

The path is relative to the spec root, with forward slashes and no `.spec` extension. An import that names no source
is E025; a binding the target does not declare is W027; files importing each other is W113.

### File defaults

When every block of one kind in a file shares a value, state it once above the first block:

```spec
defaults behavior {
  features [task_management]
}

behavior archive_task "Archive a Task" {
  category command
  contract "Archiving moves a task out of the active list."
}
```

Every behavior in the file now has `features [task_management]`; a block that writes its own `features` replaces it
whole (`features []` means none). A default sets a field the kind declares (E077), once per kind (E078); a block
restating it is W161. `specforge migrate` hoists the repeats of an existing file.

## File organization

The compiler reads every `.spec` file under `spec_root`; the layout is a convention. Group by what the domain
naturally groups by -- one file per area (`orders.spec`, `billing.spec`), or one directory per kind once a project
passes ~20 entities. Example for a project loading `@specforge/software` and `@specforge/product`:

```
specforge.json           # configuration: extensions, spec_root, settings (typed, per extension) -- created by `specforge init`
spec/
  main.spec              # the spec block
  features/orders.spec
  behaviors/orders.spec
  types/order.spec
  product/personas.spec
```

## What NOT to Do

- Do not write a kind before checking that a loaded extension declares it
- Do not describe the builtin kinds as "SpecForge's entity types" -- they are what the builtin extensions declare
- Do not invent fields: an undeclared field is W020 and carries no meaning to any check
- Do not configure in the `spec` block -- configuration is `specforge.json`
- Do not hand-write traceability matrices or indexes -- `specforge trace` and `specforge export` generate them
- Do not include the `.spec` extension in `use` paths
