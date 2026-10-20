# Anthropic Cookbook — Recipe Library

Production-quality code guides and Jupyter notebooks for building with Claude. Covers capabilities, tool use, multimodal input, agentic patterns, Managed Agents, Claude Agent SDK, evals, skills, and third-party integrations.

**Source:** `anthropics/anthropic-cookbook` (public)
**Local clone:** `/home/user/anthropics/anthropic-cookbook`
**API key required:** yes — `ANTHROPIC_API_KEY`

---

## Section Index

### Capabilities (`capabilities/`)

| Directory | Guide | What it covers |
|-----------|-------|----------------|
| `classification/` | `guide.ipynb` | Text and data classification techniques, vector DB eval |
| `content_moderation/` | `guide.ipynb` | Content moderation pipeline with evaluation harness |
| `contextual-embeddings/` | `guide.ipynb` | Contextual RAG with embeddings; Lambda/S3 adapters |
| `knowledge_graph/` | `guide.ipynb` | Knowledge graph extraction from unstructured text |
| `retrieval_augmented_generation/` | `guide.ipynb` | Full RAG pipeline with retrieval and end-to-end evals |
| `summarization/` | `guide.ipynb` | Summarization with BLEU/ROUGE/LLM eval |
| `text_to_sql/` | `guide.ipynb` | Natural language → SQL with test suite |

---

### Tool Use (`tool_use/`)

| Notebook | What it covers |
|----------|----------------|
| `calculator_tool.ipynb` | Basic tool definition and calling |
| `customer_service_agent.ipynb` | Multi-tool customer service agent |
| `extracting_structured_json.ipynb` | Structured JSON extraction via tools |
| `tool_choice.ipynb` | Forcing specific tool selection |
| `parallel_tools.ipynb` | Parallel tool execution |
| `programmatic_tool_calling_ptc.ipynb` | Programmatic tool calling (PTC) |
| `tool_use_with_pydantic.ipynb` | Pydantic models as tool input schemas |
| `tool_search_with_embeddings.ipynb` | Dynamic tool selection via embeddings |
| `tool_search_alternate_approaches.ipynb` | Alternate tool search strategies |
| `memory_cookbook.ipynb` | Persistent memory with tools |
| `context_engineering/context_engineering_tools.ipynb` | Context engineering via tools |
| `automatic-context-compaction.ipynb` | Automatic context window compaction |
| `threat_intel_enrichment_agent.ipynb` | Threat intel enrichment agent |
| `vision_with_tools.ipynb` | Vision + tool use combined |

---

### Agentic Patterns (`patterns/agents/`)

| Notebook | Pattern |
|----------|---------|
| `basic_workflows.ipynb` | Prompt chaining, routing, parallelization |
| `orchestrator_workers.ipynb` | Orchestrator → worker multi-agent |
| `evaluator_optimizer.ipynb` | Eval-then-optimize loop |
| `async_multi_agent_orchestration.ipynb` | Async parallel multi-agent orchestration |

---

### Claude Agent SDK (`claude_agent_sdk/`)

Full notebooks for building production agents with the Claude Agent SDK (Managed Agents platform).

| Notebook | Agent / Pattern |
|----------|----------------|
| `00_The_one_liner_research_agent.ipynb` | Minimal research agent in one line |
| `01_The_chief_of_staff_agent.ipynb` | Chief-of-staff agent with financial/HR tools |
| `02_The_observability_agent.ipynb` | Agent with observability/logging hooks |
| `03_The_site_reliability_agent.ipynb` | SRE incident responder with MCP tools |
| `04_migrating_from_openai_agents_sdk.ipynb` | OpenAI Agents SDK → Claude migration guide |
| `05_Building_a_session_browser.ipynb` | Session browser / inspector UI |
| `06_The_vulnerability_detection_agent.ipynb` | Security vulnerability detection agent |
| `07_Hosting_the_agent.ipynb` | Hosting on Modal / Kubernetes |
| `08_Dynamic_workflows.ipynb` | Dynamic runtime workflow construction |
| `scheduled_repository_reviewer/` | Cron-triggered repo review agent |

