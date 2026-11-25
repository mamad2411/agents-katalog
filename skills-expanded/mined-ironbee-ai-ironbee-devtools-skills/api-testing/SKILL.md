---
name: api-testing
description: Test browser-side API integrations by mocking responses, intercepting requests, and monitoring network traffic from the page. Use when the user wants to mock backend APIs at the browser level, simulate errors, test offline behavior, intercept requests, or add authentication headers from the page. For server-side API testing (drive real HTTP/gRPC/GraphQL/WS endpoints, log correlation, db verification), use the `backend-testing` skill instead.
allowed-tools: Bash(ironbee-browser-devtools-cli:*), Bash(ironbee-node-devtools-cli:*)
---

# API Testing Skill

Test browser-side API integrations by mocking responses, intercepting requests, and monitoring network traffic from the page perspective.

> **Server-side API testing** — driving real backend endpoints over HTTP/1.1+HTTP/2, gRPC, GraphQL, or WebSocket, correlating with server logs (file/Docker/Kubernetes), and asserting on database state — belongs in the [`backend-testing`](../backend-testing/SKILL.md) skill.

## When to Use

This skill activates when:
- User wants to test API integrations
- User needs to mock backend responses
- User wants to simulate error scenarios
- User asks about request interception
- User needs to test offline behavior

## Capabilities

### Response Mocking
```bash
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/users" \
  --response '{"action":"fulfill","status":200,"body":[{"id":1,"name":"Test"}]}'
```

### Request Interception
```bash
ironbee-browser-devtools-cli stub intercept-http-request \
  --pattern "**/api/**" \
  --modifications '{"headers":{"Authorization":"Bearer token"}}'
```

### Network Monitoring
```bash
ironbee-browser-devtools-cli --json o11y get-http-requests
ironbee-browser-devtools-cli --json o11y get-http-requests --resource-type fetch
ironbee-browser-devtools-cli --json o11y get-http-requests --status '{"min":400}'
```

### Stub Management
```bash
ironbee-browser-devtools-cli stub list
ironbee-browser-devtools-cli stub clear --stub-id <id>
ironbee-browser-devtools-cli stub clear
```

## Common Scenarios

### Mock Successful Response
```bash
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/users" \
  --response '{"action":"fulfill","status":200,"body":[{"id":1,"name":"Test"}]}'
```

### Simulate Server Error
```bash
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/checkout" \
  --response '{"action":"fulfill","status":500,"body":{"error":"Internal Server Error"}}'
```

### Simulate 404 Not Found
```bash
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/missing" \
  --response '{"action":"fulfill","status":404,"body":{"error":"Not Found"}}'
```

### Simulate Network Timeout
```bash
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/slow-endpoint" \
  --response '{"action":"abort","abortErrorCode":"timedout"}'
```

### Simulate Connection Failed
```bash
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/offline" \
  --response '{"action":"abort","abortErrorCode":"connectionfailed"}'
```

### Add Auth Header
```bash
ironbee-browser-devtools-cli stub intercept-http-request \
  --pattern "**/api/**" \
  --modifications '{"headers":{"Authorization":"Bearer test-token"}}'
```

### Modify Request Body
```bash
ironbee-browser-devtools-cli stub intercept-http-request \
  --pattern "**/api/submit" \
  --modifications '{"body":{"injected":"value"}}'
```

### Add Delay
```bash
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/slow" \
  --response '{"action":"fulfill","status":200,"body":{}}' \
  --delay-ms 3000
```

### Simulate Flaky API
```bash
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/unreliable" \
  --response '{"action":"fulfill","status":503}' \
  --chance 0.3
```

### One-Shot Mock
```bash
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/once" \
  --response '{"action":"fulfill","status":200,"body":{"first":true}}' \
  --times 1
```

## Testing Workflow

```bash
SESSION="--session-id api-test"

# 1. Setup mocks before navigation
ironbee-browser-devtools-cli $SESSION stub mock-http-response \
  --pattern "**/api/users" \
  --response '{"action":"fulfill","status":200,"body":[{"id":1,"name":"Mock User"}]}'

# 2. Navigate to application
ironbee-browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com"
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle

# 3. Interact with the app
ironbee-browser-devtools-cli $SESSION interaction click --selector "#load-users"
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle

# 4. Check network requests
ironbee-browser-devtools-cli $SESSION --json o11y get-http-requests

# 5. Verify UI shows mocked data
ironbee-browser-devtools-cli $SESSION content get-as-text --selector ".user-list"

# 6. List active stubs
ironbee-browser-devtools-cli $SESSION stub list

# 7. Clear all stubs
ironbee-browser-devtools-cli $SESSION stub clear

# 8. Cleanup
ironbee-browser-devtools-cli session delete api-test
```

## Error Testing Workflow

```bash
SESSION="--session-id error-test"

# Mock error response
ironbee-browser-devtools-cli $SESSION stub mock-http-response \
  --pattern "**/api/checkout" \
  --response '{"action":"fulfill","status":500,"body":{"error":"Payment failed"}}'

# Navigate and trigger error
ironbee-browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com/checkout"
ironbee-browser-devtools-cli $SESSION interaction click --selector "#pay-button"
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle

# Check error handling in UI
ironbee-browser-devtools-cli $SESSION content take-screenshot --name "error-state"
ironbee-browser-devtools-cli $SESSION content get-as-text --selector ".error-message"

# Cleanup
ironbee-browser-devtools-cli $SESSION stub clear
ironbee-browser-devtools-cli session delete error-test
```

## Debugging Backend During API Tests

When testing against a real backend and need to debug why an endpoint fails or returns unexpected data, use `ironbee-node-devtools-cli`:

```bash
# Connect to API server process
ironbee-node-devtools-cli --session-id api-debug debug connect --process-name "api"

# Set tracepoint on the handler
ironbee-node-devtools-cli --session-id api-debug debug put-tracepoint \
  --url-pattern "routes/users.ts" \
  --line-number 42

# Trigger the API from browser (or curl), then get snapshots
ironbee-node-devtools-cli --session-id api-debug --json debug get-probe-snapshots

# Or inspect backend console logs
ironbee-node-devtools-cli --session-id api-debug --json debug get-logs --search "error"
```

## Best Practices

1. **Use specific patterns** to avoid mocking unintended requests
2. **Clear stubs after tests** to prevent interference
3. **List stubs** to debug unexpected behavior
4. **Use times limit** for one-shot mocks
5. **Add delays** to test loading states
6. **Test error scenarios** not just happy paths
7. **Set up mocks before navigation** for first-load testing
8. **Monitor actual requests** to verify mocks are working
