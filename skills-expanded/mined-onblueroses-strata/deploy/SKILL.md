---
name: deploy
description: "Deploy an authorized target to a remote machine: resolve it from live service state, prepare the correct artifact, use its owned deploy path, and report post-deploy health with rollback evidence. Trigger on deploy, ship to production, or go live."
---

# Deploy

Goal: put one authorized target live and report the state actually serving.

Success means:

- the target, local source, remote path, owner process, and public route are resolved from current VPS state;
- the deployed artifact and source revision are recorded, including the prior version needed for rollback;
- the expected public route is healthy after deployment and its serving process remains stable during the observation window.

Does not count: deploying from a remembered path; reporting success after a failed or skipped post-deploy health check; restarting an already unhealthy process; or replacing a project's deploy behavior with a generic copy/restart.

Stop when health evidence is reported, or a gate fails with the value measured and the safest next action.

```text
/deploy <target>
/deploy <target> --fast   # hotfix: may reuse a suitable artifact; never skips resolution or post-deploy health
```

## Authority and preparation

Production deployment needs an authorization covering this target. Use authorization already granted in the active conversation; do not ask again for the same approved scope. If it is absent or the target changes materially, stop before remote mutation and request it. Preparing or validating an artifact may happen before approval when it does not alter production.

Read `$VPS_RUNBOOK` first. It is the source of current connection, service, and resource guidance; configure it in [config.example](../config.example).

## Deploy

1. Resolve the target from live PM2 and nginx state, then match it to the local source and its public route. Record the process or static owner, remote directory, health route, and source revision. If any mapping is ambiguous, stop and ask; deploy to what nginx or the process manager actually serves.
2. Compare the source revision with the recorded deployed revision when available. Inspect the project's deploy script before using it; prefer it when it owns the artifact copy, restart, or readiness check. Otherwise use the service-specific reference recipe. Do not restart twice because both paths claim ownership.
3. Before remote mutation, capture the prior deployed revision/artifact location and the relevant process state. Prepare the artifact and run the scoped local checks. Refuse a target already crash-looping or a preflight state the VPS reference marks unsafe.
4. Deploy through the resolved owner path. Persist the source revision with the deployed artifact. For a static service, validate and reload its web server; for a managed process, take the post-restart baseline only after the owner reports ready.
5. Verify the live target: its expected public route must return its expected healthy response, and the serving process must remain stable after the post-deploy baseline. Check project error reporting when configured. Keep the command output, timestamps, revision, and prior revision as rollback evidence.

`--fast` may reuse an existing artifact and omit nonessential pre-deploy validation only when that fits the approved hotfix scope. It never skips live target resolution, recording the deployed revision, or post-deploy health and stability checks.

On failure, stop, preserve the evidence, name the prior revision and available rollback path, and roll back only under the applicable project runbook or explicit authorization. Report the target, source and deployed revisions, owner path, health results, checks not run, and exact next action without a fixed report template.
