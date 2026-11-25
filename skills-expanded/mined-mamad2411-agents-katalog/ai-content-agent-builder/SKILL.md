# AI Content Agent Builder

Build your first AI content agent in 10 minutes — the system that writes, drafts, and repurposes your LinkedIn content so you don't have to. By Josh Sanders.

## 9-Step Build Process

### Step 1 — Pick One Content Task
Stop trying to automate everything. Pick one painful, predictable content step.

- Choose the part of your content process you repeat every week with the same steps
- Examples: Researching post topics, repurposing posts into newsletters, writing first drafts
- Define success in one sentence: "Given X, the agent should output Y so that Z happens"

> **Best Practice:** Start with the step that consumes you the most. The more predictable the task, the better the agent performs.

### Step 2 — Map It Like a Process
Turn your content task into 4–7 clear steps before touching any tool.

```
Topic → Research → Draft → Format → Output
```

- Write it as a simple flow
- Mark which steps are rules-based (which need reading/writing, and which need your feedback)
- If you can explain your post process to a new hire in 5 mins, you can build the agent

> **Best Practice:** Write the process on paper before opening any platform. A content agent built from a clear process consistently outperforms one built from a vague idea.

### Step 3 — Choose Your Platform

| No or low code | Developer friendly |
|---------------|-------------------|
| OpenAI Agent Builder | LangChain |
| Zapier | LangGraph |
| Make | OpenAI Agents SDK |
| n8n | CrewAI |

You only need 3 things to start: Access to a strong model, tool calling, and basic logs.

> **Best Practice:** Pick the simplest option that handles your use case. Starting simple is the right call, even if it does feel like a shortcut. You can migrate later when your requirements grow.

### Step 4 — Define Inputs, Outputs, and Tools
Give the agent a clear content brief.

- **Inputs:** A topic, URL, transcript, set of talking points
- **Outputs:** A drafted LinkedIn post, a list of hooks, a repurposed newsletter section
- **Tools:** Search tool for research, writing tool for drafts, formatting tool for output

> **Best Practice:** Vague inputs = vague content. The more specific your brief, the less editing the output needs.

### Step 5 — Write the Job Description
Write the brain. This is where your voice lives.

```
Role: "You're a LinkedIn content strategist writing for a founder in [Niche]."
Boundaries: Never invent statistics, use generic phrases or corporate tone.
Style: Short paragraphs, strong hooks, direct language, no motivational filler.
```

Paste in 2 or 3 of your best posts to show it exactly what good looks like.

> **Best Practice:** Spend the most time here. A well-written system prompt is the difference between an agent that sounds like you vs one that sounds like everyone else.

### Step 6 — Add Memory and Context
Stop the agent producing generic content every time.

- **Conversation state:** Pass recent posts and performance data so it knows what is working
- **Brand memory:** Store your tone of voice, ICP, and positioning
- **Topic memory:** Connect a document store of your angles, ideas, and past posts

> **Best Practice:** Ask yourself: What does this agent need to remember to produce content that sounds like me? Add only what answers that question.

### Step 7 — Add Guardrails
Make it safe enough to trust with your brand voice.

- Any draft going directly to publishing must pass through human review first
- Never invent data, or use phrasing that conflicts with brand voice
- Flag any draft that feels off-brief rather than guessing at what you meant
- Log every output so you can track quality over time

> **Best Practice:** Any post that goes out under your name should have your eyes on it before it goes live, especially while the agent is new. Trust is built through consistent quality.

### Step 8 — Wrap It in a Simple Interface
Make it easier to use than opening a blank document.

- One input field: Paste your topic, URL, or talking points
- One run button
- Keep it to 2 clicks maximum from idea to first draft

> **Best Practice:** If accessing the agent takes more effort than opening a Google Doc, it will not become a habit. Friction kills systems, so remove it.

### Step 9 — Test on 5 Real Posts
Catch quality issues before they reach your audience.

- Run the agent on 5 posts you have already written and published
- Score 3 things: **How close the tone is to yours**, hook strength, and editing time needed
- Tighten the system prompt wherever the output falls short

> **Best Practice:** Use your own published posts as test cases, instead of random ones. If it passes 5 real posts cleanly, you can trust it with your live content workflow.

## LinkedIn Content Agent System Prompt Template

```
You are a LinkedIn content strategist writing for [YOUR NAME], a [YOUR ROLE] in [YOUR NICHE].

VOICE & STYLE:
- Short paragraphs (1–2 sentences max)
- Strong hooks that create curiosity or make a bold claim
- Direct language, no corporate speak, no motivational filler
- [PASTE 2–3 EXAMPLE POSTS]

RULES:
- Never invent statistics or data
- Never use generic phrases like "In today's fast-paced world"
- Flag if the input is too vague to write a quality post
- Always end with a call to action or question

INPUT FORMAT:
Topic or talking points: [USER INPUT]
Goal of post: [awareness / engagement / lead gen]

OUTPUT FORMAT:
Hook (line 1)
Body (3–5 short paragraphs)
CTA (1 sentence)
Also provide: 3 alternative hooks to test
```

## The Agent Stack (Minimal)

```
Input: Topic / URL / transcript
   ↓
Research tool (web search or doc retrieval)
   ↓
Draft tool (LLM with system prompt)
   ↓
Format tool (structure + length check)
   ↓
Output: LinkedIn post draft + 3 hook variants
   ↓
Human review gate → Publish
```
