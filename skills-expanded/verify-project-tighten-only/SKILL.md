---
name: verify-project-tighten-only
description: 'Use in the cc-safety-net repo before finishing any change to how a project policy merges with the user policy or how a merged policy turns into protections: src/core/policy/merge.ts, safety-level.ts, env.ts (levels, capabilities, sessionSafetyLevel), effective-rules.ts, the merge call and normalizePolicyConfig in store.ts, resolveSecretDisabledRules, rule metadata flags (catastrophic, activationCapability, secret defaultOff), or a new field in GuiPolicy / ProjectPolicyProjection. Runs an exhaustive check that CC_SAFETY_NET_PROJECT_TIGHTEN_ONLY really stops a repo''s .safety-net policy from weakening the user''s protection, and explains how to read and update it.'
---

# Verify: a project policy cannot weaken the user policy under tighten-only

## The promise

**Property.** With `CC_SAFETY_NET_PROJECT_TIGHTEN_ONLY=1`, every protection the user policy gives on its own is still given after `mergeProjectPolicy` merges in the project policy.

**Harm if broken.** A user opts into tighten-only so that a cloned repo cannot relax their guard. If the merge misses one weakening, a repo's project policy file silently turns off a destructive-command rule, a capability such as `fail_closed`, or secret protection for a path, and the agent runs what the user meant to block.

## Run it

```bash
bun test tests/core/policy/merge-tighten-only.test.ts
```

It takes about 2 seconds and needs no tool beyond Bun. It also runs in `bun run check` (the pre-push hook and CI), so a break fails the push even if nobody runs it by hand.

## What it checks

The check calls the real code, not a copy: `mergeProjectPolicy(user, project, true, sessionSafetyLevel(user.safety.level, env))` exactly as `loadPolicyConfig` in `src/core/policy/store.ts` calls it. It then turns both the user policy alone and the merged policy into a set of **protections** with the same functions the hook uses: `getCCSafetyNetEnvModes` (capabilities, worktree mode), `resolveEffectiveDestructiveCommandRules` (which destructive rules are on), and `resolveSecretDisabledRules`. It fails if any protection of the user policy is missing from the merged one, and prints at most three counterexamples.

A protection is one of these strings:

| Protection | Present when |
| --- | --- |
| `fail_closed`, `paranoid_rm`, `paranoid_interpreters` | that capability is enabled |
| `no worktree relaxations` | worktree mode is off |
| `rule <id>` | that destructive rule is enabled (catastrophic rules always are) |
| `recursive delete checked in <path>` | destructive protection is on and `<path>` is not in `allow_paths` |
| `secret deny <path>` | secret protection is on and `<path>` is in `deny_paths` |
| `secret rule <id> in <path>` | secret protection is on, the rule is not disabled, and `<path>` is not in `allow_paths` |

Every combination in each group below is tried; nothing is sampled:

| Test | Varied together | Cases |
| --- | --- | --- |
| safety level and capabilities | `CC_SAFETY_NET_LEVEL` (unset or each level), user level, all 27 user override sets, project level (absent or each), all 27 project override sets | 34,992 |
| destructive rule `<id>`, once per rule class | session level, both levels, that rule's own capability override in each scope, both protection switches, the rule's `on`/`off`/absent override in each scope | 23,328 each |
| recursive delete allow paths | user switch (on/off), user allow list (every subset of two paths), project switch (on/off/absent), project allow list (every subset or absent) | 120 |
| secret rules, deny paths, allow paths | both switches, overrides for one default-on and one default-off secret rule in each scope, both deny lists and both allow lists over two paths | 194,400 |
| worktree mode | user value, project value or absent | 6 |

A rule class is one `(catastrophic, activationCapability)` pair in `DESTRUCTIVE_COMMAND_RULE_METADATA`; the check picks the last rule of each class, so a new class is covered without editing the test.

## What it does not cover

