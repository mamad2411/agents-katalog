# execute_skill Tool

Execute a Brainy skill with the provided parameters.

## Usage

```json
{
  "skill_name": "dummy",
  "params": {
    "mode": "success",
    "message": "Hello from MCP!"
  }
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skill_name | string | Yes | Name of the skill to execute |
| params | object | No | Parameters to pass to the skill |

## Available Skills

Use `list_tools` to see all available skills.

### dummy

Dummy skill for testing. Supports multiple modes: success, error, slow.

**Parameters:**
- `mode` (optional): Test mode - success, error, or slow
- `message` (optional): Custom message for success mode
- `delay` (optional): Delay in milliseconds for slow mode

## Examples

### Execute dummy skill with success mode

```json
{
  "skill_name": "dummy",
  "params": {
    "mode": "success",
    "message": "Test completed!"
  }
}
```

### Execute dummy skill with slow mode

```json
{
  "skill_name": "dummy",
  "params": {
    "mode": "slow",
    "delay": "500"
  }
}
```

## Error Handling

If the skill execution fails, the response will include:
- `success: false`
- `error`: Description of the error

## Notes

- Some skills may not work fully in MCP context (e.g., skills requiring VS Code UI)
- Parameters are passed as strings and converted by the skill
