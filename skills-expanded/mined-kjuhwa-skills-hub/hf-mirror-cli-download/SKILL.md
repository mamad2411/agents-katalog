---
name: hf-mirror-cli-download
description: Route HuggingFace model and dataset downloads through the hf-mirror.com China mirror using the huggingface-cli tool.
category: automation
version: 1.0.0
version_origin: extracted
tags: [huggingface, mirror, china, offline]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Lordog/dive-into-llms.git
source_ref: main
source_commit: f84c04268794ef94f8949808bbc14ab8636763a0
source_project: dive-into-llms
source_path: documents/chapter4/README.md
imported_at: 2026-04-18T00:00:00Z
---

# HuggingFace Mirror CLI Download

## When to use
- In China where direct HuggingFace downloads are slow or blocked.
- Download models or datasets via huggingface-cli with a mirror endpoint.

## Steps

1. Set the mirror endpoint:

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

2. Download a model:

```bash
huggingface-cli download --resume-download Qwen/Qwen2.5-Math-1.5B \
    --local-dir model/Qwen2.5-Math-1.5B
```

3. Download a dataset:

```bash
huggingface-cli download --resume-download zwhe99/DeepMath-103K \
    --repo-type dataset --local-dir dataset/DeepMath-103K
```

4. RLHF chapter downloads:

```bash
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download --resume-download stanfordnlp/imdb --local-dir dataset/imdb --repo-type dataset
huggingface-cli download --resume-download lvwerra/gpt2-imdb --local-dir model/gpt2-imdb
huggingface-cli download --resume-download lvwerra/distilbert-imdb --local-dir model/distilbert-imdb
```

## Pitfalls
- Mirror may lag for very new uploads.
- Use --resume-download for large models to avoid restarting interrupted downloads.
- Set HF_ENDPOINT before running any HuggingFace Python code too.

## Source
- Chapters 4 and 11 of dive-into-llms
