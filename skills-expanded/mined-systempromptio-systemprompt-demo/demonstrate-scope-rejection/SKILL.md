# Demonstrate Scope Rejection

Prove the `scope_check` stage of the governance pipeline by reaching for a tool
this session is not entitled to call, and being refused.

## When to Use

Use this when the question is *"who is allowed to do this?"* rather than *"is
this input dangerous?"*. The other governance demonstrations turn on the content
of a call — a credential in the arguments, a blocked name. This one turns on
nothing but the identity making it. The same call, from an admin console, would
be allowed. From here it is not.

## What is being refused

The hub exposes `admin_audit_dump`. It returns **every identity's** governance
decisions across the whole deployment: other people's user ids, their session
ids, and what they reached for.

That is a real administrative capability and a real disclosure. It is worth
being clear that it is not a stub — the handler runs a genuine unscoped query
against the audit table, and if the policy chain ever failed to refuse it, a
visitor really would receive the whole spine. A refusal only demonstrates
something if the thing refused could have done the damage.

Two facts make the refusal deterministic:

1. The tool's name carries the `admin_` prefix, and
   `services/governance/config.yaml` lists `mcp__systemprompt__admin_` under
   `policies[id=scope_check].admin_only_prefixes`. Matching is an anchored
   prefix test on the tool name alone — the policy never reads the arguments.
2. This terminal caps every caller at `user` scope, whatever their database
   roles say. `scope_check` exempts `admin` callers, but the exemption cannot
   apply here, because no caller on this surface is ever evaluated as admin.

## How to Use

### 1. A baseline allow, same identity

```
mcp__systemprompt__governance_stats {}
```

This clears `scope_check` and every other stage. Note the identity it reports
on — it is the same identity that is about to be refused. Nothing changes
between this step and the next except which tool is named.

### 2. Reach for the admin-only tool

```
mcp__systemprompt__admin_audit_dump {}
```

Expect a deny naming `policy: scope_check`, with a reason describing a scope
violation: the tool requires `admin`, and the caller does not have it. The
handler never ran, so no rows were read and nothing was disclosed.

Say the timing out loud, because it is the whole difference between governance
and etiquette: the call was stopped at the gate, before the tool was entered.
This is not the model declining to call a tool it judged inappropriate, and not
the tool checking permissions once it had already started. It is a policy the
model does not control refusing to let the call through.

### 3. The part that surprises people

Ask the viewer to consider what happens if they sign in as an administrator and
try again.

The answer is that nothing changes. `scope_check` does grant admins unrestricted
tool access — but this surface resolves scope and then *caps* it, taking the
lower of the caller's real scope and the surface's ceiling of `user`. An
operator signed in as admin sees exactly the enforcement a visitor sees.

So scope here is a property of **the session**, not of the person holding it.
That distinction is the useful one for anyone deciding whether to put an agent
in front of their own systems: privilege is a fact about the context a call is
made in, and it can be lowered by the surface without trusting anything the
agent or the account claims about itself.

### 4. Read the refusal back

```
mcp__systemprompt__governance_stats {}
```

The denial from step 2 is now a row, with `scope_check` named as the deciding
policy, alongside the allow from step 1. Put them side by side: two calls, one
identity, one session, seconds apart, and a different verdict — recorded with
the reason, not merely observed.

## Typical workflow

1. `governance_stats` (step 1) — an allow, establishing the identity.
2. `admin_audit_dump` (step 2) — denied at `scope_check`.
3. Explain the ceiling (step 3) — why signing in as admin would not help.
4. `governance_stats` (step 4) — both verdicts, audited, attributable.

Keep step 4 last. Reading the decision back is what turns the refusal from
something the viewer was told into something they can check.

## Related

- `demonstrate_tool_rejection` — refusal by tool name rather than by caller.
- `demonstrate_governance` — the full four-stage pipeline in one pass.
- `analyse_governance_stats` — spend and latency alongside the verdicts.
- `audit_this_session` — offer this as the finale: the visitor's own receipt,
  itemised off the spine the demonstration just wrote to.
