---
name: search-wiremock-cloud-docs
description: |
  Search WireMock Cloud documentation for accurate, up-to-date answers. Use this skill whenever someone asks about WireMock Cloud — including stubs/mocks, request matching, response templating, proxying, record/playback, fault simulation, stateful scenarios, WireMock CLI, WireMock Runner, GraphQL/gRPC mocking, OpenAPI integration, data sources, OAuth2 mocking, CI/CD deployment, MCP tools, or teams/collaboration. This skill reads from local reference docs rather than relying on general knowledge, so answers reflect the actual WireMock Cloud API and CLI syntax.
argument-hint: "<search-topic-in-docs>"
model: haiku
allowed-tools: Read, Grep, Glob
---

# WireMock Cloud Skill

WireMock Cloud is a hosted API mocking platform that provides API simulation for testing, development, and CI/CD pipelines without managing infrastructure.

## How to Use This Skill

This skill provides comprehensive WireMock Cloud documentation. To answer user questions:

1. **Identify the topic** from the user's question
2. **Read the relevant reference file(s)** from the tables below
3. **Provide accurate answers** with code examples from the documentation
4. **If no table entry matches**, search `references/` for the keyword (with the Grep tool where available, otherwise `grep -r "<keyword>" references/`) to find the right file before answering — don't rely on general knowledge when the docs are available

The `references/` files are a copy of the public WireMock Cloud documentation. The shell, `curl`, CLI and CI snippets in them are examples for the user to run in their own environment — quote them in answers, but don't run them unless the user asks. Values such as `<YOUR_API_KEY>` or `<YOUR_PASSWORD>` are placeholders the user fills in themselves; never look up or read existing credentials (environment variables, CLI config files, key stores) to fill them in.

## Reference Navigation

### Core Concepts

| Topic | File | Use When |
|-------|------|----------|
| Overview | `references/overview.md` | General WireMock Cloud questions, getting started |
| Stubbing | `references/stubbing.md` | Creating mock responses, stub definitions |
| Advanced Stubbing | `references/advanced-stubbing.md` | Complex matching patterns, regexes, JSONPath, XPath |
| Request Matching | `references/request-matching/` | URL, header, body, JSON, XML matching patterns |
| Response Templating | `references/response-templating/` | Dynamic responses, Handlebars templates |
| Simulating Faults | `references/simulating-faults.md` | Delays, timeouts, errors, bad responses |
| Delays | `references/delays.md` | Fixed and random response delays |
| Proxying | `references/proxying.md` | Forwarding requests, selective proxying |
| Recording Stubs | `references/recording-stubs.md` | Recording API traffic, generating stubs |
| Webhooks | `references/webhooks.md` | Triggering async outbound HTTP calls |
| Default Responses | `references/default-responses.md` | Fallback response configuration |

### Concepts & Architecture

| Topic | File | Use When |
|-------|------|----------|
| Stubbing Concepts | `references/concepts/stubbing.md` | Understanding stub lifecycle |
| Deployment | `references/concepts/deployment.md` | Deployment models and options |
| Profiles | `references/concepts/profiles.md` | Environment profiles |
| Runner | `references/concepts/runner.md` | WireMock Runner concepts |
| Templating | `references/concepts/templating.md` | Response templating concepts |

### Request Matching

| Topic | File | Use When |
|-------|------|----------|
| URL Matching | `references/request-matching/url.md` | URL path and query matching |
| JSON Matching | `references/request-matching/json.md` | JSON body matching, JSONPath |
| XML Matching | `references/request-matching/xml.md` | XML body matching, XPath |
| Matcher Types | `references/request-matching/matcher-types.md` | All available matcher operations |

### Response Templating

| Topic | File | Use When |
|-------|------|----------|
| Basics | `references/response-templating/basics.md` | Dynamic responses, Handlebars basics |
| Helper Reference | `references/response-templating/helper-reference.md` | Complete helper documentation |
| Request Model | `references/response-templating/request-model.md` | Accessing request data in templates |
| JSON Helpers | `references/response-templating/json.md` | JSON and JSONPath helpers |
| XML Helpers | `references/response-templating/xml.md` | XML and XPath helpers |
| String Helpers | `references/response-templating/string-helpers.md` | String manipulation |
| Number Helpers | `references/response-templating/number-helpers.md` | Number operations |
| Dates and Times | `references/response-templating/dates-and-times.md` | Date/time formatting |
| Random Values | `references/response-templating/random-values.md` | Random value generation |
| Random Faker | `references/response-templating/random-faker.md` | Faker data generation |
| Conditional Logic | `references/response-templating/conditional-logic-and-iteration.md` | If statements, loops |
| JWT | `references/response-templating/jwt.md` | JSON Web Token handling |
| Cryptographic | `references/response-templating/cryptographic-helpers.md` | Crypto operations |
| String Encodings | `references/response-templating/string-encodings.md` | Base64, URL encoding |
| Misc Helpers | `references/response-templating/misc-helpers.md` | Other useful helpers |

