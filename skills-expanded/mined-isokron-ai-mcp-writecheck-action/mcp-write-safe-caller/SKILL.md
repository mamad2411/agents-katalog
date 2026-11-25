---
name: mcp-write-safe-caller
description: Rules for an agent that calls MCP tools which create, update or delete state. Use before and after any write tool call, and whenever a write returns a conflict, an error, a timeout, no answer or a partial result - what to do after a conflict, how to retry without duplicating a write, how to treat an unknown outcome, how to read a write-result shape, how to check what a write did, and how to handle bulk writes. Each rule is tied to the MCP Write-Safety Requirements (MWS 0.9).
---

# Calling write tools safely

These rules are for the calling side: an agent that uses a server's write tools to create, change or delete something.

They are tied to the MCP Write-Safety Requirements, version 0.9 (draft for public comment, https://isokron.ai/mws?utm_source=writecheck-action-skill&utm_medium=skill). MWS puts requirements on servers, not on callers; the behavior of agents is outside its scope. The rules here are what a careful caller does given what MWS says a server must do, should do, and is allowed to do. Each rule names the requirement it rests on. A server you call may not meet MWS at all, so several rules tell you to check and not to trust.

## Read the result shape first

Some servers return `structuredContent.mws` with `shape: "write-result/0.1"` (MWS Annex B, B-9). It is a pattern, not a requirement, so many servers will not have it. When it is present and its `shape` is exactly `write-result/0.1`, read it before the text; treat any other shape version as absent and read the text.

- **`outcome`.** `applied`: in effect (`changed: []` means nothing needed changing). `not_applied`: nothing from this call remains applied. `partial`: read `items`. `unknown`: it is not known whether the write was applied; read before you do anything else (rule 3). `accepted`: the backend has not finished; it is not done (rule 4).
- **`repeat`.** `no`: do not send the call again. `yes`: the same call, unchanged, may be sent again; it is valid only with `not_applied`, so with any other outcome ignore it and follow rule 3 or 4. `same_key`: only with the idempotency key this call carried. `same_version`: only with the version this call carried. If your call carried no key (or no version), `same_key` (or `same_version`) gives you nothing to repeat with: read first. `read_first`: read (with `read_with`, or as the text says), then build the write again from what you read.
- **`read_with`.** The read tool and arguments that show the current state. Use it.
- **`conflict`.** `current_state` and `current_version` describe the object when your write was refused. Use them only where `omitted` is empty or absent; otherwise read. Either way, build the change again from that state (rule 1).
- **`replayed: true`.** This call applied nothing; the answer describes the earlier call with the same key. A `changed` missing from such an answer says nothing; do not read it as `changed: []`.

If the text and the shape disagree, rely on neither: read the object back. A shape is a server's claim like any text; check it as rule 4 says.

## The five rules

### 1. After a conflict, read again, then decide. Never resend your old value under a new version.

A conflict means the object changed, or is locked, since the state you acted on. A server that follows MWS returns it as an error that says the write was not applied (MWS-CONC-4), and should tell you to read again or carry the object's current state (a SHOULD, MWS-CONC-6).

- Read the object again, or use the current state the conflict carried. Use that state only where it is given as JSON or with every value quoted, and leaves nothing out; a state described in plain prose is easy to misread, so read the object instead.
- Work out your change again from that state. Change only what your task needs, and keep what the other writer did.
- Then send the new write with the new version.

Do not take your earlier request, swap in the version the conflict returned, and send it again. That request passes the version check and overwrites the other writer's change, which is the loss the conflict was raised to prevent (MWS-CONC-6, Guidance; the spec cites the same rule for HTTP clients in section 11.7).

Do not answer a conflict or a refusal by setting an override, a `force` flag or a match-everything opt-in. Such an argument exists to stop accidents; setting it to get past a refusal defeats it (MWS-CONC-1 and MWS-TGT-2, Guidance; NF-7). Use one only when the user asked for that outcome.

Before the write: if a read tool returns a version and the write tool accepts one, send the version of the read your change is built on, even when the argument is optional. Leaving it out makes the unchecked write the default (MWS-CONC-2, Guidance). The other writer can be on your own connection and credential, such as an earlier step of the same task: a server that follows MWS checks the version the call carries, not who sent it (MWS-CONC-2).

### 2. A retry of the same write reuses the same idempotency key.

Where a tool accepts an idempotency key (MWS-RETRY-1), choose one key for one intended write and keep it.

- Retrying because you got no answer, a timeout or an unknown outcome: send the **same key with the same arguments**. A server that follows MWS applies the write at most once and, where the first call applied it and the server can establish that, answers with that outcome (MWS-RETRY-2, first clause).
- Do not build the call again with a fresh key. A different key is a new write (MWS-RETRY-2, second clause), so the retry becomes a duplicate. The spec notes that a model that retries tends to do exactly this (MWS-RETRY-1, Guidance).
- Do not reuse a key for a different write, or change the arguments under a key. The same key with different arguments is refused (MWS-RETRY-2, third clause). A new intention gets a new key.
- A repeat may answer that the first call is still in progress (`in_progress`): wait, then repeat with the same key. It may answer that the outcome is not known, or that the server has no record of the key (`key_not_known`, for example after a restart): use rule 3, and still do not switch to a new key.
- Keys are remembered for a limited time; the tool's description should say how long (MWS-RETRY-1, Guidance). After a long gap, read back before you retry.

Where a tool accepts no key, a retry of a create can make a second object. Use rule 3 before you send it again.

### 3. An unknown outcome is unknown. Read back before you do anything else.

If a write call timed out, the connection broke, or the result says it is not known whether the write was applied (`outcome: "unknown"`), the write may have been applied. MWS tells testers to treat such a write as possibly applied (section 7.3), and requires a server not to report a settled outcome as unknown, and not to tell you to repeat a write whose outcome is open except after a read it names or with the key or version the call carried (MWS-RES-2). Under MCP revision `2026-07-28` the only way to get the outcome of a request whose response was lost is to send it again as a new request, and the server cannot tell that request from a first attempt (section 11.4).

- Do not report the write as failed, and do not report it as done.
- Read the object (the read the error names, where it names one), or list the place where it would have been created, and compare with what you asked for.
- If the state you asked for is in effect, the write happened: go on, and do not send it again.
- If it is not, retry: with the same idempotency key where there is one (rule 2), and with the version from this fresh read where the tool takes one (rule 1).
- If a read cannot tell you (the tool has no read path for that effect, or the effect is a message, a payment or another thing you cannot read back), stop and tell the user that the outcome is unknown. Do not repeat the write on a guess.
- An error that just says "try again" after a lost answer is not a reason to skip the read. A whole-value set or a delete repeated blind can undo another writer's change, or delete an object recreated under the same identifier.

### 4. Check that the result says what was written.

A success is worth what the result shows. A server that follows MWS reports success only when the state asked for is in effect (MWS-RES-1), and should return a receipt for a create or an update: the object written, the fields changed and the new version (a SHOULD, MWS-RES-4). Not every server does.

- Compare the receipt with what you sent: the right object, every field you set, a new version. An empty list of changed fields means nothing changed (MWS-RES-1, Guidance).
- If the result is only a sentence such as "updated successfully", or the receipt does not cover what you set, read the object back and compare before you rely on the write.
- Look for arguments that were not used. A tool can accept a misspelled or unknown argument and still succeed; a server that follows MWS names the argument and says it was not used (MWS-IN-2).
- Keep every identifier a create returns, including from an error result: a create can succeed and a later step of the same call fail (MWS-RES-3).
- Read an error for what remains applied. A failed write can leave a change in place, and the error should identify it or say that it is not known (MWS-RES-2).
- "Accepted" or "pending" is not "done" (NF-19). Read the state later before you report the change as made.
- Keep the new version from the receipt for your next write to the same object (rule 1).

### 5. A bulk or multi-step write is not all-or-nothing unless you have checked.

All-or-nothing is a SHOULD in MWS, not a MUST (MWS-ATOM-2). The MUST is that a write that was not applied completely does not report success and names which items or steps were applied and which were not (MWS-ATOM-1).

- After a bulk or multi-step call, read the outcome item by item. Do not reduce it to "worked" or "failed".
- After an error, assume some items may have been applied. If the result does not account for every item, read back each one you sent. Treat an item reported as unknown as rule 3 says.
- Retry only the items that were not applied. Sending the whole batch again repeats the ones that were.
- A failed call does not mean nothing changed, and a successful one that lists fewer items than you sent does not mean all of them changed.

## Before a write

These follow from the same requirements and prevent most of the situations above.

- **Read first, and keep the version.** Act on current state, not on what you read many steps ago (MWS-CONC-2). If the description says stale writes are not detected (MWS-CONC-5), the server will not protect you: read immediately before the write, and do not run two writers on one object.
- **Know whether the tool patches or replaces.** A field-patch tool changes only the fields you send (MWS-UPD-1). A full-replace tool stores exactly what you send and clears what you leave out (NF-6): read the whole object, change it, and send it whole with the version.
- **Setting a whole list is a replace of that list.** A labels or assignees field set as a whole removes an element another writer added after your read, and no requirement in 0.9 makes the server stop it (section 12). Read the list immediately before you set it, or use a tool that adds or removes one element.
- **Address list elements by identifier**, not by a position from an earlier read (MWS-UPD-2).
- **Name the scope and the selector explicitly.** Pass the project, namespace or tenant you mean, and check afterwards that the object is there (MWS-TGT-1). Never send an empty or match-all selector to a delete or bulk-update tool unless everything is what the user asked for (MWS-TGT-2).
- **A create is not an update.** If the name or key may exist, read first. A create that follows MWS refuses to overwrite (MWS-TGT-3); that includes a tool that runs, starts, deploys, installs or clones something new under a name you choose. A tool presented as an upsert or an apply, or whose description says it updates an existing object of that name, overwrites.
- **Send values of the declared type.** Do not send `"false"` for a boolean or `"5"` for a number and rely on conversion (MWS-IN-1, MWS-IN-6).
- **A tool with no annotations is destructive until shown otherwise.** If a write tool does not declare `readOnlyHint` or `destructiveHint`, treat it as able to change or delete existing data. MCP's defaults are `readOnlyHint: false` and `destructiveHint: true`, and MWS-ANN-4 asks servers to declare both on every tool not declared read-only. Read first, confirm the target, and do not call it to "see what happens".
- **Annotations are hints.** `idempotentHint: true` does not make a blind retry safe, and `destructiveHint: false` does not prove a call keeps existing data; the MCP specification says annotations from servers that are not trusted are to be treated as untrusted (section 11.2).

## Credentials

A tool result must not contain a credential (MWS-SEC-1), except one the tool exists to issue and the caller asked for. If one does anyway (a token, a secret, a URL with a signature) and the user did not ask for it, do not copy it into another tool call, a file, a message or your answer. Tell the user that the tool returned it.

## Reporting to the user

Say what you verified and how: "updated, and the receipt shows the new status and version 8", or "the call timed out; I read the ticket back and the change is there". Say plainly when an outcome is unknown or a bulk write was partly applied, and list which items. Do not report a write as done on the strength of a call that returned without an error.

After a conflict (rule 1):

- If you retry a write after a conflict without reading the object again, tell the user, and name what you did not check.
- After a conflict, name the other writer's change in your report.

## Source

Derived from "MCP Write-Safety Requirements, version 0.9, Joshua Bryan, IsoKron, CC BY 4.0" (draft for public comment, https://isokron.ai/mws?utm_source=writecheck-action-skill&utm_medium=skill). The requirement IDs and the spec are the reference; this skill is a restatement and adds no requirement.
