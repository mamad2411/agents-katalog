---
name: agentsystemtools_vision
description: agent.system.tools vision
---

# agent.system.tools vision

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.tools vision**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/prompts/agent.system.tools_vision.md`

## 🧠 Master Agent Prompt & Capabilities

## "Multimodal (Vision) Agent Tools" available:

### vision_load:
load image data to LLM
use paths arg for attachments
multiple images if needed
only bitmaps supported convert first if needed

**Example usage**:
```json
{
    "thoughts": [
        "I need to see the image...",
    ],
    "headline": "Loading image for visual analysis",
    "tool_name": "vision_load",
    "tool_args": {
        "paths": ["/path/to/image.png"],
    }
}
```

