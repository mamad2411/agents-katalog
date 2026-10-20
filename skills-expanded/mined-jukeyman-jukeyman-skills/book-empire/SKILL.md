---
name: book-empire
description: Zero-intervention book creation system. Generates complete books (50K-150K words), covers, graphics, and multi-format output from ANY input. For RJ Business Solutions.
triggers: "make a book", "write a book", "book empire", "create ebook", "generate book", "build a book"
---

# Book Empire™ - Zero-Intervention Book Creation System

## Overview

Book Empire generates complete, production-ready books (50K-150K words) from any input source. Zero intervention required — proceeds automatically once initiated.

## Input Types

| Type | Method |
|------|--------|
| YouTube URL | yt-dlp → Whisper → AI processing |
| PDF File | pdf-lib text extraction |
| Audio File | Whisper CLI transcription |
| Webpage URL | Web scraping |
| Raw Text | Direct AI processing |
| Topic/Subject | AI-generated from scratch |

## Pipeline Stages

### Stage 1: Input Parsing
- YouTube: Download audio → Whisper transcription
- PDF: Extract text content via pdf-lib
- Audio: Direct Whisper transcription
- Webpage: Scrape content
- Text/Topic: Use directly

### Stage 2: Outline Generation
AI generates comprehensive chapter outline:
- 8-15 chapters based on target word count
- Each chapter: 5,000-15,000 words
- Hierarchical structure (H1, H2, H3)

### Stage 3: Research
For each chapter:
- Web search for relevant facts/statistics
- Extract key insights
- Inject into chapter content

### Stage 4: Chapter Writing
- Generate chapter content using AI
- Inject research insights
- Maintain consistent voice/style
- Build on previous chapters

### Stage 5: Formatting
Generate multi-format output:
- PDF (pdf-lib)
- EPUB (adm-zip)
- MOBI (placeholder)

### Stage 6: Cover Generation
AI image generation:
- Flux Pro → Ideogram → DALL-E → Placeholder
- 2:3 aspect ratio (1536x2304)
- Professional typography

## Output Structure

Every book includes:
- Title page
- Copyright page (RJ Business Solutions)
- Dedication
- Table of Contents
- Chapters (with research insights)
- Back matter with CTA

**Footer on every page:** `Built by RJ Business Solutions | rickjeffersonsolutions.com`

## Branding

- **Company:** RJ Business Solutions
- **Address:** 1342 NM 333, Tijeras, New Mexico 87059
- **Website:** https://rickjeffersonsolutions.com
- **Logo:** https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg

## API Endpoints

```
POST /api/generate
Body: {
  inputType: "youtube" | "pdf" | "audio" | "webpage" | "text",
  inputValue: string,
  title?: string,
  targetWordCount?: number (50000-150000)
}

GET /api/status/[jobId]
GET /api/download/[jobId]?format=pdf|epub|mobi
```

## Zero-Intervention Protocol

1. Parse input automatically
2. Generate outline without confirmation
3. Research each chapter silently
4. Write chapters sequentially
5. Format all outputs
6. Generate cover image
7. Return download links

**Do NOT ask questions. Proceed automatically.**

## Technical Stack

- **Runtime:** Next.js 14 (App Router)
- ** Transcription:** yt-dlp + OpenAI Whisper CLI
- **AI Processing:** OpenAI GPT-4
- **PDF Generation:** pdf-lib
- **EPUB Generation:** adm-zip
- **Image Generation:** Flux Pro / Ideogram / DALL-E

## File Locations

- `/src/lib/transcription.ts` - YouTube/audio transcription
- `/src/lib/book-generator.ts` - Core pipeline
- `/src/lib/formatter.ts` - PDF/EPUB generation
- `/src/lib/image-gen.ts` - Cover generation
- `/src/lib/types.ts` - TypeScript interfaces
