---
name: cartograph
description: >
  Use this skill whenever the MemPalace knowledge graph needs to be populated, expanded, or
  restructured from vault content. Trigger when the user says "cartograph", "map the KG",
  "build the knowledge graph", "add triples", "populate the graph", "map relationships",
  "chart the connections", "who connects to whom", or "seed the KG for X". Also trigger
  when the user asks to plan KG triples for a character, faction, arc, or concept — even
  if they phrase it casually like "let's get [entity] into the knowledge graph" or "can you
  figure out the relationships for [entity]". Trigger when a chronicle or memorize pass has
  added new relics and the user wants those entities reflected in the KG. Trigger when the
  user wants to audit, verify, or test-query existing KG data. When in doubt, trigger: this
  skill handles any task where vault content needs to become structured, queryable knowledge
  graph triples.
---

## Identity

Cartograph is the relational mapping layer of Reliquery. Where memorize indexes relic *content* into searchable drawers, cartograph indexes relic *relationships* into queryable graph triples. The two are complementary — drawers give Claude prose and flavor, the KG gives Claude structured facts and temporal state. Together they form the complete memory of a world: what things *are* and how they *connect*.

Cartograph approaches the knowledge graph the way a cartographer approaches unmapped territory — survey first, chart second, verify third. Every triple it proposes has been cross-referenced against vault content. Every triple it files has been reviewed by the user. The KG is the authoritative record of what is currently true in a world; carelessness here means Claude acts on bad facts in future sessions.

---

## When to Use Cartograph vs. Other Skills

| Situation | Skill |
|-----------|-------|
| Raw content → structured relics | **Chronicle** |
| Relics → searchable drawers | **Memorize** |
| Entity relationships → KG triples | **Cartograph** |
| Palace drawers need to be deleted | **Forget** |
| Full pipeline: content → relics → memory → KG | **Study** |

---

## Phase 1 — Survey

Search the vault for everything relevant to the target entity. Build a complete picture before designing any triples.

**How to search:**
1. Direct name search: `mempalace_search(query="[entity]", wing="[wing]", limit=10)`
2. Temporal history: `mempalace_kg_timeline(entity="[entity]")` — review the entity's existing relationship timeline before proposing new triples. This prevents duplicates, reveals invalidated facts that shouldn't be re-added, and surfaces temporal gaps worth filling.
3. Follow the threads — every connected entity in the results gets a follow-up search
4. Relationship-specific queries: `"[entity] [connected entity] relationship"`, `"[entity] motivations goals"`
5. Typical scope: 3–6 searches for a single character, 5–10 for a major arc or faction

**What to extract:**
- Named relationships (allies, enemies, handlers, mentors, family)
- Organizational affiliations (factions, roles, departments)
- Status facts (alive, dead, missing, transformed)
- Identity links (aliases, codenames, true identities)
- Temporal markers (when relationships started, ended, changed)
- Narrative state (what's happening now, what's unresolved)
- Mystery flags (unknown connections, foreshadowing, unrevealed links)

**Checkpoint**: "I've surveyed [N] sources and found [summary]. Ready to design the triples, or should I dig deeper?"

---

## Phase 2 — Design

Translate survey findings into a structured triple plan.

### Entity Naming

Full canonical names as identifiers. Consistency is critical — the same entity must always use the same string.

- **Characters**: `Sera Voss`, `Aldric Thane`
- **Factions**: `The Iron Council`, `Pale Archive`
- **Locations**: `Duskhollow`, `The Thornveil`
- **Concepts**: `Project Helix`, `the tribunal system`

Aliases and codenames get their own identity-linking triples rather than being used as primary names.

### Predicate Vocabulary

See `references/predicate-vocabulary.md` for the canonical list, direction conventions, and extension rules. Core categories: Identity, Status, Organizational, Interpersonal, Personal, Conflict, Narrative, Ability & Assets.

Consistency matters more than expressiveness. `member_of` used everywhere beats a mix of `member_of`, `belongs_to`, and `part_of`.

### Temporal Dating

- Use `valid_from` when the story establishes a clear start point
- Use approximate dates (YYYY-01-01) when exact timing isn't established
- Omit `valid_from` entirely when ambiguous — dateless beats guessed
- `valid_to` is set later via `kg_invalidate`, not during initial seeding

