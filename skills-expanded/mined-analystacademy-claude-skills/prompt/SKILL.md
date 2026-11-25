---
name: prompt
description: Build a great prompt through a conversational interview. Use this skill whenever the user wants help writing, improving, or crafting a prompt — including phrases like "help me write a prompt", "I need a prompt for", "how do I prompt Claude to", "make me a prompt that", "I want to prompt an AI to", "create a prompt for", or any time the user describes a task they want an AI to do and seems to want help framing it. Even if they just describe a task vaguely and seem unsure how to ask for it — this skill applies. Trigger it early and often.
---

# Prompt Builder Skill

Help the user craft a high-quality, ready-to-use prompt through a friendly, one-question-at-a-time conversation. At the end, output only the finished prompt — no explanation, no preamble.

---

## Core Philosophy

A great prompt gives Claude (or any LLM) exactly what it needs to succeed:
- **Role / persona** — who should Claude be?
- **Task** — what exactly should it do?
- **Context** — what background info does it need?
- **Output format** — what should the result look like?
- **Constraints** — what should it avoid or keep in mind?
- **Tone** — what voice or style is appropriate?
- **Examples** — any few-shot examples to anchor the output?

Not every prompt needs all of these. Your job is to figure out which ones matter for *this* task and ask about those — skipping what's irrelevant.

---

## Conversation Flow

### Step 1 — Open with the task

Always start with one question:

> "What do you want the prompt to accomplish? Just describe it naturally — I'll ask follow-ups from there."

Listen carefully. From the answer, infer:
- The **task type** (see below)
- What information you already have vs. what's still missing

### Step 2 — Ask task-specific follow-ups

Ask one question at a time. Never ask two questions in the same message. After each answer, decide what the single most important missing piece is, and ask about that next.

Use the task type to guide which follow-ups matter most:

#### Writing / Content Creation
Priority questions (in rough order):
1. Who is the audience?
2. What tone or voice? (formal, casual, punchy, warm, etc.)
3. Approximate length or format?
4. Any specific things to include or avoid?
5. Do you have an example of the style you're going for?

#### Coding / Technical
Priority questions:
1. What language, framework, or stack?
2. What should the code do exactly — any edge cases to handle?
3. Should it explain its reasoning, or just output the code?
4. Any constraints (performance, libraries, style guide)?
5. What level of detail in comments/explanation?

#### Analysis / Research
Priority questions:
1. What's the source material — will they paste it in, or is it a general question?
2. What kind of output — summary, comparison, bullet points, pros/cons?
3. How deep vs. how concise?
4. Any specific angle or lens to analyze through?

#### Brainstorming / Ideation
Priority questions:
1. How many ideas? Any quantity target?
2. Should ideas be practical/realistic or wild/creative?
3. Any constraints on the ideas (budget, timeline, audience)?
4. What format — list, short descriptions, ranked?

#### Roleplay / Persona
Priority questions:
1. Who or what should Claude be playing?
2. What's the scenario or setting?
3. Any rules for how to stay in character?
4. What's the user's role in the interaction?

#### Data / Formatting Tasks
Priority questions:
1. What's the input format?
2. What's the desired output format?
3. Any transformation rules or edge cases?

---

### Step 3 — Fill in universal best practices

Once you have the task-specific info, check if these universal elements are still missing and worth asking about:

- **Role**: Would giving Claude a specific persona improve the output? (e.g., "Act as a senior UX designer") — ask if unclear.
- **Examples**: Would a few-shot example help? Ask: *"Do you have an example of the kind of output you're hoping for?"*
- **Format**: If the output format hasn't come up and it matters, ask.
- **Constraints**: If there are obvious things to avoid that haven't been mentioned, ask once.

Don't ask about things that are clearly irrelevant. A prompt for summarizing a contract doesn't need a tone question.

---

### Step 4 — Know when to stop

Stop asking when you have enough to write a genuinely good prompt. Usually 3–6 questions is enough. If you have the key pieces, don't drag it out.

Signal the end naturally:
> "Got it — let me put that together for you."

---

### Step 5 — Output the prompt

Output **only the finished prompt**. No explanation of what you did. No "here's your prompt:". Just the prompt itself, ready to copy and use.

#### Prompt construction best practices:

- **Lead with role if helpful**: "You are a [role] with expertise in [domain]."
- **State the task clearly and specifically**: Use action verbs. "Write", "Analyze", "Extract", "Generate".
- **Provide context inline**: Don't assume — include what the user told you directly in the prompt.
- **Specify format explicitly**: "Respond in bullet points." / "Keep your response under 200 words." / "Use markdown headers."
- **Add constraints as negatives when useful**: "Do not include..." / "Avoid..."
- **Use XML tags for complex inputs**: If the prompt will have a document or data pasted in, use `<document>`, `<data>`, or `<context>` tags with a placeholder like `[PASTE HERE]`.
- **Invite reasoning when appropriate**: For analytical tasks, add "Think through this step by step before answering."
- **Be specific, not vague**: "Write a 3-paragraph blog intro" beats "Write something engaging."

#### Format the prompt cleanly:
- Use line breaks between logical sections
- Use XML tags for any user-supplied content blocks
- Bold is fine for section labels if the prompt is long
- Keep it as concise as possible while being complete

---

## Example Interaction

**User**: Help me write a prompt

**Claude**: What do you want the prompt to accomplish? Just describe it naturally — I'll ask follow-ups from there.

**User**: I want Claude to review my cover letters and give me feedback

**Claude**: Who's the audience for these cover letters — what kinds of roles or industries are you applying to?

**User**: Tech jobs, mostly product management roles

**Claude**: Got it. Should the feedback focus on anything specific — like storytelling, conciseness, matching the job description — or do you want a well-rounded review?

**User**: Well-rounded, but I especially want to know if I'm being too generic

**Claude**: One more: how much feedback is useful — a few key bullets, or a detailed breakdown section by section?

**User**: A few key bullets, I don't want to be overwhelmed

**Claude**: Got it — let me put that together for you.

---

*Output:*

You are an expert career coach who specializes in helping candidates land product management roles at tech companies. I'm going to share a cover letter with you.

Review it and give me 3–5 bullet points of honest, actionable feedback. Focus especially on whether the letter sounds generic — flag any phrases or sections that could have been written for any job rather than this specific one. Also note any other significant strengths or weaknesses.

Be direct and specific. If something isn't working, say so clearly and explain why.

<cover_letter>
[PASTE YOUR COVER LETTER HERE]
</cover_letter>
