---
name: reading-personal-library
description: Search the owner's Personal Library and download a file from it over Talgent's public HTTP API. Use when the owner points to an earlier Artifact of theirs, or one shared with them, and the Work has no talgent MCP tools for the Library.
---

# Reading the Personal Library

The Personal Library is the Artifacts of your owner's Works and of the Works shared with them. Only the Agent of a Work done for a person, without a Project, reads it. Talgent's entry for this Work answers at `$TALGENT_API_ADDRESS`. When the Work has the `talgent` MCP server's Library tools, use those instead. When `$TALGENT_API_ADDRESS` is unset or empty, the Work cannot reach the Library this way: tell your owner that the Library is unavailable here.

## Calling it

Every call is a JSON `POST` to `$TALGENT_API_ADDRESS/api/<procedure>`:

```sh
curl -sS -X POST "$TALGENT_API_ADDRESS/api/agent.public.v2.WorkService/ListLibraryFiles" \
  -H 'Content-Type: application/json' -d '{}'
```

The Work's environment adds its identity to every request sent there: you call as this Work's Agent, never as your owner. Send only `Content-Type` and the body. A success answers HTTP 200 with a JSON body; a refusal answers another status with `{"code": "...", "message": "..."}`.

## Finding and downloading a file

1. **Search**: `agent.public.v2.WorkService/ListLibraryFiles` with `{"nameQuery": "<part of a name>"}`, and `"workId"` to narrow to one Work; both are optional. It answers `files`, newest first, each with `workId`, `name`, `sizeBytes`, `contentType` and `addedAt`, and `works` with each Work's `title`.
2. **Get a link**: `agent.public.v1.WorkFileService/CreateWorkFileAccessLink` with `{"workId": "<workId>", "kind": "WORK_FILE_KIND_ARTIFACT", "name": "<name>", "disposition": "WORK_FILE_ACCESS_DISPOSITION_DOWNLOAD"}`. It answers `accessUrl`, the link as a path on the entry, and `expiresAt`.
3. **Download** within the link's lifetime, outside `inputs/`:

   ```sh
   curl -fsS -o "$TALGENT_WORK_ROOT/<path>" "$TALGENT_API_ADDRESS<accessUrl>"
   ```

The copy is a snapshot for reference: it is not an Artifact of this Work and does not follow later changes.

## Refusals

| `code` | Meaning | Next |
|---|---|---|
| `not_found` | No Library file by this name | Search again and use the name it answers |
| `permission_denied` | This Work may not read the Library, as a Work of a Project | Tell your owner what you could not do |
| `unauthenticated` | The Work's identity is not current, as while it stops | Stop calling; the call will not succeed in this session |
