---
name: speckit-rest-api-generator
description: Use this skill when the user asks to create a single REST API specification using Spec Kit / Speckit style. This includes Indonesian prompts such as "buatkan speckit REST API", "buatkan API speckit", "buatkan spesifikasi REST API", "buatkan dokumen API", or English prompts such as "generate REST API spec", "create REST API specification", and "make REST API feature spec". The output must be created under docs/speckit/<feature-name>/ and must describe only one requested API operation.
---

# Speckit REST API Generator

Use this skill when the user wants to create a Speckit specification for one REST API operation before implementation.

The output must be written under:

```text
docs/speckit/<feature-name>/
```

Use kebab-case for `<feature-name>`.

## Goal

Create concise specs for exactly one REST API operation so the implementation agent understands the URL, headers, payload, success response, error response, optional validation rules, and implementation tasks.

Do not turn one requested API into a full CRUD feature. Do not add List, Detail, Create, Update, Delete, pagination, search, filter, sort, or relationship endpoints unless the user explicitly includes that behavior in the single API contract.

## Workflow

Follow this order:

```text
clarify -> specify -> plan -> tasks
```

## 1. Clarify

The expected user input is limited to:

- URL or endpoint path, optionally prefixed with the HTTP method.
  * Example: `POST /api/job-vacancies/apply`
- Required request headers.
- Request payload, query parameters, or path parameters.
- Success response example or schema.
- Error response example or schema.
- Optional custom validation rules.
- Used tables on database.

Ask only when the API operation itself cannot be identified. Otherwise, generate the speckit from the available input and use `TBD` for missing details.

Derive the feature name from the HTTP method and URL when the user does not provide one. Example: `POST /api/job-vacancies/apply` becomes `post-job-vacancies-apply`.

If the HTTP method is not included, set the method to `TBD`; do not infer the method from the payload.

## 2. Output Files

Create these files:

```text
docs/speckit/<feature-name>/
  spec.md
  plan.md
  tasks.md
```

## 3. spec.md

Focus on what the single REST API operation should do and why.

Must include:

* Feature name
* Purpose
* Target consumer
* Scope
* Out of scope
* Single API operation
* Method
* URL
* Request headers
* Request path parameters
* Request query parameters
* Request payload
* Response fields
* Success response format
* Error response format
* Custom validation expectations
* Status codes
* Success criteria

For the single API operation, include:

* Method
* Path
* Purpose
* Headers
* Query parameters
* Path parameters
* Request payload
* Success response
* Error response
* Custom validation
* Status codes

Keep `spec.md` scoped to this one operation. Use `TBD` for missing details instead of inventing extra API behavior.

## 4. plan.md

Focus on how the single REST API operation will be built.

Must include:

* Tech stack
* Architecture pattern
* Single endpoint design
* Header handling
* Payload or parameter mapping
* Success response mapping
* Error response mapping
* Custom validation approach
* Error handling approach
* Authentication approach, only if identifiable from headers or user input
* Authorization/policy approach, only if provided by the user

Do not include implementation plans for endpoints that were not requested.

## 5. tasks.md

Break the plan into ordered implementation tasks.

Use checkbox format.

Example:

```md
# Tasks

- [ ] Define one API operation only
- [ ] Define method and URL
- [ ] Define request headers
- [ ] Define request payload, query parameters, and path parameters
- [ ] Define success response format
- [ ] Define error response format
- [ ] Define custom validation rules, if provided
- [ ] Map request data into the handler or service
- [ ] Map success response from the handler or service
- [ ] Map error responses and status codes
- [ ] Implement validation, only for provided validation rules
- [ ] Add tests for this single API operation
- [ ] Review speckit completeness against the provided input
```
