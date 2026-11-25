---
name: follow-tool-scalar
description: Use Scalar to design, test, and document APIs end to end
argument-hint: "[scope]"
related:
  - run-api-docs
  - follow-tool-bruno
  - follow-tool-hurl
  - follow-test
  - follow-release
  - follow-deploy
  - follow-tool-github-actions

---

## Goal

Use Scalar to design APIs, test endpoints, and create documentation and a mock server end to end

## Scope

For projects that need API documentation, an API playground, a mock server, and schema validation using the Scalar toolchain

- Latest: `@scalar/api-reference@1.72.1` / `@scalar/cli@2.5.2` (verified 2026-09-26)

## Execute

### 1. Installation

> Goal: Install the Scalar CLI or the right package

1. Check the project stack for OpenAPI, AsyncAPI, or GraphQL
2. Install `@scalar/cli` with `bun add -D @scalar/cli` (the binary is named `scalar`, requires Node `>=24`)
3. Check the version with `bunx @scalar/cli --version` and run `bunx @scalar/cli init` to create a starting config
4. Use `@scalar/api-reference` when you want to embed the API reference in an app (React/Vue/standalone)
5. See the CLI commands in 

### 2. Configuration

> Goal: Create the Scalar config for the project

1. Create `scalar.config.json`, `scalar.config.yaml`, or `scalar.config.ts`
2. Set `title`, `description`, `proxyUrl`, `theme`, `layout`
3. Set environment variables such as `SCALAR_PORT`, `SCALAR_API_URL`
4. See the config options in 

### 3. Schema Design

> Goal: Design a correct API schema with complete documentation

1. Use the appropriate type system (OpenAPI/AsyncAPI/GraphQL)
2. Name types, fields, and operations clearly
3. Add descriptions, examples, and deprecation notes
4. Use enums for fixed values and input types for mutations
5. See the API patterns in 

### 4. Mock and Test

> Goal: Test APIs with a mock server and validation

1. Run a mock server with `bunx @scalar/cli document mock openapi.yaml --watch --port 8080`
2. Test queries, mutations, and error scenarios (the mock server validates requests against the OpenAPI contract by default)
3. Use `bunx @scalar/cli document validate openapi.yaml` to check schema validity and `document lint` for spectral rules
4. Use `bunx @scalar/cli document serve openapi.yaml` to preview the API reference locally — or run `/run-api-docs` to start the docs server with a browser preview
5. To test a real API from the spec → export/import into Bruno (`bru import openapi`) or write `.hurl` files — see `/deep-test api`
6. Run `/follow-test` to expand test coverage

### 5. Documentation and Deploy

> Goal: Publish documentation and integrate with CI

1. Create Markdown docs with `bunx @scalar/cli document markdown openapi.yaml` or bundle refs with `document bundle`
2. Use `@scalar/api-reference` (standalone script tag or framework integration) for HTML docs, or publish via the `scalar registry`/`scalar project`
3. Set up GitHub Actions or a CI/CD pipeline for `document validate` and deploying docs
4. Deploy to a static host such as GitHub Pages or Cloudflare Pages
5. See the official resources in 

## Rules

### 1. Schema Design

- Use descriptive names for types and fields
- Add descriptions for every public type and field
- Use examples for complex queries and mutations
- Mark deprecated fields clearly

### 2. Mock and Test

- Use a mock server for development and manual testing
- Test error scenarios and performance
- Use version control for schema changes

### 3. Documentation

- Generate docs automatically from the schema
- Deploy docs on a static host
- Update docs when the schema changes

### 4. Integration

- Use CI/CD to validate and build docs
- Never hard-code secrets or API keys
- Use environment variables for environment-specific config

- Use /follow-release if needed
- Use /follow-deploy if needed
- Use /follow-tool-github-actions if needed (tool scalar)

## References

- [CLI reference](references/cli.md)

- Use /follow-tool-bruno if needed
- Use /follow-tool-hurl if needed


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Scalar installed and configured
- An API schema that is correct and fully documented
- A working mock server
- Documentation published
- Tests and validation passing

