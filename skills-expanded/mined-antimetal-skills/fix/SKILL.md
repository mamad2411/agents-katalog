---
name: fix
description: Apply Antimetal's fix for an Issue or Improvement to the user's code or systems. Use when the user wants to fix, resolve, patch, remediate, or apply changes for any Issue or Improvement, or when they say things like "how do I fix this", "what should I change", "apply the fix", "let's resolve it", or when investigation is done and the next step is action.
---

# Fix

You are applying Antimetal's remediation to the user's actual codebase. Antimetal wrote the fix from its view of production and the repository. Your job is to bridge the gap between that and the local code.

## Get the Plan

Call `get_issue_fixes` for an Issue, or `get_improvement_fixes` for an Improvement.

- `remediation: null` means no fix exists yet. Check the report: the investigation may still be running or may have failed.
- `remediation.outcome.kind` says what kind of fix it is:
  - `code_fix`: a change to the code, in the action's `diff`. See Apply It.
  - `operational`: `steps` an engineer runs outside the code, such as a config change or a command.
  - `structured_proposal`: a config ready to import. Today it is a Datadog monitor: `proposal.kind` is `datadog_monitor`, `operation` is `create` and `payload` is the monitor JSON. If the repository manages monitors as code (Terraform, Pulumi), add it there. Otherwise give the user the JSON to import in Datadog. Never use it to change an existing monitor.
  - `no_fix_required`: tell the user its `rationale` and stop.
- If `outcome.needsMoreInfo` is set, tell the user its `explanation` and ask its `requiredInformation` before you apply anything.
- If an action has `changeRequest`, Antimetal already opened that pull request. Show its `prUrl` and review it instead of opening another one.

### Actions

Current results usually have one action with `category: "root_cause"`. Older results can also have `immediate` and `preventative` actions. When several exist:

- **Default: the root cause action.** It solves the problem properly.
- **Immediate first** when the issue is ongoing and hurting users (service down, errors spiking). Stabilize first, then come back to the root cause fix.
- **Preventative last.** Offer it after the main fix, framed as "want to add monitoring so we catch this earlier next time?" Don't apply it automatically.

### What an action contains

- `steps`: `info` steps explain why the fix works, so present them before you change anything. `cli` steps carry a `command`. Never skip a step marked `required: true`.
- `diff`: for a code fix, the `repository`, a `description` of the change written for a coding agent, and `files[]`, each with a `path`, a `status` and a unified `diff`. Older results may carry code steps with `files: [{ filename, language, content }]` instead.

## Apply It

### Code changes

1. **Check the repository.** If `diff.repository` is the repo you are in, try each patch with `git apply --check` first.
2. **Adapt when it does not apply.** The patch was made against the code at investigation time. Find the current file, read the surrounding code, and apply the same intent in the local style.
3. **Read `diff.description`** for what the change is meant to do and how it was verified.

### CLI steps

Adapt paths, package managers and tooling to the local environment. Show every command to the user before you run it. Never execute blindly.

## After Applying

- Suggest how to verify the fix works (tests to run, endpoints to hit, metrics to watch).
- If you open a pull request for an Issue, put the Issue's `issueUrl` in its description so Antimetal can link it. Antimetal reads Issue URLs only, so an Improvement is linked only through `attach_link`.
- If `attach_link` is available, call it with the URL of each pull request, commit, ticket or doc you make or find for the Issue or Improvement, and a sentence on why it is related. Skip Antimetal's own fix pull request.
- Do not mark the Issue resolved when you open a pull request. When a linked pull request merges, Antimetal moves the Issue to Monitoring on its own. If the user fixed it another way and asks, call `update_issue_status` or `update_improvement_status` with `resolved`.
