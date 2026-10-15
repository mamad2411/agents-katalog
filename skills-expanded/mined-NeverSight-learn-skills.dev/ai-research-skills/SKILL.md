---
name: ai-research-skills
description: >
  Comprehensive AI research skills library (86 skills, 22 categories) enabling AI agents to
  autonomously conduct end-to-end AI research — from ideation and literature survey through
  model training, evaluation, and paper writing. Orchestrates the full research lifecycle via
  the autoresearch skill. Use when conducting ML/AI research experiments, fine-tuning LLMs,
  running distributed training, optimizing inference, building RAG pipelines, or writing
  research papers. Triggers on: ai research, autoresearch, fine-tuning, GRPO, vLLM, LoRA,
  RLHF, distributed training, mechanistic interpretability, megatron, llama, ml experiments,
  research agent, train model, run benchmark, inference optimization, ml paper.
allowed-tools: Bash Read Write Edit Glob Grep
metadata:
  tags: ai-research, ml, autoresearch, fine-tuning, distributed-training, inference, rlhf, grpo, vllm, rag, multimodal, mlops
  version: "1.0"
  source: Orchestra-Research/AI-Research-SKILLs
  keyword: ai-research-skills
  platforms: Claude Code, Codex CLI, Gemini CLI, OpenCode, Cursor
  license: MIT
---

# AI Research Skills

