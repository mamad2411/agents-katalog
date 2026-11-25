---
name: verify-work
description: Independently verifies a finished work item against its brief and writes review.md with evidence. Use when acting as the reviewer, or when asked to review, verify, or sign off on work someone else built.
---
# Verify work

**Role:** reviewer. This skill is the method. The reviewer's `ROLE.md` holds the routing: where the item goes before the verdict (the Security review section) and after it (who acts after `verified`, or back to the builder). Follow both.

You must not be the role that built the item. If you were, stop and hand it to a fresh session.

1. Read the brief first, then the handoff, then the diff (for a light item, its single file is both). Do not start from the builder's summary.
2. Read the brief's Security review section and route on it before any verdict: see "Route before any verdict" in the reviewer's `ROLE.md`. If the item came back from security, read `security-review.md` before step 3.
3. Run the checks yourself. Do not trust pasted output:
   ```
   python3 tools/check.py
   <the project's test command>
   ```
4. For each acceptance criterion: verify it and record the evidence (command, output, file path). Also check that nothing outside the brief changed, accepted ADRs are respected, and file ownership was respected.
5. Create `review.md` with `python3 tools/item_file.py <id> review`, then fill it: a verdict (approve / changes requested / reject), per-criterion results, and findings ranked blocker, major, minor. Each finding says what, where, why it matters and a recommended fix. A light item has no `review.md`: fill its `## Review` section instead.
6. Move the item as "Route after the verdict" in the reviewer's `ROLE.md` says. A `reject` is routed as `agents/protocols/review.md` says.
7. Do not fix findings yourself.

Details and severity definitions: `agents/protocols/review.md`.
