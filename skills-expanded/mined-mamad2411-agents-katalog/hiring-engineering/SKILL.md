---
name: hiring-engineering
version: 1.0.0
min_mindforge_version: 10.3.0
status: stable
triggers: hiring engineer, technical interview design, coding challenge creation, system design interview rubric, candidate evaluation rubric, hiring pipeline engineering, technical assessment, technical interview scorecard, take-home assignment design, hiring committee, engineering recruitment, technical screen design
compose:
  - technical-interview-design
---

# Hiring Engineering

## When this skill activates

This skill activates when designing technical interviews, creating coding challenges, evaluating engineering candidates, building interview scorecards, designing take-home assignments, or participating in hiring committees. It applies to senior engineers, tech leads, and engineering managers responsible for growing their teams.

## Mandatory actions when this skill is active

### Before starting the hiring process

1. **Define the role requirements explicitly** — List must-have skills (e.g., 3+ years backend Go, experience with Postgres, strong testing discipline) and nice-to-have skills (e.g., distributed systems, Kubernetes). Vague requirements attract the wrong candidates.
2. **Identify assessment dimensions** — What are you evaluating? Common dimensions: coding ability, system design, debugging, communication, collaboration, problem-solving, learning agility. Map each interview stage to 1-2 dimensions.
3. **Calibrate the bar** — Look at your current top performers. What skills/behaviors do they exhibit? Use that as the hiring bar. Don't hire people you wouldn't be excited to work with.
4. **Design the interview pipeline** — Typical stages: recruiter screen → technical phone screen → take-home or live coding → system design → behavioral → hiring committee. Each stage filters for different signals.

### During interview design

#### Technical Phone Screen (30-45 minutes)

- **Goal** — Validate basic coding competency before investing in longer interviews. Filter out candidates who can't code at all.
- **Format** — 1-2 small problems (e.g., manipulate a string, traverse a tree). Real-time coding in a shared editor (CoderPad, Replit).
- **Pitfall** — Don't make it a LeetCode grind. Focus on practical problems similar to your day-to-day work, not algorithmic olympiad questions.
- **Scoring** — Pass/Fail. Pass if candidate writes working code with prompting. Fail if they can't produce a solution even with hints.

#### Coding Challenge (Take-Home or Live Coding)

**Take-Home Assignment Design:**
- **Scope** — Should take 2-4 hours. Respect candidate's time. Projects that take 8+ hours are disrespectful.
- **Realism** — Design problems that resemble actual work. Building a mini REST API is better than "implement quicksort."
- **Evaluation criteria** — Code correctness, test coverage, edge case handling, documentation, architecture. Provide a rubric upfront.
- **Pitfall** — Don't make it too open-ended. Candidates will over-engineer. Give constraints: "Use language X, don't spend more than Y hours."

**Live Coding Session:**
- **Duration** — 45-60 minutes. One medium-difficulty problem.
- **Interactivity** — Treat it as pair programming, not an exam. Ask clarifying questions, give hints if stuck, discuss tradeoffs.
- **What to look for** — Can they break down the problem? Write clean code? Test edge cases? Communicate their thought process?
- **Pitfall** — Don't stay silent while they code. Engage. The goal is to simulate real collaboration.

#### System Design Interview (60 minutes)

- **Goal** — Assess candidate's ability to design scalable, maintainable systems. Evaluates architectural thinking, tradeoff analysis, and communication.
- **Format** — Open-ended problem: "Design a URL shortener" or "Design a chat system." Candidate drives the conversation.
- **What to evaluate** — Requirements gathering, high-level architecture, component design, data model, API design, scale considerations, tradeoffs.
- **Pitfall** — Don't expect candidates to know your exact tech stack. If they propose Redis but you use Memcached, that's fine. The pattern matters, not the tool.
- **Hints to look for strength** — Do they ask clarifying questions? Do they consider scale and failure modes? Do they make tradeoffs explicit?

#### Behavioral Interview (45 minutes)

- **Goal** — Assess collaboration, communication, adaptability, conflict resolution, and learning agility.
- **Format** — STAR questions (Situation, Task, Action, Result): "Tell me about a time you disagreed with a teammate. How did you resolve it?"
- **What to evaluate** — Self-awareness, ownership, growth mindset, team orientation, handling of ambiguity.
- **Pitfall** — Don't accept vague answers. Probe: "What specifically did you do?" "What was the outcome?" "What would you do differently next time?"

