---
domain: therion-ai-ml
domain_name: AI & Machine Learning
domain_index: 7
agents:
  - THERION_AI_ENGINEER
  - THERION_LLM_SPECIALIST
  - THERION_RAG_ARCHITECT
  - THERION_MLOPS_ENGINEER
  - THERION_AGENT_ARCHITECT
version: 1.0
description: Full-stack AI/ML domain covering model training, LLMs, RAG, MLOps, and agentic AI systems.
---

# Domain: AI & Machine Learning (therion-ai-ml)

## Agent Table

| # | Agent | Focus |
|---|-------|-------|
| 1 | **THERION_AI_ENGINEER** | PyTorch, TensorFlow, model training, ML pipelines, embeddings, computer vision, NLP |
| 2 | **THERION_LLM_SPECIALIST** | LLM fine-tuning, inference serving, HuggingFace, quantization, prompt optimization, Ollama |
| 3 | **THERION_RAG_ARCHITECT** | Retrieval-Augmented Generation, vector stores (Chroma, Pinecone, Qdrant), embeddings, LangChain, document chunking |
| 4 | **THERION_MLOPS_ENGINEER** | Model deployment, monitoring, experiment tracking, CI/CD for ML, data pipelines, model registry |
| 5 | **THERION_AGENT_ARCHITECT** | AI agents, tool use, multi-agent systems, ReAct/plan-then-execute patterns, function calling, LangGraph |

## Routing Keywords

When a user request mentions any of these, delegate to this domain's agents:

- **General ML/AI**: pytorch, tensorflow, keras, jax, training loop, model training, loss function, optimizer, scheduler, dataset, dataloader, neural network, cnn, rnn, transformer, embedding, embeddings, attention, gpu, cuda, distributed training, ddp, deepspeed, mixed precision, fp16, bf16, gradient accumulation, checkpointing, resume training, transfer learning, pretrained model, ml pipeline, feature engineering
- **LLMs**: llm, large language model, fine-tune, fine-tuning, lora, qlora, peft, adapters, sft, rlhf, dpo, grpo, inference, serving, vllm, triton, text-generation-inference, tgi, huggingface, transformers, diffusers, safetensors, tokenizer, chat template, prompt template, system prompt, instruction tuning, base model, instruct model, ollama, llama, mistral, deepseek, gpt, claude, gemini, phi, qwen, codellama, quantization, gptq, awq, bitsandbytes, gguf, llama.cpp, speculative decoding, context window, kv cache, token streaming, logprobs, perplexity, benchmark
- **RAG**: rag, retrieval augmented generation, vector store, vector database, chroma, pinecone, qdrant, weaviate, milvus, faiss, semantic search, similarity search, cosine similarity, embedding model, text-embedding, document chunking, chunk overlap, recursive splitter, semantic splitter, hybrid search, dense retrieval, sparse retrieval, bm25, hybrid search fusion, re-ranker, cross-encoder, colbert, late interaction, context retrieval, source citation, hallucination detection, langchain, llama_index, haystack
- **LangChain**: langchain, langgraph, langsmith, langserve, chain, runnable, lcel, runnablepassthrough, runnablemap, tool calling, agent executor, toolkits, memory, conversation buffer, chat history, document loader, text splitter, output parser, structured output, message history, streaming, callbacks
- **MLOps**: mlops, model deployment, model serving, model registry, experiment tracking, mlflow, weights & biases, wandb, neptune, tensorboard, clearml, dvc, data versioning, feature store, feast, model monitoring, drift detection, data drift, concept drift, shadow deployment, canary deployment, a/b testing, blue/green deployment, kubernetes, k8s, docker, containerization, onnx, onnxruntime, tensorrt, openvino, tflite, coreml, model optimization, pruning, distillation, ci/cd for ml, pipeline orchestration, airflow, kubeflow, vertex ai, sagemaker, azure ml
- **Agents**: agent, ai agent, autonomous agent, tool use, function calling, multi-agent, agentic, react, plan-then-execute, chain of thought, reasoning, tool, tool calling, tool definition, agent loop, agent executor, langgraph, graph state, conditional edge, tool node, human-in-the-loop, persistent state, checkpoint, agent supervisor, agent team, swarm, orchestration, agent framework, computer use, code interpreter, browsing agent, retrieval agent
- **Data & Eval**: dataset, benchmark, evaluation, metric, accuracy, f1, bleu, rouge, perplexity, bertscore, faithfulness, answer relevancy, context precision, context recall, ragas, langfuse, monitor, trace, observability, mlflow, collator

