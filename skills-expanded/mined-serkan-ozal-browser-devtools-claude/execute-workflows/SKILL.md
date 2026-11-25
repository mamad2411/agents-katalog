---
name: execute-workflows
description: Use when the user wants to run JavaScript in the browser, run code in Node, or batch multiple MCP tool calls. Run script, execute code, batch tools.
---

# Execute Workflows Skill

Use this skill when the user asks to run JavaScript, execute code in the page or on the server, or batch several tool calls into one.

## Rule: Use execute only

There are **no separate run-JS tools**. Always use the MCP tool **`execute`**.

### Run JavaScript in the browser page

Use **`execute`** with `page.evaluate()`:

```javascript
// execute tool, code:
return await page.evaluate(() => document.title);
```

You have access to `page` (Playwright Page) and `callTool(name, input, returnOutput?)` inside the execute VM. Use `await` with `callTool`.

### Run JavaScript on the server (Node VM, no DOM)

Use **`execute`** without `page.evaluate()` — e.g. Buffer, crypto, or multiple `callTool` calls:

```javascript
return Buffer.from('hello').toString('base64');
```

### Batch multiple tool calls

Use **`execute`** and call tools via `await callTool(name, input, returnOutput?)`:

```javascript
await callTool('interaction_fill', { selector: 'e3', value: 'user@test.com' });
await callTool('interaction_click', { selector: 'e7', waitForNavigation: true });
const snapshot = await callTool('a11y_take-aria-snapshot', {}, true);
return snapshot;
```

Max 50 `callTool` calls per execution. Pass `true` as third argument to include that tool’s output in the response `toolOutputs`.

### Node platform (backend debugging)

On Node platform, **`execute`** has no `page`; use `callTool` only. See [commands/node/execute.md](../../commands/node/execute.md).

## References

- Browser: [commands/browser/execute.md](../../commands/browser/execute.md) — `page`, `callTool`, VM API
- Node: [commands/node/execute.md](../../commands/node/execute.md) — `callTool` only
