---
name: project-exploration
description: Maps an unfamiliar codebase before any change: stack detection from manifests and lockfiles, directory census, routes, data model, auth, tests, CI, conventions, and end to end tracing of critical flows. Use before architecture, implementation, debugging or review on unread code.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core]
  outputs: [project-map, stack-report, convention-report, flow-traces]
---

# Project Exploration

Turns an unknown repository into a set of verified facts. Nothing downstream
is allowed to guess, so this skill is what makes the rest of the suite
possible.

Exploration is proportional. A one line copy fix does not require a full
census; a new payment flow does. Section 2 sets the depth.

## 1. Entry condition

Run this skill when any of the following holds:

- the repository has not been read in this session;
- the task touches files that have not been read;
- a previous finding depends on a convention nobody verified;
- the user reports behaviour that contradicts the current mental model.

Skip it only when every file the task touches has already been read in this
session, and say so explicitly.

## 2. Depth levels

| Level | Trigger | Budget |
|---|---|---|
| L1 targeted | localized fix in code already read | the touched file, its callers, its tests |
| L2 feature | new endpoint, new page, bug of unknown origin | the vertical slice plus stack detection |
| L3 full | first contact, architecture work, security audit, release | the complete protocol below |

Declare the chosen level before starting. Escalate when a finding contradicts
the level assumption.

## 3. Protocol

### Step 1, stack detection

Read, in this order, and stop guessing the moment a file answers:

1. Package manifests: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`,
   `composer.json`, `Gemfile`, `pom.xml`, `build.gradle`.
2. Lockfiles, which reveal the package manager and the resolved versions:
   `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`,
   `poetry.lock`, `uv.lock`, `go.sum`, `Cargo.lock`.
3. Runtime and tooling config: `tsconfig.json`, framework config files,
   bundler config, linter and formatter config, `.editorconfig`.
4. Scripts section of the manifest, or the `Makefile`, or `Taskfile.yml`. This
   is the authoritative list of how the project is built, run and tested.

Output: framework and version, language and version, package manager, test
runner, linter, formatter, build tool, run commands. Each with its evidence.

### Step 2, shape of the repository

Determine whether the repository is single application, monorepo with
workspaces, or polyrepo fragment. Evidence: workspace declarations,
`turbo.json`, `nx.json`, `pnpm-workspace.yaml`, `lerna.json`, or their
absence.

Then census the source tree one level at a time. Never recurse blindly into
`node_modules`, `vendor`, `dist`, `build`, `.next`, `target`, `.venv`.

For each top level source directory, record what it holds in one line.

### Step 3, the seven maps

Build only the maps the depth level requires.

**Routes map.** Backend routes and frontend routes, each with method, path,
handler file, and whether it is public or authenticated. Source: the router
files, the file system routing convention, or the route registration calls.

**Data map.** Schema files, migrations directory, latest migration, ORM or
query builder in use, main entities and their relations. Read the schema, not
the model class names.

**Auth map.** How identity is established, where the session or token lives,
how it is verified on each request, where authorization decisions are made,
what roles exist and where they are stored.

**Boundary map.** Every point where data enters the system: HTTP handlers,
form actions, webhooks, queue consumers, CLI arguments, file uploads,
scheduled jobs, third party callbacks.

**Integration map.** External services called, the client used for each, where
credentials come from, and what happens when the service is down.

**Test map.** Frameworks, directory layout, naming convention, how to run one
test, how to run all, what is covered and what is visibly not.

**Delivery map.** CI workflows and what they enforce, deployment target,
environment variable inventory taken from example files and config, build
output.

### Step 4, convention extraction

Conventions are observed, never imported from habit. A convention needs at
least two independent occurrences before it is treated as a rule.

Record: file naming, directory placement rules, export style, error handling
pattern, logging pattern, validation library and where it is applied, data
fetching pattern, state management, styling approach, component composition
style, test structure, commit message style taken from `git log`.

When two conflicting patterns coexist, record both, note which is more recent
by file history, and follow the more recent unless the user says otherwise.

### Step 5, flow tracing

For each flow the task touches, trace it end to end and write the chain:

```
user action -> UI component -> client call -> route handler -> validation
-> authorization -> service or business logic -> data access -> external
service -> response shape -> client state -> rendered result
```

For every critical flow, trace the failure path as well: what happens on
invalid input, on denied permission, on database error, on third party
timeout, on duplicate submission.

A flow trace that cannot be completed marks the gap as `Unknown` and names the
file where the chain broke.

### Step 6, risk pass

While reading, note without fixing: missing validation at a boundary,
authorization checked in the UI only, secrets in tracked files, unbounded
queries, absent timeouts, silent catch blocks, untested critical paths. Hand
this list to `security-audit` or `code-review-protocol`.

## 4. Deliverable

A project map, compact, with evidence attached to each line:

```
Stack
  framework, language, package manager, runner, linter, build
Shape
  monorepo or single app, workspaces, top level directories
Routes
  count, list of those relevant to the task
Data
  engine, ORM, entities touched by the task
Auth
  mechanism, verification point, authorization model
Boundaries
  entry points relevant to the task
Conventions
  the rules the change must follow
Flows
  the traced chain for each flow the task touches
Commands
  install, run, test, lint, build, typecheck
Unknowns
  named missing facts and what they block
```

Length target: one screen for L1 and L2, two screens for L3. Exploration that
produces more text than the change it enables has failed its purpose.

## 5. Prohibitions

- No conclusion from a directory listing alone. Directory names lie.
- No stack claim from a single config file when a lockfile exists.
- No convention claimed from one occurrence.
- No reading of dependency source trees to answer a project question.
- No exhaustive dump of file contents into the report.
- No question to the user about anything the repository states.

## 6. Auto-critique

Score from 0 to 5: evidence attached to every claim, correct depth level,
completeness of the maps the task needs, quality of the flow traces including
failure paths, conventions actually extracted rather than assumed, explicit
list of unknowns, conciseness.

Threshold: no axis below 3, average at least 4. A map with an unmarked gap is
below threshold whatever the other scores.

## 7. Interfaces

- Upstream: `engineering-core`, `engineering-orchestrator`.
- Downstream: every implementation, review, security and testing skill.
- Feeds: `architecture-design` with the current architecture,
  `security-audit` with the boundary map, `testing-quality` with the test map,
  `project-continuity` with the stack and command inventory.
