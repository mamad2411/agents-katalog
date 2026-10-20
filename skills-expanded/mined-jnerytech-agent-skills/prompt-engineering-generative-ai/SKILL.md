---
name: prompt-engineering-generative-ai
description: "Knowledge base from \"Prompt Engineering for Generative AI: Future-Proof Inputs for Reliable AI Outputs at Scale\" by James Phoenix & Mike Taylor (O'Reilly, 2024). Use when applying the authors' Five Principles of Prompting (Give Direction, Specify Format, Provide Examples, Evaluate Quality, Divide Labor), structured LLM output, LangChain chains, RAG/vector databases, agents with memory and tools, prompt evaluation/A-B testing, or image prompting (Midjourney, Stable Diffusion, ControlNet, DreamBooth) — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Prompt Engineering for Generative AI
**Authors**: James Phoenix & Mike Taylor | **Pages**: ~423 | **Chapters**: 10 | **Generated**: 2026-10-09

> Code and model landscape are from the 2024 edition (OpenAI SDK v1, LangChain 0.1-era imports, GPT-4/3.5, Midjourney v5–6, SD 1.5/SDXL). Learn the patterns; verify current APIs before reusing snippets.

## How to Use This Skill

- **Without arguments** — load the core frameworks below
- **With a topic** — ask about `RAG`, `output parsers`, `ControlNet`, `memory`…; I find and read the relevant chapter
- **With chapter** — ask for `ch05`; I load that chapter file
- **Browse** — ask "what chapters do you have?"

When a question goes beyond the Core Frameworks below, read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### The Five Principles of Prompting (ch01 — the spine of the book)
Model-agnostic conventions that "work for any level of intelligence, biological or artificial". Templates don't transfer between models; principles do. Each fixes one failure mode of a naive prompt:

| Principle | Fixes | Text levers | Image levers |
|---|---|---|---|
| **1. Give Direction** — describe the desired style or reference a persona | Vague direction | Role prompting, "in the style of Steve Jobs", prewarming, rules, retrieved context (RAG) | Art-style modifiers, quality boosters, negative prompts, prompt weights |
| **2. Specify Format** — rules + required structure of the response | Unformatted output | JSON/YAML + parser + retry, "Return only…", output parsers, function calling | Format modifiers ("a stock photo of"), aspect ratio, upscaling |
| **3. Provide Examples** — diverse test cases done correctly | Missing examples | Zero/one/few-shot; 1–3 almost always help; >3–5 trades creativity for reliability | Img2Img / image prompts, ControlNet, DreamBooth |
| **4. Evaluate Quality** — identify errors, rate responses, test what drives performance | Limited evaluation | Blind A/B tests, ground truth, LLM-as-judge, evals, embedding distance | Permutation grids, fixed seeds, X/Y/Z plots, `/shorten` |
| **5. Divide Labor** — split tasks into chained steps | No task division | Chains, CoT, meta prompting, self-evaluation, agents | Inpainting, base+refiner, prompt rewriting, SAM masks |

- **Apply in order of cost**: Direction first (cheapest; evidence it beats examples), then Format, then Examples, while Evaluating throughout; Divide Labor when one prompt can't do it.
- **"Average prompts return average responses."** Every token in the prompt shifts the probability of every generated token.
- **Think of a prompt as a creative brief to an agency**: what context would a human need? Put it in.
- **Direction = style; Format = output type.** When they conflict (or you over-specify), drop the less important one.

### Evaluation is the moat (ch01, ch03, ch04, ch10)
- **Blind prompting → blind A/B testing**: run each variant N times (5–10+), shuffle, rate thumbs-up/down without seeing the prompt, compare mean score by variant. "Usually in less than 10 test runs you uncover a deviation."
- **Programmatic evals beat vibes**: exact match, Levenshtein, embedding distance, `labeled_pairwise_string`; GPT-4 output as ground truth to justify moving to a cheaper/open model.
- **LLM-as-evaluator**: ~10× cheaper than humans — but **evaluate the evaluator** (false positives / negatives on known cases) and run cheap programmatic checks first.
- **Use evaluation to shorten prompts** — untested instructions are often superfluous or harmful.
- **10+ runs per case, across several cases** before trusting a prompt change; escalate to fine-tuning (≥50 samples, beats prompting at a few thousand) or DSPy.

