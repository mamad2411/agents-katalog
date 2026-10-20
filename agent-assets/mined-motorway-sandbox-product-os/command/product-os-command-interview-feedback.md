<!-- owner: shared | audience: all-pms | last-updated: 2026-02 -->
<!-- purpose: Generate PM interview scorecard from Granola transcript against hiring competencies -->

# Interview Feedback Scorecard

Generate a rigorous, objective interview feedback scorecard for a PM candidate based on the Granola meeting transcript, assessed against our PM hiring competencies and the role's job description.

## Instructions

### Phase 1: Gather Context

1. **Parse the arguments**
   - The user provides arguments in the format: `$ARGUMENTS`
   - Expected format: `[Candidate Name], [Target Level], [Interview Type]`
   - Example: `Jane Smith, Senior PM, product case study`
   - If any of the three required fields are missing or unclear, ask ONLY for the missing information. Do not re-ask for fields already provided.
   - Check the auto-memory (MEMORY.md) for the interviewer's name — use this in the scorecard header

2. **Find the interview in Granola**
   - Use `mcp__claude_ai_Granola__list_meetings` (with a custom date range if the interview date is known, or `last_30_days`) to find candidate meetings, then filter by the candidate's name in the title or participants
   - If multiple meetings are found, ask the user to confirm which one
   - Use `mcp__claude_ai_Granola__get_meeting_transcript` to retrieve the full transcript

3. **Fetch the job description from Notion**
   - The job library is at: {your-notion-scorecard-url}
   - Use `mcp__claude_ai_Notion__notion-fetch` to retrieve the job library page
   - Find the job description matching the target role and level, then fetch that specific JD page
   - If the JD is not found in the library, ask the user to provide a Notion link or paste it in. Note this limitation in the output.

4. **Read the PM hiring competencies**
   - Read the file at `team/hiring/best-practice-pm-hiring.md`
   - This contains the full competency framework with excellent/poor indicators for all skills and attitudes

### Phase 2: Analyse the Transcript

5. **Map competencies to interview type**
   - Not all competencies are equally assessable in every interview type. Based on the interview type, identify which competencies are:
     - **Primary** (should be thoroughly assessed in this interview type)
     - **Secondary** (some signal may be present)
     - **Not assessable** (no meaningful signal expected)
   - Use this mapping as a guide:
     - **Screening call**: Communication (primary), Delivering Impact (primary), Curiosity (primary), Growth Mindset (secondary), Hunger for Impact (secondary), Product Process (secondary)
     - **Product case study**: Product Process - all sub-competencies (primary), Delivering Impact (primary), Communication (primary), Experiment Design (primary), Measurement (primary)
     - **Stakeholder interview**: Collaboration (primary), Communication (primary), Project Management (primary), Ownership (primary), Growth Mindset (secondary)
     - **Technical deep-dive**: Product Process - Build (primary), Experiment Design (primary), Measurement (primary), Project Management (primary), Solutionisation (primary)
     - **Culture/values interview**: All Attitude competencies (primary), Communication (secondary), Collaboration (secondary)
   - If the interview type does not match the above, use judgement to assign primary/secondary/not assessable

6. **Assess each primary and secondary competency**
   - For EACH competency that is primary or secondary, evaluate the candidate against the excellent/poor indicators from the hiring criteria file
   - Extract **direct quotes from the transcript** as evidence for each rating
   - Assign a rating:
     - **Strong**: Clear evidence of excellent-level responses. Multiple strong indicators present.
     - **Adequate**: Some positive signals but not consistently strong. May have gaps.
     - **Weak**: Evidence aligns more with poor indicators. Significant gaps or concerns.
     - **Insufficient signal**: Not enough data from this interview to assess fairly.
   - IMPORTANT: Be specific. Do not give a rating without a supporting quote or concrete observation.

7. **Calibrate for level**
   - Adjust expectations based on the target level:
     - **PM**: Solid fundamentals. Can describe good process with guidance. Has delivered measurable impact in a defined scope. May need coaching on ambiguity.
     - **Senior PM**: Independently breaks down ambiguous problems. Drives cross-functional alignment. Strong experimentation and measurement rigour. Evidence of coaching others.
     - **Lead PM**: Sets direction for multiple teams or a domain. Influences company strategy. Demonstrates thought leadership. Mentors other PMs. Navigates complex organisational dynamics.
   - Flag where a candidate may be performing at a different level than the target.

