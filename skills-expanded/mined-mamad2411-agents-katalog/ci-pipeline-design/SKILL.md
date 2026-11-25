---
name: ci-pipeline-design
description: "Design a CI/CD pipeline that does not exist yet, or restructure one that grew badly: decide which checks are allowed to block a merge before drawing any stage, lay the stages out as a dependency graph so nothing waits on output it never uses, key caches on what actually invalidates them, choose a matrix or separate jobs, build the artefact once and promote the same digest through every environment, decide which job may ever see a secret, and hold wall-clock to a number people will wait for. Use whenever someone says \"our CI takes 40 minutes\", \"what should be a required check\", \"how do I cache node_modules properly\", or \"set up a pipeline for this repo\". Not for red CI (ci-triage), writing a workflow file or script (code-scaffold), how a change reaches users (release-strategy), or auditing an existing workflow for attacker reach (pipeline-hardening)."
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(gh:*), Bash(jq:*), Bash(git:*), Bash(actionlint:*)"
---

# CI Pipeline Design

A pipeline is designed well when every check that can block a merge is one the team trusts enough to act on, the slowest path through it is short enough that people wait for the result instead of routing around it, and the artefact that reaches production is the identical bytes the tests ran against.

Pipelines are rarely designed. They accrete, and every addition is locally reasonable: one more job, one more required check, one more rebuild per environment. The aggregate then has properties nobody chose. Three stages run in sequence that had no dependency between them, so the critical path is the sum of everything rather than the longest thing. A required check fails once every several runs for reasons unrelated to the change, so the team makes it advisory, and six months later nothing gates anything. A cache is keyed on a branch name and never hits, or keyed on nothing and serves a stale toolchain. The container image is built for staging and built again for production, so the thing that was tested is not the thing that shipped. Each of those is invisible in the workflow file you are editing and obvious in the run history, which is why this procedure starts by reading the history rather than by writing YAML.

## Scope

Use for: designing a pipeline for a repository that has none; restructuring one that has grown badly; deciding which checks are required for merge and which are advisory; laying out the stage graph and what gates what; cache keys and what actually invalidates them; matrix strategy versus separate jobs; promoting one artefact across environments instead of rebuilding; where secrets enter and which job can see them; getting total wall-clock down to a number people will wait for.

Do not use for: a pipeline that is red right now and you want to know why, including "the build broke", "my PR is blocked" and "is this a flake" — that is `ci-triage`; writing a single workflow file, job or helper script from a description — that is `code-scaffold`; how a built change reaches users, canaries, rings, flags and blue/green — that is `release-strategy`; moving wholesale from one CI system to another as a project with a parallel run and a retirement plan — that is `plan-platform-migration`; deciding what the tests should cover — that is `test-design`; auditing a workflow that already exists for what an attacker, rather than a slow build, can reach through it — that is `pipeline-hardening`.

## Workflow

### 1. Decide what the pipeline is allowed to block, before designing a single stage

This is the gate on everything below, and it comes first because the failure it prevents is irreversible in practice. A required check that fails for reasons the author did not cause gets made advisory within a few weeks — that is the humane decision each time it is taken — and once a team has learned that a red check can be waved through, the checks that were worth blocking on lose their force too. The blocking set is a trust budget. Spend it before you spend runner minutes.

Classify every check you have or intend to add into exactly one of three:

| Class | What happens on failure | What a check must have to qualify |
| --- | --- | --- |
| **Blocking** | The merge does not happen | Deterministic on a given commit: same commit, same answer. A named owner. A defined first action the author takes in the next five minutes that is not "re-run it" |
| **Advisory** | Reported on the pull request, merge proceeds | Genuine signal whose failure is regularly not the author's fault or not urgent — a performance benchmark, a scanner with a triage backlog, a flaky end-to-end suite that has not yet earned its place |
| **Informational** | Recorded, surfaced in a summary or dashboard, nothing reported on the pull request | Measurements: coverage delta, image size, job durations, cost per run |

