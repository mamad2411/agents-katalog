---
name: first-tree-read
version: 0.8.1-local.1
description: Read the applicable Context Tree before acting. In BYO sessions, route only among locally authorized Teams by reading each exact root SCOPE.md before selecting one task snapshot; in managed workspaces, use the bound Tree. Do not use for a Context Tree PR/MR review or an explicit broad audit of stored tree content.
---

# First Tree Read — Local Context

## Purpose and authority

Read the current Agent's private Local Context before acting on a task with a
repo, path, feature, domain, owner, bug, or error signal. This payload is the
managed Local variant of `first-tree-read`; its public name and routing
description intentionally match the Remote payload.

Local Context is host-local truth for this Agent only. It is not Team-approved
truth, a Git checkout, a BYO snapshot, or a fallback for an unreadable or
invalid remote binding. `first-tree-seed`, `context-tree-review`, and
`context-tree-audit` never operate on it.

Apply the generated Context Tree Policy's normal/archive/member authority and
code-vs-tree drift rules. Never modify Tree content with this Skill.

## Workflow

1. Run the generated briefing's exact First Tree CLI invocation:

   ```text
   <firstTreeInvocation> --json tree local resolve --ensure --intent read
   ```

   Use only the returned `data.path`. The guard accepts no caller-supplied live
   path and rechecks runtime identity, fixed Workspace containment, resource
   limits, the remote-observed latch, and the live Server binding. Missing,
   corrupt, unknown, invalid, frozen, or bound state stops the Local read.

2. Before reading business Context, run:

   ```text
   <firstTreeInvocation> tree verify --tree-path "<live-root>"
   ```

   A non-zero result stops the read. Report that Local Write must repair the
   live Tree; do not guess an older version or continue from partial files.

3. Inspect the filesystem hierarchy command from the live root, then use its
   selectors before native Markdown reads:

   ```text
   <firstTreeInvocation> tree tree --tree-path "<live-root>" --help
   <firstTreeInvocation> tree tree --tree-path "<live-root>" [path] [selectors]
   ```

   This mode performs no Git discovery, pull, branch, commit, snapshot, forge,
   Cloud Tree IO, or attribution. Keep the read focused: root and relevant
   parents, matched leaves, and material `soft_links` only.

4. If a selected file vanishes, fails to parse, or appears to be an in-flight
   concurrent edit, discard that read and restart from verification. Local
   reads have no stable snapshot guarantee.

5. Immediately before using Local Context for a substantive choice, run the
   same full `tree verify --tree-path` again. Passing proves only that the live
   Tree is mechanically valid at that moment; it does not prove the bytes read
   earlier were unchanged.

6. Carry forward only relevant durable decisions, constraints, ownership, and
   cross-domain relationships. Local V0 has no immutable commit attribution,
   so do not emit the standard remote Context Tree influence note or fabricate
   source links.

## Failure boundary

Local writers use no content lock, snapshot, candidate, fingerprint, journal,
rollback, or per-write approval. A reader may observe moving state. Never turn
that accepted limitation into a claim of transaction safety or silently accept
an invalid intermediate Tree.
