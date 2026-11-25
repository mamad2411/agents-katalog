---
name: aprimo-references
description: Write, fix, and verify Aprimo reference expressions (an XML DSL that runs against a digital-asset-management record). Use whenever the user asks to create, debug, explain, or convert an Aprimo reference, or mentions ref: tags, fieldName, onVariable, datetimeeval, switch/catch/foreach refs, or "DAM reference" logic. Bundles the actual compiler for verification plus the full tag documentation.
---

# Aprimo References

Aprimo references are a small XML DSL (`<ref:...>` tags) that executes against a digital-asset
record to produce a string. This skill lets you write them **correctly** by verifying every
reference against the real compiler instead of relying on memory — the same way you'd write code
against a linter and test runner. You do not need to have Aprimo memorized; you need to **check
your work**.

A reference computes a **value**; it doesn't *act* on its own. Goals like expiring assets on a
date, e-mailing an owner before expiry, firing an HTTP call, or keeping a field in sync run inside
DAM **fields** and **rules** (triggers, conditions, scheduled nightly checks) — with references
plugged into the field defaults and rule actions. So when a "write me a reference to do X" request
is really "how do I accomplish X," recognize it: tell the user which fields/rule they need, then
write and verify the reference parts. See [`reference/automation-patterns.md`](reference/automation-patterns.md).

## The non-negotiable workflow

Never hand the user a reference you have not run through the compiler. Always:

1. **Understand the requirement.** Identify the fields read, the conditions, the branches, and the
   exact output text.
2. **Check the docs for any tag you're unsure about** (`docs/`). One file per tag, e.g.
   `docs/compare.md`, `docs/datetimeeval.md`, `docs/switch.md`.
   The docs are ground truth for attributes and behavior — read them, don't guess.
3. **Write the reference**, following the rules in `reference/catalog.md` and
   `reference/operators-and-logic.md`.
4. **Lint it** (`-mode lint`). Fix every error. The error message names the problem precisely
   (e.g. invalid operator → it lists the valid set; unknown attribute → it lists the valid ones).
5. **Execute it** (`-mode execute`) against a context that exercises the logic, and confirm the
   output is what the requirement asks for. Run it on a few different inputs to check each branch.
6. **Iterate** until it lints clean AND behaves correctly, then deliver it. If you needed several
   tries, the user only sees the final, verified reference — be terse unless they ask why.

Reading a transpiler error and fixing it is normal and expected. A first draft that fails lint is
fine; an unverified reference handed to the user is not.

## Verifying — the compiler

The compiler is bundled in `bin/`. Use the binary for the OS you are running on wherever the
examples below say `transpiler.exe`: `bin/transpiler.exe` on Windows, `bin/transpiler` on macOS,
`bin/transpiler-linux` on Linux — including Claude's own sandbox on claude.ai, which is Linux.
Input is the bare reference XML on **stdin**. Full details + examples in `reference/compiler.md`.

`execute` is a **simulation** of the platform's evaluator, not a call to Aprimo: it resolves
classifications, settings, users and fields from the context you pass, so mirror the real data
(and the blank-field cases) into `-context-json` before trusting a result.

```bash
# 1. LINT — is it valid?  -> {"valid":true,"warnings":[]}  or errors with exact remedies
echo '<ref:record fieldName="Title" out="value" store="@title"/><ref:text out="@title"/>' | bin/transpiler.exe -mode lint

# 2. EXECUTE — what does it actually output?  (default context, or pass your own)
echo '<ref:text out="Hello"/>' | bin/transpiler.exe -mode execute
echo '<ref:record fieldName="Status" out="value" store="@status"/><ref:text out="@status"/>' \
  | bin/transpiler.exe -mode execute -context-json '{"records":[{"fields":{"Status":"Approved"}}]}'

# 3. ANALYZE — structural report (depth, branches, loops) when debugging nesting
echo '<ref:foreach in="@items" storeitem="@item"><ref:text out="@item"/></ref:foreach>' | bin/transpiler.exe -mode analyze
```

To exercise branches, pass different `-context-json` values (vary `records[0].fields.*` and record
attributes like `status`, `createdOnUTC`). `bin/default_context.json` shows the full context shape;
`-mode dump-context` prints the live default.

**List/typed fields aren't plain strings in the context.** An Option List is a structured
`{value, valuename}`, a Classification/User/Record List is an id plus a sibling lookup table, a
Text List is an array — and each field's type goes in `fieldMetadata`. Don't guess the format:
copy it from `bin/default_context.json` (it has one of every type) — see `docs/field.md`
(*Representing fields in the execution context*).

## The rules that matter most

