---
name: dev-ones-app
description: Evaluate, design, implement, and deliver ONES Apps (ONES Plugin / `.opkx`) against local ONES App specs. Use for feasibility assessment, capability mapping, implementation planning, and delivery across OpenAPI, Hosted API, Events, Extensions, Web SDK, and manifest/runtime configuration.
---

## Goal
Convert ONES App requirements into spec-backed `.opkx` solutions that can be evaluated, built, and delivered.

## App Model And Runtime Defaults

- In this skill, a ONES App means a ONES Hosted App unless the user explicitly says they need an externally hosted app.
- Backend code runs in the ONES runtime container.
- Default backend language is Node.js.
- Default backend framework is NestJS.
- Frontend code runs in the ONES frontend sandbox.
- Default frontend framework is React.
- Open Platform ability families include OpenAPI, Events, Extensions, Web SDK, and lifecycle callbacks.
- Hosted ability families include structured data storage and file storage.

## Scope
- Clarify requirements, assess feasibility, map capabilities, design solutions, implement features, and deliver ONES Apps (`.opkx`).
- Validate OpenAPI, Hosted API, Events, Extensions, Web SDK, and manifest/runtime capabilities against `.ones/ones-app-specs`.
- Provide a minimum viable demo path when the user needs a starting point.

## Spec Source And Selection Rules

- Prefer project-level specs: `<project>/.ones/ones-app-specs`
- If project-level specs do not exist, use global specs: `~/.ones/ones-app-specs`
- Install the `ones` CLI with `npm install -g @ones-open/cli`
- When working inside a project, run `ones specs fetch --dir "$(pwd)"` first to ensure the specs match the current project version
- Requirement evaluation, capability mapping, and implementation decisions must all be traceable to local spec files. Do not answer from memory.
- Follow [references/ones-app-specs-playbook.md](references/ones-app-specs-playbook.md) to search `.ones/ones-app-specs`.
- Use these lightweight references only when needed:
  - `references/ones-cli-playbook.md`
  - `references/ones-app-dev-playbook.md`

## Default Flow For Requirement Evaluation

Use this default flow when the user asks "can this be done", "how do I do this", or "what scopes / events / extensions / manifest fields are required":

1. Load `references/ones-app-specs-playbook.md` first
2. Normalize the capability terms and business object terms in the requirement
3. Inspect `capability-tree.json` and `guide/guide-index.json` first to narrow the search scope
4. Then use `rg` to search `openapi-spec.yaml`, `hosted-api/*.yaml`, `schemas/**/*.json`, and `guide/**/*.mdx`
5. Output a capability evidence table. If there is no local evidence, classify it as `REQUIRES CLARIFICATION` or `unsupported` according to the playbook rules

## First Response Requirements

After receiving a requirement, the first reply should include these three sections by default:

1. Requirement understanding checklist
- List the requirement points in numbered form
- Mark high-risk assumptions as `Pending confirmation`

2. Capability mapping draft
- List items in the format "requirement point -> ONES capability type -> initial evidence entry point"
- List temporarily unmapped items separately

3. Next actions
- State which spec files will be searched next
- If critical information is missing, ask only the minimum questions that affect capability judgment

## Standard Flow From Requirement To Implementation

1. Requirement collection and clarification
- When the user requirement is incomplete, fill in the key details that affect capability judgment first: runtime mode, OAuth / scope, event source, extension entry point, storage, and delivery form
- When the user has no clear requirement, provide a minimum viable demo path

2. Requirement confirmation
- Repeat back the understanding in a numbered list
- Clearly distinguish what the user has confirmed from what is still an assumption

3. Feasibility evaluation
- Every requirement point must map to local spec evidence
- Mark it as `supported` when clear evidence exists
- Mark it as `REQUIRES CLARIFICATION` when the user's wording is too unclear to decide
- After targeted search, if there is still no matching capability evidence, mark it directly as `unsupported`

4. Solution design (complex requirements)
- Complex requirements must cover: manifest changes, backend endpoints / services, frontend pages / Web SDK, storage model, authentication / scope, and verification path
- Backend callback path:
  - Use this path when the feature is mainly triggered by an event callback or lifecycle callback, and may also call OpenAPI or persist business data or files.
  - Inspect the current project's event, lifecycle, OpenAPI, hosted API, and schema files.
  - If there is no clear match, tell the user which capability is unsupported or still requires clarification.
  - If there is a clear match, implement the callback flow according to the project specs.
