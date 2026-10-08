---
name: jira-api-test-cases
description: Create API test cases from a Jira user story and the project's Swagger or OpenAPI file. Use when the task is to read a Jira story, derive functional API test cases from its acceptance criteria, propose the list for approval, and then create the approved cases as Jira subtasks with a consistent template.
---

# Jira API Test Cases

Use this skill when the user wants to turn a Jira story into API test cases and track those cases as Jira subtasks.

## Workflow

Follow this sequence:

1. Read the Jira user story and capture its acceptance criteria.
2. Read the project's Swagger or OpenAPI definition and identify the endpoint operations that map to the story.
3. Define functional test case variations that cover the acceptance criteria.
4. Propose the test cases to the user and wait for approval before creating Jira issues.
5. After approval, create each test case as a subtask under the user story.

## Rules

- Each test case should represent a possible variation of the API use based on the acceptance criteria of the user story.
- Each test case should be represented by a Jira subtask under the user story, with the prefix `[Test Case]`.
- Each test case should include the sections `Title`, `Operation (Method and Endpoint)`, `Request Parameters / Headers` (if applicable), `Request Body` (if applicable), `Response Status Code`, and `Response Body` (if applicable).
- Each test case should check response codes against their usually expected results, not only against the current project specs or implementation. Example: if trying to register an email that is already registered, the common choice is `409 Conflict`, so the test case should expect `409` even if the current spec and/or code say `400`.

## Working Notes

- Prefer functional coverage over duplicating the same scenario with cosmetic variations.
- Call out when a proposed test case intentionally differs from the current Swagger or implementation so the user knows it reflects common API practice rather than the current project behavior.
- If the story maps to multiple endpoints, group the proposed test cases clearly by endpoint.
- If the Swagger documents a generic validation error for multiple missing-field cases, it is fine to split them into separate test cases when that improves coverage clarity.

## Jira Template

Use this structure for each proposed or created test case:

Title
<test case title>

Operation (Method and Endpoint)
`<METHOD /path>`

Request Parameters / Headers
```text
Path params: ...
Query params: ...
Headers: ...
```

Request Body
```json
{ ... }
```

Response Status Code
`<status code>`

Response Body
```json
{ ... }
```
