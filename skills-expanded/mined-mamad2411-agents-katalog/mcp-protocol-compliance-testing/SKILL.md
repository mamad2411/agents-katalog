---
name: mcp-protocol-compliance-testing
version: "1.0"
description: >
  Test JSON-RPC 2.0 protocol compliance and Pydantic schema validation for MCP servers.
  PROACTIVELY activate for: (1) writing MCP server tests, (2) protocol compliance validation, (3) async tool testing.
  Triggers: "mcp testing", "protocol compliance", "pytest asyncio"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# MCP Protocol Compliance Testing Skill

## Metadata (Tier 1)

**Keywords**: testing, protocol, json-rpc, validation, pytest, compliance

**File Patterns**: **/test_*.py, **/tests/*.py

**Modes**: testing_backend

---

## Instructions (Tier 2)

### JSON-RPC 2.0 Message Validation

```python
import pytest
from pydantic import ValidationError
from server.protocol import JsonRpcRequest, JsonRpcResponse

class TestJsonRpcCompliance:
    """Test JSON-RPC 2.0 protocol compliance."""

    def test_valid_request(self):
        """Valid JSON-RPC 2.0 request passes validation."""
        request = JsonRpcRequest(
            jsonrpc="2.0",
            method="tools/call",
            params={"name": "search", "arguments": {}},
            id=1
        )
        assert request.jsonrpc == "2.0"
        assert request.method == "tools/call"
        assert request.id == 1

    def test_invalid_jsonrpc_version(self):
        """Invalid jsonrpc version raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            JsonRpcRequest(
                jsonrpc="1.0",  # Invalid
                method="tools/call",
                id=1
            )
        assert "jsonrpc" in str(exc_info.value).lower()

    def test_missing_required_fields(self):
        """Missing required fields raise ValidationError."""
        with pytest.raises(ValidationError):
            JsonRpcRequest(
                jsonrpc="2.0"
                # Missing method
            )

    def test_valid_response(self):
        """Valid JSON-RPC 2.0 response structure."""
        response = JsonRpcResponse(
            jsonrpc="2.0",
            result={"data": "test"},
            id=1
        )
        assert response.result == {"data": "test"}
        assert response.error is None

    def test_error_response(self):
        """Error response has proper structure."""
        error = JsonRpcError(
            code=-32601,
            message="Method not found",
            data={"method": "unknown"}
        )
        response = JsonRpcResponse(
            jsonrpc="2.0",
            error=error,
            id=1
        )
        assert response.error.code == -32601
        assert response.result is None
```

### Tool Schema Validation

```python
from tools.schemas import SearchInput, SearchOutput

class TestToolSchemas:
    """Test Pydantic tool schema compliance."""

    def test_valid_input(self):
        """Valid input passes strict mode validation."""
        input_data = SearchInput(
            query="test",
            limit=10,
            filter_type="code"
        )
        assert input_data.query == "test"
        assert input_data.limit == 10

    def test_strict_mode_prevents_coercion(self):
        """Strict mode blocks type coercion."""
        with pytest.raises(ValidationError) as exc_info:
            SearchInput(
                query="test",
                limit="10"  # String instead of int
            )
        # Verify it's a type error, not coercion
        assert "int" in str(exc_info.value).lower()

    def test_field_constraints(self):
        """Field constraints are enforced (ge, le, etc.)."""
        # Below minimum
        with pytest.raises(ValidationError):
            SearchInput(query="test", limit=0)

        # Above maximum
        with pytest.raises(ValidationError):
            SearchInput(query="test", limit=101)

    def test_literal_enum_validation(self):
        """Literal types only accept specified values."""
        # Valid literal
        input1 = SearchInput(query="test", filter_type="code")
        assert input1.filter_type == "code"

        # Invalid literal
        with pytest.raises(ValidationError):
            SearchInput(query="test", filter_type="invalid")

    def test_schema_generation(self):
        """Pydantic generates valid JSON Schema."""
        schema = SearchInput.model_json_schema()

        assert schema["type"] == "object"
        assert "query" in schema["properties"]
        assert "limit" in schema["properties"]

        # Verify constraints in schema
        limit_schema = schema["properties"]["limit"]
        assert limit_schema["minimum"] == 1
        assert limit_schema["maximum"] == 100

    def test_output_serialization(self):
        """Output models serialize correctly."""
        output = SearchOutput(
            results=[{"file": "test.py", "line": 10}],
            total_count=1,
            execution_time_ms=42
        )

        dumped = output.model_dump()
        assert isinstance(dumped, dict)
        assert dumped["total_count"] == 1
```

### Async Tool Execution Tests

```python
import pytest
import asyncio

class TestAsyncToolExecution:
    """Test async tool execution patterns."""

    @pytest.mark.asyncio
    async def test_tool_executes_async(self, mcp_server):
        """Tools execute without blocking."""
        result = await mcp_server.call_tool(
            "search_code",
            {"query": "async def", "limit": 5}
        )
        assert result is not None
        assert "results" in result

    @pytest.mark.asyncio
    async def test_concurrent_execution(self, mcp_server):
        """Multiple tools execute concurrently."""
        start = asyncio.get_event_loop().time()

        # Execute concurrently using TaskGroup
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(
                mcp_server.call_tool("search", {"query": "test1"})
            )
            t2 = tg.create_task(
                mcp_server.call_tool("search", {"query": "test2"})
            )

        duration = asyncio.get_event_loop().time() - start

        # Concurrent execution should be faster than sequential
        assert duration < 2.0
        assert t1.result() is not None
        assert t2.result() is not None

    @pytest.mark.asyncio
    async def test_tool_timeout(self, mcp_server):
        """Tool execution respects timeout."""
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(
                mcp_server.call_tool("slow_tool", {}),
                timeout=1.0
            )

    @pytest.mark.asyncio
    async def test_tool_cancellation(self, mcp_server):
        """Tool execution can be cancelled."""
        task = asyncio.create_task(
            mcp_server.call_tool("long_running_tool", {})
        )

        # Cancel after short delay
        await asyncio.sleep(0.1)
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task
```

### Integration Tests

```python
class TestMcpIntegration:
    """Full request/response cycle tests."""

    @pytest.mark.asyncio
    async def test_list_tools(self, mcp_server):
        """list_tools returns valid tool descriptors."""
        tools = await mcp_server.list_tools()

        assert len(tools) > 0
        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool

            # Validate schema structure
            schema = tool["inputSchema"]
            assert schema["type"] == "object"
            assert "properties" in schema

    @pytest.mark.asyncio
    async def test_call_tool_success(self, mcp_server):
        """Successful tool call returns result."""
        result = await mcp_server.call_tool(
            "search_code",
            {"query": "test", "limit": 5}
        )

        assert "results" in result
        assert isinstance(result["results"], list)

    @pytest.mark.asyncio
    async def test_call_tool_invalid_name(self, mcp_server):
        """Invalid tool name returns error."""
        with pytest.raises(ValueError) as exc_info:
            await mcp_server.call_tool("nonexistent_tool", {})

        assert "unknown" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_call_tool_invalid_arguments(self, mcp_server):
        """Invalid arguments raise ValidationError."""
        with pytest.raises(ValidationError):
            await mcp_server.call_tool(
                "search_code",
                {"invalid_param": "value"}
            )

    @pytest.mark.asyncio
    async def test_list_resources(self, mcp_server):
        """list_resources returns valid descriptors."""
        resources = await mcp_server.list_resources()

        for resource in resources:
            assert "uri" in resource
            assert "name" in resource
            assert "mimeType" in resource
            # Validate URI scheme
            assert resource["uri"].startswith(
                ("file://", "db://", "api://", "log://")
            )

    @pytest.mark.asyncio
    async def test_read_resource(self, mcp_server):
        """read_resource returns content."""
        result = await mcp_server.read_resource(
            "file:///project/README.md"
        )

        assert "contents" in result
        assert len(result["contents"]) > 0
        content = result["contents"][0]
        assert "uri" in content
        assert "text" in content or "blob" in content
```

### Error Handling Tests

```python
class TestErrorHandling:
    """Test proper error responses."""

    @pytest.mark.asyncio
    async def test_validation_error_response(self, mcp_server):
        """Validation errors return -32602 (Invalid params)."""
        try:
            await mcp_server.call_tool(
                "search_code",
                {"limit": "invalid"}  # Type error
            )
        except McpError as e:
            assert e.code == -32602
            assert "validation" in e.message.lower()

    @pytest.mark.asyncio
    async def test_method_not_found_response(self, mcp_server):
        """Unknown methods return -32601 (Method not found)."""
        try:
            await mcp_server.call_tool("unknown_tool", {})
        except McpError as e:
            assert e.code == -32601
            assert "not found" in e.message.lower()

    @pytest.mark.asyncio
    async def test_internal_error_response(self, mcp_server):
        """Internal errors return -32603."""
        with pytest.raises(McpError) as exc_info:
            await mcp_server.call_tool("failing_tool", {})

        error = exc_info.value
        assert error.code == -32603
```

### Pytest Fixtures

```python
# conftest.py
import pytest
from server import create_mcp_server

@pytest.fixture
async def mcp_server():
    """Fixture providing initialized MCP server."""
    server = await create_mcp_server("test-server")
    yield server
    # Cleanup
    await server.cleanup()

@pytest.fixture
def sample_search_input():
    """Fixture for valid search input."""
    return {
        "query": "test query",
        "limit": 10,
        "filter_type": "code"
    }

@pytest.fixture
async def mcp_client():
    """Fixture providing MCP client for integration tests."""
    client = McpClient("test-client")
    await client.connect()
    yield client
    await client.disconnect()
```

### Coverage Requirements

```bash
# Run tests with coverage
pytest --cov=server --cov-report=html --cov-report=term

# Coverage targets
# - Protocol code (JSON-RPC): 100%
# - Tool implementations: 90%+
# - Resource handlers: 90%+
# - Overall: 90%+
```

### Anti-Patterns

❌ **Not Testing Strict Mode**
```python
# WRONG - doesn't verify strict mode prevents coercion
def test_input():
    SearchInput(limit="10")  # Should fail but test doesn't verify
```

❌ **Missing Async Tests**
```python
# WRONG - testing async code without pytest-asyncio
def test_async_tool():  # Should be @pytest.mark.asyncio async def
    result = call_tool()  # Should be await
```

❌ **Not Testing Error Cases**
```python
# WRONG - only testing happy path
def test_tool():
    result = call_tool(valid_input)
    assert result  # Missing invalid input tests
```

---

## Resources (Tier 3)

**pytest-asyncio**: https://pytest-asyncio.readthedocs.io/
**Pydantic Testing**: https://docs.pydantic.dev/latest/concepts/validation/
**JSON-RPC 2.0 Spec**: https://www.jsonrpc.org/specification
