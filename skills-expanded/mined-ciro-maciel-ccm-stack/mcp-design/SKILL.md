---
name: mcp-design
description: Design a product's MCP as four tools (guide, read, write, delete) over its own routes, destruction confirmed by the person. Use for any MCP server.
---

# An MCP in four tools

An MCP with one tool per endpoint grows without end, fills the agent's context, and drifts from the product. Four tools over the routes the product already has stay small and never fall behind.

## The four tools

| Tool | Does | Maps to |
|---|---|---|
| `<product>_guide` | Returns the table of routes and operations: path, method, what it does, its arguments. The agent reads it first. | Nothing; it is documentation generated from the route table. |
| `<product>_read` | Reads anything the person could see on screen. | `GET` routes |
| `<product>_write` | Creates and changes. | `POST`, `PUT`, `PATCH` routes |
| `<product>_delete` | Destroys, after the person confirms. | `DELETE` and destructive routes |

Every call enters the **same handler the screen uses**, with the person's identity and permissions. No parallel logic, no separate checks: what the screen allows, the MCP allows, and nothing more.

## Destruction asks the person

`delete` takes two calls. The first returns `confirmRequired` with what will be destroyed and a short-lived confirmation code (an HMAC over account, method, path and body, valid for 10 minutes). The agent shows this to the person. Only a second call carrying that code and an explicit confirmation acts.

Count as destructive: `DELETE`, and routes whose last segment is a destructive verb such as revoke, disable, cancel, archive, unpublish or refund. Rotating a key is not destruction.

## The agent never decides for the person

Routes where a person approves, rejects, answers or decides are refused to agents. An agent that asks a question never answers it.

## Grow the guide, not the tools

A new feature adds rows to the route table, and `guide` shows them at once. Never add a fifth tool for one endpoint.

## Prove it

For each tool, one live call with a test account: `guide` lists every route, `read` returns what the screen shows, `write` creates something you then read back with a unique value, and `delete` refuses without confirmation and acts with it.