- Frontend interaction path:
  - Use this path when the feature is mainly triggered by interaction in a frontend page, and may also call OpenAPI, the app backend API, or persist business data or files.
  - Inspect the current project's extension docs, Web SDK docs, OpenAPI specs, hosted specs, and related schemas.
  - Use `ONES.fetchApp` for app backend calls and confirm the backend route exists in the current app.
  - Use `ONES.fetchOpenAPI` for ONES platform API calls.
  - When frontend OpenAPI calls need `teamUUID` or `orgUUID`, use `ONES.getTeamInfo()`.
  - When implementing frontend UI, inspect the project's installed `@ones-design/core` usage first.
  - Prefer `@ones-design/table` for table scenarios.
  - Prefer `@ones-design/core` for common components such as `Button`, `Modal`, and `Space`.
  - If frontend code uses raw `fetch`, `XMLHttpRequest`, or `axios` to call suspicious internal paths such as `/api/project/...`, treat that as high risk and verify whether it should instead be `ONES.fetchApp` or `ONES.fetchOpenAPI`.

5. Task breakdown and progress tracking (complex requirements)
- Break the work into executable tasks, covering at least: spec mapping, manifest, backend, frontend, storage, and verification
- Continuously update current progress and blockers during execution

6. Development and verification
- Complete the minimum vertical slice first, then add enhancements
- At minimum, verify build, key callbacks, key permissions, and key page or API paths

7. Delivery
- Produce the `.opkx`
- Explain installation steps, verification steps, known limitations, and pending confirmations

## Mandatory Command Rules

- When creating a project, use `ones create`. Do not replace it with manual scaffolding unless the user explicitly asks for that.
- Prefer `ones build` to generate the deliverable.
- Do not use `ones dev` unless the task is local development, debugging, or issue diagnosis.
- The tools for debugging an app against a real ONES environment are `ones app`, `ones dev`, and `ones tunnel`. Before using them, the user must manually run `ones login` to ensure they are logged in. Use `ones whoami` to confirm the login status.
- Use `ones app logs` when runtime logs are needed.

## Environment And Project Preparation

### Environment Preparation

- Confirm whether `ones` exists.
- Run `ones`.
- Run `ones app`.
- Continue only if these commands return normal output without errors.

If any of these checks fail, install or upgrade the CLI with:

```bash
curl -fsSL "https://open.ones.cn/quickstart.sh" | bash
```

### Project Preparation

- If the current directory already contains `opkx.json`, treat it as an existing ONES App.
- If `.ones/ones-app-specs` does not exist, fetch it with `ones specs fetch --dir "/real/project/path"`.
- Replace `"/real/project/path"` with the real project path and keep the surrounding double quotes.
- After `.ones/ones-app-specs` is available, treat the current project's relative paths under it as the primary implementation reference.
- Even when specs already exist, refresh them before capability mapping if there is any doubt that they match the current project version.

## Recommended Development Workflow

1. Create the project
> If the user specified a directory and it already contains `opkx.json`, this step can be skipped.

```bash
ones create <project-path>
# Optional: generate only the manifest (opkx.json)
ones create <project-path> --manifest-only
```

2. Pull the spec documents into the project workspace

```bash
cd <project-path>
ones specs fetch --dir "$(pwd)"
```

3. Build and produce the artifact (default path)

```bash
cd <project-path>
ones build
# Optional examples
ones build --output ./dist/app.opkx
ones build --command "pnpm build"
```

4. Use dev mode only when necessary (exception path)

```bash
cd <project-path>
ones dev
# Optional examples
ones dev --install
ones dev --command "pnpm dev"
```

5. Install and verify
If the user is already logged in and has confirmed that the app is installed, the following command can be used to fetch app logs:
```bash
ones app logs <app-id>
# Optional examples
ones app logs --from-opkx-json
ones app logs --tail 100
```

Install decision rules:

- if the user is still in the context of developing the app and asks to install it, use `ones app install`
- if the user asks to build first and then install, guide them to upload the generated `.opkx` file in the ONES app management page
- if remote CLI actions require authentication, ask the user to run `ones login` first and use `ones whoami` to confirm status

`ones build` is the default schema validation gate for OPKX. Do not introduce extra custom OPKX schema validation logic unless the user explicitly asks for it.

## Complex Requirement Criteria

A requirement is considered complex if any of the following conditions are met:

