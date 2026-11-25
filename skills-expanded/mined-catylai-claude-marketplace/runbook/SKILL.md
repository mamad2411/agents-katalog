---
name: runbook
description: "Writes an on-call runbook for a service or procedure from the repo's manifests, CI and alert definitions, marking gaps TODO(owner). Use when someone asks for a runbook or on-call guide. Not for a live incident (use observability-core:incident-declaration) or a postmortem (use incident-postmortem)."
argument-hint: "<service or procedure name>"
allowed-tools: Read, Glob, Grep, Edit(docs/runbooks/**)
license: MIT
---

# Runbook

Write a runbook for: $ARGUMENTS

The reader is an on-call engineer who did not build the service, paged at 3am. Every command
they read is one they will paste, so a wrong command is worse than a visible gap. Base the
runbook on evidence and mark everything else as a gap for the owner to fill.

If $ARGUMENTS is empty, ask which service or procedure the runbook is for.

## Step 1: Gather evidence

Search the project for anything about the service: Terraform, Kubernetes or Helm manifests,
Dockerfiles, CI and deploy configs, Makefiles and scripts, alert and dashboard definitions,
existing docs, and any `## Observability capabilities` section in `CLAUDE.md`. Note the file
behind each fact, because the runbook cites it.

Check `docs/runbooks/` for an existing runbook with this name. If one exists, read it and update
it in place, keeping sections the owner wrote by hand; ask before replacing it wholesale.

- **Nothing relevant found:** say so, ask the user for the service's owner, deploy method and
  main alerts in one question, and write the runbook from the answers with the rest marked
  `TODO(owner)`.
- **Without a checkout** (web, or no file access): ask the user to paste the manifests, alert
  definitions or notes they have, write from those, and return the runbook inline instead of
  saving it.

## Step 2: Write it

Conventions:

- **Owner** in the header is a team with a named contact. It decides who each `TODO` belongs to.
- **`TODO(owner): <what is missing>`** marks every fact you could not find, with `owner`
  replaced by the header owner's name, or left as the literal `owner` when the owner is unknown.
  One question per TODO, specific enough to answer in a sentence.
- **Commands** come from the evidence (a Makefile target, a CI step, a manifest's resource names)
  and cite their source as `(from <path>)`. A command built from standard tooling for a
  resource you found, such as a rollback for a Deployment in a manifest, cites the manifest.
  A step you cannot ground becomes a `TODO(owner)` rather than a guess.
- **Expected output** follows every command, so the reader knows whether it worked.

Template:

```markdown
# Runbook: <service or procedure>

**Owner:** <team> (<contact>)   **Last reviewed:** <YYYY-MM-DD>   **Escalation:** <who, how, after how long>

## What this is
One paragraph: what the service does, who depends on it, and what healthy looks like
(the metric and its normal range).

## First three things to look at
Dashboards, log queries or commands, each with what normal looks like.

## Alerts
### <alert name> (from <path>)
- **Means:** <what condition fired, in user terms>
- **First checks:** <commands, each with expected output>
- **Likely causes:** <ordered by likelihood>
- **Fix:** <steps>
- **Confirm the fix:** <the check that shows the symptom has cleared>
- **Declare an incident when:** <user impact is confirmed; follow observability-core:incident-declaration>

## Procedures
### <restart | scale | roll back | rotate credentials | fail over>
1. <command> (from <path>)
   Expected: <output>

## Known failure modes
| Symptom | Cause | Fix | Link |
|---|---|---|---|

## Tempting but harmful
Actions that look like fixes and make things worse, each with the reason.

## Open TODOs
Every `TODO(owner)` in this runbook, one per line, so the owner can clear them in one pass.
```

Use today's date for Last reviewed if you know it; otherwise write `TODO(owner)`.

<example>
Evidence: `k8s/payments-worker/deployment.yaml` defines Deployment `payments-worker` in
namespace `payments`; `alerts/payments.yaml` defines `PaymentsQueueBacklog` (queue depth above
5,000 for 10 minutes). No doc says what drains the queue.

```markdown
### PaymentsQueueBacklog (from alerts/payments.yaml)
- **Means:** payments are waiting more than about 10 minutes to be processed.
- **First checks:** `kubectl -n payments get deploy payments-worker` (from k8s/payments-worker/deployment.yaml)
  Expected: READY equals the desired replica count, for example `4/4`.
- **Likely causes:** workers crash-looping; a slow downstream; TODO(payments): which
  downstream calls dominate worker time?
- **Fix:** TODO(payments): is scaling workers safe, or does the downstream rate-limit?
```

The scale step is a TODO rather than a `kubectl scale` command, because the evidence does not
say whether more workers help or overload the downstream.
</example>

## Step 3: Save and hand back

Save to `docs/runbooks/<kebab-name>.md` and give the path. If the write is denied or fails,
return the runbook inline and say it was not saved.

Then summarise in a few lines: the files the runbook was built from, and every `TODO(owner)`
with its question, so the owner can see the gaps without opening the file.

## Verify

Re-read the saved file (or the inline copy) and check:

- Every template section is present, even if its content is a `TODO(owner)`.
- Every command has a `(from <path>)` citation and an expected output.
- The `TODO(owner)` items in the file, the Open TODOs section and your summary are the same list.
  Count them in each; if the counts differ, fix the runbook before handing back.
