---
name: structured-output-json-fallback-extractor
description: Wrap LLM calls in a structured-output adapter that injects the Pydantic schema into the prompt, then extracts JSON from the response by trying direct parse → fenced-block strip → object regex → array regex, with a "single field" fallback for models that return just the array.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [structured-output, llm, json-extraction, pydantic, schema]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/services/llm_client.py
imported_at: 2026-04-18T00:00:00Z
---

# Structured Output with JSON Fallback Extraction

## When to use
You want `llm.with_structured_output(MyPydanticModel).invoke(prompt)` semantics across providers that don't all support structured output natively. The wrapper must handle the common LLM "I returned valid JSON but inside a fenced markdown block / preceded by an apology" failure modes gracefully.

## How it works
- `StructuredOutputClient` wraps any LLM client. `invoke()` injects the schema JSON into the prompt, calls the underlying client, then extracts JSON.
- `_extract_json_payload(text)` tries four strategies in order:
  1. Direct `json.loads` after stripping leading/trailing whitespace.
  2. Strip triple-backtick fences (` ```json ` / ` ``` `) and retry.
  3. Regex `\{.*\}` to grab the first object.
  4. Regex `\[.*\]` to grab the first array.
- If validation fails on a list payload, try wrapping it as `{"actions": payload, "rationale": "..."}` for models that returned a list when an object with one list field was expected.

## Example
```python
class StructuredOutputClient:
    def __init__(self, base, model):
        self._base = base; self._model = model

    def invoke(self, prompt):
        schema_json = json.dumps(self._model.model_json_schema(), indent=2)
        wrapped = (f"{prompt}\n\nReturn ONLY valid JSON that matches this schema:\n"
                   f"{schema_json}\n")
        response = self._base.invoke(wrapped)
        payload = _extract_json_payload(response.content)
        try:
            return self._model.model_validate(payload)
        except ValidationError:
            if isinstance(payload, list) and "actions" in self._model.model_fields:
                fallback = {"actions": payload, "rationale": "LLM returned actions only."}
                return self._model.model_validate(fallback)
            raise

def _extract_json_payload(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()
    try:    return json.loads(cleaned)
    except json.JSONDecodeError: pass
    if (m := re.search(r"\{.*\}", cleaned, re.DOTALL)):
        try:    return json.loads(m.group(0))
        except json.JSONDecodeError: pass
    if (m := re.search(r"\[.*\]", cleaned, re.DOTALL)):
        try:    return json.loads(m.group(0))
        except json.JSONDecodeError: pass
    raise ValueError("LLM did not return valid JSON payload")
```

## Gotchas
- `re.DOTALL` is mandatory — JSON output spans newlines.
- Use `json.loads(..., strict=False)` as a second attempt to allow control characters in strings (some LLMs emit raw `\n` inside strings).
- For lists-when-object-expected, only auto-wrap when the model has exactly one list field whose name you can guess; otherwise the validation error is more honest.
- Schema injection MUST be at the end of the prompt; some models pay more attention to the last instructions.
