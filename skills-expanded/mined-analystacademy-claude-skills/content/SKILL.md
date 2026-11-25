---
name: content
description: >
  Turn any content into 3-4 finished LinkedIn posts ready to publish. Use this skill whenever the user shares something and wants LinkedIn posts from it — a PDF, an email, a newsletter, a URL, pasted text, a report, or anything else. Trigger on phrases like "turn this into posts", "what can I post about this", "LinkedIn content from this", "post ideas", "what should I post", or any time the user shares a piece of content and seems to want to repurpose it for LinkedIn.
---

# Content → LinkedIn Posts

Turn any content the user shares into 3-4 finished LinkedIn posts, ready to publish.

> **Setup note:** This skill pairs with the `post` skill, which carries the user's voice profile. Make sure both are installed. References below assume both skills live under your skills directory (e.g. `~/.claude/skills/post/SKILL.md` and `~/.claude/skills/factcheck/SKILL.md`) — adjust the paths if yours are different.

---

## Step 1: Get the Content

Identify what the user has provided and handle accordingly:

**Pasted text or notes** — use directly from the conversation.

**PDF or uploaded file** — read the `pdf-reading` skill (if available) for extraction instructions before proceeding.

**URL or web page** — use `web_fetch` to retrieve the full page content.

**Email** — search Gmail using relevant terms from the user's description. Fetch the full thread.

**Newsletter** — if the user has a recurring newsletter they pull from, search Gmail for the sender address and fetch the most recent edition. Extract plain text body; ignore tracking pixels, unsubscribe links, and HTML artifacts.

**Nothing provided** — ask the user what content they'd like to repurpose, or default to whatever recurring source you've been set up to use.

---

## Step 2: Identify the Best 3-4 Angles

Read through the content and find the strongest raw material across these four angles. Not every piece will have all four equally — pick the best 3-4 total, don't force weak ones.

- **Hot take / opinion** — A claim or framing the user could stake a strong position on. Something that pushes back on conventional wisdom.
- **Surprising stat or data point** — A number that would stop someone mid-scroll and reframe how they think about a topic.
- **Practical tip** — A tool, framework, or piece of advice someone could apply immediately.
- **Story or narrative** — A real moment, case, or observation that opens a post in a human way.

---

## Step 3: Draft the Posts

**Critical rule: use the user's exact words wherever possible if they wrote the source** (newsletter, email, notes). Lift sentences, transitions, and analogies directly — don't paraphrase their phrasing into something blander. If the source is third-party (a PDF, article, URL), extract the core ideas and write in the user's voice using the `post` skill.

For each post:
- Open with the sharpest, most concrete line available — not a setup, not a broad statement
- Do not open with newsletter meta-framing ("This week's newsletter covers..." / "I wrote about this on the plane...")
- Stay inside the insight — the post should stand alone without any reference to the newsletter
- Use the voice profile from the `post` skill (read its SKILL.md before drafting)

Write full, un-hatcheted drafts first. Paragraph form. Do not pre-trim.

---

## Step 4: Run /factcheck on Any Posts with Stats

Before presenting, identify any posts containing statistics, named figures, or specific claims attributed to organizations or surveys. Run the `factcheck` skill on those posts (standard tier).

Read the `factcheck` SKILL.md and verify all checkable claims via web search.

Apply any corrections directly into the drafts before presenting. Note what was fixed and why — one line per fix, after the posts.

---

## Step 5: Present the Posts

Present all posts in full, ready to copy-paste. Label each with its angle type.

After the posts, include a single short note on any factcheck fixes applied.

Ask the user which (if any) they want to adjust, shorten, or take in a different direction.

---

## What NOT to do

- Do not open any post with a reference to the source ("This week's newsletter...", "I read a PDF that...", "In this report...")
- Do not paraphrase the user's phrasing into generic language — use their words when they wrote the source
- Do not run `hatchet` automatically — only shorten if asked
- Do not present post ideas before drafts — go straight to finished posts
