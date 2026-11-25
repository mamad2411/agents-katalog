---
name: gemini-api
description: Provides the official Protobuf specifications and gRPC/REST service definitions for the Gemini API (Google Generative Language API v1beta). Use this skill when you need precise schema definitions for requests/responses (e.g., GenerateContent, Tools, FunctionCalling), multimodal content structures (Content, Part), context caching, model metadata, safety settings, or file uploads.
---

# Gemini API Documentation (Protobuf Definitions)

This skill provides the official v1beta Protobuf definitions for the Google Generative Language API (Gemini). These files contain the absolute source of truth for API capabilities, request/response structures, and schema definitions.

## When to use these references

When implementing or debugging Gemini API clients (such as in Rust, Go, or other languages), refer to these files for the exact structure of messages, enums, and RPC methods.

## Core Services & Schemas

The `.proto` files are located in `references/`. Here is a guide on where to look for specific features:

### Content Generation & Tools
- **`generative_service.proto`**: Contains the core `GenerateContentRequest` and `GenerateContentResponse`. Look here for tool configurations, system instructions, and generation configurations.
- **`content.proto`**: Defines the `Content`, `Part`, `FunctionCall`, `FunctionResponse`, `Tool`, and `ToolConfig` structures. Essential for understanding how to construct multimodal payloads and function calling schemas.
- **`safety.proto`**: Defines `HarmCategory`, `SafetySetting`, and `SafetyRating` enums and messages.

### Models & Metadata
- **`model.proto`**: Defines the `Model` message, including properties like `input_token_limit`, `output_token_limit`, and supported generation methods.
- **`model_service.proto`**: RPCs for listing and getting models (`GetModel`, `ListModels`).

### Context Caching
- **`cached_content.proto`**: Defines the `CachedContent` resource for caching large prompts.
- **`cache_service.proto`**: RPCs for managing cached contents (`CreateCachedContent`, `UpdateCachedContent`, etc.).

### File API (Multimodal Uploads)
- **`file.proto`**: Defines the `File` resource representing uploaded media (video, images, documents).
- **`file_service.proto`**: RPCs for the File API (`CreateFile`, `ListFiles`, `GetFile`, `DeleteFile`).

### Semantic Retrieval (RAG/AQA)
- **`retriever.proto` / `retriever_service.proto`**: Definitions for Corpora, Documents, Chunks, and operations like Semantic Search and Attributed Question Answering (AQA).

### Fine-tuning
- **`tuned_model.proto`**: Definitions for tuning jobs and datasets.
- **`permission.proto` / `permission_service.proto`**: Access control for tuned models and corpora.

### Legacy / PaLM Services
- **`discuss_service.proto` / `text_service.proto` / `prediction_service.proto`**: Older APIs (like `GenerateMessage` or `GenerateText`), primarily for PaLM 2 models. Usually not needed for modern Gemini implementations.

## How to use

If you need to know the exact field names, types, or enums (e.g., "Does `ToolConfig` take a string or an enum for function calling mode?"), use `grep_search` or view the relevant file in the `references/` directory.

Example: If implementing function calling, check `content.proto` for `FunctionCall` and `generative_service.proto` for where `tools` is placed in the `GenerateContentRequest`.
