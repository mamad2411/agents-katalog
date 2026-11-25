---
name: typespec
description: "TypeSpec 1.x: design APIs in the TypeSpec language and emit OpenAPI 3.0, 3.1 or 3.2 with the @typespec/openapi3 emitter. Covers TypeSpec 1.x (current) and upgrades from pre-1.0 TypeSpec 0.x and Cadl; no preview line exists. Use when writing or reviewing .tsp files or tspconfig.yaml, modeling REST APIs with @typespec/http (@route, @get, @post, @path, @query, @header, @body, @bodyRoot, @statusCode, @error, @useAuth with OAuth2, API key, bearer or OpenID Connect), choosing the openapi-versions emitter option, setting operationId, tags, extensions or external docs with @typespec/openapi, versioning an API with @versioned, @added, @removed, @renamedFrom and @madeOptional, converting an existing OpenAPI 3 file to TypeSpec with tsp-openapi3, or running tsp compile, tsp init and tsp format. Triggers: TypeSpec, tsp, main.tsp, tspconfig.yaml, @typespec/compiler, @typespec/http, @typespec/openapi3, @typespec/versioning, design-first API, API-first, OpenAPI generation."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# TypeSpec

TypeSpec is a language and toolset, developed by Microsoft, for defining data models and service APIs and generating artifacts such as OpenAPI from them. With this skill the agent writes TypeSpec for HTTP APIs, configures the OpenAPI 3 emitter, versions the API, and checks the emitted OpenAPI.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). TypeSpec documentation has no numbered sections, so rules cite the documentation page and heading (for example "HTTP Operations, Implicit body resolution"). When a rule and the pinned source disagree, the source wins; when the packages have moved past the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: API designer (writes TypeSpec), emitter user (configures output), or reviewer.
- Target version: TypeSpec 1.x (default, the latest 1.x release). TypeSpec 0.x, including Cadl, is legacy: read it and upgrade from it, never author it. No preview line exists; `next` builds are 1.x development builds and are not a target. See [`references/versions.md`](references/versions.md).
- Target OpenAPI version or versions: `3.0.0`, `3.1.0` or `3.2.0`. The emitter's default is `3.0.0` only.
- Whether the API is versioned, and the list of versions.
- Revision: compiler, http, openapi and openapi3 at 1.16.0, and versioning at 0.86.0, unless the project pins others. Use the project's `package.json` versions when they differ.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check npm for newer `@typespec/*` releases, read the changelogs since the pin, and update the pins.

## Invariants

1. **Declaration names are unique within a scope**, even across kinds: a model and a namespace cannot share a name (Language basics, Declarations).
2. **The service is a namespace marked `@service`**, with `@server` for each endpoint; libraries are brought in with `import` and `using` (Getting started, Defining a REST Service).
3. **Without `@body`, everything not marked `@header`, `@query` or `@path` is the request body**, and every response property not marked `@header` or `@statusCode` is the response body (HTTP Operations, Implicit body resolution).
4. **`@body` defines the body exactly; `@bodyRoot` allows metadata properties inside it** (HTTP Operations, `@body` vs `@bodyRoot`).
5. **A response marked `@error` is the error response**: `4xx,5xx` by default, emitted as the OpenAPI `default` response (HTTP Operations, Status codes; OpenAPI v3 emitter, Error Responses).
6. **`@useAuth` on a child replaces the parent's schemes**; a tuple means all of them, a union means one of them (HTTP Authentication, Application hierarchy).
7. **Set `openapi-versions` explicitly.** It accepts `3.0.0`, `3.1.0` and `3.2.0` and defaults to `["3.0.0"]` (openapi3 emitter options).
8. **Versioned TypeSpec describes the current state of the API**; versioning decorators record the version where each change happened and the previous value (Versioning guide).
9. **Unions emit `anyOf` unless the named union has `@oneOf`**, and `extends` emits `allOf` while spread and `is` copy properties (OpenAPI v3 emitter, Model Composition).
10. **`tsp init` with an external template URL can run untrusted packages**; use only templates you trust (CLI usage).

## Workflow

1. **Pick the version.** Use TypeSpec 1.x; read `package.json` of an existing project to see whether it is on 0.x.
   -> [`references/versions.md`](references/versions.md)
   ✓ The compiler, http, openapi and openapi3 packages are on the same 1.x version, or a 0.x project is marked for upgrade.
