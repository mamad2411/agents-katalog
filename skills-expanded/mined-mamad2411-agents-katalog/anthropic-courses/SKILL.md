# Anthropic Courses — Educational Curriculum

Five sequential courses teaching Claude API development from first principles through production-grade tool use. Jupyter notebooks with hands-on exercises.

**Source:** `anthropics/courses` (public)
**Local clone:** `/home/user/anthropics/courses`
**API key required:** yes — `ANTHROPIC_API_KEY`
**Preferred model:** Claude 3 Haiku (cost-efficient for students; substitute any Claude model)

---

## Recommended Learning Order

| # | Course | What it covers |
|---|--------|----------------|
| 1 | `anthropic_api_fundamentals` | SDK setup, message format, models, parameters, streaming, vision |
| 2 | `prompt_engineering_interactive_tutorial` | Comprehensive prompting techniques (interactive exercises) |
| 3 | `real_world_prompting` | Prompting in complex, real-world use cases |
| 4 | `prompt_evaluations` | Writing production-grade prompt evals |
| 5 | `tool_use` | End-to-end tool use implementation |

---

## Course 1 — Anthropic API Fundamentals (`anthropic_api_fundamentals/`)

| Notebook | What it covers |
|----------|----------------|
| `01_getting_started.ipynb` | API key setup, first `client.messages.create` call, reading the response |
| `02_messages_format.ipynb` | The messages array, roles (user/assistant), multi-turn conversation structure |
| `03_models.ipynb` | Available Claude models, capability vs. cost tradeoffs, choosing the right model |
| `04_parameters.ipynb` | `max_tokens`, `temperature`, `top_p`, `top_k`, `stop_sequences` — what each does |
| `05_Streaming.ipynb` | Streaming responses with `stream=True`, processing delta events in real time |
| `06_vision.ipynb` | Sending images (base64 + URL), multimodal prompts, image understanding patterns |

---

## Course 2 — Prompt Engineering Interactive Tutorial (`prompt_engineering_interactive_tutorial/`)

Two variants of the same curriculum:

| Variant | Path |
|---------|------|
| Anthropic 1P | `prompt_engineering_interactive_tutorial/Anthropic 1P/` |
| Amazon Bedrock | `prompt_engineering_interactive_tutorial/AmazonBedrock/` |

Covers: being clear and direct, building complex prompts, avoiding hallucination, role prompting, formatting outputs, chain-of-thought, few-shot examples, long-context tasks.

AWS Workshop version: https://catalog.us-east-1.prod.workshops.aws/workshops/0644c9e9-5b82-45f2-8835-3b5aa30b1848/en-US

---

## Course 3 — Real World Prompting (`real_world_prompting/`)

| Notebook | What it covers |
|----------|----------------|
| `01_prompting_recap.ipynb` | Recap of core prompting techniques before applying them |
| `02_medical_prompt.ipynb` | Medical domain prompt — precise, safe, structured outputs |
| `03_prompt_engineering.ipynb` | Applying multiple techniques together in a single prompt |
| `04_call_summarizer.ipynb` | Summarizing call transcripts with structured extraction |
| `05_customer_support_ai.ipynb` | Full customer support agent with routing, tone, and escalation |

Google Vertex version: https://github.com/anthropics/courses/tree/vertex/real_world_prompting

---

## Course 4 — Prompt Evaluations (`prompt_evaluations/`)

| Directory | What it covers |
|-----------|----------------|
| `01_intro_to_evals/` | What evals are, why they matter, designing an eval harness |
| `02_workbench_evals/` | Running evals in the Anthropic Console Workbench |
| `03_code_graded_evals/` | Writing code-based graders (exact match, regex, schema validation) |
| `04_code_graded_classification_evals/` | Eval harness for classification tasks with accuracy metrics |
| `05_prompt_foo_code_graded_animals/` | PromptFoo integration — code-graded animal classification |
| `06_prompt_foo_code_graded_classification/` | PromptFoo for arbitrary classification prompt evaluation |
| `07_prompt_foo_custom_graders/` | Writing custom PromptFoo grader functions |
| `08_prompt_foo_model_graded/` | Using a model as the eval judge (LLM-as-a-judge pattern) |
| `09_custom_model_graded_prompt_foo/` | Custom model graders inside PromptFoo pipelines |

---

## Course 5 — Tool Use (`tool_use/`)

| Notebook | What it covers |
|----------|----------------|
| `01_tool_use_overview.ipynb` | Tool use architecture: defining tools, the API request/response cycle |
| `02_your_first_simple_tool.ipynb` | Building and calling your first tool end to end |
| `03_structured_outputs.ipynb` | Using tools to force structured JSON output from Claude |
| `04_complete_workflow.ipynb` | Full agentic loop: Claude calls tool → results fed back → final answer |
| `05_tool_choice.ipynb` | Forcing a specific tool (`tool_choice`), auto vs. any vs. tool |
| `06_chatbot_with_multiple_tools.ipynb` | Multi-turn chatbot with several tools, tool selection logic |

---

## Setup

```bash
cd /home/user/anthropics/courses
pip install anthropic jupyter
export ANTHROPIC_API_KEY=sk-ant-...
jupyter notebook
```

---

## Prompts

### Work through API fundamentals

```
Open /home/user/anthropics/courses/anthropic_api_fundamentals/ and walk me through
notebooks 01–06 in order. For each, explain the concept and show a minimal runnable example.
```

### Study a specific prompting technique

```
Using /home/user/anthropics/courses/prompt_engineering_interactive_tutorial/Anthropic 1P/:
Explain [technique] with the notebook's examples and give me a template I can adapt.
```

### Build a real-world prompt

```
Using /home/user/anthropics/courses/real_world_prompting/[notebook].ipynb:
Help me adapt the [use case] prompt for [my domain].
Key constraints: [list them].
```

### Design an eval suite

```
Using /home/user/anthropics/courses/prompt_evaluations/:
Design a [code-graded / model-graded] eval for my [classification / generation] prompt.
Expected inputs: [describe]. Success criteria: [describe].
```

### Implement tool use

```
Using /home/user/anthropics/courses/tool_use/:
Build a [use case] that requires [N] tools.
Walk through the tool definition, the agentic loop, and result handling.
```
