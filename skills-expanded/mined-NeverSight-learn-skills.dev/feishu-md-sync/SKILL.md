---
name: feishu-md-sync
description: Use when local Markdown is the source of truth and an agent needs to synchronize it with Feishu/Lark through status, diff, dry-run publish, scoped publish, document creation, pull, merge, receipt-aware conflict handling, or explicit SVG-to-Whiteboard synchronization. Do not use for ad hoc remote-only document editing or for creating diagram source assets.
---

# Feishu Markdown Sync

Use `feishu-md-sync` as the execution engine. This Skill supplies routing, sequencing, compatibility checks, and safety policy; it does not recreate sync logic.

## Route The Task

- Use this Skill when local Markdown is the source of truth for an existing or new Feishu document.
- Use `$lark-doc` for ad hoc reading or editing that exists only in the remote Feishu document.
- Use `$lark-shared` for login, user/bot identity, missing scopes, app configuration, and permission repair.
- Keep diagram authoring and SVG generation outside this Skill. Synchronize an existing PNG/SVG pair only when the user explicitly requests Whiteboard sync.

## Resolve The CLI

Treat the executable as one path, never as a shell fragment.

```bash
if [ -n "${FEISHU_MD_SYNC_BIN:-}" ]; then
  FMS="$FEISHU_MD_SYNC_BIN"
else
  FMS="$(command -v feishu-md-sync)"
fi
test -n "$FMS" && test -x "$FMS"
"$FMS" --version
command -v lark-cli
```

For PATH-based stable use, require `feishu-md-sync >=0.4.0 <0.5.0`. Stop and give the matching npm upgrade command when the version is outside this range or cannot be parsed.

`FEISHU_MD_SYNC_BIN` explicitly selects an unreleased development build. If its package version is outside the stable range, continue only when all of these probes succeed:

```bash
"$FMS" --help
"$FMS" publish --help
"$FMS" status --help
"$FMS" diff --help
"$FMS" pull --help
"$FMS" merge --help
"$FMS" doctor auth --help
```

Require the top-level commands `publish`, `status`, `diff`, `pull`, `merge`, and `doctor`. Require every option used by this Skill: publish `--target`, `--profile`, `--dialect`, `--write`, `--create`, `--strategy`, `--confirm-destructive`, `--confirm-collaboration-risk`, `--confirm-untracked-remote`, `--sync-whiteboards`, `--confirm-remote-whiteboard-overwrite`, and `--format`; status and diff `--target`, `--profile`, `--dialect`, `--sync-whiteboards`, and `--format`; pull `--target`, `--output`, `--profile`, `--overwrite`, and `--format`; merge `--target`, `--profile`, `--dialect`, `--check`, `--abort`, and `--format`; doctor auth `--format`. Do not search arbitrary worktrees or guess another build.

## Check Authentication

When Feishu IO fails with `authentication`, `authorization`, or `config`:

```bash
"$FMS" doctor auth --format json
```

Then invoke `$lark-shared` when available. Preserve the reported subtype, hint, missing scopes, and console URL. Never request, print, store, or move an App Secret into this project. Do not run a user login to repair bot permissions.

## Resolve The Source Dialect

When the user explicitly supplies `gfm`, `docusaurus`, or `milvus-authoring`, use that dialect. Otherwise, run the first status without `--dialect`, read `result.dialect`, and then reuse that selected dialect explicitly for diff, publish, merge, and final status. This preserves the workspace default or the CLI's `gfm` fallback without agent-side guessing.

When `dialectDiagnostics` contains `dialect-suggestion`, explain the suggested dialect and ask the user before selecting it. Never infer and silently switch dialects from file contents, repository names, or warning text.

## Handle Dialect And Link Diagnostics

Inspect `dialectBlockers`, `dialectDiagnostics`, `linkResolution`, and resolved link details before any write.

- Any `dialectBlockers` stop the workflow. Confirmation flags cannot bypass dialect or link blockers.
- Report stale Base cache diagnostics. A stale cache remains usable when the affected links still resolve to Feishu.
- Ambiguous or unresolved links stop the workflow.
- A `link-resolver-unavailable` diagnostic with public fallback, or `linkResolution.resolvedToPublicSite > 0`, requires showing every public-site fallback URL and waiting for explicit user acceptance before writing.
- Do not parse warning message prose when a structured diagnostic code or count is available.

## Publish An Existing Document

Use JSON for every planning command:

```bash
"$FMS" status <markdown-file> --target <target> --dialect <dialect> --profile <profile> --format json
"$FMS" diff <markdown-file> --target <target> --dialect <dialect> --profile <profile> --format json
"$FMS" publish <markdown-file> --target <target> --dialect <dialect> --profile <profile> --format json
```

