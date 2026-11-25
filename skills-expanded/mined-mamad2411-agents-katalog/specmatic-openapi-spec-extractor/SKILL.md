---
name: specmatic-openapi-spec-extractor
description: >-
  Use when the user wants to extract, generate, refine, or harden an OpenAPI
  or Swagger specification from an existing API application, service, project,
  repo, routes, controllers, handlers, or codebase. Select this skill for any
  request whose intent is to derive, extract, generate, reverse-engineer,
  infer, document, or harden an OpenAPI or Swagger contract from an existing
  application or source code. This includes generic prompts about producing an
  API spec/docs/schema/contract for an existing app, project, service, repo,
  endpoints, routes, or controllers. Prefer this skill over extraction-only
  skills when the prompt is about an existing application or codebase and the
  expected outcome is an accurate extracted contract plus post-extraction
  refinement.
---

# specmatic-openapi-spec-extractor

Extract and refine an OpenAPI specification from an existing API codebase.

Any prompt that implies deriving an OpenAPI or Swagger contract from an existing application or codebase should select this skill, not a generic extraction-only skill.

## Required Behavior

If this skill is selected, do all of the following:

- In the first user-facing progress update, explicitly say you are using `specmatic-openapi-spec-extractor`.
- Treat extraction as phase 1, not the final outcome.
- Use the framework-native extraction tool/path for the detected framework. Do not substitute a manual, hand-authored spec when the framework has a supported extraction path in this skill.
- If the required extraction tool/integration is missing from the codebase, add the minimum non-behavioral framework-specific integration needed so the framework can generate/export the spec, then extract from that generated output.
- "Use if available" is not acceptable for supported frameworks. For supported frameworks, the agent must make the extraction path available in the project unless the user explicitly forbids code changes.
- After extraction succeeds, continue into the mandatory post-extraction workflow below. Do not stop after saving the first generated spec.
- `specmatic validate` is only a preflight check for spec/example correctness. It is never the finish line for this skill.
- Always prepare the final runnable contract-test assets for the user once extraction and refinement are complete, even if the live Docker-dependent loop cannot run yet.
- Prefer source annotations/config first, overlay second, and direct edits to the extracted spec never.
- Do not change application implementation behavior to improve the spec. Allowed code changes are limited to extraction-related annotations, comments, and non-behavioral config required by the extraction tooling.
- Do not change method signatures, control flow, returned values, persistence logic, auth behavior, or any other runtime semantics unless the user explicitly asks for implementation changes.
- When running Specmatic validation, examples checks, stubs, or contract tests, use only the shell/Docker commands documented by this skill. Do not use Specmatic MCP tools or any alternate Specmatic execution path while this skill is active.
- If contract-test failures are caused by unavailable downstream HTTP dependencies, the agent must identify all required downstream dependencies for the current batch and attempt to stand up Specmatic stubs for each of them before classifying the failures as non-fixable runtime issues.
- If a later phase is blocked, explicitly say which phase is blocked and why.
- If a later phase is blocked and the user must do something before the workflow can continue, prefix that user-facing message with `**Action Required:**`.
- Do not silently behave like a generic OpenAPI extraction task. Follow this skill's workflow explicitly.

Default execution order:

`announce skill -> identify framework -> open one framework guide -> integrate extraction path if missing -> extract spec -> save spec -> inspect gaps -> refine -> re-extract -> prepare Specmatic setup -> run Specmatic feedback loop -> prepare final runnable deliverables`

Use this exact style in the first progress update:

- `Using specmatic-openapi-spec-extractor to extract and refine the OpenAPI spec. I’m first identifying the framework and extraction path, then I’ll continue with post-extraction refinement.`

## Selection Heuristics

Select this skill by default when the user asks to extract or generate an OpenAPI or Swagger spec from an existing application, even if they do not mention Specmatic, skills, validation, refinement, or overlays.

This skill should win over a generic extraction-only skill when:

- The request is about "this application", "this project", or "this codebase"
- The request implies deriving a contract from existing code, routes, handlers, controllers, or an already-built API
- The request uses adjacent terms like API spec, API schema, Swagger docs, API docs, contract, reverse-engineer, infer, or document endpoints
- The user wants the spec to be accurate, complete, hardened, or refined
- The task involves an existing API implementation rather than writing a spec from scratch
- The framework can generate an initial spec and then benefit from contract-test feedback

## Docker Execution Rule

