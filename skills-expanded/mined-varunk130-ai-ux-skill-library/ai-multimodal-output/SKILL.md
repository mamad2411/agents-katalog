---
name: ai-multimodal-output
description: 'Design how AI presents results across text, code, images, charts, and mixed media - response formatting, output hierarchy, and cross-modal transitions. Use when: AI output design, response formatting, AI results display, multimodal output, AI-generated content presentation, code output UX, AI visualization.'
---

# AI Output & Multimodal Design

Design how AI results are presented, formatted, and consumed across every output modality - text, code, images, data visualizations, and mixed media. The RENDER framework ensures AI outputs are scannable, actionable, and trustworthy regardless of format.

## Core Principle

AI generates output. Humans consume meaning. The gap between raw AI output and human understanding is a **design problem**, not a model problem. A brilliant AI answer poorly formatted is worse than a mediocre answer well-structured.

---

## The RENDER Framework

| Letter | Principle | Design Question |
|---|---|---|
| **R** | Right Format | Is the output in the format that best serves the user's goal (not the model's default)? |
| **E** | Easy to Scan | Can the user extract the key insight in under 5 seconds? |
| **N** | Navigable Depth | Can the user drill into details without drowning in them upfront? |
| **D** | Directly Actionable | Can the user act on this output without additional steps? |
| **E** | Editable | Can the user modify, refine, or iterate on the output in-place? |
| **R** | Reproducible | Can the user understand how to get this output again or share it? |

---

## Output Format Selection Matrix

The AI should automatically select the best output format based on the content type:

| Content Type | Best Format | Why | Anti-Pattern |
|---|---|---|---|
| Single factual answer | Inline text (1-2 sentences) | Quick to consume | A 3-paragraph essay for a yes/no question |
| Step-by-step instructions | Numbered list with headers | Scannable, sequenceable | Prose paragraphs describing steps |
| Comparison | Table with clear columns | Side-by-side evaluation | Alternating paragraphs about each option |
| Code | Syntax-highlighted code block with language label | Copy-friendly, readable | Code embedded in prose without formatting |
| Data/trends | Chart or visualization | Pattern recognition | Raw numbers in a paragraph |
| Complex explanation | Headers + sections + summary | Navigable hierarchy | Wall of undifferentiated text |
| Creative writing | Clean prose, no artifacts | Immersive reading | Bullet points for a poem |
| Mixed | Composite card with labeled sections | Each element in its optimal format | Forcing everything into one format |

---

## The Response Hierarchy

Every AI response should follow this structure (whether the output is 1 line or 100):

| Level | What It Contains | Always Visible? | Example |
|---|---|---|---|
| **Headline** | The core answer in one sentence or phrase | Yes | "Your churn rate increased 12% QoQ, driven by enterprise segment." |
| **Key Details** | Supporting information, top 3-5 points | Yes (brief) | Key drivers, affected metrics, comparison to benchmark |
| **Evidence** | Sources, data, methodology, reasoning | Collapsed - expand on demand | Data tables, source citations, model confidence |
| **Actions** | What the user can do next | Yes (as buttons or suggestions) | "View affected accounts" / "Generate retention plan" / "Share with team" |

**Rule:** If the user has to scroll past the headline to understand the output, the formatting failed.

---

## Text Output Patterns

### Length Calibration

| User Context | Target Length | Formatting |
|---|---|---|
| Chat conversation | 50-150 words | Conversational paragraphs, minimal formatting |
| Professional analysis | 200-500 words | Headers, bullet points, key metrics highlighted |
| Research/deep dive | 500-2000 words | Table of contents, collapsible sections, executive summary |
| Quick reference | 10-50 words | Single sentence or small table |

### Text Formatting Rules

| Rule | Implementation | Why |
|---|---|---|
| Bold key numbers and conclusions | **12% increase** not "12% increase" | Users scan for emphasized content |
| Use tables for comparisons, not prose | | Humans process tabular data 3x faster than narrative comparisons |
| Break at natural section points | New header every 3-5 paragraphs | Prevents wall-of-text fatigue |
| Lead with the answer, not the reasoning | Answer first, then "Here's why..." | Most users want the answer; some want the reasoning |

