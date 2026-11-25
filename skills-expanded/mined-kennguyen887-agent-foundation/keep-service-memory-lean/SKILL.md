---
name: keep-service-memory-lean
description: Use when a service OOMs / its tasks restart after a PR that added a dependency, when memory-tight replicas (small containers — e.g. 512MB/1GB) die under load or on deploy, or whenever the proposed fix for memory pressure is "just give it more RAM". Also use proactively when ADDING a heavy or optional library (cloud/vendor SDK, PDF/image/ML/crypto lib) to a long-running service. The discipline: keep per-process RSS lean by lazy-loading cold-path dependencies, and treat a memory regression as a code smell to hunt — not a reason to upsize the host. Covers the reservation-vs-actual-RSS + deploy-2x-surge mechanism that turns a small boot-memory regression into a full OOM outage. Principle-first; Node/ESM examples, ports to any language/orchestrator.
metadata:
  last-updated: 2026-06-28
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Keep service memory lean

## When to use
- A service **OOMs / restarts / fails its health check after a deploy**, and the diff added a library — especially a heavy one only used on a rare path (a PDF/image parser, a cloud or vendor SDK, an ML/crypto lib).
- Tasks die on **small replicas** (512MB / 1GB containers) under load or *specifically during a rolling deploy*, while the same image is fine when given lots of RAM.
- Someone proposes **"just bump the memory limit / upsize the host"** as the fix for memory pressure.
- You are **about to add a heavy or optional dependency** to a long-running service and want it to not cost RAM on every replica forever.

Trigger phrases: "OOM after merge", "tasks keep restarting", "works on a big host but not the small one", "just give it more RAM", "boot memory went up", "health check 503 after deploy on a memory-tight cluster".

This is the **code/dependency** side of memory pressure. The **ops** side (how to safely scale/restart/recover a live service, health-probe survival, scheduler back-off) is `operate-ecs-services-safely`. Disk **image** size is `containerize-and-ship-a-service` — a different thing from runtime process RSS.

## The one principle
**Runtime memory is a budget paid by every replica, continuously.** A library imported at module top-level is resident for the whole life of the process **× every replica**, whether or not its code path ever runs. Most "we need more RAM" is **accidental** cost (eager heavy imports, whole-payload buffering, unbounded caches), not an essential feature. If the service has no genuinely memory-heavy feature — it does I/O, CRUD, and calls other services — it should fit a small replica comfortably. **A memory regression is a signal to find the accidental cost in code, not to grow the host.** Upsizing hides the regression and normalizes bloat; a small replica is a useful forcing function.

## The discipline (write the code this way)

### 1. Lazy-load heavy / optional dependencies
If a heavy library is only used on a **rare, optional, or feature-gated** path, do **not** `import` it at module top. Load it dynamically inside the function that needs it, and memoize.

```js
// BAD — resident at boot on every replica, even if Claude is never called:
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic({ apiKey: env.KEY });

// GOOD — loads only on first real use; an env with the feature off never imports it:
let _client = null;
async function getClient() {
  if (!_client) {
    const { default: Anthropic } = await import("@anthropic-ai/sdk"); // dynamic import
    _client = new Anthropic({ apiKey: env.KEY });
  }
  return _client;
}
```
Candidates are almost always: cloud SDKs (`aws-sdk` v2 is ~25MB+, `sharp` ~9MB), vendor SDKs (payments, e-sign, banking), document/media parsers (PDF, image, video), ML/NLP, heavyweight crypto. ▸ *Other stacks:* Python `import` inside the function; Go build tags / lazy package init; JVM lazy bean / `Supplier`. Principle: **pay for a dependency only when the code path that needs it actually runs.**

### 2. Don't instantiate heavy clients in constructors or at module load
A singleton that does `new VendorClient()` in its constructor (or at file top) pulls the dep **eagerly** the moment the module is imported anywhere — even if no request ever uses it. Defer client creation to the lazy getter above. A module that merely *defines* a service should cost almost nothing to import.