### KG vs. Drawers

| KG (triples) | Drawers (search) |
|---|---|
| `Sera → status → alive` | Physical description, demeanor, voice |
| `Sera → member_of → The Iron Council` | Background story, motivations, fears |
| `Sera → rival_of → Aldric` | The texture of their rivalry, dialogue |
| `Duskhollow → controlled_by → The Iron Council` | Sensory atmosphere, architecture |

Rule of thumb: "Would I query this by entity name and want a structured answer?" → triple. "Would I read this when writing a scene?" → drawer.

### Triple Plan Format

Present as grouped markdown tables:

```
| # | Subject | Predicate | Object | valid_from |
|---|---------|-----------|--------|------------|
| 1 | Sera Voss | member_of | The Iron Council | 2024-01-01 |
```

Include **expansion notes** listing entities or domains not covered in this batch.

**Checkpoint**: Present the full plan. Flag uncertain predicate directions, total count, category breakdown, and suggested expansions. Wait for approval.

---

## Phase 3 — Pre-flight

Run `mempalace_kg_stats` for a baseline — entity count, triple count, relationship types.

If the KG already has triples:
- `mempalace_kg_query` on key affected entities to check for conflicts or duplicates
- `mempalace_kg_timeline` on entities with temporal complexity (characters who change allegiance, factions that evolve, events with distinct phases) to verify the proposed triples don't collide with existing temporal records or re-add facts that were intentionally invalidated

---

## Phase 4 — Execute

Batch-execute approved triples via `mempalace_kg_add`.

**Rules:**
- Fire calls sequentially — the MCP server can timeout under rapid parallel load
- On timeout: pause, `mempalace_kg_stats` to check landed count, resume from last unconfirmed
- On directional error: immediately `kg_invalidate` the wrong triple, `kg_add` the corrected version
- Track progress every ~15 calls
- Never silently skip a failed triple

**Checkpoint**: Run `mempalace_kg_stats`, compare to pre-flight. Report triples added (expected vs. actual), new entities, new relationship types, any expired facts from fixes.

---

## Phase 5 — Verify

Run demonstration queries:

1. **Entity query**: `kg_query("[main entity]")` — full relationship web
2. **Incoming query**: `kg_query("[faction]", direction="incoming")` — all members/affiliates
3. **Timeline**: `kg_timeline("[main entity]")` — chronological progression
4. **Temporal snapshot** (if applicable): `kg_query("[entity]", as_of="[date]")` — facts valid at that point

Present results as proof the data is queryable and correct.

> ⚠️ **Restart Claude** (for Desktop: exit from the system tray, then relaunch) for KG changes to take effect in future sessions.

---

## Error Recovery

**MCP timeout**: Wait 10–15 seconds, `mempalace_kg_stats` to check state, resume from last unconfirmed triple.

**Duplicate triples**: `kg_add` does not auto-deduplicate. Query the entity first if uncertain. Duplicates are messy but not harmful.

**Character encoding**: Accented characters may display as escaped Unicode in results. Cosmetic — the KG handles them correctly.

---

## Expansion Patterns

A single session typically covers one character's immediate web (30–50 triples). Plan future batches for faction rosters, location control, arc state, system/concept entities, and historical events. Reuse established predicates; note new ones in the reference doc.

---

## Integration

**After Chronicle**: New relics should have their relationships mapped. Chronicle captures content; cartograph captures connections.

**After Memorize**: Memorize offers to invoke cartograph after committing drawers, if indexed relics contain unmapped relationships.

**After Forget**: Forget offers to invoke cartograph for KG cleanup when drawers are deleted.

**During co-writing**: Apply approved `<!-- CHANGELOG -->` changes via `kg_add` and `kg_invalidate` directly — no full survey needed.

---

## Tools Used

| Tool | Phase |
|------|-------|
| `mempalace_search` | 1: Survey |
| `mempalace_kg_stats` | 3 & 4: Baseline and verification |
| `mempalace_kg_query` | 3: Conflict check; 5: Verification |
| `mempalace_kg_add` | 4: Execution |
| `mempalace_kg_invalidate` | 4: Fixes; ongoing: retiring facts |
| `mempalace_kg_timeline` | 1: Survey history; 3: Temporal conflict check; 5: Verification |
