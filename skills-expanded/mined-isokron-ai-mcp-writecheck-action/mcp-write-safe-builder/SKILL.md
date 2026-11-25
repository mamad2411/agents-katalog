---
name: mcp-write-safe-builder
description: Build rules for MCP servers whose tools create, update or delete state, taken from the MCP Write-Safety Requirements (MWS 0.9), each with its requirement ID. Use when building, changing or reviewing an MCP server or one of its write tools (update semantics, concurrency and versions, targeting, truthful results and errors, unknown outcomes, bulk writes, retries and idempotency keys, input validation, read-only mode and tool filters, tool annotations, credentials in results, the write-result shape), and when adding the mcp-writecheck check to a server's CI.
---

# Building a write-safe MCP server (MWS 0.9)

MWS states what an MCP server must do so that a write made through one of its tools has the effect the caller asked for, on the object the caller named, and is reported truthfully. This skill restates its 37 requirements as build rules.

Source: MCP Write-Safety Requirements, version 0.9 (draft for public comment), <https://isokron.ai/mws?utm_source=writecheck-action-skill&utm_medium=skill>. Every requirement in 0.9 has the status `draft`; wording and levels may change before 1.0. The requirement is the sentence in section 9 of the spec. Where this skill and the spec differ, the spec is right: read the requirement by its ID before you rely on a rule here.

How to read the rules:

- **MUST** and **SHOULD** are the requirement's level. Treat a MUST as a defect to fix before the change ships. Follow a SHOULD unless the user gives a reason not to, and say so when you do not.
- *Applies when* is the requirement's condition. If it is false for a tool, the rule does not apply to it.
- *How* lines are the spec's informative guidance and mitigation patterns (its Guidance paragraphs and Annex B). They are ways to meet a rule, not rules. The same holds for the result shape and the helper kits below.

MWS does not cover authentication, authorization, transport security or prompt injection. Do not treat this skill as a security review.

## Before you write or change a tool

Establish these facts first. Each rule below depends on one of them.

1. **Which tools write.** A write tool can create, change or delete state in the backend. Keep the list in code; rules CFG-3 and ANN-* need it.
2. **Each update tool's mode, read from its input schema.** Fields as separate arguments, some optional: *field patch*. Every field required: *full replace*. A named operation such as "close": *command*. More than one backend write per call: *composite*. If the description says one thing and the schema another, the schema decides. Make them agree.
3. **What concurrency control the backend offers** for each operation: a version or entity tag precondition, a lock, a non-forced apply. Also note where it offers none.
4. **What the platform's own API does by default** for the same operation. A tool must not be less safe than that default (CONC-1).

## Update semantics

**MWS-UPD-1 (MUST).** *Applies when* the tool is an update in field-patch mode.
Change only the fields the arguments name. Every other field keeps its stored value, apart from fields the backend manages itself, and no default is written that the caller did not send.
*How:* use the platform's partial-update operation where it has one, and do not read, merge and write back the whole object (B-1). Where the platform only replaces whole objects, read the stored object first. Do not let schema defaults, including nested ones, fill in arguments the caller omitted. The spec does not say whether an explicit `null` clears a field or leaves it; whichever the tool does, the fields the call did not name stay as they were, and the result says what happened to the named one (RES-1).

**MWS-UPD-2 (MUST).** *Applies when* the tool edits, moves or removes one element of a list held inside an object.
Apply the change to the element that the caller's address denoted in the list as the caller read it, or refuse the call, when elements have been inserted, removed or reordered since that read.
*How:* give each element a stable identifier and accept it in the edit tool. A positional tool that refuses a stale edit through a version check (CONC-2) also meets the rule.

**Watch for: a list field set as a whole from an older read.** This is not a requirement in 0.9; the spec lists it as a candidate (section 12), and it is one of the most common ways an agent loses a person's change. An agent reads a ticket's labels or assignees, adds one, and sends the whole list back. If another writer added an element after that read, it is gone, and UPD-1 still holds because only the named field changed.
*How:* offer tools that add or remove one element (`add_label`, `remove_assignee`), or accept a version on the tool that sets the whole list and refuse a stale one (CONC-2). Do not leave that version optional with the unchecked write as the default. A body sent as a merge patch has the same problem for every list in it.

