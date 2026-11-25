---
name: gemini-prompting
description: Internal guidance for composing Gemini 2.5 Pro/Flash prompts for coding, review, diagnosis, and research tasks inside the Gemini Claude Code plugin
user-invocable: false
---

# Gemini 2.5 Prompting Guide for Coding Tasks

Reference document for writing effective prompts when delegating to Gemini 2.5 Pro or Flash. Covers model selection, thinking mode, context window use, structured output, tool use, and antipatterns.

---

## Model Selection

Choose based on task complexity and cost tolerance:

| Model | Use when | Context | Thinking |
|---|---|---|---|
| `gemini-2.5-pro` | Complex architecture, cross-file refactors, SWE-bench-style tasks, novel algorithm design | 1M tokens | Always on (128–32,768 tokens, default dynamic) |
| `gemini-2.5-flash` | Production tasks with good cost/quality balance: reviews, summaries, data extraction, chat | 1M tokens | Dynamic by default (0–24,576 tokens, can disable) |
| `gemini-2.5-flash-lite` | High-volume, low-cost: classification, routing, simple translation, triage | 1M tokens | Off by default (512–24,576 tokens) |

**Decision rule:** Default to Flash for most coding assistance. Switch to Pro only when Flash produces shallow or incorrect reasoning on complex multi-step problems. Use Flash-Lite only when cost is the primary constraint and quality requirements are low.

**SWE-bench data point:** Gemini 2.5 Pro scores ~63.8% on SWE-bench Verified with a custom agent setup — comparable to frontier models for real-world GitHub issue resolution.

---

## Thinking Mode (Budget Tokens)

Gemini 2.5 models have an internal reasoning phase ("thinking") before responding. You control how many tokens it can spend reasoning.

### How to configure (Gemini API)

```python
# Python SDK
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Refactor this authentication module...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=8192  # or -1 for dynamic, or 0 to disable
        )
    )
)
```

### Token budget ranges

| Model | Min | Max | Default |
|---|---|---|---|
| gemini-2.5-pro | 128 | 32,768 | Dynamic (cannot disable) |
| gemini-2.5-flash | 0 | 24,576 | Dynamic (-1) |
| gemini-2.5-flash-lite | 512 | 24,576 | 0 (disabled) |

### When to use each level

**Disable (budget=0) or minimal:**
- Simple lookups: "What does this function return?"
- Mechanical transforms: format conversion, renaming, boilerplate
- Single-file edits with clear instructions
- When latency is critical

**Medium (512–4096 tokens):**
- Standard code review requests
- "Explain why this is slow"
- Bug diagnosis with provided stack trace
- Multi-file but clearly scoped changes

**High (8192–32,768 tokens) or dynamic (-1):**
- Complex algorithm design or optimization
- Architectural planning across a full codebase
- Debugging non-obvious failures with multiple possible causes
- Code migration or refactoring with implicit constraints
- Writing Python web apps with auth ("verified code generation")

**Cost warning:** High thinking budgets cost significantly more. One practitioner reported auto-mode costing ~37x more than flash-only mode for identical workloads ($6k vs $163/month at scale). Match thinking budget to actual task complexity.

---

## Prompt Structure for Coding Tasks

### The canonical structure

```
[Role/persona — optional but effective]

[Context: what exists, what matters]

[Task: specific, scoped, explicit]

[Constraints: what NOT to do, style rules]

[Output format: how to structure the response]
```

### Role setting works well with Gemini

Gemini responds well to role framing. Set it in the system prompt or at the start:

```
You are a senior Go engineer specializing in performance-critical systems.
You follow idiomatic Go, prefer composition over inheritance, and always
handle errors explicitly rather than panicking.
```

### Task decomposition

Break large tasks into sequential prompts. Do not cram multi-phase work into one prompt.

**Bad:**
```
Refactor the authentication module, add rate limiting, write tests,
and update the API documentation.
```

**Good (4 separate prompts):**
1. "Refactor the auth module. Preserve the existing interface exactly."
2. "Add rate limiting middleware. Wire it after the auth middleware."
3. "Write unit tests for the rate limiter. Cover the burst and sustained rate cases."
4. "Update the API docs for the two new rate-limiting headers."

### Explicit negation — critical for Gemini

Gemini's most common failure mode: "I Know Better" syndrome — it fixes unrelated code you didn't ask it to touch. Always state what NOT to do:

**Bad:**
```
Refactor this function to be more efficient.
```

**Good:**
```
Refactor this function for efficiency. 
DO NOT change the function signature.
DO NOT modify the input validation logic.
DO NOT add or remove comments.
DO NOT change error return types.
```

### Architecture-first, then implementation

For complex features, establish the design before writing code:

