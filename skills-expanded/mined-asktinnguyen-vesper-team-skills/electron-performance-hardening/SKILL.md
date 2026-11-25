---
name: electron-performance-hardening
description: This skill should be used when diagnosing or fixing memory pressure, startup overhead, reconnect storms, or duplicated runtime work in Electron applications. Use it for incidents involving session churn, watcher churn, repeated credential reads, noisy logs, or messaging integration retry storms.
---

# Electron Performance Hardening

## Overview

Run this skill when Electron apps show high RSS, startup hangs, reconnect floods, or duplicated background work. Prioritize removing churn and deduplicating repeated reads/work before adding more infrastructure.

## When To Use

Use this skill for requests like:
- "memory crisis", "high RAM", "out of application memory"
- "startup is slow/heavy"
- "reconnect storm", "retry flood", "EFATAL loops"
- "too many watchers", "session churn", "duplicate polling"
- "too much logging / terminal scrollback memory"

## Workflow

### 1) Baseline First

Capture process and startup baseline:
- Use `scripts/profile-electron-memory.sh "<process match>"` for quick RSS snapshots.
- Capture startup logs with timestamps and identify burst windows.
- Record active account/workspace counts to normalize comparisons.

### 2) Locate Churn and Duplication

Check these high-probability waste patterns:
- Worker/session create-destroy loops on periodic jobs
- Per-service duplicate reads of same credential/config at startup
- Multi-account integrations reconnecting simultaneously
- Monitoring all historical bindings/sessions immediately on boot
- Dev logs emitting high-volume repetitive info-level messages

### 3) Apply Hardening Patterns

Prefer these patterns:
- **Pool + reset workers** instead of create/delete per run.
- **Short-lived read cache + in-flight dedupe** for startup secrets/config.
- **Stagger startup** and add **global retry gate** for reconnect loops.
- **Lazy, bounded monitoring** for historical sessions/bindings.
- **Evict inactive message/session data** in memory managers.
- **Rate-limit noisy logs** and keep only high-signal summaries at info level.

### 4) Validate

Validate with:
- Typecheck and tests for changed packages.
- Startup profile comparison (before vs after): peak RSS, retries, watcher count.
- Regression pass on account auto-connect and heartbeat behaviors.

### 5) Ship Controls

Expose tuning controls through env vars with safe defaults, document them, and keep names explicit (e.g., `*_STAGGER_MS`, `*_RECONNECT_GAP_MS`, `*_CACHE_TTL_MS`).

## References

- Read `references/startup-memory-crisis-vesper-20260212.md` for a concrete implementation.

## Scripts

- Use `scripts/profile-electron-memory.sh` to sample Electron/Node process memory during startup experiments.