## Concurrency and preconditions

**MWS-CONC-1 (MUST).** *Applies when* the backend offers a concurrency control for an operation the tool performs.
Do not disable or bypass that control, unless the caller sets an explicit override argument whose default is off. A tool bypasses a control when its default request skips a check that the platform API's default request performs: forcing an overwrite, writing through another user's lock, force-applying.
*How:* a tool with no override at all meets the rule. A refusal should not present the override as the way to make the call succeed.

**MWS-CONC-2 (MUST).** *Applies when* the tool replaces a whole object, deletes an object, or accepts a version from the caller.
Refuse the write with a conflict when the object has changed since the state the caller read, wherever the backend can detect the change.
*How:* return the version from every read tool, accept it on every such write tool, and send it to the backend as the precondition (B-2). Send the caller's version, never the current one fetched just before the write. If the tool accepts a version, use it. For a delete, send the precondition where the platform's delete accepts one. On a tool that replaces a whole object or deletes, an optional version argument makes the unchecked write the default: require the version, or offer an explicit override that is off by default. Key the check to the version (or a server-minted handle) that the call carries, not to the credential, the user, the connection or the server process: the other writer can use the same connection and the same credential, and the spec's test stages the stale write that way.

**MWS-CONC-3 (MUST).** *Applies when* two different fields of one object can be changed through a write tool.
Two concurrent writes to different parts of one object must not both report success when either change is absent afterwards.
*How:* send only what changed (B-1), so that the server has no read-modify-write of its own. Where the tool must read and write, guard that interval with the backend's version check and return a conflict when it fails. A per-object lock in the server (B-4) covers only calls through that one process.

**MWS-CONC-4 (MUST).** *Applies when* the tool can refuse a write because of a conflict.
A write refused because of a conflict must not be applied, in whole or in part, and must be returned as a tool execution error (`isError: true`) that says the write was not applied.

**MWS-CONC-5 (SHOULD).** *Applies when* the tool replaces a whole object, deletes an object or accepts a version, and the backend cannot detect that the object changed since the caller's read.
State in the tool's description that stale writes are not detected, or are detected only on a best-effort basis by the server.
*How:* where the backend has no version check, the server can derive a version (a timestamp, a hash of the exposed fields), return it from reads, and compare before writing (B-3). A gap remains between the comparison and the write, and the description should say so (B-8).

**MWS-CONC-6 (SHOULD).** *Applies when* the tool can refuse a write because the object changed since the caller's read.
Make the conflict error tell the caller to read the object again before it retries, or carry the object's current state.
*How:* give the current state only in a form that can be read one way: a JSON object, or every string and list member quoted. Never restate it in unquoted prose; in the spec's exploratory test that did worse than giving no state at all. Where you cannot give it that way, leave it out and tell the caller to read the object again, naming the read. Give the current version on its own under the name the write tool accepts; that is for determinism, not protection. The refusal itself (CONC-2, CONC-4) is what keeps the other writer's change: a version in the error is not a reason to retry with the new version alone, because a caller that resends its old body under the new version overwrites that change.

## Targeting

**MWS-TGT-1 (MUST).** *Applies when* a write tool accepts a scope argument (a namespace, project, tenant, locale).
Apply the write within the scope the argument names, or reject the call. Never apply it anywhere else, including the server's configured default scope.
*How:* this rule is about where the write lands, not about who may write there. Meeting it says nothing about whether the caller may act in the scope it names; that is access control, which MWS does not cover.

**MWS-TGT-2 (MUST).** *Applies when* a tool deletes, or updates more than one object, and accepts a selector or a path.
Do not treat an empty, missing or match-all selector, or the path of a container, as selecting every object, unless the caller sets an explicit argument that opts in.
*How:* a refusal should not present the opt-in as the way to make the call succeed. A bulk tool that can report how many objects a selector matches, before it acts, lets a caller check first. A tool whose stated purpose is to delete a container may delete the container it was given (NF-18).