```
Before writing any code, describe the architecture for adding webhook
support to this service. Cover: data model changes, handler design,
retry strategy, and failure modes. I'll confirm the approach before
you implement.
```

### Incremental generation for large features

For anything generating hundreds of lines, do it in stages:

```
Generate the HTML structure for the dashboard component first.
Stop after the HTML. I'll review it before we proceed to CSS and JS.
```

---

## Context Window Strategy (1M tokens)

### What to include

- All files directly relevant to the task (source, not compiled output)
- Configuration files that affect behavior (tsconfig, pyproject, etc.)
- Interface/type definitions that the code must satisfy
- Existing tests that encode the expected behavior
- The specific error message, stack trace, or failing test output

### What to exclude

Aggressively filter before passing a repo:

| Exclude | Reason |
|---|---|
| `*.csv`, `*.json` data files | No semantic value for code tasks |
| `*.svg`, `*.png`, static assets | Not code |
| `*_test.py`, `test_*.py` | Unless understanding tests is the goal |
| `*.lock`, `*.sum` files | Noise |
| `node_modules/`, `.venv/`, `dist/` | Never include |
| Comments + whitespace | Compress with tools like `yek` or `repomix` |

**Filtering workflow for large repos:**
1. Assess token count: `repomix --output-show-line-numbers`
2. Remove irrelevant file types via ignore patterns
3. Target subdirectory relevant to the task
4. Exclude test directories if not needed
5. Strip comments as final step

**Practical reality:** 1M tokens = ~30,000 lines of code. Most real projects that need full context fit within this after filtering. For repos that genuinely exceed 1M tokens even after filtering, use RAG or chunk by subdirectory.

### Query placement in long-context prompts

**Always put your question/task AFTER the context, not before.**

```
[All code/documents here]

---

Given the above codebase, identify all places where database connections
are not properly closed on error paths.
```

Google's official guidance: "the model's performance will be better if you put your query at the end of the prompt."

### Multiple-needle limitation

Gemini handles single-query retrieval well (up to 99% accuracy) but performance degrades when searching for multiple independent facts simultaneously. For multi-part questions, ask them sequentially rather than in one prompt.

### Context caching (API)

