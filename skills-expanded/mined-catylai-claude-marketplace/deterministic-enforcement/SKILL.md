---
name: deterministic-enforcement
description: "Decides whether a rule belongs in a prompt or in code, then builds the gate. Use when a tool must never run before a prerequisite, a spend or security limit has to hold every time, or a prompt rule keeps being violated. Covers PreToolUse decisions with actionable reasons, permission rules, and sandboxing. Not for editing settings files (use update-config); not for auditing existing hooks (use review-hooks); not for when to hand off to a human (use provenance-and-escalation)."
when_to_use: "rule keeps getting ignored, block this tool unless, enforce a spend limit, PreToolUse gate, permission deny rule, sandbox an autonomous agent"
license: MIT
---

# Deterministic enforcement

A prompt raises the odds that Claude follows a rule. A gate in code makes the rule hold every
time. This skill picks which one a requirement needs, and then shows how to build the gate so it
actually works.

## 1. Choose by the blast radius of a single failure

| If one failure would cause | Use |
| --- | --- |
| Financial loss, a security breach, data loss, or a compliance violation | **Programmatic enforcement**: a hook, a permission rule, or a prerequisite gate |
| Only a formatting, style, ordering or tone deviation | **Prompt guidance** |

Ask: if this instruction is ignored once, what is the worst outcome? That answer picks the row.
Making the prompt louder does not move a rule into the first row. "Always verify identity before a
refund" still fails some fraction of the time. The failures land on ambiguous identities and
insistent users, which are exactly the cases the rule was written for.

## 2. A gate reads session state and names the way out

A gate depends on state your code owns, not on what the model intends. For example, the refund
tool stays blocked until an identity lookup has returned a verified customer ID in this session.
Put the check in a `PreToolUse` hook or an Agent SDK permission callback.

Every gate does three things:

1. It blocks the call.
2. It says why, in terms the agent can act on.
3. It names the call that satisfies the prerequisite.

A bare "denied" leaves the agent guessing and burning turns.

## 3. PreToolUse prevents; PostToolUse only reacts

**PreToolUse** runs before the tool executes. Return the decision inside `hookSpecificOutput`:

