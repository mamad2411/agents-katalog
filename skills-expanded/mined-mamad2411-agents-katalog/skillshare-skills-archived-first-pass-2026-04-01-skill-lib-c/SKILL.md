# One-Shot Prompt

Use this as a standalone prompt when you want a quick audit without
installing the full skill. Paste it into a new conversation along with
your skill list or directory path.

---

```text
Audit my skill library and produce a rationalization plan.

Read every skill in my library. For each skill, extract: name, purpose
(one sentence), trigger contexts, tools/scripts used, reference file
count, and freshness signals.

Before comparing skills for similarity, map their relationships:
- Designed pairs (skills built to complement each other — NEVER merge these)
- Override chains (user skill supersedes a public/default skill)
- Command bindings (skills bound to slash commands)
- Dependency clusters (skills that reference each other)
- Platform scope (skills targeting different environments)

Then cluster by functional similarity. Two skills are merge candidates
only if they share the same job, same core workflow, AND same output type.
Trigger word overlap alone is a routing collision, not a merge signal.

For every skill, assign exactly one action:
- KEEP — distinct, healthy, well-routed
- KEEP+REWRITE — valuable but structurally weak or stale
- MERGE INTO [target] — same job as another; combine best parts (confidence ≥ 0.75)
- ARCHIVE — superseded but may have recoverable value (confidence ≥ 0.50)
- REMOVE — exact duplicate, broken, or empty (confidence ≥ 0.90)
- SPLIT — one skill hiding 2+ distinct jobs
- FIX TRIGGERS — healthy skill with a description/routing problem

Safeguards:
- Never remove the only skill serving a niche task
- Never merge designed pairs or complementary skills
- Never merge skills bound to different slash commands
- Prefer archive over remove when uncertain
- Flag staleness (obsolete model refs, deprecated tools, missing FEEDBACK.md)
  but don't auto-remove based on staleness alone
- Flag bloat (SKILL.md > 500 lines with no references, 3+ distinct jobs
  in one skill) and recommend splitting

Output in this order:
1. Executive summary (counts, proposed end-state size)
2. Relationship map (pairs, overrides, commands, dependencies)
3. Inventory table (skill, category, action, reason, confidence)
4. Merge proposals (what each source contributes, canonical result)
5. System prompt impact (routing table changes, command rebindings)
6. Migration checklist (ordered steps with rollback notes)

Be conservative. A false merge destroys more value than keeping an extra
skill. When uncertain, ask rather than deciding.
```