For repeated queries over the same large context (e.g., a full codebase you're asking multiple questions about), use context caching to avoid re-sending the same tokens:

```python
# Cache the codebase context, then query multiple times
cached_content = client.caches.create(
    model="gemini-2.5-pro",
    contents=[large_codebase_content],
    ttl="3600s"
)
# Subsequent queries reuse the cache, costing much less
```

### Context degradation warning

Despite the 1M token window, **reliability drops after ~200K tokens** in practice. If you notice Gemini forgetting earlier instructions, reinserting bugs it already fixed, or contradicting itself: start a fresh session. Use "checkpoint messages" to hand off state between sessions.

---

## Code-Specific Prompting Patterns

### Code review

```
Review this diff for: (1) correctness issues, (2) error handling gaps,
(3) performance concerns. Focus on the changed lines only.
Flag issues by severity: CRITICAL / WARNING / SUGGESTION.
Do not suggest style changes.

[diff here]
```

### Bug diagnosis

```
This test is failing with the following output. Identify the root cause.
Do not propose a fix yet — explain the cause first.

Test: [test name]
Error: [full stack trace]
Relevant code: [paste the relevant functions]
```

### Codebase analysis

```
I'm sharing my project's codebase. Analyze its structure and identify:
1. Architectural issues (coupling, violation of single responsibility)
2. Missing error handling
3. Inconsistencies in naming or patterns

Organize findings by severity. Do not suggest new features.

[codebase here]
```

### Targeted refactor

```
Refactor the `processPayment` function in payments/processor.go.

Goal: reduce cyclomatic complexity from ~18 to below 10.

Constraints:
- Do not change the function signature
- Do not change behavior — existing tests must still pass
- Do not modify other functions
- Preserve all existing error types

Show the refactored function only, not the entire file.
```

### Legacy code migration

```
Migrate this Python 2 module to Python 3.10+.

Rules:
- Use f-strings, not .format()
- Replace print statements with logging module
- Replace unicode() with str()
- Do not change the public API
- Add type hints to all function signatures

[module code]
```

---

## Structured Output

### Use the API's native schema support — do not rely on prompt tricks

"Please respond in JSON format" is fragile. Use `response_schema` instead:

```python
import typing_extensions as typing

class CodeIssue(typing.TypedDict):
    file: str
    line: int
    severity: typing.Literal["critical", "warning", "suggestion"]
    description: str
    suggestion: str

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=review_prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=list[CodeIssue],
    ),
)
```

### Schema design guidelines

- Use `description` fields on every property — they directly improve extraction accuracy
- Mark fields as `required` when they must always be present
- Use `enum` for fixed value sets (severity levels, categories)
- Keep schemas focused: 5–10 properties is better than 20
- Complex schemas (long enums, deep nesting, many optional fields) cause errors

### Known limitation: tool calls + structured output

When there are tool calls in the message history, structured output fails for Gemini 2.5 models (works in 2.0). If you need both tool use and structured output in the same session, collect tool results first, then make a final structured-output request with the results injected as context.

### For classification tasks, use `text/x.enum`

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"Classify this bug: {bug_description}",
    config=types.GenerateContentConfig(
        response_mime_type="text/x.enum",
        response_schema={"enum": ["null_pointer", "race_condition", "off_by_one", "type_error", "other"]},
    ),
)
```

---

## Tool Use / Function Calling

### Mode selection

```python
tool_config = types.ToolConfig(
    function_calling_config=types.FunctionCallingConfig(
        mode="AUTO"   # Model decides — best default for coding agents
        # mode="ANY"  # Always calls a function — use for strict pipelines
        # mode="NONE" # No function calls — use for pure text generation
    )
)
```

### Writing effective function descriptions

The quality of your function description directly determines call accuracy:

**Bad:**
```python
{"name": "read_file", "description": "Read a file"}
```

**Good:**
```python
{
    "name": "read_file",
    "description": "Read the full contents of a file at the given path. "
                   "Use this when you need to examine existing code before "
                   "making changes. Returns the file contents as a string.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Absolute or relative path to the file, e.g. 'src/auth/handler.go'"
            }
        },
        "required": ["path"]
    }
}
```

### Key implementation rules

- Limit active tool set to 10–20 functions; more degrades reliability
- Use enums over open strings for fixed value sets
- For Gemini 3 models: keep temperature at default 1.0 — lowering it below 1.0 causes looping
- For Gemini 2.5 models: temperature 0.0–0.2 for deterministic tool calls
- Always check `finishReason` in the response to detect failed tool call attempts
- In multi-turn conversations with Gemini 3: preserve `thought_signature` fields intact
- Validate high-consequence calls (file deletion, deploys) with the user before execution

### Parallel function calling

Gemini can call multiple independent functions in a single turn. Design your tool set to enable this: independent operations (read file A, read file B) should be separate tools, not one combined tool.

---

## Temperature Settings

| Task type | Temperature |
|---|---|
| Code generation / editing | 0.0–0.2 |
| Code review / analysis | 0.2–0.4 |
| Technical documentation | 0.4–0.7 |
| Default / general purpose | 1.0 |
| Creative / exploratory design | 1.5–2.0 |

**Gemini 3 exception:** Google strongly recommends keeping temperature at the default 1.0 for Gemini 3 models. Setting it below 1.0 may cause looping or degraded performance, especially with function calling.

---

## Antipatterns

### 1. Vague task + no constraints

**Symptom:** Gemini rewrites things you didn't ask it to change, adds unsolicited comments, "improves" unrelated code.

**Fix:** Be hyper-explicit about scope. State what to do AND what not to do.

### 2. Multi-objective single prompt

**Symptom:** One objective is addressed well; others are shallow or ignored.

**Fix:** One prompt, one task. Chain prompts sequentially.

### 3. No output format specification

**Symptom:** Asked for JSON, got prose. Asked for a list, got paragraphs.

**Fix:** Specify format explicitly in the prompt. For machine-readable output, use the API's `response_schema`.

### 4. Injecting the whole repo without filtering

**Symptom:** Slow, expensive responses; model focuses on irrelevant files; hits context degradation.

**Fix:** Filter to relevant files before passing context. Exclude data files, lock files, assets, test directories if not relevant.

### 5. Assuming context persists reliably past 200K tokens

**Symptom:** Instructions from early in a long session are forgotten; fixed bugs reappear.

**Fix:** Start fresh sessions. Use checkpoint messages. For long tasks, pass only what's needed per turn.

### 6. Using prompt tricks for structured output

**Symptom:** "Respond in JSON" works until it doesn't — random markdown fences, extra text, malformed output.

**Fix:** Use `response_mime_type="application/json"` + `response_schema` via the API.

### 7. Overconstrained schema for structured output

**Symptom:** API returns errors on complex schemas.

**Cause:** Very long property names, large enums, deeply nested objects, many optional fields.

**Fix:** Simplify schema. Split into multiple smaller schemas if needed.

### 8. Maxing out thinking budget for every request

**Symptom:** Latency and cost spike without meaningful quality improvement on simple tasks.

**Fix:** Use `thinking_budget=0` for simple queries, `-1` (dynamic) for general use, high values only for genuinely complex tasks.

### 9. Conflicting or contradictory instructions

**Symptom:** Unpredictable behavior, partial compliance.

**Fix:** Review the prompt for contradictions before sending. Place critical instructions at the beginning (system prompt) and reinforce at the end for long prompts.

### 10. Not asking Gemini to explain its reasoning for debugging

**Symptom:** Gemini gives you wrong code and you don't know why.

**Fix:** Ask for reasoning before implementation: "Before writing code, explain your approach and what assumptions you're making." Review the thought process in AI Studio when unexpected results occur.

---

## Differences from Claude Prompting

| Dimension | Gemini 2.5 | Claude |
|---|---|---|
| Context volume | Handles massive contexts (1M tokens); put query at the end | Also strong at long context; query placement less critical |
| Constraint following | Requires explicit "DO NOT" statements; tends to over-help | Follows complex constraint lists more reliably |
| System prompt depth | Benefits from role + scope + format specified upfront | Handles 2000-word system prompts with 15+ constraints reliably |
| JSON output | Native schema support preferred over prompt instructions | Both work; Claude more reliable from prompt alone |
| Temperature for function calling | 0.0–0.2 for 2.5; 1.0 for Gemini 3 | 0.0–0.3 generally safe |
| Thinking/reasoning | Explicit budget control (0 to 32K tokens) | Extended thinking with budget_tokens parameter |
| Codebase tasks | Excellent with full repo in context, but filter aggressively | Strong at cross-file reasoning; explicit about which files to read |
| Unsolicited changes | Common antipattern — needs explicit scope constraints | Less prone to modifying unrequested code |

**Where Gemini excels:** massive codebase analysis, multimodal (code + screenshots), research-style tasks requiring broad synthesis.

**Where Claude excels:** following long complex constraint lists, consistent behavior across long conversations, precise surgical edits.

---

## Quick Reference: Prompt Templates

### Code review
```
Review this code for correctness, security, and performance issues.
Severity levels: CRITICAL | WARNING | SUGGESTION.
Do not comment on style or formatting.

