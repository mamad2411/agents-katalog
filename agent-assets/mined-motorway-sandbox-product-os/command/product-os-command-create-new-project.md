<!-- owner: shared | audience: all-pms | last-updated: 2026-01 -->
<!-- purpose: Guided project/experiment doc creation with Socratic questioning -->

# Create New Project

Create a new experiment/project document using the standard template, complete it through guided conversation, and ensure quality through review criteria and Socratic questioning.

## Instructions

### Phase 1: Gather Project Information

1. **Start the conversation** by asking the user for the project/experiment name and a brief description of what they want to achieve.

2. **Use Socratic questioning** to help the user think through the project. Ask 3-5 questions from the categories below (pick the most relevant):

   **Problem Clarity:**
   - "What specific user pain point does this solve?"
   - "How do we know this is a real problem? What evidence do we have?"
   - "Who experiences this problem most acutely?"
   - "What's the cost of NOT solving this?"

   **Solution Validation:**
   - "Why is this the right solution for that problem?"
   - "What alternatives did you consider? Why did you reject them?"
   - "What's the simplest version that solves the core problem?"
   - "How will users discover this feature?"

   **Success Criteria:**
   - "How will we know if this feature is successful?"
   - "What would make you consider this a failure?"
   - "What metric are we trying to move? By how much?"
   - "What's the adoption target?"

   **Constraints & Trade-offs:**
   - "What are the technical constraints or risks?"
   - "What are we NOT going to do as part of this?"
   - "What existing features or workflows does this affect?"
   - "If we had half the time/resources, what would we cut?"

   **Strategic Fit:**
   - "Why is this the right feature to build RIGHT NOW?"
   - "How does this fit into our broader product strategy?"
   - "What happens if we wait 6 months to build this?"
   - "How does this affect our competitive position?"

