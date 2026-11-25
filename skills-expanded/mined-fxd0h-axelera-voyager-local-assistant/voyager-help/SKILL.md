---
name: voyager-help
description: Get help with Voyager SDK for Axelera AI hardware. Use when the user asks questions about Voyager SDK, Axelera hardware, pipelines, InferenceStream API, or model zoo. Explanation-only answers; no code changes or pipeline runs.
argument-hint: "<question about Voyager SDK>"
allowed-tools: Read, Bash, Glob, Grep, mcp__voyager__*
---

# Voyager SDK Help

Get help with Voyager SDK for Axelera AI hardware

## Important Context

Answer with explanations only; do not change code or run pipelines.

## Instructions

Answer questions about Voyager SDK: **$ARGUMENTS**

### Step 1: Data Source & Environment Selection

{{INCLUDE common/voyager-sdk-setup.md}}

### Step 2: Answer the Question

After gathering information from the selected source:

1. **Synthesize Response**
   - Always frame answers in context of Axelera AI hardware
   - Provide Voyager SDK-specific code examples only after checking SDK/RAG evidence
   - Reference specific SDK components (InferenceStream, deploy.py, inference.py)
   - Distinguish `documented`, `observed locally`, and `not validated here`
   - Include a concise source note naming the SDK file, command output, or RAG result used

2. **Include Practical Examples**
   - Show actual command-line usage
   - Include YAML pipeline snippets when relevant
   - Reference model zoo locations (`ax_models/zoo/`)

3. **Hardware Context**
   - Mention detected Axelera device when relevant
   - Include AIPU core configuration options
   - Reference hardware capabilities such as vaapi, opencl, or opengl only when
     `.voyager-runtime.json` or SDK documentation supports them for this host

### Common Topics

| Topic            | RAG Query                  | Key Files                             |
| ---------------- | -------------------------- | ------------------------------------- |
| Pipeline YAML    | "pipeline YAML structure"  | `ax_models/zoo/**/*.yaml`             |
| InferenceStream  | "InferenceStream API"      | `axelera/app/stream.py`               |
| Deployment       | "model deployment compile" | `deploy.py`, `axelera/app/compile.py` |
| Input Sources    | "USB RTSP video sources"   | `axelera/app/config.py`               |
| Custom Operators | "custom operator pipeline" | `axelera/app/operators/`              |
| Trackers         | "ByteTrack OC-SORT"        | `trackers/`                           |

### Example Usage

```
voyager-help: How do I set up multi-stream inference?
voyager-help: What is the difference between the gst and torch-aipu pipes?
voyager-help: How to create a custom post-processor?
voyager-help: Explain the pipeline YAML structure
voyager-help: How to optimize for Axelera PCIe with 4 cores?
```