[code]
```

### Bug fix
```
Fix the bug described below. 
DO NOT change anything outside the broken function.
DO NOT refactor or clean up unrelated code.

Bug: [description]
Error: [error message / stack trace]

[relevant code]
```

### Feature implementation
```
You are a [language] engineer following [project conventions].

Implement [feature] in [file/module].

Requirements:
- [requirement 1]
- [requirement 2]

Constraints:
- DO NOT modify the existing public API
- Follow the patterns used in [reference file]
- Add error handling consistent with the existing code

Return only the changed file(s), not a full explanation.
```

### Architecture review
```
Analyze the architecture of this codebase. Identify:
1. Tight coupling between components
2. Missing abstractions
3. Violation of single responsibility
4. Any patterns that will make the system hard to test or extend

Do not suggest new features. Focus on structural issues only.

[codebase]
```

---

## Sources

- [Gemini API — Thinking documentation](https://ai.google.dev/gemini-api/docs/thinking)
- [Gemini API — Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Gemini API — Long context](https://ai.google.dev/gemini-api/docs/long-context)
- [Gemini API — Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Vertex AI — Thinking configuration](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking)
- [Vertex AI — Structured output](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output)
- [Google Cloud Blog — Gemini 2.5 GA](https://cloud.google.com/blog/products/ai-machine-learning/gemini-2-5-flash-lite-flash-pro-ga-vertex-ai)
- [Medium — Best Practices for Prompt Engineering with Gemini 2.5 Pro](https://medium.com/google-cloud/best-practices-for-prompt-engineering-with-gemini-2-5-pro-755cb473de70)
- [Medium — Think Fast, Think Smart: Optimizing Gemini 2.5 Pro with Thinking Budgets](https://medium.com/google-cloud/think-fast-think-smart-optimizing-gemini-2-5-pro-with-thinking-budgets-d1347bb49b5c)
- [Medium — Optimize your prompt size for long context window LLMs](https://medium.com/google-cloud/optimize-your-prompt-size-for-long-context-window-llms-0a5c2bab4a0f)
- [Arsturn — Common Gemini 2.5 Pro Coding Mistakes](https://www.arsturn.com/blog/common-gemini-2-5-pro-coding-mistakes-and-how-to-fix-them)
- [PromptBuilder — Claude vs ChatGPT vs Gemini prompting](https://promptbuilder.cc/blog/claude-vs-chatgpt-vs-gemini-best-prompt-engineering-practices-2025)
- [Firebase — Generate structured output](https://firebase.google.com/docs/ai-logic/generate-structured-output)
- [DEV.to — Gemini 2.5 Pro: A Developer's Guide](https://dev.to/brylie/gemini-25-pro-a-developers-guide-to-googles-most-advanced-ai-53lf)