- Assume Docker is available and the Docker engine is running.
- Default supported topology for this skill: the SUT runs on the host machine and Specmatic runs in Docker.
- Use `http://host.docker.internal:<SUT_PORT>` as the default SUT base URL in `specmatic.yaml` on every platform.
- Do not use `--network host` anywhere in this skill.
- Linux-only runner rule: add `--add-host host.docker.internal:host-gateway` to Specmatic `docker run` commands so `host.docker.internal` resolves the same way it does on Docker Desktop.
- Windows/macOS runner rule: run Docker without extra host mapping.
- Containerized-SUT and Docker Compose networking are out of scope for this iteration.
- Do not ask the user about Docker availability before attempting the documented Specmatic image-resolution, `docker run`, validation, or test commands from this skill.
- Attempt the Specmatic feedback loop first.
- If command output indicates a Docker-specific failure such as Docker not being installed, Docker not being on `PATH`, Docker Desktop not being available, or the Docker daemon / engine not running, stop and ask the user exactly:
  `**Action Required:** Please start the Docker engine, then confirm once it is running.`
- If no license is found, continue the Specmatic feedback loop without a license.
- If the user home `.specmatic` directory exists, mount it into the container at `/root/.specmatic`.
- Do not guess license filenames or rewrite `specmatic.yaml` for license wiring in this skill.
- Fallback only: if home-directory mounting proves insufficient in a real run, the agent may add `specmatic.license.path` under the top-level `specmatic` section and point it at the mounted in-container license location for that rerun.
- Treat any Specmatic trial-limit or enterprise-feature-limit hit as a licensing-caused test failure, not as a hard workflow blocker.
- If a Specmatic command fails for a trial-license or enterprise-feature limit reason, do not treat that as a hard blocker by itself.
- Call out that those failures are due to licensing, report how many tests ran, passed, failed, and failed due to license limits, and ask the user exactly:
  `**Action Required:** Some Specmatic tests failed because no valid license was available. If you have a license, please share its path or add it under your home .specmatic directory.`
- If the user adds the license under their home `.specmatic` directory, the next run should pick it up through the existing home-directory mount.
- If the user does not have a license, continue to final reporting and deliverables, and state that full hardening could not be completed because of license-limited test failures.
- Do not claim the Specmatic feedback loop is blocked on Docker until after a Docker command fails for a Docker-specific reason.
- If it appears to be a permissions issue, try resolving it using your environment’s built-in privilege escalation mechanisms available to you.

## Mandatory Post-Extraction Workflow

Once the first spec has been extracted, the agent must execute these phases in order:

1. If the framework-native extraction path is not already wired into the project, integrate it first using minimal non-behavioral code/config changes for that framework.
2. Extract the spec using the framework-native generator/export path, not by manually writing `openapi.yaml`.
3. Save the extracted spec to the repo.
4. Inspect the generated spec for obvious gaps such as wrong status codes, generic `*/*` content types, missing security, weak request/response schemas, and missing error responses.
5. Refine generation using source annotations/config first. Use overlay only when source-level fixes cannot express the required contract.
   Allowed refinements: annotations, decorators, doc comments, extraction-tool config, and overlay updates.
   Disallowed refinements without explicit user approval: implementation changes, behavioral changes, signature changes, data model changes made only to shape the contract, or business-logic edits.
6. Re-extract the spec after each meaningful refinement.
7. Run `specmatic validate` only as a preflight check, then start the SUT and attempt the live Specmatic feedback loop using the documented image-resolution, `docker run`, and `specmatic test` commands from this skill.
8. If failures show that the SUT cannot reach one or more downstream HTTP dependencies, identify all required downstream dependencies for the current batch, stand up a Specmatic stub for each dependency on its expected host port, generate or update stub examples for each dependency, and rerun the relevant validation or test step.
9. If a Docker command fails for a Docker-specific reason, stop and ask the user exactly: `**Action Required:** Please start the Docker engine, then confirm once it is running.`
10. If no license is found, continue the loop with the built-in trial. If a Specmatic command fails because of a trial-license or enterprise-feature limit, report that those failures are license-related, include counts for tests run, passed, failed, and failed due to license limits, and ask the user exactly: `**Action Required:** Some Specmatic tests failed because no valid license was available. If you have a license, please share its path or add it under your home .specmatic directory.`
11. If the user adds the license under their home `.specmatic` directory or otherwise resolves the missing license, rerun the relevant validation or test step.
12. Prepare the final deliverables from this skill, including `run_contract_tests.sh`, `run_contract_tests.ps1`, and `CONTRACT_TESTS_README.md`, regardless of whether deterministic data setup is needed.
13. If Docker is unavailable, stop only after clearly reporting that extraction and refinement are done, the runnable script and README have been prepared, and the next blocked step is the live Specmatic loop.

