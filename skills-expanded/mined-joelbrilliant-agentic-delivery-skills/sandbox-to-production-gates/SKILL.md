---
name: sandbox-to-production-gates
description: Defines safe sandbox-to-production promotion gates for agent-built software. Use when deploying, restarting, promoting builds, validating runtime surfaces, checking rollback readiness, or proving that the running production artefact matches the reviewed source commit.
---

# Sandbox to Production Gates

## Overview

Use this skill when an agent wants to move work from local or sandbox into production.

The goal is simple: prove that the reviewed source, built artefact, deployed service, and live runtime are the same thing.

Green tests are not a deployment. A restart is not a deployment. A deployed bundle without smoke evidence is not a deployment.

## When to Use

- Promoting sandbox work to production.
- Restarting services after config or code changes.
- Verifying a deployed UI/API after build.
- Checking whether production is running the expected commit.
- Preparing rollback before risky changes.
- Reporting production status to a user.

## Promotion Gates

### Gate 1: Source truth

Capture:

- repo path;
- branch;
- commit SHA;
- dirty state;
- reviewed diff surface;
- exact files intentionally included.

If there is unrelated dirty work, do not stage it. Isolate the promotion.

### Gate 2: Build truth

Run the real build command for the promoted surface.

Capture:

- command;
- exit code;
- artefact path or bundle name;
- build timestamp or hash when available.

Do not claim a build passed because a dev server still runs.

### Gate 3: Service truth

Identify the actual runtime service:

- service name;
- port;
- process ID;
- environment file;
- working directory;
- last restart time.

Restart only the intended service. Never restart a neighbouring prod service by matching a vague process name.

### Gate 4: Runtime truth

Smoke the live runtime, not localhost in the wrong mode.

Check:

- health endpoint;
- authenticated endpoint if auth exists;
- gateway/worker connectivity if relevant;
- static asset or API version;
- key user workflow;
- logs after startup.

If a public CDN or proxy blocks automation, smoke the backend with the correct Host header and say that is what you did.

### Gate 5: Rollback truth

Before promotion, know the rollback:

- previous commit;
- previous build artefact if retained;
- command to restart old version;
- config backup location;
- data migration reversibility.

If rollback is not known, label the promotion high risk.

## Required Evidence

Return:

```text
Commit promoted:
Build command:
Build result:
Service restarted:
Runtime smoke:
Logs checked:
Rollback path:
Dirty state:
```

## Stop Conditions

Stop and ask or hold if:

- source commit and runtime artefact do not match;
- build artefacts are dirty and uncommitted but production depends on them;
- health returns HTML where JSON is expected;
- auth smoke cannot be run;
- service restarts but gateway/worker truth is degraded;
- rollback path is unknown for a risky change.

## Anti-patterns

- "Tests passed, so prod is fine."
- "I restarted something, probably the right thing."
- "The browser loaded, so the backend is healthy."
- "The build succeeded, so the deployed asset changed."
- "The health endpoint is public and unauthenticated, so auth is fine."
