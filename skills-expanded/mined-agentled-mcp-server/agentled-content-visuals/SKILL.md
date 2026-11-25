---
name: agentled-content-visuals
version: 0.2.1
description: Generate or review one useful visual from the user's explicit content brief.
category: content
allowedApps: openai
allowedActions: openai.generate-image
relevanceKeywords: visual, image, illustration, content quality, accessibility
---

# AgentLed Content Visuals

Use this independent specialist only when the user asks to generate an image or needs a visual brief or candidate reviewed. In AgentLed, ground the work only in the authenticated current workspace and the relevant selected company, brand, page, or content context. Never borrow another workspace's context or invent a brand identity. In a portable host, use only the caller-selected root and context.

Listing `openai` or `openai.generate-image` recommends the existing AgentLed capability; it grants no app access, provider credential, approval, billing authority, publication authority, or permission to retry. Existing AgentLed action permission, approval, and credit checks remain authoritative.

When a required source, tool, or capability is unavailable, return a useful `Partial result:` and identify the missing evidence or access.

## Generate one visual

1. Preserve the user's explicit brief and load only the relevant selected brand, content, and material facts.
2. Choose one supported size that fits the requested use: square, landscape, portrait, or the existing Instagram portrait preset.
3. State the intended visual and any material assumptions before the paid action when the existing approval surface requires review.
4. After explicit generation intent and only when current action approval and credit checks allow it, make exactly one `openai.generate-image` attempt.
5. Return the generated image URL or artifact, useful alt text, and a concise visual-quality review covering claim fit, focal point, legibility, accessibility, and brand fit.

Do not retry automatically. A second paid attempt requires fresh explicit user intent after the first result or failure is visible. If generation fails, is ambiguous, or lacks a verifiable artifact, begin with `Partial result:`, preserve the exact brief and assumptions, name the gap, and ask before another attempt.

## Review a brief or candidate

Apply the quality checks directly from this skill: verify that the visual supports the claim without adding an unsupported one, has a clear focal point at the intended size, keeps essential text legible, includes useful alt text, and follows the selected brand's palette and tone without copying another brand. The supplementary portable-host checklist is in [references/quality-checks.md](references/quality-checks.md); AgentLed does not require that relative file at runtime.

## Separate action boundaries

Image generation does not authorize publication. Do not publish, schedule, create a workflow or routine, connect a provider, or make a durable preference change as part of this skill. Each external or durable action remains a separate explicit and approval-gated decision.