### Structured output (ch03, ch04)
- Ask for JSON/YAML with an example payload + a "You must follow the following principles:" contract ("Only return valid JSON… will be parsed with json.loads()").
- **Prefer YAML** when escaping is a pain; **prefer JSON/YAML over regex** once structure nests.
- Always **parse + validate in code** (typed exceptions, schema checks) and retry/auto-fix on failure.
- In LangChain: **Pydantic output parser** (`get_format_instructions()` + `parse`) or **function calling** (`bind_tools`, `PydanticToolsParser`). LLMs ignore numeric constraints ("10 items", "1000 words") — validate counts.

### Divide Labor patterns (ch01, ch03, ch04, ch06)
- **Chain of Thought** ("Let's think step by step" / "giving the model time to think").
- **Self-evaluation**: the model judges finished output better than it generates it — add a rating/critique call.
- **Meta Prompting**: an LLM writes prompts for another model (LLMs are "human-level prompt engineers").
- **Least to Most**, **Prompt Chaining** (smart model for ideation, cheap model for generation), **Task Decomposition**, **Query Planning** (dependency graph of sub-queries).
- **Document chains** for oversized text: Stuff (small) · Refine (progressive) · Map Reduce (scale, loses order) · Map Re-rank (most confident answer).
- Chains add latency — keep them on server/batch paths.

### Retrieval (RAG) (ch05)
- Pipeline: **chunk → index → search → insert as context** + "use only this context, else say I don't know". RAG = dynamic **Give Direction**.
- Chunking is the craft: budget tokens first (context − prompt/response = k × chunk size), use **recursive splitting with overlap**; huge chunks regress to the mean, tiny ones lose meaning.
- **Metadata strategy is as important as chunking**: filter on it, or let a **Self-Querying retriever** (temperature 0) extract filters.
- Never mix embedding models in one index; persist vectors; test that added context is worth its cost.

### Agents (ch06)
- Agent = **inputs + goal/reward + action space**, plus memory, planning strategy, retrieval for LLMs.
- **OpenAI functions** for one definitive action or parallel calls; **ReAct** for sequential, reflective, multi-tool tasks (use a stop sequence so it doesn't invent tool results).
- **Tool names, descriptions and docstrings are prompts.** Don't overload tools; cap `max_iterations` / `max_execution_time`.
- Memory reads before the run and writes after; pick buffer / window / summary / token-buffer by length and budget.
- **Tree of Thoughts** for search-like problems (Game of 24: 74% vs 4% CoT).

### Image generation (ch07–ch09)
- Prompts are **coordinates in latent space**; image models mirror training data, they don't pursue quality unless asked.
- Start with a **format modifier**; then style (prefer **Meme Unbundling** over naming living artists), quality boosters, `--no`/negative prompts, `::` weights tuned by **grid search**.
- **An image is the strongest example**: Img2Img, ControlNet (structure), DreamBooth (subject, one concept, rare token, 20–30 images).
- Diffusion is **coarse→fine**: prompt editing, ControlNet start/end steps, SDXL refiner switch (0.6 @ 30 steps) exploit it.
- **Use the lowest denoising that works** (hallucinations above ~0.4). Default CFG ~7, DPM++ 2M Karras 20–30 steps.
- Pick by task: DALL-E 3 composition · Midjourney aesthetics · Stable Diffusion control/products.

### Building applications (ch10)
- Audit every prompt against the Five Principles; replace mega-prompts with **a chain of small, testable prompts**.
- Unique output needs unique input: **interview the user for information gain**.
- Spend the expensive model + testing budget on the **strategically hardest step**.
- Ship a **Gradio prototype** first; human feedback is the most valuable eval data.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-five-principles-of-prompting.md) | The Five Principles of Prompting | Five Principles, prewarming, blind A/B testing, permutation prompting, self-evaluation, meta prompting |
| [ch02](chapters/ch02-intro-to-llms.md) | Introduction to LLMs for Text Generation | Token/BPE, transformer & attention, RLHF, model landscape, cross-model comparison |
| [ch03](chapters/ch03-standard-practices-text-generation.md) | Standard Practices for Text Generation with ChatGPT | Lists, JSON/YAML, ELI5, Ask for Context, style unbundling, chunking, Least to Most, role prompting, majority vote, LLM evaluator |
| [ch04](chapters/ch04-advanced-text-generation-langchain.md) | Advanced Text Generation with LangChain | LCEL, output parsers, evals, function calling, query planning, few-shot templates, text splitters, document chains |
| [ch05](chapters/ch05-vector-databases-faiss-pinecone.md) | Vector Databases with FAISS and Pinecone | Embeddings, RAG, chunking strategy, metadata filtering, self-querying, alternative retrievers |
| [ch06](chapters/ch06-autonomous-agents-memory-tools.md) | Autonomous Agents with Memory and Tools | CoT, agent components, ReAct, OpenAI functions, toolkits, memory types, plan-and-execute, ToT, callbacks |
| [ch07](chapters/ch07-intro-diffusion-models.md) | Introduction to Diffusion Models for Image Generation | Diffusion process, latent space, DALL-E vs Midjourney vs Stable Diffusion |
| [ch08](chapters/ch08-standard-practices-image-generation.md) | Standard Practices for Image Generation with Midjourney | Format/style modifiers, negative prompts, weights, Img2Img, inpainting, consistent characters, prompt rewriting, meme unbundling/mapping |
| [ch09](chapters/ch09-advanced-stable-diffusion.md) | Advanced Image Generation with Stable Diffusion | AUTOMATIC1111 weights, prompt editing, Img2Img, SD Upscale, inpainting, ControlNet, SAM, DreamBooth, SDXL refiner |
| [ch10](chapters/ch10-building-ai-powered-applications.md) | Building AI-Powered Applications | Five-Principles audit, AI blog pipeline, expert interview, style optimization by embedding distance, Gradio |

