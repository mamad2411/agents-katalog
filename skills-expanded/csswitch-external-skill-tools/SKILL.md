---
name: csswitch-external-skill-tools
description: "CSSwitch 外部 Skill 安装与卸载的强制路由。MUST use in CSSwitch-managed Claude Science whenever the user asks to install, import, add, uninstall, remove, or delete an external Skill."
---

# CSSwitch external Skill tools

This Skill only routes external Skill operations. It is not an authoring or
publishing workflow. For every request in scope, use the CSSwitch external Skill
connector and its matching tool. Do not load `customize`.

## Install or import

1. Accept a public GitHub repository root, ref root, Plugin/Skill collection,
   or exact Skill directory URL. Preserve it exactly. If the user supplied only
   a name, ask for the URL; do not search for or guess a source.
2. Load the generated connector Skill `mcp-csswitch-skill-installer`.
3. Follow that connector's API and call `install_external_skill` with the exact
   `source_url`. The equivalent REPL call is:

```python
host.mcp(
    "csswitch-skill-installer",
    "install_external_skill",
    source_url=source_url,
)
```

Never call `host.skills.edit` or `host.skills.publish` as a fallback.
Never use Add Skill ZIP or `marketplace.importSkills` as a fallback.
Never download the Skill yourself, use shell/Python filesystem APIs, use a
GitHub credential, or pass staged files to CSSwitch. The CSSwitch host owns URL
resolution, one-archive download, validation, atomic commit, and OPERON
attachment. Repository and collection URLs may install a Nature-like bundle;
this installs only its Skill collection and support resources, not hooks, MCP,
agents, or a complete Claude Plugin runtime.

### Exact-plan confirmation for one fixed-commit Skill

When the user asks to review and explicitly confirm a single-Skill install, and
the supplied `source_url` already contains a 40-hex GitHub commit SHA, first
request a plan without downloading or installing anything into Science:

```python
planned = host.mcp(
    "csswitch-skill-installer",
    "install_external_skill",
    source_url=source_url,
    confirmation={"schema_version": 1, "action": "plan"},
)
```

If it returns `CONFIRMATION_REQUIRED`, show the user its exact source, complete
`effects`, `plan_digest`, expiry, and any degradation. Host access approval is
not the user's confirmation of those effects. Only after an explicit approval,
call once with the returned values unchanged:

```python
host.mcp(
    "csswitch-skill-installer",
    "install_external_skill",
    source_url=source_url,
    confirmation={
        "schema_version": 1,
        "action": "apply",
        "operation_id": planned["operation_id"],
        "plan_digest": planned["plan_digest"],
        "capability": planned["capability"],
    },
)
```

Do not infer, alter, log, or reuse the capability. It expires quickly and is
single-use. Any source, plan, runtime, active-org, expiry, capability, or
operation mismatch requires a new plan and a new user confirmation. This
optional **install** route currently accepts only one exact-commit GitHub Skill;
bundles, Plugins, MCP payloads, and local packages remain outside the install
plan. The separately documented opt-in removal route accepts an already
installed, CSSwitch-owned non-bundle Skill, including a `local_zip` import.

For either explicit-plan operation, if `recovery_required=true`, do not call a
`null` effect field false. `post_effect_observation` is only an immediate host
readback (`observed_true`, `observed_false`, or `unknown`), not a durable
receipt or retry authority. Call operation-id-only `reconcile` and report its
durable projection.

## Uninstall, remove, or delete

1. Extract the exact Skill name from the user's current request. There is no
   default or hard-coded Skill name.
2. If no exact name is present, or more than one installed name could apply, ask
   the user. Never infer a filesystem path.
3. Load the generated connector Skill `mcp-csswitch-skill-installer`.
4. Follow that connector's API and call `uninstall_external_skill` with the
   exact `skill_name`. The equivalent REPL call is:

```python
host.mcp(
    "csswitch-skill-installer",
    "uninstall_external_skill",
    skill_name=skill_name,
)
```

### Exact-plan confirmation for one installed Skill

When the user asks to review and explicitly confirm removal of one installed
CSSwitch-owned Skill, first request a plan. This opt-in route is for one Skill,
not a bundle, and never infers a path or a second name:

```python
planned = host.mcp(
    "csswitch-skill-installer",
    "uninstall_external_skill",
    skill_name=skill_name,
    confirmation={"schema_version": 1, "action": "plan"},
)
```

If it returns `REMOVAL_CONFIRMATION_REQUIRED`, show the user the exact Skill and the
complete ordered `effects`. The expected one-Skill effects are native OPERON
detach followed by CSSwitch package quarantine. Host access approval is not
confirmation of either effect. Only after the user explicitly approves that
plan, call once with the returned values unchanged:

