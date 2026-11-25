---
name: llm-must-read-kb
description: "Prescribed-access trigger banks (must-read.kb/). Agent MUST load when adding, retiring, or re-scoping a trigger in a bank, or when a trigger misfired -- never fired, or fired on the wrong condition. Design successor: Skill(llm-triggers)."
---
--- # workaround: anthropics/claude-code#13005
setup: |
    Adopting a `must-read.kb/` requires a "Required Reading" stanza in the
    host CLAUDE.md, wiring the agent to the trigger bank. See "Adoption" in
    the skill body for the exact text. Nothing else: a description names
    when to load a skill, but only this stanza names where the bank is.
---

# Must-Read Trigger Banks

Extends `Skill(llm-kb)` with a **prescribed access pattern**: a `.kb/`
whose entries are consulted by *triggered conditional read*, not by free
query. Filename names the trigger; body holds the directives.

A plain `.kb/` is access-pattern-agnostic — readers decide when and how
to load. A `must-read.kb/` is not: the host CLAUDE.md instructs the
agent to scan filenames during planning, match them against the current
situation, and read matched bodies before the named action.

## The Innovation: Prescribed Access

The pattern works because filenames are *cheap to scan* and *expensive
to ignore*:

1. Agent runs `ls -RF must-read.kb/` once at session start.
2. The listing becomes a passive index of all trigger conditions.
3. Before any action (and continuously while planning), the agent
   mentally walks the listing and asks: *does any trigger fire here?*
4. On match, the agent reads that file's body and applies it before
   proceeding.

A trigger binds from the moment its listing is in context. The `ls`
that produces the listing therefore precedes every trigger in the
bank — `before/ANY-shell-commands.md` included — and no entry needs
to carve it out; a skill bank's triggers likewise bind once the
skill's own `ls` has run.

No tool-call hook, no startup tax beyond the `ls`. Bodies stay unloaded
until their trigger fires. The directory IS the index.

## Anatomy

```
must-read.kb/
├── before/
│   └── $TRIGGER.md         ─ read+act BEFORE the named action
├── after/
│   └── $TRIGGER.md         ─ read AFTER the named event completes
└── when/
    └── $TRIGGER.md         ─ read WHEN the situational match fires
```

All three subdirs are optional. Topical sub-grouping is allowed when a
trigger family grows (see "Nesting").

## Trigger Junctures

The three subdirs encode *when* the read fires. Pick by the directive's
relationship to the named situation:

| Subdir | Semantics | Example |
|---|---|---|
| `before/` | Hard precondition. Read MUST complete *and* prescribed actions MUST run before the named action. | `before/ANY-shell-commands.md` |
| `after/` | Read on completion of the named event. Typically for cleanup, audits, or post-mortems. | `after/an-unexpected-Bash()-tool-call-failure.md` |
| `when/` | Read when a situational predicate holds mid-task. Fuzzier triggers. | `when/user-instructions-are-inconsistent.md` |

`before/` creates an action dependency: the read is sequenced *before*
the triggered action — not parallel, not deferred.

## Trigger File Format

Each file is a small markdown directive. Recommended template:

```markdown
# {Before|After|When} {restated trigger}

{1–2 sentences naming the situation in author's own words. Helps the
agent confirm the match before reading further.}

## {Directive section(s)}

{Rules, examples, anti-patterns. Code blocks where useful.}

## When NOT to trigger   ← recommended for `when/`, optional elsewhere

- {edge cases that look like the trigger but aren't}
```

**Conventions:**

- **H1 restates the trigger** with the juncture verb (`# Before X`,
  `# After X`, `# When X`). Files are often opened standalone; the H1
  must self-orient the reader.
- **Keep bodies short.** A trigger file that exceeds ~50 lines is a
  signal that the method belongs in a shared `procedures.kb/` (see
  "Composition with procedures.kb/").
- **State the trigger condition in prose**, even though the filename
  encodes it. Filenames slug; bodies disambiguate.

## Naming

Filename + parent-dir verb = full trigger phrase.

