---
name: chatgpt-ads-builder
description: Build complete ChatGPT Ads campaigns including campaign structure, ad groups with context hints, and ads with character-validated copy (35-char headlines, 67-char descriptions) plus image generation prompts for 1024x1024 icons. Use this skill whenever the user mentions creating ChatGPT Ads, OpenAI Ads, SearchGPT ads, conversational ads, sponsored ChatGPT results, or wants to build, plan, or generate copy for advertising on the ChatGPT platform. Also trigger when the user asks for ad copy, headlines, descriptions, ad creative, or campaign structure specifically for ChatGPT, even if they don't explicitly say the word "skill". The skill interviews the user about campaign goal, audience, product, and proof points, then outputs a complete ready-to-configure campaign with multiple ad groups, two creative variants per ad, image prompts ready to paste into Gemini or Imagen, and context hints aligned with the platform's targeting model.
---

# ChatGPT Ads Builder

This skill produces complete ChatGPT Ads campaigns: campaign structure, ad groups with context hints, and ads with strictly-validated copy plus image prompts.

## How ChatGPT Ads work (operating constraints)

Before building anything, internalize these constraints. They drive every decision in this skill.

**Format constraints:**
- Headline maximum: 35 characters. Beyond this, text truncates.
- Description maximum: 67 characters. Beyond this, text truncates.
- Image: 1024x1024 PNG, but renders as a thumbnail (~80 to 120 pixels) in the actual ad slot.
- The advertiser's logo appears in the corner of the ad automatically. The image slot should NOT repeat the logo.

**Targeting model:**
- Ads use contextual intent matching, not behavioral history.
- Each ad group has "Context hints" describing the conversations, topics, or keywords where the ads may appear.
- Context hints are guidance, not exact-match rules. The system uses them to score relevance against live ChatGPT conversations.
- Ad groups should be organized by intent cluster: each group covers one coherent user need.

**Reading mode:**
- Users see ads as small thumbnails at the bottom of ChatGPT responses, mid-conversation. They are not actively searching.
- The image must read as a recognizable shape in under one second.
- The copy must communicate value in 35 characters of headline and 67 characters of description.

## Workflow

Three phases: Interview, Structure, Generate. Do them in order. Do not skip the interview.

**Supporting references** (load when needed):
- `references/interview-guide.md` covers the full interview question set with follow-ups for vague answers
- `references/copy-patterns.md` covers the extended copy pattern library with worked examples across industries
- `references/icon-design.md` covers the full icon concept library and prompt templates

### Phase 1: Interview

Ask the questions below conversationally, one topic per turn. Wait for a clear answer before moving on. If the user has already provided the answer in earlier conversation, skip that question. For the full question set with follow-ups for vague answers, read `references/interview-guide.md`.

When the user is experienced with marketing, batch related questions into a single turn (max 3 questions) using `ask_user_input_v0` if the questions have clean multiple-choice answers. For open-ended business questions, ask in prose.

1. **Campaign goal.** What is the primary objective of this campaign? Common goals: lead generation for a specific service, brand awareness, event or product launch, retargeting on a specific page, app installs, e-commerce sales. Get one concrete primary goal, not a list.

2. **Product or service.** What exactly is being advertised? Get the name, the one-sentence pitch, who it's for, and the destination URL.

3. **Language.** What language for the ad copy? Default to English unless the user is targeting a non-English market.

4. **Proof points.** What facts can the copy reference? Years in business, notable client or customer names, measurable outcomes, specific timeframes, certifications, scale numbers, ratings, awards. Get 3 to 5 concrete anchors. These become the credibility hooks in descriptions.

5. **Differentiators.** What makes this product different from the alternative the prospect would consider? What's the "not X" angle? Examples across industries: "not a spreadsheet", "not a course", "not a consultant", "not a chatbot", "not a generic template". Get the contrast point.

6. **Intents to target.** What kinds of ChatGPT conversations should trigger this ad? Probe for 3 to 6 distinct intent clusters. Each cluster becomes an ad group. Examples:
   - For a SaaS tool: "users asking how to automate [task X]", "users comparing [tool category]", "users frustrated with [legacy approach]"
   - For an e-commerce brand: "users researching gifts for [audience]", "users comparing [product category]", "users asking about [problem the product solves]"
   - For a service: "users asking how to find a [profession]", "users describing [problem the service solves]"
   
   Push the user to be specific about phrasing.

7. **Brand visual.** What are the brand colors? Is there an existing logo or icon style to match? Ask for hex codes if known, otherwise ask for general direction (dark + accent / light + accent / colorful).

8. **Budget and timing.** Optional but useful for the campaign overview section: rough monthly budget, campaign duration, and any geographic targeting.

### Phase 2: Structure the campaign

From the interview answers, produce a campaign skeleton before writing copy:

- **Campaign:** one campaign per primary goal. If the user gave multiple goals, ask which is primary and propose secondary campaigns for the rest.
- **Ad groups:** one ad group per intent cluster from question 6. Name each ad group after the intent it serves, not after the product.
- **Ads per group:** two ads per ad group. Both ads target the same intent but use different creative angles. This is A/B testing within the group, not running the same ad twice.

Show this skeleton to the user before writing copy. Confirm the structure makes sense. Adjust if needed.

### Phase 3: Generate

For each ad group, produce:

1. **Ad group name.** Short, descriptive, references the intent. Examples: "Spreadsheet escapers", "Gift researchers", "Course evaluators".

2. **Context hints.** Three to six short phrases describing the conversations, topics, or keywords where this ad group should match. Phrase them as natural descriptions, not boolean keyword lists. Example phrases: "users asking how to automate recurring reports", "comparisons between [category] tools", "questions about replacing manual workflows". Mix conversation topics with specific phrases the user might type.

3. **Two ads per group, each with:**
    - **Headline** at most 35 characters, validated by counting before output.
    - **Description** at most 67 characters, validated by counting before output.
    - **Display URL** with appropriate UTM parameters: `utm_source=chatgpt&utm_medium=cpc&utm_campaign={campaign_slug}&utm_content={ad_group_slug}_{variant}`.
    - **Image prompt** for a 1024x1024 icon (see Image prompt template below).

Each ad in a group should take a different angle on the same intent: one might lead with the contrast point ("X, not Y"), the other with a proof anchor (a specific number or notable customer). Don't duplicate the angle across variants.

## Copy patterns that work at 35/67 characters

These are the patterns that survive the tight character budget. Use them deliberately. For the full pattern library with worked examples across multiple industries and length tactics, read `references/copy-patterns.md`.

**Contrast.** "X, not Y" makes the differentiator unmissable in few characters.
Examples: "A CRM your team will actually use" (32), "Real photos, not stock illustrations" (35).

**Proof anchor.** A specific number, name, or timeframe lands credibility instantly.
Examples: "500 teams ship faster with us" (29), "Setup in under 10 minutes" (25).

**Imperative.** Verb-first lines feel like commands and read fast.
Examples: "Stop paying for unused seats." (28), "Skip the demo. Start free." (25).

**Compressed promise.** Subject + verb + outcome, no filler.
Examples: "Invoices that send themselves" (29), "Books delivered in 2 days" (24).

**Patterns to avoid:**

- Adjective stacks ("powerful, intelligent, scalable"): burn characters, say nothing.
- Em dashes: never use them.
- Rule of three ("better, faster, cheaper"): reads as AI-generated cadence.
- Generic openers ("Discover", "Unlock", "Transform"): replaceable by anything.
- Inflated abstractions ("solutions", "experiences", "journeys"): vague and trite.
- Brand name as headline: the brand already shows in the corner.

## Character count validation

Before outputting any ad, validate character counts. The skill includes a validation script at `scripts/validate_copy.py` that can be piped from stdin:

```bash
echo "Headline text|Description text" | python3 scripts/validate_copy.py
```

It prints a pass/fail line per ad with character counts and exits with status 1 if any ad exceeds the limits. Use this before delivering the final output to catch any over-limit copy.

If a line is over the limit, rewrite it shorter. Do not output anything that exceeds the limits. The output table should display character counts next to each line so the user can verify visually.

Example validation block (what to show the user in the output):

```
Headline: "Stop paying for unused seats." (28) ✓
Description: "Replace bloated SaaS bundles. Pay only for what you use." (56) ✓
```

## Image prompt template

The image is an icon, not a logo and not a hero. It needs to read at 80 to 120 pixels and signal what the ad is about. Use one geometric concept per ad group (so both A and B variants of an ad group share the same image, since the variation tests copy not creative). For the full icon concept library, design principles, and brand color defaults, read `references/icon-design.md`.

If the brand has known colors, use those. Otherwise default to dark background, white primary element, single accent color element. A reasonable default accent is a saturated orange or another high-attention color.

The image prompt should be ready to paste into Gemini, Imagen, or any modern image generator. Template:

```
Create a 1024x1024 square icon. Pure geometric composition, no text, no people, no photographic elements.

Background: solid [DARK_HEX].

Primary element: [CONCEPT-SPECIFIC SHAPE], filled in white (#FFFFFF), filling approximately 70% of the frame area, centered.

Accent element: [ACCENT-SPECIFIC SHAPE], filled in [ACCENT_HEX], positioned as a focal point inside or anchoring the primary element.

Style: minimalist, high-contrast, bold geometric, optimized for thumbnail display at 80-100 pixels. No gradients, no shadows, no glows, no fine details, no outlines unless explicitly specified. Reference aesthetic: Linear, Vercel, Anthropic icon style.
```