**MWS-TGT-3 (MUST).** *Applies when* a tool is presented, by name and description, as a create, for objects identified by a caller-chosen name or key. A tool presented as bringing a new object into being under a name the caller chooses (run, start, launch, deploy, install, clone) counts as a create, unless its name or description says that an existing object of that name is updated, replaced or applied over. A start of an existing object does not count. A tool presented as an upsert or an apply is not a create for this rule (NF-8).
Do not overwrite an existing object with the same name or key, unless the caller sets an explicit argument that asks for the overwrite.
*How:* if a `deploy` or `install` tool is meant to replace what is there, say so in its description; otherwise refuse the collision.

## Truthful results

**MWS-RES-1 (MUST).** *Applies when* the tool writes.
Report success only when the state the caller asked for is in effect afterwards. Do not skip a value (an empty string, an argument you did not store) and still report success. Do not say "deleted" while the declared read tool still returns the object. An explicit `null` is the one value the spec leaves open: whether it clears the field or leaves it is not judged (UPD-1), and an optional argument sent as `null` may be treated as not sent (IN-1); say in the result which the tool did.
*How:* a call that changes nothing because things were already as asked, such as deleting an absent object named by its identifier, may report success (NF-5); say that nothing was changed. If an operation was accepted and is still pending, say that, not that it was done (NF-19).

**MWS-RES-2 (MUST).** *Applies when* the tool writes. Three clauses:
1. A write that fails in whole or in part must not be reported as a success.
2. The error must identify any change that remains applied, or say that it is not known whether a change was applied. It must not report a settled outcome as not known. It must not tell the caller to repeat a write whose outcome is open, except after a read that it names, or with the idempotency key or the version that the call carried.
3. Where the failure is a refusal or failure of the backend, or of a rule the tool applies, return it as a tool execution error (`isError: true`), not as a JSON-RPC protocol error.

An outcome is *settled* when the server has the backend's own answer saying the request was carried out or refused (or has looked the request up since). It is *open* when the server sent the request, or may have, and has no such answer: no answer, an intermediary's answer, or a backend server error.
*How:* do not pass the HTTP or database client's error through as it stands, or behind words that say the write failed; fix the code that turns a backend error into a tool error. For a request that was sent and got no answer, say three things: the request was sent and no answer arrived; it is not known whether the change was applied; which read shows it. For example: "Outcome unknown: the update to item 42 was sent and the connection closed before an answer arrived. The change may have been applied. Read item 42 with get_item before repeating the call." A whole-value set or a delete by identifier is not safe to repeat blind either: name a read, or invite the repeat with the version the call carried. A refusal is reported as a refusal; a failure before any request was sent may be reported as a failure.

**MWS-RES-3 (MUST).** *Applies when* the tool creates an object.
Return the identifier of each object it created, including when a later step of the same call fails: put the identifier in the error result.

**MWS-RES-4 (SHOULD).** *Applies when* the tool creates or updates an object.
Return a receipt that identifies the object written, the fields changed and, where the resource has a version, its new version.
*How:* an empty list of changed fields is how a no-op says so. Name a field that holds a secret; do not echo its value (SEC-1).

## Multi-step and multi-item writes

**MWS-ATOM-1 (MUST).** *Applies when* a tool writes more than one item, or makes more than one backend write, in one call.
A write that is not applied completely must not report success, and must name which items or steps were applied and which were not.
*How:* name each item or step by its position in the call or by its identifier, and say of each whether it was applied, failed, was not attempted, or has an open outcome (say that it is not known; RES-2 judges that statement). Naming only the first failure is not enough. For a write by selector, a count of the objects applied with the identifiers of those not applied is enough. Do not word the text as if the whole write took effect ("All 3 items saved") when any item or step was not applied: a tester can read that text as a report of success, and a shape or another text that names the items correctly does not make up for it.

**MWS-ATOM-2 (SHOULD).** *Applies when* a tool writes more than one object in one call.
Make the write all-or-nothing: when any part fails, none of its changes remains applied.
*How:* a backend transaction is the reliable way. Without one, validate every item before writing any, undo what was written on a later failure, and report exactly what remains (B-7).

## Retries and replays

A caller that receives no answer sends the write again. Under MCP revision `2026-07-28` a request whose response stream broke is lost, and a client that sends it again sends a new request, which the server cannot tell from a first attempt.

