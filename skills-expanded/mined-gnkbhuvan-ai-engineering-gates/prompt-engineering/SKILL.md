---
name: prompt-engineering
description: |
  Prompt engineering — designing, debugging, evaluating, or chaining a prompt, grounded in
  the Five Principles of Prompting and first-principles reasoning when the task is
  ambiguous. Branches: write or design a new prompt, debug a prompt that's failing,
  evaluate or optimize an existing prompt, apply a named technique (few-shot,
  chain-of-thought, ReAct, tool-use), produce a structured/RAG output format, or build a
  multi-step prompt chain.
---

# Prompt Engineering

Systematic methodology combining the Five Principles of Prompting with architecture-driven
first-principles reasoning to craft, optimize, evaluate, and debug prompts.

## First-Principles Foundation

LLMs are **text completion engines** that mimic the patterns in their training data.
Every prompting decision derives from these axioms:

1. **Mimicry**: The model completes the prompt as if it were a document from its training set. Ask not "how would a reasonable person respond?" but "how would a document that starts like this most likely continue?"
2. **One token at a time**: The model cannot pause, backtrack, or edit. It commits to every token. Thinking aloud (chain-of-thought) is the only mechanism for "reflection."
3. **Left-to-right, single-pass**: Information flows left-to-right only. The model reads the prompt once, top to bottom. Order of content is critical—put instructions before content, context before question.
4. **Mimic the desired pattern**: If you want structured output, the prompt must look like a document that naturally contains structured output. Few-shot examples are the most reliable way to establish a pattern.
5. **Truth bias**: The model assumes its prompt is true. Counterfactual prompts produce counterfactual completions. You are responsible for giving it a correct prompt.
6. **Stay on the trained path** (the "Little Red Riding Hood principle"): a prompt that doesn't resemble any plausible training document confuses the model. Make it look like a real markdown report, code file, or transcript—not a synthetic template only you would write. For fine-tuned models this cuts both ways: look like the fine-tuning documents, and *don't* look like the base model's pre-training documents.
7. **The human test**: if a human expert couldn't complete this exact prompt in a single pass—no backtracking, no scratch paper, no re-reading—don't expect the model to either. Push subtasks that need precision or backtracking (counting, exact lookups, arithmetic) into surrounding code, not the prompt.

**Sanity check before shipping**: read your own fully-assembled prompt once, start to finish. If you can't follow it, the model can't either.

## Before You Write a Prompt: Is Prompting the Right Tool?

| Situation | Use |
|---|---|
| Novel/one-off task, no large example set | Zero-shot or few-shot prompting |
| Stable task, need consistent style/format on top of existing knowledge, 100s-1000s of examples | Few-shot, escalate to LoRA fine-tuning if prompting plateaus |
| Need fresh, private, or frequently-changing facts | RAG (retrieve + inject context)—not fine-tuning |
| Stable task, 1,000s+ labeled examples, volume justifies the up-front cost | Full fine-tuning—starts to beat prompt engineering once you can supply a few thousand examples |
| Task needs genuinely new domain knowledge the base model lacks | Full fine-tuning, not LoRA |

Default to prompting first: it's reversible, has no training cost, and is good enough for most tasks. Escalate only when prompting demonstrably plateaus. Full criteria: `references/llm-architecture.md`.

## Trigger Decision Tree

When the user's request involves an LLM interaction, run this decision tree:

1. **Is the task clear?** If ambiguous, use first-principles questioning (see below) before touching a prompt.
2. **Identify the document type**: Is this an advice conversation, analytic report, structured document (JSON/YAML), or creative output? The document type shapes the entire prompt structure.
3. **Select prompting pattern**: zero-shot, few-shot, chain-of-thought, ReAct, RAG, meta-prompting, least-to-most.
4. **Apply the Five Principles** (in order): Give Direction → Specify Format → Provide Examples → Evaluate Quality → Divide Labor.
5. **Confirm missing details with the user**—gate below; do not write the prompt until it passes.

### When Information Is Missing—First-Principles Questioning

If ANY of the following are unclear, ask the user before proceeding (never guess):

| Missing? | Ask the user |
|----------|-------------|
| Task goal | "What exactly should the output accomplish? What does success look like?" |
| Output format | "What format do you need: plain text, JSON, YAML, bullet list, code block?" |
| Tone/style/persona | "Should this be formal, casual, technical? In the style of any particular role or person?" |
| Examples | "Can you provide 1-3 examples of good outputs?" |
| Constraints | "Any constraints: length, audience, domain, what to avoid?" |
| Context needed | "What background info or retrieved data should the model have?" |
| Evaluation criteria | "How will you judge if the output is good?" |
| Model/deployment context | "Which model? Chat API or completion? What temperature? Any tool access?" |

**Exception—no user to ask**: if the prompt runs at inference time for an end user you can't interrupt, have the *model* request the missing context instead of guessing: append "If you need more context, please specify what would help you make a better decision," and feed the answer back as context on the next turn.

