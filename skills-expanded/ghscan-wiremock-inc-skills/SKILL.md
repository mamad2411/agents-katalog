---
name: review-api-simulation
description: Review a mock API simulation built in WireMock Cloud against its source documentation, OpenAPI spec, and Arazzo workflows. Use when the user wants to verify completeness and correctness of an existing mock API.
user-invocable: true
argument-hint: "<path-to-project-folder>"
---

<!-- AUTO-GENERATED from common/skills/... — do not edit directly; edit the source and run `npm run build`. -->

## Prerequisites

This skill requires the following MCP server to be configured and running:
- **WireMock Cloud MCP** - provides tools for managing mock APIs, stubs, recordings, and OpenAPI documents

If the WireMock Cloud MCP server is unavailable, stop and inform the user before proceeding.

Arazzo workflows are executed via the `@wiremock/arazzo-runner` CLI (invoked with `npx`), not an MCP tool. Node.js v18+ must be installed. See [Running Arazzo Workflows](#running-arazzo-workflows) below.

## Reference Documentation

The following WireMock guidelines are bundled as reference files. Read the relevant files when performing those steps:

- [Validating and Fixing Stubs](../references/validating-and-fixing.md) - process for validating stubs against the OpenAPI schema and fixing errors
- [Transferring Files To and From a Mock API](../references/file-transfer.md) - the download flow used by `pull`

## Running Arazzo Workflows

Whenever this skill says to "run the Arazzo workflows", invoke the CLI directly:

```
npx @wiremock/arazzo-runner run <arazzo-path> -b <source-name>=<base-url> [-a <auth-config-file>]... -r <report-path> --no-interactive
```

- `<source-name>` must match a name in the Arazzo document's `sourceDescriptions`. Pass `-b` once per source if there are multiple.
- Pass `-a` once per authenticator config file needed (omit if the API is unauthenticated).
- Always pass `--no-interactive` so the run never blocks waiting for input.
- Always pass `-r <report-path>` (e.g. `.wiremock/<service-name>/arazzo-report.yaml`) and read that report afterwards to check for step failures or response validation errors.

## Step 1: Validate Project Folder

The project folder path is: **$ARGUMENTS**

If `$ARGUMENTS` is empty, ask the user for the path to the project folder.

1. Verify the project folder exists and contains a `.wiremock/` directory. If it does not, stop and inform the user.
2. Read `.wiremock/wiremock.yaml` to identify the service name and `cloud_id`.
3. Locate the Arazzo file at `.wiremock/<service-name>/arazzo.yaml`. If it does not exist, stop and inform the user.
4. Locate the OpenAPI file at `.wiremock/<service-name>/openapi.yaml`.

## Step 2: Gather Additional Inputs

Use `AskUserQuestion` to collect any additional configuration:

1. **Documentation sources**: Paths or URLs to any API documentation, OpenAPI/Swagger specs, Postman collections, or other reference material. If none are provided, search for them using `WebSearch` and `WebFetch`.

## Step 3: Access the Cloud Mock API

1. Attempt to access the mock API in WireMock Cloud using the `cloud_id` from `wiremock.yaml` via `search_my_mock_apis`.
2. **If the mock API is accessible**, use it for the remainder of the review.
3. **If the mock API cannot be accessed** (e.g. it belongs to another user or has been deleted), create a temporary copy using the WireMock CLI's profiles feature:
   ```
   wiremock environments create -p verify
   ```
   This will create a new instance of the API in Cloud and a profile YAML file containing the new `cloud_id`. Use this new instance for the remainder of the verification process.
4. **Enable hard request validation** against the OpenAPI schema using `update_mock_api_settings` with `settingsType: "openapi"` and `validationMode: "hard"`. This ensures all responses are validated against the spec during review.
5. **Authentication:** if the mock API has authentication enabled, disable it before proceeding so the Arazzo run isn't blocked by auth failures.
   There is no MCP tool to disable authentication on a mock API. Either ask the user to disable it via the WireMock Cloud dashboard, or supply working credentials via the CLI's `-a` authenticator config flag (see [Running Arazzo Workflows](#running-arazzo-workflows)).

## Step 4: Retrieve Documentation and Specifications

Gather all available documentation for the API:

1. Read the OpenAPI spec from `.wiremock/<service-name>/openapi.yaml` and also fetch it from the mock API using `pull` (see [Transferring Files To and From a Mock API](../references/file-transfer.md) for how `pull` works).
2. Read any documentation files, OpenAPI docs, or Postman collections provided by the user or found via search.
3. Read the Arazzo workflow document from `.wiremock/<service-name>/arazzo.yaml`.

## Step 5: Verify Completeness and Correctness

Perform each of the following checks, tracking all issues found:

### 5.1: Documentation vs OpenAPI Coverage
Compare the API documentation against the OpenAPI spec:
- Verify that **all endpoints described in the documentation** have corresponding operations in the OpenAPI doc.
- Note any endpoints present in the documentation but missing from the OpenAPI spec.

### 5.2: OpenAPI vs Stub Coverage
Retrieve all stubs using `search_stub_mappings` and cross-reference against the OpenAPI spec:
- Verify that **every operation in the OpenAPI doc** has at least one stub associated with it.
- Note any operations that lack stub coverage.

### 5.3: Undocumented Fields in Stubs
Cross-reference every stub response body against the OpenAPI doc schemas:
- Verify that **no stubs contain fields that are not documented** in the OpenAPI spec schemas.
- Note any stubs returning undocumented fields.

### 5.4: OpenAPI vs Arazzo Coverage
Examine the Arazzo workflow document and cross-reference against the OpenAPI spec:
- Verify that **every endpoint in the OpenAPI doc** is executed in at least one Arazzo workflow step.
- Note any endpoints that are not exercised by the workflows.

### 5.5: Arazzo Workflow Execution
Run the Arazzo workflows against the mock API to verify they execute successfully:

1. Reset the request journal using `reset_request_journal`.
2. Run all Arazzo workflows (see [Running Arazzo Workflows](#running-arazzo-workflows)) against the mock API's base URL.
3. Check the request journal using `search_request_journal` for any response validation errors.
4. Note any workflow failures or validation errors.

## Step 6: Output Report

Produce a detailed report covering the results of all checks. The report should include:

### Summary
A brief overall assessment of the mock API's completeness and correctness.

### Documentation vs OpenAPI Coverage
- Endpoints found in documentation but missing from the OpenAPI spec
- Any discrepancies noted

### OpenAPI vs Stub Coverage
- Operations in the OpenAPI spec without corresponding stubs
- Any gaps identified

### Undocumented Fields
- Stubs containing fields not present in OpenAPI schemas
- Specific field names and the stubs they appear in

### OpenAPI vs Arazzo Coverage
- Endpoints in the OpenAPI spec not exercised by Arazzo workflows
- Any missing workflow steps

### Arazzo Workflow Execution Results
- Overall pass/fail status for each workflow
- Any validation errors returned during execution
- Details of any failing steps

### Recommendations
Actionable steps to address each issue found.

If all checks pass with no issues, confirm that the mock API simulation is complete and correct.
