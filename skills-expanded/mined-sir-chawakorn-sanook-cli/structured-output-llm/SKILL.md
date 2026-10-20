---
name: structured-output-llm
description: Gets machine-parseable JSON out of an LLM reliably — prefer provider-enforced grammar (OpenAI `response_format:{type:"json_schema",strict:true}`, Anthropic tool-calling / `tool_choice:{type:"tool"}`, Gemini `responseSchema`) over a "respond in JSON" prompt, define the contract once as a Pydantic/Zod model and validate every response (never trust the string), use constrained decoding / grammars for open weights (Outlines, llguidance, llama.cpp GBNF, vLLM `guided_json`), keep schemas SHALLOW with required fields + enums + `additionalProperties:false`, and build a repair-and-retry loop that handles refusals, `length`/`max_tokens` truncation, and streaming partial JSON (`partial-json-parser`). Schema-guided generation eliminates parse-error retries; validate-and-repair is the backstop, not the primary mechanism.
when_to_use: You need a model to emit JSON/objects a program consumes — extraction, classification into fixed labels, function arguments, form-filling, or feeding output into another service — and string-parsing or regex on free text keeps breaking. Distinct from prompt-engineering (crafts the instruction/few-shot prose; this skill enforces the output SHAPE via grammar+validation) and agent-tool-mcp-builder (defines the tools/MCP an agent decides to call; this skill is the one-shot "make THIS call return a typed object" half, even when implemented via a single forced tool).
---

## When to Use

Reach for this skill when a program — not a human — consumes the model's output and the shape must be guaranteed:

- "Extract these 8 fields from this invoice/email as JSON I can `JSON.parse`"
- "Classify into one of {refund, dispute, question} — give me just the label"
- "The model returns ```json fences / prose / trailing commas and my parse breaks ~3% of the time"
- "Function arguments come back malformed or with hallucinated keys"
- "Fill this form schema" / "map this text to my DB row"
- "Open-weights model won't reliably produce valid JSON"
- "Long extraction gets cut off mid-object" or "streaming JSON is unparseable until complete"

