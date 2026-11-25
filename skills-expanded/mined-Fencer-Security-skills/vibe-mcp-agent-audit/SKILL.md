---
name: vibe-mcp-agent-audit
description: Audit a vibe-coded MCP server or AI agent and produce a severity-tagged markdown report. Use when the user wants to security-review an MCP server (`@modelcontextprotocol/sdk`, `mcp` Python), a Claude Agent SDK loop, a LangChain/LangGraph agent, or any custom agent exposing tools to an LLM — "audit my MCP server," "review my agent's tool surface," "is my LLM app safe." Covers tool surface and least-privilege, parameter validation, prompt injection (direct and indirect via tool outputs), output sanitization, tool-level authz, and resource limits, on top of the shared baseline. Runs safe live probes against the running server / agent (enumerate tools, missing-param / wrong-type rejection, SSRF) and asks before intrusive probes.
allowed-tools: Read Grep Glob
---

# Vibe-coded MCP server / AI agent security audit

Audits MCP servers (stdio or HTTP) and AI agents (Claude Agent SDK, LangChain, LangGraph,
custom loops). These share a threat model:

- The **tool surface** is the privilege boundary. An LLM that can invoke a `shell` tool can
  do anything the user running the agent can do.
- **Prompt injection** is the dominant runtime vulnerability — user input, fetched web pages,
  emails, and tool outputs can all carry instructions that override the system prompt.
- **Parameter validation** is the tool boundary's seatbelt. If a `read_file` tool accepts any
  path the LLM proposes, that's a file-disclosure vulnerability.
- **Output sanitization**: the LLM's reply often echoes content; if that content includes
  secrets pulled from a tool, they leak to the user (or to logs).

## When to use this skill

Use this when the user wants to security-review an MCP server or an AI agent. Examples: a
filesystem MCP server, a Claude Agent SDK app, a LangChain agent with custom tools.

Don't use this for: chat bots (use `vibe-bot-audit`, even if they call an LLM), user-facing web
apps that happen to have an "AI feature" (use `vibe-webapp-audit`), or pure prompt-engineering
review with no code (out of scope).

## Inputs the skill expects

- A path to a local repo or single source file.
- Optionally, a **runtime target** — either `stdio: <command>` (for MCP stdio servers) or
  `http: <url>` (for MCP HTTP servers or agent HTTP endpoints).

Ask for the runtime target at the start. If not provided, skip live tests and note this.

## Workflow

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${SKILL_DIR}}"
SHARED_DIR="$SKILL_DIR/../../shared"
# Always reads:
#   $SHARED_DIR/references/baseline.md
#   $SHARED_DIR/references/live-tests-baseline.md
#   $SHARED_DIR/references/report-template.md
# Conditionally:
#   $SKILL_DIR/references/mcp-server.md   (if MCP server detected)
#   $SKILL_DIR/references/agent-loop.md   (if an agent loop detected)
#   $SKILL_DIR/references/live-tests.md   (if a runtime target is provided)
```

1. **Detect what kind of thing this is** (~30s — see below).
2. **Ask for the runtime target.**
3. **Run the baseline** (`$SHARED_DIR/references/baseline.md`, checks A–D).
4. **Run the category-specific static checks** (sections 1–6 below). Read the matching
   reference file.
5. **Run live tests** if a target was provided. Read `$SHARED_DIR/references/live-tests-baseline.md`
   then `$SKILL_DIR/references/live-tests.md`.
6. **Render the report** using `$SHARED_DIR/references/report-template.md`.

### Detect the shape

```bash
# MCP SDKs
grep -hE '"@modelcontextprotocol/sdk"' package.json 2>/dev/null
grep -hE "(mcp|fastmcp)" requirements.txt pyproject.toml 2>/dev/null

# Agent SDKs
grep -hE '"@anthropic-ai/(claude-agent-sdk|sdk)"|"openai"|"langchain"|"langgraph"' \
  package.json 2>/dev/null
grep -hE "(anthropic|openai|langchain|langgraph)" requirements.txt pyproject.toml 2>/dev/null

