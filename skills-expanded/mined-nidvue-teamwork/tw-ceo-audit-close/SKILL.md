---
name: tw-ceo-audit-close
description: "when the queue is empty and loop is about to report STOP: verify the chain, the gates and the archive, export the audit manifest, and report from records"
kind: workflow
---

# tw-ceo-audit-close

Owner role: **ceo** (created by CEO on 2026-10-19).

Use this skill when: when the queue is empty and loop is about to report STOP: verify the chain, the gates and the archive, export the audit manifest, and report from records

## Why this exists

This flow is repetitive, widely reused and must stay consistent across every
ceo instance. Extracted once so it is executed the same way every time.

## Steps

1. **Freeze the revision.** `git status --short` is empty and `git log -1` is the
   merge the Reviewer approved. Evidence is bound to a revision; nothing below
   counts on a dirty tree.

2. **Chain first, gates second.**

   ```sh
   teamwork.py ledger verify    # chain intact, digests match
   teamwork.py loop             # STOP, not CONTINUE
   teamwork.py audit            # 0 problems
   teamwork.py links            # 0 issues
   teamwork.py tests plan       # no GAP lines; every staffed role has a layer
   ```

   A non-zero exit is a blocker, not a note. `loop` is the stop gate; `audit` is
   the wider health check (links, LFS, duplicates, ownership, forced overrides).

3. **Check the archive agrees with the tree.** For every task in
   `docs/Team/Archive.md` for this milestone: branch merged and deleted,
   `review_status: passed`, review evidence carries a revision. A stale branch or
   a `forced` override fails the close-out and belongs in the report.

4. **Publish the manifest last.** `ledger export` writes
   `docs/Team/AuditManifest.json` and `AuditManifest.md` (head, record count, team
   id, artifact digests). It records the HEAD at export time, which is necessarily
   an ancestor of the commit that carries the manifest, so export after the final
   merge and never hand-edit.

5. **Commit it through the normal gate.** Branch, commit the two manifest files,
   self-check with the export command as the `--test` line, PR, Reviewer merge. A
   manifest committed straight to `main` is an unreviewed claim.

6. **Re-run the gates on the merged manifest revision.** The manifest records
   `dirty: false` and the head it was exported from; any later merge or edit
   invalidates it, so export last and re-verify.

7. **Write the final report from records, not memory**: deliverable, how to run
   it, the evidence table (`command @rev -> result`), known limits still labelled
   `UNVERIFIED`, and the follow-ups left on the queue.

## Failure modes this catches

| Symptom | What it means |
|---|---|
| `loop` CONTINUE with only `todo` tasks | work was queued, not finished; do not report done |
| `audit` reports a forced gate | someone bypassed a gate; the reason must be in the report |
| manifest head is not an ancestor of its own commit | the export predates its commit; regenerate |
| manifest head predates a later merge | the export is stale; regenerate and re-verify |
| `dirty: true` in the manifest | exported from a working tree; it proves nothing |
| digest mismatch on a recorded artifact | a reviewed file changed after its evidence |

## Evidence

Every run records command + revision + observed result, as the team requires.

### Verdict on this skill

verdict: no observed effect

- **The pre-skill failure this file was written for** (`f222211`, 2026-10-17, a
  day and a half before the extraction at `debb237`):
  `git show f222211:docs/Team/AuditManifest.json` reports `git.dirty: true`,
  `ledger.records: 241`, and a `git.head` of `bbb9d299` that does not exist in the
  repository at all (`git cat-file -e bbb9d299` -> `fatal: Not a valid object
  name`). The manifest was exported from a working tree and names a revision
  nobody can check.
- **The same failure recurring after the extraction**, which is why the label is
  not `helped`: `git show 291d348:docs/Team/AuditManifest.json` and
  `git show 756b8c8:docs/Team/AuditManifest.json` both report `git.dirty: true`
  (2026-10-19T13:47:17 and 2026-10-19T19:41:50 - respectively 14m20s and about
  six hours after `1a27a46`, which already carried step 4). Three later manifests
  (`f222211`, `350c933`, `2b52af6`) also name a `git.head` that is absent from the
  repository, so the stale-head mode is present in both eras.
- **Counts are stated as the command that produces them, never as a figure**:
  `.pi/Teamwork/Teams/Teamwork/Ledger.jsonl` held 2075 records with
  `ts <= $(git log -1 --format=%cI 2b52af6)` at that revision, against the
  manifest's `ledger.records: 666` - measure it with
  `python3 -c "import json,subprocess;cut=subprocess.run(['git','log','-1','--format=%cI','2b52af6'],capture_output=True,text=True).stdout.strip();print(sum(1 for l in open('.pi/Teamwork/Teams/Teamwork/Ledger.jsonl') if l.strip() and json.loads(l).get('ts','') and json.loads(l)['ts']<=cut))"`.
  A written-down count is stale the moment it is committed; this row is the
  reason that rule exists.
- **Why `no observed effect` and not `helped`:** no close-out has yet been shown
  to read this file and land a manifest with `dirty: false` whose `git.head` is an
  ancestor of its own commit, and the failures above repeated after the file
  existed. `confounded` would be wrong too - there is no competing change to
  blame; the flow was simply not followed.
- **What would change the label:** one close-out executed from steps 1-7 that
  lands `dirty: false` with an ancestor head makes this `helped`; a close-out that
  reads this file and still produces a dirty or orphaned head makes it `confounded`.
- **Note for the gate's owner:** `VERDICT_RE`
  (`src/teamwork/harness.py:118-121`) is an unanchored search and
  `evidence_findings` (`:563-590`) only checks that a label exists, so this row
  passed lint while carrying invented numbers. Mechanically checking that a
  verdict names a resolvable revision would have caught it.

## Guardrails

- This skill does not replace `AGENTS.md`, the red lines, or the quality gates.
  If it conflicts with them, they win and this file must be fixed.
- It never bypasses: self-check, independent review, the PR, or the Reviewer-only
  merge. It may not weaken or skip a test layer.
- Changing this skill is normal work: branch, commit with the fixed message style,
  PR, review, merge. Never edit it on `main`.