**MWS-RETRY-1 (SHOULD).** *Applies when* two calls of a create tool with the same arguments create two objects.
Accept an idempotency key from the caller. MCP defines no carrier for it: use a tool argument or a `_meta` field, and document which.
*How:* say in the description that a retry of the same intended write sends the same key, and how long a key is remembered. A create that refuses a duplicate of a caller-chosen name or key needs no key (B-6).

**MWS-RETRY-2 (MUST).** *Applies when* a write tool accepts an idempotency key. Three clauses:
1. The same key with the same arguments is applied at most once and, where the first call applied the write and the server can establish that, is answered with the outcome of that call.
2. A different key is a new write.
3. The same key with different arguments is refused.

*How:* keep each key with a hash of the arguments and the result, written in the same transaction as the write; where that is impossible, store the key as pending before calling the backend and complete it from the answer (B-5). Every instance of the server must see the record. Keep it durable: a key kept only in memory is lost in a restart, and a server that then takes the key for a new one applies the write again, which the spec's test checks (step (e)). A server that has no record of a key and cannot vouch for it applies nothing and says the outcome is not known (`key_not_known`); the spec's test gives that `held` with the note "key record not kept". Where the server cannot establish what the first call did (its answer was lost, or a key it has no record of and cannot vouch for), apply nothing and say that the outcome is not known. A repeat that arrives while the first call is in progress may wait for the first outcome or be refused with an error that says so. Mark a replay (`replayed: true` in the result shape).

**MWS-RETRY-3 (MUST).** *Applies when* a write tool can answer with an `input_required` result (MCP revision `2026-07-28`).
When the tool answers `input_required`, it must not have put the requested write into effect in that call, in whole or in part.
*How:* collect the missing input first and write afterwards, or stage a draft and commit that same draft on the retry. Staged state should expire; say in the description what is left behind if the client does not retry.

## Inputs

These seven apply to every tool, read tools included: the same handling serves both.

**MWS-IN-1 (MUST).** *Applies when* the schema declares a type for an argument.
Do not coerce an argument to a value whose meaning differs from the value sent. Never: `"false"` used as true; `null` or `""` used as a number, as false or as an empty value; `null` for a required argument replaced by a default; a non-numeric string used as a number; a fraction rounded or truncated to an integer; an object or a list flattened to a string; a non-null value dropped. A `null` sent for an argument the schema does not require may be treated as not sent. A conversion that keeps the meaning, such as `"5"` used as 5, does not break this rule; IN-6 covers it.

**MWS-IN-2 (MUST).** *Applies when* the schema does not explicitly allow additional properties at that level.
Do not silently drop an argument the schema does not define. Reject the call, or name the argument in the result and say it was not used.