NOT this skill:
- Writing the *instruction*, few-shot examples, role/system prompt, or chain-of-thought prose → prompt-engineering (it shapes WHAT to say; this skill enforces the machine SHAPE of the reply)
- Defining tools/an MCP server an agent autonomously selects among across many turns → agent-tool-mcp-builder (this skill is one forced, schema-constrained call returning a typed object)
- Reliability of the whole LLM app — timeouts, fallbacks, circuit-breakers, idempotency around the call → harden-llm-app-reliability (this skill owns only the output-shape contract)
- Token/latency/cost tuning, caching, model selection → optimize-llm-cost-latency (note: strict schemas cost a cache miss on first use — that skill weighs it)
- Stopping a malicious payload in retrieved/user text from hijacking the model → defend-llm-prompt-injection (orthogonal; a valid-schema output can still be adversarial content)
- Retrieval/chunking/grounding that feeds the prompt → rag-pipeline (this skill structures rag's *output* step)
- Scoring whether the extracted values are *correct* across a dataset → llm-eval-harness (this skill guarantees parseable; that one measures accuracy)
- Validating ordinary user-submitted form data (no LLM) → build-form-validation
- The wire/serialization contract between your own services → rest-graphql-contract
- Scraping the HTML/DOM the text came from → scrape-structured-web-data

## Steps

1. **Prefer provider-enforced schema over a "respond in JSON" prompt — it's a different mechanism, not a stronger hint.** A prompt is a request the model may ignore (fences, preamble, extra keys); enforced schema masks the decoder's token logits so only schema-valid tokens are emittable — invalid JSON becomes *impossible*, not just unlikely. Use the strongest enforcement the provider offers:

   | Provider | Enforcement | How |
   |---|---|---|
   | **OpenAI** (gpt-4o+, gpt-4.1, o-series) | Structured Outputs, 100% guaranteed | `response_format:{type:"json_schema",json_schema:{name,schema,strict:true}}` — or `strict:true` on a function tool |
   | **Anthropic Claude** | Tool-calling (no native json_schema) | define one tool with `input_schema`, set `tool_choice:{type:"tool",name:"..."}` to force it; read `tool_use.input` |
   | **Google Gemini** | Controlled generation | `generationConfig:{responseMimeType:"application/json",responseSchema:{...}}` (also supports `responseSchema` enums) |
   | **Azure OpenAI** | same as OpenAI | `response_format` json_schema on `2024-08-01-preview`+ |
   | **Open weights** (vLLM/TGI/llama.cpp/Ollama) | Constrained decoding (step 5) | `guided_json` / GBNF grammar / Outlines |

   `json_object` mode (the older `{type:"json_object"}`) only guarantees *syntactically* valid JSON, NOT your schema — treat it as a weak fallback, never the goal.

2. **Define the contract ONCE as a typed model; let the SDK emit the schema and parse the result.** Don't hand-write JSON Schema and a parser separately — they drift. Use the model class as the single source of truth:
   - **Python** → Pydantic v2. OpenAI: `client.beta.chat.completions.parse(..., response_format=MyModel)` → `.choices[0].message.parsed` is a typed instance (or `.refusal`). Or `MyModel.model_validate_json(raw)`.
   - **TS/JS** → Zod + the OpenAI helper `zodResponseFormat(MySchema, "name")`, then `completion.choices[0].message.parsed`; or `MySchema.parse(JSON.parse(raw))`. (Instructor / `instructor-js` wrap this with retries.)
   - **Anthropic** → derive `input_schema` from Pydantic via `Model.model_json_schema()` and pass as the tool's input_schema; validate `tool_use.input` back through the model.
   The rule: **validate every response through the typed model even when the provider guarantees the schema** — guarantees cover JSON-schema-expressible constraints, not your business invariants (date ranges, cross-field rules, enum-of-enums), and self-hosted/fallback paths have no guarantee at all.

3. **Keep the schema SHALLOW and tight — depth and looseness are where models fail and where strict mode rejects you.** Constraints that materially improve reliability:
   - **`required` everything + `additionalProperties:false`.** OpenAI strict mode *requires* every property be in `required` and forbids additional props — model "optional" as `required` + nullable union (`{"type":["string","null"]}`). This also blocks hallucinated keys.
   - **Enums over free strings for categories** (`"type":"string","enum":["refund","dispute","question"]`) — turns classification into a closed set the decoder can't escape.
   - **Flatten.** Prefer a flat object or a top-level `{"items":[...]}` array wrapper over 4-level nesting. Deep/recursive schemas raise latency, hit provider depth/property caps (OpenAI: ≤5000 props, ≤5 nesting for strict), and degrade accuracy.
   - **Avoid where unsupported:** OpenAI strict mode disallows `minLength`/`maximum`/`pattern`/`format` and many keywords — enforce those in step 2's validator, not the wire schema. (Anthropic/Gemini tolerate more but don't *guarantee* them.)
   - **Order fields so reasoning precedes the answer:** put a `reasoning`/`evidence` string field *before* the `answer`/`label` field — the model generates them in order, so it "thinks" before committing (cheap, schema-native CoT).

4. **Don't ask for JSON and reasoning in the same free-text turn.** If you need chain-of-thought, either (a) put it inside the schema as a leading field (step 3), or (b) do a two-call split: one reasoning call (free text), one extraction call (strict schema) over the reasoning. Mixing "think step by step, then output JSON" in one un-enforced response is the classic source of prose-before-the-brace parse failures.

