---
name: generate-mmo-content
description: Generate Programmatic SEO (pSEO) Answer-First landing pages with JSON-LD schemas and multimodal short-form social video hooks (TikTok/Reels/Shorts) with AIDA/PAS scripts. Use when launching programmatic landing page campaigns, scaling SEO content volume, or producing high-converting social video hooks.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Generate MMO Content

Use this skill to automate the production of high-converting Programmatic SEO (pSEO) landing pages and multimodal short-form video hooks for performance marketing at scale, replacing obsolete spin content with modern structured data and direct-response frameworks.

## Legal & Compliance Notice

Generating large volumes of near-duplicate ad copy/creatives specifically to bypass a platform's duplicate-content or ad-review filters can violate platform advertising policies even when each individual piece is legal content. This skill's automation mechanics are content-neutral; the `COMPLIANCE-LOCK` rule below is a floor, not a ceiling — confirm the target platform's advertising policy permits the intended volume/variation strategy before scaling a spin run.

## When to Use

- generating Programmatic SEO (pSEO) landing pages with Answer-First (BLUF) layouts for Google AI Overviews
- embedding rich JSON-LD structured schemas (`Product`, `Review`, `AggregateRating`, `FAQPage`)
- crafting 3-second video hooks and AIDA/PAS scripts for TikTok, Instagram Reels, and YouTube Shorts
- creating automated audio/video generation prompts for ElevenLabs TTS and Remotion/CapCut video rendering
- scaling data-driven comparison and review pages from dynamic product feeds while enforcing API budget caps

## Example (Answer-First pSEO Page & Multimodal Social Video Hook)

```html
<!-- Answer-First BLUF (Bottom Line Up Front <= 60 words) -->
<section class="bluf-answer-box">
  <p><strong>Quick Verdict:</strong> The EcoClean Robot Vacuum offers superior 5000Pa suction and self-emptying at 40% lower cost than flagship competitors, making it our top budget recommendation for pet owners in 2027.</p>
</section>

<!-- JSON-LD Product, Review & AggregateRating Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "EcoClean Robot Vacuum",
  "review": {
    "@type": "Review",
    "reviewRating": { "@type": "Rating", "ratingValue": "4.8", "bestRating": "5" },
    "author": { "@type": "Organization", "name": "Performance Review Labs" }
  },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "124" }
}
</script>
```

```json
// Multimodal Social Video Script (TikTok/Reels/Shorts - 45s)
{
  "hook_type": "Negative Framing",
  "hook_visual": "Split-screen: dirty pet carpet vs instant single-pass clean with zoom",
  "hook_audio": "Stop spending $800 on branded robot vacuums until you check this one out.",
  "problem_agitation": "Most pet vacuums clog on long hair within two weeks and charge monthly fees for replacement bags.",
  "demo_value": "This 5000Pa motor features dual anti-tangle rubber rollers and self-empties into a sealed HEPA dock for 60 days.",
  "call_to_action": "Tap the link below to claim 35% off the introductory launch batch before it sells out.",
  "tts_engine": "ElevenLabs-Multilingual-v2",
  "tts_voice_id": "21m00Tcm4TlvDq8ikWAM"
}
```

```python
# Programmatic SEO page generator with budget circuit-breaker
def render_pseo_page(product: dict, budget_tracker) -> str:
    if budget_tracker.is_exceeded():
        raise RuntimeError("Budget-Lock: API spend threshold exceeded")
    
    bluf = f"The {product['name']} scores {product['rating']}/5 with {product['feature']}, delivering top performance at ${product['price']}."
    faq_schema = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in product['faqs']]
    return render_template("pseo_layout.html", product=product, bluf=bluf, faq_schema=faq_schema)
```

## Core Rules

- **PSEO-ANSWER-FIRST**: All programmatic SEO pages MUST incorporate an Answer-First (BLUF - Bottom Line Up Front) summary block containing <= 60 words positioned directly above the fold. This enables direct snippet extraction by AI Overviews and search engines before tabular comparisons.
- **JSON-LD-SCHEMA-INTEGRITY**: Every programmatic landing page MUST inject valid, verified JSON-LD structured data (`Product`, `Review`, `AggregateRating`, `FAQPage`). Never deploy pSEO pages without search-engine-readable entity schemas.
- **MULTIMODAL-HOOK-TAXONOMY**: Social short-form video scripts (TikTok, Reels, Shorts) MUST open with a verified 3-second hook taxonomy (Visual Pattern Interrupt, Negative Framing, Controversy, Curiosity Gap) followed by strict AIDA/PAS pacing: Hook (0–3s), Agitation (3–15s), Demo/Value (15–45s), and Actionable CTA (45–60s).
- **DATA-DRIVEN-DISTINCTIVENESS**: Deprecate legacy synonym spinning. Programmatic landing pages MUST be generated from rich, primary product feeds and benchmark datasets, ensuring semantic distinctiveness and high information gain.
- **BUDGET-LOCK**: Enforce hard programmatic spending and token caps in code (max tokens and cost circuit-breakers per batch execution) to prevent runaway LLM/TTS generation costs.
- **COMPLIANCE-LOCK**: Content must never violate legal boundaries (no deceptive claims, no fake medical guarantees, no prohibited financial schemes).
- **MULTI-MODEL-FALLBACK**: Implement multi-model fallback (OpenAI GPT-4o -> Anthropic Claude -> Google Gemini) to guarantee 99.9% uptime during API rate limits or outages.
- **EU-AI-ACT-DISCLOSURE**: Per EU AI Act Article 50, synthetic media and AI-generated commercial content targeting EU users MUST include appropriate AI provenance metadata and visual disclosures.