2. **Set up the project.** Node.js 22 or later, `@typespec/compiler`, a `main.tsp`, and a `tspconfig.yaml` that emits `@typespec/openapi3`.
   -> [`references/project.md`](references/project.md)
   ✓ `tsp compile .` succeeds and writes to `tsp-output/`.
3. **Model the data.** Use models, scalars, enums, unions, templates and doc comments.
   -> [`references/language.md`](references/language.md)
   ✓ Invariant 1 holds, and every public type has a doc comment.
4. **Describe the HTTP surface.** Routes, verbs, parameters, bodies, status codes, errors and authentication.
   -> [`references/http.md`](references/http.md)
   ✓ Invariants 3 to 6 hold, and every operation returns its error type in a union.
5. **Configure the OpenAPI emitter.** Choose `openapi-versions`, the output file, `operation-id-strategy` and other options, and add `@typespec/openapi` decorators where needed.
   -> [`references/openapi3-emitter.md`](references/openapi3-emitter.md)
   ✓ Invariant 7 holds, and features that exist only in 3.2 are not expected in 3.0 output.
6. **Version the API** (only when it is versioned). Add `@versioned`, the versions enum, and change decorators.
   -> [`references/versioning.md`](references/versioning.md)
   ✓ Invariant 8 holds, and one OpenAPI file is emitted per version.
7. **Check the output.** Compile with warnings as errors, then validate each emitted file against the official OpenAPI JSON Schema for its version.
   -> [`references/openapi3-emitter.md`](references/openapi3-emitter.md)
   ✓ No warnings, and every emitted file validates.
8. **Upgrade** (only when asked). Follow the upgrade section from the project's version to the target: 0.x to 1.x, or within 1.x.
   -> [`references/versions.md`](references/versions.md)
   ✓ The project compiles with `--warn-as-error`, and the emitted OpenAPI differs only where the upgrade notes say it should.

## Verify before done

- [ ] `tsp compile . --warn-as-error` exits with code zero (Configuration, `warn-as-error`).
- [ ] `tsp format` leaves the `.tsp` files unchanged (CLI usage).
- [ ] Each emitted OpenAPI file validates against the official OAS JSON Schema for its `openapi` version; the `openapi` skill lists the schemas.
- [ ] Every versioned output (`openapi.v1.yaml`, `openapi.v2.yaml`, ...) reflects the right shape for that version (Versioning guide).
- [ ] Operation IDs are stable and unique; set `@operationId` where the default would change on refactoring (OpenAPI v3 emitter, Operation ID).
- [ ] Authentication appears as `securitySchemes` and security requirements in the output (OpenAPI v3 emitter, Security Definitions).

## Reference index

- **`references/versions.md`**: the TypeSpec 1.x and 0.x lines, which packages are stable or preview, what changed at 1.0, upgrade steps, and why no preview is listed. Load for steps 1 and 8.
- **`references/project.md`**: installation, `tspconfig.yaml`, the `tsp` CLI and linting. Load for steps 2 and 7.
- **`references/language.md`**: language basics with examples. Load for step 3.
- **`references/http.md`**: `@typespec/http` decorators, body and status code rules, files, visibility and authentication. Load for step 4.
- **`references/openapi3-emitter.md`**: emitter options, OpenAPI version support, the TypeSpec to OpenAPI mapping, `@typespec/openapi` decorators and `tsp-openapi3`. Load for steps 5 and 7.
- **`references/versioning.md`**: `@typespec/versioning` decorators and patterns. Load for step 6.

## Related skills