#### Debugging/Troubleshooting Interview (Optional, 45 minutes)

- **Goal** — Assess candidate's ability to diagnose and fix production issues. Especially valuable for senior hires.
- **Format** — Give candidate a broken codebase or system. Ask them to identify the issue and fix it.
- **What to evaluate** — Debugging process, use of tools (logs, debuggers, metrics), hypothesis testing, communication.
- **Pitfall** — Don't make it obscure. The bug should be findable with reasonable effort (30-40 minutes).

### During candidate evaluation

#### Scorecard Design

- **Use a consistent rubric** — Each dimension (coding, system design, communication) gets a 1-4 score: 1 = Strong No, 2 = No, 3 = Yes, 4 = Strong Yes. Define what each score means.
- **Provide evidence, not just scores** — Don't write "Communication: 3." Write "Communication: 3 – Candidate clearly explained their architecture choices and responded well to probing questions."
- **Avoid bias** — Don't let the candidate's similarity to you inflate scores. Evaluate against the rubric, not your personal preferences.
- **Distinguish between "not demonstrated" and "weak"** — If the candidate didn't have a chance to show a skill (e.g., debugging wasn't tested), mark it as "N/A," not a low score.

#### Hiring Committee Best Practices

- **All interviewers submit scorecards before the meeting** — Prevents groupthink. If everyone reads each other's feedback first, later voters anchor on early opinions.
- **Discuss discrepancies first** — If one interviewer gave a Strong Yes and another gave a No, discuss why before discussing the overall hire/no-hire decision.
- **Avoid "they're not a culture fit" as a veto reason** — That phrase often masks unconscious bias. Be specific: what behavior or value misalignment did you observe?
- **Use the "would you want this person on your team?" test** — If the answer is no, it's a no-hire. Hiring mediocre engineers lowers the bar and demoralizes high performers.

#### Red Flags in Candidates

- **Can't explain their own code** — If they wrote it but can't articulate the reasoning, they likely copy-pasted.
- **Blames teammates for failures** — "My team was slow, so the project failed." Red flag for collaboration and ownership.
- **Doesn't ask clarifying questions** — Jumps into coding without understanding requirements. Shows poor communication and product sense.
- **Over-engineers simple problems** — Proposes microservices for a CRUD app. Shows lack of pragmatism.
- **Dismissive of feedback** — When given a hint or suggestion, becomes defensive. Shows poor learning agility.

#### Green Flags in Candidates

- **Admits when they don't know** — "I haven't used Kubernetes, but here's how I'd approach learning it." Shows humility and learning agility.
- **Communicates tradeoffs clearly** — "Option A is faster but harder to maintain. Option B is slower but more reliable." Shows architectural maturity.
- **Writes tests without prompting** — Shows quality-first mindset.
- **Asks insightful questions** — About architecture, team culture, technical challenges. Shows genuine interest.
- **Handles ambiguity well** — When the problem is open-ended, they ask clarifying questions and propose a structured approach.

### After interviews

- **Debrief immediately** — Submit scorecards within 24 hours while memory is fresh. Delayed feedback loses fidelity.
- **Provide candidate feedback (if rejected)** — Not legally required, but considerate. Keep it high-level: "We were looking for more depth in system design." Don't critique their personality.
- **Track hiring pipeline metrics** — Pass rates at each stage, time to hire, offer acceptance rate, source of hire (referrals, LinkedIn, etc.). Optimize the bottlenecks.
- **Improve interview questions over time** — If a question doesn't differentiate strong vs weak candidates, retire it. Iterate based on hiring outcomes.

## Self-check before task completion

- [ ] Role requirements are explicit with must-have and nice-to-have skills
- [ ] Assessment dimensions are mapped to specific interview stages
- [ ] Interview pipeline is designed with clear goals for each stage
- [ ] Take-home assignments are scoped to 2-4 hours with clear evaluation criteria
- [ ] System design interviews focus on tradeoff analysis, not memorized solutions
- [ ] Scorecards use a consistent rubric with evidence, not just scores
- [ ] Hiring committee reviews scorecards independently before group discussion
- [ ] Red flags (can't explain own code, blames teammates) are documented and weighted appropriately