These are where references most often go wrong (read `reference/operators-and-logic.md` for detail):

- **Read a field into a variable before you use it.** `<ref:record fieldName="X" out="value"
  store="@xv"/>` first, then reference `@xv`. Using `@xv` before a `store="@xv"` defines it is the #1
  error ("used before defined").
- **List fields read back ids, not text - and a list stays a list.** `out="value"` on an Option
  List, Classification List, User List or Record List returns the selected object's **id(s)** as a
  collection, **even when one item is selected**: `switch keys=` on it throws and `compare` never
  matches. For the readable **name** use `out="tostring"` (Classification List → classification
  name, User List → user name, Option List → option name; `out="valuename"` is Option List only
  and throws elsewhere). For the **path** or any other property do the two-step read
  (`<ref:record fieldName="X" out="value" store="@id"/>` then `<ref:classification id="@id"
  out="namePath"/>`). A Record Link rejects both `value` and `tostring` - use
  `valuechildren`/`valueparents`/`valuelinks`. Declare the field's `dataType` in the context's
  `fieldMetadata` and the compiler warns on both mistakes. See `docs/field.md`.
- **Namepaths start with a slash.** `out="namePath"` returns `/Security/Published/Restricted`;
  a `namepath = '...'` search accepts the path with or without the slash. Write search values in
  **single quotes** inside the attribute (`&quot;` breaks on paste). A search that matches nothing
  or several items **throws** - see `docs/classification.md`.
- **Empty inputs throw.** `ref:classification id=""`/`id="@blank"`, `ref:datetimeeval in="@blank"`,
  and `switch keys=` on a null all throw; gate lookups with `IsNotEmpty` and use the default-value
  template in `reference/patterns.md` (gate each lookup + one outer `ref:catch`) for defaults that
  read classification or date fields.
- **Variable names need 2+ characters.** A name is `@` + a letter then letters/digits — **at least
  two characters**, no underscores (`@s` and `@a_b` are invalid; use `@status`, `@aVal`). The
  compiler hard-errors on an invalid `store=`, `storeitem=`, or `counter=` name, and a stray `@x`
  read is treated as literal text, not a variable.
- **`compare` operators are a closed set (verified):** `equal/eq/==`, `notEqual/ne/!=`,
  `greaterThan/gt`, `greaterThanOrEquals/ge`, `lessThan/lt`, `lessThanOrEquals/le`. The only symbol
  forms are `==`/`!=` (no `>`/`<`/`>=`/`<=`); it's `ge`/`le`, not `gte`/`lte`. There is **no
  `contains`, `startsWith`, `in`, `matches`, `between`** — use `ref:regex` for substring, and
  compare-per-candidate + OR (or `switch`) for membership.
- **There are no `ref:if`, `ref:and`, `ref:or`, `ref:else` tags.** Branch with `ref:switch`
  (multi-way) or `onVariable`-gated `ref:text`/`ref:object` (single condition). Combine *truth*
  conditions by **nesting `IsNotZero` gates** (AND) or a gated emit + nested `IsZero` fallback (OR);
  `onAllVariables`/`onAnyVariable` only check whether the variables are **defined** (a `compare`
  result is always defined), so they're for "was this variable ever set", not boolean AND/OR.
- **Date math is `ref:datetimeeval`** (`addYears`, `addMonths`, `addDays`, ...), never literal
  text like `now+5`.
- **`store` suppresses emission.** A ref with `store="@xv"` captures its value but prints nothing —
  only an *ungated* `ref:text` emits. So you can read fields and run compares freely; only your
  final `text` shows. `compare` yields `True`/`False` (not numbers), so combine conditions with
  **gates**: AND = nested `IsNotZero` gates, OR = a gated emit plus a nested `IsZero` fallback;
  `eval` is for numeric math only and **errors** on `True`/`False`.
- **To turn programming intent into refs, use the construct map.** `if/else`, `switch`, `for-each`,
  AND/OR/NOT, `try/catch`, counters, date math each have a fixed idiom in
  `reference/computational-model.md`. Note the constructs with **no** idiom: no `while`/unbounded
  loop (a `foreach` count is fixed by its input), recursion only via `result="ref"` capped at 3, and
  variables are **one flat set** - there is no block scope, so a `store` inside a
  `foreach`/`switch`/`object`/`catch` **is** readable afterwards. It is missing only when the
  storing element never ran (its gate was false or it threw). A switch is the exception: running
  it resets every variable stored in any of its branches to null, so an untaken branch's variable
  reads empty - and a value preset before the switch is wiped. Put fallbacks in `<default>`.
