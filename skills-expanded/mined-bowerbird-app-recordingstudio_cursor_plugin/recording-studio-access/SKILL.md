---
name: recording-studio-access
description: Explain and use Recording Studio Accessible for hierarchy-based access grants to actors. Use when granting, checking, or designing access for users, API clients, AI agents, or other actor types. Do not invent custom access; ask if Accessible is lacking.
---

# Recording Studio access

**Recording Studio Accessible** is the access-control addon for Recording Studio. Add it right after core on a new product (`recording-studio-getting-started`). Access is always about a **recording in the hierarchy under a root**, granted to an **actor**.

The same grant and check path applies whether the actor is a user, an API credential, an AI agent, a workspace, or a future actor type. Predictable results come from treating every actor the same way against recordings — not inventing separate permission systems per actor kind.

## Do not invent custom access

**Recording Studio Accessible is the required approach for access control in this ecosystem.**

Do **not** create:

- custom permission tables or ACL gems for one app
- Devise-only or user-only authorization that bypasses recordings
- parallel "can_access?" helpers that ignore the recording hierarchy
- hand-built `RecordingStudio::Access` rows outside `grant_access`
- admin or API auth that reimplements roles instead of calling Accessible

If Accessible appears to lack a capability for the scenario (for example a new actor pattern, through-access rule, named action, or grant shape), **stop and ask how to proceed**. Do not paper over the gap with custom access code. Prefer extending Accessible, using named actions / through-actors, or confirming product intent before writing anything else.

## Core idea

1. Content lives under a **root** recording (the bucket).
2. Access grants attach to **recordings** at a point in that tree.
3. An **actor** receives a role on a recording.
4. Effective access walks the hierarchy: strongest role on the target or an applicable ancestor up to the root.

Users are not the owners of content. Roots are. Actors only get access to buckets and nodes in the tree.

## Actors

An **actor** is whoever or whatever may act in the system:

| Actor example | Still just an actor? |
| --- | --- |
| User | Yes |
| API access / machine client | Yes |
| AI agent | Yes |
| Workspace, team, or company | Yes, when configured |
| Future identity type | Yes, if allowlisted |

Design rules:

- Pass the actor into Accessible APIs. Do not hard-code "only User".
- Configure which polymorphic types may receive **new** grants with `access_actor_types`.
- Existing grants remain readable and effective even if the allowlist later changes.
- Prefer an explicit allowlist in production. `:all` is security-sensitive and only for intentional open polymorphism.

```ruby
RecordingStudioAccessible.configure do |config|
  config.access_actor_types = ["User", "Workspace", "ApiClient", "AiAgent"]
end
```

`authorized?` and `role_for` are **exact actor checks**. Checking a workspace does not automatically check whether a user can act through that workspace — use `authorized_through?` / `role_through` when one actor should use another actor's grant.

## Grants live on recordings in the hierarchy

Access is not a global user ACL table. Grants are recording-scoped and inherit through the tree.

```text
Root recording (workspace / site / admin root)
├── Folder recording
│   └── Page recording
└── Access grants can sit on any of these nodes
```

Behavior:

- Grant on the **root** → typically covers the whole bucket via inheritance.
- Grant on a **child** → applies at that node; effective role still considers ancestors.
- Direct grants are **additive**. A weaker child grant does not reduce a stronger inherited role.
- Example: root grants `:admin`, child directly grants `:view` → child's direct role is `:view`, effective role is `:admin`.

Enable the capability on host recordables that should allow access children:

```ruby
class Workspace < ApplicationRecord
  recording_studio_recordable label: "Workspace", root: true
  RecordingStudio.enable_capability(:accessible, on: self)
end
```

Without that enablement, placement of `RecordingStudio::Access` under the recordable is rejected.

## Grant and check the same way for every actor

Always use the public API. Do not create `RecordingStudio::Access` rows by hand.

```ruby
result = RecordingStudioAccessible.grant_access(
  recording: recording,
  actor: actor,                 # User, ApiClient, AiAgent, ...
  role: :view,                  # or :edit, :admin, etc.
  manager_actor: current_actor  # who performed the grant
)

raise result.error if result.failure?

RecordingStudioAccessible.role_for(actor: actor, recording: recording)
RecordingStudioAccessible.authorized?(actor: actor, recording: recording, role: :edit)
```

Predictability checklist:

- Same method for every actor type
- Same role vocabulary
- Same hierarchy walk for effective access
- Fail closed when config, placement, or authorization is missing

One actor may hold separate direct grants under different parents. Under one parent, keep a single active direct grant per actor (the grant path deduplicates).

## Through-actors

Sometimes a user acts **through** another actor (for example a workspace grant):

```ruby
RecordingStudioAccessible.authorized_through?(
  actor: current_user,
  through: workspace,
  recording: message_group_recording,
  role: :edit
)
```

This is true only when:

1. `current_user` is allowed to act through `workspace`, and
2. `workspace` itself has the required access on the recording.

Configure `authorize_actor_through` in the host app. By default, actors may only act through themselves.

## Named actions vs recording access

Use ordinary recording access for "can this actor use this recording?"

Use **named actions** for operations that are not just a role on an existing node — for example creating a private child without opening up the whole root:

```ruby
RecordingStudioAccessible.authorized_action?(
  actor: current_actor,
  action: :"recording_studio_messages.create_group",
  recording: site_messages_recording,
  context: { ... },
  controller: self
)
```

Do **not** grant broad root access just to unlock one create flow. Prefer an action permission, then grant ordinary access on the created child recording.

## Mounted access UI

Optional Flatpack UI for managing direct grants:

```bash
bin/rails generate recording_studio_accessible:access_management --link-helper
```

Typical path shape:

```text
/recording_studio_accessible/recordings/:recording_id/accesses
```

Host apps still own account lookup / provisioning hooks. The engine owns grant/revoke. Notifiers own share emails.

## Install sketch

```bash
bin/rails generate recording_studio_accessible:install
bin/rails generate recording_studio_accessible:migrations
bin/rails db:migrate
```

Then:

1. Configure `access_actor_types`
2. Enable `:accessible` on the right recordables
3. Grant with `grant_access`
4. Authorize with `authorized?` / `role_for` (and through/action helpers when needed)

For admin screens that rely on Accessible, also follow `recording-studio-admin`.

## Guardrails

- Use Recording Studio Accessible for access. Do not invent custom access systems.
- If Accessible cannot cover the case, ask how to proceed before coding an alternative.
- Access subjects are actors; content owners are roots.
- Keep grants on recordings; do not invent parallel permission tables for users only.
- Prefer hierarchy inheritance over copying the same grant onto every child.
- Fail closed: blank actor allowlists reject new grants; missing through hooks deny through-access.
- Treat API and AI actors as first-class — same APIs, same predictable hierarchy rules.
