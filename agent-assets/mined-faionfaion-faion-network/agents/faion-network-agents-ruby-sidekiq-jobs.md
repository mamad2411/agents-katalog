# Sidekiq Background Jobs

## Summary

**One-sentence:** Sidekiq job patterns for Rails apps: explicit sidekiq_options, idempotency-first perform, primitive-ID arguments, custom retry backoff, and RSpec testing.

**One-paragraph:** Sidekiq job patterns for Rails apps: explicit sidekiq_options, idempotency-first perform, primitive-ID arguments, custom retry backoff, and RSpec testing. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-ruby-sidekiq-jobs.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Rails 6+ app з Redis на стеку, де потрібен async-throughput >100 jobs/min.
- Mailers / webhooks / third-party API calls, які не можна тримати в request-response cycle.
- Idempotency-critical pipelines (payments, notifications): дублікати delivery лиш через at-least-once Redis.
- Custom retry backoff (linear / exponential per error class) — не дефолтний 25-retry expo.

## Applies If (ALL must hold)

- Rails app з Redis уже в стеку та async job throughput ≥100 jobs/min
- Idempotent perform body можна гарантувати (DB unique constraint, version flag, або memoized check)
- Job arguments serializable до primitive IDs (Integer / String / UUID), не AR-objects
- RSpec test infra налаштована з Sidekiq::Testing.fake! та drain support

## Skip If (ANY kills it)

- Strict FIFO per partition — Sidekiq best-effort ordering; обери Kafka/SQS-FIFO
- Jobs мають persistance beyond Redis durability — обери GoodJob (Postgres-backed) або Solid Queue
- Serverless без persistent compute — обери queue-as-a-service (SQS + ECS task)
- Low-volume one-shot mailers — Rails 8 Solid Queue / ActiveJob async adapter достатньо

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-ruby-sidekiq-jobs` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/job.rb` | Canonical Sidekiq job example (idempotent perform, retry backoff) |
| `templates/sidekiq.service` | systemd unit template for running Sidekiq in production |
| `templates/sidekiq.yml` | Sidekiq config skeleton (queues, concurrency) |
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.rb` | Language skeleton implementing the canonical rule set |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-sidekiq-jobs.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[ruby-rails-patterns]]
- [[ruby-rspec-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/job.rb`

```ruby
# app/jobs/process_order_job.rb
# Required: include Sidekiq::Job, sidekiq_options, idempotency, primitive args, retry backoff.

class ProcessOrderJob
  include Sidekiq::Job

  sidekiq_options queue: :default, retry: 3, dead: true

  sidekiq_retry_in do |count, exception|
    case exception
    when PaymentGatewayError
      (count + 1) * 60 # Linear backoff for payment issues
    else
      (count**4) + 15  # Exponential backoff (15s, 31s, 96s)
    end
  end

  def perform(order_id)
    order = Order.find(order_id)
    return if order.processed? # idempotency check

    OrderProcessor.new(order).process!
    NotifyCustomerJob.perform_async(order_id)
  rescue ActiveRecord::RecordNotFound
    # Order was deleted — nothing to do; do NOT re-raise (no retry needed).
    Sidekiq.logger.warn "Order #{order_id} not found — skipping"
  rescue PaymentGatewayError => e
    raise # retry with custom backoff
  rescue StandardError => e
    ErrorTracker.capture(e, order_id: order_id)
    raise # always re-raise so Sidekiq schedules the retry
  end
end
```

### `templates/sidekiq.service`

```ini
# /etc/systemd/system/sidekiq.service
# Systemd unit for daemonized Sidekiq with graceful shutdown (SIGTERM).
# Reload: systemctl daemon-reload && systemctl restart sidekiq

[Unit]
Description=Sidekiq Background Worker
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/www/app/current
ExecStart=/usr/local/bin/bundle exec sidekiq -e production -C config/sidekiq.yml
Restart=always
KillSignal=SIGTERM
# Allow 30s for in-flight jobs to finish before force-kill.
TimeoutStopSec=30
User=deploy
Environment=RAILS_ENV=production

[Install]
WantedBy=multi-user.target
```

### `templates/sidekiq.yml`

```yaml
# config/sidekiq.yml
# Queue weights control priority: higher weight = more polling slots.
# All queues here must be registered or jobs sit silently in Redis.

:concurrency: 10
:max_retries: 5
:queues:
  - [critical, 4]
  - [default, 2]
  - [notifications, 2]
  - [exports, 1]

production:
  :concurrency: 25
```

### `templates/skeleton.json`

```json
{
  "artefact_id": "ruby-sidekiq-jobs-2026Q2-001",
  "owner": "ruslan@faion.net",
  "language": "ruby",
  "module": "app/jobs/example.rb",
  "evidence_quote": "Sidekiq delivers at-least-once; idempotency check at top of perform is mandatory.",
  "rationale": "Closes the gap surfaced by the parent skill \u2014 input artefact 'task-brief.md' explicitly names the constraint set; output ties decisions to rule r1.",
  "inputs_used": [
    "task-brief.md",
    "constitution.md"
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-23"
}
```

### `templates/skeleton.rb`

```ruby
# ProcessOrderJob — required: include Sidekiq::Job, sidekiq_options, idempotency, primitive args, retry backoff.

class ProcessOrderJob
  include Sidekiq::Job

  sidekiq_options queue: :default, retry: 3, dead: true

  sidekiq_retry_in do |count, exception|
    case exception
    when PaymentGatewayError
      (count + 1) * 60         # linear backoff for transient payment issues
    else
      (count**4) + 15          # exponential backoff (15s, 31s, 96s)
    end
  end

  def perform(order_id)
    order = Order.find(order_id)
    return if order.processed?  # idempotency check at top of perform

    OrderProcessor.new(order).process!
    NotifyCustomerJob.perform_async(order_id)
  rescue ActiveRecord::RecordNotFound
    Sidekiq.logger.warn "Order \#{order_id} not found — skipping (no retry)"
  rescue PaymentGatewayError => e
    raise                       # retry with custom backoff
  rescue StandardError => e
    ErrorTracker.capture(e, order_id: order_id)
    raise                       # always re-raise so Sidekiq schedules the retry
  end
end
```
