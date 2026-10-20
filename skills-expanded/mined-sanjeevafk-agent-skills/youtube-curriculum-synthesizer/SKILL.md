---
name: youtube-curriculum-synthesizer
description: Long-form lecture transcription, timeline chaptering, key concept extraction, and study guide builder.
metadata:
  category: research
  stack: ["yt-dlp", "faster-whisper", "pydantic"]
  source_reference: "web-scraping-agents/youtube-educator-plus-agent"
---

# YouTube Educational Lecture Synthesizer

## 1. Architectural Pattern & Core Intent

Long-form lecture transcription, timeline chaptering, key concept extraction, and study guide builder.

### Key Characteristics:
- **Primary Domain:** `RESEARCH`
- **Core Technology Stack:** `yt-dlp`, `faster-whisper`, `pydantic`
- **Upstream Implementation:** [`web-scraping-agents/youtube-educator-plus-agent`](file://web-scraping-agents/youtube-educator-plus-agent)

Author: [David Zhu](https://www.linkedin.com/in/david-zhu-704579248/) **Platform:** n8n (you can import the .json file into your own n8n to check out the flow) **Note:** All API keys have been removed from the .json file This agent takes a YouTube link as input and generates a fill-in-the-blank note sheet, a quiz to take at the end of the video, and additional resources. It also provides a PDF file link containing all the generated content. (Note: The PDF may appear slightly off due to markdown 

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install yt-dlp faster-whisper pydantic
```

### Essential Environment Variables:
```env
# Configure matching credentials based on active provider
OPENAI_API_KEY="your-api-key"
ANTHROPIC_API_KEY="your-api-key"
# Database / Vector store connections if applicable
NEO4J_URI="bolt://localhost:7687"
QDRANT_URL="http://localhost:6333"
```

---

## 3. Standard Execution Workflows

### Primary Invocation Pattern:
Refer to the upstream reference code in `web-scraping-agents/youtube-educator-plus-agent` for concrete implementation templates:

```python
# Minimal execution idiom for youtube-curriculum-synthesizer
# Inspect web-scraping-agents/youtube-educator-plus-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
