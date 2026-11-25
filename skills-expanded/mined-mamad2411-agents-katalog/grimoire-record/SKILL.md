---
name: grimoire-record
description: Record domain terminology and architectural decisions from conversations.
---

# Purpose

Watch the conversation for domain concepts and architectural decisions. Record them into the `.grimoire` knowledge store.

# Scope

This skill edits two areas under `.grimoire/`:

- `CONTEXT.md` — domain entities, definitions, synonyms, relationships
- `adr/` — architecture decision records

This skill does NOT:

- Bootstrap `.grimoire/` (use grimoire-init)
- Interrogate the user (use grimoire-clarify)
- Write `spec/` or `ticket/` files

Completion: Only CONTEXT.md and adr/ are modified by this skill.

---

# Trigger Detection

Before every response, scan the current conversation turn for:

- New domain terms, entity names, or jargon the user introduces
- A term used with a meaning specific to the project
- Synonyms or aliases for an existing term
- An architectural decision: technology choice, integration pattern, boundary definition, constraint, or rejected alternative

If nothing qualifies, do nothing. Do not force entries.

Completion: Every qualifying item from the current turn is either recorded or intentionally skipped with a reason.

---

# CONTEXT.md Workflow

## Entry format

Every concept gets one entry:

```markdown
### [concept-name]
- **Definition:** [one concise sentence]
- **Synonyms:** [alias1, alias2, ...] (omit if none)
- **Relationships:**
  - [verb] [target-concept] (omit if none)
```

Constraints:
- One sentence per definition. Split long definitions by creating sub-concepts.
- Synonyms list comma-separated aliases the user or codebase uses interchangeably.
- Relationship verbs: `depends on`, `contains`, `references`, `implements`, `extends`, `communicates with`, `belongs to`.

See [references/context-template.md](./references/context-template.md) for full template and examples.

## Adding a concept

1. Read the current `CONTEXT.md`.
2. Check: does this concept already exist (name or synonym match)?
   - If yes and the definition matches: skip.
   - If yes and the definition conflicts: flag to user, ask which definition is correct.
   - If no: append the new entry.
3. Update any existing entries whose relationships or synonyms reference this new concept.
4. If the entry count now exceeds 100, trigger [Entity Overflow Split](#entity-overflow-split).

Completion: New concept is present in CONTEXT.md. Cross-references updated. Entry count checked.

## Updating a concept

When the user refines a definition:

1. Locate the existing entry.
2. Replace the definition/synonyms/relationships with the refined version.
3. Check all entries that reference this concept — update if the relationship changed.

Completion: Old definition replaced. Dependent entries consistent.

## Entity Overflow Split

When CONTEXT.md exceeds 100 entries:

1. Group entries into larger domain categories (e.g., "Billing", "Auth", "Ordering").
2. For each domain with ≥5 entries, create `.grimoire/CONTEXT-[domain-slug].md`.
3. Move those entries into the domain file.
4. Replace entries in `CONTEXT.md` with a domain index table.

Index table format:

```markdown
## Domain Index

| Domain        | File                               | Entry Count |
| ------------- | ---------------------------------- | ----------- |
| [Domain Name] | [CONTEXT-xxx.md](./CONTEXT-xxx.md) | N           |
```

5. Entries that don't fit any domain (<5 per category) stay inline in CONTEXT.md under an "Uncategorized" section.

Completion: No single file exceeds 100 entries. CONTEXT.md contains the index. Every entry is reachable through the index.

---

# ADR Workflow

## When to write an ADR

Write an ADR only when a decision meets ALL of:

1. It has long-term consequences (reversing it costs a quarter or more).
2. A rational reader could have chosen differently — the decision was not obvious.
3. Multiple alternatives existed at the time.

Do NOT write an ADR for:
- Trivial or obvious defaults (e.g., "we use Git").
- Library choices with low switching cost.
- Decisions already captured in CONTEXT.md as concepts.
- Temporary or experimental choices that don't yet commit the project.

Completion: Every qualifying decision has an ADR. Every skipped decision can be justified by the exclusion criteria.

## ADR categories

Record decisions in these categories:

| Category              | Example triggers                                                                    |
| --------------------- | ----------------------------------------------------------------------------------- |
| Architecture pattern  | Monorepo vs polyrepo, event sourcing, CQRS, microservices vs monolith               |
| Integration pattern   | Domain events vs sync HTTP, shared DB vs API                                        |
| Strong tech binding   | Database, message bus, auth provider, deployment target — switching costs a quarter |
| Boundary definition   | "X belongs to Y context; others reference by ID only." Explicit NOT-dos.            |
| Intentional deviation | "We hand-write SQL instead of using an ORM because X."                              |
| Invisible constraint  | "Compliance forbids AWS." "Partner API requires <200ms response."                   |
| Rejected alternative  | "We chose REST over GraphQL because X." Record the rejected option.                 |

## File format

Naming: `NNNN-title-with-dashes.md` (zero-padded, next available sequence number).

Template:

```markdown
# [Decision Title]

**Status:** [Proposed | Implementing | Testing | Completed | Deprecated | Superseded]
**Date:** YYYY-MM-DD

## Context

[1–2 sentences: what prompted this decision and what alternatives existed.]

## Decision

[1–2 sentences: what we chose and why.]

## Consequences

- [What this enables.]
- [What this constrains.]
- [What we must do because of this.]
```

See [references/adr-template.md](./references/adr-template.md) for full template and examples.

## Adding an ADR

1. Determine the next available sequence number (check existing adr/ files).
2. Create the file.
3. Set status to `Proposed` unless the user indicates otherwise.

Completion: ADR file exists with correct sequence number and valid frontmatter.

## Updating ADR status

When implementation progresses:

1. Read the ADR.
2. Update the `Status` field.
3. If superseded, add a `Superseded by:` line pointing to the new ADR.
4. Do NOT delete or rewrite the decision itself — ADRs are immutable history.

Completion: Status field reflects current reality. Superseded ADRs point to their replacement.

---

# Pre-Flight Checks

Before writing any file:

- Verify `.grimoire/` exists. If not, tell the user to run grimoire-init first. Do NOT create it.
- Verify `.grimoire/CONTEXT.md` exists. If not, create it from the template in references.
- Verify `.grimoire/adr/` exists. If not, create the directory.

Completion: Target paths exist. Write operations will succeed.

---

# Rules

- One sentence per definition. Split before adding a second sentence.
- Never invent definitions. If the conversation doesn't provide enough information, ask the user.
- Never remove entries from CONTEXT.md or ADR files. Append and update only.
- CONTEXT.md is for domain terminology. ADRs are for irreversible decisions with multiple alternatives. Do not cross-contaminate.
- Do not record library choices with low switching cost as ADRs.
- Status field is the only mutable field in an ADR after creation. The decision text is immutable.