8. **Apply the assessment philosophy**
   - Hold a VERY HIGH BAR. Progressing weak candidates is expensive for the team and the candidate.
   - Be OBJECTIVE. Assess only what is evidenced in the transcript and any context the user provided. Do not infer or assume.
   - Be FAIR. Apply criteria consistently. Do not let one strong answer mask weaknesses elsewhere.
   - Default to caution. It is better to flag a concern and explore it further than to overlook it. Hiring the wrong person is far more costly than an extra interview round.
   - Actively look for both strengths AND red flags. Do not anchor on first impressions.
   - Assess what was SAID, not how it was said (unless Communication is the competency being assessed). Do not factor in confidence, charisma, or likability unless directly relevant to a competency.

### Phase 3: Generate the Scorecard

9. **Produce the structured scorecard** using this format:

```
# Interview Feedback: [Candidate Name]

**Date:** [Interview date]
**Interviewer:** [Interviewer name from MEMORY.md]
**Interview type:** [Type]
**Role:** [Role title]
**Target level:** [PM / Senior PM / Lead PM]
**Job description:** [Link to Notion JD, or "Not available"]

---

## Competency Scorecard

### Skills

| Competency | Rating | Signal | Key evidence |
|:-----------|:------:|:------:|:-------------|
| Delivering Impact | [Strong/Adequate/Weak/Insufficient] | [Primary/Secondary] | [1-2 sentence summary with quote] |
| Discovery | [Rating] | [Signal] | [Evidence] |
| Solutionisation | [Rating] | [Signal] | [Evidence] |
| Design/Prototyping/Validation | [Rating] | [Signal] | [Evidence] |
| Experiment Design | [Rating] | [Signal] | [Evidence] |
| Build | [Rating] | [Signal] | [Evidence] |
| Measurement & Analysis | [Rating] | [Signal] | [Evidence] |
| Communication | [Rating] | [Signal] | [Evidence] |
| Collaboration & Stakeholders | [Rating] | [Signal] | [Evidence] |
| Project Management | [Rating] | [Signal] | [Evidence] |

### Attitude

| Competency | Rating | Signal | Key evidence |
|:-----------|:------:|:------:|:-------------|
| Curiosity & Continuous Learning | [Rating] | [Signal] | [Evidence] |
| Growth Mindset & Resilience | [Rating] | [Signal] | [Evidence] |
| Hunger for Impact & Proactivity | [Rating] | [Signal] | [Evidence] |
| Ownership & Accountability | [Rating] | [Signal] | [Evidence] |
| Values Alignment | [Rating] | [Signal] | [Evidence] |

---

## Detailed Evidence

For each competency rated as Primary signal, provide:
- What the candidate said (with direct quotes)
- How this maps to the excellent/poor indicators
- What this tells us about their capability at the target level

### [Competency Name]
[Detailed evidence paragraph]

---

## Summary

### Strengths
- [What the candidate did well, with evidence references]

### Concerns
- [Areas of weakness or red flags, with evidence references]

### Level Calibration
[Whether the candidate appears to be at/above/below the target level, and why]

---

## Areas to Explore in Future Rounds

- [Specific competency or question area that needs deeper probing, with suggested question angles]

---

## Recommendation

**Decision: [PROGRESS / DO NOT PROGRESS / NEED MORE INFORMATION]**

[2-3 sentence justification tied to evidence and the assessment bar.]

[If PROGRESS: what should the next interview focus on?]
[If DO NOT PROGRESS: primary reasons, stated clearly and respectfully]
[If NEED MORE INFORMATION: exactly what is needed and how to get it]
```

### Phase 4: Save and Offer Adjustments

10. **Save the scorecard**
    - Save to `team/hiring/feedback/[candidate-name-slugified]-[YYYY-MM-DD].md`
    - Create the `team/hiring/feedback/` directory if it does not exist
    - Use lowercase with hyphens for the candidate name (e.g. `jane-smith-2026-02-13.md`)

11. **Confirm and offer adjustments**
    - Display the saved file path
    - Ask: "Want to adjust anything, add off-transcript context, share via Slack, or draft follow-up questions for flagged areas?"

## Output

1. Structured scorecard saved to `team/hiring/feedback/[candidate-name]-[date].md`
2. Full scorecard displayed in the terminal
3. Clear recommendation with justification

## Assessment Principles

These principles MUST guide every assessment:

- **Evidence over impression**: Every rating must be supported by transcript evidence. "Seemed strong" is not sufficient.
- **High bar**: The cost of a bad hire far exceeds the cost of an extra interview round. When evidence is ambiguous, rate conservatively.
- **Level-appropriate**: A strong answer from a PM candidate may be a weak answer from a Lead PM candidate. Always calibrate.
- **Bias awareness**: Assess what was SAID, not how it was said (unless Communication is the competency). Do not factor in confidence, charisma, or likability.
- **Completeness over speed**: It is better to flag "insufficient signal" than to guess. Gaps inform what future rounds should probe.
- **Fairness with rigour**: Apply the same criteria to every candidate. Be thorough, be fair, but do not lower the bar.