Use profile `none` unless the user or workspace configuration requires `milvus` or `zilliz`.

Interpret the dry-run plan before writing:

- `no-op`: report that no remote write is needed.
- A safe plan with no additional confirmation requirement: an explicit user request to publish or sync authorizes `--write`.
- `requiresUntrackedRemoteConfirmation`: explain that the workspace is adopting an existing untracked document and wait for explicit confirmation.
- `requiresCollaborationRiskConfirmation`: summarize the affected blocks and collaboration risk, then wait for explicit confirmation.
- `requiredRemoteWhiteboardOverwrites`: show each exact asset key and wait for asset-specific confirmation.
- `blocked`, an overlapping scope conflict, or a remote change in the same managed scope: do not write. Recommend conflict resolution or pull/merge.
- `document-replace`: never select it automatically. Run it only after a document-replace dry-run and separate explicit approval.

After approval, repeat the reviewed publish command with `--write` and only the confirmation flags the user approved. Never add a `--confirm-*` flag merely because a failed command lists it.

## Create A Document

For a Drive folder or Wiki parent target:

```bash
"$FMS" publish <markdown-file> --target <folder-or-wiki-parent> --create --dialect <dialect> --profile <profile> --format json
```

Review the dry-run. If the user explicitly requested creation and the plan is safe, repeat with `--write`. Do not combine `--create` with `--sync-whiteboards`.

After creation, read the write result and run status against the returned `document.url` or `document.documentId`, not the original folder or Wiki parent:

```bash
"$FMS" status <markdown-file> --target <created-document-target> --dialect <dialect> --profile <profile> --format json
```

## Synchronize Whiteboards

Do not infer Whiteboard intent from a sibling SVG. Enable it only when the user explicitly asks to synchronize diagram assets:

```bash
"$FMS" status <markdown-file> --target <target> --dialect <dialect> --profile <profile> --sync-whiteboards --format json
"$FMS" diff <markdown-file> --target <target> --dialect <dialect> --profile <profile> --sync-whiteboards --format json
"$FMS" publish <markdown-file> --target <target> --dialect <dialect> --profile <profile> --sync-whiteboards --format json
```

A remotely changed Whiteboard must stop the workflow until the user approves the exact normalized PNG asset key. Never substitute a broad confirmation for asset-specific review.

After a Whiteboard write, preserve the opt-in during final Whiteboard-aware status verification:

```bash
"$FMS" status <markdown-file> --target <target> --dialect <dialect> --profile <profile> --sync-whiteboards --format json
```

## Pull Remote Content

Pull to an independent snapshot unless the user explicitly requested an overwrite:

```bash
"$FMS" pull --target <target> --output <remote-snapshot.md> --profile <profile> --format json
```

Do not replace canonical local Markdown by default. Use `--overwrite` only for an output path the user has approved. A pull receipt is independent of the publish receipt.

## Merge Remote Changes

Automatic merge is available only for `gfm`. Docusaurus and Milvus authoring sources contain source-only syntax that Feishu cannot reconstruct; for those dialects, pull an independent snapshot and reconcile the source manually.

Check before writing the local file:

```bash
"$FMS" merge <markdown-file> --target <target> --dialect <dialect> --profile <profile> --check --format json
```

If the user requested a merge and the check is safe, run the same merge without `--check`. Treat a conflict result as a valid stop state: report the local conflict markers and do not publish. Use `merge --abort` only when the user asks to restore the pre-merge file.

## Handle Machine Errors

With `--format json`, failures are one JSON object on stderr:

```json
{
  "ok": false,
  "error": {
    "type": "confirmation_required",
    "subtype": "collaboration_risk",
    "message": "...",
    "hint": "...",
    "requiredFlags": ["--confirm-collaboration-risk"],
    "retryable": false
  }
}
```

Branch on exit code plus `error.type`, `error.subtype`, `retryable`, and declared extension fields. Never branch on human-readable `message` text.

- Exit `2`: fix validation or arguments.
- Exit `3`: route authentication, authorization, or configuration through `$lark-shared`.
- Exit `4`: retry only when `retryable` is true.
- Exit `5`: inspect verification or internal failure; do not claim success.
- Exit `10`: present the risk and wait for explicit approval. Never automatically retry with `requiredFlags`.
- Exit `1` with a complete stdout result: handle a blocked plan or merge conflict as a domain outcome.

## Verify Completion

After every remote write, run:

```bash
"$FMS" status <markdown-file> --target <target> --dialect <dialect> --profile <profile> --format json
```

Use the returned document target after `--create`, and preserve `--sync-whiteboards` after a Whiteboard write. Report success only when the write passed readback verification and the final status matches the intended synchronized state. Explain any residual state, warnings, or unrelated remote changes. When rendered document structure changed, ask the user to inspect the Feishu document visually.
