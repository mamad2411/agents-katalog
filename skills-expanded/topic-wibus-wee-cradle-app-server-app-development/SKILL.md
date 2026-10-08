---
name: server-app-development
description: Use when modifying Cradle apps/server Elysia modules, adding or changing HTTP routes, TypeBox schemas, OpenAPI details, x-cradle-cli command metadata, module README files, server-side capability ownership, or server-owned downloads and artifact installation flows.
---

# Server App Development

Use this skill for `apps/server` work. Cradle server features are owned by modules under `apps/server/src/modules/{domain}` and exposed through Elysia route modules.

## Core Ownership Rule

Every server feature needs a clear owner and namespace:

- Put business routes in the owning `modules/{domain}/index.ts`.
- Keep shared HTTP/runtime concerns under `src/http`, `src/config`, `src/errors`, `src/database`, or `src/infra`.
- Modules may read other namespaces when needed, but should not write data owned by another product namespace.
- If a route is for a generated CLI command, the server route still owns the API contract; the CLI only projects that contract.

## Download Workflow

新增或修改涉及远程文件下载的 Server 能力时，默认先评估并优先复用 `DownloadCenterService`，不要直接增加 `fetch()`、`arrayBuffer()`、手写 HTTP stream 或新的下载队列。以下场景应接入 Download Center：HTTP(S) artifact 下载需要排队、进度、取消、重试、大小限制、checksum 校验、断点续传或临时 artifact 交接。

- 由业务 owner 构造 `DownloadRequest`：使用稳定的 `owner.namespace`、`resourceType`、`resourceId` 和面向用户的 `displayName`，并明确 `sources`、`integrity` 与 `maxBytes`。不要让 Download Center 推断业务身份。
- 从 `apps/server/src/app.ts` 注入现有 Download Center；不要在业务 module 内创建第二个实例或第二套任务存储。
- 让 Download Center 拥有队列、传输、重试状态、校验、临时 artifact 和任务历史；让业务 owner 继续拥有 URL/manifest 发现、安装、解压、信任判断、资源状态、最终发布与卸载。
- 仅在业务 owner 已复制或发布 artifact、或失败清理已完成后调用 `release()`。一旦取得 artifact，使用 `try/finally` 或等价的结构覆盖成功与失败路径，避免遗留 staging artifact。
- 由 owner 操作触发 retry，因为只有 owner 知道下载完成后如何继续业务流程。不要新增脱离 owner 的通用 retry/install route。
- 不要向 Web、CLI 或公共 task view 暴露 source URL、authorization headers、filesystem artifact path、resume metadata 或原始错误堆栈。
- 不要为了复用而把 Git clone、`npm pack`、长连接 stream 或其他协议专属 transport 伪装成普通 artifact 下载。若现有 Download Center contract 无法表达所需语义，保留 owner transport，并在该 module 的 `README.md` 记录具体不兼容点；不要仅以实现方便作为绕过理由。

修改下载接入时，除 owner 的 focused tests 外，运行：

```bash
pnpm --filter @cradle/server exec vitest run tests/download-center.test.ts
```

## Route Workflow

1. Read the existing module `index.ts`, `model.ts`, `service.ts`, and `README.md`.
2. Add or update TypeBox/Elysia `t` schemas in `model.ts` when the request or response shape changes.
3. Add the Elysia route in `index.ts` with `summary`, `params`, `query`, `body`, and `response` schemas.
4. Keep handler logic thin; call `service.ts` for capability semantics.
5. Update the module `README.md` inventory and note CLI metadata when route metadata changes.
6. Run focused verification:

```bash
pnpm typecheck:server
pnpm test:server
```

If repo-wide server typecheck is blocked by unrelated concurrent work, report the exact unrelated files and still run narrower checks that cover your changes where possible.

## Codex App-Server Runtime

When changing `apps/server/src/modules/chat-runtime-providers/codex`, keep the server adapter aligned with the desktop-vendored Codex runtime:

