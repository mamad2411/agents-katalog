# Gamma Presentation API Skill

_AI-powered presentation generation_

---

## Brand Guidelines

| Element | Value |
|---------|-------|
| Primary Color | #BFF549 (Lime) |
| Secondary Color | #60a5fa (Blue) |
| Preferred Theme | KDS Void Cyber |

---

## Workflow

### Step 1: Gather Requirements (6 Questions)

| # | Question | Options |
|---|----------|---------|
| 1 | Topic & Objective | What + desired action |
| 2 | Number of Slides | 5 (quick) · 8-10 (standard) · 12-15 (comprehensive) |
| 3 | Target Audience | Executives · Investors · Clients · Students · Internal |
| 4 | Text Density | Minimalistic · Balanced · Detailed |
| 5 | Visual Style | Corporate · Lifestyle · Tech · Abstract · Playful · Serious |
| 6 | Logo Placement | Top-right · Top-left · Bottom-right · Bottom-left · None |

### Step 2: Confirm Requirements
Always summarize and wait for confirmation before generating.

### Step 3: Generate API Request
```json
{
  "inputText": "[Detailed prompt based on requirements]",
  "textMode": "generate",
  "format": "presentation",
  "numCards": "[number]",
  "cardSplit": "auto",
  "exportAs": "pdf",
  "themeId": "[selected theme]",
  "textOptions": { "amount": "[brief/concise/detailed]", "language": "en" },
  "imageOptions": { "source": "aiGenerated", "model": "dall-e-3", "style": "[style]" },
  "cardOptions": {
    "headerFooter": {
      "[logoPlacement]": {
        "type": "image", "source": "custom", "src": "[logo-url]", "size": "md"
      }
    }
  }
}
```

### Step 4: API Execution
1. POST to `/v1.0/generations`
2. Poll status at `/v1.0/generations/{id}` every 10 seconds
3. Return both URLs when complete

---

## Content Templates

### 5-Slide (Quick Pitch)
| Slide | Purpose |
|-------|---------|
| 1 | Hook / Overview |
| 2 | Problem / Opportunity |
| 3 | Solution / Approach |
| 4 | Proof / Results |
| 5 | Call-to-Action |

### 8-10 Slide (Standard)
| Slide | Purpose |
|-------|---------|
| 1 | Title / Hook |
| 2 | Problem Statement |
| 3 | Market / Context |
| 4 | Solution Overview |
| 5 | Features / Benefits |
| 6 | How It Works |
| 7 | Case Study / Results |
| 8 | Pricing / Offering |
| 9 | Next Steps |
| 10 | Contact / CTA |

---

## API Reference

| Setting | Value |
|---------|-------|
| Base URL | https://api.gamma.app |
| Auth | Request user's API key (never hardcode) |
| Endpoint | POST /v1.0/generations |
| Status | GET /v1.0/generations/{id} |

---

## Quality Standards

### Always
- ✅ Theme matches brand
- ✅ Colors applied consistently
- ✅ One clear idea per slide
- ✅ Text density matches audience
- ✅ Both URLs in final delivery

### Never
- ❌ Skip the 6 questions
- ❌ Use default theme without checking
- ❌ Generate without confirming
- ❌ Forget both URLs

---

## Final Delivery Format
```
✅ Presentation Complete!
📊 [Title]
Slides: [n] | Theme: [name] | Style: [style]
🔗 View: [gammaUrl]
📥 PDF: [exportUrl]
```

---

## Use Cases for KDS

- Investor pitch decks for KMDSSLI shards
- Dragon Key personalized demos for billionaires
- Community onboarding presentations
- Marketplace seller guides
- Partnership proposals

---

_Added: 2026-03-28_