### 3. Stream, don't buffer whole payloads
Reading an entire upload / file / downstream response into a Buffer makes RSS scale with **payload size × concurrency**. Stream through (pipe) when you can; cap the max size you'll accept. One large file × a few concurrent requests is a classic small-host OOM that no dependency audit will explain.

### 4. Bound every in-memory cache
An unbounded `Map`/object used as a cache grows until OOM. Give it a max size (LRU) and/or TTL. "It's just a small cache" is how slow memory leaks ship.

## The diagnostic (memory regressed / OOM after a change)
1. **Do NOT reach for "upsize the host" first.** An OOM that started with a specific PR is almost always a **newly-added eager dependency** or a new buffering path — find what changed before touching infra.
2. **Measure per-dependency import cost** with a tiny RSS-delta probe (no app boot needed):
   ```bash
   node --input-type=module -e 'const mb=()=>Math.round(process.memoryUsage().rss/1048576); const b=mb(); await import("<suspect-package>"); console.log(`+${mb()-b}MB`)'
   ```
   Run it per suspect. A single import adding tens of MB to RSS, multiplied by replicas and the deploy surge (below), is your outage.
3. **Audit top-level imports for heavy libs on cold paths** and convert them to the lazy pattern (§1–§2). Grep the service for `^import .* from "<heavy-pkg>"` and for client instantiation in constructors.
4. **Re-measure boot RSS** of the real running process and compare against the replica limit **and the 2× deploy ceiling** (next section).

## Why small RSS matters more than the raw number — the mechanism that causes the outage
Two orchestrator facts turn a "small" boot-memory regression into a full outage. Know them, because the raw MB figure alone looks harmless:

- **Schedulers pack by your declared reservation/request, not by actual RSS.** ECS `memoryReservation`, k8s `requests.memory`. If the reservation (say 200MB) is far below real RSS (say 350MB), the scheduler thinks the host has room and **bin-packs more replicas onto it than physically fit** → they OOM under load. Fix: keep RSS near/below the reservation, **or** set the reservation to the real measured RSS so the scheduler stops overcommitting.
- **A rolling deploy momentarily runs ~2× the replicas.** `maximumPercent: 200` / k8s `maxSurge` start the new tasks **before** draining the old. So the memory ceiling must hold at **2× replica count during the deploy window**, not just at steady state — which is exactly why these OOMs trigger *on deploy*, not while idle.

These compound: a heavy eager import inflates RSS → the reservation under-counts it → bin-pack stacks replicas → the deploy doubles them → the host runs out of memory and every task on it dies at once. The lean-code discipline above is what keeps you under that ceiling without growing the host. (Acting on the *live* service safely once this happens — one change, observe, no churn — is `operate-ecs-services-safely`.)

## Verification
- **Per-dep cost is known and small:** the RSS-delta probe (above) for each heavy dependency you kept eager returns a few MB, not tens. Anything large is lazy-loaded (§1).
- **No eager heavy imports / no client-in-constructor:** `grep -rnE '^import .+ from "(aws-sdk|sharp|pdfjs-dist|docusign|plaid|stripe|@anthropic|sequelize|puppeteer)' src/` returns only files that genuinely use the dep on the hot path; the rest use dynamic `import()`. Constructors of singleton services don't `new` a heavy vendor client.
- **Boot RSS fits the 2× deploy ceiling:** start the real service (its actual dev/prod runner), read the process RSS, and confirm `2 × replicas-per-host × boot-RSS  <  host memory` — i.e. a rolling deploy can't OOM the host. If it can't, either trim RSS (this skill) or the reservation/limit is lying to the scheduler (raise the reservation to real RSS).
- **Caches are bounded:** every long-lived in-memory cache has a max size or TTL (`grep` for `new Map()` used as a cache → confirm an eviction policy).

## Related
- `operate-ecs-services-safely` — the ops side: how to scale/restart/recover the live service safely once it's memory-starved (one change, observe, never churn; health-probe survival; scheduler back-off).
- `containerize-and-ship-a-service` — slim **disk image** (multi-stage build). Distinct from runtime RSS, but the same "build heavy, run slim" instinct.
- `integrate-external-services` — where vendor SDKs get added (the prime source of heavy eager imports to lazy-load).
