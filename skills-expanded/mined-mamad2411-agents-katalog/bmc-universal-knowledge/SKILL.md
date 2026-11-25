---
name: bmc-universal-knowledge
description: >
  Maintains and evolves the BMC team's Universal Knowledge Base (UKB) — a
  persistent, self-structuring database of all validated team knowledge,
  pristine agent conclusions, architectural decisions, and conversation
  history. Every agent reads from and contributes to the UKB as their
  collective long-term memory. Use when recording validated insights,
  querying past conclusions, evolving the knowledge schema, or ensuring
  continuity across runs.
---

# BMC Universal Knowledge Base — Skill Protocol

**Before working:** Read `docs/team/knowledge-base/UNIVERSAL-KNOWLEDGE-BASE.md`.

The **Universal Knowledge Base (UKB)** is the **persistent, collective memory**
of the entire BMC agent team. It accumulates validated knowledge across all
runs, all agents, and all time — acting as the universal source of truth that
grows alongside the team's work.

---

## When to Use

- Any agent needs to look up a past decision, architectural fact, or team
  conclusion before starting work.
- An agent has reached a **pristine conclusion** (high-confidence finding) that
  must survive beyond the current run.
- The Orchestrator wants to seed new runs with full team context.
- The Judge wants to validate or elevate a candidate truth.
- The team needs to add a new knowledge domain (new §N section).
- User says: "knowledge base", "memoria del equipo", "base de conocimiento",
  "verdades del equipo", "UKB", "source of truth", "que no se olvide", "log
  base", "database de conversaciones".

---

## Core Concepts

### 1. Universal Knowledge Base (UKB)

A single, versioned, auto-evolving Markdown file at
`docs/team/knowledge-base/UNIVERSAL-KNOWLEDGE-BASE.md`.

It is organized in **numbered sections (§N)**:

| Section | Content |
|---------|---------|
| §0 | Meta-structure: schema version, section index, contributor list |
| §1 | Verdades Universales — validated, immutable conclusions |
| §2 | System architecture (endpoints, ports, stack) |
| §3 | Active integrations |
| §4 | Run history summary |
| §5 | Team decisions with justification |
| §6 | Critical pending items |
| §7 | Team glossary |
| §8 | Contribution & evolution protocol |
| §N | New domain added by agents as needed |

### 2. Knowledge Evolution Log (KEL)

An append-only companion log at
`docs/team/knowledge-base/KNOWLEDGE-EVOLUTION-LOG.md`.

Every structural change to the UKB (new section, schema version bump, new
truth, deprecation) is recorded here. The KEL is the **audit trail of how
the knowledge base itself has evolved**.

### 3. Pristine Conclusion

A finding or insight from an agent that has been validated and elevated to
a Verdad Universal (§1). Requirements:
- High-confidence (repeatable, verified by code or evidence).
- Cited with the validating agent and date.
- Reviewed by Judge or Orchestrator before being marked `Alta` confidence.

### 4. Auto-Evolution

The UKB is **not static**. Any agent can:
- Add a new §N section when a new knowledge domain is needed.
- Add entries to existing sections.
- Deprecate outdated entries (with `~~strikethrough~~` and a note).

The only invariant: **never delete validated entries** — deprecate instead.

---

## Workflow

### Reading the UKB (start of any task)

1. Open `docs/team/knowledge-base/UNIVERSAL-KNOWLEDGE-BASE.md`.
2. Read §1 (Verdades Universales) and any section relevant to your task.
3. If a truth contradicts what you observe, note it as a candidate update —
   do not silently ignore the discrepancy.

### Recording a Pristine Conclusion

1. Append a new row to §1 with confidence `Media`.
2. Add a row to `KNOWLEDGE-EVOLUTION-LOG.md` with type `TRUTH`.
3. Notify the Judge or Orchestrator via `LIVE-LOG-CENTER.md`:
   ```
   | YYYY-MM-DD HH:MM:SS | [YourRole] | HANDOFF | → Judge: new UKB truth candidate T00N ready for validation. |
   ```
4. Judge reviews and updates confidence to `Alta` or removes the entry.

### Adding a New Section

1. Identify the new knowledge domain (must not fit any existing §).
2. Append `## § N · [Descriptive Name]` to the UKB (N = next integer).
3. Update §0 "Secciones activas" row in the UKB.
4. Bump `schema-version` in the UKB front-matter if the section is a major
   structural addition (e.g., 1.0 → 1.1).
5. Record in KEL with type `STRUCTURE`.

### Deprecating an Entry

1. Wrap the entry text in `~~strikethrough~~`.
2. Add an inline note: `*[Deprecada YYYY-MM-DD: reason]*`.
3. Record in KEL with type `DEPRECATE`.

### Resolving a Pending Item (§6)

1. Mark the row in §6 with `[x]` and add a "Resolved on YYYY-MM-DD" note.
2. Record in KEL with type `RESOLVED`.

---

## Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Universal Knowledge Base | `docs/team/knowledge-base/UNIVERSAL-KNOWLEDGE-BASE.md` | Auto-evolving team memory |
| Knowledge Evolution Log | `docs/team/knowledge-base/KNOWLEDGE-EVOLUTION-LOG.md` | Append-only structural change log |
| Skill | `.cursor/skills/bmc-universal-knowledge/SKILL.md` | This file |
| Quick reference | `.cursor/skills/bmc-universal-knowledge/reference.md` | Schema cheat-sheet |

---

## Agent Responsibilities

| Agent | Responsibility |
|-------|---------------|
| **All agents** | Read UKB at task start; add pristine conclusions to §1 candidates |
| **Judge** | Review §1 candidates; elevate to `Alta` or reject |
| **Orchestrator** | Seed new runs from UKB context; record run in §4; coordinate UKB updates |
| **Universal Knowledge** *(this skill)* | Manage schema evolution; guide other agents on format; ensure KEL is updated |
| **Live Comms** | Notify agents of new UKB entries via `LIVE-LOG-CENTER.md` |
| **Fiscal** | Supervise that agents actually read and contribute to UKB (protocol compliance) |

---

## Rules

- **Never delete validated entries** — deprecate with `~~text~~` instead.
- **Always cite the source:** validating agent + date for every entry.
- **No secrets:** never log credentials, tokens, or sensitive data.
- **Append-only for §1:** Verdades Universales are immutable once marked `Alta`.
- **Schema versioning:** bump `schema-version` in §0 front-matter when adding
  a new section or making breaking structural changes.
- **KEL is append-only:** never edit past KEL entries.

---

## Reference

- Quick reference schema: [reference.md](reference.md)
- Live communication log: `docs/team/live-comms/LIVE-LOG-CENTER.md`
- Project state: `docs/team/PROJECT-STATE.md`
- Judge evaluation: `docs/team/judge/JUDGE-CRITERIA-POR-AGENTE.md`
- Orchestrator: `.cursor/agents/bmc-dashboard-team-orchestrator.md`
