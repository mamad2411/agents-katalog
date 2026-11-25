---
name: reading-inputs
description: List this Work's inputs and download one into inputs/ over Talgent's public HTTP API. Use on a Managed Computer, where inputs/ holds only the files you downloaded, before reading an input, and when the Work has no talgent MCP tools for inputs.
---

# Reading inputs

The Work's inputs are the Attachments it reads: its own, or, for a Work with a File Home, its File Home's. On a Cloud, `inputs/` is mounted with their current content: read them there. On a Managed Computer, `inputs/` holds only the files you downloaded, so list the inputs and download the ones you need. Talgent's entry for this Work answers at `$TALGENT_API_ADDRESS`. When the Work has the `talgent` MCP server's input tools, use those instead. When `$TALGENT_API_ADDRESS` is unset or empty, the Work cannot read its inputs this way: tell your owner that its inputs are unavailable here.

## Calling it

Every call is a JSON `POST` to `$TALGENT_API_ADDRESS/api/<procedure>`:

```sh
curl -sS -X POST "$TALGENT_API_ADDRESS/api/agent.public.v1.IdentityService/WhoAmI" \
  -H 'Content-Type: application/json' -d '{}'
```

The Work's environment adds its identity to every request sent there: you call as this Work's Agent, never as your owner. Send only `Content-Type` and the body. A success answers HTTP 200 with a JSON body; a refusal answers another status with `{"code": "...", "message": "..."}`. `WhoAmI` answers this Work's `workId`.

## Listing and downloading an input

1. **List**: `agent.public.v1.WorkFileService/ListWorkFiles` with `{"workId": "<this Work's workId>"}`. It answers `files`, each with `name`, `sizeBytes`, `contentType` and `updatedAt`, the inputs' current state.
2. **Get a link**: `agent.public.v1.WorkFileService/CreateWorkFileAccessLink` with `{"workId": "<this Work's workId>", "kind": "WORK_FILE_KIND_ATTACHMENT", "name": "<name>", "disposition": "WORK_FILE_ACCESS_DISPOSITION_DOWNLOAD"}`. It answers `accessUrl`, the link as a path on the entry, and `expiresAt`. Each call issues a new link.
3. **Download** within the link's lifetime:

   ```sh
   curl -fsS -o "$TALGENT_WORK_ROOT/inputs/<name>" "$TALGENT_API_ADDRESS<accessUrl>"
   ```

The download is a snapshot of the input at that moment. Note its `updatedAt`, and download it again when you need its current content.

## Refusals

| `code` | Meaning | Next |
|---|---|---|
| `not_found` | No input by this name | List again and use the name it answers |
| `permission_denied` | The `workId` is not this Work's | Use the `workId` that `WhoAmI` answers |
| `unauthenticated` | The Work's identity is not current, as while it stops | Stop calling; the call will not succeed in this session |
