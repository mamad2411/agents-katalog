---
name: autoeval-video-eval
description: This benchmark evaluates large vision-language models on open-ended video question answering across nine skill dimensions, including dynamic perception, temporal comprehension, causal reasoning, and response specificity. It probes the model's ability to connect multiple frames, understand temporal dynamics, and generate precise, video-grounded answers rather than generic or hallucinated text. Use when the user wants to benchmark on AutoEval-Video, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2311.14906
  bibtex_key: chen2023autoevalvideo
  confidence: high
---

# autoeval-video-eval

> AutoEval-Video: An Automatic Benchmark for Assessing Large Vision Language Models in Open-Ended Video Question Answering — Chen et al. (2023) (arXiv:2311.14906, 2023)

## What this evaluates

This benchmark evaluates large vision-language models on open-ended video question answering across nine skill dimensions, including dynamic perception, temporal comprehension, causal reasoning, and response specificity. It probes the model's ability to connect multiple frames, understand temporal dynamics, and generate precise, video-grounded answers rather than generic or hallucinated text.

## Datasets

- **AutoEval-Video** — total ?; splits: test (-1); repo https://github.com/Xiuyuan-Chen/AutoEval-Video

## Metrics

- `Accuracy` **(primary)** — range: percent
  - Percentage of correctly answered questions, determined by an LLM-based automatic evaluator (GPT-4) using instance-specific rules or human experts. Calculated as (number of correct responses / total number of instances) × 100.

## Input / output format

**Input**: A video clip (uniformly sampled into 8 or 16 frames) paired with an open-ended question.

**Output**: An open-ended natural language answer describing the event, reasoning, or information requested in the question.

## Scoring recipe

```python
correct_count = 0
for instance in dataset:
    eval_result = gpt4_evaluate(
        prompt=instance.rules,
        video_frames=instance.frames,
        question=instance.question,
        model_answer=instance.answer
    )
    if eval_result.is_correct:
        correct_count += 1
accuracy = (correct_count / len(dataset)) * 100
```

## Common pitfalls

- Using a unified prompt instead of instance-specific, adversarially refined rules causes a significant drop in evaluation accuracy (from 97% to 87%).
- Models often fail by reasoning on isolated frames rather than connecting temporal sequences, leading to hallucinations or overly general responses.
- Evaluating GPT-4V's own outputs can introduce self-bias; the protocol specifically tests on GPT-4V's incorrect responses to verify evaluator robustness.

## Evidence (verbatim from paper)

> Human baseline. We recruit three human participants to answer questions in AutoEval-Video. The overall average accuracy is 72.8%. Through closely examining the mistakes made by humans, we identify two major challenges they face: 1) Questions related to external knowledge, such as unfamiliar games, may lead to incorrect answers from humans; 2) Questions requiring precise memory skills, such as recalling multi-step processes in a video, may cause a person to overlook one or more steps.

## Citation

```bibtex
@misc{chen2023autoevalvideo,
  title={AutoEval-Video: An Automatic Benchmark for Assessing Large Vision Language Models in Open-Ended Video Question Answering},
  author={Chen et al. (2023)},
  year={2023},
  note={arXiv:2311.14906}
}
```

- arXiv: 2311.14906