- Do not depend on the user's global `codex` command for Desktop runtime behavior.
- Desktop owns the bundled executable path and injects it as `CRADLE_CODEX_APP_SERVER_PATH`; the server Codex client should default to that env var and only fall back to `codex` for non-desktop/dev contexts.
- Keep the launch shape as `codex app-server --listen stdio://`. Do not add `--analytics-default-enabled`.
- Use the full Codex CLI release asset (`codex-*`), not the standalone `codex-app-server-*` asset, unless the adapter no longer needs CLI-only behavior. The current adapter needs `codex app-server --config ...` and protocol generation needs `codex app-server generate-ts`.
- Runtime download/update is handled by `apps/desktop/scripts/sync-codex-runtime.mjs`; generated binaries and runtime manifests under `apps/desktop/resources/codex/**` are build artifacts and should stay ignored.

Codex runtime update workflow:

```bash
pnpm --filter @cradle/desktop sync:codex-runtime
pnpm --filter @cradle/server generate:codex-app-server-protocol
pnpm --filter @cradle/server typecheck
pnpm --filter @cradle/server exec vitest run src/modules/chat-runtime-providers/codex/app-server-client.test.ts src/modules/chat-runtime-providers/codex/app-server-capabilities.test.ts src/modules/chat-runtime-providers/codex/provider.test.ts
```

For reproducible release work, set `CRADLE_CODEX_RELEASE_TAG=rust-vX.Y.Z` for both sync and generation. If regenerated protocol removes deprecated fields, delete those request fields and update tests rather than preserving compatibility shims.

## Generated CLI Metadata

Cradle CLI is generated from the server OpenAPI document. Add `x-cradle-cli` only to routes that should become stable Agent-facing shell commands.

The metadata should be command-only by default:

```typescript
detail: {
  summary: 'List issues',
  'x-cradle-cli': {
    command: ['issue', 'list'],
  },
}
```

Optional ambient defaults the generator understands:

- `defaultWorkspaceId: true` — path/query/body `workspaceId` resolves from explicit value, then `CRADLE_WORKSPACE_ID`, then cwd.
- `defaultChatSessionId: true` — chat-session id fields (`path.id` on `/sessions/{id}...`, or `chatSessionId` / `sessionId`) default from `CRADLE_CHAT_SESSION_ID`. Use for session self-ops (pull-request, isolation, linked-issue, await). Do **not** set this on destructive session commands (`delete`, `archive`, `update`, `get`) or await **record** ids.

Do not add `operationId` for CLI generation. The CLI generator does not need it.

Do not duplicate schema data in `x-cradle-cli`:

- Path parameters become positional arguments from OpenAPI parameters.
- Query parameters become flags from OpenAPI query schemas.
- Body object properties become flags from OpenAPI request body schemas.
- Requiredness, primitive type hints, arrays, objects, and enums are inferred from schemas.

Only add more metadata if the CLI generator explicitly supports it and the behavior cannot be inferred from the API schema.

## CLI Exposure Criteria

Add `x-cradle-cli` for routes that are useful to Agents and bash pipelines:

- Read/query/list/get endpoints.
- Normal CRUD endpoints with explicit IDs and typed bodies.
- Export endpoints that return structured data.
- Operational commands such as git status/fetch, approval respond, or chat cancel.

Skip routes that are not good plain CLI commands:

- SSE or long-lived streaming endpoints.
- PTY terminal interactive endpoints.
- Test reset or test-only endpoints.
- Internal producer endpoints such as manual approval creation.
- Secret value writes that would put sensitive values into shell history.

When skipping a route intentionally, prefer documenting the reason in the module README if it is not obvious.

## Validation For CLI-Aware Route Changes

After adding or removing `x-cradle-cli`, run:

```bash
pnpm gen:cli
pnpm --filter @cradle/cli typecheck
pnpm --filter @cradle/cli cradle --help
```

Inspect generated commands under `packages/cli/src/commands/generated` only as build artifacts. Do not edit generated command files manually.
