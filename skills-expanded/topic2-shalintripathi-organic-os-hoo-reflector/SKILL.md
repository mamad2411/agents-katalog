---
name: hoo-reflector
description: Use to distill lessons from recent signals and outcomes - "run the reflector", weekly routine step 4, or "what did we learn". Proposes skillbook deltas; the curator merge is gated.
---

# Reflector (weekly) - propose deltas, never write directly

1. Read: all signals/ since the last reflection, outcomes/ records, current
   skillbook.md, the last reflections/ file.
2. Propose deltas, each referencing an entry ID or NEW:
   - NEW lesson (with evidence tag + source: which signal/outcome proves it)
   - `S-nnn helpful+1` / `harmful+1` (an outcome confirmed/contradicted it)
   - `S-nnn deprecate` (contradicted repeatedly - cite the evidence)
   - `S-nnn edit: <new text>` (sharpen wording; meaning preserved)
   NEVER propose a full rewrite. NEVER propose deleting lines.
3. Write reflections/YYYY-Www.md listing every delta + evidence.
4. Stale review: list the entries whose last-confirmed date has aged past
   their evidence tier's threshold.
   `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -c "..."` snippet calling
   `core.contracts.skillbook_stale(<brain>)`, which returns
   `{id, evidence, last_confirmed, days_stale, threshold, text}` per entry,
   most stale first. Thresholds by tier: anecdotal 90 days, moderate 180,
   strong 365 (canonical in `core.contracts.STALE_DEFAULTS`; a site can
   override any tier with `skillbook: {stale_days: {...}}` in
   site-profile.yaml). Deprecated entries never appear here.
   Present each one for re-validation next to the evidence from this
   week's signals and outcomes that would confirm or contradict it:
   - Re-confirmed (the lesson still holds): propose it as a delta applied
     through `skillbook_update(root, "S-nnn")`, which stamps
     last-confirmed to today. That refresh is the point of the review.
   - Cannot be re-confirmed: PROPOSE deprecation as a delta, citing what
     is missing. The reflector NEVER auto-deprecates and never writes the
     book on its own - a stale entry is a question for a human, not a
     verdict, exactly like every other delta in step 2.
   An entry nobody can speak to this week is left as it is and listed
   again next week. Age is a prompt to re-check, never a reason to delete.
5. Curator merge: if the profile marks curator as gated (default), present the
   deltas for approval (in-session or channel); on approval apply each via
   `skillbook_append` / `skillbook_update` calls - one call per delta.
6. Commit "reflection: YYYY-Www" if git.
