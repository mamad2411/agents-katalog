---
name: hear-me
description: Checks voice-dictated requests with a readback and stays active in the current conversation until disabled.
disable-model-invocation: true
argument-hint: "[dictated request|on|off]"
---

# Hear Me

Speech-to-text errors cluster in **brittle terms**: names, commands, flags, paths,
identifiers, acronyms, versions, numbers, negation, and action words. Focus on a brittle term
only when a wrong interpretation would change the action, target, scope, result, or safety.
Accept ordinary wording as given.

## Invocation

Match `on` and `off` without case sensitivity after trimming surrounding whitespace. Treat
them as controls only when they are the entire argument of an explicit skill invocation.
Reply to a control with only a confirmation of the new state.

- No argument or `on`: Enable dictation mode for the current conversation. Reply `Hear Me is
  on for this conversation.`
- `off`: Disable dictation mode. Reply `Hear Me is off.`
- Any other non-empty argument: Enable dictation mode and apply the protocol to that request.
  When this changes the state from off to on, state `Hear Me is on for this conversation.`
  after the `Heard:` readback and before other skill announcements or task work. Do not
  repeat the state for a later request while the mode is already on.

While the mode is on, apply the protocol to every later user message, including typed text
and explicit skill invocations. Controls are the one exception: do not apply the protocol
to an `on` or `off` control, and reply with only the confirmation. Only an explicit `off`
control disables it. Start each new
conversation with the mode off, and keep its state only in that conversation's history.

## Protocol

1. Make a concise `Heard:` readback the first text of the first assistant message for each
   dictated request, before any skill announcement, tool call, or task work. Restate the
   action, target, scope, and all consequential constraints. Use one line when it preserves
   them; otherwise use a short block.
   - Format each correction or assumption as code. Include the original transcript when the
     change is not obvious: `ruff check` (from "rough check").
   - Mark an unresolved phrase and its credible candidates instead of choosing one:
     `[unclear: feature/cash-sync or feature/cache-sync?]`.
   - Replace a secret or sensitive value with a role label such as `[API token]`.
2. Resolve every consequential brittle term before work that depends on it. Use the
   conversation, repository state, and cheap read-only checks to test candidates. Treat a
   term as resolved only when one candidate has direct support and no credible alternative
   remains.
3. The readback is an error check, not a confirmation gate: proceed in the same turn when
   all dependent terms are resolved. When two or more credible interpretations remain, ask
   one focused question, complete every independent part of the request while that part is
   blocked, and mutate state only when the action and its target are both resolved.