---

## Code Output Patterns

| Pattern | When to Use | Implementation |
|---|---|---|
| **Copy-ready block** | User will paste code directly | Syntax highlighting + one-click copy button + language label |
| **Diff view** | AI modified existing code | Side-by-side or inline diff showing changes |
| **Annotated code** | Code needs explanation | Inline comments or adjacent explanation panel |
| **Executable snippet** | Code can run in-place | Run button + output preview below the code block |
| **Multi-file output** | Change spans multiple files | Tabbed interface or file tree with per-file diffs |

### Code Output Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Code in a paragraph without code block formatting | Unreadable, uncopyable |
| Explaining code in prose ABOVE the code block | User reads explanation, forgets it by the time they see the code |
| Showing only the changed lines without surrounding context | User can't locate where to put the code |
| No language label on code blocks | User can't tell if it's Python, JavaScript, or pseudocode |

---

## Data Visualization Output

When AI output contains data, choose the right visualization:

| Data Relationship | Visualization | When NOT to Use |
|---|---|---|
| Trend over time | Line chart | Fewer than 4 data points (use table instead) |
| Part of whole | Pie chart (< 6 slices) or stacked bar | More than 6 categories (use bar chart) |
| Comparison across categories | Horizontal bar chart | Time-series data (use line chart) |
| Distribution | Histogram or box plot | Categorical data |
| Correlation | Scatter plot | More than 2 variables (use small multiples) |
| Geographic | Map | Non-geographic data forced onto a map |

### Visualization Output Rules

| Rule | Why |
|---|---|
| Always include a text summary alongside the visualization | Not all users are visual learners; screen readers can't read charts |
| Label axes and include units | "Revenue" means nothing without "$M" and time period |
| Show data source and recency | "Based on Q1 2026 data" builds trust; undated charts don't |
| Offer "View as table" toggle | Some users prefer raw numbers; tables are more accessible |

---

## Multimodal Output Composition

When AI output spans multiple modalities (text + image + code + data):

### The Composite Output Card

| Section | Content | Position |
|---|---|---|
| **Summary text** | 1-2 sentence headline of what the AI produced | Top |
| **Primary output** | The main deliverable (image, analysis, document) | Center, largest |
| **Supporting detail** | Methodology, sources, alternative versions | Below primary, collapsible |
| **Action bar** | Copy, download, share, regenerate, iterate | Bottom, always visible |

### Cross-Modal Transition Design

When output switches between modalities:

| Transition | Design Pattern |
|---|---|
| Text → Chart | "Here's the breakdown:" + inline chart + "Key takeaway: [text summary below chart]" |
| Text → Code | "Here's how to implement this:" + code block + "This does X by Y" |
| Text → Image | "Here's what that looks like:" + image + descriptive caption |
| Multiple modalities in one response | Use clear section headers and visual separators between modalities |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Defaulting to maximum length for every response | Users asked a simple question and got a dissertation |
| Prose when a table would work | Forces linear reading of comparative information |
| Charts without text summaries | Excludes screen reader users; misses users who don't read charts |
| Outputting raw JSON/XML to non-technical users | Data format is not information format |
| No copy/download affordance on generated content | Users have to manually select and copy, or take screenshots |
| Identical formatting for 1-line answers and 100-line analyses | One size fits no one |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Design output formatting for AI product | Output Format Selection Matrix + Response Hierarchy | Format rules by content type + response structure spec |
| Improve readability of AI responses | Text Output Patterns | Length calibration guide + formatting rules |
| Design code output experience | Code Output Patterns | Code block component spec with copy, diff, and run features |
| Add data visualization to AI outputs | Data Visualization Output table | Chart selection guide + accessibility requirements |
| Design mixed-modality responses | Composite Output Card + Cross-Modal Transitions | Multimodal response template |

## Integration

Works with: `ai-trust-transparency` (confidence indicators in output), `ai-error-resilience` (error display formatting), `ai-prompt-ux` (output format matching input intent), `ai-conversation-architect` (response formatting in dialogue).