- **Path matching.** Paths are two strings. This is sound only because the analyzer's matching only adds coverage per list entry: `isAllowedPathTarget` in `src/gate/analyzer/recursive-delete-targets.ts` and `matchesAllowedPath` / `matchesPolicyPath` in `src/gate/secret/secret-protection.ts` use `some(...)` over the list. If either starts to let one entry cancel another, this check no longer covers paths.
- **Allow paths and catastrophic rules.** The check treats destructive `allow_paths` as reaching only non-catastrophic outcomes, because `recursive-delete-targets.ts` returns `git_metadata_target` and root/home results before it consults allow paths. Secret `deny_paths` win over `allow_paths` in `findSensitivePolicyPathTarget`, and the check models the secret rules that way.
- **Fields across groups.** Each group fixes every other field at the default (`createDefaultGuiPolicy()`, project section absent). A bug where one section's weakening test reads another section's field is caught only if it shows within one group.
- **Other environment flags.** `CC_SAFETY_NET_STRICT`, `_PARANOID`, `_PARANOID_RM`, `_PARANOID_INTERPRETERS`, and `_WORKTREE` are not varied. The first four only switch capabilities on, after overrides, in both the user and the merged policy.
- **Reading the files.** `projectPolicyProjection` and the user-policy validation are not exercised. The check starts from already parsed policies.
- **The command analyzer itself.** The check proves that the merged policy is at least as strict as the user policy. It does not prove that the analyzer blocks what a strict policy says to block.
- **The merge without the flag.** Without tighten-only, weakenings are reported, not ignored, and this check does not apply.

## When it fails

Read the counterexample: `user` and `project` are the two policies, `env` is the environment, and `lost` names the protections the merge dropped. Retell it in the code's words before acting, for example: "the user is at standard with `CC_SAFETY_NET_LEVEL=paranoid`; the project sets `safety.overrides.paranoid_rm: false`; the merged policy has `paranoid_rm` off".

Then decide which of these it is:

1. **A real weakening in product code.** The merged policy really is weaker, and `collectWeakenings` in `merge.ts` did not list it, or `mergeProjectPolicy` kept a field it should have dropped. This is a security bug. Fix the product code, or report it to the user if the change was not meant to touch the merge. Never edit the check to make it pass.
2. **An intended change the check does not model yet.** For example, a new policy field, a new kind of protection, or a capability whose meaning changed. Update the check (see below), and say in the commit message which protection you added or changed and why.
3. **A modeling error in the check.** The protection set says something the hook does not do. Confirm it by reading the hook code named in the table above, then fix `computeProtections`. Do not loosen it so that it stops describing the hook.

If the check passes after your change, still read the "Update it" list: a pass says nothing about a field the check does not look at.

## Update it when the code changes on purpose

- **New field in `GuiPolicy` or `ProjectPolicyProjection` that can relax protection.** Add its protection to `computeProtections`, then add a group (or extend the closest one) that varies the field in both scopes alongside the switch that gates it.
- **New capability in `SAFETY_OVERRIDE_KEYS`.** `CAPABILITY_OVERRIDE_SETS` and the rule classes pick it up through `SAFETY_OVERRIDE_KEYS` and the rule metadata, so no edit is needed. Check that the case count stays small enough to keep the run near 2 seconds.
- **New secret rule category with its own default.** Add a representative id to `SECRET_RULE_CLASSES`.
- **A path matcher that is no longer a plain `some(...)` over the list.** The path abstraction above is no longer sound. Extend `PATHS` with the cases the new matcher can tell apart, or tell the user that the path part is no longer verified.

## Make sure it can still fail

After changing the check, break `merge.ts` on a scratch copy and confirm that the check catches it, then restore the file and confirm `git diff --quiet src/core/policy/merge.ts`. Each of these changes must make at least one test fail:

- In `collectWeakenings`, replace `SAFETY_LEVEL_CAPABILITIES[sessionLevel]` with `SAFETY_LEVEL_CAPABILITIES[user.safety.level]`. This fails the capability group and the capability-gated rules.
- Replace the destructive `wasEnabled` condition `overrides[id] !== 'off'` with `overrides[id] === 'on'`. This fails the default-on rule classes.
- In `mergeProjectPolicy`, pass `project.secret_protection?.allow_paths` instead of `keptPaths(...)`. This fails the secret group.
