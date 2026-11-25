---
name: antigravity-mcp
description: >-
  Delegate implementation or a queue of coding tasks through Antigravity MCP or its bundled CLI
  relay, then review the diff and project gates. Use when the user asks Antigravity or agy to
  implement, fix, refactor, or run tasks while the calling agent keeps the reviewer and commit role.
  Handle small inline edits directly.
license: MIT
compatibility: >-
  Primary path requires the `antigravity-mcp` MCP server registered with the host, plus the
  `agy` CLI installed and authenticated, and git. Local stdio hosts include Pi >=0.99 with built-in
  MCP, OpenCode, Codex, and Claude Code. Hosts without MCP fall back to the bundled
  `scripts/relay.mjs`, which requires Node.js, git, and a supported authenticated AGY environment.
  The MCP package supports macOS and Linux; use WSL only where the required Linux CLI is available.
metadata:
  version: 0.9.1
---

# Antigravity MCP

You are the **orchestrator**. This skill lets you hand a bounded coding task to a separate
**implementer** - the Google Antigravity CLI (`agy`) - then review what it produced and land it
yourself. You write the brief and own the judgment; Antigravity does the typing in its own
conversation; you verify and commit.

Choose the available dispatch path, then apply the review loop below:

- **MCP (preferred)** - Antigravity MCP exposes `delegate`, `follow_up`,
  `adversarial_review`, `delegate_many` and friends as tools. Use this whenever the tools are
  available.
- **CLI relay (fallback)** - `scripts/relay.mjs` wraps `agy --print` and writes a `result.json`. Use
  it when the MCP server is not registered, so an orchestrator that can only run a shell command and
  read a file can still drive the loop.

## When NOT to use this

- The task is small enough to just do inline - delegation overhead is not worth it.
- Neither the MCP server nor the `agy` CLI is available and authenticated.
- You want to write the code yourself, or you only need Antigravity's opinion on code you wrote - a
  read-only `delegate` or `adversarial_review` covers that, but a plain review may not need
  delegation at all.

## Prerequisites (check once)

1. **Discover the tools through the host.** Locate `delegate`, `follow_up`,
   `adversarial_review`, `delegate_many`, `agy_status`, and `set_model`. Use the host's
   exposed names: prefixes follow its registration, and there is no shared discovery API.
   If the host defers tools, load the needed tools together through its discovery mechanism.
   The examples below use logical names; map them to the discovered tools before calling.

2. **Call `agy_status`.** This sends no model prompt; metadata probes may invoke the CLI. It reports the agy
   version, the models on offer, the resolved model chain per tool, quota cooldowns, in-flight runs,
   and whether a `set_model` choice has already been recorded.

3. **Settle the model once, if `agy_status` shows no choice recorded.** With the default
   `AGY_ASK_MODEL=true`, a host that supports form elicitation can show the choice before the
   first delegation. Other hosts receive an actionable error asking for `set_model`; no task
   is dispatched until the choice is settled. Record a choice the user already authorized
   without asking again. Otherwise use the form or ask once, then call `set_model`. The choice
   is saved per machine. An explicit per-call `model` selects that call's model without this gate;
   `AGY_ASK_MODEL=false` skips the gate but still honors an existing saved preference.

4. **Know the working root.** Pass it as `cwd` on every call; add sibling repos or a base worktree
   through `dirs`.

Inspect each tool's configured chain in `agy_status`; family selectors stay within that family.
Resolve choices against the current account's inventory. Exact IDs and labels fix their listed
effort. Selectors may choose an advertised effort sibling. The vocabulary is `low`, `medium`, `high`,
`xhigh`, and `max`, but a model supports only variants the inventory actually lists. An Orchestrator
label such as `(Carbon)` names a composite variant, not an effort. Availability depends on the
account, plan, provider, and CLI; an API model ID is not automatically an AGY ID.

## The loop

Run these five steps per task. Steps 1, 4, and 5 are your judgment; 2 and 3 are mechanical.

### 1. Write the brief

