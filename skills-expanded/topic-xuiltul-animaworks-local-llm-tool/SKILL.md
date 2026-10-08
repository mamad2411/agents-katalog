---
name: local-llm-tool
description: >-
  A local LLM execution tool. Requests text generation and chat from models on GPU via Ollama or vLLM.
  Use when: Use when: on-premise inference, calling Ollama endpoints, or needing summaries and generation with local models.
tags: [llm, local, ollama, external]
---


# Local LLM Tool

An external tool that performs text generation and chat via local LLMs (Ollama/vLLM）).

## How to Call

**Bash**: Run with `animaworks-tool local_llm <サブコマンド> [引数]`

## List of Actions

### generate — Text Generation
```bash
animaworks-tool local_llm generate "プロンプト" [-S "システムプロンプト"]
```

### chat — Chat (Multi-turn)
```bash
animaworks-tool local_llm chat [--messages JSON] [-S "システムプロンプト"]
```

### models — List Models
```bash
animaworks-tool local_llm list
```

### status — Check Server Status
```bash
animaworks-tool local_llm status
```

## CLI Usage

```bash
animaworks-tool local_llm generate "プロンプト" [-S "システムプロンプト"]
animaworks-tool local_llm list
animaworks-tool local_llm status
```

## Notes

- The Ollama server or vLLM server must be running
- -s/--server can be used to specify the server URL
- -m/--model can be used to specify the model
