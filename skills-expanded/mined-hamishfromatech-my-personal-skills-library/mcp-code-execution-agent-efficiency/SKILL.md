---
name: mcp-code-execution-agent-efficiency
description: Improve AI agent efficiency by presenting MCP servers as code APIs rather than direct tool calls, enabling progressive disclosure, context-efficient data processing, and privacy-preserving operations. Use when building agents with many MCP tools, reducing token costs, or managing agent state across operations.
---

# MCP Code Execution for Agent Efficiency

## Overview

As MCP (Model Context Protocol) adoption scales, loading all tool definitions upfront and passing intermediate results through the context window creates excessive token consumption. **Code execution with MCP** solves this by presenting MCP servers as code APIs rather than direct tool calls — agents write code to interact with tools instead of calling them directly. This reduces token usage by up to 98.7% while enabling more powerful control flow, privacy-preserving operations, and state persistence.

Published by Anthropic (November 2025).

## When to Use

- Building agents connected to dozens or hundreds of MCP tools
- Reducing token costs and latency for tool-heavy agent workflows
- Processing large datasets through MCP tools without bloating context
- Implementing privacy-preserving agent workflows (sensitive data never enters model context)
- Persisting agent state across operations and building reusable skills
- Composing complex multi-step workflows with loops, conditionals, and error handling

## The Problem: Direct Tool Calls Don't Scale

### 1. Tool Definitions Overload Context
Most MCP clients load all tool definitions upfront. Each tool definition includes description, parameters, return types — consuming hundreds of tokens per tool. With thousands of tools, agents process hundreds of thousands of tokens before reading a request.

### 2. Intermediate Results Consume Tokens
When agents call tools directly, every intermediate result passes through the model's context. A 2-hour meeting transcript (50,000 tokens) flows through context twice — once when retrieved, once when passed to the next tool.

## The Solution: Code Execution Pattern

### Core Architecture
Present MCP servers as a file tree of code APIs:

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   ├── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   ├── index.ts
```

Each tool becomes a code file:
```typescript
// ./servers/google-drive/getDocument.ts
import { callMCPTool } from "../../../client.js";

export async function getDocument(input: { documentId: string }) {
  return callMCPTool('google_drive__get_document', input);
}
```

The agent discovers tools by **exploring the filesystem** — listing directories, reading only the files it needs. This is **progressive disclosure**.

### Token Savings Example
- **Direct tool calls**: 150,000 tokens (all tool definitions loaded upfront)
- **Code execution**: 2,000 tokens (agent reads only 2 needed tool files)
- **Savings**: 98.7% reduction

## Key Benefits

### 1. Progressive Disclosure
Models are excellent at navigating filesystems. Instead of loading all tool definitions upfront, agents:
- List the `./servers/` directory to find available servers
- Read specific tool files to understand interfaces
- Load only what they need for the current task

Alternatively, add a `search_tools` function with a detail-level parameter (name only, name+description, or full schema).

### 2. Context-Efficient Data Processing
Filter and transform large datasets in the execution environment before returning to the model:

```javascript
// Without code execution: 10,000 rows flow through context
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
// Model must process all 10,000 rows

// With code execution: filter first, return only 5 rows
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pending = allRows.filter(row => row.Status === 'pending');
console.log(pending.slice(0, 5)); // Agent sees only 5 rows
```

### 3. Powerful Control Flow
Use familiar code patterns instead of chaining individual tool calls:
- **Loops**: Poll for conditions without alternating between tool calls and sleep commands
- **Conditionals**: Evaluate if-statements in code, not through model reasoning
- **Error handling**: Try/catch blocks instead of agent loop error recovery
- **Reduced latency**: Code execution environment handles logic; model doesn't wait for intermediate evaluations

### 4. Privacy-Preserving Operations
Intermediate results stay in the execution environment by default. The agent only sees what you explicitly log or return.

**Automatic PII tokenization**: The MCP client can intercept and tokenize sensitive data before it reaches the model:
```javascript
// Agent would see (if it logged the data):
[{ email: '[EMAIL_1]', phone: '[PHONE_1]', name: '[NAME_1]' }]
// Real data flows from Google Sheets → Salesforce, never through the model
```

**Deterministic security rules**: Define where data can flow to and from, independent of model behavior.

### 5. State Persistence and Skills
Agents can write intermediate results to files and persist their own code as reusable functions:

```javascript
// Save working code for future use
// In ./skills/save-sheet-as-csv.ts
export async function saveSheetAsCsv(sheetId: string) {
  const data = await gdrive.getSheet({ sheetId });
  const csv = data.map(row => row.join(',')).join('\n');
  await fs.writeFile(`./workspace/sheet-${sheetId}.csv`, csv);
  return `./workspace/sheet-${sheetId}.csv`;
}
```

Adding a `SKILL.md` file creates a structured skill that models can reference — building a toolbox of higher-level capabilities over time.

## Implementation Considerations

### Security Requirements
- Secure execution environment with sandboxing
- Resource limits (CPU, memory, execution time)
- Monitoring for agent-generated code
- Operational overhead vs. direct tool calls

### When to Use vs. When Not to
**Use code execution when:**
- Agent connects to many MCP servers (10+)
- Processing large datasets through tools
- Privacy-sensitive workflows
- Complex multi-step workflows with logic
- Building reusable agent skills

**Use direct tool calls when:**
- Few tools (under 10)
- Simple request-response patterns
- No sensitive data concerns
- Minimal infrastructure overhead desired

## MCP Ecosystem Context (2025-2026)

- **177,000+ MCP tools** published as of February 2026
- **Action tools** grew from 27% to 65% of usage (Nov 2024 → Feb 2026)
- **General-purpose tools** (browser, computer use) growing fastest
- **AI-coauthored tools**: 28% of MCP servers show evidence of AI assistance (62% of new servers in Feb 2026)
- **Software development** dominates: 67% of all tools, 90% of downloads
- **Financial transaction tools** represent a fast-growing high-stakes category

### Security Concerns
- Tool poisoning: MCP tool contains malicious description
- Cross-server tool shadowing: Malicious agent intercepts calls to trusted servers
- Protocol focuses on simplicity, not authentication/encryption
- "Toxic flow analysis" and tools like MCP-scan emerging to address these

## Source

Jones, A. & Kelly, C. (2025). "Code execution with MCP: Building more efficient agents." Anthropic Engineering Blog, November 4, 2025.

Stein, M. (2026). "How are AI agents used? Evidence from 177,000 MCP tools." arXiv:2603.23802.

Model Context Protocol Specification (2025-11-25). modelcontextprotocol.io