---
name: accessibility-diff
description: "Compares accessibility findings between explicit revisions without disturbing the active checkout. Use when checking regressions against a baseline."
---

# Accessibility comparison

Read AGENTS.md and the repository's docs for scan targets, baseline policy and isolated
preview commands. Use [accessibility-scan](../accessibility-scan/SKILL.md) to
capture the same page states on both revisions.

1. Record requested base and candidate revisions, active branch and dirty state.
   Preserve the active checkout. Capture an existing trusted baseline if its
   revision and scenario match; otherwise create a disposable worktree/clone for
   the explicit baseline revision. Never stash or switch the user's working tree.
2. Give isolated previews distinct ports and data. Use the configured supervisor;
   verify process ownership before scanning or stopping it. Missing prerequisites
   mean an explicit incomplete comparison, not permission to reset local data.
3. Normalize findings by rule, component/target and page state. Report introduced,
   resolved and unchanged violations. Dynamic IDs alone do not establish change.
4. Stop only processes started for this comparison and remove only disposable
   resources created for it, including after failure. Preserve evidence and
   original checkout state. A comparison request does not authorize fixes or
   changing the stored baseline.
