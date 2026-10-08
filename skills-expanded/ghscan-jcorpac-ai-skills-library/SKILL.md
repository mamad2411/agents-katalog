---
name: mcp-testing-frameworks
description: Automated testing strategies for verifying MCP server logic and tool integration.
---

# MCP Testing Frameworks

Testing MCP servers requires verifying both the logic and the protocol adherence.

## Testing Layers
1.  **Unit Tests**: Testing the underlying Python functions independently of MCP.
2.  **Integration Tests**: Mocking the MCP Client to verify that tools respond correctly over the protocol.
3.  **E2E Tests**: Running the server in a real environment (e.g., Claude Desktop) and verifying behavior.

## Tools
- **`pytest`**: The standard for Python testing.
- **MCP Python SDK Test Utilities**: Helper classes for simulating client interactions.

## Best Practices
- **Schema Validation**: Verify that the generated JSON Schema matches expectations.
- **Edge Cases**: Test tools with empty, invalid, and large inputs.

