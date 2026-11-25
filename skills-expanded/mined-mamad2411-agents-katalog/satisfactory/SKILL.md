---
name: satisfactory
description: What satisfactory is and how it behaves — constraint solving as a service built on Timefold Solver and deployed as ankka services; models and datasets, the ten dataset statuses and which are final, lineage instead of mutation (from-input, from-patch, supersede), the three ways to receive a result, tenants and API keys, workers and leases, and every reference page. Use for any question about satisfactory that is not specifically writing client code, an ankka integration, or a model; load it first when unsure which skill applies.
---

# satisfactory

satisfactory is constraint solving as a service: a request names a model (a planning problem type,
compiled Java) and carries a dataset (the instance plus how long to solve and how to weigh constraints).
The API is a reimplementation of the Timefold Platform's model API. It runs as two ankka services:
`api`, which is exposed and holds every dataset as an event sourced entity, and `solver`, a pool of
workers that pull datasets and solve them with Timefold Solver Community.

## Rules

1. **Datasets are immutable, with lineage.** Never look for a way to edit a dataset in place. A changed
   problem is `POST /{id}/from-input` or `POST /{id}/from-patch`, a new dataset with `parentId`.
   Deriving from a dataset that is still solving supersedes it: the parent completes with its best
   solution and names the child in `supersededBy`.
2. **A submit answers 202 at once; the solution arrives later.** Results arrive by webhook (production),
   server-sent events (development) or polling `/metadata`. None of the three carries a solution; the
   solution is `GET /{id}`, which returns the best so far at any time.
3. **Ten statuses, five final.** `SOLVING_COMPLETED`, `SOLVING_INCOMPLETE`, `SOLVING_FAILED`,
   `DATASET_INVALID`, and `DATASET_COMPUTED` when `operation=NONE`. A terminate (`DELETE /{id}`) is a
   success that keeps the best solution. Validation happens on a worker, so `SOLVING_SCHEDULED` comes
   before `DATASET_VALIDATED`.
4. **Two APIs, two credentials.** The model API takes `X-API-KEY`; the platform API takes a bearer token
   from the identity provider and is `503` until one is configured. A dataset of another tenant is a
   `404`. Keys and tokens do not cross.
5. **A request may set termination and weights, nothing else.** `config.run.termination` and
   `config.model.overrides` (`<key>Weight`, integer, 0 disables). `maxThreadCount` is capped at 1.
   A configuration profile names a bundle of these; `standard` is the model's defaults.
6. **Every event stream frame and webhook event carries `seq`.** `?after=<seq>` resumes a stream
   exactly; a webhook receiver dedupes on the event id. Delivery is at-least-once.
7. **The lease epoch is a fencing token.** A worker command from a superseded epoch is refused with
   `409`. Only a strictly better score is recorded. No event carries a solution body.
8. **Score analysis is by ablation.** `{ score, constraints: [{ name, weight, score }] }`; no match
   counts or justifications, because those are Enterprise-only in Timefold Solver.

## Before answering

- Which API is the question about: the model API (`/api/models/{model}/{version}`) or the platform
  API (`/api/platform/v1`)? The credential and the reference page differ.
- Which model? `employee-scheduling` submits `schedules`; `vehicle-routing` submits `route-plans`.
  Each has its own constraints, weight fields, KPIs and issue codes on its reference page.
- Is the question about running it (`get-started/run-locally.md`, `deploy/`) or calling it
  (`reference/model-api.md`)?
- Does a limitation apply? Check `reference/limitations.md` before promising a feature.

## Mistakes to check for

- Describing a mutable job, a continuous mode, or an in-place problem change. None exist.
- Expecting the solution in a webhook or a stream frame.
- Using `X-API-KEY` on the platform API, or a bearer token on the model API.
- Assuming multi-threaded solving, justifications, or an uploadable model jar.
- Forgetting `SAT_PUBLIC_URL` and `SAT_METRICS_TOKEN` in a deployment.

## Reference files

Open the one a task needs; each is one topic and stands alone.

### Start here

- `references/index.md` — What satisfactory is, how a planning problem becomes a solution, the ways to receive results, and where in this documentation to start.

### Get started

- `references/get-started/run-locally.md` — Start the whole of satisfactory in one JVM with the worker in-process and a development API key, from a clone of the repository and a Postgres in Docker.
- `references/get-started/first-solve.md` — Submit the employee scheduling demo dataset with curl, watch its score improve over server-sent events, fetch the solution and its KPIs, and read the per-constraint score.
- `references/get-started/coding-agents.md` — Give a coding agent this documentation as skills from the ankka marketplace, and know what the skills carry.

### Concepts

- `references/concepts/architecture.md` — The two services, why workers pull rather than being called, what the dataset entity guarantees, and where each piece of the system lives in the repository.
- `references/concepts/models-and-datasets.md` — Why a request names a model and carries a dataset, what a model is made of, what a dataset is, and what a request may and may not influence.
- `references/concepts/lineage.md` — Why a changed problem is a new dataset derived from the old one, the three ways to derive one, and what happens when the parent is still solving.
- `references/concepts/receiving-results.md` — The three ways a result reaches you — webhooks for production, server-sent events for development, polling as the fallback — and what each carries.
- `references/concepts/workers-and-leases.md` — How a worker claims a dataset, why every report carries a lease epoch, what happens when a worker dies mid-solve, and how a rolling deploy drains without losing a solution.
- `references/concepts/tenancy.md` — How the platform API and the model API authenticate differently, what a tenant owns, how limits queue and refuse work, and where configuration profiles fit.

### Deploy and operate

- `references/deploy/deploy-on-ankka.md` — Build the two images, create the secrets the descriptors reference, deploy the api and solver services to an ankka project, expose the API, and create the first tenant and key.
- `references/deploy/operate.md` — What an operator can see and do — every tenant's datasets, the workers and their slots, draining a worker, pausing a tenant's queue, force-terminating a dataset, the audit trail, and the Prometheus metrics.

### Reference

- `references/reference/model-api.md` — Every route of a model's API — datasets, demo data, the catalog, lineage, analysis and the event stream — with its query parameters, bodies, statuses and error codes.
- `references/reference/platform-api.md` — Every route of the platform API — tenants, members, keys, limits, configuration profiles, webhook subscriptions and the delivery log — and the operator routes, with who may call each.
- `references/reference/dataset-lifecycle.md` — The ten statuses a dataset moves through, in which order, which are final, and what a terminate, a failure, a lost lease and a supersession do to them.
- `references/reference/webhook-events.md` — The event types a subscription can receive, the envelope and the data of each, the headers on every delivery, and how the signature is computed.
- `references/reference/configuration.md` — Every setting of the api and solver services, the environment variable that overrides each, its default, and what it does.
- `references/reference/employee-scheduling.md` — The employee-scheduling model, version v1 — its input and output, constraints and weight fields, KPIs, validation issues, patch paths and demo datasets.
- `references/reference/vehicle-routing.md` — The vehicle-routing model, version v1 — its input and output, constraints and weight fields, KPIs, validation issues, patch paths and demo datasets.
- `references/reference/divergences.md` — Where satisfactory's API deliberately differs from the Timefold Platform model API it reimplements, and why, so a client written against Timefold's platform knows what to expect.
- `references/reference/limitations.md` — What satisfactory does not do yet, stated plainly, so a reader who hits one of them knows it is the system and not their code.
- `references/reference/glossary.md` — The words this documentation uses in a specific sense, each defined once.