- `openapi` for the OpenAPI documents TypeSpec emits, their versions and validation: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi`.
- `openapi-overlay` for changes to emitted OpenAPI that should stay outside the TypeSpec source: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi-overlay`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [TypeSpec documentation](https://typespec.io/docs/): Living documentation for the latest release, as published, checked 2026-10-02.
- [Language basics overview](https://typespec.io/docs/language-basics/overview/): Living documentation, as published, checked 2026-10-02.
- [Getting started with TypeSpec for REST APIs](https://typespec.io/docs/getting-started/getting-started-rest/01-setup-basic-syntax/): Living documentation, as published, checked 2026-10-02.
- [CLI usage](https://typespec.io/docs/handbook/cli/): Living documentation, as published, checked 2026-10-02.
- [Configuration](https://typespec.io/docs/handbook/configuration/configuration/): Living documentation, as published, checked 2026-10-02.
- [HTTP Operations](https://typespec.io/docs/libraries/http/operations/): Living documentation, as published, checked 2026-10-02.
- [HTTP Authentication](https://typespec.io/docs/libraries/http/authentication/): Living documentation, as published, checked 2026-10-02.
- [HTTP decorators reference](https://typespec.io/docs/libraries/http/reference/decorators/): Living documentation, as published, checked 2026-10-02.
- [@typespec/http 1.16.0 auth.tsp](https://unpkg.com/@typespec/http@1.16.0/lib/auth.tsp): Released, 1.16.0 (2026-09-09), checked 2026-10-02.
- [OpenAPI v3 emitter guide](https://typespec.io/docs/emitters/openapi3/openapi/): Living documentation, as published, checked 2026-10-02.
- [@typespec/openapi3 emitter options](https://typespec.io/docs/emitters/openapi3/reference/emitter/): Living documentation, as published, checked 2026-10-02.
- [@typespec/openapi3 1.16.0 README](https://unpkg.com/@typespec/openapi3@1.16.0/README.md): Released, 1.16.0 (2026-09-09), checked 2026-10-02.
- [@typespec/openapi3 1.16.0 package.json](https://unpkg.com/@typespec/openapi3@1.16.0/package.json): Released, 1.16.0 (2026-09-09), checked 2026-10-02.
- [@typespec/openapi3 1.16.0 emitter options schema](https://unpkg.com/@typespec/openapi3@1.16.0/dist/src/lib.js): Released, 1.16.0 (2026-09-09), checked 2026-10-02.
- [@typespec/openapi3 1.16.0 emitter source](https://unpkg.com/@typespec/openapi3@1.16.0/dist/src/openapi.js): Released, 1.16.0 (2026-09-09), checked 2026-10-02.
- [@typespec/openapi3 changelog](https://raw.githubusercontent.com/microsoft/typespec/843c089f3050f46e7428d51401298825570ed3a5/packages/openapi3/CHANGELOG.md): Changelog, commit 843c089 (2026-10-02), entries through 1.16.0, checked 2026-10-02.
- [TypeSpec 1.0.0 release notes](https://typespec.io/release-notes/typespec-1-0-0/): Release notes, 1.0.0 (2025-05-06), checked 2026-10-05.
- [TypeSpec 1.0.0-rc.0 release notes](https://typespec.io/release-notes/typespec-1-0-0-rc-0/): Release notes, 1.0.0-rc.0 (2025-04-02), checked 2026-10-05.
- [TypeSpec 0.67 release notes](https://typespec.io/release-notes/typespec-0-67/): Release notes, 0.67 (last 0.x minor), checked 2026-10-05.
- [TypeSpec 1.0 GA blog post](https://typespec.io/blog/typespec-1-0-GA-release/): Announcement, 1.0 GA, checked 2026-10-05.
- [Cadl to TypeSpec migration](https://typespec.io/release-notes/cadl-typespec-migration/): Release notes, 2023-03-13 release, checked 2026-10-05.
- [@typespec/compiler on the npm registry](https://registry.npmjs.org/@typespec/compiler): Released, latest 1.16.0, next 1.17.0-dev.10, checked 2026-10-05.
- [@typespec/compiler changelog](https://raw.githubusercontent.com/microsoft/typespec/843c089f3050f46e7428d51401298825570ed3a5/packages/compiler/CHANGELOG.md): Changelog, commit 843c089 (2026-10-02), entries through 1.16.0, checked 2026-10-02.
- [OpenAPI3 to TypeSpec](https://typespec.io/docs/emitters/openapi3/cli/): Living documentation, as published, checked 2026-10-02.
- [@typespec/openapi decorators](https://typespec.io/docs/libraries/openapi/reference/decorators/): Living documentation, as published, checked 2026-10-02.
- [Versioning guide](https://typespec.io/docs/libraries/versioning/guide/): Living documentation, as published, checked 2026-10-02.
- [Versioning decorators reference](https://typespec.io/docs/libraries/versioning/reference/decorators/): Living documentation, as published, checked 2026-10-02.
- [@typespec/versioning 0.86.0 package](https://unpkg.com/@typespec/versioning@0.86.0/package.json): Released, 0.86.0 (2026-09-09), pre-1.0, draft posture: build, checked 2026-10-02.
