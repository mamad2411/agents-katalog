---
name: study
description: >
  Use this skill whenever the user wants to run the full Reliquery pipeline — processing
  content into the vault and committing it to memory in one seamless operation. Trigger when
  the user says "study this", "study the latest chapter", "study this conversation",
  "process and memorize", "full pipeline", "chronicle and memorize this", or any phrasing
  that implies both content extraction AND memory indexing in one pass. Also trigger when
  the user attaches a manuscript, session log, chat export, or scene draft and wants the
  full treatment — not just vault storage but searchable, recallable memory. Study is the
  default when the user's intent is "make the system learn this." When in doubt, trigger
  study rather than chronicle alone — study includes chronicle and extends it.
---

## Identity

Study is the orchestrator — the master pipeline that chains chronicle, memorize, cartograph, and forget into a single coherent operation. Where the individual skills each handle one stage of the Reliquery lifecycle, study handles the *intent*: "I have content, and I want the system to learn it."

Study's disposition is efficiency without shortcuts. It moves through the pipeline briskly, collapsing unnecessary pauses between stages while preserving every checkpoint that protects the user's world. It recognizes when a step can be skipped (no new relics to index, KG already up to date) and says so rather than running empty phases. It recognizes when a step needs to be added (stale drawers that should be forgotten before re-indexing) and offers it seamlessly.

The user should never have to think about which skill to invoke or in what order. Study handles the routing.

---

## How Study Works

Study operates in three stages that map to the underlying skills, with decision points between them that determine whether to continue, branch, or stop.

```
Content → [Chronicle] → Relics → [Memorize] → Drawers → [Cartograph offer] → KG
                                       ↑
                              [Forget if needed]
```

The user provides content and an intent. Study figures out the rest.

---

## Stage 1 — Intake & Memory Check

Before invoking chronicle, study performs its own reconnaissance to understand what the system already knows and what's actually new.

### 1a — Load the palace
Call `mempalace_status` to confirm the system is live and identify the relevant wing.

### 1b — Scan the input
Read the user's provided content (manuscript excerpt, session log, conversation, scene draft) and identify every named entity: characters, factions, locations, systems, events.

### 1c — Memory check
For each identified entity, run dual lookups in parallel:
- `mempalace_search(query="[entity]", wing="[wing]")` — what drawers exist
- `mempalace_kg_query(entity="[entity]")` — what the KG knows

This is not just chronicle's Phase 1 entity scan — it's a broader assessment of the system's current knowledge state relative to what the user just handed over. The goal is to answer: "What in this content is genuinely new, what updates existing knowledge, and what's already fully covered?"

### 1d — Triage report

Present a brief triage to the user before proceeding:

- **New entities** — not in the vault or palace at all. These need full chronicle treatment.
- **Updated entities** — already have relics and/or drawers, but the new content changes their state, relationships, or situation. These need relic updates and drawer updates. Apply chronicle's arc-first filing philosophy: most session-to-session changes belong in arc/state-level relics, not individual entity files.
- **Unchanged entities** — already well-covered. These can be skipped unless the user says otherwise.
- **Stale entries detected** — if existing drawers contain content that the new material contradicts or supersedes, flag this and offer to run `/forget` on the stale entries before proceeding.

Ask: "This is what I'm seeing. Want me to proceed with the new and updated entities, or adjust the scope?"

**Do not proceed until the user confirms the triage.**

---

## Stage 2 — Chronicle

Once the triage is confirmed, run chronicle for the entities in scope. Study invokes chronicle's phases directly rather than triggering the skill as a separate operation — the context is already loaded.

### 2a — Entity extraction & gap analysis
Chronicle Phase 2 and 3 — identify what needs relics, cross-reference against vault files on disk.

### 2b — Outline checkpoint
Chronicle Phase 4 — present the relic plan (new relics, updates, skips) for approval. Since study already performed the triage in Stage 1, this checkpoint can be lighter: confirm the plan matches the agreed scope, flag anything surprising, move on.

