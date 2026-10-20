---
name: json-schema-from-python-signature
description: Generate a JSON Schema for an LLM tool's input from a Python function signature using inspect + get_type_hints, mapping str→string, int→integer, list→array, with Optional→nullable handling.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [json-schema, type-hints, llm-tools, introspection]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/tools/registered_tool.py
imported_at: 2026-04-18T00:00:00Z
---

# JSON Schema from Python Function Signature

## When to use
You're auto-registering function tools for an LLM (Anthropic tool-use, OpenAI function-calling) and don't want users to hand-write a JSON Schema for every tool. The function's annotated signature already describes the inputs.

## How it works
- `_strip_optional(annotation)` peels `Optional[T]` / `T | None` and remembers whether the field is nullable.
- `_annotation_to_json_schema` maps Python types to JSON Schema primitives.
- `infer_input_schema(func)` walks the signature, skips `*args`/`**kwargs` and underscore-prefixed params, computes each property's schema, and marks the param required if it has no default and isn't optional.

## Example
```python
def _strip_optional(annotation):
    origin = get_origin(annotation)
    if origin is None:
        return annotation, False
    args = tuple(a for a in get_args(annotation) if a is not NoneType)
    if len(args) != len(get_args(annotation)):
        if len(args) == 1: return args[0], True
        return args, True
    return annotation, False

def _annotation_to_json_schema(annotation):
    base, is_optional = _strip_optional(annotation)
    origin = get_origin(base)
    if base in (inspect.Signature.empty, Any):  schema = {}
    elif base is str:    schema = {"type": "string"}
    elif base is int:    schema = {"type": "integer"}
    elif base is float:  schema = {"type": "number"}
    elif base is bool:   schema = {"type": "boolean"}
    elif base is dict or origin is dict:  schema = {"type": "object"}
    elif base is list or origin in (list, set, tuple): schema = {"type": "array"}
    else: schema = {"type": "string"}
    if is_optional: schema["nullable"] = True
    return schema

def infer_input_schema(func):
    properties, required = {}, []
    type_hints = get_type_hints(func)
    for param in inspect.signature(func).parameters.values():
        if param.kind in (inspect.Parameter.VAR_POSITIONAL,
                          inspect.Parameter.VAR_KEYWORD): continue
        if param.name.startswith("_"): continue
        ann = type_hints.get(param.name, param.annotation)
        properties[param.name] = _annotation_to_json_schema(ann)
        _, is_optional = _strip_optional(ann)
        if param.default is inspect.Signature.empty and not is_optional:
            required.append(param.name)
    return {"type": "object", "properties": properties, "required": required}
```

## Gotchas
- Use `get_type_hints(func)` instead of reading `param.annotation` directly so forward references and `from __future__ import annotations` strings are resolved.
- Skip underscore-prefixed params — they're convention for "internal, do not pass" (e.g. `_sources` injected by the framework).
- The fallback type is `"string"` because LLMs handle string inputs gracefully when in doubt; using `"object"` would cause more hallucinations.
- Add `nullable: true` for Optional fields; some providers respect it (Anthropic, NIM) and OpenAI ignores extra fields.