3. **Gather specific template fields** through conversation:
   - Objective (clear, measurable goal)
   - Hypothesis (if we do X, then Y will happen because Z)
   - Evidence (user research, data, competitive analysis)
   - Success metric (primary KPI)
   - Secondary metrics
   - Guardrail metrics (what we don't want to negatively impact)
   - ROTI score estimate (Expected impact / dev days)
   - Evaluation plan: what to evaluate, criteria, method (Logfire/manual/hybrid), baseline, frequency, owner
   - Experiment details (if applicable): test type, audience, run time, MDE/ROPE
   - Launch and end dates
   - Solution details: link, scope, build time, out of scope, key assumptions
   - Risks and mitigations: impact, technical, internal, monitoring plans
   - Cross-functional stakeholders
   - Next steps

4. **If the project is an experiment**, run `/experiment-setup` with the hypothesis and intervention details gathered above. This will generate:
   - Past experiment lookup with calibration notes
   - Recommended success metric (primary, secondary, guardrails with baselines)
   - Revenue potential estimation with 40% haircut and sensitivity table
   - ROTI score
   - Experiment parameters: sample size, run time (including metric maturity wait), confidence level, decision rules

   Populate the ROTI score, experiment details, run time, and decision rules in the document with the `/experiment-setup` output rather than leaving them as placeholders. Flag any assumptions and note if engineering days estimate is needed from the EM to finalise the ROTI.

### Phase 2: Create the Document

5. **Generate the project document** using this template format:

```markdown
# [Project Name]

**Objective:**
[Clear, measurable objective statement]

**Hypothesis:**
[If we do X, then Y will happen because Z]

**Evidence:**
[Summary of evidence supporting this project]

**Success measures**

- Success metric: [Primary KPI with target]
- Secondary metrics: [List of secondary metrics]
- Guardrail metrics: [Metrics we don't want to negatively impact]
- ROTI score: [Expected impact / dev days]

**Evaluation plan**

- What are we evaluating? [e.g. output quality, user comprehension, model accuracy]
- Eval criteria: [specific pass/fail or scoring criteria]
- Eval method: [automated via Logfire / manual review / hybrid]
- Baseline: [current performance or benchmark to compare against]
- Sample size / frequency: [how often evals run, on what volume]
- Who reviews eval results? [Owner]

**Experiment details** (if experiment)

- Type of test: [A/B, multivariate, etc.]
- Audience: [Who is included/excluded]
- Run time: [Expected duration]
- MDE/ROPE: [Minimum detectable effect / Region of practical equivalence]
- What will we do if successful or not? [Decision criteria]

**Timings**

- Launch date: [Date]
- End date: [Date]

**Solution:**

- Link: [Design/spec link]
- In scope / key features:
  - [Feature 1]
  - [Feature 2]
- Build time: [Estimate]
- Out of scope:
  - [Item 1]
  - [Item 2]
- Key assumptions:
  - [Assumption 1]
  - [Assumption 2]

**Risks and mitigations:**

- Impact related:
  - [Risk]: [Mitigation]
- Technical:
  - [Risk]: [Mitigation]
- Internal risks:
  - [Risk]: [Mitigation]
- Monitoring plans:
  - [Plan]

**Cross-functional alignment**

- [Stakeholder 1]: [Role/input needed]
- [Stakeholder 2]: [Role/input needed]

**Timelines and milestones**

| Activity | Start date | End date | Owner | Status |
|----------|------------|----------|-------|--------|
| [Activity 1] | [Date] | [Date] | [Owner] | [Status] |
| [Activity 2] | [Date] | [Date] | [Owner] | [Status] |

Jira link: [Link]

**Next steps:**
- [Next step 1]
- [Next step 2]
```

6. **Save the document** to `projects/[project-name-slugified]/experiment.md`
   - Create the `projects/[project-name-slugified]/` directory if it doesn't exist
   - Use lowercase with hyphens for the folder name (e.g., `projects/new-checkout-flow/experiment.md`)
   - If prior stage artifacts exist in the folder (e.g. `discovery.md`, `prototypes.md`), use the same folder
   - **Copy the launch checklist** from `pm-playbook/templates/launch-checklist.md` into `projects/[project-name-slugified]/launch-checklist.md`. This ensures every project has a release checklist ready to complete before go-live
   - **Update the canonical doc** (`projects/[project-name-slugified]/canonical.md`) per the convention in `pm-playbook/conventions/canonical-documents.md`:
     - Set current stage to "Experiment Design", update stage artifacts table (including the launch checklist link), update Key metrics and Key decisions
     - If no canonical doc exists, create one using the initiative canonical template from the convention doc

### Phase 3: Quality Review

7. **Review the completed document** against these criteria and provide feedback:

   **Completeness Check:**
   - [ ] Objective is specific, measurable, and outcome-focused (not output-focused)
   - [ ] Hypothesis follows "If X, then Y, because Z" format
   - [ ] Evidence is concrete (data, quotes, research) not assumptions
   - [ ] Success metric has a specific target number
   - [ ] ROTI score is calculated and reasonable
   - [ ] Risks have corresponding mitigations
   - [ ] Scope boundaries are clear (in scope AND out of scope defined)

   **Quality Check:**
   - [ ] Problem is clearly defined before solution
   - [ ] Solution logically addresses the stated problem
   - [ ] Success criteria are measurable and time-bound
   - [ ] Assumptions are explicitly stated
   - [ ] Cross-functional dependencies are identified
   - [ ] Next steps are actionable

   **Experiment Quality Check (if experiment):**
   - [ ] ROTI calculated with 40% haircut and sensitivity table included
   - [ ] Primary metric matches funnel position (your mid-funnel metric for upper funnel, your end-funnel metric for later stages)
   - [ ] Sample size calculated and run time estimated (including metric maturity wait)
   - [ ] Confidence level specified (80% low-risk / 90% high-risk) with justification
   - [ ] Decision rules defined for all outcomes (win, miss, mixed, ambiguous)
   - [ ] Guardrails identified with current baseline values
   - [ ] Pricing baseline distortion acknowledged if experiment targets conversion metrics

   **Strategic Alignment:**
   - [ ] Project ties to current company/team OKRs
   - [ ] Timing justification is clear (why now?)
   - [ ] Trade-offs are acknowledged

8. **Provide feedback** in this format:
   - Strengths (what's well-defined)
   - Areas for improvement (specific suggestions)
   - Questions to consider (any gaps in thinking)
   - Overall readiness score: Ready / Needs Work / Not Ready

9. **Ask the user** if they want to iterate on any sections based on the feedback.

## Output

After completion, display:
1. Confirmation of saved file location
2. Reminder that the [Release & Launch Checklist](../../pm-playbook/templates/launch-checklist.md) has been copied to the project folder — complete it before go-live
3. Quality review summary
4. Offer to make any refinements

## Tips for Good Questions

**Listen for red flags:**
- Vague language: "Users want better..." - What specifically?
- Solution-first thinking: Can describe feature but struggles to describe problem
- Lack of evidence: "I think users would like..." - How do we know?
- Unclear success: Can't articulate what success looks like

**If the user struggles:**
- Offer multiple-choice options
- Share examples from similar contexts
- This is a collaborative tool, not a test
