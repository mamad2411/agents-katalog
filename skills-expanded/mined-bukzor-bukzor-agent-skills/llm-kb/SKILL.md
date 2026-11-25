---
name: llm-kb
description: "Conventions for structured multi-agent knowledge bases. Agent MUST load when creating a .kb/ collection, when adding, renaming, splitting, or removing files in one, when writing or changing a `*.jsonschema.yaml`, or when explaining or repairing a .kb/ layout."
---
--- # workaround: anthropics/claude-code#13005
setup: |
    `uv add llm-kb` from within this workspace also puts `llm.kb-validate`
    on `$PATH` as an installed console script (see Tools Provided below)
    -- and code that imports `llmd` directly gets the package too.
    `llm-kb` is a workspace member, so `uv add` detects the sibling and
    wires `tool.uv.sources` to it -- no PyPI lookup, no manual
    `[tool.uv.sources]` edit.

    From a separate repo (not a workspace member), add it explicitly as
    an editable path dependency:

    ```sh
    uv add --editable ../relative/path/to/bukzor-agent-skills/llm-kb
    ```

    Editable is enforced: without it, `uv sync` snapshot-builds llm-kb once
    and later edits to its source never reach the consumer, so
    `llm.kb-validate` refuses to run from such a copy. `[tool.uv.sources] llm-kb = { path = "...", editable =
    true }` is the resulting/equivalent manual form.
---

> **IMPERATIVE:**
>
> Your FIRST action when this skill loads MUST be:
> `Bash("ls -RF skill.kb/must-read.kb/")`
>
> That listing is an index of triggers: each filename names the occasion to
> read it. Walk it while planning, before ANY action, and read every entry
> whose trigger matches the work at hand — `before/` entries must be read
> *before* the action they name, not alongside it.

The must-read entries link to audits in `skill.kb/self-audit.kb/` and
procedures in `skill.kb/procedures.kb/`; follow those links when triggers
fire. When adding new kb content of your own, browsing
`skill.kb/self-audit.kb/` directly is a cheap proactive check for relevant
quality concerns.

# llm.kb Pattern

Create structured knowledge bases using `.kb/` directory collections. Frontmatter
is optional, but if used, requires schema validation to prevent drift. Use when
organizing facts, tasks, or information for efficient LLM access across multiple
agents. Key principles: small focused files, CLAUDE.md for maintenance guidance
(never enumeration), synthesis files only when they add value beyond `ls`.

## Anatomy

```
$PROJECT/
├── CLAUDE.md ──────────────────── maintenance guide (root)
├── README.md ──────────────────── synthesis file (root scope)
├── $CATEGORY.jsonschema.yaml ─── schema
├── $CATEGORY.md ───────────────── synthesis file (category scope)
├── $CATEGORY.kb/
│   ├── CLAUDE.md ──────────────── maintenance guide (category)
│   ├── $ITEM.md ───────────────── content file
│   └── $NESTED.kb/
│       ├── CLAUDE.md ──────────── maintenance guide (nested)
│       └── $ITEM.md ───────────── content file
```

### Synthesis Files (README.md, $CATEGORY.md)

Roll up a scope to help readers decide whether to dive deeper.

- README.md -- root scope (the whole project or multiple `.kb/` collections),
  and the one nested case where `$CATEGORY.md` is unavailable: see
  "Where an Elaboration Goes"
- $CATEGORY.md -- category scope (rolls up `$CATEGORY.kb/`)

Say only what holds at collection scope -- themes, tensions, the shape the
members make together. Never enumerate the members and never restate one: a
list of the collection is what `ls` is for, and a hand-copied list goes stale
the next time a member is added or renamed. Mention a member only where
there is something to say about it that its own file cannot say. When there
is nothing to say at this scope, nothing is the right thing to say -- omit
the file.

Carries no frontmatter. A roll-up is prose about a collection, not a member
of one, so there is no schema for it to be data under -- and the one field it
used to declare, `last-updated:`, is what `git log -1` and `stat` already
answer, more honestly than a date a human remembers to bump.

### Maintenance Guides (CLAUDE.md)

Enable maintenance decisions, not content discovery. After reading, an agent
knows what belongs here -- not what's currently here.

- Root CLAUDE.md -- common principles (pushed up from per-directory guides)
- Per-directory CLAUDE.md -- category-specific guidance for that `.kb/`

Root CLAUDE.md must have an overview of available `.kb/` collections and
their purpose. It needs no frontmatter declaring this skill; the
`description:` carries the trigger.

After reading `$CATEGORY.kb/CLAUDE.md`, agent must know:
- What belongs here (concept, not enumeration)
- What does NOT belong (boundaries)
- When to add/read files here

Content discovery is `ls`. Never enumerate in CLAUDE.md.

❌ "Tools: Goose, Aider..." / "PRs: #123, #456..." / "Contains: api.md, auth.md"

## Frontmatter Directives

`triggers:` is specified by `Skill(llm-triggers)`. The rule a kb author needs:
a bare entry is well-formed only where the carrier was itself reached
conditionally. A CLAUDE.md discharges nothing, so its triggers need a stated
condition.

