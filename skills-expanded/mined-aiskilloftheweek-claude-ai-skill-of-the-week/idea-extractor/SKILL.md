---
name: idea-extractor
description: Analyzes long-form content (transcripts, articles, interviews, webinars, podcast notes) and extracts the 3 best content ideas for any publishing platform — LinkedIn, Substack, blog, newsletter, podcast, YouTube, or other. Use this skill whenever the user provides a transcript, long-form content, or any extended text and wants to identify the best post ideas, extract content angles, mine a transcript for social content, or turn a recording/article into post ideas. Trigger on phrases like "extract ideas from this", "find post ideas in this transcript", "what can I post from this", "mine this content for ideas", "turn this transcript into posts", "help me repurpose this content", or any time the user pastes a long text and asks what to do with it for content purposes — regardless of platform. Always use this skill when repurposing long-form content into post ideas, even if the user phrases it casually.
---
 
# Idea Extractor
 
Analyze long-form input content and extract the 3 best content ideas, tailored to the user's target platform, voice, positioning, and audience.
 
## Step 1 — Gather User Context
 
Before extracting ideas, you need to understand who is creating the content, for whom, and where it will be published.
 
**Check available context first**: Look for any skill files, memory, or documents that contain information about the user's:
- UVP (Unique Value Proposition)
- Services or products offered
- Tone of voice and writing style
- Positioning and niche
- Goals and objectives
- Target audience
- Value delivered to the market
 
**Always ask the target platform**, even if other context is available — this is essential to shape the format and angle of each idea:
 
> "Which platform(s) are these ideas for? (e.g., LinkedIn, Substack, blog, newsletter, YouTube, podcast, Instagram...)"
 
**If other context is also missing**, ask the following before proceeding:
 
1. Who is your target audience? (job title, level of expertise, main pain points)
2. What is your core positioning or UVP? (what makes you different)
3. What tone do you use? (educational, contrarian, personal, data-driven, etc.)
4. What action do you want readers to take after reading?
 
Do not proceed to Step 2 until you have the target platform confirmed and enough context to personalize the output.
 
---
 
## Step 2 — Analyze the Content
 
Read the entire long-form input carefully. While reading, identify:
 
- Key themes, insights, and frameworks
- Notable achievements, results, or data points
- Interesting lessons, mistakes, or turning points
- Counterintuitive or contrarian perspectives
- Concrete examples, case studies, or anecdotes
- Strong quotes or statements worth highlighting
 
---
 
## Step 3 — Select the 3 Best Post Ideas
 
From all the ideas you identified, select the top 3 based on these criteria:
 
1. **Relevance to the target audience** — Does it speak to their pain points or goals?
2. **Value potential** — Will it educate, inspire, or shift a perspective?
3. **Novelty** — Is it a fresh angle or non-obvious insight?
4. **Platform fit** — Does it match the formats and conventions of the target platform? Shape the angle accordingly:
   - **LinkedIn**: insight posts, personal stories, contrarian takes, giveaways, frameworks
   - **Substack / newsletter**: deep dives, step-by-step guides, curated lists, opinion pieces
   - **Blog / SEO**: how-to articles, comparisons, evergreen tutorials
   - **YouTube / podcast**: narrative stories, interviews, before/after case studies
   - **Instagram / TikTok**: visual hooks, short lessons, behind-the-scenes moments
5. **Alignment with user positioning** — Does it reinforce the user's authority and voice?
 
---
 
## Step 4 — Output the Results
 
Present the 3 selected ideas using this exact XML structure:
 
```xml
<post_ideas>
 
  <topic1>
    <title>[Concise, compelling title for the post]</title>
    <description>[Explain what the post is about, why it would resonate with the target audience, and what angle or hook to use. Be specific and detailed — give the writer everything they need to produce a strong post.]</description>
    <key_information>
      - [Data point, statistic, or key fact from the content]
      - [Insight, lesson, or framework extracted from the content]
      - [Supporting example or context]
      - [Any other relevant information for writing the post]
    </key_information>
    <quotes>[Relevant verbatim quotes from the source content that could be used or referenced in the post. Leave empty if none.]</quotes>
  </topic1>
 
  <topic2>
    <title>[Concise, compelling title for the post]</title>
    <description>[...]</description>
    <key_information>
      - [...]
    </key_information>
    <quotes>[...]</quotes>
  </topic2>
 
  <topic3>
    <title>[Concise, compelling title for the post]</title>
    <description>[...]</description>
    <key_information>
      - [...]
    </key_information>
    <quotes>[...]</quotes>
  </topic3>
 
</post_ideas>
```
 
---
 
## Guidelines
 
- **Stay faithful to the source**: Only extract ideas that are genuinely supported by the content. Do not invent angles not present in the input.
- **Prioritize specificity**: Vague ideas ("talk about growth") are not useful. Be concrete ("How we 3x'd trial-to-paid conversion by fixing the onboarding email sequence").
- **Think like an editor**: Choose ideas that will make the audience stop scrolling, not just ideas that summarize what was said.
- **Adapt to the confirmed platform**: Each idea's description should reference the specific format, length, and conventions that work on the target platform. A LinkedIn post, a Substack essay, and a YouTube script all require different angles from the same raw material — make that explicit.
- **Reflect the user's voice**: The description and key information should sound like they belong to the user's brand, not generic content advice.
 
