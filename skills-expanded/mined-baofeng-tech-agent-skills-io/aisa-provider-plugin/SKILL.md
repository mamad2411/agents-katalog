---
name: aisa-provider-plugin
description: Requires AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `aisa-provider`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Configure AIsa as a first-class model provider for OpenClaw, enabling production access to major Chinese AI models (Qwen, DeepSeek, Kimi K2.5, Doubao) through official partnerships with Alibaba Cloud, BytePlus, and Moonshot. Use this skill when the user wants to set up Chinese AI models, configure AIsa API access, compare pricing between AIsa and other providers (OpenRouter, Bailian), switch between Qwen/DeepSeek/Kimi models, or troubleshoot AIsa provider configuration in OpenClaw. Also use when the user mentions AISA_API_KEY, asks about Chinese LLM pricing, Kimi K2.5 setup, or needs help with Qwen Key Account setup.
version: 1.0.0
license: Apache-2.0
requires:
  bins: []
  env:
  - AISA_API_KEY
metadata:
  aisa:
    requires:
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one
---

# AIsa Provider Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/aisa-provider/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
