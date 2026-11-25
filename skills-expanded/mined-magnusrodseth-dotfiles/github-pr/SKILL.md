---
name: github-pr
description: "Prepares and opens reviewable pull requests using local conventions. Use when creating, updating or verifying a PR."
---

# GitHub pull requests

Read AGENTS.md and the repository's contributing guide and PR template. They own branch/title conventions, required checks, reviewers and PR
body requirements. Resolve the actual repository and default branch from Git
and GitHub; a directory name or a remembered `main` is insufficient.

1. Inspect branch, working tree and existing PR. Preserve unrelated work in an
   isolated checkout. Use the requested branch prefix, or the user's GitHub
   login prefix from local conventions. Preserve required commit signing.
2. Capture relevant before-state evidence through [evidence](../evidence/SKILL.md)
   while reproducing a defect. For docs or tooling, demonstrate any claimed
   mechanism with a command or runtime check.
3. Inspect every commit and the complete merge-base diff. Choose checks from
   local guidance for the affected areas. Report exact revision, command and
   result. Pending, skipped and unrun checks do not establish a passing result.
   For a code change, run [pre-pr-review](../pre-pr-review/SKILL.md)
   on the same merge-base diff and keep its report with the evidence. Skip it
   for docs-only changes.
4. Write the smallest PR description that explains the trigger, resulting
   behavior, evidence and material limitations. Lead with **Why this matters**:
   one or two sentences on who benefits and what improves. Reuse a local summary
   field where appropriate; keep trivial changes inline. Include local
   risk/template sections. Reference issues accurately; use closing keywords only
   for work whose full requirements this PR completes. Preserve remaining requirements.
5. Save multiline text to a body file. Push the intended branch and open or
   update the PR against the verified base. Request the human/team review the
   repository requires. Read back base, draft state, body and reviewer selection.
6. Report and attach the created PR when the host supports artifacts. Use
   full Markdown links outside GitHub; bare issue references autolink in GitHub
   bodies. Leave merging, release publication and deployment to their own scope.

When drafting the body, read the bundled [PR description template](references/pr-description.md).
Use the repository's PR template when present; otherwise use this default. Preserve the
concrete product or technical value and scale optional sections to the change.

Native GitHub attachments are handled through the evidence skill. Capability
checks precede use. A PR is not complete merely because one lint command passes.
