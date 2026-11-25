---
name: loki-configuration-validation
description: >
  Validates Loki configuration before deploying — checking
  `limits_config` values, `schema_config`/storage settings, and label
  cardinality assumptions with dry-run tooling (`loki -config.file
  -verify-config`, `promtool`-style structural checks, and a
  cardinality audit against a running instance) so a bad config doesn't
  reject or silently drop production log ingestion. Use when the user
  asks to "validate my Loki config before deploying," "will this Loki
  limits_config reject my logs," "check this Loki schema_config for
  mistakes," "test a Loki config change in CI," or "why is Loki
  rejecting ingestion after this config change."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Loki Configuration Validation

## Purpose

A Loki config that is syntactically valid YAML can still be functionally
wrong in ways that only show up after logs start being rejected in
production — a `schema_config` entry edited in place instead of appended,
a `limits_config` value copied from a much smaller deployment, or a
retention setting that silently does nothing because the compactor isn't
enabled. This skill covers validating a Loki config **before** it's
deployed: structural/schema checks via Loki's own `-verify-config` flag,
a pre-deploy review checklist for the specific fields most likely to
cause silent ingestion rejection, and a lightweight cardinality audit
against a candidate label design. It assumes the config's actual content
decisions (deployment mode, schema/storage choice, retention design) are
made per
[loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md)
— this skill is specifically about catching mistakes in that config
before rollout, not about designing it from scratch.

## When to use

- Before merging or deploying any change to a Loki `config.yaml`
  (`limits_config`, `schema_config`, `storage_config`, `compactor`,
  `ingester` blocks).
- Setting up a CI check that validates Loki config changes on every PR
  rather than discovering a mistake after it's live.
- Diagnosing why ingestion started rejecting logs (`429`, `entry too far
  behind`, discarded samples) immediately after a config change, to
  confirm which specific field is responsible.
- Reviewing a candidate label/limits design for cardinality risk before
  it ships to a shared/production Loki instance.
- Auditing an existing production config for common misconfigurations
  (retention set but compactor disabled, schema edited in place instead
  of appended) as a health check, not just after an incident.

## Prerequisites & environment

- The `loki` binary (or `docker run grafana/loki:<version> -verify-config
  -config.file=...`) available locally or in CI to run structural
  validation without needing a full running cluster.
- The candidate config file(s) — base config plus any per-environment
  overlay/values file if deployed via Helm (`helm template` first to
  render the final config before validating it, since the raw
  `values.yaml` alone isn't the actual Loki config).
- Read access to a running Loki instance's `/metrics` endpoint (or its
  Prometheus-scraped metrics) for the cardinality-audit and post-deploy
  confirmation steps — validation of intent is not a substitute for
  confirming actual behavior against real data.
- Familiarity with the config fields being validated — see
  [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md)
  for what each of `limits_config`, `schema_config`, `compactor`, and
  `ingester` actually controls if unfamiliar; this skill assumes that
  context rather than re-explaining it.

## Step-by-step guidance

1. **Run structural validation with Loki's own `-verify-config` flag**
   before anything else — this catches YAML/schema-level mistakes
   (wrong field name, wrong type, an invalid enum value) without needing
   a live cluster:
   ```bash
   loki -config.file=loki-config.yaml -verify-config
   # or, without a local binary:
   docker run --rm -v "$(pwd)/loki-config.yaml:/etc/loki/config.yaml" \
     grafana/loki:3.1.0 -config.file=/etc/loki/config.yaml -verify-config
   ```
   For Helm-deployed Loki, render the final config first — validating
   the raw `values.yaml` skips whatever templating logic produces the
   actual config Loki receives:
   ```bash
   helm template loki grafana/loki -f values-production.yaml \
     --show-only templates/config.yaml > rendered-config.yaml
   loki -config.file=rendered-config.yaml -verify-config
   ```

2. **Check `schema_config` was appended, not edited in place.** Diff the
   proposed change against the previous config specifically for this —
   `-verify-config` will not catch it, since editing an existing entry's
   `from`/`store`/`schema` fields is still structurally valid YAML, it
   just silently breaks the ability to read historical data:
   ```bash
   git diff HEAD~1 -- loki-config.yaml | grep -A5 'schema_config'
   ```
   > **Fix if wrong:** any change to `store`, `object_store`, or `schema`
   > version must be a **new** entry in `schema_config.configs` with a
   > future `from:` date, never a modification of an existing entry —
   > flag this in review every time a `schema_config` diff touches an
   > existing block instead of adding a new one.