> **86 skills powering autonomous AI research in 2026**
>
> Keyword: `ai-research-skills` · `autoresearch` · `ml experiments`
> Source: [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | Fork: [akillness/AI-Research-SKILLs](https://github.com/akillness/AI-Research-SKILLs)

---

## When to use this skill

- Conducting autonomous AI/ML research from idea to paper
- Fine-tuning LLMs with Axolotl, LLaMA-Factory, PEFT, or Unsloth
- Running post-training (RLHF, GRPO, DPO, SimPO, verl)
- Distributed training with Megatron-Core, DeepSpeed, FSDP, or Accelerate
- Optimizing inference with vLLM, TensorRT-LLM, llama.cpp, or SGLang
- Building RAG pipelines (Chroma, FAISS, Pinecone, Qdrant)
- Mechanistic interpretability with TransformerLens, SAELens, pyvene
- Writing ML papers (LaTeX templates for NeurIPS, ICML, ICLR, ACL)
- Running ML benchmarks and evaluations (lm-eval-harness, BigCode, NeMo Evaluator)
- Multimodal tasks: CLIP, Whisper, LLaVA, Stable Diffusion, SAM

## Do not use this skill when

- You need a simple code fix unrelated to ML/AI research
- You want general software engineering workflows (use `omg`, `bmad`, or `ralph` instead)

---

## Overview: 86 Skills × 22 Categories

| Category | Count | Key Skills |
|----------|-------|------------|
| **Autoresearch** | 1 | Autonomous research orchestration (central layer) |
| Model Architecture | 5 | LitGPT, Mamba, RWKV, NanoGPT, TorchTitan |
| Fine-Tuning | 4 | Axolotl, LLaMA-Factory, PEFT, Unsloth |
| Post-Training | 8 | TRL, GRPO, OpenRLHF, SimPO, verl, slime, miles, torchforge |
| Distributed Training | 6 | DeepSpeed, FSDP, Accelerate, Megatron-Core, Lightning, Ray Train |
| Optimization | 6 | Flash Attention, bitsandbytes, GPTQ, AWQ, HQQ, GGUF |
| Inference & Serving | 4 | vLLM, TensorRT-LLM, llama.cpp, SGLang |
| RAG | 5 | Chroma, FAISS, Pinecone, Qdrant, Sentence Transformers |
| Multimodal | 7 | CLIP, Whisper, LLaVA, BLIP-2, SAM, Stable Diffusion, AudioCraft |
| Mech Interp | 4 | TransformerLens, SAELens, pyvene, nnsight |
| Safety & Alignment | 4 | Constitutional AI, LlamaGuard, NeMo Guardrails, Prompt Guard |
| Evaluation | 3 | lm-eval-harness, BigCode, NeMo Evaluator |
| MLOps | 3 | W&B, MLflow, TensorBoard |
| Agents | 4 | LangChain, LlamaIndex, CrewAI, AutoGPT |
| Prompt Engineering | 4 | DSPy, Instructor, Guidance, Outlines |
| Observability | 2 | LangSmith, Phoenix |
| Infrastructure | 3 | Modal, Lambda Labs, SkyPilot |
| Data Processing | 2 | NeMo Curator, Ray Data |
| Tokenization | 2 | HuggingFace Tokenizers, SentencePiece |
| Emerging Techniques | 6 | MoE, Model Merging, Long Context, Speculative Decoding, Distillation, Pruning |
| ML Paper Writing | 1 | LaTeX templates (NeurIPS, ICML, ICLR, ACL, AAAI, COLM) |
| Ideation | 2 | Research Brainstorming, Creative Thinking |

---

## Instructions

### Step 1: Install the library

```bash
# Interactive installer (auto-detects Claude Code, Codex, Gemini, Cursor)
npx @orchestra-research/ai-research-skills

# Install all 86 skills non-interactively
npx @orchestra-research/ai-research-skills install --all

# Or use the install script from this skill
bash scripts/install.sh
```

After installation, **restart your agent session** so skills are loaded.

### Step 2: Start autonomous research (autoresearch)

For full autonomous research (idea → experiments → paper):

```
Read the autoresearch SKILL.md and follow its instructions to begin.
```

The autoresearch skill orchestrates:
1. Literature survey and ideation
2. Experiment design and execution (routes to domain skills)
3. Results synthesis and benchmarking
4. Paper writing with LaTeX templates

### Step 3: Use domain skills directly

For targeted work on a specific framework, call the skill by keyword:

```bash
# Fine-tuning
fine-tune with axolotl   # → activates axolotl skill

# Post-training / RLHF
run grpo training        # → activates GRPO skill

# Inference optimization
optimize with vllm       # → activates vLLM skill

# Distributed training
setup deepspeed          # → activates DeepSpeed skill
```

### Step 4: Claude Code marketplace (alternative install)

```bash
# Add marketplace
/plugin marketplace add orchestra-research/AI-research-SKILLs

# Install by category
/plugin install fine-tuning@ai-research-skills
/plugin install post-training@ai-research-skills
/plugin install inference-serving@ai-research-skills
/plugin install distributed-training@ai-research-skills
/plugin install optimization@ai-research-skills
```

### Step 5: Update or manage skills

```bash
# Update all installed skills
npx @orchestra-research/ai-research-skills update

# List installed skills
npx @orchestra-research/ai-research-skills list
```

---

## Autonomous Research Loop

The autoresearch skill uses a **two-loop architecture**:

```
Outer Loop (Synthesis):
  ↓ Research question → Literature survey → Hypothesis
  ↓ Route to domain skills
Inner Loop (Optimization):
  ↓ Run experiment → Collect results → Analyze → Adjust
  ↑ Ratchet improvements via git
  ↓ Synthesize findings → Write paper
```

This enables fully autonomous overnight GPU experiments (Karpathy-style ratchet via git).

---

## Examples

### Example 1: Start autonomous research

```
Activate ai-research-skills.
Read the autoresearch SKILL.md and begin research on:
"Does LoRA training stability correlate with layer-wise norm heterogeneity?"
```

The agent will: survey literature → design experiments → fine-tune with LoRA → run benchmarks → analyze results → write paper.

### Example 2: Fine-tune Llama 3 with LoRA

```
Use the fine-tuning skill (axolotl) to fine-tune Llama-3.1-8B with LoRA
on my dataset at ./data/train.jsonl with 4-bit quantization.
```

### Example 3: Optimize inference with vLLM

```
Set up vLLM for serving Mistral-7B with tensor parallelism on 2 GPUs,
with continuous batching and PagedAttention. Target: <50ms TTFT.
```

### Example 4: Run GRPO post-training

```
Implement GRPO training for my reward model using TRL.
Dataset: ./data/preferences.json. Base: Llama-3.1-8B-Instruct.
```

---

## Architecture: Skill Structure

Each of the 86 skills follows this structure:
```
skill-name/
├── SKILL.md          # Expert guidance (200–600 lines)
├── references/       # Official docs, API refs, GitHub issues, release notes
│   ├── README.md
│   ├── api.md
│   ├── tutorials.md
│   ├── issues.md     # Real GitHub issues with solutions
│   └── releases.md
├── scripts/          # Helper scripts (optional)
└── templates/        # Code templates (optional)
```

---

## Best practices

1. **Start with autoresearch** — it routes to the right domain skills automatically
2. **Restart after install** — skills load at session start; restart if newly installed skills aren't recognized
3. **Use the two-loop architecture** — let the inner loop optimize, outer loop synthesize
4. **Reference real GitHub issues** — each skill's `references/issues.md` contains battle-tested solutions
5. **Combine with oh-my-gods orchestration** — use `ralph` for persistence, `bmad` for structured phases, `survey` for landscape scanning before research

---

## Integration with oh-my-gods

| oh-my-gods skill | Integration |
|-----------------|-------------|
| `survey` | Pre-research landscape scan before launching autoresearch |
| `ralph` | Persistent loop — keep autoresearch running until paper complete |
| `bmad` | Structured phases for the research lifecycle |
| `autoresearch` | Native skill within this library (enhanced) |

---

## References

- [GitHub: Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)
- [GitHub: akillness/AI-Research-SKILLs](https://github.com/akillness/AI-Research-SKILLs) (fork)
- [Orchestra Research](http://orchestra-research.com)
- [npm: @orchestra-research/ai-research-skills](https://www.npmjs.com/package/@orchestra-research/ai-research-skills)
- [Blog: AI Research Skills](https://www.orchestra-research.com/perspectives/ai-research-skills)
- [Slack Community](https://join.slack.com/t/orchestrarese-efu1990/shared_invite/zt-3iu6gr8io-zJvpkZTPToEviQ9KFZvNSg)
