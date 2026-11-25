---
name: add-provider
description: Add a provider to aclif from a platform's API specification, in a chosen tier, and drive it through the conformance suite until it passes. Use when asked to add, generate, or regenerate a provider, or to cover a new SaaS API.
---

# Add a provider

A provider is one directory under `src/providers/<tier>/<name>/` that maps a platform's API onto the command surface. The inputs are all files: the API spec, `docs/CONTRACT.md`, `docs/PROVIDER_AUTHORING.md`, a finished provider to imitate, and the conformance suite, which is the acceptance test. When conformance passes, the mechanical work is done and what remains is the human review listed at the end.

## Inputs to collect first

- `name` (lower case, one word, becomes the command prefix), `displayName`, `tier` (`native`, `contributed`, or `private`).
- The machine-readable spec: OpenAPI, or the vendor's equivalent. Ask for it if only prose docs exist.
- The authentication paths the spec's `securitySchemes` describe, and which one is primary.
- Whether the API exposes metadata endpoints (object or table descriptions). If so the provider gets a tenant walk (`tenant.ts`) and schema commands.

If the spec is ambiguous about pagination, auth precedence, or which field is the record id, stop and ask before writing code.

## Read before writing

1. `docs/CONTRACT.md`: the envelope, error codes, exit codes, `aciMetadata`, introspection flags.
2. `docs/PROVIDER_AUTHORING.md`: the file checklist (section "File checklist") and every rule id (`C-META-1`, `C-CRED-2`, ...).
3. `src/providers/native/servicenow/`: the provider to imitate. Note how thin `base.ts` is and how `errors.ts` names the command that fixes each problem.
4. `test/providers/native/servicenow/servicenow.test.ts`: the fixture suite to imitate, over `msw`.

## Steps

1. Scaffold. Writes only under the tier's four prefixes.
   ```bash
   npm run scaffold-provider -- --tier <tier> --name <name> --display "<Display Name>"
   ```
2. Cover the entire spec. Every operation becomes a command; do not select a subset. Scope is enforced later, where a command is bound to an agent.
   - Command ids: `<name>:<topic>:<verb>`. Topic is the operation's first tag, else the first path segment after the version. Verb follows the uniform vocabulary where it fits: `list`, `get`, `create`, `update`, `delete`, `search`; otherwise the operationId in kebab-case.
   - `aciMetadata` from the operation: mutability from the method; blast radius from whether the path names one record; `requiresConfirmation` true for deletes, all-records operations, and anything that runs code; `capabilities: ['code_exec']` or `['metadata_change']` where they apply. Mark rows you are unsure about with a `TODO` comment.
   - Flags from parameters and the request body; required where the spec says so; enumerations become flag options.
   - `responseShape` from the response schema with the spec's example.
   - `aciExamples`: at least one runnable example per command using the spec's example values, the `$BIN` token, and `--json`. Mutations that require confirmation show `--confirm` and also a `--dry-run` example.
   - Pagination: read the spec's convention and emit `nextCommand` as a runnable `$BIN` string in `_context.pagination`.
3. Files: `credentials.ts`, `client.ts` (fetch only; a vendor SDK needs an entry in the dependency allowlist with a reason), `errors.ts`, `metadata.ts`, `base.ts` (under 40 lines, no credential logic), `plugin.ts`, `commands/**`, `tenant.ts` if the spec has metadata endpoints. Fixtures under `test/fixtures/<tier>/<name>/` built from the spec's example values. The fixture suite `test/providers/<tier>/<name>/<name>.test.ts` covering the READ, MUT, ERR, DISC, and AUTH cases from `test/helpers/provider-suite.ts` for one list command and one mutation per topic. `docs/providers/<tier>/<name>/SETUP.md` from the spec's `securitySchemes` descriptions, with `TODO` markers where a human must add admin-console steps; it must start with a heading and show how to verify with `$BIN`.
4. Constraints the suite enforces and you should not fight:
   - No `process.env` reads anywhere in the provider.
   - No hostnames, emails, tenant names, or file paths from a real deployment. Use `example.com`.
   - Every computed command string starts with the literal `$BIN` token.
   - No imports from another provider's directory, and none from `src/cli` other than the base command.
   - Do not modify files outside the four prefixes for your tier and name.
5. Run, in order, and iterate until all pass:
   ```bash
   npm run build
   npx vitest run test/conformance
   npx vitest run test/providers/<tier>/<name>
   npm run golden:capture
   npm test
   ```
   If the provider has a tenant walk, http adapter, or session support, the tenant suite will ask for a fake: add it to `test/conformance/fakes.ts` and wire it in `test/conformance/options.ts`.
6. Report every conformance failure you had to fix and what you changed. Those are the places where the spec and the contract disagreed, and the reviewer wants to know.

## What a human reviews afterwards

In order of risk: `credentials.ts` path order and which fields are secret; every `aciMetadata` row marked `TODO`, since a mutation labelled `read` or a bulk operation labelled `single_record` is a governance hole the suite cannot detect from code; the hints in `errors.ts`, where product knowledge lives; `aciExamples`, where the reviewer adds the examples that document traps; the tone and length of `metadata.ts`, which is what an agent reads first.

## In a downstream CLI package

The same workflow applies to a CLI built on the framework, with `src/providers/<name>/` in place of the tiered path, imports from `aclif` in place of relative paths into the framework, and `npm test` running `conformanceSuite` from `aclif/testing`. See `docs/BUILDING_A_CLI.md`.
