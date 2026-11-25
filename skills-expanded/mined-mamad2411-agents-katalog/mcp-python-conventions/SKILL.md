---
name: mcp-python-conventions
description: "Use when writing the Python inside an MCP server and deciding how it should behave — where log output may go when stdout carries JSON-RPC framing and why a stray print breaks the protocol, what an exception at a tool boundary should turn into for the calling model, how much internal detail an error may safely expose, and how to write a tool docstring that the model reads as its instructions rather than as documentation for a human. Scoped to stdio-transport servers. For a server's packaging, installation and registration rather than its code, see the MCP server shipping skill; for general Python design questions, see the Python conventions skill."
metadata:
  family: python
---

# MCP server code conventions

The Python inside a stdio-transport MCP server. Split out of `python-conventions` on 2026-08-31,
which keeps the general design defaults — this skill owns only what is different _because_ the code
is an MCP server, and those differences are not stylistic: two of the three are protocol
correctness.

Not about shipping. Entry points, `uv tool install`, `claude mcp add` and scope selection belong to
`mcp-server-shipping`; this is what the code does once it runs.

## MCP-stdio logging discipline

_Scope: stdio-transport MCP servers only (the `*-polite-mcp` family) — not applicable to
`power-user-linux-setup` itself, which has no MCP server._

- Snippet: [`references/snippets/mcp-tool-boundary.py`](references/snippets/mcp-tool-boundary.py)
- Default: never a bare `print()` in server package code. Route all logging through the stdlib
  `logging` module, explicitly configured to write to stderr at startup (or defer to FastMCP's own
  `configure_logging()`, which already defaults there).
- Why: the MCP stdio spec is unambiguous — a server **MUST NOT** write anything to stdout that isn't
  a valid MCP message; a single stray `print()` or a dependency's stdout-bound log handler corrupts
  the JSON-RPC stream. stderr is the sanctioned outlet for everything, logs included.
- **Don't**: trust that "no `print()` in my code" is sufficient — a dependency that logs to stdout
  on its own initiative isn't caught by explicit stderr configuration of your own logging. The
  robust check is exercising the real stdio transport end-to-end, not code review alone.
- Model default: **overrides — sharply, not a style nudge.** This is protocol-specific knowledge a
  model has no general-Python reason to know; without it, a model reaches for `print()` debugging
  exactly as it would in any other script, silently breaking the server.

## Error handling at the MCP tool boundary

_Scope: stdio-transport MCP servers only, same as above._

- Snippet: [`references/snippets/mcp-tool-boundary.py`](references/snippets/mcp-tool-boundary.py)
- Default: at the point an internal exception is about to cross back to the client, decide
  deliberately what's safe to expose — either re-raise as `fastmcp.exceptions.ToolError` with an
  explicit, hand-written message, or let a plain exception raise (FastMCP's default already surfaces
  it, unmasked, to the client). Never assume `str(exc)` of an arbitrarily caught exception is safe
  by default, especially inside a broad per-item `except Exception` (a legitimate pattern for
  isolating one bad item in a batch call — just don't let its caught exception's message reach the
  client unreviewed).
- Why: FastMCP's default (`mask_error_details=False`) already includes full exception detail in the
  client-facing response — this isn't an opt-in risk, it's the out-of-the-box behavior. The same
  shape as this skill's `SecretStr` caveat: a broad safety switch doesn't sanitize text you
  deliberately choose to expose.
- **Don't**: flip `mask_error_details=True` project-wide as a blanket fix — it suppresses
  legitimately useful validation detail (a bad argument, a batch-size violation) that plain
  `raise ValueError(...)` call sites rely on being visible to the calling agent. Prefer the
  finer-grained per-message `ToolError` choice.
- Model default: **overrides.** A model doesn't know `ToolError` exists or that FastMCP unmasks
  exceptions by default unless told — without this, it either leaves exceptions to propagate as-is
  (today's actual state in this family) or reaches for a blanket masking flag, both worse than the
  deliberate per-boundary choice.

## MCP tool docstrings

_Scope: any function decorated as an MCP tool (`@mcp.tool()` in this family). A genuinely distinct
concern from general docstring style — no general docstring-content rule exists elsewhere in this
skill to extend._

- Default: write the docstring to Anthropic's tool-definition bar, not PEP 257's — what the tool
  does and how it differs from its nearest sibling by name, when to use/not use it, where each
  non-obvious parameter's value comes from, response shape/size caveats, **at least 3–4 sentences,
  more for a complex tool**. See `references/rationale.md` §11 for the concrete template and this
  family's own strongest real examples.
- Why: the docstring becomes the wire-level `Tool.description` an LLM client reads at inference time
  to decide whether/how to call the tool — a weak one causes wrong-tool-picked, wrong-arguments, or
  never-invoked failures, a correctness cost paid by every future call, not a comprehension-speed
  one the way a weak human-facing docstring is.
- Escalate to: `Annotated[x, Field(description=...)]` for per-parameter descriptions once free-form
  prose isn't enough (so the JSON-Schema `inputSchema` itself carries them); `annotations=`
  (`readOnlyHint`/`destructiveHint`/etc.) on any tool with real side effects, since clients use it
  to decide when to skip or require confirmation prompts.
- Model default: **overrides.** A model's default docstring instinct is PEP 257's — a concise
  one-line summary — which is actively worse here; the entire point of this section is that the bar
  for an LLM-facing description is different from, not a stricter version of, ordinary docstring
  style.

## Full rationale

See [`references/rationale.md`](references/rationale.md) — the sources for the stdout constraint,
the error-taxonomy reasoning, and the docstring-as-contract argument.

## Starter snippet

[`references/snippets/mcp-tool-boundary.py`](references/snippets/mcp-tool-boundary.py) is a runnable
sketch of the tool-boundary error handling described here.

## Editing this skill

This file is _copied_ into `~/.agents/skills/mcp-python-conventions` at install time, never
symlinked. Edit the source in the [`agent-skills`](https://github.com/TheodoreAD/agent-skills) repo,
push, then re-run the install
(`npx skills add TheodoreAD/agent-skills --global --skill mcp-python-conventions`) to refresh every
project's copy. Editing the deployed copy in place is local drift and reaches no other machine.
