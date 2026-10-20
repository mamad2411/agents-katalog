---
name: huggingface-tgi
description: "HuggingFace Text Generation Inference (TGI). High-performance LLM serving with continuous batching, tensor parallelism, watermarking, and OpenAI-compatible API. Native HF model hub integration."
tags: [tgi, llm-inference, huggingface, serving, text-generation, api, zorai]
---
## Overview

Text Generation Inference (TGI) is a production-ready LLM serving solution from Hugging Face. It provides optimized inference with continuous batching, quantization (GPTQ, AWQ), tensor parallelism, flash attention, and an OpenAI-compatible API.

## Installation

```bash
# Docker deployment (recommended)
docker run --gpus all -p 8080:80   -v $HOME/models:/data   ghcr.io/huggingface/text-generation-inference:latest   --model-id Qwen/Qwen2.5-1.5B-Instruct
```

## Client

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="none")
response = client.chat.completions.create(
    model="tgi",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

## Streaming

```python
stream = client.chat.completions.create(
    model="tgi",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

## References
- [TGI docs](https://huggingface.co/docs/text-generation-inference)
- [TGI GitHub](https://github.com/huggingface/text-generation-inference)