- **Externalize config into a setting instead of hardcoding.** Aprimo supports custom setting
  definitions (text/number/xml/reference/…); read any with `ref:setting name="X"`. When a rule
  would carry a big list, a mapping table, environment-specific URLs, or tunable thresholds, prefer
  a setting the reference reads over baking it into the XML. See `docs/setting.md`.
- **Don't invent tags or attributes.** If the compiler rejects one, it tells you the valid options —
  use them. The full valid set is in `reference/catalog.md`.

For worked, compiler-verified recipes (compound boolean rules, crash-safety with `catch`,
conditional defaults, trimming before numeric compares, date logic), see `reference/patterns.md`.

## How to behave on a request

- **Start from the user's reference.** When given a working reference and asked "is something
  wrong with this?" or for one change, return a list of issues and the **minimal edit** - keep
  their variable names, tags, structure and formatting. Do not rewrite it, rename variables, swap
  `switch` for gates, or add `ref:catch` blocks that were not asked for.
- **Confirm the field type and cardinality before writing** - a Classification List or an Option
  List, single-select or multi-select - or state the assumption in one line up front. A
  single-select field does not need a `foreach`; a multi-select one does.
- **Use only values the user supplied.** Build classification paths, option names and keys from
  the exact strings given; never invent a mapping (a guessed `No Restriction` with a space caused a
  production lookup failure). When a term is ambiguous ("Draft" - the `Status` field's value, or the
  record's workflow status?) ask, or state which one you took.
- **Settings and groups:** never guess a setting name - keys differ per tenant and change over
  time, so ask the user for the exact key (there is no `.damUrl`; use
  `ref:application out="damUrl"`). References cannot list a user group's members - propose a distribution-list setting or a
  User List field (`docs/usergroup.md`).
- **Field configuration is part of the answer** when a default "never fires": the Reset-to-Default
  trigger must be **On New Field** (**None never fires**), and a default that reads another field
  needs a **higher Sort Index** than that field (`reference/field-configuration.md`).
- **A `ref:catch` around the whole reference is a template for field defaults only** - say when
  you add one, and never put one around an e-mail `<recipients>` slot.

## Reference material in this skill

- `reference/computational-model.md` — **construct map**: a copyable table translating ordinary
  programming intent (assign, if/else, switch, for-each, AND/OR/NOT, try/catch, recursion, date
  math) into the exact reference idiom, plus data types and the constructs that have no idiom
  (no `while`, recursion capped at 3, block-local vars). Start here to turn intent into refs.
- `docs/overview.md` — **concepts that span every tag**: syntax basics, variables and scope, gating,
  the shared attribute pipeline (`onEmpty` -> `format` -> `left`/`right` -> `encode` -> `case`),
  whitespace rules, and **[Missing values are null](docs/overview.md#missing-values-are-null)** -
  which tags throw on an absent field and how to guard them. Not a per-tag page, so it is easy to
  miss; read it before writing anything non-trivial.
- `reference/catalog.md` — every valid `ref:` tag, what it does, container-vs-leaf, key attributes.
- `reference/dynamic-references.md` — **advanced**: emitting literal HTML (entity-encoding, the
  `@`-sigil/`@import` collision) and building references as text to re-resolve with `result="ref"`
  (dynamic refs, and the geometric-unroll loop for when you need bounded iteration but have no
  collection to `foreach`). Fiddly multi-level escaping — use only when needed, and verify.
- `reference/operators-and-logic.md` — comparisons, AND/OR, gating, branching, variable flow, date math.
- `reference/patterns.md` — proven, compiler-verified recipes for common rule shapes.
- `reference/automation-patterns.md` — **when one reference isn't enough**: how references sit inside
  DAM fields and rules (field defaults, Set-field-value / Execute-reference / Send-email actions,
  Reference-match conditions) and the fields + scheduled-rule recipes for goals like expiration,
  reminders, and HTTP side-effects. Read this when the ask is really "how do I accomplish X."
- `reference/field-configuration.md` — **the field side of automation**: field types, default-value
  recompute triggers, scope, storage/searchability, Record-Link traversal + Metadata Inheritance, and
  what rules can set vs. read. Read this when a goal hinges on how a field is *configured* (why a
  default goes stale, why a scheduled rule never matches, how to reach a related record's value).
- `reference/debugging.md` — the loop for when a reference is wrong/blank/erroring, with a
  symptom → cause → fix table.
- `reference/compiler.md` — full compiler CLI: every mode, flags, output formats, how to read errors.
- `docs/` — the complete per-tag Aprimo documentation (one `.md` per tag), ground truth for every tag.
  The tag catalog in `reference/catalog.md` is the full set the platform accepts (including
  `ref:application`, `ref:record out="title"` and raw HTML inside containers).
