---
name: persistent-memory-stack
description: Five-layer Willow memory model — flat-file boot, intake, KB, SOIL, handoff — with write rules and promotion paths.
---

@markdownai v1.0

# Persistent memory stack

Five layers, innermost to outermost. Each layer has a distinct write rule and lifecycle.

---

## Layer 1 — Flat-file boot context

**Where:** `$WILLOW_HOME/session_anchor_<agent>.json`, `willow.md` (`~/github/.willow`; `~/.willow` alias OK)  
**Purpose:** Cold-start baseline. Readable without MCP, Postgres, or network.  
**Write rule:** Written by session close hooks and `handoff_rebuild`. Do not write ad-hoc.  
**Lifecycle:** Overwritten each session. Authoritative only when nothing else is reachable.

---

## Layer 2 — Intake

**Where:** `$WILLOW_HOME/intake/<agent>/YYYY-MM-DD.jsonl`  
**Purpose:** Annotated staging area. Every agent, tool, and script writes here first.  
**Write rule:** Use `intake_write` (MCP) or `core/intake.py` (direct). Never write directly to `knowledge` or `jeles_atoms` from ad-hoc code.  
**Lifecycle:** Records sit here until norn-pass promotes them. Promoted records are marked `promoted=true`. Staging files are not deleted — they are the audit trail.

Schema: `{id, content, title, source, agent, tier, confidence, keywords, tags, created_at, promoted, promote_tier}`

Intake tiers:

| Tier | Meaning |
|------|---------|
| `observed` | Raw session fact, unverified |
| `fetched` | Retrieved from an external source |
| `verified` | Checked against trusted source (Jeles or human) |
| `ratified` | Human-confirmed via Binder |

---

## Layer 3 — KB (Knowledge Base)

**Where:** Postgres — `knowledge`, `jeles_atoms`, `opus.atoms`  
**Purpose:** Promoted, durable, fleet-wide facts.  
**Write rule:** Via norn-pass (`promote_intake.py`) or trusted promotion paths only. `infer_7b classify` routes each record to the right sub-tier.  
**Lifecycle:** Bi-temporal. Records gain `valid_at` / `invalid_at`. Superseded atoms are not deleted — they are closed with `invalid_at`.

Sub-tiers:

| Table | When |
|-------|------|
| `jeles_atoms` | External citation exists, `relevance_score >= 0.5` |
| `knowledge` | Stable fleet fact, verified, `confidence >= 0.80` |
| `opus.atoms` | Opus-tier synthesis, high-signal cross-domain |
| Binder queue | Low confidence or needs human review |

---

## Layer 4 — SOIL

**Where:** Local structured records on disk (`$WILLOW_HOME/store/` or collection path)  
**Purpose:** Session-scoped or fast-changing state that doesn't belong in Postgres yet.  
**Write rule:** Use `soil_put` / `soil_update`. Graduate stable facts to KB when they stabilize.  
**Lifecycle:** Not automatically promoted. Agent is responsible for graduating or expiring SOIL records.

---

## Layer 5 — Handoff

**Where:** `$WILLOW_HOME/handoffs/<agent>/session_handoff-<date>_<agent>.md`  
**Purpose:** Sealed session document. What the next agent needs to resume without asking the user to repeat context.  
**Write rule:** Written at session close. Indexed via `handoff_rebuild`. A handoff with no open threads is incomplete. A handoff with no capability table is incomplete.  
**Lifecycle:** Immutable after write. Superseded by the next session's handoff, not deleted.

---

## Write decision tree

```
Is this a fleet-wide stable fact?
  → Yes: intake → norn-pass → KB
Is this session-scoped or fast-changing?
  → Yes: SOIL (graduate to KB when stable)
Is this a human-confirmed file or edge?
  → Yes: Binder (mem_binder_file / mem_binder_edge / mem_ratify)
Is this a Nest drop (human filed a document)?
  → Yes: intake at tier=verified, confidence=1.0
What does the next agent need to resume?
  → Handoff
```

---

*See also: [`willow.md` — Persistent memory section](../../../willow.md)*
