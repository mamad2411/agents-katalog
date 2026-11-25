---
name: yandex-workspace
description: Guide for agents using the Yandex Workspace MCP server
---

# Yandex Workspace Skill

This skill instructs agents on how to best interact with the `yandex-workspace-mcp` server.

## Best Practices

1. **Unified Search First**: To find information across the workspace, always start with `search` to query both Yandex Disk and Yandex Wiki simultaneously. Use the returned locator/slug to fetch detailed content.
   - If a source reports `degraded=true` and `search_mode="descendants"`, results match Wiki slugs from the bounded descendants fallback, not full page content.
   - Continue canonical searches only with the returned workspace cursor. Do not pass it to standalone Disk or Wiki tools.
2. **Wiki as Documentation, Disk as Artifacts**: Treat Yandex Wiki as the source of truth for structured documentation, project notes, and dynamic tables. Treat Yandex Disk as the source for raw files, datasets, and binary artifacts.
3. **Safe Wiki Updates**: Use page write tools only after reading the target. For grids, pass the latest returned `revision`; row, cell, and column mutations use optimistic concurrency.
4. **Destructive Actions**: Do not perform destructive actions (`wiki_delete_page`, `wiki_delete_grid`, row/column deletion, `disk_delete`, `disk_empty_trash`, or overwrite moves) without explicit user consent. Treat a page recovery handle as short-lived and single-use. Emptying Trash is permanent and requires an explicit literal confirmation.
5. **Conflict Handling**: On a grid conflict, fetch the grid again, reconcile against its current revision, and ask before retrying a destructive change. Mutations are not automatically replayed.
6. **Allowed Roots Constraints**: Be aware that your operations are confined to configured `ALLOWED_ROOTS`. Do not attempt to traverse outside these roots, as the operations will be blocked.
   Results are post-filtered by the server even when the upstream API accepted a root filter.
7. **Read Before Write**: When asked to make mass changes, first fetch the list of objects (using `disk_list`, `wiki_get_descendants`, or the `wiki_get_tree` alias) and present a plan to the user before executing the write operations.
8. **Attachments**: `wiki_upload_attachment` can only read a server-local file from an administrator allowlist and is available only in trusted stdio mode. Never assume a client-machine path is visible to the server.
9. **Copy Operations**: Page clone may wait for a bounded upstream operation. Grid copy can return `status="pending"`; do not invent a completed grid ID when it does.
10. **Disk Transfers**: Prefer inline upload only for small generated text. Local-file/background tools exist only on a trusted stdio server and can see only administrator-allowlisted server paths. URL import accepts only administrator-allowlisted exact hosts. Never ask to weaken these gates.
11. **Local Upload Jobs**: Poll only with the returned UUID using `disk_get_upload_status` or use the bounded list tool. Job records never contain the source path and disappear after their configured TTL or server restart.
12. **Public and Trash Resources**: A public key/URL must already be server-allowlisted and does not grant access to private roots. Trash results may omit entries whose original paths cannot be authorized; restore only to an allowed destination.
13. **Remote identity**: Treat `workspace:read`, `workspace:write`, and `workspace:delete` denials as server policy. Never ask for a Yandex token as an MCP bearer token or attempt to pass tokens, OAuth state, authorization codes, signed URLs, or public keys through tool text.
