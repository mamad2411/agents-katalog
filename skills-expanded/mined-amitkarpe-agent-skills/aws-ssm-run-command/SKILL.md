---
name: aws-ssm-run-command
description: Use this skill when users ask to run AWS Systems Manager Run Command (send-command/get-command-invocation), wait for terminal status, and collect stdout/stderr evidence with a reliable wrapper flow.
---

# AWS SSM Run Command

## Overview

Use this skill for reliable AWS SSM Run Command operations with a fixed contract:
- send command payload safely
- wait with transient readback retry handling (never resend the mutation)
- return triage evidence (`CommandId`, `Status`, `ResponseCode`, `StdOut`, `StdErr`)

## When To Use

Use this skill when user intent includes:
- `send-command`
- `AWS-RunShellScript`
- `get-command-invocation`
- waiting for command completion
- collecting run evidence for audit or triage

Do not use this skill for:
- State Manager associations
- Automation document workflows
- Patch Manager orchestration

## Inputs Required

- `region`
- target instance id(s)
- command text file
- run comment
- optional AWS profile (if ambient creds are not used)

## Workflow

1. Before a new or repeated send, check the owning run's durable CommandId and
   provider state. If a prior ID exists, read back that exact execution; do not
   send again. Running means wait; terminal means report its result. An unknown
   send outcome means stop and reconcile with SSM, not retry.
2. Build a command file with bash-safe commands. For a durable run, prefer
   `ssm_run.sh --command-id-file <run>/command-id.txt`; it requires and reserves a pending
   marker before sending and resumes readback from a recorded ID.
3. Use `ssm_wait.sh` and `ssm_get_output.sh` for exact-ID readback. Their
   transient API retries do not repeat `send-command`.

This is a mutation guard, not extra ceremony for read-only AWS calls. The
owning repository still supplies approval and any required account/role/region
identity gate. A terminal failure alone does not authorize a new send.

## Pre-send command and evidence checks

- Validate the **actual rendered** `AWS-RunShellScript` commands array, not only
  the source Bash file. Confirm line joining, quoting, selected interpreter,
  helper/prologue order and required environment. For a changed boundary, run
  the final assembled command with harmless fixture values and mocked AWS
  calls; `bash -n` alone is not an execution check. Never send a provider
  command merely to validate rendering.
- Treat `HOME` as optional in non-login SSM shells. Resolve effective-user
  home metadata explicitly when needed, using a task-specific variable instead
  of overwriting `HOME` or modifying authentication/configuration.
- Before dependent steps (for example, a restore), require the application's
  **supported initialization-complete signal** with a bounded wait. A port
  opening, `SELECT 1` or container-running state alone is not proof that a
  concurrent initializer finished. Fail closed on timeout or initializer exit.
- For a terminal failure, retain the **first failing operation**, response
  code and a small sanitized failure category/context in the initial report;
  keep raw stdout/stderr private when they may contain credentials or data.
  Generic `Failed/1` or `exit status 14` without causal context should
  prompt one bounded inspection, not repeated broad diagnostics.
- Bound diagnostic input, runtime and output. Verify any memory cap against
  the actual interpreter footprint; a restrictive virtual-address limit can
  produce `MemoryError` in the classifier itself, not the target workload.
- Report separately: local/rendered-code check, exact SSM terminal result,
  workload outcome and milestone acceptance. A terminal `Success/0` is not
  automatically application readiness or accepted migration evidence.
  Preserve one-send/exact-CommandId reconciliation; an UNKNOWN submission
  never authorizes another send.

## Script Usage

- `scripts/ssm_send.sh`: send command and print `CommandId`
- `scripts/ssm_wait.sh`: wait loop with transient retry window
- `scripts/ssm_get_output.sh`: fetch final invocation output
- `scripts/ssm_run.sh`: orchestration wrapper returning normalized JSON

## MCP route (`aws_sigv4` `run_script` in Codex)

Use this when the thread sends SSM commands through `aws_sigv4` instead of the
wrapper scripts. Same contract: one send, exact-ID readback, no resend on an
unknown outcome. Routing and identity rules: `~/.agent/AWS.md` and
`docs/AWS_SIGV4_PRO_GUIDE.md` in dotfiles. Evidence: work#183 (gg made 494
`GetCommandInvocation` calls for 87 sends, 477 of them one model turn per poll).

All inputs below (profile, region, account, document, targets, IDs) are
**required verified values** from the approved task and the recorded send. The
snippets refuse to run with placeholders. Never infer an account, or switch
profile/role/tool, after a denial.

- **Send:** first record the send intent (unique `Comment`, document, targets,
  region, time), as in Workflow step 1. Then one `SendCommand` with the identity assert
  in the same script. Return only `CommandId`/`Status`/`Comment`, and record
  the `CommandId` before waiting.
- **Send outcome unknown** (proxy 60 s timeout, error, no `CommandId`):
  reconcile only, never send.
  - `ListCommands` has **no server-side `Comment` filter**. Its filter keys are
    `InvokedAfter`, `InvokedBefore`, `Status`, `ExecutionStage` and
    `DocumentName`
    ([reference](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_CommandFilter.html)).
  - List within a bounded window from the recorded send time, plus
    `DocumentName`, with bounded pagination.
  - Client-side, require the exact `Comment`, `DocumentName` and explicit
    `InstanceIds`, with no `Targets`. The account is the asserted identity;
    the region is the call's region.
  - **Supported scope:** the example covers only a `SendCommand` that used
    approved explicit `InstanceIds`. It does not compare `Targets`
    (tag/resource-group) or `Parameters`. For tag/resource-group sends, or
    when parameter equality matters, a match is not proven: treat it as
    **UNKNOWN / NO RESEND** unless it is reconciled separately.
  - `MATCH` (a complete scan and exactly one match) resumes readback of that
    `CommandId`. `NOT_FOUND`, `AMBIGUOUS` or `INCOMPLETE` mean **UNKNOWN / NO
    RESEND**: report and stop.

