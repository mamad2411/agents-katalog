---
name: scaledock-mcp-server
description: Build or harden a ScaleDock MCP server that follows the MCP base protocol and authorization spec, OAuth 2.1, JWT verification and Problem Details, with PermDock deciding every tool call. Use when adding an MCP surface, protecting MCP tools, wiring Protected Resource Metadata, scope challenges or step-up, filtering tools/list per user, adding MCP Apps UI to tools, adding human approval to destructive tools, or reviewing an MCP server against the specs.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.4.0"
---

# ScaleDock MCP server

An MCP server that is a correct OAuth 2.1 resource server, acts as the signed-in user, and asks PermDock for every tool call. The spec skills carry the rules of each standard; this skill says which ones apply, how they fit the ScaleDock stack, and where PermDock takes over.

**Follow the workflow below step by step.** Read the installed SDK and PermDock docs before you configure anything; option names drift between versions.

## Inputs (fill in, or ask before starting)

- Repo: an existing ScaleDock repo with an `mcp` surface, or a new one (then run `scaledock-repo-standard` first).
- Authorization server: Supabase Auth's OAuth 2.1 server (default), or another issuer the user names.
- Tools: the contract procedures to expose, and which of them write or destroy data.
- Approval store: where `approval-required` decisions wait for a human (required when any tool is destructive).

## Skills to install

```bash
npx skills add ScaleDockHQ/scaledock-skills --skill mcp --skill mcp-authorization --skill oauth --skill jwt --skill problem-details --skill json-rpc --skill server-sent-events
npx skills add ScaleDockHQ/PermDock
```

Optional: `mcp-apps` (`npx skills add ScaleDockHQ/scaledock-skills --skill mcp-apps`) when a tool ships an interactive `ui://` view next to its text result.

`scaledock-repo-standard` (its `references/mcp.md` and `references/auth.md`) owns the app layout: the `@modelcontextprotocol/server` package, the Hono mount, the per-request server factory and tools from the contract.

## Invariants

1. **The spec skills win on protocol details.** Messages, transports, `tools/list`, tool results and errors follow `mcp`; UI views follow `mcp-apps`. Protected Resource Metadata, the `WWW-Authenticate` challenge, resource indicators and audience checks follow `mcp-authorization` and `oauth`; token checks follow `jwt`. Do not restate them here or in the app; link the skill in code review.
2. **Every tool call is a PermDock decision.** Tools register through `createPermDock(...).protectServer(server)` from `permdock/mcp`, one permission per tool. PermDock filters `tools/list`, validates arguments against the resource schema, and audits each call.
3. **Authorization comes from the user, not from scopes.** Scopes say what the client may ask for; PermDock and RLS say what the user may do. Enforce a scope only when the authorization server can issue it.
4. **The subject is never model-supplied.** It comes from the verified access token (`authInfo`) through the PermDock subject resolver, never from tool arguments.
5. **Destructive tools wait for a human.** A tool that deletes, pays, publishes or changes access has `approval` on its grant, so PermDock returns `approval-required` and the MCP adapter turns it into an elicitation.
6. **One error shape.** Denials and failures are RFC 9457 Problem Details: HTTP responses use `application/problem+json`, tool results use `isError: true` with the problem as text and `structuredContent`.
7. **Never pass a token through.** The server never forwards the client's access token to another API; it calls `services` as the user.

## Workflow

1. **Set the inputs and read the docs.** Read the installed `@modelcontextprotocol/server` docs, the `permdock/mcp` page through the PermDock docs MCP (`https://permdock.dev/mcp`), and the `mcp` and `mcp-authorization` skills' Invariants.
   ✓ You can name the spec revision the SDK serves and the PermDock options you will set.
2. **Resource server.** Serve Protected Resource Metadata, return 401 with the `resource_metadata` challenge, and verify every bearer token (signature, issuer, expiry, audience) as `mcp-authorization` and `jwt` require. With Supabase, compose `withOAuthProtectedResource` and then `withSupabase({ auth: "user" })` from `@supabase/server` in a `pipeline` from `@supabase/middleware`, and serve the OAuth Consent block at `/oauth/consent` in the app.
   -> [`references/stack.md`](references/stack.md) (how each requirement maps to the ScaleDock stack)
   ✓ An unauthenticated request gets 401 with the metadata URL, a token for another resource is rejected, and a signed-out user reaching `/oauth/consent` signs in and returns to the consent screen.
3. **Permissions.** Define one permission per tool in `permissions.ts`, grant them in `policy.ts`, and register tools with `protectServer`. Follow `wire-permdock` from `ScaleDockHQ/PermDock`. With `mcp-apps`, link each UI tool to its `ui://` resource and keep its text result; a view's `tools/call` goes through the same PermDock decision.
   ✓ `tools/list` differs per role, and a call without a grant returns a Problem Details denial.
4. **Approvals and step-up.** Put `approval` on every destructive grant and configure a durable approval store. When a tool needs a scope the token lacks, return the scope challenge that `mcp-authorization` describes.
   ✓ A destructive call returns `approval-required` and resumes only after a distinct approver accepts.
5. **Errors.** Route every error through one `problemResult()` helper that follows `problem-details`.
   ✓ No stack trace or raw provider message reaches a client.
6. **Test and audit.** Run the MCP tests from `scaledock-repo-standard` (`tools/list` per role, 401 with metadata, a denial, structured output, the approval path), then run `audit-permissions` from `ScaleDockHQ/PermDock`.
   ✓ The tests pass and the audit has no blocker.

## Verify before done

- [ ] Every item in the `mcp` and `mcp-authorization` Verify lists passes (and `mcp-apps` when installed).
- [ ] Every tool has exactly one permission, and an unmapped tool is not listed.
- [ ] `/oauth/consent` is reachable signed out and returns to the consent screen after sign-in.
- [ ] The subject comes from `authInfo`; no tool reads a user, tenant or actor id from its arguments.
- [ ] Every destructive tool returns `approval-required` without an approval.
- [ ] Every denial is a Problem Details object with a stable `type`.
- [ ] `permdock doctor` reports no error, and `pnpm verify` passes.

## Reference index

- **[`references/stack.md`](references/stack.md)**: each spec requirement mapped to the ScaleDock stack and the PermDock adapter.
