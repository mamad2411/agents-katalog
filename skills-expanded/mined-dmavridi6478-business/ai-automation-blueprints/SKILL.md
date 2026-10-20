---
name: ai-automation-blueprints
description: Eight ready-to-build AI automation blueprints for Make.com or n8n — inbound AI voice call agent, B2B lead generation, AI UGC ad deconstruction, faceless short-form video, content creation agent, multilingual FAQ chatbot, YouTube idea generator, and AI avatar video — each with trigger, node sequence, tools, credentials, the LLM prompt to drop into the AI node, and the compliance/cost risks to check first. Use when the user wants to build one of these automations, asks "which automation should I build first", wants a node map for Make/n8n, or wants to sell one of these as a service. Hand off to `n8n-agent-builder` for the JSON skeleton.
---

# AI Automation Blueprints (Make.com / n8n)

Source: uploaded carousel "Best 8 AI Automation Tools" (@theromanknox,
skool.com/knox), pages 1–5. The carousel shows screenshots of workflows
without templates or JSON; the node maps below are transcribed from those
screenshots, and the prompts, credentials and risk notes are added here.

**Read first — what the carousel does not tell you:**
- It is a lead magnet for a paid community. Performance claims on it
  ("10 calls simultaneously, unlimited daily capacity", "UGC 10× faster")
  are the author's marketing, not measured benchmarks. Treat as unverified.
- Make.com and n8n are **orchestrators**, not the AI. Every blueprint below
  also needs paid API accounts (OpenAI, HeyGen, Apify, a video model, etc.).
  Running cost is dominated by those APIs, not by Make/n8n.
- Four of the eight touch personal data or automated contact with people.
  In the EU (GDPR, ePrivacy, AI Act Art. 50 transparency) that is a legal
  design constraint, not a footnote. See the risk column.

## Pick-order (by value-to-effort for a small B2B / services business)

| Rank | Blueprint | Why this order |
|---|---|---|
| 1 | 06 Multilingual FAQ chatbot | Lowest risk, answers from your own knowledge base, immediate time saving |
| 2 | 07 YouTube idea generator | Read-only, cheap, no personal data |
| 3 | 05 Content creation agent | High leverage — but only with a human approval gate before publish |
| 4 | 02 Lead generation AI | High value, highest legal exposure in the EU — build only with a lawful basis |
| 5 | 01 AI voice call agent | Powerful, but real-time voice cost and disclosure obligations |
| 6–8 | 03 UGC spy, 04 faceless video, 08 avatar | Consumer/creator-economy plays; low fit for B2B/medtech unless that is the business |

## The eight blueprints

### 01 — AI voice call agent (inbound, e.g. hotel / clinic reception)
- **Trigger:** Custom webhook (telephony provider: Twilio / Vapi / Retell) → call starts.
- **Nodes:** Webhook → Call agent (OpenAI Realtime) → Router, three branches:
  - Check availability (tool) → Book appointment (Google Calendar)
  - Handle questions (AI assistant) → Send confirmation (Gmail)
  - Escalate to human (router) → Create CRM contact (HubSpot)
- **Credentials:** telephony, OpenAI, Google Calendar, Gmail, HubSpot.
- **Risk:** must disclose the caller is talking to an AI (EU AI Act Art. 50); call recording needs consent; realtime voice is billed per minute — cap concurrent calls.

### 02 — Lead generation AI (B2B cold outreach)
- **Trigger:** Schedule (daily).
- **Nodes:** Scrape leads (Apify) → Research & enrich (OpenAI) → Qualify leads (Filter) → Send outreach (Gmail) → Follow-ups (Scheduler).
- **Credentials:** Apify, OpenAI, Gmail/Workspace, a sheet/CRM for state.
- **Risk:** scraping personal data + unsolicited email = GDPR Art. 6 lawful-basis and ePrivacy issues in the EU; Gmail sending limits and domain reputation. Use `outbound-campaign-brief` (human approval + send cap) rather than full autopilot.

### 03 — AI UGC ads spy generator
- **Trigger:** Form / manual — paste a viral ad link or upload a video (TikTok / Instagram / YouTube).
- **Nodes:** Input → Analyze ad (extract key elements) → Get insights (Gemini: hook, script, format) → Generate prompts (5 Sora 2 video prompts) → Create UGC (brand-specific) → Output.
- **Credentials:** Gemini (video understanding), OpenAI / Sora (or another video model), storage.
- **Risk:** deconstructing is fine; copying protected creative, faces or music is not. Synthetic "customer" testimonials presented as real are misleading advertising (EU UCPD) — label AI content.

### 04 — Animated faceless AI videos
- **Trigger:** Schedule or topic list.
- **Nodes:** Write video script (AI script generator, trending topics, custom prompt) → Create faceless video (AI avatars / stock footage / voiceover) → Publish to social (auto-posting, multi-channel, track performance).
- **Credentials:** LLM, TTS, stock/video generator, TikTok/Instagram APIs.
- **Risk:** platforms down-rank mass-produced AI content; auto-posting APIs are restricted. See `yt-faceless-channel`.

