---
name: access-control
description: >-
  Use when adding a permission, a role or an ownership rule, when code needs the connected
  user or the tenant, when filtering a list by rights, or on an authz/* rule.
  Authentication, authorization, access scopes, policies, RBAC, ABAC, ReBAC.
allowed-tools:
  - Read
  - Bash(npx ddd-ts-kit generate *)
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit list *)
  - Bash(npx ddd-ts-kit describe *)
---

# Access control

Three questions, three places. API and examples: README of `@ddd-ts-kit/auth`.

| Question | Where | How |
|---|---|---|
| Who is calling? (authentication) | `src/platform/auth/authentication/`, at the boundary | an adapter of the `Authenticator` port turns the credential into a `Session` holding the `Actor`; a route hands `actorOf(...)` to the use case and declares its `security` |
| May this actor do this, on this? (authorization) | `application/authorization/` of the context | permissions as data, required by each use case, decided by the `Authorizer` port in a bus middleware before the handler runs |
| Is this valid at all? (invariant) | `domain/` | "an invoice cannot be paid twice" is not a permission and knows no actor |

The platform side lives in `<platformDir>/auth/`, one folder per question: `authentication/`
(the authenticator, the session of a request, the HTTP boundary), `authorization/` (the
authorizer behind the port, the guard of the buses, the access policies, the `Role` vocabulary,
the registry of permissions, the grants of every signed-in person), then the folder of the
model: `roles/`, `attributes/`, `relationships/` or `custom/`. A project generated before the
folders keeps them flat: read and write them there, or run `npx ddd-ts-kit platform-folders`
when the team asks for the move (it moves the whole platform: `composition/`, `observability/`,
`jobs/`, `audit/search-audit-entries/` too).

Under `stack.authz: rebac`, read [relationships.md](relationships.md) first: who holds a
permission left on the context, the resource each use case names, the searches and the system
actors.

## A permission is mandatory

Nothing is reachable by default (`authz/declared`): the generator refuses a command or a
query without one of the two.

```bash
npx ddd-ts-kit generate command <ctx> <UseCase> --permission <aggregate>.<action> --grant <role> --json
npx ddd-ts-kit generate query <ctx> <UseCase> --public --json
```

- A permission is held by somebody: decide who when you declare it. With roles
  (`stack.authz` `rbac`), `--grant <role>` writes `[Role.<Role>]: [<context>Permissions['<p>']]`
  in `<platformDir>/auth/roles/roles.ts` and adds the role to `authorization/role.ts` when it is new. The
  super-admin `*` alone does not count: a permission no role names is refused to everybody
  else, and `check` warns (`authz/granted`). One meant for administrators only is granted to
  `Role.Admin` by name. A grant to every signed-in person goes in `authorization/signed-in-grants.ts`.
  Under attributes or relationships, `--grant` is refused: give the right in that model.

- The permission is named in the ubiquitous language (`invoice.issue`, not `admin.write`),
  joins `<context>.permissions.ts`, and its words are checked
  against the glossary.
- Declared style: `@Requires(permissions['invoice.issue'])` or `@Public()` on the message
  class. Explicit style: `.requires(...)` or `.public()` where the handler is registered, which is
  `<context>.module.ts`, or `<module>/<module>.module.ts` with `--module <module>` (the module
  file keeps the context file short). Never a hand-written `application/authorization/*.policy.ts`
  that returns declarations: a policy decides on one element.
- Nothing else for a plain permission: no check in the controller, none in the handler. The
  generated handler spec already proves that an actor without it is refused.
- A guard is another thing: a control at the edge over a set of routes, named in `guards` of
  a `@RouteGroup` or of a controller (`Authenticated`, `HasRole(Role.Auditor)`, `HasScope('invoices:read')`, `TenantMember`, `Public`, or a
  guard of the project in `presentation/http/guards/*.guard.ts`, `shared/presentation/http/guards/` in a context with modules). It reads the caller and the
  request, answers 401 or 403 before the controller runs (before the request is read when it
  decides on the caller alone, through `admit`), and never loads an element
  (`presentation/guard-at-the-edge`). It never replaces the permission: a job or an event
  handler sends the same command without passing any guard. Use a guard for what is true of
  the whole set of routes (signed in, a role, the tenant of the path), a permission or a policy
  for everything that depends on the element.
- A role is never a string in code: it is a key of the vocabulary `Role` of the platform
  (`<platformDir>/auth/authorization/role.ts`), and `generate route-group <ctx> <Name> --role <role>` adds
  the role there. A grant names the permission through its set,
  `billingPermissions['invoice.issue']`, never by its id `'billing:invoice.issue'`.
- `npx ddd-ts-kit describe <ctx>` shows what each use case and route requires; the
  permissions of a context are listed in its `CONTEXT.md`.

## A rule on one element

"Only the author may edit" depends on loaded state:

```bash
npx ddd-ts-kit generate policy <ctx> <Name> --permission <aggregate>.<action> --json
```

A policy is a named, pure, unit-tested class in `application/authorization/*.policy.ts`
(`@Policy(permission, { name: '<context>.<name>' })`); the handler loads the aggregate and
asks `Access.authorize(command.actor, permission, appointment)`, the loaded aggregate named after its concept. Every
handler of a use case requiring that permission must ask it: `authz/policy-asked` reports one that
does not or drops the decision of a `decide`, and at run time its result is refused with `PolicyNotAskedError`, or with `PolicyDenialIgnoredError` when it answers a success with no question on it allowed, and rolled back. The
generators write the question about the message; replace the message by the loaded aggregate. A rule that holds whoever asks ("not after publication") is an invariant: it goes in
the aggregate.

## Searches

Never load then filter in memory. `generate query ... --search` writes a handler that asks the
access scope of the actor (`all`, `none`, a set of ids, or a filter) and hands it to the read
port; the adapter turns it into the query.

A search across many elements asks two questions, under two permissions:

- **May the actor run it?** The requirement of the query.
- **Which elements?** `Access.scope(query.actor, <context>Permissions['folder.view'], 'folder')`,
  the permission of one element, mapped on its type. An empty page for an actor who reaches
  nothing is the right answer, not a leak.

Never put the permission the scope asks in `signed-in-grants.ts` to let the query past the bus:
what those grants cover lists `all` before the model is asked, so every signed-in person reads
every element. When anybody may run the search, grant there its own permission
(`folder.search`) and keep the scope on the permission of the element.

## A field only some callers see

"The patient does not see the internal note" is a right on a field, not a role test in a
serializer or a query (`authz/fields-by-schema`, `authz/in-application`). Mark it on the schema of
the answer, and of the body when the caller sets it:
`withFieldAccess(schema, { internalNote: { read: { permission }, write: { permission }, subject } })`
of `@ddd-ts-kit/http`, decided through `Access` (`fieldDeciderOf`, which `presentation-of.ts`
of the platform wires). It is left out of JSON, XML and CSV alike for a caller who may not read
it, refused with 403 in a body from one who may not set it, absent or read-only in the form of
the route. The handler still authorizes the write itself, for the callers that are not HTTP. A
field shown or hidden is decided without being recorded; a field set is recorded.

The form of a route (`defineForm`) names the permission of its use case, asked as its
`@Requires` asks it: `requires: { permission, subject: (values) => ..., context: (values, actor)
=> ... }`. A caller who may not run the use case gets 403 instead of the form.

## The current actor

- **Use cases**: explicit, the first field of the command or query (`command.actor`).
  Integration event handlers and jobs act as `systemActor('<context>.<name>')`.
- **Infrastructure** that needs it without being handed it (audit columns, tenant scoping,
  log fields): the `ExecutionScope`, opened at the boundary for every request, consumed event
  and job; `ActorContext` is a view of it. Neither is named nor read in `domain/` or
  `application/` (`authz/actor-explicit`).
- **Domain**: never. Pass an identifier named for its role: `approve(approverId)`.

## Choosing the model

The owner's choice (`stack.authz`); all sit behind the one `Authorizer` port, so changing
later replaces an adapter and the permission mapping, not the handlers. Ask, in order, and
stop at the first answer that changes the model (the guide
`docs/guides/choosing-access-control.md` of the kit has a worked preset for each):

1. Does a right depend on **which element**? No: roles.
2. Do users **share** elements, **delegate**, or inherit along a **hierarchy**, and must a list
   show what each one reaches? Yes: relationships (Zanzibar), in the PostgreSQL tuple store of
   the project, or OpenFGA once it outgrows it.
3. Do rights follow **properties** or need **explicit refusals**? Yes: attribute policies over
   roles. No: roles plus a policy per element rule.
4. Do **third parties** act with a limited credential? Add scopes: `HasScope` on the routes,
   the vocabulary in `SessionScopes`.
5. Do **several customers** share the deployment? Add a tenancy strategy (skill
   `ddd-ts-kit:persistence`), roles per tenant, `TenantMember` on the routes of tenant data.

| Model | Fits when | Costs |
|---|---|---|
| roles (`rbac`) | rights follow job functions | role explosion once rights depend on the element |
| attributes (`abac`) | rights depend on attributes of actor, resource, moment | rules spread out; needs tests |
| relationships (`rebac`) | rights follow relations: owner, member of, shared with | tuples to keep in sync; lists need care |

**Why was it refused.** Every authorizer of the kit answers `explain(request)` with the same
decision as `check` and a trace in words; `traceText(trace)` lays it out, `x` before what did
not hold. Use it in a spec or a console when a decision surprises, never in an answer or a log.

## Refuse these shortcuts

| Shortcut | Instead |
|---|---|
| `if (user.role === 'admin')` in a controller or a handler | a permission required by the use case; `HasRole(Role.Admin)` on the route group when the whole set of routes is for admins |
| a guard that loads the appointment to see who owns it | a policy on the permission of the use case |
| a policy declared and a handler that never asks it | `Access.authorize` in every handler of that permission |
| reading the user from a global or the request in a handler | `command.actor` |
| passing the request or the token inward | an `Actor`, mapped at the boundary |
| an `isAdmin` flag on an entity deciding access | roles or relations in the authorizer |
| `if (actor.roles.includes('staff'))` removing a field from an answer | `withFieldAccess` on the response schema |
| authorization in a repository | tenant scoping only there; rights in the application |
| a search permission given to every signed-in person to get it past the bus | a requirement on an enclosing resource; the signed-in grant would make the scope `all` (`authz/scope-narrows`) |

Finish with
`npx ddd-ts-kit check --rule authz/declared --rule authz/in-application --rule authz/actor-explicit --rule authz/fields-by-schema --rule authz/policy-asked --rule authz/granted --rule authz/scope-narrows --rule authz/resource-modelled --rule authz/system-actor-granted`.
Every decision, denials included, is recorded by the audit trail (skill
`ddd-ts-kit:cross-cutting`), the refusals of the guards at the edge too (`onGuardRefusal` of the
HTTP boundary, wired to `auditGuardRefusals`).
