---
name: publishing-artifacts
description: Publish, replace or delete this Work's Artifacts, and ask who this Work is, over Talgent's public HTTP API. Use to deliver a file from the workspace to the Work's owner when the Work has no talgent MCP tools for Artifacts.
---

# Publishing Artifacts

An Artifact is a file of this Work published for its owner; it reaches nobody until published. Talgent's entry for this Work answers at `$TALGENT_API_ADDRESS`. When the Work has the `talgent` MCP server's Artifact tools, use those instead. When `$TALGENT_API_ADDRESS` is unset or empty, the Work cannot publish this way: tell your owner that publishing is unavailable here.

## Calling it

Every call is a JSON `POST` to `$TALGENT_API_ADDRESS/api/<procedure>`:

```sh
curl -sS -X POST "$TALGENT_API_ADDRESS/api/agent.public.v1.IdentityService/WhoAmI" \
  -H 'Content-Type: application/json' -d '{}'
```

The Work's environment adds its identity to every request sent there: you call as this Work's Agent, never as your owner. Send only `Content-Type` and the body. A success answers HTTP 200 with a JSON body; a refusal answers another status with `{"code": "...", "message": "..."}`.

## Who this Work is

`agent.public.v1.IdentityService/WhoAmI` with `{}` answers `workId`, and the Work's `projectId`, `subjectKind`, `subjectId`, `purpose` and `agentId`; those it lacks are absent.

## Artifacts of this Work

Name the file by `"workDirectory": "workspace"` and its `path` relative to `$TALGENT_WORK_ROOT`.

| Procedure | Body | Does |
|---|---|---|
| `storage.public.v1.ArtifactService/CreateArtifact` | `{"name": "<file name>", "workDirectory": "workspace", "path": "<path>"}` | Publishes the file as a new Artifact named `name` |
| `storage.public.v1.ArtifactService/ReplaceArtifact` | `{"name": "<file name>", "workDirectory": "workspace", "path": "<path>"}` | Replaces an existing Artifact's content; its name and share links stay |
| `storage.public.v1.ArtifactService/DeleteArtifact` | `{"name": "<file name>"}` | Deletes the Artifact; its share links end and the source stays in the workspace |

Each answers `{"artifact": {"name": ..., "sizeBytes": ...}}`, and DeleteArtifact `{}`.

## Refusals

| `code` | Meaning | Next |
|---|---|---|
| `already_exists` | An Artifact already has this name | ReplaceArtifact to update it on purpose, or another name |
| `not_found` | No Artifact by this name, or the source file is missing | Check the name, or the path under `$TALGENT_WORK_ROOT` |
| `invalid_argument` | The source is not one regular file under `$TALGENT_WORK_ROOT` outside `inputs/` and `knowledge/`, reached without symbolic links; or the name is not one file name | Pack several files into one archive; name it without slashes |
| `permission_denied` | This Work may not make the call | Tell your owner what you could not do |
| `unauthenticated` | The Work's identity is not current, as while it stops | Stop calling; the call will not succeed in this session |
