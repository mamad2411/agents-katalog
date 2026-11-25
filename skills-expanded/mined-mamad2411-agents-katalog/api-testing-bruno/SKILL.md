---
name: api-testing-bruno
description: How to run end-to-end API tests using Bruno CLI against a locally running backend service.
---

# Bruno API Testing Skill

## Overview

Bruno is a fast, Git-friendly API client. This skill uses the **Bruno CLI (`bru`)** to
execute API test collections against the running backend service as a post-implementation
smoke / E2E validation step.

Bruno collections live in the repository under a configurable directory (default: `api-tests/`).
Each collection folder contains `.bru` request files with optional assertions and tests.

---

## Prerequisites

- Bruno CLI installed: `npm install -g @usebruno/cli` (or available in project devDependencies)
- The backend application is running locally (default: `http://localhost:8080`)
- Bruno collection directory exists in the repository

---

## Directory Convention

```
<project-root>/
  api-tests/                    ← Bruno collection root
    bruno.json                  ← Collection metadata
    environments/
      local.bru                 ← Local environment (base URL, variables)
    locations/                  ← Folder per domain / module
      create-location.bru
      list-locations.bru
      get-location-by-code.bru
      update-location.bru
    orders/
      create-order.bru
      ...
```

If no Bruno collection directory exists yet, create one following this structure.

---

## Environment File

The `local.bru` environment file should define at minimum:

```
vars {
  baseUrl: http://localhost:8080
}
```

Additional variables (auth tokens, test IDs) can be added as needed.

---

## Writing Bruno Requests

Each `.bru` file contains a single API request with optional test assertions.

### Example: Create Location

```
meta {
  name: Create Location
  type: http
  seq: 1
}

post {
  url: {{baseUrl}}/api/v1/locations
  body: json
  auth: none
}

body:json {
  {
    "code": "WH-TEST-001",
    "name": "Test Warehouse",
    "type": "WAREHOUSE",
    "address": {
      "street": "123 Test St",
      "city": "TestCity",
      "state": "TS",
      "zipCode": "12345",
      "country": "US"
    }
  }
}

assert {
  res.status: eq 201
  res.body.code: eq WH-TEST-001
  res.body.name: eq Test Warehouse
}

tests {
  test("should return 201 Created", function() {
    expect(res.getStatus()).to.equal(201);
  });

  test("should return the created location", function() {
    const body = res.getBody();
    expect(body.code).to.equal("WH-TEST-001");
    expect(body.type).to.equal("WAREHOUSE");
  });
}
```

### Example: Validation Error

```
meta {
  name: Create Location - Missing Code
  type: http
  seq: 2
}

post {
  url: {{baseUrl}}/api/v1/locations
  body: json
  auth: none
}

body:json {
  {
    "name": "No Code Location",
    "type": "WAREHOUSE"
  }
}

assert {
  res.status: eq 400
}

tests {
  test("should return 400 for missing code", function() {
    expect(res.getStatus()).to.equal(400);
  });
}
```

---

## Running Tests

### Run all tests in the collection
```bash
bru run api-tests/ --env local
```

### Run a specific folder (module)
```bash
bru run api-tests/locations/ --env local
```

### Run a single request file
```bash
bru run api-tests/locations/create-location.bru --env local
```

### Output format
Bruno CLI outputs test results to stdout. Failures are reported with request name
and assertion details. Non-zero exit code indicates test failures.

---

## Workflow Integration (Phase 7D)

When this skill is invoked from the developer agent:

### Step 1 — Start the application
Start the Spring Boot application in the background:
```bash
./gradlew bootRun --no-daemon &
```
Wait for the application to be ready (poll the health endpoint):
```bash
until curl -sf http://localhost:8080/actuator/health > /dev/null 2>&1; do sleep 2; done
```

### Step 2 — Identify or create Bruno tests

For the endpoints you **created or modified**, determine:
- Do Bruno request files already exist? → use them
- No request files? → create `.bru` files covering:
  - **Happy path** — valid request → expected success response
  - **Validation error** — invalid request → 400 with error details
  - **Not found** (if applicable) — non-existent resource → 404
  - **Duplicate / conflict** (if applicable) → 409

### Step 3 — Run the tests
```bash
bru run api-tests/<module>/ --env local
```

### Step 4 — Interpret results
- **All pass**: proceed to next phase
- **Failures**: read the failure output, determine if it's a production bug or a test bug, fix, re-run
- **Max 3 attempts** — if still failing, STOP and report

### Step 5 — Stop the application
```bash
kill %1  # or kill the backgrounded bootRun process
```

---

## Test Authoring Rules

- One `.bru` file per scenario (not per endpoint)
- Use descriptive `meta.name` values
- Always include `assert` blocks for status codes at minimum
- Use `tests` blocks for complex assertions (response body structure, field values)
- Use environment variables (`{{baseUrl}}`) — never hardcode URLs
- Keep test data deterministic — use unique codes/names to avoid collisions
- Clean up test data if the API supports DELETE, or rely on test database reset

---

## When NOT to Use Bruno

- **Unit tests** — use JUnit + Mockito instead
- **Integration tests with DB assertions** — use Testcontainers + WebTestClient instead
- **Load testing** — Bruno is not a load testing tool

Bruno E2E tests complement (not replace) unit and integration tests.
They validate the **deployed API contract** end-to-end through the real HTTP stack.
