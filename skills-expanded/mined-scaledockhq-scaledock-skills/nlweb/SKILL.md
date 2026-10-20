---
name: nlweb
description: >-
  NLWeb: expose a website to natural-language queries and agents through the /ask and /mcp endpoints. Covers NLWeb. Use when exposing a site through the NLWeb REST API. Triggers: NLWeb.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# NLWeb

NLWeb defines a natural-language `ask` interface (with `await` for long-running answers) that sites and agents expose over HTTP or as MCP tools, returning Schema.org-typed JSON results. This skill quotes the NLWeb Specification v0.55, the source of nlweb.ai/spec in the nlweb-ai/website repository, and the REST API document of the reference implementation in nlweb-ai/NLWeb, both pinned at a commit.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: NLWeb agent or site implementer (server), NLWeb client or MCP host, or reviewer of an NLWeb endpoint.
- Target version: NLWeb (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 3.1 Query (Required).** "text (string, required): The natural language query string from the user."
2. **§ 4 Response Structure.** "NLWeb responses are always JSON objects with a required metadata field (_meta) and one or more content fields whose structure depends on the response type."
3. **§ 4 Response Structure.** "Request metadata uses the attribute name meta. Response metadata uses _meta (with a leading underscore) to clearly distinguish request metadata from response metadata."
4. **§ 4 Response Structure: \_meta.** "response_type (string, required): One of "answer", "elicitation", "promise", or "failure"."
5. **§ 4.1.2 Promise.** "token (string, required): An opaque identifier for the promise, used with the await API."
6. **§ 4.2 Await.** "If the task is still running, it returns another promise (with an updated progress value if available). If complete, it returns an answer. If the task was cancelled, it returns a failure with code "CANCELLED"."
7. **§ 6.1 Event Types: complete.** "Clients MUST process this event to capture session state for subsequent requests."
8. **§ 7.1 Endpoints.** "POST /ask — Submit a natural language query."
9. **§ 7.4 HTTP Status Codes.** "Note that an NLWeb failure response (Section 4.1.4) is an application-level response and is typically returned with HTTP 200, since the HTTP request itself was processed successfully."
10. **NLWeb Rest API.** "In the included implementation, there is no server side state. So, the context of the conversation thus far has to be passed back as part of the request."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Every response carries `_meta` with `response_type` and `version`, and streaming responses end with a `complete` event.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `mcp`, `schema-org`, `json-ld`, `server-sent-events`, `a2a`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [NLWeb Specification v0.55](https://raw.githubusercontent.com/nlweb-ai/website/9cd2fd6ceb9e23c6257db782e7058c0a1655894e/NLWEBSPEC.md): Specification draft, v0.55, nlweb-ai/website commit 9cd2fd6, 2026-08-11, checked 2026-10-06.
- [NLWeb Rest API (reference implementation)](https://raw.githubusercontent.com/nlweb-ai/NLWeb/b423f15d9aeaa023ce75993ac9deed2354597043/docs/nlweb-rest-api.md): Documentation, nlweb-ai/NLWeb commit b423f15, 2026-06-10, checked 2026-10-06.