**Gate**: this step is done only when every row above that's actually unclear from context has either been answered by the user or stated out loud as an explicit assumption with no objection. Silently assuming and continuing does not satisfy this — stop and ask instead.

## The Five Principles of Prompting (Apply in Order)

1. **Give Direction** — role, persona, style, or descriptive keywords. Imagine what a human expert would need to know for the task, and include it. Default to more direction, not less.
2. **Specify Format** — state the output structure unambiguously (JSON/YAML/bullets/schema). On conflict between style and format, drop whichever is less important.
3. **Provide Examples** — 2-5 diverse few-shot examples is the reliability sweet spot; push past that and reliability keeps rising while creativity drops. Prefer Direction over Examples when good examples are hard to collect.
4. **Evaluate Quality** — never ship an unevaluated prompt. Start with blind eyeballing; escalate rigor only as stakes rise.
5. **Divide Labor** — split into chained subtasks once a single prompt exceeds ~200 words of instructions or mixes unrelated subtasks.

→ Full techniques, trade-offs, and image-prompting notes: `references/five-principles.md`

## Choosing a Prompting Pattern

| Pattern | When to Use | Key Technique |
|---------|------------|---------------|
| **Zero-shot** | Simple, clear tasks; throwaway interactions | Clear instruction + format specification |
| **Few-shot** | Need reliable output format; pattern matching tasks | 2-5 diverse examples matching target distribution |
| **Chain-of-Thought** | Reasoning, math, logic, multi-step problems | "Let's think step by step." or few-shot CoT with reasoning traces |
| **ReAct** | Tasks requiring tool use, search, or external actions | Interleave Thought→Action→Observation→Thought |
| **RAG** | Tasks needing factual grounding on fresh/private data | Retrieve context → inject into prompt → answer from context only |
| **Role Prompting** | Need specific expertise, tone, or perspective | System message: "You are a [role] with expertise in [domain]." |
| **Meta-Prompting** | Generating prompts for other models (text→image, etc.) | Ask LLM to write a prompt for the target model |
| **Least-to-Most** | Complex compositional problems | Decompose → solve subproblems in order → combine |
| **Self-Eval/Self-Critique** | Quality assurance on outputs | Generate → evaluate against criteria → revise if needed |
| **Tree of Thoughts** | Problems requiring exploration of multiple paths; CoT plateaus | Branch reasoning paths → evaluate each → select best (GPT-4+CoT scores 4% on "Game of 24"; GPT-4+ToT scores 74%—worth the extra cost only when a single linear chain genuinely fails) |
| **Classification** | Categorization tasks | Define categories + few-shot examples per category + majority vote |

→ Full templates, RAG retrieval trade-offs, and worked examples: `references/prompting-patterns.md`

## Prompt Structure (Quick Rules)

The model reads left-to-right, once, top to bottom:

1. **Instructions before content**: put "Summarize the following:" BEFORE the article.
2. **Sandwich technique**: in long prompts, restate the goal once at the start and once again right before the answer. The early-to-mid region of a long prompt—the "Valley of Meh"—gets the least attention; bracket it instead of relying on it.
3. **Examples immediately before the input**: the model best recognizes patterns that appear right before the target.
4. **Dependencies before dependents**: if section B references section A, A must come first.

→ Full anatomy, document types, and content-ranking framework: `references/prompt-assembly.md`

## Deliverables

When delivering prompt work, always provide:

1. **Final prompt** with clear sections labeled (System/User, role, task, constraints, format)
2. **Test cases** (3-5 diverse inputs) and their outputs
3. **Recommended parameters** (model, temperature, max_tokens)
4. **Evaluation results** (accuracy, consistency, failure cases)
5. **Known limitations** and edge cases
6. **Usage instructions** (how to integrate, any preprocessing needed)

## References

Load these only when deeper detail is needed for a specific topic:

| File | Topic | Load When |
|------|-------|-----------|
| `references/five-principles.md` | Five Principles expanded + image-prompting notes | Applying Give Direction, Specify Format, Provide Examples, Evaluate Quality, or Divide Labor |
| `references/llm-architecture.md` | LLM internals for prompt engineers | Tokenization, hallucinations, truth bias, ChatML, RLHF, Little Red Riding Hood, fine-tuning vs. prompting depth |
| `references/prompt-assembly.md` | Prompt structure & ordering | Designing prompt layout, content ordering, context window management |
| `references/prompting-patterns.md` | All prompting patterns | Zero-shot, few-shot, CoT, ReAct, RAG (incl. retrieval trade-offs), Tree of Thoughts, meta-prompting, least-to-most, structured output/tool-call templates |
| `references/evaluation-debugging.md` | Evaluation & debugging | LLM-as-judge rubric design (SOMA), manual review checklist, metrics, debugging workflow, hallucination mitigation |
| `references/agents-workflows.md` | Agents, tools & workflows | ReAct agents, tool-definition and tool-safety guidelines, workflow vs. agent decomposition, temperature/sampling params |