3. **Review `limits_config` values against the deployment's actual
   expected scale**, not defaults copied from a different environment's
   config — this is the check `-verify-config` can't do because an
   overly generous *or* overly strict limit is still valid config:
   - `ingestion_rate_mb`/`ingestion_burst_size_mb` — compare against
     current/projected total log volume across all shippers pushing to
     this instance.
   - `per_stream_rate_limit`/`per_stream_rate_limit_burst` — compare
     against the highest-volume single stream expected (usually the
     noisiest app's `error`/`info` combined stream).
   - `max_streams_per_user` — compare against `(number of apps) ×
     (number of namespaces) × (number of enumerated label values)`
     for the actual label design, with headroom, not an arbitrary round
     number.
   - `retention_period` — confirm it matches the compliance/operational
     requirement that was actually agreed, and cross-check step 5 that
     the compactor will actually enforce it.

4. **Audit label cardinality for any new/changed label** before the
   config or the app instrumentation change ships, using a running
   instance's existing data as a proxy where available:
   ```bash
   curl -s -G 'http://<LOKI>/loki/api/v1/series' \
     --data-urlencode 'match[]={app="payments-api"}' \
     --data-urlencode 'start=2026-07-27T00:00:00Z' | jq '.data | length'
   ```
   A rapidly growing count for a label expected to be small/enumerated
   (e.g. `level`, `env`) versus one legitimately expected to be large
   tells you whether a proposed label is safe. Reject any new label
   candidate that is a raw identifier (request ID, user ID, IP address,
   trace ID) at the design stage — see
   [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md)
   for where such fields belong instead (unindexed log content, parsed
   at query time).

5. **Confirm retention will actually be enforced**, not just configured
   — check that the compactor is present in the deployment topology and
   `retention_enabled: true` is set together with `retention_period`,
   since one without the other is a common silent misconfiguration:
   ```bash
   grep -A3 'compactor:' loki-config.yaml
   ```
   If `compactor.retention_enabled` is absent or `false` while
   `limits_config.retention_period` is set, flag it — the retention
   period value alone is inert.

6. **Wire structural validation into CI** so a bad config fails the PR
   instead of failing at deploy time:
   ```yaml
   # GitHub Actions example
   - name: Validate Loki config
     run: |
       docker run --rm -v "${{ github.workspace }}/loki-config.yaml:/etc/loki/config.yaml" \
         grafana/loki:3.1.0 -config.file=/etc/loki/config.yaml -verify-config
   ```
   Pair with a simple script/lint step asserting `schema_config.configs`
   only ever grows (new entries appended, existing entries' `from`/
   `store`/`schema` fields unchanged) so step 2's check is enforced
   automatically rather than relying on a reviewer catching it by eye.

7. **After deploying, confirm the config behaves as validated** — static
   validation reduces risk but doesn't replace watching real ingestion
   behavior for the first period after a change:
   ```bash
   curl -s http://<LOKI>/metrics | grep loki_discarded_samples_total
   ```
   A non-zero and growing count immediately after a `limits_config`
   change, broken down by `reason`, tells you exactly which limit is
   too strict for real traffic — treat this as the final confirmation
   step, not the first line of defense.

## Best practices

- Run `-verify-config` (or the Docker equivalent) in CI on every PR
  touching Loki config — treat a failing structural check the same as a
  failing unit test, not a manual pre-deploy step someone might skip.
- Never validate a Helm `values.yaml` directly — always render the
  actual templated config first, since that's what Loki receives.
- Diff `schema_config` specifically on every review, looking for an
  edited existing entry rather than a new appended one — this is the
  single most common config mistake that structural validation cannot
  catch on its own.
- Size `limits_config` values against real, current numbers for the
  specific deployment (actual log volume, actual stream count) rather
  than copying values from a reference architecture doc or a different
  environment's config.
- Treat any new label as guilty until proven low-cardinality — run the
  `/loki/api/v1/series` cardinality check (or equivalent) before a label
  design ships broadly, not after ingestion starts struggling.
- Confirm compactor + retention settings are reviewed together, every
  time either changes — they're two fields that must agree to actually
  do anything.
- Watch `loki_discarded_samples_total` immediately after any
  `limits_config` deploy as the real-world confirmation that validation
  didn't miss something — static checks reduce but don't eliminate this
  risk.

## Common pitfalls

- **Symptom:** `-verify-config` passes cleanly, but ingestion starts
  rejecting logs within minutes of deploying the "validated" config.
  **Fix:** `-verify-config` only checks structural/type validity, not
  whether the *values* make sense for actual traffic. Cross-check
  `limits_config` values (step 3) against real current volume/stream
  counts specifically — a structurally valid but too-strict
  `per_stream_rate_limit` is the most common cause.

- **Symptom:** A schema/storage-backend change was reviewed and merged,
  and shortly after, queries against historical (pre-change) log data
  start returning nothing.
  **Fix:** The `schema_config` entry was edited in place instead of a
  new dated entry being appended (step 2) — this is exactly the mistake
  structural validation misses since both forms are valid YAML. Revert
  to the original entry, add the change as a new entry with a future
  `from:` date instead.

- **Symptom:** A retention change (e.g. shortening from 90 to 30 days)
  was deployed, reviewed as "looks right" in the diff, but storage usage
  keeps growing at the same rate as before.
  **Fix:** `retention_period` was changed but the compactor's
  `retention_enabled` was never set to `true` (or the compactor isn't
  deployed at all in this topology) — step 5's check catches exactly
  this; confirm both together, not just the number that looks intuitive
  in a diff.

- **Symptom:** A new label added to improve log searchability (e.g.
  promoting a `customer_tier` field to a label) is approved in code
  review because it "sounds bounded," but stream count spikes
  dramatically after rollout.
  **Fix:** The label's actual cardinality wasn't checked against real
  data before shipping — "sounds bounded" is not validation. Run the
  `/loki/api/v1/series` cardinality check against a staging/canary
  instance with the new label before it reaches production broadly, per
  step 4.

- **Symptom:** A Loki config change passes CI's `-verify-config` step
  but the actual production rollout uses a different, un-rendered
  `values.yaml` that was never checked.
  **Fix:** The CI validation step was validating a hand-written raw
  config file, not the Helm-templated output actually deployed. Render
  via `helm template --show-only templates/config.yaml` (or the
  equivalent for the deployment tool in use) and validate that rendered
  output, matching exactly what ships.

## Worked example

**Scenario:** A PR proposes raising `max_streams_per_user` from 5,000 to
50,000 "to stop seeing rejected logs from the new `checkout-events`
service," and separately bumps the schema store from `boltdb-shipper` to
`tsdb`.

1. Run structural validation first:
   ```bash
   loki -config.file=loki-config.yaml -verify-config
   ```
   Passes — both changes are structurally valid.

2. Diff `schema_config` specifically:
   ```diff
   schema_config:
     configs:
       - from: 2024-01-01
   -     store: boltdb-shipper
   +     store: tsdb
         object_store: s3
   -     schema: v11
   +     schema: v13
   ```
   This is an **edited existing entry**, not an appended one — flagged
   as a blocking review comment per step 2. The fix requested: add a new
   `configs` entry with `from: 2026-08-01` (a near-future date) carrying
   the new `store`/`schema` values, leaving the original `2024-01-01`
   entry untouched so historical data stays readable.

3. Check the `max_streams_per_user` bump against real numbers instead of
   accepting the round number: query `/loki/api/v1/series` for
   `checkout-events` and find it's actually emitting a `session_id` label
   per user session — an unbounded label, not a volume problem at all.
   Raising `max_streams_per_user` to 50,000 would have masked a real
   cardinality bug rather than fixed a capacity shortfall.

4. Correct recommendation delivered in review: don't raise the limit;
   remove `session_id` as a label (move it into log content, filtered at
   query time via LogQL per
   [logql-query-authoring](../logql-query-authoring/SKILL.md)) and keep
   `max_streams_per_user` at a value sized to the actual bounded label
   design, per
   [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md).

5. Re-submit with the schema change as a new appended entry and the
   labeling bug fixed at the source; `-verify-config` and the CI
   cardinality check both pass, and the PR merges without the earlier
   config accidentally masking a real ingestion bug.

## Cross-references

- [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md) — designing the schema, limits, and label strategy this skill validates before deployment.
- [logql-query-authoring](../logql-query-authoring/SKILL.md) — where a label that should have stayed unindexed content gets parsed/filtered at query time instead.
- [fluent-bit-configuration-validation](../fluent-bit-configuration-validation/SKILL.md) — the equivalent pre-deploy validation discipline applied to the shipper side of the pipeline feeding this Loki instance.
