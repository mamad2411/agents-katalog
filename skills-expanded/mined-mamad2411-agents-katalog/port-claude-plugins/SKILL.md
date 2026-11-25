---
name: port-claude-plugins
description: Triggered when the user asks to reconcile or port Claude or Codex plugin changes into Antigravity. Starts a read-only semantic ledger campaign and stops for an explicit operator decision.
---

# Reconcile Claude and Codex Plugin Semantics

Use a committed semantic port ledger. Do not begin with file copying, path
heuristics, or implementation planning.

## Safety boundary

- Read local `HEAD` and local `origin/main` only. Do not fetch, pull, checkout,
  update refs, or write either sibling repository.
- Stop if Claude or Codex `HEAD` differs from local `origin/main`.
  Antigravity may be on a feature branch: record its `HEAD` separately, bind
  its inventory and drift comparison to local `origin/main`, and never treat
  feature-branch implementation files as source candidates.
- Write only the explicitly named campaign output beneath
  `docs/ports/<campaign-id>/`.
- Do not write an installed-plugin root, user configuration, host state, or a
  source repository.
- Ranking is advisory. Never approve, reject, hide, or select a candidate from
  its scores.
- Before the operator decision, do not create migration units, estimates,
  dependency order, implementation sequence, code changes, or outcome edges.
- Do not invoke `scripts/port_claude_plugin.py`. It is a legacy destructive
  bulk-copy utility, not a normal campaign entry point.

## Workflow

1. **Pin the local snapshots.**

   Record the planning and inventory commits for Claude, Codex, and
   Antigravity. Claude and Codex inventory their matching local `HEAD` and
   `origin/main`; Antigravity inventories local `origin/main` while retaining
   its feature `HEAD` as implementation context. Record the selected plugin
   and shared-tool surfaces. Treat a historical sync commit only as a history
   seed.

2. **Obtain a promotable host-capability receipt.**

   Use the fleet-core capability doctor through its safe observation
   interface. Bind the ledger only to the receipt digest, catalog digest, and
   sanitized capability ID/state pairs. Never copy paths, hostnames,
   transcripts, or private diagnostic values into the ledger.

3. **Run read-only discovery.**

   The canonical command is:

   ```bash
   python3 scripts/port_ledger.py discover \
     --campaign-id <campaign-id> \
     --output docs/ports/<campaign-id>/ledger.yaml \
     --claude-seed <full-commit> \
     --claude-planning-snapshot <full-commit> \
     --codex-planning-snapshot <full-commit> \
     --antigravity-planning-snapshot <full-commit> \
     --host-receipt <promotable-receipt.json> \
     --checked-at <iso-8601-time>
   ```

   Discovery reconciles the Claude history delta with complete current-tree
   manifests for all three repositories. It emits normalized edit packets and
   discloses unmatched drift. It does not classify semantic value.

4. **Curate stable candidates.**

   Group every edit packet under exactly one stable capability ID. Bind each
   candidate to exact packet IDs and exact provenance. Record its semantic
   contract, adjacent dependencies, current Antigravity state, proposed
   disposition, four ranking inputs, later evidence expectation, and pending
   decision. Pending rows still explain the maintainer's advisory rationale
   and a concrete revisit trigger, but record no operator or decision time.
   Repeated edits for one behavior remain evidence under one candidate.

5. **Validate and report the pending inventory.**

   ```bash
   python3 scripts/port_ledger.py validate --inventory-only \
     docs/ports/<campaign-id>/ledger.yaml
   python3 scripts/port_ledger.py report \
     docs/ports/<campaign-id>/ledger.yaml
   ```

   Inventory-only validation may pass with pending decisions, but it must fail
   for missing packets, duplicate ownership, unmatched drift, incomplete
   ranking or rationale fields, unsafe provenance, or incomplete receipt and
   snapshot disclosure. Plain validation must remain nonzero while any
   candidate is pending.

6. **Stop for the operator.**

   Present the complete report, including every low-ranked, rejected,
   metadata-only, superseded, or blocked recommendation. Ask the operator for
   one explicit complete mapping over the current candidate ID set. Approval
   of a plan or workflow does not approve candidates.

7. **Record only the complete mapping.**

   After the operator supplies every candidate state, rationale, and revisit
   trigger, apply that exact mapping:

   ```bash
   python3 scripts/port_ledger.py record-decisions \
     docs/ports/<campaign-id>/ledger.yaml \
     <complete-decision-mapping.yaml> \
     --operator <operator-identity> \
     --decided-at <iso-8601-time>
   python3 scripts/port_ledger.py validate \
     docs/ports/<campaign-id>/ledger.yaml
   ```

   Reject partial, extra, or stale candidate IDs. Decision recording does not
   create or schedule migration work.

8. **Refresh before release use.**

   Repeat read-only discovery against matching Claude and Codex local `HEAD`
   and local `origin/main`, plus Antigravity local `origin/main` with its
   feature `HEAD` recorded separately. Preserve stable candidate ownership,
   disclose new unmatched packets, and compare existing decisions with the
   refreshed snapshots, packet content identities, selected surfaces, and
   required host-capability evidence. A byte-identical evidence refresh keeps
   existing decisions. Any changed snapshot or semantic input returns each
   affected decided candidate to `pending` and requires the operator gate
   again, even when candidate and packet IDs remain unchanged.

The campaign README is the human runbook and `ledger.yaml` is the canonical
decision authority. Later migration work consumes only the fully decided stable
candidate IDs.
