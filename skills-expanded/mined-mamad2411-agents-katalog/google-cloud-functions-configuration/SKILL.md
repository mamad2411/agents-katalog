---
name: google-cloud-functions-configuration
description: >
  Configures Google Cloud Functions Gen1 vs. Gen2 (Cloud Run-backed)
  runtime differences, HTTP/event/CloudEvent triggers, and min/max
  instance scaling settings, including concurrency and cold-start
  tradeoffs unique to each generation. Use when the user asks to
  "choose Cloud Functions Gen1 or Gen2," "set min instances on a Cloud
  Function," "configure a Pub/Sub or Eventarc trigger," "reduce Cloud
  Functions cold start," "migrate a function from Gen1 to Gen2," or
  "why is my Cloud Function scaling past max instances."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# Google Cloud Functions Configuration

## Purpose

Google Cloud Functions ships as two distinct generations with materially
different execution models: **Gen1** runs on a purpose-built, single-
concurrency-per-instance execution environment, while **Gen2** runs on
top of Cloud Run and Eventarc, giving it concurrent requests per
instance, longer timeouts, and larger max instance counts — but also a
different (and in some cases slower) cold-start profile and a different
trigger/IAM plumbing underneath. Picking the wrong generation, or
carrying over Gen1 scaling assumptions (`maxInstances` as a hard
concurrency limit, one request per instance) into a Gen2 function, is a
common source of unexpected throttling, cost, or latency. This skill
covers choosing between generations, wiring triggers correctly for each,
and setting min/max instance scaling deliberately rather than by default.

## When to use

- Deciding between Gen1 and Gen2 for a new function, or evaluating
  whether to migrate an existing Gen1 function.
- Configuring an HTTP, Pub/Sub, Cloud Storage, Firestore, or generic
  Eventarc/CloudEvent trigger.
- Setting `min-instances`/`max-instances` to control cold starts and
  cap cost/blast radius.
- Diagnosing a function that throttles under load despite `max-instances`
  looking generous, or one that cold-starts on every invocation despite
  steady traffic.
- Reviewing an IaC (Terraform/`gcloud`/Deployment Manager) change that
  touches a Cloud Function's generation, trigger, or scaling block.

## Prerequisites & environment

- `gcloud` CLI authenticated against the target project, with the
  `cloudfunctions.functions.*` and (for Gen2) `run.services.*` and
  `eventarc.triggers.*` IAM permissions — Gen2 functions are Cloud Run
  services underneath, and Eventarc-routed triggers need their own
  service account permissions.