```python
# run_script code: reconcile an unknown send. Read-only; never sends.
EXPECT = {'account': '<ACCOUNT_ID>', 'region': '<REGION>',
          'comment': '<UNIQUE_COMMENT>', 'document': '<DOCUMENT_NAME>',
          'instance_ids': ['<INSTANCE_ID>'], 'invoked_after': '<SEND_TIME_ISO8601_MINUS_MARGIN>'}
MAX_PAGES = 5
assert not any('<' in str(v) for v in EXPECT.values()), 'set verified inputs'
ident = await call_boto3(service_name='sts', operation_name='GetCallerIdentity',
                         region_name=EXPECT['region'], params={})
assert ident['Account'] == EXPECT['account'], 'identity mismatch'
seen, token, complete = [], None, False
for _ in range(MAX_PAGES):
    p = {'Filters': [{'key': 'InvokedAfter', 'value': EXPECT['invoked_after']},
                     {'key': 'DocumentName', 'value': EXPECT['document']}], 'MaxResults': 50}
    if token:
        p['NextToken'] = token
    r = await call_boto3(service_name='ssm', operation_name='ListCommands',
                         region_name=EXPECT['region'], params=p)
    seen += r.get('Commands') or []
    token = r.get('NextToken')
    if not token:
        complete = True
        break
m = [c['CommandId'] for c in seen
     if c.get('Comment') == EXPECT['comment'] and c.get('DocumentName') == EXPECT['document']
     and sorted(c.get('InstanceIds') or []) == sorted(EXPECT['instance_ids'])
     and not c.get('Targets')]
decision = ('MATCH' if complete and len(m) == 1 else 'AMBIGUOUS' if len(m) > 1
            else 'INCOMPLETE' if not complete else 'NOT_FOUND')
result = {'decision': decision, 'command_id': m[0] if decision == 'MATCH' else None,
          'matches': len(m), 'scanned': len(seen), 'complete': complete}
result
```

- **Wait** inside one bounded exec, never one model turn per poll:
  - `Pending`, `InProgress`, `Delayed` and `Cancelling` are not terminal.
  - Only `Success`, `Failed`, `Cancelled` and `TimedOut` end the wait. A
    missing or unrecognised `Status` never counts as terminal.
  - A thrown tool call, a missing `return_value`, or a brief
    `InvocationDoesNotExist` right after the send is transient readback,
    retried within the budget.
  - Exits are `READBACK_UNAVAILABLE` or `WAIT_DEADLINE`, both carrying the
    original `CommandId`. Both mean **UNKNOWN**: read that ID again later; it
    never authorizes another send.
  - If the runtime cannot hold the wait, report the `CommandId` and resume
    later.

```js
// One Codex exec: wait for an existing CommandId; print only bounded status metadata.
const IN = { profile: "<VERIFIED_PROFILE>", region: "<VERIFIED_REGION>",
             commandId: "<COMMAND_ID>", instanceId: "<INSTANCE_ID>",
             deadlineMs: 15 * 60 * 1000 };   // from the command's own timeout
for (const [k, v] of Object.entries(IN)) if (!v || String(v).includes("<")) throw new Error(`set verified ${k}`);
const code = `
try:
    r = await call_boto3(service_name='ssm', operation_name='GetCommandInvocation',
        region_name=${JSON.stringify(IN.region)},
        params={'CommandId': ${JSON.stringify(IN.commandId)}, 'InstanceId': ${JSON.stringify(IN.instanceId)}})
    result = {k: r.get(k) for k in ('Status', 'StatusDetails', 'ResponseCode')}
except Exception as e:
    result = {'readback_error': type(e).__name__}  # Never return exception text.
result`;
const TERMINAL = ["Success", "Failed", "Cancelled", "TimedOut"];
const end = Date.now() + IN.deadlineMs;
let last = null, readErrors = 0, out;
while (true) {
  let rv;
  try {
    const res = await tools.mcp__aws_sigv4__aws___run_script({ aws_profile: IN.profile, code });
    rv = res?.isError ? undefined : res?.structuredContent?.return_value;
  } catch (e) { rv = undefined; }
  if (rv && typeof rv.Status === "string" && !rv.readback_error) {
    readErrors = 0;
    last = { Status: rv.Status, StatusDetails: typeof rv.StatusDetails === "string" ? rv.StatusDetails.slice(0, 120) : null,
             ResponseCode: typeof rv.ResponseCode === "number" ? rv.ResponseCode : null };
    if (TERMINAL.includes(rv.Status)) { out = { outcome: "TERMINAL", ...last }; break; }
  } else if (++readErrors > 10) { out = { outcome: "READBACK_UNAVAILABLE", last }; break; }
  if (Date.now() >= end) { out = { outcome: "WAIT_DEADLINE", last }; break; }
  await new Promise(r => setTimeout(r, 30000));
}
text(JSON.stringify({ commandId: IN.commandId, ...out }));   // never send again from here
```

- **Privacy by default:** return only bounded status metadata and the original
  `CommandId`. Never print stdout/stderr tails, unknown tool fields or raw
  exception text. The JS waiter projects an explicit allowlist before printing.
- When full stdout/stderr is required evidence, fetch it once at terminal
  state into the run's approved private evidence file. Keep it out of the
  model-visible print. Never fetch raw output for routine polling.

## References

Load only what is needed:
- `references/operation-contract.md`
- `references/failure-map.md`
- `references/examples.md`
