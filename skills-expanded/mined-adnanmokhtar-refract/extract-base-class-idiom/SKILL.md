---
name: extract-base-class-idiom
description: Walk a load-bearing unit — a base class, a composable/hook, a shared wrapper component, a shared service module, or a generic type primitive — plus its dependents, to extract the project-specific protocol, configuration surface, automatic behaviors, escape hatches, and pitfalls. Output is a pattern file authored in the project's own voice (citing real paths, real dependents, real anti-patterns) — NOT a generic template. Used by /setup-project Phase 2.5 + Phase 4.2a to author ai/patterns/<unit>.md from codebase reality instead of copying generic pack content.
kind: skill
pack: learning
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: extract-base-class-idiom

## Purpose

Generic pack templates produce generic output. This skill produces project-specific pattern files by reading the actual load-bearing unit + its dependents + their tests + their callers, then authoring the pattern in the project's voice.

The output should read like a senior engineer who has worked in this codebase for 6 months wrote it — citing real files, real dependents, real failure modes — not like a template that has had paths injected.

**What "load-bearing unit" means, and why this skill is not class-only.** The extraction shape here — read the unit in full, count its dependents, sample across the range, name what it does automatically, name how to escape it, find the pitfalls in git history — is not a property of inheritance. It is a property of *anything ≥3 things depend on*. Phase 2.5 detects five idiom patterns (`phase-2-profile.md § Idiom-pattern detection`) and every one of them yields units of exactly that shape. For a long time the spec dispatched three separate named skills for the non-class patterns; none of them ever shipped, so a composition-style frontend — Vue 3, React hooks, any design-system wrapper library — *matched* a pattern and then hit an extractor that did not exist. That is undefined behaviour, not a defined degrade, and it silently emptied `_extracted-idioms.md § Wrappers` / `§ Composables`, which `templates/packs/ui-ux/_topics.md` and align's reinvented-wrapper detector both read. Three thin skills would have been worse than one that covers the shape properly: this one is parameterised by `unit_kind` instead.

## Premise

- Real source is the truth. Read the unit's file in full + every sampled dependent in full + every cited collaborator before authoring a single section.
- Every method, prop, option, hook, automatic behavior, escape hatch, and pitfall cites `<path:line>` from the actual unit — not from an assumed protocol. This holds identically for a composable's returned state and a wrapper's default-true props.
- Pitfalls cite a commit SHA, a line in `ai/failures/`, or an in-code `DON'T` / `HACK` comment — never "common mistakes" without evidence.
- Empty extraction is honest — omit the section per Step 7 instead of writing `_TBD_` or generic prose.
- Fabrication — citing a method that doesn't exist on the unit, a dependent count without a grep, a pitfall with no source — is the failure mode the per-section verifier rejects.

## Mechanical halt