## Topic Index

- **A/B testing (blind)** → ch01, ch10
- **Agent toolkits (CSV, SQL, Pandas)** → ch06
- **Art style modifiers / quality boosters** → ch08
- **Ask for Context** → ch03
- **AUTOMATIC1111 / prompt weights / prompt editing** → ch09
- **CFG, seed, samplers, denoising** → ch07, ch09
- **Chain of Thought / "Let's think step by step"** → ch01, ch03, ch06
- **Chunking (sentence, token, sliding window, recursive)** → ch03, ch04, ch05
- **Classification / sentiment / majority vote** → ch03
- **Consistent characters** → ch08, ch09
- **ControlNet / Segment Anything (SAM)** → ch09
- **Diffusion models / latent space** → ch07
- **Document chains (Stuff, Refine, Map Reduce, Map Re-rank)** → ch04
- **DreamBooth / fine-tuning** → ch09 (LLM fine-tuning: ch01, ch02, ch10)
- **DSPy** → ch10
- **ELI5 / universal translation** → ch03
- **Embeddings / vector databases (FAISS, Pinecone)** → ch05
- **Evals / LLM-as-judge / evaluate the evaluator** → ch01, ch03, ch04
- **Few-shot / example selectors** → ch01, ch03, ch04
- **Function calling / tools / parallel calls** → ch04, ch06
- **Gradio prototyping** → ch10
- **Hallucination avoidance (reference text, citations)** → ch03, ch05
- **Img2Img / inpainting / outpainting / upscaling** → ch08, ch09
- **JSON / YAML output and validation** → ch01, ch03
- **LCEL / runnables** → ch04
- **Least to Most / prompt chaining / task decomposition** → ch03, ch04
- **Memory (STM/LTM, buffer, window, summary)** → ch06, ch10
- **Meme unbundling / meme mapping / style unbundling** → ch03, ch08, ch10
- **Meta prompting / prompt rewriting** → ch01, ch03, ch08, ch10
- **Metadata filtering / self-querying retriever** → ch05
- **Model selection (LLMs / image models)** → ch02, ch07
- **Negative prompts / weighted terms** → ch08, ch09
- **Output parsers (Pydantic)** → ch04, ch10
- **Permutation prompting / X/Y/Z plot / grid search** → ch01, ch08, ch09
- **Plan-and-execute (BabyAGI, AutoGPT) / Tree of Thoughts** → ch06
- **Prewarming / internal retrieval** → ch01
- **Query planning** → ch04
- **RAG** → ch05, ch10
- **ReAct** → ch01, ch06
- **RLHF / transformers / tokens / BPE / tiktoken** → ch02, ch03
- **Role prompting / personas** → ch01, ch03
- **SDXL base + refiner** → ch09
- **Self-evaluation / inner monologue / thinking time** → ch01, ch03
- **Summarization (progressive, map reduce)** → ch01, ch03, ch04

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and patterns (When / How / Trade-offs)
- [cheatsheet.md](cheatsheet.md) — decision rules, thresholds, trade-off tables

---

## Scope & Limits

Covers the book's content only (2024 edition); vendor features, prices, model names and library APIs have moved since. For current Claude/Anthropic API details use the `claude-api` skill; for broader AI-engineering practice see `huyen-ai-engineering` and `ai-agents-and-applications`.
