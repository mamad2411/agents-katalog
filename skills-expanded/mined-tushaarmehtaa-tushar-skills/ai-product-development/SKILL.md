---
name: ai-product-development
description: Build or audit AI features that call tools, stream, or charge for usage. Covers tool-time authorization, reserve-then-settle billing and evals before model changes. Use when adding AI to an app.
license: MIT
---

# AI product development

A model call that works in a demo fails in production in three places: a tool handler that trusts an earlier authorization check, usage charged after the fact under concurrency, and a model or prompt change shipped without an evaluation. Get those three right, then map every UI state to its failure and its charge. Input validation, secret handling and typed routes are assumed.

## Choose a mode

- **Build:** add or change an AI feature. Apply every section that the feature touches.
- **Audit:** review an existing feature. Do not edit unless asked. Report findings ranked by severity, each with `file:line`, the failure it allows, and the fix.
- **Model or prompt change:** swap a model, edit instructions, change tools, retrieval, temperature or output limits. Run [Evaluate before changing a model or prompt](#evaluate-before-changing-a-model-or-prompt) first. Use the `ai-cost-audit` skill when the motive is cost.

A request that says "review", "check" or "is this safe" is Audit. A request to "add", "make", or "wire" is Build. Ask only when the request could be either and the answer decides whether files change.

## Inspect first

Read before asking:

- the AI SDK and its **installed major version** (`package.json` plus the lockfile), the providers, and every place a tool is defined or executed;
- how the server identifies actor and tenant, and how that identity reaches a tool handler;
- the credit, quota or billing path, and whether requests can run concurrently or loop through tools;
- existing eval fixtures, golden outputs, prompt files and telemetry.

Ask only about choices that change the boundary: which tool actions need human approval, the charging policy for cancelled or failed work, and whether work must outlive the request (background job versus stream). Continue with labeled assumptions when the choice is reversible.

## Authorize at tool execution time

Treat the tool name and arguments the model selects as untrusted input from the internet. Retrieved documents, emails and web pages can inject them. Authorizing the chat request does not authorize the action the model picks three steps later.

Inside every consequential tool handler (writes, sends, spends, deletes, grants access, or reads data outside the caller's own scope):

1. **Actor and tenant** come from server-side context the model cannot see or write, never from tool arguments or prompt text. Pass identity through the SDK's server-only context or a closure. In AI SDK 7, `toolsContext` and `runtimeContext` do this (see [the AI SDK reference](references/streaming.md)).
2. **Current resource state.** Load the resource by ID scoped to that tenant. Re-check the policy against its state now, not its state when the conversation started: refundable amount, ownership, status, limits, time windows.
3. **Approval** where the action is irreversible, financial, external or above a policy threshold. Bind the approval to the exact tool, normalized arguments and resource version. Expire it. One approval executes once. Re-check state between approval and execution.
4. **Idempotency around the external mutation.** Derive the key from the tool call or approval ID. Send it to the provider when the provider supports idempotency keys. Otherwise record the intent under a unique constraint before calling out, and return the stored result on retry. Model retries, SDK retries and double-clicked approvals all replay tool calls.
5. **Minimal return.** Return only what the next step needs. Tool output fed back to the model is also untrusted on the next turn.
6. **Audit record:** actor, tenant, tool, argument hash, approval ID, idempotency key, outcome.

Read-only tools still scope every query by tenant. A tool that takes a raw resource ID with no tenant filter is a cross-tenant read.

Stop for the user's decision before letting a model trigger refunds, payments, deletions, outbound messages to third parties, or permission changes without a human approval step.

## Reserve, then settle usage

When usage costs money or credits and requests can overlap or loop, a balance check followed by a deduction afterwards lets parallel requests each pass the check and overspend. Use reservation and settlement instead:

1. **Cap first.** Bound steps, output tokens, tool calls and per-tool paid API cost. Without caps the worst case is unbounded and no reservation is safe.
2. **Reserve** the capped worst case atomically before the first model call, keyed by an idempotency key from the client or request.
3. **Settle** on actual usage across **all** steps plus paid tool calls. SDKs differ on whether `usage` means the last step or the whole run. Check the installed major before reading it (the AI SDK changed this in v7).
4. **Release** the unused remainder. On failure, apply the stated policy for partial work.
5. **Abort and disconnect** are not completion. Settle from the steps that completed plus a stated policy for the step in flight. Settlement runs on the server even when the client is gone.
6. **Recover.** SDK callbacks can fire twice or not at all. Persist the reservation, make settlement idempotent by reservation ID, and sweep reservations that stay open past a timeout.

Use the `credit-metering` skill for the ledger, schema, purchases and provider webhooks. This section decides where reserve and settle sit in the AI request path.

## Evaluate before changing a model or prompt

Never judge a model or prompt change on a few manual tries. Before the change ships:

1. **Build or reuse a set** of representative cases (sampled from real traffic with personal data removed, or realistic stand-ins) and adversarial cases: prompt injection inside retrieved content, cross-tenant IDs in arguments, oversized and empty input, ambiguous requests, inputs that should be refused. With no existing set, start with about 20 representative and 10 adversarial cases. That is a working floor, not a statistical guarantee. Record the count.
2. **Score deterministic checks first:** schema validity, correct tool and arguments, refusal when expected, citations that resolve, latency, cost per case.
3. **For subjective output** (tone, helpfulness, summary quality), keep a held-out set the prompt author never tuned against. Before trusting an LLM judge, run it on examples a human labeled good and bad, and check that it ranks them correctly. Pin the judge model and judge prompt. Report disagreement instead of averaging it away. When taste decides quality (posts, captions, copy), use the `taste-evals` skill for the full method: blind pairwise comparison, judge calibration on real hits and flops, and a pre-registered decision rule.
4. **Run baseline and candidate on the same set.** Repeat nondeterministic cases. Ship only with no regression on must-pass cases, then canary with a rollback path.

If the user wants the change now and no set exists, build the minimal set first and say what it cannot detect.

## UI state and failure matrix

Model the states the chosen interaction actually has: initial, submitted with no token yet, streaming, tool running, awaiting approval, partial, stopped by the user, refused, rate limited or out of credits, failed mid-stream, complete. For each failure, decide all three columns together:

| Failure | Server behavior | User sees | Charge |
| --- | --- | --- | --- |
| Slow first token | Keep the request alive within the timeout | Submitted state, Stop available | Reservation held |
| Mid-stream provider error | Stop, persist the partial result if useful | Partial text marked incomplete, Retry | Settle per partial-work policy |
| User presses Stop | Abort upstream | Partial text kept, Regenerate | Completed steps only |
| Client disconnects | Abort or finish deliberately, never by accident | Restored state on return if persisted | Settled server-side |
| Tool awaiting approval | Hold; no mutation | Exact action and arguments to approve | Nothing for the action yet |
| Tool rejected by authorization | Return a refusal to the model, log it | Plain explanation, no internal detail | Model usage only |
| Out of credits or rate limited | Reject before the model call | Balance or retry time, a next step | Nothing |
| Duplicate submit | Return the original via idempotency key | One answer | Once |

## Vercel AI SDK

Detect the installed `ai` and `@ai-sdk/react` majors first. For API shapes, use Vercel's official `ai-sdk` agent skill when installed, or the docs for that major. Read [the AI SDK reference](references/streaming.md) for the version traps that break billing and validation, the abort behavior, and the caps. For other SDKs, apply the same rules and check that SDK's usage semantics for multi-step runs.

## Verification

- **Build:** test the happy path, then each row of the failure matrix. For tools, test a prompt-injected argument, a cross-tenant resource ID, a state change between proposal and execution, a replayed approval, a provider retry, and a policy-limit breach. Fire concurrent requests against one balance and assert it never goes below the policy floor. Abort mid-run and confirm settlement reflects completed steps. Run the repository's lint, type, test and build commands.
- **Audit:** cite the line for each finding. Mark a finding confirmed only after reproducing it or tracing the full path. Otherwise label it suspected.
- **Model or prompt change:** show baseline and candidate scores on the same set, the judge calibration result for subjective cases, and the rollback path.

## Output

- **Build:** chosen interaction and why, files changed, tool authorization per consequential tool, reservation and settlement behavior, state coverage, verification evidence, remaining provider or production setup.
- **Audit:** findings ranked by severity with `file:line`, failure, fix, and confirmed or suspected.
- **Model or prompt change:** eval set size and composition, scores before and after, regressions, judge calibration, ship or hold recommendation.