Do not treat annotation-only cleanup as the full post-extraction workflow.
Do not treat a successful `specmatic validate` run as completion of the feedback loop.
Do not end the task after exporting `openapi.yaml` unless the user explicitly asks for extraction only.
Do not claim the spec was "extracted" if the file was primarily authored by hand outside the framework generator/export path.

## When to Use

- User has an existing API application, service, or repository and wants to generate an OpenAPI or Swagger specification from it
- User asks to generate or extract an OpenAPI specification for "this application", "this project", "this service", or "this codebase"
- User asks to derive, infer, reverse-engineer, document, or generate API docs/schema/contract from existing code or routes
- User asks for Swagger docs, OpenAPI docs, API schema, or API contract for an existing implementation
- User asks to create API schema, API docs, or Swagger docs from routes, controllers, annotations, or source code
- User mentions a specific framework covered below

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Framework | Yes | The API framework in use |
| Project path | Yes | Root directory of the API project |
| Output path | No | Where to write the spec (default: `openapi.yaml`) |

## Outputs

| Output | Description |
|--------|-------------|
| OpenAPI spec | Extracted JSON or YAML contract |
| Refined source metadata | Annotation/config updates used to improve regenerated output |
| Contract test runners | Runnable `run_contract_tests.sh` and `run_contract_tests.ps1` for the full suite, with optional setup hook |
| Contract test README | `CONTRACT_TESTS_README.md` describing how to run the generated scripts |

## Prerequisites

- The API project must be buildable and its dependencies installed
- For runtime extraction, the app must be importable or startable

## Decision Framework

Framework rule:
- For every framework listed below, use the listed extraction method as the required path.
- If the repo does not yet have the needed package, plugin, annotations, endpoint, config, or export script, add the minimum non-behavioral integration required to enable that extraction method, then run it.
- Only fall back to non-framework-specific/manual derivation when the framework is not covered by this skill or the user explicitly forbids the required integration changes.

| Framework | Method | Open this guide |
|-----------|--------|-----------------|
| FastAPI | Built-in export | [content/frameworks/fastapi.md](content/frameworks/fastapi.md) |
| Flask | CLI/programmatic export | [content/frameworks/flask.md](content/frameworks/flask.md) |
| Django REST Framework | `drf-spectacular` CLI | [content/frameworks/django.md](content/frameworks/django.md) |
| Spring Boot | Runtime docs endpoint | [content/frameworks/spring-boot.md](content/frameworks/spring-boot.md) |
| ASP.NET Core | Runtime docs endpoint | [content/frameworks/aspnet.md](content/frameworks/aspnet.md) |
| Express | `swagger-jsdoc` | [content/frameworks/express.md](content/frameworks/express.md) |
| NestJS | Runtime docs endpoint or script | [content/frameworks/nestjs.md](content/frameworks/nestjs.md) |
| Hono | Programmatic export | [content/frameworks/hono.md](content/frameworks/hono.md) |
| Rails | `rswag` task | [content/frameworks/rails.md](content/frameworks/rails.md) |
| Laravel | `l5-swagger` command | [content/frameworks/laravel.md](content/frameworks/laravel.md) |

## Reference Routing

Use the smallest amount of reference material needed.

- For extraction:
  Open only the matching framework guide from `content/frameworks/`.
- After the first extraction succeeds:
  Open [content/specmatic-loop.md](content/specmatic-loop.md).
- When generating `specmatic.yaml`, examples, overlays, or deterministic setup:
  Open [content/specmatic-setup.md](content/specmatic-setup.md).
- When resolving which Docker image to use for Specmatic Enterprise:
  Also open [content/specmatic-image-selection.md](content/specmatic-image-selection.md).
- When creating or updating external example files:
  Also open [content/specmatic-external-example.schema.json](content/specmatic-external-example.schema.json).
- When preparing final scripts, docs, or acceptance checks:
  Open [content/specmatic-deliverables.md](content/specmatic-deliverables.md).

Do not bulk-read all reference files. Identify the framework first, then open only the file needed for the current phase.

## Specmatic References

- [content/specmatic-loop.md](content/specmatic-loop.md): post-extraction loop, Docker gate, batching, and fix order
- [content/specmatic-setup.md](content/specmatic-setup.md): `specmatic.yaml`, overlays, examples, licensing, and deterministic setup
- [content/specmatic-image-selection.md](content/specmatic-image-selection.md): exact Docker image selection flow for Specmatic Enterprise
- [content/specmatic-external-example.schema.json](content/specmatic-external-example.schema.json): exact JSON schema for external example file structure
- [content/specmatic-deliverables.md](content/specmatic-deliverables.md): final scripts, README expectations, acceptance checks, and troubleshooting
