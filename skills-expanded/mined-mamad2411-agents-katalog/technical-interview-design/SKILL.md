---
name: technical-interview-design
version: 1.0.0
min_mindforge_version: 10.1.0
status: stable
triggers: technical interview, coding challenge design, system design interview, evaluation rubric, interview signal, interview bias reduction, hiring assessment, take-home challenge, interview scorecard, coding round design, debrief calibration, interview fairness
---

# Technical Interview Design

## When this skill activates

This skill activates when designing, improving, or evaluating technical interview
processes. It covers coding challenges, system design rounds, evaluation rubrics,
bias reduction techniques, and debrief calibration to ensure interviews extract
meaningful signal while treating candidates fairly.

## Mandatory actions when this skill is active

### Before

1. **Define the role clearly** — What does this person actually do day-to-day? What
   skills are essential vs. nice-to-have? What level of seniority?
2. **Identify signals to extract** — Map each interview round to specific competencies
   being evaluated. No round should exist without a clear signal target.
3. **Audit for relevance** — Every question and challenge must relate to actual work
   the candidate would perform. No puzzle questions, no trivia, no gotchas.

### During

4. **Coding challenge design principles:**
   - Relevant to actual work the team does (not algorithmic puzzles unless role requires)
   - Time-boxed with clear expectations communicated upfront
   - Multiple valid solution paths (not one "correct" answer)
   - Clear evaluation criteria shared with interviewers before use
   - Scaffolding provided (no time wasted on boilerplate setup)
   - Accommodations available (extra time, alternative formats)

5. **Evaluation rubric (score each dimension 1-4):**
   - **Problem decomposition** — Breaks problem into manageable parts, identifies
     unknowns, asks clarifying questions before diving in.
   - **Communication** — Explains thinking clearly, responds to hints, collaborates
     with interviewer, articulates tradeoffs.
   - **Code quality** — Readable, well-structured, appropriate abstractions, handles
     edge cases, follows conventions.
   - **Testing mindset** — Considers test cases, validates assumptions, identifies
     failure modes, demonstrates correctness.
   - **Tradeoff awareness** — Articulates time/space tradeoffs, discusses scalability,
     acknowledges limitations of chosen approach.

6. **Bias reduction techniques:**
   - Score independently before debrief discussion (prevent anchoring)
   - Use structured scorecards with specific evidence required per score
   - Same questions for all candidates at same level (allow follow-ups to vary)
   - Diverse interview panels (varied backgrounds, roles, tenure)
   - Evaluate against rubric, not against other candidates or "culture fit"
   - Train interviewers on common biases (halo effect, similarity bias, confirmation)

7. **System design round structure:**
   - Phase 1: Scope and requirements (candidate drives, interviewer clarifies)
   - Phase 2: High-level design (components, data flow, API boundaries)
   - Phase 3: Deep dive (interviewer picks area to explore in depth)
   - Phase 4: Tradeoffs and evolution (scalability, failure modes, future changes)
   - Evaluate: scalability thinking, tradeoff articulation, communication clarity,
     ability to handle ambiguity, depth of technical knowledge.

8. **Take-home challenge guidelines:**
   - Maximum 3-4 hours of work (state this explicitly)
   - Provide clear submission criteria and evaluation rubric upfront
   - Allow technology choice where possible
   - Pay candidates for take-homes exceeding 2 hours
   - Review within 48 hours (respect candidate time)

9. **Debrief calibration:**
   - Each interviewer presents evidence and scores before group discussion
   - No "veto without evidence" — strong no requires specific rubric failures
   - Calibrate scores across interviewers quarterly using past candidates
   - Track hire-to-performance correlation to improve signal extraction

### After

10. **Provide candidate feedback** — Specific, actionable, kind. Even for rejections,
    share what went well and areas for growth.
11. **Iterate on the process** — Track interviewer consistency, candidate satisfaction
    scores, and time-to-decision. Improve quarterly.
12. **Document interview guides** — Maintain living documents with questions, rubrics,
    and calibration notes for each role type.

## Self-check before task completion

- [ ] Every round maps to specific, documented signals
- [ ] Challenges are relevant to actual work (no trivia or puzzles)
- [ ] Rubric uses 1-4 scale with clear behavioral anchors per level
- [ ] Bias reduction measures in place (structured scoring, diverse panels)
- [ ] Time expectations clearly communicated to candidates
- [ ] Debrief process requires evidence-backed scores before discussion
- [ ] Candidate feedback mechanism exists
- [ ] Process review cadence established (at least quarterly)
