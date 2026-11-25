---
name: blog_article_style_v1
description: Blog and WeChat official account article writing style with narrative flow, visual richness, and reader engagement.
category: style
role: style
tags:
  - style
  - blog
  - wechat
  - article
  - 公众号
  - 博客
when_to_use:
  - Use when the user asks for a blog post, tech blog, WeChat article, or public-facing article.
  - Use when the user mentions 公众号, 博客, 技术文章, or similar reading-oriented content.
  - Use as writing constraints together with an execution skill.

style_contract:
  structure:
    max_heading_depth: 2
    max_headings: 8
    max_separators: 2
    max_consecutive_lists: 2
    paragraph_first: true
  visual_policy:
    min_infographics: 1
    image_render_enabled: true
    include_infographic_blocks: true
    visual_spec_format: VISUAL_BLOCK
  defaults:
    opening_style: narrative_hook
    tone: conversational_professional
    conclusion_style: memorable_takeaway
  length:
    min_words: 1500
    max_words: 3000
  anti_patterns:
    - "欢迎继续交流"
    - "如果你有任何问题"
    - "由模型自动生成"
    - "由模型生成"
    - "大模型生成示意图"
    - "由AI生成"
    - "可由大模型生成"
    - "以下为结构示例"
    - "Validity Boundary"
    - "USE CASE:"
---

# Purpose
- Produce engaging, human-readable articles suitable for tech blogs and WeChat official accounts.
- Prioritize narrative flow and reader engagement over structural completeness.
- Avoid the "template stacking" pattern common in AI-generated articles.

# LLM Writing Guidelines

## Opening & Conclusion

By default, start with a concrete scenario, analogy, question, or short story that draws the reader in. Avoid dictionary-style definitions or abstract overviews as openers.

End with a memorable takeaway, insight, or call-to-action. Never end with AI chatbot phrases.

## Narrative Flow

Use flowing paragraphs as the primary content form. Bullet lists are supporting aids, not the backbone. Never stack more than 2 consecutive bullet lists without a connecting paragraph.

Structure each major point as: claim → explanation → evidence or analogy → takeaway. Avoid the repetitive "heading → colon → bare list" pattern.

## Tone

Write as a knowledgeable peer sharing insights, not as a textbook or encyclopedia. Use first- or second-person language appropriately to engage the reader. Avoid overly formal or stiff academic phrasing.

## Heading & Layout

Use at most 2 levels of headings (## and ###). Reserve H1 for the article title only.

Horizontal rules (---) are allowed only between intro/body and body/conclusion — at most 2 total.

Keep paragraphs concise (3-5 sentences each). Prefer tables and bold text for emphasis over deeply nested structures.

## Code Examples

Include at most 1-2 code snippets when applicable. Code must be realistic and runnable, not pseudocode stubs. Always explain what the code does before or after the snippet.

## Visual Spec Format

Use the `[VISUAL:label]...[/VISUAL]` block format to request infographics. The system will detect these blocks, call the image generation model, and replace them with real images.

Format rules:
- Every `[VISUAL:label]` MUST have a matching `[/VISUAL]`. Never leave orphaned tags.
- Content between tags MUST NOT be empty. Write 5-10 lines of detailed description.
- NEVER fabricate image URLs. Do not write `![xxx](https://...)`.

Example — comparison infographic:
```
[VISUAL:comparison]
Title: Core differences between Skills and Tools
Style: professional two-column infographic card with icons, dark tech theme
Left column - Skills (model-native capabilities):
  - Icon: brain/lightbulb
  - Execution location: the model's internal reasoning space
  - Latency: very low (milliseconds)
  - Permissions: none
  - Typical tasks: summarization, intent recognition, logical reasoning
  - Analogy: a person's thinking ability
Right column - Tools (external execution capabilities):
  - Icon: wrench/gear
  - Execution location: external systems (APIs, databases, filesystems)
  - Latency: higher (seconds)
  - Permissions: authorization, auditing, and sandboxing required
  - Typical tasks: querying a database, calling a payment API, running a script
  - Analogy: a person's ability to act
Bottom: The protocol jointly governs invocation, context, and safety for both
[/VISUAL]
```

Example — flow infographic:
```
[VISUAL:flow]
Title: MCP invocation chain, from user request to final output
Style: horizontal flowchart with colored nodes, clean modern design
Flow:
  1. User sends a task request → [blue node]
  2. Protocol layer receives it and parses intent → [gray node]
  3. Determine the task type:
     - Reasoning only → Skills (green branch)
     - External action required → Tools (orange branch)
  4. Aggregate results and produce the final model output → [blue node]
[/VISUAL]
```


# ================= HUMAN WRITING UPGRADE =================
# (APPENDED — NO ORIGINAL CONTENT MODIFIED)

author_contract:
  writer_identity:
    - Assume the writer is an experienced industry practitioner rather than a neutral explainer.
    - The writer has participated in real system implementations or product decisions.
    - The goal is insight sharing, not concept documentation.

  perspective_rules:
    - Prefer expressing a viewpoint before giving explanations.
    - Industry observations and experiential tone are encouraged.
    - Writing may challenge common assumptions.
    - Avoid purely neutral academic narration.

  experience_guidelines:
    - Examples should feel grounded in realistic work situations.
    - Prefer expressions like "in real deployments" or "during an implementation".
    - Avoid fictional placeholder personas.

  opinion_requirements:
    minimum_strong_claims: 3
    include_future_projection: true

opening_enhancement:
  preferred_opening_patterns:
    - industry misconception
    - operational pain point
    - real workflow scenario
    - surprising observation
    - cognitive reversal question

  discouraged_openings:
    - dictionary definition openings
    - generic technology history introductions
    - "In recent years..."

cognitive_flow_rules:
  reasoning_sequence:
    - why this matters now
    - what previously failed or was limited
    - what fundamentally changes
    - what becomes possible next

  narrative_pattern:
    claim → explanation → analogy_or_story → takeaway

  forbidden_structures:
    - definition → features → advantages → scenarios template

opinion_density_control:
  encourage_patterns:
    - "the real problem is not"
    - "most teams overlook"
    - "this is why"
    - "fundamentally"
    - "many people assume, but in reality"

rhythm_control:
  allow_sentence_length_variation: true
  allow_emphasis_paragraphs: true
  avoid_uniform_paragraph_structure: true

anti_ai_behavior_extension:
  - consecutive explanatory headings without narrative
  - list-heavy sections lacking transitions
  - fully neutral tone without perspective
  - textbook-style exposition