The test that does the work is the third column of the first row. If the honest answer to "what does the author do when this goes red" is "look at whether it is the flaky one, then press re-run", the check is advisory, whatever anyone wants it to be.

Do not assume the determinism, measure it. On the default branch every failure is either a genuine break of that branch or a false failure, so the run history of `main` is the cheapest estimate of a check's false-failure rate that exists:

```bash
set -Eeuo pipefail

# Per-job outcomes over the last 100 runs of the workflow on the default branch.
# Anything with failures here is either breaking main regularly or is not deterministic.
gh run list --workflow ci.yml --branch main --limit 100 --json databaseId \
  --jq '.[].databaseId' \
  | while read -r run_id; do
      gh run view "$run_id" --json jobs \
        --jq '.jobs[] | [.name, .conclusion] | @tsv'
    done \
  | sort | uniq -c | sort -rn
```

Read the result per job, not in aggregate. One job at a few per cent failure on a branch that is supposed to be green is the whole problem, and it disappears into an overall pass rate.

Where the bar sits is a decision for the team that lives with the pipeline, and it depends on how many pull requests a day pass through the check: the same per-run rate is a nuisance at five merges a day and a standing outage at two hundred. What is not a judgement call is making a check required without knowing its number.

Record the outcome as an explicit list before designing stages, because it determines the shape: blocking checks belong on the critical path and have to be fast, advisory checks can run long and in parallel with everything, informational checks can run after the merge entirely.

### 2. Take the wall-clock numbers you have now

Wall-clock is a design constraint rather than an optimisation to do later, because a pipeline people do not wait for is one they work around — by batching several changes into one pull request, by merging on a green-looking subset, or by pushing the fix and going to lunch, which is how a broken main gets an hour of nobody watching it.

Extreme Programming Explained names a ten-minute build as a practice (Beck, 2nd edition), and it remains the most widely quoted target. Treat it as a target somebody chose, not as a measurement of your repository: take your own numbers first.

```bash
set -Eeuo pipefail

# Distribution of end-to-end pipeline duration in seconds, last 100 runs on main.
gh run list --workflow ci.yml --branch main --limit 100 \
  --json startedAt,updatedAt \
  --jq '.[] | ((.updatedAt | fromdate) - (.startedAt | fromdate))' \
  | sort -n \
  | awk '{ v[NR] = $1 } END { printf "n=%d p50=%ds p95=%ds max=%ds\n", NR, v[int(NR*0.5)], v[int(NR*0.95)], v[NR] }'
```

Three numbers matter and they are different questions:

- **The critical path**, meaning the longest chain of jobs that must run in sequence. This is the floor. Adding parallelism elsewhere cannot go below it.
- **p95, not the mean.** People remember the bad runs, and queue time for runners lives in the tail.
- **Queue time separately from execution time.** A pipeline whose jobs each take two minutes and which takes twenty is a capacity problem, and no amount of caching touches it. `gh run view <run-id> --json jobs` carries `startedAt` per job against the run's `createdAt`, which is where that gap shows.

Then decide the budget out loud: the number a developer waits for, and what falls off the critical path to get there. The usual answer is that the blocking set from step 1 is what runs on the critical path, and everything else moves beside it or after it.

### 3. Draw the stage graph as a dependency graph, not a line

Most slow pipelines are slow because a stage waits on something it does not need. Write the graph as edges, and require a reason for every edge: this job consumes an output of that job, or this job must not run if that one failed because running it costs money or has an effect.

Two shapes cover most repositories:

```text
                 ┌─ lint ──────────────┐
checkout+setup ──┼─ unit tests ────────┼─ build artefact ─ integration ─ publish
                 └─ type check ────────┘                       (uses artefact)
```

Lint, unit tests and type checks have no dependency on each other and produce nothing the build consumes, so they fan out. The build is the fan-in point because integration tests need the artefact. Publish depends on everything because it has an effect outside the pipeline.