---

### Managed Agents (`managed_agents/`)

Patterns for the Managed Agents (Claude Managed Agents / CMA) platform.

| Notebook | Pattern |
|----------|---------|
| `CMA_cap_session_spend.ipynb` | Cap per-session spend |
| `CMA_consult_an_advisor.ipynb` | Advisor agent consulted by main agent |
| `CMA_coordinate_specialist_team.ipynb` | Coordinator + specialist team |
| `CMA_explore_unfamiliar_codebase.ipynb` | Codebase exploration agent |
| `CMA_gate_human_in_the_loop.ipynb` | Human-in-the-loop approval gate |
| `CMA_iterate_fix_failing_tests.ipynb` | Test-fix iteration loop |
| `CMA_operate_in_production.ipynb` | Production operations agent |
| `CMA_orchestrate_issue_to_pr.ipynb` | Issue → PR orchestration |
| `CMA_pin_inference_geo.ipynb` | Pin inference to a geographic region |
| `CMA_plan_big_execute_small.ipynb` | Plan at high level, execute in small steps |
| `CMA_prompt_versioning_and_rollback.ipynb` | Prompt versioning and rollback |
| `CMA_remember_user_preferences.ipynb` | Per-user memory with MemoryStores |
| `CMA_use_skills_from_a_repo.ipynb` | Use skills registered in a repo |
| `CMA_verify_with_outcome_grader.ipynb` | Agent self-verification with grader |
| `CMA_watch_subagents_live.ipynb` | Live subagent observation |
| `CMA_with_mongodb_atlas.ipynb` | CMA + MongoDB Atlas integration |
| `data_analyst_agent.ipynb` | Data analyst agent |
| `slack_data_bot.ipynb` | Slack data bot via managed agent |
| `sre_incident_responder.ipynb` | SRE incident responder |
| `linear/` | Linear issue agent |
| `roadtrip_planner/` | Road trip planner |
| `sentry/` | Sentry triage agent |
| `slack/` | Slack webhook bridge |
| `self_hosted_sandboxes/` | Self-hosted Docker sandboxes |
| `cma-mcp/` | CMA + MCP server integration |

---

### Multimodal (`multimodal/`)

| Notebook | What it covers |
|----------|----------------|
| `getting_started_with_vision.ipynb` | Image input basics |
| `best_practices_for_vision.ipynb` | Image sizing, quality, resolution tips |
| `reading_charts_graphs_powerpoints.ipynb` | Interpreting charts, graphs, and slides |
| `how_to_transcribe_text.ipynb` | OCR / form extraction |
| `crop_tool.ipynb` | Dynamic crop tool for zooming into images |
| `using_sub_agents.ipynb` | Vision sub-agent orchestration |

---

### Skills (`skills/`)

Notebooks and utilities for building, registering, and using Claude Code skills programmatically.

| Item | What it covers |
|------|----------------|
| `notebooks/01_skills_introduction.ipynb` | Skills overview and API |
| `notebooks/02_skills_financial_applications.ipynb` | Financial skills: DCF, ratio analysis |
| `notebooks/03_skills_custom_development.ipynb` | Building custom skills |
| `custom_skills/analyzing-financial-statements/` | Financial statement analyzer |
| `custom_skills/applying-brand-guidelines/` | Brand guidelines enforcer |
| `custom_skills/creating-financial-models/` | DCF + sensitivity analysis |
| `skill_utils.py` | Utility functions for skill operations |
| `file_utils.py` | File handling utilities |

---

### Misc (`misc/`)

