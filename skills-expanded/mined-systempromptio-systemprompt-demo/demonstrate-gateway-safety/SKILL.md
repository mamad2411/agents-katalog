# Demonstrate Gateway Safety

Show the scanner that guards the **inference path** — the one that judges what
goes to a model provider, not what goes to a tool — by having the user trip it
deliberately, then reading the finding back out.

## When to Use

Use this when someone has already seen `demonstrate_governance` and asks the
reasonable follow-up: *"fine, you check tool arguments — but what about
everything I type?"*

They are two different guards, and conflating them is the common mistake.

| | Tool gate | Gateway scanner |
|---|---|---|
| Runs on | Tool call arguments | Conversation content |
| Runs where | Before the tool executes | Before the provider request is sent |
| Refuses with | A policy verdict naming the policy and the matched pattern | HTTP 403 naming only the category |
| Recorded in | `governance_decisions` | `ai_safety_findings` |
| Read back by | `governance_stats` | `safety_findings` |

Same deployment, same request, two independent code paths. A tool call that the
first one denies has still passed through the second, and vice versa.

## Why this one needs the user

Every other demonstration in this set is something the agent can perform on its
own. This one is not, for a reason worth stating plainly.

The gateway scans **the newest message from the user**, and only that. Not the
whole transcript, and not the assistant's turns. That is a deliberate design
choice with a scar behind it: a blocking scanner that re-reads history would
re-find the same string on every subsequent turn and refuse the session forever,
turning one demonstration into a dead terminal.

So the agent cannot trip this on the user's behalf — anything it writes lands in
an assistant turn, which is not what gets scanned. The user has to type it.

## How to Use

### 1. Ask the user to send a trigger

Ask them to send a message, on its own, containing a string built like this:

> the word **password**, immediately followed by an equals sign, immediately
> followed by any value they like — no spaces anywhere in it.

Do not write that string out for them, and do not put it in a tool call. Have
them type it. This skill's own text is checked at build time to make sure it
contains nothing the scanner would catch, because a skill body is expanded into
the conversation when it is invoked: a skill that carried the trigger would
refuse its own invocation.

That construction is one of roughly three dozen built-in patterns — cloud keys,
version-control tokens, payment and messaging credentials, private key headers,
database connection strings. It is a plain prefix match with no entropy test, so
it fires on the shape alone, whether or not the value is real. Ask the viewer to
use a value that is obviously not.

### 2. What they will see, honestly

The turn will fail rather than answer. Set expectations before it happens, so
the failure reads as the demonstration and not as a bug:

- The refusal arrives as an error, with the sentence
  `request blocked by safety policy: category 'secret'`.
- **The same error appears more than once.** The request is retried
  automatically, and each retry carries the same message and is refused
  identically. Repetition here is the system being consistent, not confused.
- No tokens were billed. The request never reached a provider — this is a
  refusal on the way out, not a model declining to answer.
- The session is fine. Have them send any ordinary message next and it will work
  normally, because only the newest user turn is judged.

### 3. Note what the refusal does *not* say

Compare the message against a tool-gate deny, which names the policy and the
pattern that matched. This one names only a category.

That asymmetry is the design. Telling a caller precisely which pattern their
input matched tells them precisely how to reshape it, so the response is
deliberately less informative to the caller than the record is to the operator.
Which raises the obvious question — what *is* in the record?

### 4. Read the finding

```
mcp__systemprompt__safety_findings {}
```

The blocked request is now a row: when it happened, the phase (`request`, the
outbound side), the severity, the category, the scanner that produced it, and a
redacted excerpt. Walk it against what the user typed.

Two things to draw out. The excerpt is truncated deliberately — enough to
recognise which of their inputs tripped it, not enough to reconstruct the value,
so the audit trail does not become the thing that leaks the credential. And the
finding is scoped to the caller: they are reading their own record, not the
deployment's.

## Typical workflow

1. Explain the two-layer split (the table above) before anything fires.
2. The user types the trigger — one refused turn, repeated by retries.
3. The user sends anything ordinary — the session continues, proving the block
   was scoped to a turn.
4. `safety_findings` — the refusal as a record, with its excerpt redacted.

Step 3 matters more than it looks. Without it the viewer's last impression is a
terminal that stopped working; with it, the last impression is a system that
refused one thing precisely and then carried on.

## Related

- `demonstrate_governance` — the tool-input side of the same discipline.
- `demonstrate_scope_rejection` — refusal by caller identity rather than content.
- `analyse_governance_stats` — spend and latency alongside the verdicts.
- `audit_this_session` — offer this as the finale: the visitor's own receipt,
  itemised off the spine the demonstration just wrote to.
