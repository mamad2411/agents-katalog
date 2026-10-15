---
name: tech-learning-guide
description: >
  Generate a comprehensive, structured learning guide for any technical topic or technology.
  Use this skill whenever a user wants to learn a new technology, programming language, framework,
  tool, or concept — even if they phrase it casually (e.g., "teach me Rust", "how do I get started
  with Kubernetes", "I want to learn React", "help me understand GraphQL", "give me a roadmap for
  learning Docker"). This skill covers concept identification and categorization, weekly study
  schedules, local dev setup, concept explanations with examples, exercises, popular libraries,
  project ideas, and resources. Trigger for any "how do I learn X", "roadmap for X", "getting
  started with X", "study plan for X", or "teach me X" request — even if they don't explicitly
  ask for a guide or roadmap.
---

# Tech Learning Guide Skill

Generate a complete, structured, opinionated learning guide for any technical topic. The guide
should feel like it was written by an experienced senior engineer who has taught the topic before
— practical, direct, and honest about what matters most.

## Output Structure

Produce the guide as a **rendered artifact** (`.md` file) with the following sections in order.
The tone should be warm, direct, and technically confident — avoid fluff and padding.

---

## Section 1 — Overview & Concept Map

Open with 2–3 sentences describing what the technology is and why it matters in today's ecosystem.
Then list all key concepts the learner needs to master, grouped into three tiers:

| Tier | Label            | What it means                                                               |
|------|------------------|-----------------------------------------------------------------------------|
| 🟢   | **Basics**       | Concepts a beginner must learn first; no prior knowledge of the tech needed |
| 🔵   | **Foundational** | Core concepts that form day-to-day working knowledge                        |
| 🔴   | **Advanced**     | Deep internals, production concerns, performance, or ecosystem integrations |

Format as a table or grouped list. Aim for 5–8 concepts per tier (15–24 total), but adjust
naturally for the scope of the technology. Don't pad artificially.

---

## Section 2 — Weekly Learning Schedule

Create a realistic week-by-week study plan. Assume **1–2 hours per day, 5 days/week**.
Structure:

- **Week N: [Theme]** — 2 sentence description of the week's focus
    - Day 1–5: specific daily objectives (1–2 sentences each)

Cover all three tiers across the schedule. Basics first, then Foundational, then Advanced.
Typical schedule length: 6–10 weeks depending on technology breadth. Be honest if some weeks
require more time (e.g., "this week is dense — budget extra time if needed").

---

## Section 3 — Local Development Setup

Provide concrete, copy-paste-ready instructions for getting a working local environment.
Include:

- **Prerequisites** (OS, required tools, versions)
- **Installation steps** (numbered, shell commands in code blocks)
- **Verify it works** — a minimal "hello world" command or snippet to confirm setup
- **Recommended IDE / editor** with key plugins or extensions
- **Useful dev tools** (linters, formatters, debuggers, local test runners)

Be opinionated. If one approach is clearly better for learning, say so.

---

## Section 4 — Concept Deep-Dives

For every concept listed in Section 1, provide a dedicated subsection:

```
### [Tier emoji] [Concept Name]

**What it is**: 2–3 sentence plain-language explanation.

**Why it matters**: 1–2 sentences on practical relevance.

**How it works**: Explanation with code example(s). For code-heavy concepts, show at least
one realistic example (not just "hello world"). For architectural concepts, use a short
diagram or analogy.

**Common pitfalls**: 1–3 bullet points of mistakes beginners make.

---
#### ✏️ Exercises

1. [Concrete, hands-on exercise — beginner friendly]
2. [Slightly harder exercise that builds on the first]
3. [Challenge exercise that combines this concept with a previous one]
```

Group the concepts under their tier heading:
`## 🟢 Basics`, `## 🔵 Foundational`, `## 🔴 Advanced`

---

## Section 5 — Popular Libraries & Ecosystem

Give a concise ecosystem map. For each major library or tool in the technology's orbit:

- **Name** + one-liner on what it does
- **When to use it** (2 sentences)
- A code snippet showing the simplest useful example (where applicable)

Aim for 6–10 entries. Group by category if the ecosystem is large (e.g., "Testing", "HTTP",
"ORM"). Don't list everything — list what a practitioner actually reaches for.

---

## Section 6 — Project Ideas

Provide exactly **3 project ideas**, progressing in complexity:

1. **[Small] Project Name** — 1–2 weeks. What you'll build, which concepts it exercises,
   why it's a good learning vehicle.
2. **[Medium] Project Name** — 3–5 weeks. Same format. Introduce more Foundational concepts.
3. **[Stretch] Project Name** — Open-ended. Brings in Advanced concepts and real-world
   concerns (auth, persistence, deployment, performance).

For each project, include:
- A brief feature list (3–5 bullet points)
- Key concepts practiced
- Optional: suggested tech stack to pair with

---

## Section 7 — What's Next

After mastering everything in this guide, where does the learner go? Provide:

- **2–3 adjacent technologies** to explore (with 1-sentence rationale each)
- **2–3 advanced topics** within the technology itself that weren't covered
- **1–2 community resources** to stay current (conference, newsletter, forum)

Frame this as an honest "graduation" — you've learned the fundamentals; here's the horizon.

---

## Section 8 — Resources

Curated reference list. Organize into categories:

- **Official Docs** — link + 1-sentence description
- **Books** — title, author, why it's recommended
- **Online Courses** — platform + course name, ideal for which learner level
- **Blogs / Sites** — name + what kind of content they publish
- **YouTube / Video** — channel or specific series, what makes it worth watching
- **Community** — Discord, Slack, forum, subreddit

Keep it tight — 3–5 entries per category max. Every entry should earn its place.

---

## Quality Guidelines

- **Be concrete**: No vague advice like "practice a lot." Say what to practice and how.
- **Be honest**: If a concept is genuinely hard or a common sticking point, say so.
- **Examples must run**: Any code snippet should be minimal but complete enough to actually
  execute or be understood in isolation.
- **Calibrate depth to the technology**: A guide for Bash scripting vs. distributed systems
  should feel different in depth and breadth.
- **No hallucinated resources**: Only include books, courses, and links you're confident exist.
  If unsure about a specific URL, name the resource without a link rather than guess.
- **Developer Advocate tone**: Write as a knowledgeable peer, not a textbook. First-person
  asides are fine ("I'd start with X before Y because...").

---

## Handling Broad vs. Narrow Topics

- **Very broad topic** (e.g., "cloud computing", "web development"): Narrow the scope in the
  intro. Tell the user what angle you're covering and why. Suggest they ask follow-up guides for
  adjacent areas.
- **Very narrow topic** (e.g., a single library method or niche tool): Scale down accordingly.
  A 10-week schedule for `Array.prototype.reduce` is absurd. Use judgment.
- **Version-sensitive technology**: Mention the version the guide targets at the top. Flag any
  areas where older versions differ significantly.

---

## References

- `references/schedule-templates.md` — Example schedule patterns for different technology scopes
  (language, framework, tool, concept). Read if you need calibration on schedule length/density.
- `references/concept-tiers.md` — Guidance on how to classify concepts into Basics / Foundational
  / Advanced for common technology categories.