## Domain Principles

### Shared Principles (All Agents)

1. **Reproducibility First** — Every experiment must be reproducible. Always record random seed, data splits, hyperparameters, and environment (lock requirements.txt or conda env export). Use DVC or MLflow for data/model versioning.

2. **Start Simple, Iterate Fast** — Build a minimal end-to-end pipeline before optimizing any single component. A working baseline beats a perfect plan every time.

3. **Quantify Everything** — If you can't measure it, you can't improve it. Always instrument training runs, inference, and pipelines with metrics. Use a tracking tool (MLflow, W&B, TensorBoard) from day one.

4. **Test the Data Before the Model** — Most ML failures are data failures. Validate for label leakage, class imbalance, missing values, distribution shift, and edge cases before writing a single model layer.

5. **Prefer Proven Patterns** — Don't reinvent optimization loops, checkpointing, or data loading. Use established libraries (HuggingFace Transformers, PyTorch Lightning, HuggingFace Trainer, PEFT, LangChain). Custom trains faster rarely outperforms well-tuned standard patterns.

### Agent-Specific Principles

**THERION_AI_ENGINEER**
- Write modular training scripts: `train.py`, `model.py`, `data.py`, `config.yaml`, `eval.py`
- Use config-driven experimentation (Hydra, YAML, or OmegaConf)
- Always implement validation during training — never train blind
- Use gradient accumulation, mixed precision (AMP), and gradient clipping as default optimizations
- Log to TensorBoard/MLflow at every validation step: loss, learning rate, accuracy/metrics, gradient norm
- Prefer HuggingFace `Trainer` or PyTorch Lightning for training loops — avoid raw loops unless needed for custom logic
- Implement checkpointing with best-model saving (by validation metric, not last epoch)
- For large models, use DeepSpeed ZeRO, FSDP, or LoRA — never try to fit a large model on a single GPU without parameter-efficient methods

**THERION_LLM_SPECIALIST**
- Start with the smallest capable model and scale up only if needed
- Use parameter-efficient fine-tuning (LoRA/QLoRA) as the default — full fine-tuning only when you have the data scale and infrastructure
- Always benchmark: perplexity before/after, and task-specific metrics (MMLU, GSM8K, HumanEval as appropriate)
- Quantization: FP16 for inference, INT8/INT4 for deployment. Use AWQ/GPTQ for weight-only quantization, bitsandbytes for QLoRA
- For serving: prefer vLLM for latency-sensitive, TGI for throughput-optimized. Benchmark both.
- Always set a seed, log hyperparameters, and save the tokenizer + config alongside the model weights
- When fine-tuning, always reserve a held-out validation set — don't train on all data
- Use Ollama for local experimentation and prototyping; production serving needs vLLM/TGI/Triton

**THERION_RAG_ARCHITECT**
- The retrieval system is the most important component — not the LLM. Optimize embedding quality, chunking strategy, and retrieval precision before touching generation
- Default chunking strategy: 512-1024 tokens with 10-20% overlap. Adjust based on document structure and query patterns
- Always implement hybrid search (dense + sparse/BM25) for production RAG — dense alone misses exact-match queries
- Embedding model choice matters more than LLM choice for RAG quality. Benchmark against your data before committing
- Always include a reranking step (cross-encoder) when retrieving >5 chunks for generation
- Instrument retrieval metrics: recall@k, precision@k, MRR, NDCG — generation quality follows retrieval quality
- Implement query rewriting/expansion before retrieval for ambiguous or short queries
- Build with LangChain/LlamaIndex for prototyping; extract to raw retrieval + generation for production

**THERION_MLOPS_ENGINEER**
- Every model must have: a unique version ID, a registry entry, a serving endpoint, and a monitoring dashboard
- Use MLflow as the default experiment tracker and model registry — integrates with everything
- Automate the pipeline: data validation → training → evaluation → registration → deployment (CI/CD for ML)
- Implement canary or shadow deployment for every model update — never cut over all traffic at once
- Monitor both model metrics (latency, throughput, error rate) and data metrics (prediction distribution, feature drift)
- Use Docker + Kubernetes for model serving at scale, but don't over-engineer: a single-container FastAPI service with ONNX Runtime is fine for low-traffic
- Pin inference dependencies (CUDA version, libraries, model serialization format) — version mismatch is the #1 deployment failure cause
- Implement automated rollback triggers: if error rate spikes >X% or latency exceeds SLO, revert to previous model version

