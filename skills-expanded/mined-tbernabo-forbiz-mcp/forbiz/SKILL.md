---
name: forbiz
description: Keep a business's commitments, expected signals, evidence and outcomes in Forbiz so that any later session or any other agent can resume the work instead of starting over. Use it when the user asks you to follow up on something, remember what was promised to whom, track whether an outreach, quote or request got an answer, hand work over to another agent or session, or pick up business work that an earlier session started. Also use it at the start of business work, to see what is already open or overdue before acting. Requires the forbiz MCP server (npx -y forbiz-mcp); no account is needed to start.
---

# Forbiz: commitments an agent can resume

Forbiz is a system of record for a business that agents operate. You write down what you committed to do, the signal you expect back and by when, what you observed, and how it turned out. The next session or the next agent reads it and continues. Forbiz is the source of truth across sessions, and your chat memory is not.

## Before you start

You need the `forbiz` MCP tools (`forbiz_me`, `forbiz_commit` and the rest). If they are not available, tell the user that installing them takes one command, and do not pretend to record anything:

- Claude Code: `claude mcp add forbiz -- npx -y forbiz-mcp`
- Claude Desktop, Cursor or any MCP client: add `{"mcpServers":{"forbiz":{"command":"npx","args":["-y","forbiz-mcp"]}}}`

Without MCP, the same API works over HTTP: read https://forbiz.io/llms.txt.

## When to use it

- The user asks you to send, ask, quote, call or propose something whose answer matters later.
- The user says "follow up", "remind me", "did they answer", "where were we" or "what's pending".
- Work will continue in another session, with another agent, or after a handoff.
- You are starting business work in a workspace that already has history: check what is open first.

Skip it for one-off questions, code edits and anything with no counterpart and no expected answer.

## First time in a session

1. Call `forbiz_me`. It returns the workspace, your identity, your capabilities, the plan and its limits.
   - If it reports `NO_CREDENTIAL`, call `forbiz_start` once with your `agent_name` and the business name. That opens a provisional workspace with no account. The credential is stored locally by the server: never ask for it, print it or paste it anywhere.
   - If it reports `CREDENTIAL_EXISTS`, use that workspace. Pass `replace: true` only when the user explicitly wants a different workspace.
2. Call `forbiz_next` for the single next thing that needs attention, `forbiz_prompts` for everything pending, grouped, or `forbiz_state` for an overview of the workspace.
3. If the work is new, run `forbiz_claim_link` once and give the link to the human owner. The owner claims the workspace with it, and you keep working after the claim.

Plan limits change. `forbiz_me` is the authority, so do not quote limits from memory.

## The cycle

1. **Observe.** `forbiz_add_evidence` with what you saw or were told. Use `kind: "statement"` and `epistemicStatus: "observed"` for something you saw yourself, and a short reusable `subject`, for example `acme/pricing`.
2. **Commit.** `forbiz_commit` with:
   - `description`: the action in one sentence.
   - `commitmentKey`: a short, stable id for the objective, for example `acme/quote-followup`. Always send one.
   - `expectedSignal`: what you expect to see if it worked, for example "Dana replies with a date".
   - `expectedSignalAt`: when that should have happened, in ISO 8601.
   - Optional: `expectedSignalSource` (where to look), `dueAt` (without it the action never becomes overdue), `verb`, `whyThisMove`, `roi`.
3. **Execute.** Do the action itself with your own tools, then call `forbiz_mark_executed`. Do this only after it really happened.
4. **Look for the signal.** When `expectedSignalAt` arrives, check the source and record what you did:
   - Found it: `forbiz_record_signal` with `actualSignal` in plain words and an `outcomeStatus` (`expected`, `partial`, `unexpected` or `deferred`).
   - Looked and did not find it: `forbiz_check_signal` with `result: "not_found_in_source"`, plus the `source` and the `period` you checked. This states where and when you looked. It never states that the other party did not answer.
   - Cannot check: `forbiz_check_signal` with `result: "cannot_check"` and a `reason` (`no_access`, `source_unknown` or `needs_human`).
5. **Close.** Use `forbiz_close` with the outcome, `forbiz_postpone` to move the date with a reason, or `forbiz_close_without_signal` with a reason when no signal will come. Add a `learningNote` when something was learned.

## Resuming work

- To continue a commitment, call `forbiz_commit` again with the same `commitmentKey`. If it is still open, Forbiz refuses with `409 COMMITMENT_ALREADY_OPEN` and returns the open commitment. That is the expected way to resume, not an error to work around.
- `409 POSSIBLE_DUPLICATE` means something similar already exists. Resend with `confirm_new: true` only if it really is a different objective.
- `forbiz_get_action` and `forbiz_action_history` show one action and who changed it. `forbiz_search` and `forbiz_find_evidence` recover context. `forbiz_agents` shows what each agent in the workspace has done.

## Rules

- **Read every refusal.** When Forbiz refuses, the response body says what to do next. Follow it instead of retrying the same call.
- **Evidence is not truth.** What you write is append-only history. To correct something, add a new item with `contradictsEvidenceId`. Nothing becomes workspace truth until a human confirms it.
- **Silence is not rejection.** Record where and when you looked. Do not record what a third party thought or meant.
- **Record only what happened.** Do not mark an action executed, or record a signal, that you have not seen.
- **No secrets in Forbiz.** Never put credentials, passwords or payment data into evidence or descriptions.
- **Forbiz records; it does not act.** Sending a message, paying or calling still happens through your own tools, under the permissions the user gave you. A commitment in Forbiz is not permission to act.

For anything the dedicated tools do not cover (projects, decisions, delegations, outreach, export), use `forbiz_request` with a path from https://forbiz.io/openapi.json.
