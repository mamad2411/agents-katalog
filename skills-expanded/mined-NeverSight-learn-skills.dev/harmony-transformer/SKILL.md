---
name: harmony-transformer
description: Create scripts to transform datasets into OpenAI's Harmony format, or generate synthetic harmony-formatted data. Use this skill whenever you need to work with the Harmony response format for gpt-oss models.
---

# Harmony Transformer

This skill covers two capabilities:
1. **Transform** an existing dataset into Harmony format → see [transform.md](transform.md)
2. **Generate** synthetic harmony-formatted data → see [generate.md](generate.md)

**Use the official harmony-renderer library whenever possible.** Available on [PyPI](https://pypi.org/project/openai-harmony/) (`pip install openai-harmony`) and [crates.io](https://crates.io/crates/openai-harmony).

---

## Harmony Format Reference

### Roles & Hierarchy

| Role | Purpose |
|---|---|
| `system` | Reasoning effort, meta info, built-in tools |
| `developer` | Instructions (system prompt), function tools |
| `user` | User input |
| `assistant` | Model output — tool calls or message |
| `tool` | Tool call output; role name = tool name |

Hierarchy (higher overrides lower): `system > developer > user > assistant > tool`

### Channels

Assistant messages use exactly one channel:

| Channel | Purpose |
|---|---|
| `final` | User-facing response |
| `analysis` | Chain-of-thought; **do not expose to users** |
| `commentary` | Tool calls (`to=functions.{name}`), preambles |

### Special Tokens

| Token | ID | Purpose |
|---|---|---|
| `<|start|>` | `200006` | Message start |
| `<|end|>` | `200007` | Message end (stored history) |
| `<|message|>` | `200008` | Content delimiter |
| `<|channel|>` | `200005` | Channel delimiter |
| `<|constrain|>` | `200003` | Data type for tool call |
| `<|call|>` | `200012` | Tool call stop token |
| `<|return|>` | `200002` | Completion stop token |

### Message Structure

Basic:
```
<|start|>{header}<|message|>{content}<|end|>
```

With channel:
```
<|start|>assistant<|channel|>final<|message|>Hello.<|end|>
```

With recipient (tool call on commentary):
```
<|start|>assistant<|channel|>commentary to=functions.get_weather<|constrain|>json<|message|>{"location":"Paris"}<|call|>
```

Tool result:
```
<|start|>functions.get_weather to=assistant<|channel|>commentary<|message|>{"sunny": true, "temperature": 20}<|end|>
```

### System Message (required for gpt-oss)

Minimal with reasoning:
```
<|start|>system<|message|>You are ChatGPT, a large language model trained by OpenAI.
Knowledge cutoff: 2024-06
Current date: {date}

Reasoning: {low|medium|high}

# Valid channels: analysis, commentary, final. Channel must be included for every message.<|end|>
```

With function tools:
```
<|start|>system<|message|>You are ChatGPT, a large language model trained by OpenAI.
Knowledge cutoff: 2024-06
Current date: {date}

Reasoning: high

# Valid channels: analysis, commentary, final. Channel must be included for every message.
Calls to these tools must go to the commentary channel: 'functions'.<|end|>
```

### Developer Message (system prompt + tools)

```
<|start|>developer<|message|># Instructions

{instructions}

# Tools

## functions

namespace functions {

// {description}
type {name} = (_: {
// {param}: {type},
}) => any;

} // namespace functions<|end|>
```

### Reasoning

Model outputs CoT to `analysis` channel, final answer to `final` channel:

```
<|channel|>analysis<|message|>User asks 2+2. Simple math.<|end|>
<|start|>assistant<|channel|>final<|message|>2 + 2 = 4.<|return|>
```

On subsequent turns: replace `<|return|>` with `<|end|>` in history. Drop prior CoT if assistant ended on `final`.

### Tool Calling

- Define tools in the `developer` message (and note `Calls to these tools must go to the commentary channel: 'functions'.` in `system` message).
- Recipient format: `to=functions.{tool_name}`
- Tool call message: includes `<|constrain|>json` before arguments
- Tool result: role = tool name, `to=assistant`, channel = `commentary`

### Preambles

Before multiple tool calls, model may output a `commentary` message (visible to user) describing the plan:
```
<|channel|>commentary<|message|>**Action plan**:
1. Call get_weather
2. Call get_location
---<|end|>
```

### Structured Output

In developer message:
```
# Response Formats

## {format_name}

{json_schema}<|end|>
```

### Built-in Tools

Browser and python tools go in the `system` message on the `analysis` channel with recipients `browser.search`, `browser.open`, `browser.find`, and `python` respectively.

### Stop Token Rules

- `<|call|>` → stop, execute tool, continue inference
- `<|return|>` → stop, done. When storing to history, replace with `<|end|>`
- `<|end|>` → fully completed message in stored history

---

For detailed examples, see the [harmony renderer docs](https://github.com/openai/harmony).
