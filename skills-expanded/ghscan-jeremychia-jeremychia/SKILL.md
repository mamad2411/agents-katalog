---
name: memory-keeping
description: Add to or maintain Jeremy's preference memory system in this repo — write a new preference file, update an existing one, or decide whether something belongs here at all. Use when asked to remember a preference, record feedback, or tidy the memory index.
---

# Memory keeping

This repo holds **preferences** — how I want things written, reviewed and built. Project
facts live in that project's own local memory directory and are not copied here.

## 1. Decide whether it belongs here

| Belongs here | Belongs in project memory | Belongs nowhere |
| --- | --- | --- |
| A standard I hold across codebases | A codebase's internals, prod behaviour, ticket keys | Anything the repo already records |
| Feedback I gave on how to work | Which model does what, how CI is wired | Facts that only matter to one conversation |
| An engineering preference with a reason | Credentials, project ids, internal URLs | Restating a language's documented behaviour |

Two hard rules:

- **Never put employer-internal detail in this repo — it is public.** No internal project
  or bucket ids, no internal model or table names, no ticket keys, no internal Slack or
  wiki links, no production row counts, no group email addresses. Where a preference was
  learned on a real PR, keep the lesson and drop the identifiers: "a 948-word body" rather
  than the repo and number, "a fee booked separately" rather than the vendor.
- **If a preference cannot be stated without the internal specifics, it is a project fact.**
  Leave it in project memory.

## 2. Check for an existing file first

```bash
ls claude/memory/
grep -ril "<keyword>" claude/memory/
```

Update the existing file rather than adding a near-duplicate — that is the common failure,
and it produces two files that drift. Add a new one only when the fact is genuinely
separate. Delete a file that turns out to be wrong rather than qualifying it.

## 3. Write the file

`claude/memory/<short-kebab-slug>.md`:

```markdown
---
name: <same as the filename, without .md>
description: <one line — this is what gets read when deciding relevance>
metadata:
  type: user | feedback | project | reference
---

<the fact, stated first and plainly>

**Why:** <the reason — this is what makes it applicable to a case I have not seen yet>

**How to apply:** <what to do differently, concretely>
```

- `feedback` and `project` entries **must** carry **Why** and **How to apply**. A rule
  without its reason gets misapplied to the case it was not written for.
- **Link related memories liberally** with `[[name]]`, using the other file's `name:` slug.
  A `[[link]]` with no file yet is fine — it marks something worth writing.
- State the rule before the evidence. Keep the evidence to the part that shows the shape
  of the mistake.
- Same voice as everything else: lowercase prose, concise, plain language. The memory files
  are subject to their own rules.

## 4. Add exactly one line to the index

`claude/memory/MEMORY.md`, one line per memory, no frontmatter, never any content:

```markdown
- [Title](file.md) — hook that says when this matters
```

The hook is what makes it get loaded, so write it as the situation it applies to, not as a
summary of the file.

## 5. If a rule changes how Claude behaves by default

Also add or amend the corresponding line in `claude/CLAUDE.md`. That file is the
always-loaded short version; the memory file is the reasoning. Keep `CLAUDE.md` to the rule
itself — if it starts carrying the reasoning, it is too long to be read every session.