The judgement calls, in the order they come up:

**Fail-fast ordering only pays when the jobs are serialised.** Putting the thirty-second linter before the eight-minute test suite saves eight minutes on a lint failure and costs thirty seconds on every other run. That trade is good when runners are scarce or billed, and pointless when the jobs would have run in parallel anyway on capacity you are already paying for. Decide from which constraint you have, and say which one in the design.

**Do not gate on something with no consumer.** A security scan that blocks the build without the build consuming its output is a sequential edge bought for nothing: run it in parallel and let it block the merge instead of the build.

**Split what the branch needs from what a merge needs.** Pull request runs need the blocking set and fast feedback. The default branch can additionally run the long end-to-end suite, the nightly matrix breadth, and the publishing steps. Two entry points into shared, reusable jobs beats one workflow full of conditionals, which is the construct that becomes unreadable first.

`references/stage-graph.md` has worked graphs for the four common repository shapes — library, service, container image and monorepo — plus how to decompose into reusable workflows without creating a dependency nobody can see. Read it when laying out stages for a specific repository rather than in the abstract.

### 4. Choose a matrix or separate jobs on purpose

A matrix is a loop over one dimension where every cell runs the same steps. It is the right tool when the axis is a genuine compatibility surface — interpreter versions you support, operating systems you ship on, database engines you claim to work with — and each cell's result is independently meaningful.

| Use a matrix when | Use separate jobs when |
| --- | --- |
| The steps are identical and only a variable changes | The steps differ, even slightly, and the matrix would need `if:` conditions per cell |
| Every cell's failure means the same thing | One cell is blocking and another is advisory |
| The cells need the same permissions and secrets | One cell needs credentials the others do not — a matrix shares its permissions across every cell |
| Cell durations are comparable | One cell takes many times longer, so it holds the whole stage's completion |

Three costs are easy to miss:

- **Runner minutes multiply, wall-clock does not shrink.** A matrix of eight is eight times the spend for the duration of the slowest cell, and the slowest cell is what the developer waits for. Cut breadth by moving rarely broken axes to a scheduled run and keeping the pull request matrix to what changes most.
- **`fail-fast` cancels siblings.** The default of cancelling the rest on the first failure saves minutes and destroys evidence: you cannot tell whether one cell or all eight are broken, which is the first thing you want to know about a compatibility failure. Turn it off for compatibility matrices; leave it on where the cells are redundant.
- **Cell names are check names.** Branch protection matches required checks by name, and matrix cell names embed the axis values. Change a version in the matrix and the required check silently no longer exists, so the rule is satisfied by nothing at all. Require an aggregate job that depends on the matrix and reports one stable name, and make that the required check.

### 5. Key caches on what invalidates them

A cache key is a claim that any two commits producing the same key can share the same bytes. Most cache problems are one of two failures of that claim: the key includes something that changes on every commit, so the cache never hits and the save cost is pure loss, or the key omits something that does change the contents, so the cache serves the wrong bytes and the failure appears as a build error nobody can reproduce locally.

| Cached thing | Key on | Not on |
| --- | --- | --- |
| Dependency downloads (`~/.npm`, `~/.cache/pip`, `~/go/pkg/mod`, `~/.m2`) | A hash of the lockfile, plus the runner OS and the language version | The branch name, the commit SHA, or a fixed literal |
| Installed tree (`node_modules`, `.venv`) | The lockfile hash plus OS plus interpreter version plus anything the install step reads, such as a post-install script | The lockfile alone when native modules compile against a system library |
| Compiler and build caches (Gradle, Bazel, `sccache`, Turborepo) | The tool's own content-addressed key where it has one, with the cache path scoped per tool | A hand-rolled key that approximates the tool's input set |
| Container layers | The registry plus a content digest, through the builder's own cache backend | Anything resembling `latest` |

Prefer caching the downloads over caching the installed tree. A restored `node_modules` that is subtly wrong produces failures that look like application bugs; a restored package cache at worst costs a re-download, and the ecosystem's install step still verifies the lockfile.