### 2c — Generate, review, commit
Chronicle Phases 5–7 — generate relics in staging, present for review, backup existing files, commit to vault on approval.

**Transition logic**: Once relics are committed, study does not pause and ask "want to memorize these?" — it transitions automatically to Stage 3. The user already expressed the intent for the full pipeline by invoking study. If they only wanted chronicle, they would have called `/chronicle` directly.

---

## Stage 3 — Memorize

With fresh relics committed to the vault, study runs memorize on the just-committed files.

### 3a — Existing drawer discovery
Memorize Phase 2 — check what the palace already holds for each committed relic. Classify as new index, minor update, or major rewrite.

**If major rewrite is detected**: Study handles this seamlessly by invoking forget on the stale drawers before proceeding with the new index. Present the forget scope to the user for confirmation (forget's confirmation gate still applies — irreversible deletions always require explicit approval), then continue.

### 3b — Index plan checkpoint
Memorize Phase 3 — present the drawer plan. Since the relic content was just approved in Stage 2, this checkpoint focuses on chunking decisions and update-vs-new classification rather than re-reviewing content.

### 3c — Index execution & verification
Memorize Phases 4–5 — file drawers, verify retrieval.

### 3d — Knowledge graph offer
Memorize Phase 6 — check whether the indexed relics contain unmapped relationships. If they do, offer to run cartograph.

**If the user accepts the cartograph offer**, transition into cartograph Phase 2 (Design) — the survey is already done. Present the triple plan, get approval, execute, verify.

**If the user declines**, wrap up.

---

## Wrap-up

After the final stage completes (memorize, or cartograph if accepted), report:

- **Relics committed**: count, with file names and vault locations
- **Drawers filed**: count, broken down by created vs. updated
- **KG triples added** (if cartograph ran): count
- **Stale entries cleaned** (if forget ran): count

Then the reload reminder:

> ⚠️ **Restart Claude** (for Desktop: exit from the system tray, then relaunch) for all changes to take effect in future sessions.

---

## Lightweight Mode — Conversation Study

When the user says "study this conversation" or "study what we just discussed," the input isn't a manuscript — it's the conversation itself. Study adapts:

1. **Scan the conversation context** for load-bearing lore: decisions made, facts established, relationships introduced or changed, status updates, new concepts.
2. **Filter out noise**: meta-discussion, debugging, questions about how the system works, and other non-lore content. Only extract what belongs in the vault.
3. **Present the triage** as normal — what's new, what updates existing knowledge, what's already covered.
4. **Proceed through the pipeline** at the same pace, with the same checkpoints.

The key difference is source material quality. A manuscript is authored, deliberate, and structured. A conversation is messy, exploratory, and may contain speculative ideas the user hasn't committed to. Study should flag anything that feels speculative: "You mentioned [concept] as a possibility — should I treat this as established lore or leave it out for now?"

---

## When Study Calls Other Skills

| Condition | Action |
|-----------|--------|
| New content needs to become relics | Run chronicle stages |
| Committed relics need to become searchable | Run memorize stages |
| Existing drawers are stale/contradicted | Run forget (with confirmation gate) before re-indexing |
| Indexed relics have unmapped relationships | Offer cartograph |
| User asks how the system works mid-pipeline | Answer directly — don't invoke reliquery-help as a separate skill |
| Nothing is genuinely new in the content | Say so at triage and stop — don't run empty phases |

---

## What Study Does Not Do

- **Skip checkpoints.** Study is faster than running skills individually because it shares context across stages, not because it removes approval gates. Every irreversible action still requires confirmation.
- **Run empty phases.** If the triage shows nothing new and nothing stale, study says "the system already knows this" and stops.
- **Assume cartograph is always needed.** The KG offer happens only when unmapped relationships are detected. Simple factual relics (locations with no relationships, standalone concepts) don't trigger it.
- **Conflate "speculative" with "established."** Content from conversations gets extra scrutiny. Study asks before treating exploratory ideas as canon.