```
before/ANY-shell-commands.md          →  "Before ANY shell commands"
when/cwd-starts-with-wsl.localhost.md →  "When cwd starts with wsl.localhost"
after/distilling-from-a-raw-source.md →  "After distilling from a raw source"
```

Rules:

- Kebab-case slug; descriptive enough that filename alone signals match.
- Use `ANY-` prefix for unconditional triggers within a juncture (e.g.
  `before/ANY-shell-commands.md` fires for every shell command).
- Verb tense in the slug should compose with the juncture: `before/`
  pairs with gerunds (`making-code-changes`), `after/` with nouns or
  past events (`an-unexpected-Bash-failure`), `when/` with predicates
  (`user-instructions-are-inconsistent`).
- Name the locus, not the decision.

  > [!@bukzor] 2026-11-22: the slug names where the directive applies
  > (`before/dotfiles-repo/committing.md`), never what it decides
  > (`committing--hold-till-session-end.md`), so changing the directive
  > never renames the trigger. A `--` separates alternate titles for one
  > occasion (`spawning-a-sub-agent--delegating-a-task.md`).

## Nesting

Topical subdirs are allowed when a trigger family grows past ~3 files:

```
must-read.kb/before/git/
must-read.kb/before/git/ANY-git-command.md
must-read.kb/before/git/commit.md
must-read.kb/before/lazy-loading/
must-read.kb/before/lazy-loading/skills.md
must-read.kb/before/lazy-loading/commands.md
```

The juncture verb (`before`/`after`/`when`) stays at the top; nested
dirs add a topic axis. Don't sub-nest `.kb/` directories — the trigger
slug, not the directory shape, carries the categorization.

## No aliasing

Do not give one body multiple filenames, by symlink or copy. Every
alias is its own row in the index: the scan surfaces each name, the
agent reads each match, and the same body lands in context once per
alias. Copies add drift on top of the duplication.

When one body seems to serve several triggers:

- **Broaden the canonical slug** until it names the whole family
  (`before/modifying-production-data.md`, not per-variant delete/
  update/insert names) — but only while it stays concrete. A slug of
  action verbs fires; an abstract description of the situation gets
  scanned past.
- **Keep the name that fires.** When one variant's slug has proven to
  trigger reads and the broader description hasn't, effectiveness
  outranks incumbency: the proven name becomes canonical.
- **Name the remaining occasions in the body's opening prose**, where
  the H1 restates the trigger — the slug fires the read; prose
  carries the variants a slug cannot.
- **Two occasions with no honest broader name are two entries.** If
  they share method, factor it into `procedures.kb/` (next section)
  and keep each trigger file a thin pointer.

## Composition with `procedures.kb/`

When a trigger's method is shared across triggers, or long enough to
deserve its own file, factor it out:

```
skill.kb/
├── must-read.kb/
│   ├── before/marking-kb-work-done.md   ─ "run the validation pass"
│   └── after/creating-or-editing-kb-files.md  ─ "run the audit pass"
└── procedures.kb/
    ├── self-audit.kb/
    │   ├── audit-claudemd-enumeration.md
    │   └── audit-per-file-scope.md
    └── validation.md
```

Trigger file says **when**; procedure file says **how**. The trigger
references the procedure by path. Multiple triggers can reference one
procedure (deduplication).

## Scopes (Homes)

The pattern installs at three scopes:

| Scope | Location | Purpose |
|---|---|---|
| Personal | `~/.claude/must-read.kb/` | User's own rules across all projects |
| Project | `$REPO/.claude/must-read.kb/` | Project-specific triggers, versioned with the code |
| Skill | `$SKILL/skill.kb/must-read.kb/` | Triggers bundled with a skill; consumers inherit them on load |

All three coexist; each scope ships its own `must-read.kb/`. The agent
scans every reachable one during planning. Same-named triggers across
scopes are not deduplicated — each trigger file is independent.

## Adoption

Each scope's host CLAUDE.md needs a "Required Reading" stanza. The
canonical text:

```markdown
## Required Reading: Triggers

Continually monitor for installed triggers' occasions; take the action when
one arrives.

### Definitions

- an "occasion" is a condition that may hold at any given moment
- a "trigger" is user-written instruction binding an action to an occasion
- a trigger is "installed" once it appears in your context
- `before` marks a dependency: the trigger's action completes before the named
  action starts
- `must-read://DIR` means `Bash(llm-must-read-ls DIR)`

### Installation

0. statically:
   - before: your first tool call
     read: must-read://$SCOPE
1. `must-read.kb/` paths, each naming the occasion to read that file
2. skill `description`s, each naming the occasion to load the skill
3. `triggers:` frontmatter of any file you load
4. `requires:` frontmatter, an immediate trigger (deprecated)
```

`$SCOPE` is the directory whose bank this CLAUDE.md governs: `~` for a
personal home, `.` for a project. `must-read://` finds `must-read.kb/` or
`.claude/must-read.kb/` beneath it. `llm-must-read-ls` does not yet ship
with this skill; `ls -RF $SCOPE/must-read.kb` lists the same index.

### Schema

Beside the bank, a one-line `must-read.jsonschema.yaml` binds entries to
the canonical schema, so `llm.kb-validate` checks their frontmatter
(`Skill(llm-kb)`, positional binding):

```yaml
# yaml-language-server: $schema=https://json-schema.org/draft-07/schema
$ref: "skill://llm-must-read-kb/jsonschema/must-read.jsonschema.yaml"
```

The canonical (`jsonschema/must-read.jsonschema.yaml`) admits `triggers:`
only; `name:`/`description:` are SKILL.md fields, and a bank entry's
trigger is its filename.

### Skill scope

A skill has no host CLAUDE.md in the consumer's context — its `SKILL.md`
*is* what loads. So the stanza goes in the `SKILL.md` body, near the top,
and its cadence is skill-load rather than session-start. The canonical
text, verbatim:

```markdown
> **IMPERATIVE:**
>
> Your FIRST action when this skill loads MUST be:
> `Bash("ls -RF skill.kb/must-read.kb/")`
>
> That listing is an index of triggers: each filename names the occasion to
> read it. Walk it while planning, before ANY action, and read every entry
> whose trigger matches the work at hand — `before/` entries must be read
> *before* the action they name, not alongside it.
```

Ship it in every skill that carries a bank; a bank nothing points at is a
bank nothing reads. The skill's own `CLAUDE.md` governs maintainers, not
consumers, and is not a substitute.

## When to Use

Good fit:

- Rules that apply only to *some* actions, not all sessions.
- Directives the agent forgets when not foregrounded.
- Conventions whose full text is too large to inline in CLAUDE.md.
- Cross-cutting concerns (shell hygiene, commit etiquette, language
  style) that fire in many contexts.

Poor fit:

- One-shot project orientation → put in CLAUDE.md directly.
- Decision rationale or history → use ADR (`Skill(llm-collab)`).
- Living design knowledge → use `design.kb/` (`Skill(llm-design-kb)`).
- Always-applicable rules → inline in CLAUDE.md; trigger banks add
  overhead the agent must traverse every plan.
- **Anything needed to recognize the trigger** → inline it. A trigger
  cannot gate the knowledge that fires it: a command table filed under
  `when/the-user-issues-a-command.md` reaches only agents who already
  know the commands exist. Vocabulary, notation, and command names are
  recognition; file them where they load unconditionally. Banks hold
  what an agent *does* once it knows where it is, never what tells it
  where it is.

## Relationship to `Skill(llm-kb)`

A `must-read.kb/` is a regular `.kb/` — same naming, promotion, and
maintenance rules apply. This skill **specializes** the parent pattern
by:

1. Fixing the top-level structure (`before/`/`after/`/`when/`
   subdirs).
2. Prescribing the access pattern (scan-and-trigger, not free query).
3. Treating filenames as the index, not just identifiers.

When the prescribed access pattern is not wanted, use a plain `.kb/`
instead. The two are not interchangeable: a regular `.kb/` will not be
read on the trigger cadence, and a `must-read.kb/` is overkill for
content readers will query on their own.