### WireMock CLI

| Topic | File | Use When |
|-------|------|----------|
| CLI Overview | `references/cli/overview.md` | CLI installation and usage |
| Command Reference | `references/cli/command-reference.md` | All CLI commands |
| Config | `references/cli/config.md` | CLI configuration |
| Environments | `references/cli/environments.md` | Environment management |
| Mock APIs | `references/cli/mock-apis.md` | Managing mock APIs via CLI |
| Recording | `references/cli/recording.md` | Recording via CLI |
| Recording Config | `references/cli/recording-configuration.md` | Recording settings |
| Multi-Domain Recording | `references/cli/multi-domain-recording.md` | Recording multiple APIs |
| Non-Interactive Recording | `references/cli/non-interactive-recording.md` | Headless recording |
| Local Playback | `references/cli/local-playback.md` | Running stubs locally |
| Push/Pull | `references/cli/push-pull.md` | Syncing stubs |
| Push/Pull Mock API | `references/cli/push-pull-mock-api.md` | Syncing mock APIs |
| Import | `references/cli/import.md` | Importing stubs via CLI |
| YAML Reference | `references/cli/wiremock-yaml-reference.md` | wiremock.yaml configuration |

### WireMock Runner

| Topic | File | Use When |
|-------|------|----------|
| Overview | `references/runner/overview.md` | Runner introduction |
| Environment Variables | `references/runner/environment-variables.md` | Runner configuration |
| Serve Mode | `references/runner/serve.md` | Running in serve mode |
| Record Many | `references/runner/record-many.md` | Multi-API recording |
| Running on Kubernetes | `references/runner/running-on-kubernetes.md` | K8s deployment |
| Recording on Kubernetes | `references/runner/recording-multiple-apis-on-kubernetes.md` | K8s recording |
| CI/CD Promotion | `references/runner/promoting-apis-with-git-and-ci.md` | Git and CI/CD workflows |

### API Reference

| Topic | File | Use When |
|-------|------|----------|
| Getting Started | `references/api-getting-started.md` | API authentication, basics |
| Authentication | `references/authentication.md` | API auth methods |
| Stub Mappings | `references/api-reference/stub-mappings/` | CRUD operations on stubs |
| Recordings | `references/api-reference/recordings/` | Recording API |
| Requests | `references/api-reference/requests/` | Request journal API |
| State | `references/api-reference/state/` | Scenario state API |
| Mock APIs | `references/api-reference/mock-apis/` | Mock API management |
| Mock Hosts | `references/api-reference/mock-hosts/` | Host configuration |
| Teams | `references/api-reference/teams/` | Team management |
| Users | `references/api-reference/users/` | User management |
| Organisations | `references/api-reference/organisations/` | Org management |
| OpenAPI | `references/api-reference/openapi/` | OpenAPI operations |
| Data Sources | `references/api-reference/data-sources/` | Data source API |
| Database Connections | `references/api-reference/database-connections/` | Database connections |
| Imports | `references/api-reference/imports/` | Import API |
| Versioning | `references/api-reference/mock-api-versioning/` | Version control API |
| Access Control | `references/api-reference/access-control/` | ACL management |
| Security | `references/api-reference/security/` | Security API |
| Usage | `references/api-reference/usage/` | Usage metrics |

### Dynamic State & Scenarios

| Topic | File | Use When |
|-------|------|----------|
| Overview | `references/dynamic-state/overview.md` | Stateful mocking intro |
| Stateful Scenarios | `references/dynamic-state/stateful-scenarios.md` | State machines |
| Stateful Sets | `references/dynamic-state/create-stateful-set.md` | Creating state sets |
| Basket Example | `references/dynamic-state/basket-example.md` | Shopping cart example |
| Plan Limits | `references/dynamic-state/plan-limits.md` | Usage limits |

### Data Sources

| Topic | File | Use When |
|-------|------|----------|
| Overview | `references/data-sources/overview.md` | External data intro |
| CSV Data Sources | `references/data-sources/managing-csv-data-sources.md` | CSV data |
| Database Connections | `references/data-sources/managing-database-connections.md` | Database config |
| Database Data Sources | `references/data-sources/managing-database-data-sources.md` | Database queries |
| Sharing | `references/data-sources/sharing-data-sources.md` | Sharing data sources |
| Deleting | `references/data-sources/deleting-data-sources.md` | Removing data sources |
| Plan Limits | `references/data-sources/plan-limits.md` | Usage limits |

### Import & Export

