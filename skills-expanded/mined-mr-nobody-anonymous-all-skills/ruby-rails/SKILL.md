---
name: ruby-rails
description: "Build and maintain Ruby and Rails applications: idiomatic Ruby, ActiveRecord query hygiene, migrations with zero downtime, jobs, and RSpec coverage."
type: procedural
category: programming
domain: programming
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - rails migration zero downtime
  - activerecord n+1 query
  - rspec test setup
  - sidekiq job design
  - ruby gem conflict
keywords:
  - ruby
  - rails
  - activerecord
  - rspec
  - bundler
  - sidekiq
source: custom
enabled: true
---

# Ruby and Rails

## Purpose

Build and maintain Ruby and Rails applications: idiomatic Ruby, ActiveRecord query hygiene, migrations with zero downtime, jobs, and RSpec coverage.

## When to Use

- You are adding a Rails feature and need model, controller, job and test changes to fit together.
- Database migrations must run against a live application without downtime.
- An ActiveRecord query is slow or issues N+1 statements.

## When NOT to Use

- The codebase is plain Ruby with no Rails, where controller and ActiveRecord guidance does not apply.
- The work is front-end or asset-pipeline-only with no Ruby logic.
- You need a Ruby version upgrade plan spanning majors; treat that as its own migration project.

## Capabilities

- Write ActiveRecord queries that avoid N+1 and unbounded result sets.
- Design expand/contract migrations safe for rolling deploys.
- Model background jobs with idempotency and retry semantics.
- Cover behaviour with RSpec request and model specs instead of controller internals.

## Inputs

- Rails and Ruby versions plus the database adapter in use.
- The failing query, endpoint or spec, and its expected behaviour.
- Deployment model: rolling restarts, migrations run before or after boot.

## Workflow

1. Inspect models, schema.rb and existing specs for the area you are changing.
2. Write a failing request/model spec that expresses the desired behaviour.
3. Implement the smallest change; use `includes`/`preload` to fix N+1 and add indexes for new lookups.
4. Split migrations into expand (add), backfill (batched), contract (remove) steps.
5. Run `bundle exec rspec` and the linter; verify the migration against a copy of production-shaped data.

## Tools

- bundler
- rails console / dbconsole
- rspec
- rubocop

## Examples

- `bundle exec rspec spec/requests/orders_spec.rb`
- `bundle exec rails db:migrate:status`
- `EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;`

## Safety

- Migrations that drop or rename columns break running instances during rolling deploys.
- Callbacks that send email or hit APIs make saves non-idempotent; move side effects into jobs.
- `update_all` and `delete_all` skip validations and callbacks — confirm that is intended.

## Source

All-Skills canonical library (`skills/programming/ruby-rails`). First-party skill, maintained in this repository.

## Notes

- `strong_migrations` catches most unsafe DDL at review time.
- Long backfills belong in a batching job, not in a migration.
- Pairs with: `databases/schema-evolution`, `development/testing`.