### Content Files ($ITEM.md in .kb/)

Individual items within collections. Each file represents one thing (one tool,
one decision, one task).

- Markdown prose, optionally with YAML frontmatter
- If frontmatter used, must conform to `$CATEGORY.jsonschema.yaml`

Create when adding a new item to a collection. The file IS the item; there's no
separate registry.

### Schema Files ($CATEGORY.jsonschema.yaml)

Validates frontmatter in `$CATEGORY.kb/*.md`, and in the sibling
`$CATEGORY.md` roll-up where that carries frontmatter (a claims ledger's
defining claim does). Prevents drift between files in the same collection.

- Required if any content files in that collection use frontmatter
- Optional if content files are prose-only
- Skips CLAUDE.md files (maintenance guides don't need frontmatter)
- Is a component of `$CATEGORY.kb/`, though it sits beside it: moving,
  renaming, or removing the collection moves, renames, or removes the
  schema too. [!@bukzor] 2026-11-18

Create when you want structured metadata on content files. Omit for prose-only
collections.

### Collections ($CATEGORY.kb/)

A directory holding homogeneous content files -- **same type of thing**.

- Each item is one file
- All files share the same schema (if using frontmatter)
- Related by type, not by tool/subject

Create when you have multiple items of the same kind. Use the `.kb/` suffix to
signal "this is a collection, use `ls` for contents."

Example: `tools.kb/` contains tool profiles; `features.kb/` contains feature
comparisons.

### Decision Points ($ITEM.md + $ITEM.kb/)

At its second contending answer, a question or decision SHOULD be
elaborated: `$ITEM.md` poses the question, `$ITEM.kb/` holds one file
per candidate answer or option -- open, chosen, and declined alike
(same shape as any other collection -- one file per item).

When the decision closes, rewrite `$ITEM.md` to state the resolution and
why, rather than leaving it as a bare question. Then choose per option's
ongoing value:

- keep `$ITEM.kb/` as background context, if the rejected alternatives are
  worth remembering why they lost
- clean it up entirely, if the options stop mattering once decided

Either way, `$ITEM.md` should stand alone as the answer -- a reader
shouldn't need `$ITEM.kb/` to know what was decided, only to know why an
alternative wasn't picked.

### Where an Elaboration Goes

Nest by what a file *elaborates*, not by what it resembles. Anything
elaborating `X.md` goes under `X.kb/`, at whatever depth `X.md` sits.
The trap is a directory that already holds peer collections: two
`$SIBLING.kb/` beside `X.md` make a third peer look like the
precedent, when the only question is what the new collection is about.

Its roll-up takes the collection's own name -- `X.kb/candidates.md`
rolling up `X.kb/candidates.kb/`. `README.md` inside a collection is
for the case that forces it: a collection elaborating a same-named
item file cannot name its roll-up `X.md`, because `X.md` is the item.

## Recognizing the Shape

The pattern is defined by its end state, not by how content arrives.
Wherever several same-type items share a parent -- parallel sections in
one file, an ad hoc directory, scattered loose files, or a newly-noticed
category -- that end state is a `.kb/` collection: one file per item,
`$CATEGORY.kb/` naming, sibling `$CATEGORY.md`/`.jsonschema.yaml` where
they'd help.

Recognize non-canonical instances by the same shape, regardless of
starting form: a directory of homogeneous items missing the `.kb`
suffix, a sibling pointer file, or the parent scope's naming convention
(a date-prefixed sibling in `todo.kb/` implies the promoted collection
keeps that prefix -- `references/dated-slug-filename.md`) is this
pattern in the wrong shape. Bring it into
shape the same way you'd promote a flat file -- growth-signal checklist
and mechanical steps: `skill.kb/self-audit.kb/promotion-signals.md`,
`skill.kb/procedures.kb/promote-to-collection.md`.

## Naming

Applies to `$CATEGORY` and `$ITEM` identifiers (directory and file names).

- Use kebab-case
- Be descriptive -- agent must know roughly the content from the filename
- Name what the item is about, so the name stays true as the content
  is edited
- Prepend digits if inherently ordered (e.g., `001-setup.md`, `002-config.md`)
- Zero-pad to twice the digits you expect to need
- Dated items (events): `YYYY-MM-DD-NNN-slug.md` -- see
  `references/dated-slug-filename.md`

## When to Use

Good fit:

- Information with structure (metadata + explanation)
- Multiple categories of related content
- Future agents will maintain/extend
- LLMs will consume frequently

Poor fit:

- Simple flat information (single README suffices)
- One-time use
- No structured metadata needed

## Creating a Collection

When creating a `.kb` from scratch, **read `references/creating-a-new-kb.md`
before writing files.** It contains the full procedure and the four quality
passes (enumerate-and-categorize, persistence, per-file scope, schema
potential). The summary procedure here is for orientation only:

1. Ensure root CLAUDE.md meets requirements (see Maintenance Guides above)
2. Identify homogeneous categories → `$CATEGORY.kb/` directories
3. Design schemas for frontmatter → `$CATEGORY.jsonschema.yaml` (if using frontmatter)
4. Create per-directory CLAUDE.md guides
5. Create synthesis files (`$CATEGORY.md`) where they help
6. Populate content files
7. Validate with `llm.kb-validate <path>`

## Reading Collections

Use category directories as query filters. Load entire categories in one
operation to save tokens and time:

```bash
head -n999 $CATEGORY.kb/*.md          # All items in category
head -n999 $CATEGORY.kb/**/*.md       # Including nested
grep -l "keyword" $CATEGORY.kb/*.md   # Search within category
```

This exploits small focused files -- loading 5 related files is faster than
searching one 500-line file.

## Tools Provided

### llm.kb-validate

Purpose: catch frontmatter schema violations (error prevention).

Why offered: manual validation is error-prone and wastes tokens debugging
schema mismatches.

Usage:

```bash
llm.kb-validate                  # Validate current directory (default)
llm.kb-validate path/to/project  # Validate specific directory
llm.kb-validate category.kb/     # Validate one category
llm.kb-validate file.md          # Validate single file
```

Recursively finds and validates `.kb/` directories. Auto-detects schemas. Skips CLAUDE.md files.

What the walk *discovers* is filtered by `.gitignore`: a `.kb/` under
`trash/` or `node_modules/` is scratch, not corpus, and its rot must
not pad the error count. Name such a path on the command line and you
get it anyway -- asking is asking. Each path is asked of the repository
holding it, so a submodule's own `.gitignore` governs inside it.

Recommended: run `llm.kb-validate` before committing changes.

"No schema found" for `ideas.kb`/`todo.kb`: copy from `llm-subtask/skeleton/.claude/`.

### llm.kb-validate-links

Purpose: catch path references that don't resolve -- the failure a
schema cannot see. `llm.kb-validate` checks that a `why:` field is an
array of strings; it has no way to know those strings are meant to be
paths, so a typo'd cross-reference passes schema validation and
becomes a broken chain nobody notices.

Not an installed console script -- run it by path, `uv` handles its
deps:

```bash
~/.claude/skills/llm-kb/bin/llm.kb-validate-links            # cwd, --strict
~/.claude/skills/llm-kb/bin/llm.kb-validate-links --lax path/
```

`--strict` (default) nominates only `./`- and `../`-prefixed strings:
no false positives, but blind to bare-relative refs like `foo.kb/bar.md`.
`--lax` also nominates path-shaped strings without that prefix -- more
recall, and CLI examples in prose will surface as hits to triage. Use
it for a deliberate sweep, not as a per-commit gate.

> [!DRAFT] agent-authored 2026-09-09, c388d0cc, vetoable
>
> Read the prefix as an authoring convention, not only as a precision
> knob: write `../foo.md` to ask that it resolve, `foo.md` to mention
> it. A backticked path can be a link, or a string quoted from
> elsewhere -- a path another file's `why:` holds, a name a rename
> retired and an ADR keeps as provenance. Only a link must resolve
> here, and a quotation written as one is a defect in the prose, not
> in the tool. Two of the three broken links in `docs/dev` on
> 2026-09-09 were exactly that (commit `767d56a`), and a third of the
> species -- a command example with a trailing placeholder -- is
> already a regression case in
> `./.claude/todo.kb/2026-07-25-000-Test-coverage-for-llm-kb-validate-links.md`.

Checks three sources: frontmatter path fields, backticked body paths,
and markdown link destinations (inline `[t](../x.md)` and reference
definitions `[label]: ../x.md`, wrapped or not). URLs and bare `#anchor`
destinations are skipped; a trailing `#anchor` is stripped before
resolving. Destinations pass the same `--strict`/`--lax` shape gate as
backticked paths. Folding it
into `llm.kb-validate` proper is tracked in
`./.claude/todo.kb/2026-06-03-000-validate-path-references.md`.

## References

When creating a `.kb` from scratch, you must read
`references/creating-a-new-kb.md` before writing files.

Other references, load as relevant:

- `references/pattern-guide.md` - Complete pattern explanation
- `references/schema-design.md` - Schema design guidance
- `references/schema-reuse.md` - Sharing schema fields/files via `$ref`
- `references/frontmatter-outside-a-collection.md` - The three fixes when a file's frontmatter is under no schema
- `references/complete-example.md` - Worked example (birthday party planning)
- `references/splitting-large-docs.md` - Splitting heuristics
- `references/dated-slug-filename.md` - `$DATE-NNN-slug.md` naming, used by any dated collection

## Methodology kb (self-applied)

`docs/dev/` contains pre-distilled methodology this skill applies to itself:

- `procedures.kb/` -- step-by-step methods for recurring kb tasks
- `case-studies.kb/` -- narratives from instructive failures
- `concepts.kb/` -- structured definitions of recurring terms

`ls -RF docs/dev/procedures.kb/` lists procedures by task-shaped filename
(`post-mortem.md`, not `error-recovery-method.md`). Load one when its task
matches the user's request. Cross-referenced sibling collections
(`failure-modes.kb/`, `principles.kb/`, `glossary.kb/`) are seeded by
procedures as they're run; consult those when procedure files reference them.