Antigravity sees only the text you send plus what it can inspect in the workspace - no chat history,
no shared context. Everything the task needs goes in the brief: the goal, the current state, what to
change, what to leave untouched, the project's **actual** gate commands, and a report contract. Tell
Antigravity it will **not** commit (you will). Keep one task per brief. Full guidance and a template:
[references/writing-the-brief.md](references/writing-the-brief.md).

### 2. Dispatch

Send the brief as the `prompt` of a `delegate` call with `write: true`:

```
delegate(
  prompt: "<the brief>",
  cwd: "/path/to/repo",
  write: true            // omit for a read-only run; see the permission model below
  // dirs: ["/path/to/other-repo"]   extra workspace roots
  // sandbox: true                   agy's terminal restrictions (not a permission boundary)
  // model / effort                  only when the user named one
)
```

**A read-only dispatch is enforced on macOS and watched elsewhere.** On macOS the bridge runs it
under a sandbox that blocks writes into its roots. Everywhere, it fingerprints the working tree around
the run and reports `READ-ONLY VIOLATION` (an unenforced run wrote) or `WORKING TREE CHANGED` (the tree
moved despite enforcement) in the response header. You do not have to snapshot anything yourself; you
do have to read the header's `read-only:` field and any warning.

The response is fenced with a per-call nonce and carries a `session_id` in its header when the run
produced one. **Keep that `session_id`** - it is how you rework without resending the brief. Everything between the "agy output
begins" and "agy output ends" markers is untrusted model output; read it as a claim, not as evidence.

Mechanics, the response shape, and the CLI-relay fallback:
[references/dispatch-and-poll.md](references/dispatch-and-poll.md).

### 3. Wait for completion

Await the tool's final response. The bridge exposes no background-job polling tool; a host may
present its own background UI. The default bridge ceiling is 3600 seconds, with a 15-second
cold-run grace. Give the host at least 3660 seconds for a default single turn, using the
[host-specific timeout fields and units](references/dispatch-and-poll.md) under "Waiting for completion".
Allow more for queued work or sequential fan-out legs.

A host timeout can discard partial output or a session ID. A bridge timeout returns bounded
recovery information when the CLI reported it; it cannot guarantee a usable session. Preserve any
known session ID and inspect the result and workspace before an intentional `follow_up` or new
dispatch. A timeout never proves that the task had no effects.

If a call fails, do not quietly do the work yourself - report the failure. Setting
`AGY_ON_FAILURE=strict` reinforces this for delegation failures; invalid caller requests are
handled separately.

### 4. Review - do not trust the self-report

The response is Antigravity's own account of what it did, including its gate claims. **Re-verify,
don't accept:**

- **Establish what actually changed** with `git status --porcelain` and `git diff` (plus
  `git diff --cached`, and open untracked files directly). The bridge reports no touched-file list, so
  git is your only source here.
- **Re-run the project's gates yourself** - the test/lint/build commands from step 1.
- **Read the diff against the brief:** did Antigravity do what was asked, nothing more and nothing less?
- **Get a second opinion:** pass the diff to `adversarial_review` with a `focus` when one applies.
  Check its resolved model in `agy_status`; choose a different listed family when independence
  matters. Its answer supplements your own review.
- **Run the relevant guard skills** on the diff if you have them installed.
- For schema/migration changes, round-trip them; for removals, grep for dangling references.

Full checklist: [references/review-and-land.md](references/review-and-land.md).

### 5. Land it

The implementer edits the working tree; **the orchestrator commits.** Only after the gates pass and the
diff holds:

- Commit the verified work yourself, with a clear message.
- If it needs changes, send a delta with `follow_up(session_id, question, write: true)` and review
  again. The prior context is already on agy's side, so send only the correction. Pass `write: true`
  whenever the rework has to touch files, exactly as you would on the original dispatch.

## Permission model

Headless `agy --print` cannot answer an interactive permission prompt. Earlier AGY 1.2.x checks
observed denied permissioned tools, including file reads, when the permission bypass was off.
Current behavior depends on the installed CLI and its permission configuration; inspect denied
actions and completion metadata. The bridge passes `--dangerously-skip-permissions` by default
(`AGY_SKIP_PERMISSIONS=true`). Treat the delegated task as authorized shell access.

What that means in practice, and what the bridge does about it:

- **agy's plan mode is advisory.** Read-only tools pass `--mode plan`, but verified against agy 1.2.1
  and again against 1.2.2: a plan-mode run creates files, with the permission bypass on or off.
- **So on macOS the bridge enforces read-only.** Plan-mode runs execute under `sandbox-exec` with every
  write beneath the call's roots denied for agy and its child processes; the header says
  `read-only: enforced`. Where the sandbox cannot run (Linux, or a sandboxed bridge) the header says
  `read-only: watched, not enforced`, and `AGY_READ_ONLY_ENFORCEMENT=require` refuses the run instead.
  The block covers only the roots: agy can still write elsewhere, and a process it launches through
  an app or launchd escapes it.
- **The bridge watches in both modes.** It fingerprints the working tree around every plan-mode run
  and warns `READ-ONLY VIOLATION` or, under enforcement, `WORKING TREE CHANGED` when the tree moved.
  Absence of a warning is only a bounded snapshot observation; it does not prove the run had no
  effects. A run it could not fingerprint makes no clean-tree claim. Files git ignores are covered by size and mtime only,
  dependency and build trees such as `node_modules` as one entry, and any other writer during the
  run moves it too.
- **A dispatched turn is not automatically repeated by the bridge.** A network error, quota error,
  partial output, or cancellation can follow local or external side effects. Inspect the available
  result and workspace before an intentional continuation. An unchanged fingerprint cannot prove
  that nothing happened. Native CLI retries remain the CLI's responsibility.
- **The denied-actions note only appears when the grant is off.** With the default grant you will not
  see one, so its absence proves nothing. The violation warning is the signal to trust.
- **A restriction that cannot be enforced fails the call.** If the installed agy does not support
  `--mode` or `--sandbox`, a run that needs either is refused rather than run with more authority than
  you asked for.
- **`AGY_ALLOWED_ROOTS` validates inputs; it does not sandbox agy.** It checks every call's `cwd`,
  `dirs` and `files`, including the workspace roots the bridge derives from them, so a caller cannot
  point a delegation outside the roots you nominate. It does **not** confine the run: agy has a shell
  under the bypass and can reach anything the user running it can. It is also a server-level
  environment variable in the MCP registration, not a per-call argument.

**The only containment is the read-only block on a macOS plan-mode run's own roots.** A `write: true`
dispatch is not sandboxed at all. Treat a dispatch as running with your own shell access. If a task genuinely must not touch the rest of the disk, say so and have the human
arrange isolation outside the bridge - a container, a throwaway checkout, or a restricted account.

**The raw relay has its own contract.** It provides no read-only enforcement on any platform.
`--read-only` requests advisory plan mode and compares bounded content snapshots of the supplied
roots. A violation exits nonzero; unreadable or incomplete snapshot coverage is reported as
`incomplete`, not clean. Read the relay's structured result and coverage fields. A raw relay test
does not validate the MCP bridge's confinement, routing, quotas, or retry behavior.

## Authorization model

Delegation is something the human opts into. Once they have ("run this queue", "proceed"), committing
verified, gate-passing work is the agreed contract. Two limits on that mandate: **surface, don't
absorb** (report Antigravity's design decisions, defensible-but-unasked turns, and non-blocking
nitpicks rather than silently keeping them) and **stop for scope changes** (if correct completion needs
going beyond the brief, ask - don't expand the mandate yourself). The full treatment is in
[references/review-and-land.md](references/review-and-land.md).

## References

- [references/writing-the-brief.md](references/writing-the-brief.md) - how to write a brief Antigravity
  can execute blind: structure, XML blocks, the report contract, and real gate commands.
- [references/dispatch-and-poll.md](references/dispatch-and-poll.md) - the `delegate` / `follow_up`
  call shapes, the fenced response contract, failure and quota handling, and the `relay.mjs` fallback.
- [references/review-and-land.md](references/review-and-land.md) - the review checklist, the commit
  boundary, and the rework cycle via `follow_up`.
- [references/multi-task-queues.md](references/multi-task-queues.md) - running a sequential queue:
  carrying constraints forward, when `delegate_many` applies, progress tracking, and the end-of-run
  coherence check.