## Suggested Process

1. **Product Feed Ingestion**: Ingest tabular product datasets (pricing, specifications, benchmark ratings, affiliate deep links) into structured JSON repositories.
2. **Programmatic SEO Page Generation**: Procedurally generate static HTML pages with Answer-First BLUF summaries (<= 60w), dynamic comparison tables, FAQ accordions, and JSON-LD structured data.
3. **Multimodal Script Generation**: Use direct-response LLM prompt pipelines to generate 45-60s short-form video scripts categorized by hook type (Negative Framing, Pattern Interrupt) with exact visual and audio cues.
4. **Automated Voice & Visual Rendering**: Pipe approved scripts to ElevenLabs API for realistic voiceover synthesis and trigger Remotion/CapCut CLI pipelines to composite video creatives.
5. **Quality & Compliance Verification**: Run automated linters verifying BLUF word counts, JSON-LD schema validity via Google Rich Results standards, and compliance disclosure tags.

## Checklist

- [ ] Programmatic SEO landing pages include an Answer-First BLUF summary (<= 60 words).
- [ ] Valid JSON-LD structured data (`Product`, `Review`, `AggregateRating`, `FAQPage`) injected.
- [ ] Rich comparison tables generated from primary product data feeds.
- [ ] Short-form video scripts open with tested 3-second hooks (Negative Framing, Pattern Interrupt).
- [ ] Script pacing adheres strictly to AIDA/PAS progression ([Hook] -> [Agitation] -> [Demo] -> [CTA]).
- [ ] Automated TTS voiceover prompts configured with verified voice IDs and pacing.
- [ ] Hard API budget caps (Budget-Lock) enforced in generation scripts.
- [ ] Multi-model fallback (OpenAI -> Anthropic -> Gemini) operational.
- [ ] EU AI Act Article 50 disclosures applied to AI-generated creative assets.
- [ ] Generated assets pass human review gates before ad platform or CMS publication.

## Output Contracts

When the generated content is compiled for publishing or cross-role handoff, emit:

- **`contracts/schemas/content-handoff.json`** capturing asset type, channel (`pSEO`, `TikTok`, `Shorts`), target keywords, BLUF summary, JSON-LD schema status, and human review sign-off.
- Markdown content brief detailing campaign messaging angles, hook variations, and conversion metrics.

Skip emission for single-asset local experiments that do not cross role boundaries.

## Failure Modes

- **JSON-LD schema validation failure**: Syntax errors or missing required fields in JSON-LD prevent rich snippets from rendering. Mitigation: validate schema against Google Rich Results test API before export.
- **BLUF word count overflow**: Answer-First block exceeds 60 words, causing search engines to truncate or ignore snippet. Mitigation: enforce automated character and word count linters.
- **Social video hook fatigue**: Using generic hooks yields < 15% 3-second retention on TikTok/Reels. Mitigation: rotate across the 4 core hook archetypes and measure 3s drop-off rates.
- **API budget overrun**: Batch generation script enters unhandled retry loop, exhausting API credits. Mitigation: enforce hard-coded `MAX_BUDGET_USD` circuit breaker.
- **Shallow spin de-indexing**: Pages lack unique information gain and get de-indexed as spam. Mitigation: anchor every page with unique product dataset attributes and real user reviews.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: Untrusted product feed reviews or third-party descriptions must not inject malicious prompt instructions into generation pipelines.
- **ASI03 Identity & Privilege Abuse**: Never embed API keys, internal CMS endpoints, or tracking tokens in generated HTML or video metadata.
- **ASI04 Supply Chain**: Content generation packages and templating libraries must be pinned to verified versions; audit third-party prompt templates.
- **ASI05 RCE Guard**: Never construct shell rendering commands (e.g. FFmpeg, Remotion) directly from unsanitized user-generated content without parameterization.
- **ASI07 Inter-Agent Communication**: Content handoffs must conform to `contracts/schemas/content-handoff.json` for consumption by deployment pipelines.
- **ASI09 Human-Agent Trust Exploitation**: Always disclose AI generation provenance and verify promotional claims before distributing public marketing materials.

## Related Skills

- **setup-deployment**: Deploy generated programmatic landing pages to CDNs or hosting infrastructure.
- **analyze-campaign-roi**: Measure conversion rates, organic search traffic, and CPA of generated content.
- Companion reference: `references/pseo-landing-pages-and-social-video-hooks.md`
- Companion example: `examples/pseo-programmatic-page-generator.ts`