5. **For open-weights / self-hosted, use constrained decoding (grammar-level), not prompting.** These enforce validity at the token sampler:

   | Tool | Use | Invoke |
   |---|---|---|
   | **vLLM** | production serving | `guided_json=<schema>` / `guided_choice=[...]` / `guided_regex` in `extra_body` (backed by xgrammar/outlines) |
   | **Outlines** | library, any HF model | `outlines.generate.json(model, PydanticModel)` → returns typed object |
   | **llguidance / xgrammar** | fast grammar engines | embedded in vLLM/TGI; sub-ms per-token masking |
   | **llama.cpp / Ollama** | local GGUF | GBNF grammar file, or `format:"json"`+schema (Ollama) |
   | **TGI** | HF Inference | `grammar:{type:"json",value:<schema>}` |

   Constrained decoding makes invalid JSON *structurally impossible*. Caveat: an over-tight grammar can force the model down an unnatural path and *lower content* quality (it'll fill a required field with junk rather than refuse) — keep the grammar permissive on values, strict on structure, and still validate semantics in step 2.

6. **Build repair-and-retry as the BACKSTOP for paths with no hard guarantee.** Even guaranteed providers can return refusals or truncation; self-hosted/`json_object` paths can emit broken JSON. Ladder:
   1. **Salvage first (no LLM call):** strip ```` ```json ```` fences and any pre/post prose; extract the outermost balanced `{...}`/`[...]`; libraries: `json-repair` (py), `jsonrepair` (js) fix trailing commas/single quotes/unescaped newlines. Cheap, deterministic — try before re-prompting.
   2. **Re-prompt with the error:** on `ValidationError`, send the broken output + the exact validator message back ("Your previous reply failed validation: `<pydantic error>`. Return ONLY valid JSON matching the schema.") — Instructor's `max_retries` does exactly this. Cap at **2–3 attempts**; a 4th rarely converges.
   3. **Feed the schema again** in the repair turn; models drift from it across long contexts.

7. **Handle refusals, truncation, and length explicitly — they are NOT parse errors and must not be "repaired" into garbage.**
   - **Refusal:** OpenAI returns `message.refusal` (non-null) instead of `parsed`; Anthropic may emit a text block, not the forced tool. Branch on it — surface to the user/safety path, don't retry-loop into the rate limit.
   - **Truncation:** check `finish_reason == "length"` (OpenAI) / `stop_reason == "max_tokens"` (Anthropic) → the JSON is cut mid-object and is *un*-repairable by salvage. Fix the cause: raise `max_tokens`, shrink the schema/array, or paginate the extraction — don't json-repair a truncated object (it'll silently drop fields).
   - **Empty/whitespace:** treat as failure, retry once, then fail loud.

8. **Streaming structured output — buffer or parse incrementally, never `JSON.parse` mid-stream.** A partial stream `{"name":"Al` is invalid JSON. Two correct patterns:
   - **Simplest:** accumulate all deltas, parse once on `finish`. Use when you don't need live UI.
   - **Incremental:** `partial-json-parser` (js) / `pydantic` partial / OpenAI's streamed-parse helpers / `jsonriver` to coerce the buffer into a valid partial object on each delta for live rendering. For tool-calls, concatenate `tool_call.function.arguments` deltas across chunks (they arrive fragmented) and parse only when the tool-call completes.

9. **Verify.** (a) Round-trip: 100+ live calls on representative inputs → 100% deserialize into the typed model with zero `JSON.parse`/`ValidationError`; assert in CI against a recorded/replayed set. (b) Schema-escape probe: feed adversarial inputs that tempt the model to add commentary or a key — confirm `additionalProperties:false` + strict mode still yields clean objects. (c) Edge branches: force a refusal (policy-tripping input) and a truncation (tiny `max_tokens`) and assert each hits its dedicated branch, not the JSON repairer. (d) Enum closure: classification only ever returns a member of the enum. (e) Open-weights: same round-trip on the self-hosted path with constrained decoding ON, then OFF — confirm the constraint is what's carrying validity. Done = the program never sees a string it can't parse into the typed model, categories are closed enums, refusals/truncation route to their own branches, repair is rare (a metric you watch, not the load-bearing path), and the typed model — not the wire schema — is the single source of the contract.