### Concept-to-shape library

When generating the image prompt for an ad group, pick the concept that best matches the intent the group serves, then plug the shape description into the template:

| Intent / Concept | Primary shape | Accent shape |
|---|---|---|
| Foundation, base, start, beginning | Three stacked horizontal bars, growing wider toward bottom, rounded corners | Bottom bar in accent color, dominant width |
| Speed, velocity, fast delivery | A right-pointing chevron or forward triangle | A trailing dot or smaller chevron in accent |
| Modularity, components, units | Three hexagons clustered in a triangle formation | One hexagon in accent color, the other two white |
| Automation, agents, autonomous systems | A central circle with three or four radiating lines reaching toward smaller circles | The central node in accent color |
| Strategy, planning, structure | A 3x3 dot grid or geometric compass mark | One central or anchor dot in accent |
| Custom, tailored, assembled | Two interlocking squares with offset | The smaller square in accent |
| Durability, built to last | A solid square with thick weighted base bar | The base bar in accent |
| Outcomes, results, delivery | A filled chevron pointing right with a target circle behind | The chevron in accent, circle in white |
| Integration, connection, network | One central dot with four lines radiating to corner dots | Central dot in accent |
| Intelligence, AI, neural | An abstract neural-style geometric mark: three connected circles in triangle, with lines between | Connection lines in accent |
| Savings, value, discount | A solid circle with a thick downward arrow inside | The arrow in accent |
| Security, trust, protection | A solid shield outline filled white with a small geometric mark inside | The inner mark in accent |
| Growth, progress, scaling | Three vertical bars of increasing height, like a simple bar chart | The tallest bar in accent |
| Simplicity, minimalism, focus | A single solid circle or square centered in the frame | A smaller centered dot in accent |

If the user has a brand-specific visual system, prefer that over this library.

## Output format

Output the complete campaign as a single Markdown document the user can paste into their notes, share with their team, or process into the ChatGPT Ads UI manually. Use the structure below.

```markdown
# Campaign: [Campaign Name]

**Primary goal:** [from interview]
**Language:** [from interview]
**Destination URL pattern:** [base URL with UTM template]
**Suggested budget:** [if provided]

## Ad Group 1: [Intent name]

### Context hints
- [hint 1]
- [hint 2]
- [hint 3]
- [hint 4]
- [hint 5]

### Ad 1A
- **Headline** (XX chars): [text]
- **Description** (XX chars): [text]
- **Display URL:** [URL with UTM tags]
- **Image prompt:** see below

### Ad 1B
- **Headline** (XX chars): [text]
- **Description** (XX chars): [text]
- **Display URL:** [URL with UTM tags]
- **Image prompt:** same as 1A (shared image for A/B copy test)

### Image prompt for Ad Group 1
```
[Full image prompt, ready to paste into Gemini/Imagen]
```

## Ad Group 2: [Intent name]
... (same structure)
```

Continue for all ad groups.

## After generation

After delivering the campaign document, offer two follow-ups:

1. Generate the icons. If the user wants the icons created directly instead of going to Gemini, offer to produce them as SVG/PNG using the concept-to-shape library, sized 1024x1024 with the brand's dark background and accent color.

2. Refine the copy. Offer to iterate on any specific ad's headline or description if the user wants alternatives.

## Voice and writing rules

When writing the campaign document and the ad copy itself:

- Never use em dashes. Use commas, colons, or sentence breaks.
- Do not use the rule of three. Two beats lands harder than three at 35 characters.
- Avoid filler verbs: "discover", "unlock", "transform", "revolutionize", "elevate", "leverage".
- Avoid abstraction nouns: "solutions", "experiences", "journeys", "ecosystems".
- Prefer concrete over abstract. "10 minutes" beats "fast". "Used by 500 teams" beats "trusted by leaders".
- Brand name in copy is wasted budget. The advertiser's logo appears in the ad corner automatically. Use those 35 characters for value, not brand repetition.
- If the user has loaded a brand voice or style skill, prefer those rules over the defaults above.

## Reference: ChatGPT Ads platform mechanics

Brief recap of platform mechanics the user may ask about during the interview:

- Ads currently appear only to ChatGPT free-tier users. Plus, Team, and Enterprise users are ad-free.
- Two main ad formats exist: SearchGPT sponsored results and conversational ads at the bottom of chat responses.
- The "Ask ChatGPT about this ad" engagement format lets users query the ad via a knowledge base the advertiser configures. If the user is interested in this, suggest preparing the knowledge base separately (top FAQs, pricing, use cases, objection handling).
- Self-serve access opened broadly in 2026 after an enterprise-only pilot. Pricing and audience syncing capabilities continue to evolve.

If the user has specific platform questions Claude doesn't have current answers for, suggest checking the OpenAI advertiser documentation directly.