| Notebook | What it covers |
|----------|----------------|
| `prompt_caching.ipynb` | Prompt caching with `cache_control` |
| `batch_processing.ipynb` | Message Batches API |
| `building_evals.ipynb` | Automated eval construction with Claude |
| `generate_test_cases.ipynb` | Generating test cases for evals |
| `how_to_enable_json_mode.ipynb` | Reliable JSON output |
| `how_to_make_sql_queries.ipynb` | Text-to-SQL |
| `building_moderation_filter.ipynb` | Content moderation filter |
| `pdf_upload_summarization.ipynb` | PDF upload + summarization |
| `read_web_pages_with_haiku.ipynb` | Web page reading with Haiku |
| `admin_api.ipynb` | Admin API usage |
| `using_citations.ipynb` | Citations feature |
| `metaprompt.ipynb` | Metaprompting: Claude writing prompts |
| `session_memory_compaction.ipynb` | Session memory and compaction |
| `speculative_prompt_caching.ipynb` | Speculative prompt caching |
| `sampling_past_max_tokens.ipynb` | Sampling beyond max_tokens |

---

### Extended Thinking (`extended_thinking/`)

`extended_thinking.ipynb` — enable extended thinking, budget tokens, streaming thinking blocks.

### Cost Optimization (`cost_optimization/`)

`cost_optimization.ipynb` — checklist-driven optimization: measure pass rate + cost per task, find the Pareto-optimal model/configuration.

### Evals (`evals/`)

`agentic_search/reproduce_agentic_search_benchmarks.ipynb` — reproduce agentic search benchmarks; includes eval harness utilities.

### Tool Evaluation (`tool_evaluation/`)

`tool_evaluation.ipynb` — evaluate Claude's tool calling accuracy.

### Coding (`coding/`)

`prompting_for_frontend_aesthetics.ipynb` — prompting strategies for generating aesthetic frontend code.

### Observability (`observability/`)

`usage_cost_api.ipynb` — track API usage and cost programmatically.

### Fable 5 (`fable_5_fallback_billing/`)

Fallback billing patterns for Fable 5 deployments.

---

### Third-Party Integrations (`third_party/`)

| Integration | Notebooks |
|-------------|-----------|
| **LlamaIndex** | Basic RAG, Multi-Document Agents, Multi-Modal, ReAct Agent, Router Query Engine, SubQuestion Query Engine |
| **Pinecone** | RAG with Pinecone, Claude 3 RAG agent |
| **MongoDB** | RAG with MongoDB Atlas |
| **Deepgram** | Prerecorded audio transcription |
| **ElevenLabs** | Low-latency STT + Claude + TTS; streaming voice assistant |
| **WolframAlpha** | LLM API integration |
| **Wikipedia** | Wikipedia search tool |

---

## Setup

```bash
cd /home/user/anthropics/anthropic-cookbook
pip install anthropic jupyter
export ANTHROPIC_API_KEY=sk-ant-...
jupyter notebook
```

---

## Prompts

### Explore a capability guide

```
Open /home/user/anthropics/anthropic-cookbook/capabilities/[topic]/guide.ipynb.
Walk through the notebook step by step and explain each pattern.
```

### Adapt a Managed Agents pattern

```
Using /home/user/anthropics/anthropic-cookbook/managed_agents/[notebook].ipynb:
Adapt the [pattern] for [use case].
Key requirements: [list them].
```

### Study agentic patterns

```
Using /home/user/anthropics/anthropic-cookbook/patterns/agents/:
Explain the orchestrator-workers, evaluator-optimizer, and async multi-agent patterns
with code examples from the notebooks.
```

### Build a Claude Agent SDK agent

```
Using /home/user/anthropics/anthropic-cookbook/claude_agent_sdk/[notebook].ipynb:
Build a [use-case] agent following the same pattern.
Show the agent initialization, tool definitions, and session management.
```

### Run the cost optimization checklist

```
Using /home/user/anthropics/anthropic-cookbook/cost_optimization/cost_optimization.ipynb:
Run the optimization checklist for [agent/task].
Measure pass rate and cost per task at each configuration and find the Pareto-optimal setup.
```
