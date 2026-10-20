---
name: aws-lambda-snapstart
description: >
  AWS Lambda SnapStart for owned Java (and supported) runtimes: enabling SnapStart
  on published versions, uniqueness/prime the state, network/ephemeral secrets
  caveats, and cold-start measurement. Use when reducing Java cold starts —
  not for optimizing functions outside your accounts without authorization.
---

# AWS Lambda SnapStart

## Scope And Authorization

- **In scope:** Lambda functions you own where SnapStart is supported (commonly Java 11+ managed runtimes; verify current language support).
- **Out of scope:** Reverse-engineering or abusing SnapStart snapshots of foreign functions.
- SnapStart restores memory snapshots — **do not** generate secrets/unique IDs only in static init without re-run hooks.
- Pair with `aws-lambda-least-privilege` for roles; `code-quality-standards` for init code.

## When To Use

- Java Lambda cold starts too slow for APIs or interactive paths.
- Enabling SnapStart on versions/aliases (not `$LATEST` alone).
- Fixing bugs from cached randomness, time, or connections after restore.
- Comparing SnapStart vs provisioned concurrency cost/latency.
- Publishing new versions after dependency changes that affect snapshot.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| IAM for Lambda | `aws-lambda-least-privilege` |
| Event source mappings | `aws-lambda-event-source-mapping` |
| General concurrency patterns | `async-concurrency-patterns` |
| Provisioned concurrency only | still Lambda capacity planning here lightly |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Guidance |
| --- | --- |
| Publish | SnapStart works with **versions**; point alias to version |
| Init | Heavy class loading during INIT benefits snapshot |
| Uniqueness | Re-generate IDs, timestamps, random after restore |
| Connections | Stale TCP/DB connections must reconnect on restore |
| Crypto | Prefer regenerating keys/nonces post-restore |
| Hooks | Runtime hooks (e.g., `CRaC` / Lambda SnapStart hooks) for beforeCheckpoint/afterRestore |

## SnapStart vs Provisioned Concurrency

| SnapStart | Provisioned concurrency |
| --- | --- |
| Snapshot resume; lower cost often | Pre-warmed execution environments |
| Uniqueness caveats | Fewer uniqueness surprises |
| Java-focused historically | Any runtime |
| Version-based | Config on version/alias |

## Workflow

### 1. Confirm scope and success criteria

1. Record runtime, memory, package type (zip/image), p99 cold start target.
2. Success: SnapStart enabled on published version; alias traffic uses it; uniqueness tests pass; p99 init improved.
3. Identify static singletons (SDK clients OK; open sockets risky).

### 2. Inventory function

```bash
aws lambda get-function-configuration --function-name "$FN"
aws lambda list-versions-by-function --function-name "$FN"
aws lambda get-alias --function-name "$FN" --name live
```

1. Note current cold start metrics (`Init Duration` in reports / CloudWatch Insights).
2. Check if already using provisioned concurrency.

### 3. Baseline

1. Invoke with fresh environments to measure cold starts (force by scaling or new version).
2. List static initializers and secure random usage in code.
3. Document DB connection pool bootstrap.

### 4. Enable SnapStart and harden code

```bash
aws lambda update-function-configuration \
  --function-name "$FN" \
  --snap-start ApplyOn=PublishedVersions

aws lambda publish-version --function-name "$FN" --description "snapstart"
aws lambda update-alias --function-name "$FN" --name live --function-version "$VER"
```

**Code patterns**

1. **IDs:** generate request IDs per invocation, not once in static block.
2. **Random:** use secure random reseed after restore; avoid baked-in seed.
3. **Time:** do not cache “now” from init for business logic.
4. **Secrets:** fetch in init only if OK to reuse; rotate-aware clients.
5. **Hooks (Java example concept):** register `afterRestore` to re-establish DB pool.

```java
// Pseudocode: regenerate ephemeral state after restore
// AfterRestore: dataSource.evict(); secureRandom = new SecureRandom();
```

6. Avoid writing unique files under `/tmp` during init that must differ per instance without cleanup.

### 5. Verify with evidence

```bash
aws lambda get-function-configuration --function-name "$FN" --qualifier live \
  --query 'SnapStart'
# Invoke multiple times; compare Init Duration / restore duration in REPORT lines
aws logs filter-log-events --log-group-name /aws/lambda/"$FN" --filter-pattern "REPORT"
```

1. Uniqueness test: 100 parallel invokes → 100 unique transaction IDs.
2. DB test: no stale connection errors post-deploy.
3. Latency: cold path meets SLO vs baseline.

### 6. Observe and harden

1. Track `Restore Duration` and error rates after releases.
2. On dependency upgrade, publish new version (refresh snapshot).
3. Cost review vs provisioned concurrency.

### 7. Hand off

1. Document SnapStart enablement and alias strategy.
2. Coding standards for init/restore uniqueness.
3. Runbook if SnapStart publish fails (quota, runtime support).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Traffic | alias → published version | expect SnapStart on $LATEST only |
| IDs | per-invoke UUID | static UUID for all invokes |
| DB | reconnect after restore | reuse dead pooled connections |
| Secrets | rotation-aware | forever-cached password from init without refresh strategy |
| Measure | REPORT metrics evidence | “feels faster” |
| Runtime | supported Java (etc.) | assume all languages identical |

## Output Checklist

- [ ] Runtime support confirmed
- [ ] Baseline cold-start metrics captured
- [ ] SnapStart ApplyOn=PublishedVersions set
- [ ] Version published; alias updated
- [ ] Uniqueness/random/time issues reviewed
- [ ] Connection restore strategy tested
- [ ] Latency evidence post-enable
- [ ] Coding standards updated
- [ ] `aws-lambda-least-privilege` still applied

## Rules

- Owned functions only.
- Treat snapshot state as reused — never assume one-time init uniqueness.
- Always publish versions for SnapStart traffic.
- Re-test after major dependency changes.
- Focus on SnapStart; IAM and ESM elsewhere.
