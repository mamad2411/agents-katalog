---
name: admin-console
description: Builds the privileged back-office of an application so that its power is bounded and every use of it is on record: role-based access with least privilege, an audit log of who did what to whom, actions that are still authorized on the server, no secret shown in the interface, and the operational controls an operator needs. The admin surface is the highest-value target in the system and is built as one. Use when a project needs an admin panel, a back-office or operator tooling.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core]
  outputs: [admin-architecture, role-model, audit-log-design, operator-controls]
---

# Admin Console

The admin console is where a few people hold power over everyone else's data,
which makes it the highest-value target in the system and the place a mistake
hurts most. It is built so that the power is bounded by role, every use of it
is on record, and the interface itself leaks nothing an attacker who reaches it
could use.

## 1. Roles, at least privilege

An admin console is not one god role. It is a set of roles, each holding only
what its job needs.

```
model        name the roles by what they do: support can read a user and reset
             a password, finance can issue a refund, an owner can change a role.
             Not one admin that can do everything.
least        each role holds the narrowest set of powers its job requires; a
             power granted to everyone is a power the weakest account carries
separation   the dangerous actions, granting a role, deleting data, moving
             money, are held by fewer roles than the everyday ones, and the
             most dangerous may require a second person
```

The failure mode is the single all-powerful admin role handed to everyone on
the team, so one phished support account owns the platform.

## 2. Authorization is on the server, always

An admin interface that hides a button the user may not use has hidden nothing;
the request behind the button still exists.

```
server        every admin action checks the role on the server, on the action,
              not in the client that rendered the screen
object level   an admin acting on a record is authorized for that record and
              that action, not merely authenticated as an admin
never          the client deciding what an admin may do; it decides only what to
              show, and the server decides what to allow
```

This is `authorization-design` applied to the highest-privilege surface, where
getting it wrong is worst.

## 3. Every privileged action is on record

The audit log is the difference between knowing what happened and guessing.

```
who           the admin identity that acted
what          the action, and the before and after where it changed data
whom          the record or user it acted on
when          the time
from          the source, where the threat model needs it
```

The audit log is append-only, is not editable from the console it records, and
holds no secret in its entries. An admin console without an audit log is a
console where a compromised account leaves no trace.

## 4. The interface leaks nothing

The admin screen is a screen an attacker most wants to reach, so it shows the
least that does the job.

```
no secret     no API key, no token, no password, no full credential rendered in
              the interface, ever; a secret is referenced, rotated, or shown
              once at creation and never again
minimal data  a support view shows what support needs, not the whole record;
              sensitive fields are masked unless the role and the task need them
no debug      no stack trace, no internal error, no raw record dump in
              production
```

## 5. The operational controls an operator needs

An admin console is also where the system is operated, and those controls are
part of it.

```
user management     find, view, suspend, restore, and act on a user within the
                    role's bounds
configuration       the settings an operator changes, each change audited
feature and limits  toggles and rate limits an operator adjusts, where the
                    product allows
monitoring          the health and the signals an operator reads, without
                    leaving the console to guess
```

Each operational control is itself a privileged action: role checked, audited,
leaking nothing.

## 6. The console is hardened like the front door it is

Everything the rest of the suite requires of a sensitive surface applies here,
more so.

```
access        strong authentication, ideally a second factor for the powers it
              holds; sessions short and revocable
limits        login and sensitive actions rate limited
exposure      the console is not casually reachable; it is behind
              authentication and, where the threat model needs it, network
              restriction
```

## 7. Prohibitions

- No single all-powerful admin role granted to everyone.
- No authorization decided in the client; the server checks every action.
- No privileged action without an audit entry.
- No secret, no full credential, rendered in the interface.
- No debug output, stack trace or raw record dump in production.
- No audit log that the console it records can edit.

## 8. Protocol

1. Model the roles by task, least privilege, the dangerous actions held by
   fewer roles and possibly a second person.
2. Enforce every action on the server, at the object level, per
   `authorization-design`; the client only chooses what to show.
3. Design the append-only audit log: who, what, whom, when, before and after,
   no secret, not editable from the console.
4. Ensure the interface renders no secret and only the data the role and task
   need, with no debug output in production.
5. Build the operational controls as privileged actions: role checked, audited.
6. Harden access: strong authentication and a second factor for the powers
   held, short revocable sessions, rate-limited sensitive actions, restricted
   exposure.

## 9. Auto-critique

Score from 0 to 5: roles are least-privilege rather than one god role, every
action is authorized on the server at the object level, every privileged action
is in an append-only audit log with before and after, the interface renders no
secret and only the needed data, operational controls are themselves audited
privileged actions, and access is hardened with strong authentication and
rate limiting.

Threshold: no axis below 3, average at least 4. Authorization decided in the
client, or a privileged action with no audit entry, scores 0 overall, because
the first lets a crafted request act as an admin and the second lets a
compromised admin act without a trace.

## 10. Interfaces

- Upstream: `engineering-core`.
- Lateral: `authorization-design` for the role and object-level model,
  `authentication-security` for the strong access and second factor,
  `session-security` for the short revocable sessions, `rate-limiting` for the
  sensitive-action limits, `data-privacy` for the minimal-data and masking
  rules, `security-headers` for the response hardening.
- Downstream: `observability` for the operational signals the console surfaces,
  `security-audit` before it ships.