### 05 — Content creation agent
- **Trigger:** Schedule ("repeat automatically").
- **Nodes:** Topic research (trends & ideas) → Generate script (AI writing) → Create video (images / voice / edit) → Add captions (auto subtitles) → Publish (TikTok, Instagram, YouTube, LinkedIn, X).
- **Credentials:** LLM, media generation, each platform's API.
- **Risk:** "instant publishing" removes the human gate. Insert a human-approval step before Publish (see `governed-marketing-team` gate G1).

### 06 — Multilingual FAQ chatbot
- **Trigger:** User message (website widget / link).
- **Nodes:** User message → Language detection → GPT (FAQ answer, grounded in knowledge base) → Send reply in user's language → loop: handle follow-up questions.
- **Credentials:** LLM, website chat widget or WhatsApp/Messenger, knowledge base (docs / vector store).
- **Risk:** hallucinated answers. Ground on your FAQ only and answer "I don't know — here is a human" outside it. See `customer-faq-responder`, `rag-pipeline-architecture`.

### 07 — Viral YouTube video idea generator
- **Trigger:** Manual "Run automation" or weekly schedule.
- **Nodes:** Fetch top-performing videos (YouTube Data API) → Analyze content (titles, keywords, engagement) → Generate fresh ideas (AI) → Get actionable ideas (titles, angles, keywords).
- **Credentials:** YouTube Data API key, LLM, sheet/Notion for output.
- **Risk:** low. YouTube API quota (10,000 units/day default). See `youtube-niche-finder`, `yt-niche`.

### 08 — AI avatar generator (HeyGen + n8n)
- **Trigger:** Script input (sheet row / form).
- **Nodes:** Create script (AI generated) → Generate avatar (HeyGen) → Add voice & edit (AI voice) → Export video (ready to publish).
- **Credentials:** LLM, HeyGen API (paid, per-minute credits), storage.
- **Risk:** cloning a real person's face or voice needs their written consent; label as AI-generated.

## Prompts to drop into the AI node

Paste into the OpenAI / Claude node's system prompt. Replace `{{ }}` with n8n expressions or Make mapped fields.

**02 Research & qualify (lead gen)**
```
You are a B2B lead qualifier for {{company}}, which sells {{offer}} to {{ICP}}.
Given this lead record: {{lead_json}}
Return JSON only: {"fit_score": 0-10, "reason": "<one sentence>", "personal_hook": "<one specific, verifiable detail from the record, or null>", "disqualify": true|false}.
Disqualify if any of: {{disqualifiers}}. Never invent facts not present in the record.
```

**03 Ad deconstruction (UGC spy)**
```
Analyse this ad video. Return: 1) the hook in the first 3 seconds (verbatim + visual), 2) script structure as beats with timestamps, 3) format (UGC selfie / demo / skit / voiceover), 4) the emotional trigger, 5) CTA.
Then write 5 video-generation prompts that reuse the STRUCTURE (not the people, brand or music) for {{brand}} selling {{product}} to {{audience}}, in the brand voice: {{voice}}. Each prompt: subject, action, setting, camera, style, closing beat, max 80 words.
```

**05 Script (content agent)**
```
Write a {{length}}-second vertical video script on "{{topic}}" for {{audience}}.
Structure: hook (≤ 8 words, first 2 s) → 3 beats → CTA "{{cta}}".
Only use claims from this proof list: {{proof_rows}}. If a beat needs an unproven claim, drop the beat.
Output JSON: {"hook","beats":[...],"cta","caption","hashtags":[max 5]}.
```

**06 FAQ bot**
```
You answer customer questions for {{business}} using ONLY the FAQ below. Detect the user's language and reply in it.
If the answer is not in the FAQ, reply (in the user's language): "I don't have that answer — a colleague will contact you." and set "handoff": true.
Return JSON: {"language","answer","handoff": true|false}.
FAQ:
{{faq_text}}
```

**07 YouTube ideas**
```
Here are the top {{n}} videos in the niche "{{niche}}" from the last {{days}} days with views, likes and titles: {{videos_json}}.
1) Identify the 5 title patterns that over-perform (views vs channel average). 2) List 10 high-intent keywords. 3) Propose 10 new video ideas: title, angle, why it should work (cite the pattern), target keyword. No idea may copy an existing title.
```

**08 Avatar script**
```
Write a {{seconds}}-second talking-head script for an AI avatar presenting {{topic}} to {{audience}}. Conversational, first person, sentences ≤ 15 words, no stage directions, one CTA at the end. Language: {{language}}.
```

## How to build one

1. Pick a blueprint from the table above.
2. Run `/automation-blueprint <number or name> <platform: n8n|make>` for the build sheet.
3. For n8n JSON, hand the node map to `n8n-agent-builder`.
4. Test with 5 records and a spend cap before any schedule trigger goes live.

## Related
`n8n-agent-builder`, `n8n-claude-workflow`, `outbound-campaign-brief`,
`customer-faq-responder`, `yt-faceless-channel`, `ai-voice-tools`,
`governed-marketing-team`, `trigger-based-automation`, `self-healing-automation`.
