---
name: domain-nlp-llm
description: "Use for text / NLP / LLM tasks: text classification, sentiment, NER/token tagging, QA, summarization, translation, semantic search / embeddings, retrieval-augmented generation (RAG), chatbots/agents, and fine-tuning language models. Picks prompt vs fine-tune vs RAG, the right model, and rigorous text evaluation. Triggers on 'classify text', 'sentiment', 'NER', 'summarize', 'chatbot', 'RAG', 'embeddings', 'fine-tune LLM', 'question answering'."
---

# NLP / LLM - Method Selection

First decide the *cheapest approach that works*: prompt, then RAG, then fine-tune, in that order of effort.

## Decision table
| Sub-task | Recommended | Notes |
|---|---|---|
| Text classification / sentiment | **Fine-tune DeBERTa-v3 / RoBERTa** (or a strong LLM few-shot if data is tiny) | Encoder models are cheap, strong, and fast for fixed label sets. |
| NER / token tagging | **DeBERTa/RoBERTa token-classification** | Span-level F1; watch tokenizer alignment. |
| Semantic search / dedup / clustering | **Sentence-embeddings (e5 / BGE / GTE)** + vector index | Cosine similarity; evaluate with retrieval metrics. |
| Knowledge Q&A over your docs | **RAG** (embed + retrieve + LLM answer) | Prefer RAG over fine-tuning for factual/updatable knowledge. |
| Summarize / rewrite / extract / generate | **Instruction-tuned LLM (prompted)** | Start with prompting + few-shot; structured output via schema. |
| Domain adaptation of an LLM | **LoRA/QLoRA fine-tune** | Parameter-efficient; only after prompting/RAG proves insufficient. |
| Chatbot / tool-use agent | **LLM + tools/function-calling**, RAG for grounding | Define tools crisply; add guardrails. |

## Choosing prompt vs RAG vs fine-tune
- **Prompt / few-shot**: fastest; use when the base model can already do it with instructions.
- **RAG**: when the model lacks *knowledge* (private/updatable facts). Fixes hallucination better than fine-tuning.
- **Fine-tune (LoRA)**: when you need a *behavior/format/style* the base model won't follow, or a cheap specialized classifier. Not for injecting facts.

## Rigor
- **Split leakage**: dedup near-duplicate texts; split by **document/author/time**, not random sentences. For RAG, keep eval questions out of the indexed corpus if testing generalization.
- **Metrics**: classification uses F1/AUC (macro for imbalance); generation uses task metrics plus **LLM-as-judge with a rubric** plus human spot-checks; retrieval uses recall@k / nDCG; QA uses exact-match/F1 plus faithfulness/groundedness.
- **Robustness**: check prompt sensitivity, class imbalance, and demographic/topic subgroups.
- Improve: use `accuracy-improvement-loop` (better retriever, hard-negative mining, better chunking, ensemble/judge, fine-tune last).
