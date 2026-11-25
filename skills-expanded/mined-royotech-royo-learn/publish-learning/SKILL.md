---
name: publish-learning
description: Publish only a curated and approved learning. Generate and show a preview first, obtain human approval for AGENTS.md, shared libraries or existing Skill changes, apply through royo-learn, verify, audit and rollback on failure.
license: MIT
metadata:
  author: RoyoTech
  version: "4.0.0"
  mcp_profile: admin
---

# Publish Learning

## Preconditions

- status is approved;
- curation specifies target and action;
- acceptance checks exist;
- no unresolved conflict;
- preview is current;
- required approval exists.

## Workflow

1. Call `learning_publication_preview`.
2. Inspect targets, diff, risk and verification.
3. Show high-impact previews to the user.
4. When the preview reports `requires_approval: true` (AGENTS.md, shared scope or
   existing Skill updates), obtain explicit human approval, then call
   `learning_approve` with the exact preview hash to record it. See "Approval
   step" below.
5. Call `learning_publish` with the exact preview hash, and pass the
   `approval_id` returned by `learning_approve` whenever approval was required.
6. Verify result and registry.
7. If verification fails, ensure rollback occurred.
8. Report canonical target and publication ID.

## Approval step

royo-learn now enforces approval. When a preview reports `requires_approval: true`,
publishing is refused until a valid approval exists, so the burden is shared with
the tool rather than resting entirely on you.

- obtain explicit human approval in conversation first;
- record it with `learning_approve`, passing the exact `preview_hash`,
  `approved_by`, `reason` and `approval_evidence` (a link, message id or ticket);
- the approval is bound to that preview hash. It is rejected if the preview
  changes, a destination changes, the prior file content of a destination
  changes, the relevant policy changes, it expires, or it is revoked;
- never treat a preview as an authorization: a preview describes, it does not
  permit;
- never reuse an approval for a different preview — `learning_publish` will
  reject it.

## Rules

- never edit targets directly when royo-learn can apply the approved operation;
- never reuse approval for another preview;
- never place a long procedure in AGENTS.md;
- never guess a global path;
- never bypass a dirty-target block silently;
- never publish secrets or project-private assumptions into shared scope.