```python
host.mcp(
    "csswitch-skill-installer",
    "uninstall_external_skill",
    confirmation={
        "schema_version": 1,
        "action": "apply",
        "operation_id": planned["operation_id"],
        "plan_digest": planned["plan_digest"],
        "capability": planned["capability"],
    },
)
```

Do not infer, alter, log, or reuse the capability. It is short-lived and
single-use; removal apply is operation-authoritative and carries no
`skill_name` or bundle field. Any Skill, plan, runtime, active-org, expiry,
capability, or operation mismatch requires a new plan and a new user confirmation. To inspect
an interrupted or completed opt-in operation, call the same tool with only its
`operation_id` and `confirmation={"schema_version": 1, "action":
"reconcile"}`. Reconcile is readback-only: it must not repeat detach,
quarantine, or any other mutation.

If a process stopped after a durable verified first effect but before the
second effect began, use `{"schema_version":1,"action":"continue",
"operation_id":"<original>"}` with no other operation fields. Continue is
not retry: it admits only the exact `Verified → NotStarted` durable prefix,
rechecks the target and owned package, then executes the one remaining effect.
Any expiry, target, ownership, or ledger-shape drift returns
`SKILL_OPERATION_NEW_PLAN_REQUIRED` without mutation.

Omitting `confirmation` preserves the established legacy single-Skill
quarantine-and-manual-detach flow. Bundle, Plugin, and MCP payload boundaries
continue to use their existing flows; do not send this one-Skill confirmation
protocol for them.

The opt-in install plan remains GitHub-exact only. The opt-in removal plan is
source-neutral for a non-bundle Skill already owned by CSSwitch: a current
`local_zip` marker is eligible just like a GitHub marker, because the sealed
subject is the installed marker/content rather than an archive URL.

If the result is `BUNDLE_UNINSTALL_CONFIRMATION_REQUIRED`, do not call any
uninstall or detach tool again yet. Show the user the returned `bundle_name`
and complete `affected_skill_names` list, explain that the operation is
whole-bundle only, and ask for an explicit confirm or cancel decision. If the
user cancels, stop without another tool call. If the user explicitly confirms,
call the same tool once more with the same `skill_name` and the exact returned
`bundle_id` as `confirm_bundle_id`:

```python
host.mcp(
    "csswitch-skill-installer",
    "uninstall_external_skill",
    skill_name=skill_name,
    confirm_bundle_id=bundle_id,
)
```

The confirmed call re-finds and re-verifies the installed bundle. If it returns
a new `BUNDLE_UNINSTALL_CONFIRMATION_REQUIRED`, show the new membership and ask
again. Never infer or retain an older bundle ID, never confirm on the user's
behalf, and never offer partial physical deletion of bundle members.

Never call `host.skills.delete`, `skills.deleteDraft`, `host.skills.edit`, shell
commands, Python filesystem APIs, or manual filesystem deletion as a fallback.
Do not locate similarly named directories outside the CSSwitch-managed Science
data directory. If the MCP call fails, report that failure and stop.

## Result handling

For `HOST_ACCESS_REQUIRED`, submit the returned `request.payload` exactly once
under its original request ID. Then use `poll_external_skill_request` with that
same `request_id`; omit `last_sequence` on the first call, and pass the previous
`PROCESSING.sequence` on later calls. The polling tool waits inside the gateway
and returns bounded `phase`, heartbeat timestamps, elapsed time, and
`deadline_at`, or the final response. Do not read the bridge files repeatedly,
run `sleep`, or start a shell/Python polling loop. Never write the request again
and never call the install/uninstall tool again merely because a bundle is still
downloading. Success, failure, timeout, and interrupted-host recovery all arrive
as a final response after `.processing` is cleared.
`REQUEST_INTERRUPTED` is final and retryable through one new MCP call; CSSwitch
will verify any possible committed state before changing files again.

For `INSTALLED_ATTACHED_VERIFY_REQUIRED`, call `skill(skill_name)` in the current
conversation. Report the Skill usable only if that call succeeds. For
`BUNDLE_INSTALLED_ATTACHED`, report that CSSwitch installed and read back the
OPERON binding for the returned number of Skills. Do not call every member with
`skill()` and do not claim that Plugin hooks or MCP servers were installed. For
`FILES_COMMITTED_ATTACH_REQUIRED` or `ATTACH_STATE_UNCERTAIN`, call
`install_external_skill` again with the same URL to let CSSwitch verify the
committed content and retry attachment. Never call `host.agents.attach_skill`
manually.

For single-Skill uninstall, follow the native detach step explicitly returned
by the connector, then verify that `skill(skill_name)` no longer loads. A
`BUNDLE_UNINSTALL_CONFIRMATION_REQUIRED` result is non-mutating and requires the
explicit two-step flow above. A `BUNDLE_UNINSTALLED_DETACHED` result already
means the entire owning bundle was batch-detached and quarantined; do not detach
its members again. Report every response faithfully.
