---
name: microcks-api-v17
description: "Microcks API v1.7 API skill. Use when working with Microcks API v1.7 for services, tests, jobs. Covers 44 endpoints."
version: 1.0.0
generator: lapsh
---

# Microcks API v1.7
API version: 1.7.1

## Auth
OAuth2

## Base URL
http://microcks.example.com/api

## Setup
1. Configure auth: OAuth2
2. GET /services -- verify access
3. POST /tests -- create first tests

## Endpoints

44 endpoints across 11 groups. See references/api-spec.lap for full details.

### services
| Method | Path | Description |
|--------|------|-------------|
| GET | /services | Get Services and APIs |
| GET | /services/count | Get the Services counter |
| GET | /services/{id} | Get Service |
| DELETE | /services/{id} | Delete Service |
| PUT | /services/{id}/operation | Override Service Operation |
| PUT | /services/{id}/metadata | Update Service Metadata |
| GET | /services/labels | Get the already used labels for Services |
| GET | /services/search | Search for Services and APIs |

### tests
| Method | Path | Description |
|--------|------|-------------|
| POST | /tests | Create a new Test |
| GET | /tests/service/{serviceId} | Get TestResults by Service |
| GET | /tests/service/{serviceId}/count | Get the TestResults for Service counter |
| GET | /tests/{id} | Get TestResult |
| GET | /tests/{id}/messages/{testCaseId} | Get messages for TestCase |
| POST | /tests/{id}/testCaseResult | Report and create a new TestCaseResult |
| GET | /tests/{id}/events/{testCaseId} | Get events for TestCase |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /jobs | Get ImportJobs |
| POST | /jobs | Create ImportJob |
| GET | /jobs/{id} | Get ImportJob |
| POST | /jobs/{id} | Update ImportJob |
| DELETE | /jobs/{id} | Delete ImportJob |
| PUT | /jobs/{id}/activate | Activate an ImportJob |
| PUT | /jobs/{id}/start | Start an ImportJob |
| PUT | /jobs/{id}/stop | Stop an ImportJob |
| GET | /jobs/count | Get the ImportJobs counter |

### artifact
| Method | Path | Description |
|--------|------|-------------|
| POST | /artifact/upload | Upload an artifact |

### secrets
| Method | Path | Description |
|--------|------|-------------|
| GET | /secrets | Get Secrets |
| POST | /secrets | Create a new Secret |
| GET | /secrets/{id} | Get Secret |
| PUT | /secrets/{id} | Update Secret |
| DELETE | /secrets/{id} | Delete Secret |
| GET | /secrets/count | Get the Secrets counter |

### keycloak
| Method | Path | Description |
|--------|------|-------------|
| GET | /keycloak/config | Get authentification configuration |

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/{name} | Get Resource |
| GET | /resources/service/{serviceId} | Get Resources by Service |

### features
| Method | Path | Description |
|--------|------|-------------|
| GET | /features/config | Get features configuration |

### import
| Method | Path | Description |
|--------|------|-------------|
| POST | /import | Import a snapshot |

### export
| Method | Path | Description |
|--------|------|-------------|
| GET | /export | Export a snapshot |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics/invocations/global | Get aggregated invocation statistics for a day |
| GET | /metrics/conformance/aggregate | Get aggregation of conformance metrics |
| GET | /metrics/conformance/service/{serviceId} | Get conformance metrics for a Service |
| GET | /metrics/invocations/top | Get top invocation statistics for a day |
| GET | /metrics/invocations/{serviceName}/{serviceVersion} | Get invocation statistics for Service |
| GET | /metrics/invocations/global/latest | Get aggregated invocations statistics for latest days |
| GET | /metrics/tests/latest | Get latest tests results |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all services?" -> GET /services
- "Create a test?" -> POST /tests
- "List all count?" -> GET /services/count
- "List all jobs?" -> GET /jobs
- "Create a job?" -> POST /jobs
- "Get job details?" -> GET /jobs/{id}
- "Delete a job?" -> DELETE /jobs/{id}
- "Get service details?" -> GET /services/{id}
- "Delete a service?" -> DELETE /services/{id}
- "Create a upload?" -> POST /artifact/upload
- "List all count?" -> GET /jobs/count
- "List all secrets?" -> GET /secrets
- "Create a secret?" -> POST /secrets
- "Get secret details?" -> GET /secrets/{id}
- "Update a secret?" -> PUT /secrets/{id}
- "Delete a secret?" -> DELETE /secrets/{id}
- "List all count?" -> GET /secrets/count
- "Get service details?" -> GET /tests/service/{serviceId}
- "List all count?" -> GET /tests/service/{serviceId}/count
- "Get test details?" -> GET /tests/{id}
- "Get message details?" -> GET /tests/{id}/messages/{testCaseId}
- "Create a testCaseResult?" -> POST /tests/{id}/testCaseResult
- "List all config?" -> GET /keycloak/config
- "List all labels?" -> GET /services/labels
- "List all search?" -> GET /services/search
- "Get event details?" -> GET /tests/{id}/events/{testCaseId}
- "Get resource details?" -> GET /resources/{name}
- "Get service details?" -> GET /resources/service/{serviceId}
- "List all config?" -> GET /features/config
- "Create a import?" -> POST /import
- "List all export?" -> GET /export
- "List all global?" -> GET /metrics/invocations/global
- "List all aggregate?" -> GET /metrics/conformance/aggregate
- "Get service details?" -> GET /metrics/conformance/service/{serviceId}
- "List all top?" -> GET /metrics/invocations/top
- "Get invocation details?" -> GET /metrics/invocations/{serviceName}/{serviceVersion}
- "List all latest?" -> GET /metrics/invocations/global/latest
- "List all latest?" -> GET /metrics/tests/latest
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
