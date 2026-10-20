---
name: handler-dispatch-pattern-with-tool-callbacks
description: Minimal agent tool-dispatch pattern with before/after hooks, turn-end callback, and generator-based streaming outcomes.
category: architecture
version: 1.0.0
tags: [llm-agents, architecture, middleware, dispatch, python]
source_type: extracted-from-git
source_url: https://github.com/lsdefine/GenericAgent.git
source_ref: main
source_commit: ec34b7e1c0f11fbb9709680ccfe313187a1b942b
source_project: GenericAgent
source_path: agent_loop.py
imported_at: 2026-04-18T00:00:00Z
confidence: medium
version_origin: extracted
---

# Handler dispatch with tool callbacks

A ~30-line Python pattern for routing LLM tool calls to concrete methods, with pre/post callbacks and a turn-end hook, plus a `StepOutcome` shape that cleanly encodes three exit paths (continue, done, exit-now). Lets you bolt instrumentation, auth, rate-limiting, or memory-updating logic onto any tool call without touching the tool's body.

## When to use

Building an agent framework in Python where:

- The LLM emits structured tool calls (OpenAI function-calling style, Anthropic tool-use, etc.).
- You want middleware-style cross-cutting concerns (logging, metric collection, argument rewriting, response postprocessing) without wrapping every tool manually.
- You want streaming output (the tool implementation yields progress text as it works), without sacrificing a clean return value.

## The shape

```python
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class StepOutcome:
    data: Any                           # the tool's return value
    next_prompt: Optional[str] = None   # what to feed back to the LLM next turn
    should_exit: bool = False           # terminate the loop immediately

class BaseHandler:
    # Hooks — subclass overrides these to inject instrumentation.
    def tool_before_callback(self, tool_name, args, response): pass
    def tool_after_callback(self, tool_name, args, response, ret): pass
    def turn_end_callback(self, response, tool_calls, tool_results,
                          turn, next_prompt, exit_reason):
        return next_prompt

    def dispatch(self, tool_name, args, response, index=0):
        method = f"do_{tool_name}"
        if hasattr(self, method):
            args["_index"] = index
            # before-hook may be a plain function or a generator (for progress).
            yield from _try_call_gen(self.tool_before_callback, tool_name, args, response)
            ret = yield from _try_call_gen(getattr(self, method), args, response)
            yield from _try_call_gen(self.tool_after_callback, tool_name, args, response, ret)
            return ret
        elif tool_name == "bad_json":
            return StepOutcome(None, next_prompt=args.get("msg", "bad_json"))
        else:
            yield f"Unknown tool: {tool_name}\n"
            return StepOutcome(None, next_prompt=f"Unknown tool {tool_name}")
```

where `_try_call_gen` dual-dispatches plain-returns and generator-returns:

```python
def _try_call_gen(func, *args, **kwargs):
    ret = func(*args, **kwargs)
    if hasattr(ret, "__iter__") and not isinstance(ret, (str, bytes, dict, list)):
        ret = yield from ret
    return ret
```

## Defining a tool

```python
class MyHandler(BaseHandler):
    def do_file_read(self, args, response):
        path = args["path"]
        yield f"Reading {path}...\n"           # streamed progress
        text = open(path).read()
        return StepOutcome(data=text, next_prompt=None)   # next_prompt None ⇒ task-done signal
```

## What the three `StepOutcome` fields mean (in the loop)

The outer loop (see companion knowledge entry `agent-loop-architecture-reference`) interprets the outcome like this:

| Field | Effect on the loop |
|---|---|
| `should_exit=True` | Stop the loop immediately; mark as `EXITED` |
| `next_prompt=None` | This tool is signaling "current task is complete"; stop unless other tools in the same turn disagree |
| `next_prompt="..."` | Feed this string back to the LLM as the user message for next turn |
| `data` | Serialized and included in the tool_results payload to the LLM |

## Before/after hooks — the useful cases

```python
class LoggingHandler(MyHandler):
    def tool_before_callback(self, tool_name, args, response):
        yield f"→ {tool_name}({_short(args)})\n"

    def tool_after_callback(self, tool_name, args, response, ret):
        if isinstance(ret, StepOutcome) and ret.should_exit:
            metrics.increment(f"tool.exit.{tool_name}")
```

Typical uses: redact sensitive fields before logging, rewrite the result for a specific tool, collect latency metrics, or inject a `_keyinfo` side-channel update after the tool completes.

## turn_end_callback — the "what did we just do" hook

Called once per turn, after all tools have dispatched and the next prompt is assembled. Good place for: updating a rolling checkpoint, compressing history, noticing a stall (same exit reason twice in a row), or injecting a cooldown reminder into the next prompt.

Return value: the (possibly rewritten) `next_prompt`. Return the incoming `next_prompt` unchanged if you just want to observe.

## Why generators?

Making `do_*` methods into generators lets the tool emit progress (streamed to stdout / client) *and* a final `StepOutcome` return value, with natural Python syntax. `yield` means progress text; `return StepOutcome(...)` means the final answer. The loop's `yield from`/`StopIteration` machinery handles both ends automatically.

If your tool doesn't need streaming, just `return StepOutcome(...)` from a plain method — `_try_call_gen` detects and degrades to a normal call.

## Pattern extensions

- **Tool indexing for parallel calls:** The `_index` arg (injected by `dispatch`) lets tools disambiguate when the LLM emits multiple parallel calls (e.g., `search` called twice in one turn).
- **Bad-JSON recovery:** The `bad_json` tool name is a conventional sentinel the caller injects when the LLM emits malformed JSON; `dispatch` echoes the message back as the next prompt without blowing up the loop.
- **Hook auto-fallthrough:** `_try_call_gen` means subclasses can *optionally* make hooks generators (to stream diagnostic text) without base callers needing to care.

## Anti-patterns

- Wrapping every tool in ad-hoc decorators instead of using the callbacks. Decorator soup breeds; hooks scale.
- Returning raw strings/dicts instead of `StepOutcome`. You lose the exit semantics.
- Making `turn_end_callback` do heavy IO. It runs every turn; keep it cheap or gate it on conditions.

---

Extracted from GenericAgent's `agent_loop.py`. The pattern is framework-agnostic — adaptable to any Python-based agent loop.
