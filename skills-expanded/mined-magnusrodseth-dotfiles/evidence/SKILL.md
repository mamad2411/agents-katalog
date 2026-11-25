---
name: evidence
description: "Captures and publishes revision-specific proof for a change. Use while reproducing a defect, demonstrating tooling, or preparing PR verification."
---

# Evidence

Read AGENTS.md for the repository's checks, services, synthetic data and
browser tooling. Capture the broken behavior before fixing
it. Record separate revisions and dirty-tree state for before and after.

1. Define observable assertions for the requested behavior. Save captures and
   `assertions.md` in a task-specific temporary directory outside the repo.
   Record environment, setup, commands and one of passed/failed/untested per
   assertion. Every untested result has a reason.
2. Use the same scenario on both revisions. A UI change gets a before and an
   after capture of every changed screen and viewport, placed as a pair in the
   PR body; this is the default, not an extra. Screenshots or short recordings
   demonstrate UI behavior; sanitized request/response pairs, state transitions
   or measured probes demonstrate backend and infrastructure changes.
   Performance claims need numbers from the same realistic workload on both
   revisions, with several alternating runs. Report the before and after
   values and the change in percent. For
   documentation-only work, state the exemption and demonstrate any claimed
   mechanism. A lost before-state is an explicit limitation.
3. Confirm each listener/process belongs to the intended checkout. Inspect
   every image/frame before claiming success. Use synthetic data and remove
   secrets and personal identifiers before publishing. Required repository
   checks remain separate evidence and must pass on the claimed revision.
4. Publish evidence in the requested PR body, with assertion results and
   limitations. Check native `gh --attach` support before uploading. Use a
   complete body file with attachment placeholders when placement matters.
   Keep videos as standalone player references, and images as image Markdown.
   Use the target private repository's approved attachment path; an external
   paste host is not an automatic fallback. A fork PR to an upstream where you
   only have read access still gets images: see the read-only row in
   [gh-image](../gh-image/SKILL.md) troubleshooting.
5. Read back the published body and verify its rendered attachments and
   expected player count. Rendered markup does not prove playback. Report a
   failed upload or missing player as unverified. Evidence left only in a
   local temporary file has not been delivered to the reviewer.

Use a selected local browser skill for its actual route/auth setup. CLI uploads
can create or change a PR/comment, so publish only to the user-authorized
surface. Choose the tool available in the active harness; personal skills and
browser profiles are not cloud prerequisites.
