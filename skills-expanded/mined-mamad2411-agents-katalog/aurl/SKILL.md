---
name: aurl
description: Turn any API into a CLI command. Register OpenAPI or GraphQL endpoints by name, then explore and invoke them. Built for AI agents to use APIs like tool calls.
---

# aurl

Turn any API spec into a CLI command. Register APIs by name, explore their endpoints, and make requests.

## Commands

```bash
aurl add [name] [openapi.json URL or path]       # register an API
aurl add [name] [spec] --base-url [URL]           # override base URL
aurl add [name] [spec] --header "Key: Value"      # manual auth header
aurl add --graphql [name] [endpoint]              # register a GraphQL API
aurl list                                          # list registered APIs
aurl remove [name]                                 # unregister
aurl auth [name]                                   # reconfigure auth
```

## Using a Registered API

```bash
aurl [name] --help                                # see all endpoints, params, enums, response codes
aurl [name] describe METHOD /path                 # detailed docs for one endpoint
aurl [name] describe [field]                      # detailed docs for a GraphQL field/type
aurl [name] docs                                  # open external docs in browser
aurl [name] METHOD /path                          # make a REST request
aurl [name] METHOD /path '{"key":"value"}'        # make a REST request with JSON body
aurl [name] '{ graphql query }'                   # run a GraphQL query
aurl [name] '{ query }' '{"var":"val"}'           # GraphQL with variables
```

## Discovery Workflow

When working with an unfamiliar registered API:

1. `aurl [name] --help` — scan all endpoints grouped by tag
2. `aurl [name] describe METHOD /path` — read full docs for an endpoint before calling it
3. Make the request — enum params are validated before sending, missing required body fields trigger a warning

## Notes

- Auth is auto-detected from the spec's `securitySchemes` during `aurl add`
- Query params go inline in the path: `aurl [name] GET '/path?key=value'`
- Quote paths with `?` to prevent shell globbing
- On 4xx errors, the CLI suggests the expected request body from the spec