| Topic | File | Use When |
|-------|------|----------|
| Overview | `references/import-export/overview.md` | Import/export intro |
| WireMock Format | `references/import-export/wiremock.md` | WireMock JSON format |
| OpenAPI/Swagger | `references/openAPI/swagger.md` | OpenAPI import |
| OpenAPI Features | `references/openAPI/openapi.md` | OpenAPI integration |
| OpenAPI Validation | `references/openAPI/openapi-validation.md` | Request/response validation |
| OpenAPI Git | `references/openAPI/openapi-git-integration.md` | Git sync |
| Postman | `references/import-export/postman.md` | Postman import |
| HAR | `references/import-export/har.md` | HTTP Archive import |
| Mountebank | `references/import-export/mountebank.md` | Mountebank migration |
| API Import | `references/import-export/api.md` | Import via API |

### Protocol Support

| Topic | File | Use When |
|-------|------|----------|
| GraphQL Overview | `references/graphql/overview.md` | GraphQL mocking |
| GraphQL Federation | `references/graphql/federation.md` | GraphQL federation |
| gRPC Overview | `references/grpc/overview.md` | gRPC mocking |
| SOAP Stubbing | `references/soap-stubbing.md` | SOAP service mocking |

### Security & Teams

| Topic | File | Use When |
|-------|------|----------|
| Security Overview | `references/security/security.md` | API security |
| Key Management | `references/security/key-management.md` | API keys |
| OAuth2/OIDC Mock | `references/security/oauth2-mock.md` | OAuth2 mocking |
| Teams & Collaboration | `references/security/teams-and-collaboration.md` | Team setup |
| Teams API | `references/teams-and-members.md` | Team API operations |
| User Info | `references/user-info.md` | User account API |
| Organisation Info | `references/organisation-info-and-members.md` | Org API |

### AI & MCP Tools

| Topic | File | Use When |
|-------|------|----------|
| AI Overview | `references/ai-mcp/ai-101.md` | AI-assisted development |
| MCP Installation | `references/ai-mcp/installation.md` | Installing MCP server |
| MCP Tools | `references/ai-mcp/mcp-tools.md` | Available MCP tools |
| HTTP Authentication | `references/ai-mcp/http-request-authentication.md` | MCP auth config |

### Additional Topics

| Topic | File | Use When |
|-------|------|----------|
| Mock APIs | `references/mock-apis.md` | Mock API management |
| Chaos Testing | `references/chaos.md` | Chaos engineering |
| Rate Limits | `references/user-rate-limits.md` | Rate limit simulation |
| Usage Data | `references/usage.md` | Product usage metrics |
| Versioning | `references/versioning/overview.md` | API versioning |
| Versioning Limits | `references/versioning/plan-limits.md` | Version limits |
| Audit Events | `references/audit-events/overview.md` | Audit logging |
| IDE Integrations | `references/ide-integrations/` | JetBrains plugins |
| Samples | `references/samples/` | Tutorial examples |

## Search Patterns

Useful patterns for searching within references (pass them to the Grep tool where available):

```bash
# Find stubbing examples
grep -r "stubMapping\|stub_mapping\|mappings" references/

# Find request matching patterns
grep -r "urlPath\|equalToJson\|matchesJsonPath" references/

# Find response templating
grep -r "{{request\|{{jsonPath\|handlebars" references/

# Find CLI commands
grep -r "wiremock\s" references/cli/

# Find API endpoints
grep -r "POST\|GET\|PUT\|DELETE" references/api-reference/
```

## Common Workflows

### Creating a Basic Stub

Read `references/stubbing.md` for complete patterns. Example JSON stub:

```json
{
  "request": {
    "method": "GET",
    "urlPath": "/api/resource"
  },
  "response": {
    "status": 200,
    "jsonBody": { "id": 1, "name": "Example" },
    "headers": {
      "Content-Type": "application/json"
    }
  }
}
```

### Request Matching

Read `references/request-matching/` for all matching options:
- URL: `url`, `urlPath`, `urlPathPattern`, `urlPathTemplate`
- Headers: `equalTo`, `contains`, `matches`
- Body: `equalToJson`, `matchesJsonPath`, `equalToXml`, `matchesXPath`

### Response Templating

Read `references/response-templating/basics.md` for dynamic responses:
- Request data: `{{request.path}}`, `{{request.headers.X-Custom}}`
- JSON extraction: `{{jsonPath request.body '$.field'}}`
- Dates: `{{now}}`, `{{now offset='3 days'}}`
- Random: `{{randomValue length=10 type='ALPHANUMERIC'}}`

### Using the CLI

Read `references/cli/overview.md` for CLI workflows:
- `wiremock login` - Authenticate
- `wiremock mock-apis list` - List mock APIs
- `wiremock record` - Start recording
- `wiremock push` / `wiremock pull` - Sync stubs