**MWS-IN-3 (MUST).** *Applies when* the schema declares a constraint with `required`, `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `multipleOf`, `minLength`, `maxLength`, `pattern`, `minItems`, `maxItems`, `uniqueItems`, `minProperties`, `maxProperties`, `enum` or `const`.
Reject a call that breaks the constraint. Do not clamp or truncate the value to fit. A refusal passed on from the backend counts as a rejection.

**MWS-IN-4 (MUST).** *Applies when* the tool can refuse an argument.
Report an input validation failure as a tool execution error (`isError: true`) that names the argument at fault and the reason it was refused.
*How:* keep stack traces and internal type names out of the error.

**MWS-IN-5 (SHOULD).** *Applies when* the server or its backend enforces a fixed constraint on the value of one argument that the keywords of IN-3 can express.
Declare each such constraint in the input schema.

**MWS-IN-6 (SHOULD).** *Applies when* the schema declares a type for an argument.
Reject an argument whose value is not of a declared type, rather than convert or drop it. Check what the SDK or validation library does by default; some convert.

**MWS-IN-7 (SHOULD).** *Applies when* the schema does not explicitly allow additional properties at that level.
Reject an argument the schema does not define.
*How:* declare `additionalProperties: false` wherever the tool rejects undefined arguments, so that a client checking a call against the schema sees the same rule. Some validation libraries strip unknown properties by default; configure them not to.

## Safety settings

**MWS-CFG-1 (MUST).** *Applies when* the server has a read-only mode or another setting whose purpose is to restrict writes, applied at start or with a request.
Never accept a write when that setting has a value the server does not recognize, such as a typo, or `yes` where the server understands only `true`.
*How:* refuse to start, or refuse the request; that tells the operator about the mistake.

**MWS-CFG-2 (MUST).** *Applies when* the server has a setting that denies tools by name.
When the deny-list contains a name that is not a tool the server defines, refuse to start, refuse to serve the request that carries the list, or disable every write tool.

**MWS-CFG-3 (MUST).** *Applies when* the server has a read-only mode.
In read-only mode refuse every call to a write tool, whatever that tool's annotations declare.
*How:* decide from the server's own list of write tools (fact 1), not from annotations.

**MWS-CFG-4 (SHOULD).** *Applies when* the server has a setting that allows tools by name.
When the allow-list contains a name that is not a tool the server defines, refuse to start, or refuse to serve the request that carries the list.

## Annotations

The MCP defaults are the cautious values (`readOnlyHint` false, `destructiveHint` true, `idempotentHint` false, `openWorldHint` true). Declaring the cautious value is never a violation (NF-2); only an optimistic claim can be false. When unsure, declare the cautious value.

**MWS-ANN-1 (MUST).** A tool that declares `readOnlyHint: true` must not change state.

**MWS-ANN-2 (MUST).** *Applies when* a tool declares `destructiveHint: false` and not `readOnlyHint: true`.
The tool must not delete an object, and must not remove or replace data that the caller's arguments did not name.

**MWS-ANN-3 (MUST).** *Applies when* a tool declares `idempotentHint: true` and not `readOnlyHint: true`.
Calling the tool again with the same arguments must have no further effect. A tool that creates a new object on each call is not idempotent.

**MWS-ANN-4 (SHOULD).** Declare `readOnlyHint` explicitly on every tool, and `destructiveHint` explicitly on every tool that does not declare `readOnlyHint: true`.
*How:* declare `openWorldHint: false` only where the tool's domain of interaction is closed, as the MCP schema words it.

**MWS-ANN-5 (SHOULD, marked at risk in 0.9).** *Applies when* a tool declares `destructiveHint: false` and not `readOnlyHint: true`.
The tool should perform only additive updates, as the MCP schema states. Under this strict reading a tool that replaces an existing value does not declare the hint false. The requirement may be reworded or withdrawn when the MCP specification clarifies the hint.

## Credentials in results

**MWS-SEC-1 (MUST).** *Applies to* every tool.
A tool result, whether a success or an error, must not contain a credential: a token, a secret, or a URL that carries a token or a signature. The one exception is a credential that the tool exists to issue and the caller asked for. The credential the server itself uses to reach its backend is never excepted.
*How:* do not echo request or response headers into errors. Check what the backend's responses carry before passing them on; a signed download URL from the backend is a credential in the result.

## The result shape `write-result/0.1` (Annex B, B-9)

A pattern, not a requirement: a server meets every requirement without it, and a result that carries it is judged by the same requirements as text. It gives the outcome, the repeat rule and the read in fixed terms, which is what a caller most often misreads. Use it on write tools you build or change unless the user decides otherwise.

- **Placement.** `structuredContent.mws`, beside the tool's own output. `shape: "write-result/0.1"` and `outcome` are required; leave out a member that does not apply (never `null`). Return it on every result your tool code produces, success or error.
- **`outcome`.** `applied` (in effect; with `changed: []`, nothing needed changing), `not_applied` (nothing remains applied), `partial` (several items or steps, each settled or not attempted), `unknown` (any part open), `accepted` (only for an operation the backend completes asynchronously; no `changed`, no `object.version`). `isError: true` with `not_applied`, `partial` and `unknown`.
- **`repeat`.** `no`; `yes` (only with `not_applied`, where nothing was sent or the refusal may not recur); `same_key` and `same_version` (only the key or version this call carried; on a call that carried none they read as `yes`, so do not send them there); `read_first` (every conflict; also `unknown` and `partial`). Never `yes` with `unknown`, `partial`, `accepted` or `applied`; after `applied`, `same_key` or `same_version` where the call carried one, else `no`.
- **Other members.** `object` (`type`, `id`, `version` after the write, `scope`, `parent`), `changed` (JSON Pointers; names only, never secret values), `items` with `applied_count`, `replayed`, `argument` and `argument_errors`, `conflict` (`current_version`, `checked_by`, `current_state`, `omitted`, `held_by`), `read_with` (`tool` and `arguments` of a read tool the server lists), `version_argument`. Give identifiers and versions in the JSON type the write tool's argument accepts. On a repeat with a key where you do not have the first answer's `changed`, leave `changed` out; never send `changed: []` for it, which says the write changed nothing.
- **Reserved codes.** Use these with their fixed outcome: `conflict`, `locked`, `version_required`, `invalid_argument`, `not_found`, `idempotency_key_reused`, `unavailable`, `not_permitted`, `not_sent` (all `not_applied`); `in_progress`, `key_not_known`, `no_answer`, `backend_error`, `internal_error` (all `unknown`). `unavailable` is a refusal that a later repeat may get past, such as a rate limit; `not_permitted` is one that a repeat meets again until a setting or a permission changes (writes disabled, read-only mode, the tool switched off, the caller may not make the write), so its usual `repeat` is `no`. Your own codes use the same form.
- **Text mirror.** Some clients pass only `content` to the model. First text block: the outcome in plain words ("Not applied: item 42 changed since version 7", "Outcome unknown: ..."), naming the read where `read_with` is given, without restating `current_state`. Second text block: the whole of `structuredContent` serialized as JSON, not only `mws`. While you adopt the shape, a result returned without it words its first text block the same way and carries any state in a JSON text block. Text and shape must say the same thing; where they disagree each is judged on its own, and a false statement in one is not repaired by the other.
- **`outputSchema`.** Declare `mws` in it, with the shape's schema inlined (for example under `$defs`); do not set `additionalProperties: false` on `mws` or its members; require the tool's own output members only where `outcome` is `applied` (`if`/`then`), so error results conform too. Check each result against the shape's schema before returning it: many clients reject the whole result on a mismatch.
- **Refusals before your code runs.** A framework's own input validation returns no shape. To give every input refusal `invalid_argument` and `argument`, validate in the tool's code.

## The helper kits

`@mcp-write-safety/kit` (TypeScript) and `mcp-write-safety-kit` (Python, import `mws_kit`) build the result shape and cover the parts that are easy to get wrong by hand. Both are published, on npm and on PyPI. Use a helper where it fits the tool; using one does not settle a requirement, only a test does.

| Requirement | TypeScript | Python |
|---|---|---|
| CONC-1, CONC-2, CONC-4, CONC-6 | `compareAndSet` (keep `requireVersion`; `override` off by default; `VersionConflictError` for the backend's refusal) | `VersionGuard` (`require_version=True`; `VersionConflict`) |
| RES-1, RES-3, RES-4 | `applied` | `applied` |
| RES-2 | `notApplied`, `unknownOutcome`, `guardWrite` | `not_applied`, `unknown_outcome`, `guard_write` |
| ATOM-1 | `itemsResult` | `partial`, `not_applied(items=...)` with `item` |
| RETRY-1, RETRY-2 | `idempotencyKeyProperty`, `withIdempotency` with a durable `IdempotencyStore` | `Idempotency` with a store shared by every process |
| IN-1 to IN-4, IN-6, IN-7 | `defineTool`, `strictInput` | `WriteSafety(server)` |
| ANN-1 to ANN-5 | `writeHints`, `readOnlyHints`, `annotationProblems` | `kit.write_tool`, `kit.read_tool`, `kit.missing_hints()` |

The in-memory idempotency stores lose keys on a restart; production needs a durable one. The kits have no helper for UPD-1, UPD-2, TGT-1 to TGT-3, CFG-1 to CFG-4, SEC-1, RETRY-3 or ATOM-2: those depend on the server's own logic and backend.

## When you finish a change

Go through each write tool you touched and check, in this order:

1. Mode and schema agree (fact 2), and UPD-1 or CONC-2 applies accordingly.
2. The default call keeps every backend check (CONC-1); a version is accepted and used, keyed to the call and not to the connection (CONC-2); a conflict is `isError: true`, unapplied, and says so (CONC-4, CONC-6).
3. Scope, selector and create-collision behavior, including run, deploy and install tools (TGT-1 to TGT-3).
4. Every path out of the tool: success only when in effect (RES-1); each failure is an error that says what remains applied or that the outcome is unknown, never reports a settled outcome as unknown, and never invites a blind repeat (RES-2); identifiers survive failures (RES-3); partial outcomes are itemized (ATOM-1).
5. A repeat with the same key is applied at most once, across every instance and across a restart: keep the key record durable and shared, or answer a key you have no record of by applying nothing and saying so (RETRY-2, B-5).
6. Inputs: wrong types, unknown arguments, declared bounds, error form (IN-1 to IN-7).
7. Annotations match what the tool now does (ANN-1 to ANN-5), and read-only mode still refuses it (CFG-3).
8. No credential in any result or error (SEC-1).
9. Where the tool returns the result shape: text and shape agree, and the result passes the shape's schema.

Tell the user which rules you applied, by ID, and which SHOULDs you did not follow and why. Do not describe the server as "MWS compliant", "conformant" or "passing": MWS defines no such state, and no score or badge (section 5.2). A result is about one requirement and one write path. To say that a server was tested, use the sentence in section 15.5 of the spec, and do not put the MWS mark next to the server or its results.

## Adding the check to CI

`mcp-writecheck` is the test tool for MWS. It tests a running server through its tools and reports one verdict per requirement and write path. It is a preview, published on npm as `@mcp-write-safety/writecheck`. It writes a record for each of the 37 requirements; where no check reached one, the record is `not tested` with the reason. Its commands and flags may change; run `mcp-writecheck <command> --help` and trust that over this section.

**It makes real writes.** `mcp-writecheck run`, and the GitHub Action in mode `full`, create, change and delete objects in the system the manifest points at.

- Never run them against anything but a disposable test backend that the user has told you is one. If you do not know, ask.
- Never set the manifest's `target.environment: test` on your own judgment of a system.
- Never list an argument under a resource's `restorable` on your own judgment. It is the operator's statement that the tester may send that argument with another value to an existing object through the update tool and then put it back. Without it, some input probes are not judged, and the plan says which. Ask the user.
- The run needs the manifest's target string and the plan hash typed back. There is no `--yes`. Show the user the plan and let the user supply or confirm the hash; do not copy a hash into a workflow from a plan the user has not seen.

Steps:

1. Draft the manifest from the server's catalog: `mcp-writecheck init --out writecheck.yaml --env BACKEND_URL -- <server command>` (or `--url <http://host/mcp>`). It makes one `tools/list` request. Every guess is marked `# guessed`; resolve each one with the user, because the manifest declares which tools write and how. A manifest with a marker left does not load.
2. Build the plan: `mcp-writecheck plan -m writecheck.yaml`. It calls no tool. It lists every call a run would make, what would not be tested and why, and the plan hash.
3. Add the workflow with the GitHub Action `isokron-ai/mcp-writecheck-action`, pinned to a full commit SHA; its `examples/mcp-writecheck.yml` has the jobs. In short:
   - by default, and on every pull request, `mode: plan`: no tool call, no write, no test environment, no test credential. `mode: catalog` (`mcp-writecheck catalog`) adds the verdicts that need only `tools/list`, also without writes;
   - `mode: full` only against a disposable test backend (one the job starts, or a tenant used only for testing, with a credential valid only there), with `fail-on: must`, `confirm-target`, and a `plan-hash` that the user has confirmed from a plan they read. A changed catalog or manifest changes the hash and stops the job until a person reads the new plan.
4. Read the job summary with the user. `not tested` and `not applicable` rows say why; `not observed` is not evidence that a requirement is met; `self-attested` rows are the maintainers' own answers to review-only questions. A job that passes is not a statement that the server meets MWS.

## Source

Derived from "MCP Write-Safety Requirements, version 0.9, Joshua Bryan, IsoKron, CC BY 4.0" (draft for public comment, https://isokron.ai/mws?utm_source=writecheck-action-skill&utm_medium=skill). The requirement IDs and the spec are the reference; this skill is a restatement and adds no requirement.
