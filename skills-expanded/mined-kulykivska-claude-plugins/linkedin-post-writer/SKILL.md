---
name: linkedin-post-writer
description: >
  Use this skill whenever the user wants to write, draft, or improve a LinkedIn post — especially when the goal is maximum reach, impressions, or engagement. Trigger for requests like "write a LinkedIn post", "help me draft a post", "create a LinkedIn post about...", "write a LinkedIn post about...", "draft a post for my LinkedIn", "how should I post about X on LinkedIn", or any request to create social media content for LinkedIn. Also trigger when the user says "publish this post", "make a post", or asks for content that would fit a LinkedIn update. This skill encodes a data-driven formula derived from real post analytics — use it proactively any time LinkedIn post creation is involved.
---

# LinkedIn Post Writer — Proven High-Reach Formula

This skill is built from analysis of real LinkedIn post data for a Senior AI Engineer profile (956 followers, 28 110 impressions/year, +32% growth). The patterns below are what actually drove the highest-performing posts — not general best practices, but observed results from the account.

## The Core Post Formula

Every high-performing post follows this 4-part structure:

```
[HOOK] — First 1–2 lines. Visible BEFORE "...see more". This is everything.
[CONTEXT] — Why it matters right now, for this audience.
[VALUE] — Structured body with specifics: numbers, emojis as anchors, concrete data.
[QUESTION] — One open question inviting a reply. Required for comments.
```

The hook is the single biggest lever. If it doesn't create curiosity or tension, nothing else matters — the post won't be expanded.

**Hook patterns that work (ranked by observed impact):**
- Personal admission: *"3 weeks ago I deleted ChatGPT."* → 6 279 impressions
- Provocative contrast: *"The tech industry feels like a pool of inflatable balloons."* → 425 impressions, strong comments
- Project reveal: *"I built a small tool to fix a painfully annoying problem."* → 371 impressions, 6 likes
- Analogy hook: *"In Formula 1, speed is not created by pressure. It's created by structure."* → 659 impressions, 13 likes

**Hook patterns to avoid:**
- Starting with a question ("Have you ever wondered...") — feels generic
- Starting with the conclusion ("Here are 5 tips for...") — no tension, no reason to expand
- Starting with a company/product name — reads as an ad

---

## Topic Tiers (by observed engagement)

### Tier 1 — Maximum Reach (AI Hot Takes)
**35% of posts.** Highest impressions. Provocation + personal experience + current AI news.

Write about: LLM comparisons with real production experience, controversial opinions on AI tools (Claude vs GPT vs Gemini based on actual use), responses to major AI releases, "I switched from X to Y and here's what happened."

The key ingredient: take a clear personal stance. "I deleted ChatGPT" outperforms "here's a balanced comparison" by 40x. Neutrality kills reach.

### Tier 2 — Highest Engagement Rate (Analogy Posts)
**20% of posts.** Fewer impressions than Tier 1, but the most likes and comments per impression. These posts attract a loyal, high-quality audience.

Write about: a principle from Formula 1, sports, military, or history — then draw a sharp parallel to AI, engineering, or team work. Example: McLaren's pit stop concurrency → parallel agent architectures. The analogy must be earned, not forced.

Formula: short story from the non-tech domain → the engineering insight → "the same principle applies to..." → concrete example from AI/software → open question.

### Tier 3 — Trust Builders (Personal Project/Tool Reveals)
**25% of posts.** Moderate reach, but strongest conversion to followers and DMs. These are the posts that make people hit "Follow."

Write about: something you actually built, debugged, or shipped — with real numbers, real failure modes, and what you learned. Show the messy middle, not just the result.

Key: the post must include at least one specific number, error message, or architectural detail. Vague project posts don't convert.

**Make the substance the topic, not the process metrics.** The post is about *what you implemented, discovered, or fixed* — a feature, a bug's root cause, an integration gotcha, a modeling decision. It is NOT about how the work was done with an AI assistant.

❌ "Just wrapped a 64-message Claude session debugging my F1 race predictor."
❌ "44 messages with Claude analyzing the pipeline."
❌ "After a long debugging session with Claude, I finally shipped X."

Why these fail: message counts and session lengths measure effort spent talking to a tool, not value created for the reader. They tell the audience nothing they can learn from or react to. Lead with the finding instead:

✅ "My F1 predictor was leaking qualifying data into the training set — here's how I caught it."
✅ "Turns out my feature-importance ranking was dominated by a column that didn't exist at inference time."
✅ "Integrating the timing API, I hit a timezone bug that silently shifted every lap by an hour."

Rule of thumb: if a sentence describes the conversation with Claude/ChatGPT (how many messages, how long the session, that an AI helped), cut it and replace it with the technical thing you actually found or built. The reader cares about the *what* and the *why*, never the message log.

### Tier 4 — Industry Commentary
**15% of posts.** Works when you have a clear, non-obvious opinion and are willing to defend it. Generates comments from disagreers and fans alike.

Write about: what's broken in how teams use AI, undervalued fundamentals, what everyone gets wrong about X, honest post-mortems.

Avoid: crypto commentary, niche debugging guides without a broader insight, pure how-to content without a personal story.

---

## Style Rules

**Voice:** Always first person. "I built", "I deleted", "I noticed", "I was wrong about". Impersonal posts ("teams should...") underperform personal ones by 3–5x.

**Structure inside the post:**
- Use emoji as visual anchors for sections (⚡ 🔴 ✅ ⚠️ 🔧 💡) — they allow skimming on mobile
- Keep paragraphs to 1–3 lines max — LinkedIn's mobile feed punishes walls of text
- If listing things, use 4–7 items. More than 7 loses readers before the CTA

**Numbers and specifics matter:** "MAE dropped from 4.5 to 3.0" is 10x more credible than "accuracy improved." Use real data from your work whenever possible.

**Length:** 150–300 words is the sweet spot. Longer posts only work when the hook is very strong and every paragraph earns its place. Under 100 words risks looking low-effort.

**Hashtags:** Max 3, always at the very end, never inline in the text. LinkedIn treats inline hashtags as a spam signal.

**Links:** Never in the post body — the LinkedIn algorithm suppresses posts with external links. Put links in the first comment instead, and mention at the end of the post: "link in comments ↓"

---

## Media Guidance

| Format | When to use | What to create |
|--------|-------------|----------------|
| **1 image (best)** | Most posts | Terminal/code screenshot with caption; comparison table; analytics dashboard; architecture diagram |
| **Infographic card** | Hot takes, comparisons | One clear idea per image. Dark or LinkedIn-blue background. Large font, minimal text. Canva/Figma. |
| **PDF carousel** | Deep guides, series | 3–7 slides. First = hook slide. Last = CTA. Boosts dwell time. |
| **Video** | Product demos, before/after | Under 60s. Subtitles are mandatory (90% watch without sound). First 3 seconds must hook. |
| **No media** | Only for exceptionally strong hooks | Risky — algorithm favors posts with media. Use rarely. |

For code screenshots: use Carbon.sh or Warp with Dracula/One Dark theme. Add a one-line caption on the image.

For architecture diagrams: Mermaid (built into Claude), Excalidraw, or draw.io. LinkedIn reads diagrams as high-value content.

---

## Post Output Format

When writing a post, always output:

1. **THE POST** — ready to copy-paste, with emoji, structure, and question
2. **HOOK ANALYSIS** — one sentence on why the opening line should work
3. **RECOMMENDED MEDIA** — specific description of what image/graphic to create or attach
4. **BEST TIME TO POST** — Tue/Thu/Sat, 8–14:00 PT (San Diego time)

If the user gives you a topic, identify which tier it belongs to and apply the corresponding formula. If the topic fits Tier 1 or Tier 4, push for a stronger, more opinionated angle — the data consistently shows that neutral posts underperform.

---

## Quick Reference: What to Avoid

- ❌ Starting with "I'm excited to announce..."
- ❌ Crypto commentary (wrong audience for AI/engineering profile)
- ❌ Pure technical how-to without a story (92 impressions vs 6k+)
- ❌ Message counts / session length as the hook or topic ("64-message debugging session", "44 messages with Claude") — they measure effort, not value. Lead with the feature or finding instead.
- ❌ Neutral tool comparisons without taking a side
- ❌ Links in the post body (suppressed by algorithm)
- ❌ More than 3 hashtags
- ❌ Posting without an image (except exceptionally strong hooks)
- ❌ Questions as hooks ("Have you ever...")