- `gcloud components update` recent enough to support `--gen2` and
  Gen2-specific flags (`gcloud functions deploy` gained `--gen2` in the
  `gcloud` CLI well before Gen2 became the default for new deploys in
  the console; always pass the flag explicitly in scripts/CI rather
  than relying on the CLI's current default).
- For event triggers other than Pub/Sub/HTTP: the Eventarc API enabled
  on the project, since Gen2 event triggers route through Eventarc even
  for sources (like Cloud Storage) that Gen1 wired directly.
- A runtime version supported by the chosen generation (check
  `gcloud functions runtimes list --region=<REGION>` since supported
  runtimes and their generation availability change over time — don't
  assume a runtime available in Gen1 is available in Gen2 or vice
  versa).

## Step-by-step guidance

1. **Choose the generation deliberately, not by inertia.** Gen2 is the
   better default for new functions needing larger max instance counts,
   concurrent requests per instance (reducing instance count needed
   under load), longer timeouts, or larger resource allocations — it
   runs on Cloud Run. Gen1 remains simpler and can have a faster
   per-request cold start for very small, single-purpose functions since
   there's no Cloud Run revision layer underneath. Decide once per
   function and be explicit in every deploy path (CLI, Terraform, CI):
   ```bash
   # Gen2 explicit
   gcloud functions deploy order-validator \
     --gen2 \
     --runtime=nodejs20 \
     --region=us-central1 \
     --source=. \
     --entry-point=validateOrder \
     --trigger-http \
     --no-allow-unauthenticated
   ```
   ```bash
   # Gen1 explicit
   gcloud functions deploy legacy-thumbnail \
     --no-gen2 \
     --runtime=nodejs18 \
     --region=us-central1 \
     --source=. \
     --entry-point=makeThumbnail \
     --trigger-bucket=<GCS_BUCKET_NAME>
   ```

2. **Wire triggers according to generation.** Gen1 event triggers
   (`--trigger-bucket`, `--trigger-topic`) call the underlying service
   directly; Gen2 event triggers route through **Eventarc** even for
   the same-looking source, which means the function's runtime service
   account needs `roles/eventarc.eventReceiver` and the Eventarc trigger
   needs its own service account with permission to invoke the
   underlying Cloud Run service:
   ```bash
   gcloud functions deploy image-processor \
     --gen2 \
     --runtime=python312 \
     --region=us-central1 \
     --source=. \
     --entry-point=process_image \
     --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
     --trigger-event-filters="bucket=<GCS_BUCKET_NAME>" \
     --trigger-service-account=eventarc-trigger-sa@<PROJECT_ID>.iam.gserviceaccount.com
   ```
   A Gen2 CloudEvent function receives a standardized CloudEvent
   envelope (`type`, `source`, `data`), not the Gen1-specific event
   payload shape — code written for Gen1's `event, context` signature
   needs a compatibility shim or a rewrite to the CloudEvent
   `functions-framework` signature when migrating.

3. **Set `min-instances` deliberately to trade cost for cold-start
   latency**, not left at the default of zero for latency-sensitive
   paths:
   ```bash
   gcloud functions deploy checkout-api \
     --gen2 \
     --region=us-central1 \
     --min-instances=1 \
     --max-instances=50 \
     --concurrency=40 \
     --cpu=1 \
     --memory=512Mi
   ```
   `--min-instances` keeps that many instances warm continuously — this
   is a direct, ongoing cost, so size it to the smallest number that
   keeps p99 cold-start-affected latency acceptable, not to "always
   warm" by default.

4. **Set `max-instances` against real downstream capacity, and remember
   Gen2's `--concurrency` changes what `max-instances` actually caps.**
   In Gen1, each instance serves exactly one request, so `max-instances`
   directly bounds concurrent requests. In Gen2, each instance can serve
   up to `--concurrency` concurrent requests, so the effective request
   ceiling is `max-instances × concurrency` — a Gen2 function with
   `max-instances=50, concurrency=40` can have up to 2,000 concurrent
   requests hitting a downstream database that may only tolerate a
   fraction of that:
   ```bash
   gcloud functions describe checkout-api --gen2 --region=us-central1 \
     --format="value(serviceConfig.maxInstanceCount,serviceConfig.maxInstanceRequestConcurrency)"
   ```
   Size `max-instances` against the actual capacity of whatever the
   function calls (a database connection pool, a rate-limited
   third-party API), not against an arbitrary round number.

5. **Validate the runtime service account is scoped per function, not
   the shared default compute service account.** Both generations
   default to the project's default compute service account if none is
   specified — assign a dedicated, least-privilege service account per
   function instead:
   ```bash
   gcloud functions deploy order-validator \
     --gen2 \
     --service-account=order-validator-sa@<PROJECT_ID>.iam.gserviceaccount.com
   ```

6. **Confirm timeout and resource limits match the generation's
   ceiling.** Gen1 caps HTTP function timeout at 9 minutes (event-driven
   functions at 9 minutes as well) and has lower max memory/CPU ceilings
   than Gen2, which allows longer timeouts and larger CPU/memory
   allocations because it runs on Cloud Run. A function migrated from
   Gen1 assuming Gen1's ceilings may be needlessly under-provisioned on
   Gen2 — but don't over-provision reflexively either; size to measured
   need.

## Best practices

- Default new functions to Gen2 unless there's a specific, understood
  reason to use Gen1 (e.g. a very simple, latency-sensitive function
  where the Cloud Run layer's overhead measurably matters) — Gen2 has
  the more actively developed feature set.
- Treat `min-instances > 0` as a cost decision requiring sign-off, not a
  reflexive fix for cold-start complaints — measure actual cold-start
  impact on the SLO before paying to keep instances warm.
- Size `max-instances` against the weakest downstream dependency's
  actual capacity (DB connections, third-party rate limits), factoring
  in Gen2's `concurrency` multiplier, not against Cloud Functions' own
  account-level ceiling.
- Give every function its own service account scoped to only the APIs
  it calls, rather than sharing the default compute service account
  across functions with different privilege needs.
- Pin the runtime version explicitly (e.g. `nodejs20`, not an
  unspecified "latest") in CI/IaC so a Google-side default runtime bump
  doesn't silently change behavior.
- When migrating Gen1 → Gen2, test both the trigger event shape
  (Eventarc CloudEvent vs. Gen1 native payload) and the effective
  concurrency ceiling change before cutting production traffic over.

## Common pitfalls

- **Symptom:** A Gen2 function's downstream database starts refusing
  connections under moderate traffic even though `max-instances` looks
  conservative.
  **Fix:** The effective concurrent-request ceiling is
  `max-instances × concurrency`, not `max-instances` alone; lower
  `--concurrency` (down to `1` reproduces Gen1's one-request-per-instance
  model) or size the downstream connection pool/pooler (e.g. a proxy in
  front of the database) to the true worst-case concurrency.

- **Symptom:** A Cloud Storage-triggered function migrated from Gen1 to
  Gen2 stops firing, or fires with a payload the code can't parse.
  **Fix:** Gen2 event triggers route through Eventarc and deliver a
  CloudEvent envelope, not Gen1's native event/context payload; update
  the trigger to `--trigger-event-filters` with the Eventarc event type,
  grant the trigger's service account `roles/eventarc.eventReceiver` and
  invoke permission on the underlying Cloud Run service, and update the
  function code to the CloudEvent function signature.

- **Symptom:** A latency-sensitive HTTP function shows an occasional
  multi-second spike in p99 latency despite steady traffic volume.
  **Fix:** `min-instances` is likely `0`, so instances scale down during
  low-traffic windows and cold-start on the next request; set
  `min-instances` to at least `1` (or higher, sized to expected
  concurrent baseline traffic) for latency-sensitive paths, accepting
  the added standing cost.

- **Symptom:** A function's service account shows broad project-level
  roles when reviewed, inherited from the project's default compute
  service account.
  **Fix:** Deploy did not specify `--service-account`; create and assign
  a dedicated per-function service account scoped only to the specific
  APIs/resources that function calls, then redeploy and rotate out the
  default-service-account binding.

- **Symptom:** A team assumes Gen1 timeout/memory ceilings still apply
  after migrating to Gen2 and under-provisions a long-running batch-style
  function, causing it to time out.
  **Fix:** Gen2 (Cloud Run-backed) supports longer timeouts and larger
  memory/CPU allocations than Gen1; check current ceilings with
  `gcloud functions describe --gen2` against the deployed
  `serviceConfig.timeoutSeconds`/`availableMemoryMb` and raise them
  explicitly rather than assuming Gen1's lower ceiling still applies.

## Worked example

**Scenario:** An order-validation HTTP function currently on Gen1
suffers cold starts during a morning traffic ramp, and a separate
Cloud Storage-triggered thumbnail function needs to move to Gen2 as
part of a platform-wide migration.

Gen2 deploy for the latency-sensitive HTTP function, with a warm pool
sized to the observed baseline concurrent request count:
```bash
gcloud functions deploy order-validator \
  --gen2 \
  --runtime=nodejs20 \
  --region=us-central1 \
  --source=. \
  --entry-point=validateOrder \
  --trigger-http \
  --no-allow-unauthenticated \
  --service-account=order-validator-sa@<PROJECT_ID>.iam.gserviceaccount.com \
  --min-instances=2 \
  --max-instances=30 \
  --concurrency=20 \
  --cpu=1 \
  --memory=512Mi \
  --timeout=30s
```
With `min-instances=2`, at least two instances stay warm through
traffic lulls, eliminating cold starts on the morning ramp; `max-
instances=30 × concurrency=20` caps effective concurrent requests at
600, checked against the order-validation database's connection pooler
capacity before deploy.

Gen2 migration for the Cloud Storage-triggered function, moving off
Gen1's native bucket trigger to an Eventarc-routed one:
```bash
gcloud functions deploy image-processor \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --source=. \
  --entry-point=process_image \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=<GCS_BUCKET_NAME>" \
  --trigger-service-account=eventarc-trigger-sa@<PROJECT_ID>.iam.gserviceaccount.com \
  --max-instances=10 \
  --memory=1Gi
```
The function code is updated from Gen1's `def make_thumbnail(event,
context):` signature to the CloudEvent-based
`functions-framework` signature (`@functions_framework.cloud_event` /
`def process_image(cloud_event):`), and `eventarc-trigger-sa` is
granted `roles/eventarc.eventReceiver` plus invoke permission on the
resulting Cloud Run service before cutting the Gen1 trigger over.

## Cross-references

- [aws-lambda-packaging-and-configuration](../aws-lambda-packaging-and-configuration/SKILL.md) — equivalent packaging, scaling, and cold-start tradeoffs on AWS Lambda.
- [azure-functions-configuration](../azure-functions-configuration/SKILL.md) — equivalent hosting-plan and trigger/binding configuration on Azure Functions.
- [knative-serverless-configuration](../knative-serverless-configuration/SKILL.md) — the scale-to-zero/revision model Gen2 Cloud Functions builds on, generalized to any container on Kubernetes via Knative Serving.