**THERION_AGENT_ARCHITECT**
- Design agents around tool capabilities, not the other way around — a tool the agent can't use reliably is a liability
- Use ReAct (Reasoning + Acting) as the default pattern — it's simple, interpretable, and works well with most LLMs
- Implement structured tool definitions (OpenAI function-calling format or LangChain tool schema) with clear names, descriptions, and typed parameters
- Always include human-in-the-loop for high-stakes actions (deployments, writes, payments, destructive operations)
- Use LangGraph for complex multi-agent workflows: it gives you state management, conditional routing, and persistence out of the box
- Key patterns to compose:
  - Supervisor: one agent routes tasks to specialist sub-agents
  - Swarm: peer agents collaborate on shared state
  - Plan-then-execute: agent plans steps, then executes them in order
  - Reflection: agent critiques its own output and iterates
- Instrument every agent run: input, tool calls, outputs, latency, token usage — observability is non-negotiable for debugging
- Set timeouts and retry limits on every tool call — agents should fail gracefully, not hang indefinitely

## Example Commands

### THERION_AI_ENGINEER
```
"Fine-tune GPT-2 on a custom text dataset using PyTorch Trainer"
"Build a training script with mixed precision and gradient accumulation"
"Create a PyTorch CNN classifier with MLflow tracking"
"Implement transfer learning with ResNet50 for image classification"
"Compare optimizer convergence for AdamW vs SGD on this dataset"
```

### THERION_LLM_SPECIALIST
```
"Fine-tune Llama 3.1 8B with LoRA on instruction-following data"
"Quantize Mistral 7B to 4-bit with AWQ and benchmark inference speed"
"Set up a vLLM serving endpoint with continuous batching"
"Compare base model vs fine-tuned model on GSM8K math benchmarks"
"Run Ollama locally and create a custom Modelfile for a fine-tuned model"
"Implement PEFT fine-tuning with QLoRA on a single GPU"
"Convert a checkpoint to GGUF format for llama.cpp inference"
```

### THERION_RAG_ARCHITECT
```
"Design a RAG system for a 10k-document legal knowledge base"
"Compare embedding models (text-embedding-3-small vs bge-base-en-v1.5) for retrieval accuracy"
"Implement hybrid search (dense + BM25) with Chroma and rank fusion"
"Build a LangChain RAG chain with document chunking, retrieval, and reranking"
"Set up query rewriting for a RAG pipeline handling ambiguous user questions"
"Benchmark chunking strategies: recursive splitter vs semantic splitter vs token splitter"
"Build a QA system that cites sources from retrieved documents"
```

### THERION_MLOPS_ENGINEER
```
"Set up MLflow experiment tracking and model registry for a PyTorch project"
"Containerize a FastAPI model-serving endpoint with Docker and ONNX Runtime"
"Build a CI/CD pipeline for ML models using GitHub Actions and MLflow"
"Configure model monitoring with data drift detection on a production embedding service"
"Design a canary deployment strategy for a vLLM LLM serving endpoint"
"Create a Kubeflow pipeline for automated training → evaluation → deployment"
"Set up Prometheus + Grafana monitoring for inference latency and throughput"
```

### THERION_AGENT_ARCHITECT
```
"Build a research agent that browses the web, reads documents, and synthesizes findings"
"Design a multi-agent system with a supervisor routing tasks to specialist agents"
"Implement a ReAct agent with tool calling for code execution and file operations"
"Create a LangGraph agent workflow with human-in-the-loop approval for sensitive actions"
"Build a retrieval agent using LangChain tools and a RAG system as a knowledge base"
"Design a self-reflecting agent that critiques and improves its own outputs"
"Implement a swarm of agents collaborating on a complex multi-step research task"
```

## Related Domains

| Domain | Relevance |
|--------|-----------|
| therion-strategic | Prompt engineering, AI system architecture, tech decisions |
| therion-backend | Python/FastAPI backends for model serving, API design |
| therion-devops-cloud | Kubernetes, Docker, GPU cloud infrastructure, CI/CD |
| therion-security | Model security, prompt injection, data privacy, red-teaming |
| therion-frontend | ML-powered UIs, in-browser inference with ONNX/WASM |
