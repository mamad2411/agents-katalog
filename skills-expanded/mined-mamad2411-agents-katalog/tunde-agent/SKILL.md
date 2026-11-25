# Tunde Agent — project governance for AI-assisted development

## No OpenAI
- Do not suggest, import, or implement code that calls OpenAI services (APIs, SDKs, hosted endpoints, or branding).
- Do not add environment variables, settings fields, or documentation that require OpenAI credentials.

## Preferred models and providers
- **Gemini** (e.g. gemini-2.5-flash or current project default): complex reasoning, multimodal/vision, structured JSON pipelines.
- **DeepSeek** (e.g. deepseek-chat / R1-class models per project config): cost-efficient chat, coding-style tasks, high-volume calls where appropriate.

## Brand and architecture
- Treat **Tunde Agent** as a single product: prefer the existing Gemini/DeepSeek abstractions in `llm_service` and configured settings.
- Do not mix extra commercial LLM providers unless the user explicitly asks for a specific addition.

## Cost and sustainability
- Prefer **DeepSeek** for high-volume or low-stakes API usage when the task fits chat completion.
- Reserve heavier Gemini use for steps that need vision, strict JSON, or higher reasoning load.

## Image generation (illustrations)
- Use **Gemini** for prompts/planning only.
- For rendered images, use **non-OpenAI** options already in the repo (e.g. Pollinations.ai HTTP image endpoint) or other explicitly approved free/third-party image endpoints—never OpenAI image APIs.