Two rules that are about correctness rather than speed:

- **A cache miss must be correct, and a cache hit must not be trusted with anything it did not build.** Prefix restore keys let a near-miss restore an older cache, which is worth having for download caches and dangerous for anything the build treats as an output.
- **Caches cross trust boundaries.** On most hosted CI a run triggered by a fork's pull request can write to a cache scope the default branch later reads, which turns a cache into an execution path for untrusted code. Scope caches so untrusted runs restore but do not save, and never cache credentials or a login-populated config file.

Then measure, because a cache that does not hit is a cost with no benefit. `references/caching.md` has per-ecosystem key recipes, the restore-key prefix rules, how to read hit rates out of run logs, and the cache-scope boundaries per provider. Read it when writing actual cache keys or when a cache is suspected of serving stale content.

### 6. Build the artefact once, and promote the same bytes

Rebuilding per environment is the most common structural defect in an otherwise healthy pipeline, and it defeats the pipeline's purpose: whatever the tests proved, they proved it about a different build. Two builds from the same commit differ by timestamps, by a transitively floating dependency, by a base image tag that moved, by the toolchain on a newer runner image. Most of the time this is invisible, and the time it is not is a production-only failure with no reproduction.

The shape that works:

1. Build once, on the commit, producing an artefact with a content identity — an image digest, a checksummed archive, a version-stamped package.
2. Refer to it by that digest everywhere after, never by a mutable tag. Promotion moves a pointer; it does not build.
3. Keep configuration out of the artefact. Anything that differs between staging and production is injected at deploy time, because a per-environment build is a rebuild wearing a disguise.
4. Record provenance next to the artefact: the commit, the pipeline run, the inputs. Signing and attestation belong here if you do them.
5. Let each environment's gate decide whether the pointer moves, and make the gates the only difference between environments.

The test for whether you have it: from a production deployment, can you name the exact pipeline run that produced those bytes, and is that run the one whose tests went green? If the answer needs an assumption, the promotion path is not build-once.

`references/promotion.md` covers artefact identity and retention, the environment gate shape, the approval and deployment-protection mechanics, and how secrets are scoped per environment. Read it when designing the path from a merged commit to production.

### 7. Let secrets in at the job that needs them, and no earlier

Secrets scoping is a design decision made in the stage graph, not a configuration detail added at the end. Every job that can read a credential is a job whose compromise leaks it, and the jobs most likely to run attacker-influenced code — building a fork's pull request, running tests that execute repository code, installing dependencies — are exactly the ones with no need for one.

- Give credentials to the deploy and publish jobs. Test, lint and build jobs get none, which also makes them safe to run on untrusted pull requests.
- Prefer short-lived federated credentials over stored long-lived keys where the provider supports it. A workflow that exchanges an OIDC token for a role has nothing to leak between runs.
- Set permissions at the lowest scope the provider offers, and default the workflow to read-only, raising it per job that genuinely writes.
- Pass a secret through the environment rather than as a command argument. Arguments appear in process listings, in shell traces, and in the error message a tool prints when it fails to parse them.
- A fork pull request should not receive secrets, so any job that needs one has to run somewhere else. Designing that split early is much cheaper than retrofitting it after someone discovers the pipeline cannot test contributions.

Scoping secrets is a structural decision made once, here. Auditing a workflow that already exists — whether `pull_request_target` or `workflow_run` actually holds to that split, whether every pin has a SHA, whether a stored cloud key could be OIDC instead — is `pipeline-hardening`.

### 8. Write the flake policy before the first flake

The policy has to exist before the incident, because during the incident the only options that fit in the moment are "re-run it" and "make it advisory", and the second one is permanent. State, in the pipeline's own documentation:

- What a developer does when a blocking check goes red and they believe it is not their change: who they tell, and what happens to the run.
- The threshold at which a check leaves the blocking set — a specific observed rate over a specific window, agreed in advance.
- Where a quarantined check goes: still executed, reported as advisory, owned by a named person, with a date by which it is fixed or deleted.
- That the quarantine list is reviewed, because an unreviewed quarantine is just a slower deletion.

Deleting a check honestly is better than keeping one nobody believes. `ci-triage` owns the diagnosis of an individual red run; what belongs here is the standing rule that decides what happens to the check afterwards.

### 9. Give the pipeline the same observability you give production

The pipeline is a production system whose users are the developers. Record per-job duration, queue time, cache hit rate, failure rate per check and cost per run, and look at them on a schedule. Every one of the defects above shows up as a trend long before anyone complains, and none of them shows up in a single green run.

## Output format

```markdown
## Blocking set
| Check | Class | Owner | First action on red | Observed failure rate on main |

## Stage graph
[Jobs as nodes, with a reason on every edge. The critical path named, with its duration.]

## Wall-clock budget
Now:    p50 / p95 / critical path
Target: [the number people will wait for, and what moved off the critical path to get there]

## Matrix
[Axes, cells, fail-fast setting, and the aggregate job that carries the required check name.]

## Caching
| Cache | Key inputs | Restore keys | Expected hit rate | Save scope |

## Artefact and promotion
[What is built, its identity, and the gate at each environment. Configuration injected where.]

## Secrets
| Secret or credential | Jobs that can read it | Mechanism | Fork pull request behaviour |

## Flake policy
[Threshold for leaving the blocking set, where quarantined checks go, review cadence.]
```

## Anti-patterns

**Designing stages first and deciding what is required afterwards.** The blocking set determines which work is on the critical path, so choosing it last means the layout was optimised for the wrong thing. It also means the required checks get chosen by whoever configures branch protection, usually by selecting everything in the list.

**A required check nobody trusts.** It fails intermittently, everyone knows the ritual for it, and the ritual is re-running until it is green. The check is costing runner minutes and delivering no signal, and worse, it has taught the team that a red check is something to wait out. Either make it deterministic, or move it to advisory deliberately and say so.

**Stages in a line because they were written in a line.** The fastest available speed-up in most pipelines is deleting a dependency edge that exists because of file order. Every edge needs a consumed output or an avoided cost behind it.

**A cache key with the commit SHA in it.** It never hits, so every run pays the save cost for a cache nobody will ever restore, and the run history looks like caching is not helping. The mirror image is a fixed literal key, which hits every time and eventually serves bytes built against a toolchain nobody is running any more.

**Rebuilding for each environment.** Staging tested one binary and production runs another, from the same commit and therefore assumed identical. The divergence is usually a floating transitive dependency or a moved base image tag, it appears in production only, and it is unreproducible by construction because the build that failed no longer exists.

**Matrix cells as required checks.** Branch protection matches names; matrix names carry the axis values. The day the matrix drops Python 3.9 the required check named for it stops existing, and a rule satisfied by a check that never runs is a rule satisfied by nothing. Depend on the matrix from one aggregate job and require that.

**Repository-wide secrets available to every job.** The test job that runs contributor code holds the deploy credential, which means the blast radius of any dependency compromise is the production account. Scope to the job, and prefer credentials that expire.

**A pipeline nobody waits for.** Once the wait exceeds a developer's tolerance the behaviour changes rather than the pipeline: bigger pull requests, merges on partial evidence, fixes pushed and abandoned. That is a design failure, and it is measurable before anyone raises it, in the p95 you took in step 2.

## References

- `references/stage-graph.md` — worked stage graphs for library, service, container and monorepo repositories, and reusable-workflow decomposition. Read when laying out stages for a specific repository shape.
- `references/caching.md` — per-ecosystem cache key recipes, restore-key rules, hit-rate measurement and cache trust boundaries. Read when writing cache keys or investigating a stale cache.
- `references/promotion.md` — artefact identity, environment gates, approvals, and per-environment secret scoping. Read when designing the path from a merged commit to production.
