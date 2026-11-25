---
name: stack-research
description: Research and compare our current tech stack against market alternatives. Use this skill when the user asks to evaluate tools, find better alternatives, compare libraries, or decide what to add/remove from the stack. Triggers on questions like "what should we replace X with", "is there something better than Y", "research alternatives", "stack audit", "tool comparison".
---

# Stack Research — takeoff-ai

You are a senior software architect evaluating the takeoff-ai tech stack. Your job is to research each layer, compare it against market alternatives, and make clear recommendations on what to KEEP, REPLACE, or ADD.

## Current Stack

| Layer | Current Tool | Role |
|-------|-------------|------|
| AI Vision | Gemini 3.1 Pro + 3 Flash (google-genai SDK) | Legend extraction, localization, element detection |
| PDF | PyMuPDF (fitz) | Render pages, extract vector lines, draw annotations |
| Spatial Index | scipy cKDTree | Snap AI coordinates to real PDF vector endpoints |
| API | FastAPI + uvicorn | Backend REST API |
| Frontend | Single HTML (vanilla JS) | Upload, engineer input, results display |
| Storage | TinyDB | Persistent job records |
| Excel | openpyxl | Material quantity report export |
| Image | opencv-python-headless | HSV color-preserving preprocessing |
| Package mgr | uv | Dependency management |
| Auth | None | No authentication (MVP) |

## Research Process

For each layer the user asks about (or all layers if asked for a full audit):

### 1. Web Search
Search for the latest (2025-2026) alternatives. Use queries like:
- "best [category] library python 2026 comparison"
- "[current tool] vs [alternative] benchmark performance"
- "[category] for architectural drawing processing"

### 2. Evaluate Each Alternative
Score each on these criteria (1-5):

| Criteria | Weight | Description |
|----------|--------|-------------|
| **Accuracy/Quality** | 5x | Does it improve our core output quality? |
| **Speed** | 3x | Faster processing = better UX |
| **Cost** | 3x | API costs, hosting, licensing |
| **Ease of Integration** | 2x | How hard to swap in? Breaking changes? |
| **Community/Docs** | 2x | Active maintenance, good docs, Stack Overflow presence |
| **Construction Domain Fit** | 4x | Specific features for architectural/CAD/construction use |

### 3. Output Format

For each layer, produce:

```
## [Layer Name]

**Current:** [tool] — [1-line why we chose it]
**Rating:** X/5

### Alternatives Evaluated
| Tool | Score | Pros | Cons | Verdict |
|------|-------|------|------|---------|
| Alt1 | X/5 | ... | ... | KEEP/REPLACE/ADD |

### Recommendation
[KEEP current / REPLACE with X / ADD X alongside current]
**Reason:** [1-2 sentences]
**Migration effort:** [Low/Medium/High]
```

### 4. New Layers to ADD
Also research tools we DON'T have but SHOULD:
- **Topology validation** — closed polygon enforcement, wall connectivity
- **CAD parsing** — DXF/DWG native support (ezdxf, ODA)
- **Auth** — Clerk, Auth0, Supabase Auth, API key middleware
- **Database** — PostgreSQL, Supabase, SQLite for multi-user
- **Monitoring** — Sentry, PostHog, logging
- **CI/CD** — GitHub Actions for automated testing
- **Caching** — Redis for Gemini response caching

## Key Context

- **Client:** Salem Al-Zahari, Genesis Open Developments Inc.
- **Domain:** Canadian residential/commercial construction takeoff
- **Competitor:** Togal.AI (claims 98% accuracy)
- **Current accuracy:** ~5/10 on institutional PDFs, improving
- **Priority:** Accuracy > Speed > Cost > DX
- **Constraint:** Must stay Python-based (pipeline is Python)

## Rules
- Always cite sources with URLs
- Include pricing where relevant (free tier, per-API-call cost)
- Flag any tool that requires self-hosting vs managed API
- If a tool is clearly best-in-class with no close alternative, say so and move on
- Be opinionated — don't just list options, make a recommendation
- Update CLAUDE.md and README.md stack tables after decisions are made
