---
name: azure-ai-services-expert
description: Consolidated expert skill for Azure AI services including Projects, VoiceLive, Content Safety, Document Intelligence, Translation, and Vision.
allowed-tools: Read Write Edit Glob Grep Bash WebSearch WebFetch
---

# Azure AI Services Expert (Multi-Language)

This skill consolidates various Azure AI SDKs across Python, Java, TypeScript, and .NET. Use this skill when implementing Microsoft's Cognitive Services and AI Foundry tools.

## Supported Services

### 1. Azure AI Projects (Foundry)
- **Languages**: Python, Java, TypeScript, .NET
- **Purpose**: Manage AI agents, connections, datasets, evaluations, and indexes within Azure AI Foundry. High-level SDK for LLM orchestration.

### 2. Azure AI VoiceLive
- **Languages**: Python, Java, TypeScript, .NET
- **Purpose**: Real-time bidirectional voice conversations with AI assistants using WebSockets.

### 3. Azure AI Content Safety
- **Languages**: Python, Java, TypeScript
- **Purpose**: Detect harmful content in text and images. Provides multi-severity classification for hate, self-harm, sexual, and violent content.

### 4. Azure AI Document Intelligence (Form Recognizer)
- **Languages**: .NET, TypeScript, Java (Legacy name: Form Recognizer)
- **Purpose**: Extract text, tables, key-value pairs, and structured data from documents (PDFs, images) using prebuilt and custom models.

### 5. Azure AI Translation
- **Languages**: Python (Document/Text), TypeScript
- **Purpose**: Real-time text translation, transliteration, language detection, and batch document translation.

### 6. Azure AI Vision (Image Analysis)
- **Languages**: Python, Java
- **Purpose**: Image captions, tagging, object detection, OCR (Optical Character Recognition), and smart cropping.

## Cross-Language Best Practices
- **Authentication**: Always use `DefaultAzureCredential` from `azure-identity` combined with the endpoint URL, rather than hardcoding API keys.
- **Async Processing**: Use asynchronous clients for high-throughput AI operations (e.g., batch document translation or large image analysis).
- **Error Handling**: Catch `HttpResponseError` and implement retry logic for 429 Too Many Requests (Rate Limiting), which is common in AI services.
