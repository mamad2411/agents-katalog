---
name: integrate-zego-server-api
description: Implements ZEGO server API integration with signature authentication. Use when the user asks to call ZEGO server APIs, generate API signatures, or integrate backend features. Use when implementing room management, stream mixing, user kicking, or server-to-server messaging. Use when the user mentions 服务端API, 签名, 后端调用, server API signature, or backend integration with RTC/ZIM/AI Agent.
version: 2.0.3
---

# ZEGO Server API Integration

This skill provides guidance for integrating ZEGO server APIs. All ZEGO products (RTC, ZIM, AI Agent, etc.) share the same signature mechanism and request structure.

## Core Concept

Every ZEGO server API request requires a signature for authentication:

```
Signature = md5(AppId + SignatureNonce + ServerSecret + Timestamp)
```

## Workflow

### When User Needs Specific API Integration

When the user requests a specific feature or API (e.g., "kick user", "mix streams", "create room"):

1. **Get available datasets** - Call `mcp__plugin_zego-assistant_ZEGO__get_zego_product_datasets` to list all products and their knowledge base IDs
2. **Search for API docs** - Call `mcp__plugin_zego-assistant_ZEGO__search_zego_docs` with relevant dataset IDs
3. **Validate dataset IDs** - Ensure IDs contain only numbers and lowercase letters (no `-` or `_`)
4. **Confirm with user** - Present the found API and confirm before integrating
5. **Implement integration** - Add the API call with proper signature to the project

### Step 1: Get Credentials

Obtain `AppId` and `ServerSecret` from [ZEGO Console](https://console.zego.im/) or [ZEGOCLOUD Console](https://console.zegocloud.com) for english users.

**Important**: Never expose `ServerSecret` on the client side or commit it to version control.

### Step 2: Implement Signature Generation

Copy the signature implementation from `examples/` for your language:

| Language  | File              |
|-----------|-------------------|
| Go        | `signature.go`    |
| Python    | `signature.py`    |
| Java      | `Signature.java`  |
| Node.js   | `signature.ts`    |
| PHP       | `signature.php`   |
| C#        | `Signature.cs`    |

### Step 3: Build API Request

Add public parameters to every request:

| Parameter          | Value                           |
|--------------------|---------------------------------|
| AppId              | From console                    |
| SignatureNonce     | 16-char hex random (see below)  |
| Timestamp          | Unix timestamp in seconds       |
| Signature          | MD5 hash of the formula above   |
| SignatureVersion   | "2.0"                           |
| Action             | Target operation name           |

**Generate SignatureNonce**:
```python
# Python example
import secrets
nonce = secrets.token_hex(8)  # 16 hex chars
```

### Step 4: Parse Response

All responses follow this structure:

```json
{
    "Code": 0,
    "Message": "Succeed",
    "RequestId": "1843985617336143872",
    "Data": { /* action-specific data */ }
}
```

## Common API Endpoints

| Product  | API Host                   |
|----------|----------------------------|
| RTC      | rtc-api.zego.im            |
| ZIM      | zim-api.zego.im            |
| AI Agent | aigc-aiagent-api.zegotech  |

## Additional Resources

### Reference Files

- **`references/signature-mechanism.md`** - Detailed signature algorithm and error codes
- **`references/server-api-structure.md`** - Complete request/response format

### Examples

Signature implementations in `examples/`:
- **`signature.go`** - Go
- **`signature.py`** - Python
- **`Signature.java`** - Java
- **`signature.ts`** - TypeScript/Node.js
- **`signature.php`** - PHP
- **`Signature.cs`** - C#

## Quick Reference

**Error Codes**:
- `0` - Success
- `100000004` - Signature expired (regenerate)
- `100000005` - Signature invalid (verify algorithm)

**Signature Validity**: 10 minutes

**ID Rules**:
- UserId: max 32 bytes, `[a-zA-Z0-9-_]`
- RoomId: max 128 bytes, `[a-zA-Z0-9-_]`
- StreamId: max 128 bytes, `[a-zA-Z0-9-_]`
- AgentId: max 128 bytes, extended charset allowed
