---
name: mentoring-patterns
version: 1.0.0
min_mindforge_version: 10.3.0
status: stable
triggers: mentoring developer, pair programming pedagogy, code review teaching, career ladder design, junior developer growth, technical mentorship, developer onboarding mentoring, skill gap assessment, growth plan engineering, coaching engineers, feedback delivery, mentee progress tracking
---

# Mentoring Patterns

## When this skill activates

This skill activates when mentoring junior or mid-level developers, conducting pair programming sessions, giving pedagogical code reviews, designing career growth plans, assessing skill gaps, or coaching engineers through challenging technical problems. It applies to senior engineers, tech leads, and engineering managers responsible for developing others.

## Mandatory actions when this skill is active

### Before starting mentorship

1. **Assess current skill level** — Don't assume. Ask mentee to walk through a recent PR or design doc. Identify gaps in fundamentals (data structures, testing, debugging) vs advanced topics (distributed systems, performance optimization).
2. **Understand mentee's goals** — Are they aiming for senior engineer? Staff? Management? Different trajectories require different skill development. Don't project your own career path onto them.
3. **Establish mentorship contract** — Frequency (weekly 1:1s? ad-hoc?), topics (code review? architecture? career?), communication channels, and how to ask for help. Implicit expectations cause friction.
4. **Identify mentee's learning style** — Do they learn by reading (send docs), watching (pair program), or doing (give them a project)? Mismatch between teaching style and learning style wastes time.

### During mentorship activities

#### Pair Programming Pedagogy

- **Use driver-navigator pattern** — Junior is driver (typing), senior is navigator (guiding). Keeps mentee engaged and forces them to articulate their reasoning. Don't grab the keyboard.
- **Ask guiding questions, don't give answers** — Instead of "Use a hash map here," ask "How would you optimize this lookup?" Let them arrive at the solution. Spoon-feeding creates dependency.
- **Narrate your thought process** — When you're the driver, verbalize your reasoning: "I'm adding this null check because..." or "I'm writing the test first because...". Juniors can't see inside your head.
- **Timebox exploration** — Let mentee struggle for 10-15 minutes. If stuck, give a hint, not the solution. If still stuck after 30 minutes, show the approach and explain why.
- **Refactor together** — Take working but messy code and refactor it as a pair. Teaches that code quality is iterative, not achieved on the first pass.

#### Code Review Teaching

- **Classify feedback by severity** — Critical (security, correctness, data loss), Major (performance, maintainability, architectural misalignment), Minor (style, readability). Juniors often can't distinguish signal from noise.
- **Explain the "why," not just the "what"** — Don't say "Extract this into a function." Say "This block is duplicated in 3 places. Extracting it into a function ensures future bug fixes apply everywhere, not just one call site."
- **Use the "teach, don't tell" pattern** — First review: point out the issue and suggest a fix. Second occurrence: point out the issue, ask them to suggest a fix. Third occurrence: ask if they see the issue. Eventually they internalize the pattern.
- **Limit feedback to 3-5 key points per review** — Wall-of-text reviews overwhelm. Pick the most important lessons. Other issues can wait for the next PR.
- **Celebrate improvements** — When mentee applies feedback from a previous review, call it out: "Great null handling here, much cleaner than last time." Positive reinforcement accelerates learning.

#### Career Growth Plans

- **Use the skill matrix** — List skills required for the next level (e.g., to reach senior: owns 1-2 services end-to-end, writes design docs, mentors 1-2 juniors). Rate mentee as Beginner / Intermediate / Advanced / Expert on each skill.
- **Create 30-60-90 day goals** — 30 days: quick wins (improve test coverage on X service, ship Y feature). 60 days: medium scope (lead Z project, mentor junior on onboarding). 90 days: stretch goals (present at team meeting, write architecture proposal).
- **Identify growth projects** — Assign projects slightly above their current level. Too easy = no learning. Too hard = frustration and failure. The sweet spot is 20% beyond their comfort zone.
- **Track skill acquisition, not task completion** — The goal isn't "ship feature X." It's "learn how to design APIs" or "get comfortable with debugging production issues." Task completion is the vehicle, skill acquisition is the outcome.

#### Feedback Delivery

- **Use Situation-Behavior-Impact (SBI) framework** — "In yesterday's design review (situation), you interrupted Sarah twice (behavior), which made her hesitant to share more ideas (impact)." Specific, observable, non-judgmental.
- **Give feedback close to the event** — Real-time or within 24 hours. Waiting for quarterly reviews dilutes the learning and makes feedback feel like a performance audit, not coaching.
- **Balance positive and developmental feedback** — Ratio: 3-5 pieces of positive feedback for every 1 piece of developmental feedback. Overweighting critique creates defensiveness.
- **Focus on one behavior at a time** — Don't bundle 5 unrelated pieces of feedback. Pick the most impactful behavior to improve. Once they've made progress, address the next one.

#### Skill Gap Assessment

- **Distinguish between knowledge gaps and capability gaps** — Knowledge gaps (doesn't know how to use Redis) are fixed with learning. Capability gaps (struggles to break down ambiguous problems) require coaching and practice.
- **Use the Dreyfus model** — Novice (needs recipes), Advanced Beginner (starts recognizing patterns), Competent (can troubleshoot), Proficient (intuitive understanding), Expert (creates new patterns). Mentor at the appropriate level.
- **Create learning paths** — For knowledge gaps: reading list, courses, toy projects. For capability gaps: shadowing, pair programming, progressively harder assignments.

### After mentorship sessions

- **Document progress** — Keep notes on what you discussed, insights they shared, and commitments they made. Refer back in future sessions. Memory fades; notes compound.
- **Assign practice work** — After teaching a concept, give them a small task to apply it. "We talked about database indexing. Add indexes to the Users table and measure query performance before/after."
- **Check for understanding** — Ask mentee to summarize what they learned. If they can't explain it in their own words, they didn't internalize it.
- **Adjust mentorship approach based on feedback** — Periodically ask: "Is this mentorship helping? What should I do more/less of?" Course-correct before frustration builds.

## Self-check before task completion

- [ ] Mentee's current skill level and learning style are explicitly assessed
- [ ] Mentorship goals are aligned with mentee's career trajectory, not mentor's preferences
- [ ] Pair programming sessions use driver-navigator pattern with guiding questions, not answers
- [ ] Code review feedback is classified by severity and includes "why," not just "what"
- [ ] Career growth plan has 30-60-90 day goals tied to specific skill acquisition
- [ ] Feedback uses SBI framework, is delivered within 24 hours, and focuses on one behavior at a time
- [ ] Progress is documented and reviewed regularly to track skill development over time