- It combines 2 or more capability categories, such as Events + OpenAPI, Extensions + Storage, or Web SDK + OAuth
- It involves cross-entity data flow, aggregation, permission boundaries, or multi-role workflows
- It requires engineering details such as settings pages, storage models, error handling, retries, or async callbacks

For complex requirements, present the solution first, then move to implementation.

If command behavior is uncertain, check the help first:

```bash
ones --help
ones create --help
ones specs -h
ones specs fetch -h
ones dev --help
ones build --help
```

## How To Use `.ones/ones-app-specs`
Follow [references/ones-app-specs-playbook.md](references/ones-app-specs-playbook.md) and use the files in `.ones/ones-app-specs` to evaluate requirements, design solutions, and implement features.

Use the playbook to:

- determine the correct spec directory
- narrow the search scope with index files first
- search OpenAPI, Hosted API, schema, and guide files with `rg`
- extract evidence before making capability claims
- move from evidence to implementation

## Capability Mapping Principles

- Determine the runtime mode first
  - Externally hosted app: use `schemas/app_manifest_schema.json`
  - ONES hosted app (`ones create` project, default): use `schemas/app_opkx_schema.json`
- Use Guide files to understand flows, examples, and caveats
- Use Schema files to confirm manifest fields, event / extension contracts, enums, and required fields
- Use OpenAPI / Hosted API files to confirm paths, methods, scopes, parameters, and responses
- Do not invent endpoints / fields / contracts / manifest keys
- When the user's wording is too unclear to decide, mark it as `REQUIRES CLARIFICATION`
- If targeted searches across the relevant guide, schema, OpenAPI, and Hosted API files still find no local evidence, mark it explicitly as `unsupported`
- Unless the user explicitly asks for an alternative route, do not invent manual fallback solutions for missing capabilities
- Keep implementation decisions linked to evidence files so auth / scope / contract stays aligned with the spec
- Before finishing, confirm every delivered feature has corresponding evidence and run `ones build`

## Output Standard

Evaluation or implementation output should include these sections by default:

- Requirement understanding checklist
- Capability evidence table
- For complex requirements, an implementation checklist covering: manifest, backend, frontend, storage, and verification

The capability evidence table should include these fields:

- requirement
- capability type (`openapi`, `hosted_api`, `event`, `extension`, `websdk`, `schema`)
- evidence file path
- evidence pointer (`#/paths/...`, schema field, or document section)
- decision (`supported`, `unsupported`, or `REQUIRES CLARIFICATION`)

You may reuse templates and command snippets from:

- `references/ones-app-specs-playbook.md`
- `references/ones-cli-playbook.md`
- `references/ones-app-dev-playbook.md`

## Definition Of Done (DoD)

At minimum, a completed task satisfies:

- Requirement understanding and key assumptions are aligned
- Every implemented capability has local spec evidence
- Unsupported items are clearly marked as `unsupported`, and pending items are clearly marked as `REQUIRES CLARIFICATION`
- Complex requirements include a solution or a task breakdown
- The app can generate a `.opkx` through `ones build`
- Installation and minimum verification guidance has been provided
- Known limitations and pending confirmations are called out when they still exist at delivery time.

## Non-Negotiable Constraints

- Use `ones create` by default when creating a project.
- Run `ones specs fetch --dir "$(pwd)"` before capability mapping.
- Prefer `ones build` to generate the artifact, and treat it as the final OPKX schema validation gate.
- Use `ones dev` only when local development / debugging / troubleshooting requires it.
- The tools `ones app`, `ones dev`, and `ones tunnel` are for debugging an app against a real ONES environment. Before using them, the user must manually run `ones login` to ensure they are logged in. Use `ones whoami` to confirm the login status.
- Use `ones app logs` when runtime logs are needed.
- Treat the schemas in `.ones/ones-app-specs` as reference material, not as an independent validation system.
- Every capability claim must be traceable to local `.ones/ones-app-specs` files.
- When evidence is missing, stop and ask for clarification.

## Common Troubleshooting

- If a `ones` subcommand does not exist, reports `unknown command`, or does not appear in `ones --help`, do not assume the command is available.
- First confirm the current CLI version, then try upgrading to the latest version and retry:

```bash
ones --version
npm install -g @ones-open/cli@latest
ones --version
ones --help
```

- If the command is still unavailable after upgrading, follow the actual `ones --help` output for the current environment and treat that command as unavailable there. Do not keep giving usage based on memory.