- `permissionDecision`: one of `allow`, `deny`, `ask` or `defer`.
- `permissionDecisionReason`: shown to Claude on deny; on allow or ask, only to the user.
- Optionally `updatedInput` (to rewrite the call's arguments) or `additionalContext`.

When several hooks respond, the precedence is deny > defer > ask > allow. A command hook can also
block by exiting with code 2 and writing the reason to stderr. The top-level `decision` and
`reason` fields are deprecated for this event.

**PostToolUse** runs after the tool has already executed, so it cannot prevent anything:

- `decision: "block"` only puts the reason next to the tool result. Claude still sees the original
  output.
- `continue: false` stops Claude from processing any further. That can limit follow-on damage, but
  the call that triggered the hook has already happened.
- What PostToolUse is good for is `updatedToolOutput`, which replaces the result before Claude sees
  it. Use it to normalize data (dates to ISO 8601, codes to labels) and to trim bulky payloads.

The most common hook mistake is using PostToolUse to block a policy violation. By the time it
fires, the refund has been issued.

## 4. Hook behaviour that decides whether a gate holds

- **A timeout lets the call through.** A `command` hook on PreToolUse that times out is
  cancelled, and the tool call continues through the normal permission flow. The same happens when
  a hook cannot start, or exits with a code other than 2 while printing invalid JSON. An Agent SDK
  callback that times out on PreToolUse blocks the call instead. For a real control, keep the hook
  fast, set `timeout` explicitly, and back it with a deny rule wherever one can express the policy.
- **Exit code 2 is the block.** Stdout JSON is parsed for every exit code. Other non-zero codes are
  non-blocking errors on most events.
- **Matchers switch between literal and regex.** If a matcher contains only letters, digits, `_`,
  `-`, spaces, `,` and `|`, it is an exact name or list. Any other character turns it into an
  unanchored JavaScript regex, so a stray `.` or `(` quietly changes what it matches.
- **Hook types.** There are five: `command`, `http`, `mcp_tool`, `prompt` and `agent` (the last is
  experimental). A `prompt` or `agent` hook asks a model to decide. That is not a deterministic
  gate, so use one only where judgement is the point.
- **Other events.** The event list grows between releases. Check the
  [hooks reference](https://code.claude.com/docs/en/hooks) rather than a copied list. For
  subagents, validate returned output at `SubagentStop` (see
  [references/patterns.md](references/patterns.md)).

## 5. Hooks and permission rules work together

Rules are evaluated in the order deny, then ask, then allow. The first match wins, and a more
specific rule does not change that order. Anything that matches no rule falls to the permission
mode.

Hooks and rules interact in two ways:

- **A hook `allow` does not bypass rules.** Deny and ask rules still apply after a hook allows a
  call.
- **A hook exit 2 blocks before the rules are checked.** Such a block wins even over a matching
  allow rule. That lets you allow `Bash` broadly and use a hook to reject a few specific commands.

Rule syntax examples: `Bash(npm run test *)`, `Read(//absolute/path/**)` and a bare `Edit`. MCP
tools look like `mcp__<server>__<tool>`; for the full MCP naming and which wildcards each rule type
accepts, see mcp-integration.

Settings precedence, highest first: managed, command-line arguments, `.claude/settings.local.json`,
`.claude/settings.json`, user settings. Permission lists merge across these tiers. Put
safety-relevant rules in managed or project settings, not in a local file that a fresh clone or a
CI runner never sees.

## 6. Match the mode to the autonomy, and fence autonomy with a sandbox

Choose the permission mode by who is there to answer a prompt:

- **`default`, `acceptEdits`, `plan`**: a person is present to answer prompts.
- **`auto`**: a classifier reviews each action instead of the person.
- **`dontAsk`**: anything that would prompt is denied. This is the headless and CI choice.
- **`bypassPermissions`**: no prompts at all. Use it only in an isolated container or VM.

The sandbox confines **Bash, PowerShell and Monitor commands and their child processes** at the OS
level. It does not cover Read and Edit, so those still need deny rules. A strict configuration for
an autonomous agent looks like this:

```json
{
  "permissions": {
    "deny":  ["Read(//**/.env*)", "Read(//**/.ssh/**)", "mcp__*"],
    "allow": ["Read", "Grep", "Glob", "Edit", "Bash(npm run test *)", "Bash(git diff *)"]
  },
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false,
    "filesystem": {
      "allowWrite": ["."],
      "denyRead": ["./secrets"]
    },
    "network": { "allowedDomains": ["registry.npmjs.org"] }
  }
}
```

- `allowUnsandboxedCommands: false` ("strict sandbox mode") removes the escape hatch that lets a
  failed command retry outside the sandbox.
- Network access is limited to `allowedDomains`.
- To stop developers widening the domain list, set `allowManagedDomainsOnly` in managed settings.

This is process-level confinement, not VM-grade isolation. Secrets still need explicit deny rules.

## Examples

<example>
A prerequisite gate. This is a Claude Code command hook: it reads the event JSON on stdin and looks
up its own state by `session_id`.

```js
// hooks/refund-gate.js
const input = JSON.parse(require("fs").readFileSync(0, "utf8"));
if (input.tool_name === "process_refund" && !isVerified(input.session_id)) {
  console.log(JSON.stringify({ hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "deny",
    permissionDecisionReason:
      "Refund blocked: identity not verified in this session. Call get_customer with the " +
      "customer's email, phone, or customer ID, then retry process_refund.",
  } }));
}
```

The model cannot talk its way past the check, and the reason tells it how to comply in one turn.
</example>

<example>
A threshold gate that routes the request instead of only refusing it (Agent SDK callback).

```python
async def pre_tool_use(input, tool_use_id, ctx):
    if input["tool_name"] != "process_refund":
        return {}
    amount = Decimal(str(input["tool_input"].get("amount", 0)))
    if amount > Decimal("500"):
        return {"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"{amount} GBP exceeds the 500 GBP auto-approval limit. Create a manager approval "
                "request with create_approval_request (order id, reason code, customer's issue). "
                "Splitting it into smaller refunds is also blocked.")}}
    return {}
```

It closes the split-the-transaction workaround in the same message as the denial.
</example>

<example>
PostToolUse used for its real job: normalizing the result, not policing it.

```js
// input.tool_response holds the tool's structured output
const r = input.tool_response;
console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: "PostToolUse",
  updatedToolOutput: {
    order_id: r.orderNum,
    status: STATUS_LABELS[r.st] ?? `unknown(${r.st})`,
    placed_at: new Date(r.ts_ms).toISOString(),
    total: `${(r.cents / 100).toFixed(2)} ${r.cur}`,
  } } }));
```

The value has to match the tool's output shape. The model sees one consistent shape, and the
normalization lives in one place.
</example>

More patterns, including subagent lifecycle hooks, the failure modes in detail, and how this maps
to other frameworks, are in [references/patterns.md](references/patterns.md) and
[references/porting.md](references/porting.md).

## Audit a configuration

- List every prompt instruction that begins with "always", "never" or "must". For each one, ask
  whether a single failure would cause financial, security, data-loss or compliance harm. Each yes
  is a missing gate.
- Check that no PostToolUse hook returns `decision: "block"` in the belief that it prevents
  anything.
- Check that every deny reason names the prerequisite call.
- Check that threshold gates also close the split-the-transaction workaround.
- Check that each gate hook has an explicit `timeout`, and that where a rule can express the
  policy, a deny rule backs the hook, because a timed-out command hook lets the call through.
- Check that matchers contain regex characters only where a regex was intended.
- Check that safety rules live in managed or project settings, and that `bypassPermissions` appears
  only inside an isolated environment.

## Verify

Prove the gate fires before you rely on it. Feed the hook a synthetic event and confirm it exits
with code 2 or prints a `deny` decision:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/run-hook-event.sh" \
  --event PreToolUse --tool process_refund \
  --set 'tool_input={"amount": 900}' -- node hooks/refund-gate.js
```

Then run a compliant input and confirm it passes. If the script is not available, pipe a
hand-written JSON payload into the hook command and check the exit code and stdout yourself.

Without a checkout: work from the hook source and settings the user pastes, and state which checks
you could not run.