- Hand-wave content — `use parameterized queries`, `follow framework conventions`, `your service layer`, generic `<EntityType>` placeholders, a pitfall without `<path:line>` or commit ref — REFUSE to write the section.
- Regenerate the section with concrete citations OR omit it (per Step 7's "no `_TBD_`" rule).
- If a unit genuinely has no automatic behaviors / no pitfalls / no escape hatches in code, record `<NOT-DETECTED: <reason>>` (e.g. `<NOT-DETECTED: thin wrapper, no overrideable hooks>`) and skip the section.
- Never synthesize a section to fill the 9-section template shape — the omission itself is the finding.

## When to use

- `/setup-project` Phase 2.5 — once per load-bearing unit with ≥3 dependents, for EVERY idiom pattern the project matched, with `unit_kind` set accordingly. A project can match several; run the skill per unit per pattern.
- `/setup-project` Phase 4.2a (AUTHOR mode) — generating `ai/patterns/<unit>.md`.
- On-demand by `/refresh-knowledge` Phase 3 step 4, which re-invokes this skill per load-bearing unit in the freshly-written oracle and rewrites `.claude/_extracted-idioms.md`.
- Manually when adding a new pattern doc for a unit that doesn't have one.

## Inputs

- `unit_path` — absolute path to the load-bearing unit's file. (`base_class_path` is accepted as the legacy spelling of this input and means the same thing.)
- `unit_kind` — one of `base-class` / `composable` / `wrapper` / `service` / `type-primitive`. Defaults to `base-class`. Selects the terminology table below; the procedure is otherwise identical.
- `topic_spec` (optional) — `_topics.md` entry for this pattern; lists required sections. If absent, use the default 9-section template below.
- `output_path` — where to write the pattern (e.g., `ai/patterns/data-access.md`).

**Terminology per `unit_kind`.** Substitute these into every step below. Nothing else changes — the same walk, the same ≥3-dependent threshold, the same denominator discipline, the same verifier:

| `unit_kind` | The unit is | A "dependent" is | Find dependents with | "Configuration surface" is | "Override hooks" are |
|---|---|---|---|---|---|
| `base-class` | a base / abstract class | an extender | `extends <Name>` / `(<Name>)` / `: <Name>` per language | overridable static / getter properties | protected methods |
| `composable` | a `use<X>`-style function or hook | a caller | import sites of the exported symbol | the options object / arguments it accepts | the callbacks it invokes and the reactive state it returns |
| `wrapper` | a shared component wrapping a primitive | a usage site | element / tag usage plus import sites | props with defaults (esp. default-true props) | slots / children / render props / emitted events |
| `service` | a shared service or utility module | an importer | import sites of the module | constructor / factory options, env-driven config | injectable collaborators, the strategy or transport it delegates to |
| `type-primitive` | a generic type, DTO or shared interface | an instantiation site | type-position usages of the symbol | type parameters and their constraints | the members an implementor must supply |

`unit_kind`-specific things worth naming that the class case has no equivalent for: for `composable`, call-context rules (must be called during setup/render, not inside a conditional or after an await) — these are the pitfalls that actually bite; for `wrapper`, WHICH raw primitive is wrapped and what the wrapper adds on top, because "the raw primitive used directly outside the wrapper" is the single most common drift and is what align's reinvented-wrapper detector needs named; for `service`, lifecycle (singleton vs per-request) and cache strategy; for `type-primitive`, the invariants the type encodes that the compiler does not enforce.

## Procedure

### Step 1 — Read the unit fully

Read the entire file. NEVER summarize without reading. Read the `base-class` list below as the canonical example; the § Inputs terminology table gives the equivalent for the other four kinds, and the last three bullets are kind-independent. Note:
- The unit's signature + generic type parameters / props / options (and what each represents).
- Public surface (the protocol — what dependents and callers can use): public methods, the returned shape of a composable, a wrapper's props and slots, a service's exported API.
- The customization surface (what dependents change): protected methods, a composable's callbacks, a wrapper's slots and events, a service's injectable collaborators.
- Properties that look like configuration (typed, defaulted, often arrays/maps).
- Lifecycle markers (constructor / init / teardown hooks; for a composable, the framework lifecycle hooks it registers and therefore the call context it requires).
- Automatic behaviors (anything happening inside the methods that callers don't have to ask for — auto-tenant filtering, auto-soft-delete, auto-audit, auto-cache, auto-translation merge).
- Escape hatches (methods that explicitly bypass the automatic behaviors, often named `*Raw`, `getBuilder`, `getRepository`, `withDeleted`, etc.).

### Step 2 — Find all dependents

The dependent relation is per `unit_kind` (§ Inputs table). For `base-class` it is inheritance:

```bash
grep -rln "extends <BaseClassName>" --include="*.ts" --include="*.py" --include="*.java" .
```

For the other four kinds it is **import + usage**, which needs both halves — an import with no usage is a dead import and must not inflate the count:

```bash
# import sites of the exported symbol, then usage within those files
grep -rln "<UnitName>" --include="*.<ext>" . | xargs grep -ln "<UnitName>[(<[:space:]]"
```

For a `wrapper`, also count element/tag usages, which in most template syntaxes do not look like function calls. Count each dependent FILE once, however many times it uses the unit — otherwise one enthusiastic file makes a unit look load-bearing on its own.

For each dependent, note:
- Path.
- What configuration it sets (overridden statics/getters; the options object passed to a composable or service; the non-default props passed to a wrapper).
- What it customizes (overridden protected methods; slots filled; callbacks supplied).
- What it adds beyond the unit.

### Step 3 — Sample 3-5 representative dependents deeply

Pick dependents that span the range:
- Smallest dependent (least customization) → shows the minimum-viable shape.
- Most-customized dependent → shows the maximum-customization shape.
- One with a non-obvious use (overrides a hook the others ignore; passes a prop the others leave defaulted; calls the composable from an unusual context) → shows edge cases.

Read each in full. Note configuration values, override bodies, comments explaining WHY.

**Record the denominator, not just the sample.** Note the total dependent count found by the caller's grep (`extract-codebase-overview § Step 5` already has it for classes; Phase 2.5's pattern detection has it for the other four kinds) and carry it through to the output as `<N> of <M> <dependents>`, using the kind's own noun — extenders / callers / usage sites / importers / instantiation sites. "3 extenders sampled" and "3 of 4" and "3 of 273" are three different claims and the first is indistinguishable from the other two. Any statement in the authored pattern that generalizes across dependents ("every subclass sets `X`", "no caller passes `Y`", "the raw primitive is never used directly") rests on the sample, not the population, and is written `[inferred: <basis>; sampled <N>/<M> <dependents>]` per `phase-2-profile.md § Provenance discipline` — the same rule that governs sampled sections of `_extracted-codebase.md`.

### Step 3.5 — Recursive extraction of cited collaborators (NEW)

The base class almost always references other classes that are themselves part of its protocol — interfaces it consumes, helper classes it composes, criteria/factory/strategy classes its callers must implement. These collaborators are part of the pattern; documenting the base in isolation leaves a gap.

For every type the base class imports + uses in its public/protected signature (NOT every transitive dep — just the ones a caller would need to know about):

1. Read the collaborator file.
2. If it's an interface: extract the contract (methods + types) + 1-2 real implementations.
3. If it's a concrete class: extract its public surface + how the base calls it.
4. **Decide: inline or sibling pattern?**
   - **Inline** in the main pattern doc when the collaborator is small (<50 lines), used in 1-2 places, conceptually part of the base.
   - **Sibling pattern file** (`ai/patterns/<collaborator>.md`) when the collaborator has its own dependents, is referenced from multiple units, or is large enough to deserve its own doc. Schedule the sibling extraction after the main one.

For the main pattern doc, always include a "Collaborators documented separately" section linking siblings.

Heuristic for "needs its own pattern doc": collaborator has 3+ implementations OR is referenced by 2+ base classes OR is >100 lines.

### Step 4 — Identify automatic behaviors + their bypass

For each automatic behavior found in Step 1:
- WHAT does it do? (one sentence)
- WHERE in the base class is it implemented? (file:line)
- HOW do you opt out / bypass? (named method, flag parameter, decorator, etc.)
- WHEN should you bypass? (legitimate use cases — usually documented in code comments or visible in 1-2 dependents that bypass)
- WHEN should you NEVER bypass? (the failure mode — what breaks when you skip the auto-behavior)

### Step 5 — Find pitfalls from the codebase

Look for evidence of past mistakes:
- `git log --all -S "<base class name>"` for commits that fixed misuse.
- Comments containing "DON'T", "NEVER", "TODO", "HACK", "WORKAROUND" in the base class file.
- Tests with names like "should not allow X" or "regression test for Y".
- Custom rules in `.claude/rules/` mentioning the base class.
- Existing entries in `ai/dynamic/feedback-learned.md` or `ai/failures/` that reference this base.
- Memory files (`~/.claude/projects/<project>/memory/*.md`) referencing the base.

### Step 5.5 — Mirror existing pattern shape if present (NEW)

In ENHANCE / REFRESH mode, an `ai/patterns/<base>.md` may already exist. Before authoring, READ it.

- Capture its section ORDER (e.g., "Overview → Type Parameters → Key Methods → Automatic Filtering → Criteria System → ...").
- Capture its section NAMES verbatim (the existing voice — "Key Methods" vs "Public Protocol" vs "API Surface" — pick the one already in use).
- Capture its level of formality (table-heavy? prose? code-example-heavy?).

Author the new content INSIDE the existing skeleton:
- Keep every existing section name + order.
- Update existing section content with extracted facts (citing real file:line).
- ADD new sections only when extraction surfaced content the existing doc has no place for (e.g., a "Pitfalls" section the original lacked). Place them at the END unless they're correcting a critical gap mid-flow (e.g., automatic-behaviors deserves to be near the top).
- NEVER reorder existing sections without an explicit reason in the output footer (e.g., "Reordered: moved 'Pitfalls' to position 4 because deprecated APIs are critical to surface early").

In CREATE mode (no existing pattern doc) OR if the existing one is a stub (<30 lines), use the default 9-section structure from Step 6.

### Step 6 — Author the pattern (the output)

Use this 9-section structure (or match `topic_spec` if provided, or match existing shape per Step 5.5). The section NAMES below are the `base-class` spelling; for another `unit_kind`, rename each to the kind's own vocabulary per the § Inputs table — "Configuration surface" becomes "Props (with defaults)" for a wrapper and "Options" for a composable, "Override hooks" becomes "Slots + events" or "Callbacks". Rename; do not drop. A section that genuinely has no analogue for the kind is omitted per Step 7, and the omission is the finding.

```markdown
# <UnitName><GenericParams> Pattern

## Overview

<One paragraph: what this unit does + where it lives + how many dependents, and how many of those were read (`<N> of <M> sampled`). For a wrapper, name the raw primitive it wraps and what it adds. Cite the file:line.>

## Type parameters
| Param | Represents |
| `Entity` | TypeORM ORM entity class |
| ...     | ...

## Configuration surface (override these in your subclass)

| Property | Type | Default | Purpose |
| `uniquenessFields` | `string[]` | `[]` | Fields validated for uniqueness on save |
| ... | ... | ... | ... |

## The protocol — public methods extenders + callers use

| Method | Purpose | Returns |
| `find(criteriaName?)` | Standard list with criteria | `T[]` |
| ... | ... | ... |

## Override hooks — protected methods you can customize

| Method | When called | Default behavior | Override when |
| `customValidation(dto)` | After uniqueness check, before save | no-op | Adding business rules beyond uniqueness |
| ... | ... | ... | ... |

## Automatic behaviors (the base does this for you — DON'T re-implement)

1. **<Behavior name>** (`<file:line>`)
   - Does: <one sentence>
   - Bypass: <method name + when legitimate>
   - Never bypass when: <the failure mode>

## Escape hatches (when you genuinely need to skip the base)

- `getBuilder(alias)` — raw `SelectQueryBuilder` access. Use when criteria system can't express the query. Tenant + soft-delete are NOT auto-applied; you MUST add them manually.
- ...

## Examples from this codebase

- **Smallest extender**: `<path>` — only sets `uniquenessFields`.
- **Most customized**: `<path>` — overrides 4 hooks; see for a heavy-customization template.
- **Non-obvious override**: `<path>` — uses `<hook>` to <reason>.

## Pitfalls observed in this codebase

- ❌ Calling `dataSource.getRepository()` directly — bypasses tenant + soft-delete filters. Found in `<file:line>` (since fixed). Use `this.getRepository()` from base.
- ❌ ...

## When NOT to use this unit

- <Cases where a different base class / composable / wrapper / service / type is correct.>

## Related patterns + ADRs
- `ai/patterns/<related>.md`
- `ai/decisions/<NNNN>-<related>.md`
```

### Step 7 — Verify the output

Before writing, check:
- Every method/property cited exists in the actual file (no hallucinations).
- Every example file path exists.
- Every pitfall has evidence (file:line or commit reference) — no "common mistakes" without a source.
- No generic prose ("use parameterized queries" without project context).
- No section is empty — if a section genuinely has no content for this base, OMIT the section, don't write `_TBD_`.

If any check fails, regenerate the offending section. If still failing after 1 retry, leave the section out + note in skill output: "section X omitted — no extractable signal."

## Output

Write the pattern file to `output_path`. Print a one-line summary:

```
Authored <output_path> (unit_kind: <kind>): <N> of <M> <dependents> sampled, <A> automatic behaviors, <P> pitfalls cited, <Q> escape hatches.
```

## Failure modes

- **Unit is generic + project doesn't actually use it (0-2 dependents)** → don't write a pattern; not enough signal. Report and exit.
- **Unit is huge (>2000 lines) + most code is implementation, not protocol** → focus extraction on the public + customization surface signatures + property types; skip implementation walk.
- **Dependents all look identical (cookie-cutter)** → reduces value of "Examples from this codebase" section; pick just 1 and note "all dependents follow this same minimal shape."
- **Unit has no automatic behaviors (it's just a thin pass-through)** → omit the "Automatic behaviors" section entirely; this unit may not deserve a pattern doc. For a `wrapper` this is a real finding rather than a shrug: a wrapper that adds nothing over its primitive is a candidate for deletion, and saying so is more useful than a pattern doc for it.
- **A composable that is called from an invalid context somewhere in the codebase** → that IS the pitfall section, with the `<path:line>` of the offending call. Do not soften it into "must be called during setup"; cite the file that doesn't.
- **`unit_kind` is wrong for the file** (a "composable" that is actually a plain utility with no framework state, a "wrapper" that renders nothing) → re-classify and re-run with the correct kind rather than forcing the terminology; the pattern doc inherits the mistake otherwise.

## Quality bar

The output must satisfy: **a senior engineer reading this pattern + the unit's file should be able to write a new conforming dependent — a subclass, a call site, a usage, an implementation — without asking any questions.** If they'd still need to grep around to figure out conventions, the pattern is incomplete.
