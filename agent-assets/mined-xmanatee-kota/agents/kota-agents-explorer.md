# Explorer Workflow

This directory contains the explorer workflow definition and prompt.

- This workflow owns online research into relevant systems and practices when
  the local queue is empty or thin. The watchlist helps discovery; it does not
  define or limit the research agenda.
- Inspect local context to evaluate external ideas, not to replace research with
  gardener's local cleanup, progress-reviewer's systemic learning, or improver's
  incident investigation.
- Write research leads to `data/inbox/`, grounded research or adoption tasks to
  `data/tasks/`, and evolving sources to `data/watchlist.yaml`. Inbox leads need
  not already justify implementation. Preserve sources and open questions.
- Verify the selected harness can actually search and retrieve online material;
  report unavailable research capability rather than claiming offline work as research.
- Keep this workflow focused on high-leverage external discovery, meaningful
  future work selection, and strategic range.
- Keep tasks outcome-focused and concise. This workflow owns the queue contract,
  not the implementation plan.
- A healthy queue should not collapse into one repeated kind of local work.
- Treat the inspect step's queue counts and availability fields as context for
  the exploration decision; task validation and writer integration own the
  hard gates.
- Record exploration completion in the run artifact. The canonical cooldown is
  advanced by the original run's success finalizer through runtime
  compare-and-set, after any repository changes integrate.
- Its unbounded repair loop contributes the inspected queue and watchlist to
  the shared continuation authority. Because explorer has no task-decomposition
  consumer, a split or deferral preserves and yields the same run lineage.
- Keep watchlist summaries factual: record the relevant current state observed
  from a source, not an adopt/reject/defer policy verdict. Durable external
  pattern verdicts live in the typed
  `src/modules/autonomy/external-pattern-decisions.ts` catalog, which remains
  outside explorer's write scope and is curated separately.

The watchlist holds evolving sources with a reason to revisit in their notes;
one-off references belong in existing task or decision records. Prefer a project's
release or research-series surface when it covers the same development, without
treating that replacement as a redirect or copying the old source's snapshot.
Daily rechecks are the default; weekly suits slower research and specifications.
Access failures follow the same cadence and preserve the source for recovery.
Source rechecks are deterministic reads through the normal web tool boundary.
Queue demand admits discovery through the existing cooldown; unchanged or
unavailable watchlist content cannot veto independent research. The last actual
review consumes a fingerprint of observed source content, watchlist intent and
task intent to distinguish settled material from new leads. Exhausted known
leads call for a different investigation direction, not repeated review of the
same material or fabricated tasks. Time alone does not create queue demand.
Failed fetches, including unavailable readable content, preserve the last useful
content identity. Page metadata and layout markup are access evidence, not
upstream product changes. Observations and reviewed fingerprints publish
through the same finalizer, including no-action.
A changed task context can reuse readable retained material before its network
recheck is due or after a later fetch fails. Retained references preserve their
original observation time; absent or mismatched bytes cannot establish access.
One unavailable source does not veto independent research using readable sources.
Source content and failures stay in retained run evidence after sandbox cleanup;
the agent receives working copies inside its authorized run directory.

Author watchlist changes directly in YAML, preserving operator values, comments,
and untouched snapshots. Repair and integration publication validate the complete
watchlist and task files without rewriting them. YAML uses the parser's bounded
alias handling; invalid syntax, domain values, and conflicting source identities
fail at those boundaries. Runtime source evidence remains
the authority for content fingerprints and review cooldowns.
