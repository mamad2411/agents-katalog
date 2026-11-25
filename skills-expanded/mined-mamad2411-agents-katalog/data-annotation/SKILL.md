---
name: data-annotation
description: Create, format, and validate instruction-tuning and preference datasets for fine-tuning and RLHF alignment.
---

# Data Annotation

Use this skill when the user needs to create or curate labeled datasets for fine-tuning, instruction tuning, or RLHF alignment.

## Scope

- Create instruction/response pairs from raw content or domain knowledge.
- Format multi-turn conversations for chat model training.
- Build preference datasets (chosen/rejected) for DPO/RLHF.
- Generate synthetic training data using LLM-as-judge pipelines.
- Validate and clean annotation quality before training.

## Dataset Formats

Support output in standard formats:

- **Alpaca**: `{"instruction": "...", "input": "...", "output": "..."}`
- **ShareGPT**: `{"conversations": [{"from": "human", "value": "..."}, ...]}`
- **OpenAI chat**: `{"messages": [{"role": "user", "content": "..."}, ...]}`
- **DPO pairs**: `{"prompt": "...", "chosen": "...", "rejected": "..."}`

Always validate schema before export. Report and quarantine malformed entries.

## Instruction Dataset Creation

Guidelines for building instruction datasets:

- Cover diverse task types (QA, summarization, code, reasoning, creative writing).
- Vary instruction complexity (simple → multi-step → chain-of-thought).
- Include negative examples and edge cases.
- Avoid repetitive templates — aim for linguistic diversity.
- Target minimum 1,000 high-quality examples for domain-specific tuning.

## Synthetic Data Generation

When manual annotation volume is insufficient:

- Use a strong reference model to generate candidate responses.
- Apply LLM-as-judge scoring for quality filtering.
- Cross-validate synthetic outputs against human-written gold samples.
- Report synthetic-to-human ratio and quality metrics.
- Flag hallucination-prone categories for human review.

## Preference Data (DPO/RLHF)

For alignment datasets:

- Present same prompt with two responses (chosen vs rejected).
- Ensure clear quality separation between chosen and rejected.
- Cover safety, helpfulness, and factuality dimensions.
- Minimum 500 preference pairs for meaningful alignment signal.
- Track annotator agreement rate when multiple reviewers are involved.

## Quality Assurance

Run validation checks on completed datasets:

- Schema validation (required fields, types, lengths).
- Duplicate detection (exact and near-duplicate prompts/responses).
- Length distribution analysis (flag outliers).
- Toxicity/safety scan on responses.
- Coverage analysis across intended task categories.

## Deliverables

1. Formatted dataset files (JSONL/Parquet)
2. `annotation_guidelines.md` (format spec, quality criteria)
3. `dataset_quality_report.md` (stats, coverage, quality metrics)
4. `category_distribution.json` (task type breakdown)

## Python Dependencies

- `datasets`
- `pandas`
- `langdetect`
- `regex`