# Tool registration patterns
grep -rE "(server\.tool|@mcp\.tool|tools/list|registerTool)" --include="*.{ts,js,py}" . | head -20
grep -rE "(StructuredTool|@tool|client\.messages.create.*tools=)" \
  --include="*.{ts,js,py}" . | head -20

# Transport
grep -rE "(StdioServerTransport|SSEServerTransport|HttpServerTransport)" \
  --include="*.{ts,js,py}" . | head -10
```

**MANDATORY** based on detection:

- **MCP server only** (server exposes tools to clients, no autonomous agent loop) →
  **MANDATORY: read `$SKILL_DIR/references/mcp-server.md` in full.** Do NOT load `agent-loop.md`.
- **Agent loop only** (uses LLM SDK with tools, no MCP surface) → **MANDATORY: read
  `$SKILL_DIR/references/agent-loop.md` in full.** Do NOT load `mcp-server.md`.
- **Both** (agent that's also an MCP server, or MCP server with its own internal agent) →
  read both, MCP first.

## 1 — Tool surface

**Before classifying a tool, ask yourself**: if the LLM were jailbroken or prompt-injected,
what's the worst this _one_ tool lets the attacker do? "Read a file" sounds benign until the
path is unconstrained. "Fetch a URL" sounds benign until `file://` or `http://169.254.169.254`
work. Classify by the _worst legal use_ of the tool, not the intended one.

List every tool the server / agent exposes. For each:

- **Name** and one-line description.
- **Inputs** (parameter schema).
- **Side effects** (filesystem write? network? subprocess? database?).
- **Privilege** (does it act as the agent's user, or with a different identity?).

Severity by side effect:

| Side effect                                        | Severity if loosely-validated                        |
| -------------------------------------------------- | ---------------------------------------------------- |
| Read filesystem with caller-supplied path          | **High** (file disclosure)                           |
| Write filesystem with caller-supplied path         | **Critical** (arbitrary write → RCE if writing code) |
| Subprocess / shell with caller-supplied input      | **Critical** (RCE)                                   |
| Outbound HTTP with caller-supplied URL             | **High** (SSRF — can reach internal services)        |
| Database read/write with caller-supplied filter    | **High** (data exposure / corruption)                |
| Send-message / post-to-channel with caller content | **Medium** (spam / abuse)                            |
| Pure compute (math, formatting)                    | **Info**                                             |

A tool surface with `shell`, `read_file(any path)`, `fetch_url(any url)`, AND `write_file(any
path)` is functionally a remote-code-execution kit. Flag this as a finding even if validation
elsewhere is OK — least-privilege is the lesson.

## 2 — Parameter validation

**Before flagging a tool parameter, ask yourself**: is the schema _advisory_ (the SDK passes it
to the LLM as documentation) or _enforced_ (the handler rejects calls that don't match)? Most
MCP/agent SDKs do the former by default — the schema shapes the LLM's call, but doesn't
validate the actual args at runtime. The handler must validate again.

Each tool's input schema is contract. The handler must validate against it (don't trust the
LLM to send well-formed args, especially under prompt injection).

**Patterns to flag:**

| Pattern                                                                                 | Severity                                                            |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Tool handler using `args.x` without schema-level type/format checks                     | **High**                                                            |
| TypeScript `as MyType` or Python untyped dict access standing in for runtime validation | **Medium**                                                          |
| Paths accepted without `realpath` + containment check against an allowed root           | **High**                                                            |
| URLs accepted without scheme allowlist (`http`/`https` only)                            | **High** — `file://`, `gopher://`, `ftp://` enable SSRF / file read |
| Numeric inputs without bounds                                                           | **Medium**                                                          |

## 3 — Prompt injection

**Before flagging a prompt-injection risk, ask yourself**: where does _adversarial_ content
enter the model context? Direct injection (user types it) is expected and not by itself a
finding — the question is what tools the agent can call in response. Indirect injection
(content arrives via a tool that fetched the web, read an email, opened a file) is the higher-
risk category because the user often didn't _intend_ to send that content to the model.

Direct: user input goes straight into the LLM prompt. This is normal for an agent; the issue is
what the agent can do with it.

Indirect: external content reaches the LLM via tools — a fetched webpage, an email body, a
file the agent reads. This content can include "ignore previous instructions" payloads that the
LLM may obey.

Flag:

- A tool returns content from an external source (web fetch, email read, file read) AND that
  content is fed directly to the LLM with no system-prompt boundary. **High**.
- System prompt does NOT name external content as untrusted. **Medium**.
- Agent has tool access to destructive actions (delete, send-email, push) AND processes external
  content. **High** — indirect prompt injection can trigger those tools.
- No human-in-the-loop confirmation for destructive tools. **High** for irreversible actions
  (deletes, payments, public posts).

## 4 — Output sanitization

**Before flagging output as leaking, ask yourself**: who reads the agent's _full context_ —
the user, the developer in logs, or both? An agent that "summarizes a file" with a `read_file`
tool can leak the file's contents in two places: the assistant's reply (user sees it) and
the conversation log (developer sees it). Both are leak channels; severity tracks who shouldn't
have seen what.

The LLM's reply is rendered back to the user / client. If the reply contains content the LLM
read from a tool, secrets in that content leak.

Flag:

- Tool reads a credentials file then the LLM is allowed to quote arbitrary parts of it. **High**.
- Tool reads database rows including PII / secrets, LLM is asked to "summarize" without
  scrubbing. **High**.
- Logs capture full LLM context, including tool outputs that contain secrets. **High**.

## 5 — Tool-level authorization

**Before flagging an authz gap, ask yourself**: is this MCP server / agent single-tenant
(stdio, one user, one process) or multi-tenant (HTTP, multiple users connecting)? Single-tenant
stdio servers don't need per-call authz — the transport itself implies one trusted client.
Multi-tenant network deployments inherit _all_ the authz concerns of a regular service, on top
of the tool-surface concerns above.

For MCP servers exposed to multiple clients, or agents accessed by multiple users:

- Is there a per-call authorization layer? Or does the server trust whoever connected?
- For agents, does the LLM perform any check before invoking a destructive tool, or is it the
  user's responsibility?

Flag:

- MCP server with destructive tools and no client authentication. **High** if exposed over
  network; **Low** if stdio-only.
- Agent that auto-executes tool calls including destructive ones. **High** if irreversible.
- "Confirmation step" implemented as "the LLM should ask" (the LLM is non-deterministic and
  can be prompted to skip the check). **High**.

## 6 — Resource limits

**Before flagging a missing limit, ask yourself**: who _pays_ when the loop runs away? In a
developer's local agent, an unbounded loop just burns the developer's tokens — annoying but
not a security issue. In a SaaS deployment, the same loop is a DoS vector: a single user can
exhaust the team's monthly Anthropic budget in minutes. Severity tracks the deployment model,
not the code shape.

**Patterns to flag:**

| Pattern                                                                     | Severity                                               |
| --------------------------------------------------------------------------- | ------------------------------------------------------ |
| Agent loop with no maximum-iterations guard                                 | **Medium** in SaaS / multi-user; **Low** in local-only |
| Tool that recurses without depth limit (e.g., `list_all_files`)             | **Low**                                                |
| No token budget per session in a SaaS deployment                            | **Medium** — cost-DoS vector                           |
| Tool returns can balloon the context (full file contents, entire web pages) | **Low** — cost + accuracy degradation                  |

**Find the surface:**

```bash
grep -rE "(max_iterations|max_steps|max_tokens|maxTurns|MAX_LOOP)" \
  --include="*.{ts,js,py}" . | head -10
grep -rE "(setMaxListeners|stack.*limit|sys\.setrecursionlimit)" \
  --include="*.{ts,js,py}" . | head -10
```

## Producing the report

Read `$SHARED_DIR/references/report-template.md`. Save as
`vibe-mcp-agent-audit-<YYYY-MM-DD>-<HHMM>.md`. Tell the user the exact path.

## What this skill is NOT

- Not a prompt-engineering review. The skill audits the code surrounding the LLM, not the
  prompt itself.
- Not a model-capability review. "What can Claude do" is out of scope; "what can the agent do
  via tools" is in scope.
- Not a jailbreak audit. The skill doesn't try to bypass safety training; it audits the host
  application's controls.
