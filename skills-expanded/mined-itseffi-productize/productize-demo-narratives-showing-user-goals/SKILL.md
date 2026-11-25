---
name: productize-demo-narratives-showing-user-goals
description: >-
  Demo narratives showing user goals. Use when the user needs a product workflow for
  stakeholder management related to demo narratives showing user goals. Trigger terms:
  product-demo, storytelling, prototypes, user-goals, stakeholder-management.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Demo narratives showing user goals

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `demo-narratives-showing-user-goals`
- **Lifecycle**: Align
- **Category**: Marketing
- **Primary artifact**: Demo narratives showing user goals stakeholder narrative with audience, message, risks, asks, and follow-up owner

Use this skill to run the Productize prompt contract for **Demo narratives showing user goals**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{PROTOTYPE}}
- {{USER_GOALS}}
- {{AUDIENCE}}
- {{CONSTRAINTS}}
- {{RESEARCH_INSIGHTS}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Demo narratives showing user goals.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Follow these task requirements:
<task_requirements>
You are a prototype storytelling specialist skilled at crafting compelling demo narratives that showcase how products solve real user problems. Your task is to create story-driven prototype demonstrations that illustrate user jobs-to-be-done, making design decisions tangible and memorable for stakeholders.

You will be provided with:

<prototype>
{{PROTOTYPE}}
</prototype>

<user_goals>
{{USER_GOALS}}
</user_goals>

<audience>
{{AUDIENCE}}
</audience>

<constraints>
{{CONSTRAINTS}}
</constraints>

<research_insights>
{{RESEARCH_INSIGHTS}}
</research_insights>

Follow these steps to create a compelling demo narrative:

1. Define the protagonist and their context:
   - Create a specific, believable user persona (not generic "Sarah the marketer")
   - Establish their role, responsibilities, and daily workflow
   - Identify their current pain points and frustrations
   - Clarify what success looks like in their world
   - Define their technical proficiency and tool familiarity
   - Establish environmental context (where, when, with whom they work)
   - Root persona in real research data, not assumptions
   - Include relevant psychological motivators (what drives their decisions)
   - Specify constraints they operate under (time, budget, authority)
   - Identify who else is involved in their workflow (collaborators, approvers)

2. Construct the narrative scenario:
   - **Inciting incident**: What triggers the need to use your product?
   - **Stakes**: Why does this matter? What happens if they fail?
   - **Timeline**: How urgent is the need? What's the deadline?
   - **Environmental factors**: What else is happening around them?
   - **Emotional state**: How are they feeling at the start?
   - **Prior attempts**: What have they already tried?
   - **Success criteria**: What specific outcome would resolve their problem?
   - **Realistic scope**: Keep scenario bounded and believable (not "redesign entire company")
   - **Concrete details**: Specific numbers, names, dates that make it real
   - **Relatable situation**: Audience should recognize this scenario

3. Map the user journey through your prototype:
   - **Entry point**: How do they arrive at your product? (link, search, bookmark, notification)
   - **First impression**: What do they see/think in first 3 seconds?
   - **Orientation**: How do they figure out what to do next?
   - **Progressive disclosure**: What information appears when they need it?
   - **Key decision points**: Where do they make choices?
   - **Error/uncertainty moments**: Where might they hesitate or make mistakes?
   - **Confirmation moments**: How does the system validate they're on track?
   - **Aha moments**: When does value become clear?
   - **Completion**: What signals they've achieved their goal?
   - **Next steps**: What happens after this task?
   - **Realistic pacing**: Allow time for reading, thinking, not just clicking
   - **Natural interruptions**: Phone call, question from colleague (shows resilience)
   - **Context switching**: They leave and come back (tests findability)

4. Script the demo walkthrough with dialogue:
   - **Scene setting**: "It's Tuesday afternoon, Alex has 30 minutes before a client meeting..."
   - **Internal monologue**: Share user's thoughts at key moments
   - **Narration style**: First-person ("I need to...") or third-person ("Alex notices...")
   - **Action descriptions**: Specific interactions (click, scroll, type exact text)
   - **System responses**: What happens after each action
   - **Decision rationale**: Why user chooses option A over B
   - **Emotional beats**: Frustration → confusion → clarity → confidence
   - **Realistic hesitations**: "Hmm, where would that be... probably in settings"
   - **Course corrections**: Show user recovering from wrong path
   - **Time markers**: "2 minutes later..." to show efficiency
   - **Verbatim UI text**: Quote exact button labels, headings, messages
   - **Highlighting patterns**: "The bold CTA immediately draws attention to..."

5. Add contextual annotations explaining design decisions:
   - **Why this flow**: Design rationale for the path shown
   - **Alternatives considered**: What other approaches were explored
   - **Research backing**: User data supporting this design choice
   - **Progressive disclosure**: Why certain info appears when it does
   - **Accessibility considerations**: How inclusive design shows up
   - **Error prevention**: How design prevents common mistakes
   - **Cognitive load management**: How complexity is managed
   - **Pattern consistency**: How this follows established conventions
   - **Performance implications**: Loading states, perceived speed
   - **Edge case handling**: What happens in unusual situations
   - **Technical constraints**: Limitations that shaped decisions
   - **Future enhancements**: What's intentionally deferred to V2

6. Prepare for live demonstration delivery:
   - **Pre-demo setup**: What needs to be configured in advance
   - **Data staging**: Realistic content loaded into prototype
   - **Fallback plans**: What if tech fails mid-demo
   - **Interaction notes**: Exactly which hotspots to click, what to type
   - **Pacing guidelines**: How fast to move through each section
   - **Pause points**: Where to stop for questions or emphasis
   - **Audience engagement**: Where to ask "Have you experienced this?"
   - **Comparison moments**: "Unlike current process where you'd..."
   - **Zoom-in callouts**: Specific UI details to highlight
   - **Branching paths**: Alternative routes if audience asks "what if..."

7. Document variations for different audiences:
   - **Executive version**: Business outcomes, ROI, strategic alignment (5 min)
   - **End user version**: Detailed workflow, all features, realistic use (15 min)
   - **Technical version**: Integration points, data flow, architecture (10 min)
   - **Sales version**: Competitive advantages, objection handling (8 min)
   - **Stakeholder review**: Design rationale, research validation (20 min)
   - **Usability test**: Minimal guidance, observe natural exploration (no script)

Present your demo narrative in this format:

<demo_narrative>
<persona_profile>
**Name:** [Specific name with relevant context - e.g., "Jordan Chen, Operations Manager at 200-person logistics company"]

**Role and Responsibilities:**
[Detailed description of their job, what they're accountable for, who they report to]

**Daily Workflow:**
[Typical day-in-the-life - what tools they use, what meetings they attend, what reports they create]

**Current Pain Points:**
- [Pain 1]: [Specific frustration with concrete example]
- [Pain 2]: [Specific frustration with concrete example]
- [Pain 3]: [Specific frustration with concrete example]

**Technical Proficiency:**
[Their comfort level with technology, what tools they already use successfully]

**Success Metrics:**
[How their performance is measured - what they're trying to optimize]

**Constraints:**
- Time: [Specific time pressures they face]
- Budget: [Financial limitations or approval processes]
- Authority: [What they can decide vs. need approval for]

**Motivations:**
[What drives their behavior - career goals, team dynamics, personal values]

**Research Foundation:**
[Which user interviews/studies informed this persona - quote specific findings]
</persona_profile>

<scenario_setup>
**Scene:**
[Vivid description of when/where this is happening - day, time, location, environmental context]

**Inciting Incident:**
[What just happened that creates the need to use your product?]

**Stakes:**
[Why this matters - what happens if they succeed vs. fail]

**Timeline:**
[How urgent is this? When's the deadline?]

**Emotional State:**
[How they're feeling - stressed, curious, overwhelmed, hopeful]

**Prior Context:**
[What have they already tried? Why didn't it work?]

**Success Outcome:**
[Concrete description of what resolution looks like]

**Realistic Scope:**
[Boundaries of this scenario - what's in/out of scope]

Example:
"It's Thursday at 3pm. Jordan just got out of a difficult client meeting where they promised updated logistics forecasts by tomorrow morning. The current spreadsheet process takes 4-5 hours of manual data wrangling, and Jordan has a team dinner at 6pm they can't miss. Their manager is copied on the client email, so there's visibility on this commitment. Jordan has tried automating parts of this before using Excel macros, but they break whenever column names change."
</scenario_setup>

<demo_script>
<act_1_arrival>
**Narration:**
[Scene-setting description in present tense]

**Jordan's Thought:**
"[Internal monologue showing their mental state]"

**Action:**
[Exactly what they do - specific clicks, URLs, navigation]

**System Response:**
[What appears on screen - describe layout, key elements visible]

**Jordan's Reaction:**
"[Thought about what they see]"

**Design Note:**
[Annotation explaining why interface works this way - research backing, design principle, accessibility consideration]

Example:
**Narration:** Jordan opens their laptop and clicks the bookmark for ForecastPro, which their team started piloting last week.

**Jordan's Thought:** "Okay, I need to pull Q4 logistics data and create those regional forecasts they asked for. Let me see if this new tool can actually help."

**Action:** Jordan lands on the dashboard homepage.

**System Response:** The screen shows a clean interface with three prominent options: "Create New Forecast," "View Recent Reports," and "Import Data." A subtle notification badge shows "2" on Recent Reports.

**Jordan's Reaction:** "Good, I can see my starting points clearly. That notification probably means the datasets I imported yesterday are ready."

**Design Note:** We use a minimal three-option entry to prevent choice paralysis. Research showed users arriving with clear intent (create/view/import) - the IA reflects their mental model. The notification badge provides continuity for returning users without demanding attention.
</act_1_arrival>

<act_2_core_task>
[Continue narrative through the main workflow - include 5-8 key moments:]
- Initial orientation and confidence building
- First meaningful action with immediate feedback
- Decision point with clear affordances
- Potential confusion or error → system guidance
- Progress indicator showing advancement
- Confirmation of successful completion
- Next action suggested

[For each moment, include: Narration, Jordan's Thought, Action, System Response, Jordan's Reaction, Design Note]
</act_2_core_task>

<act_3_completion>
**Narration:**
[Description of reaching the goal]

**Jordan's Thought:**
"[Realization of success and what it means]"

**Action:**
[Final action - export, share, save, etc.]

**System Response:**
[Confirmation message, next steps offered]

**Jordan's Reaction:**
"[Emotional beat - relief, satisfaction, confidence]"

**Time Check:**
[How long this took vs. old method]

**Outcome:**
[What Jordan achieved and why it matters]

Example:
**Narration:** The final forecast report generates in seconds, formatted exactly how the client expects it.

**Jordan's Thought:** "Wait, that's it? That would've taken me until 7pm with the old process. And it's already in the right format."

**Action:** Jordan clicks "Export to Email" and adds the client's address, with their manager CC'd.

**System Response:** "Report sent successfully. Forecast will auto-update weekly and notify stakeholders." A subtle animation shows the email icon confirming delivery.

**Jordan's Reaction:** "Okay, this actually worked. And now it'll update automatically? That's huge."

**Time Check:** Task completed in 8 minutes vs. the usual 4-5 hours.

**Outcome:** Jordan has the rest of the afternoon free, makes it to team dinner on time, and gained credibility with the client by delivering early. More importantly, this forecast will now maintain itself weekly.
</act_3_completion>
</demo_script>

<key_moments_summary>
**1. First Impression (0:30):**
[What makes user confident they're in right place]

**2. Aha Moment (2:15):**
[When value becomes clear - what triggered the realization]

**3. Trust Moment (4:30):**
[When user believes system is reliable - what convinced them]

**4. Completion Moment (7:45):**
[When goal achieved - what confirmed success]

**5. Delight Moment (8:00):**
[Unexpected positive - what exceeded expectations]

[For each: timestamp, description, why it matters, supporting design element]
</key_moments_summary>

<contextual_annotations>
**Design Decisions Showcased:**
1. [Decision]: [Rationale + Research backing]
2. [Decision]: [Rationale + Research backing]
3. [Decision]: [Rationale + Research backing]

**Pattern Library Elements:**
- [Pattern used]: [Why appropriate for this context]
- [Pattern used]: [Why appropriate for this context]

**Accessibility Features Highlighted:**
- [Feature]: [How it helps specific users]
- [Feature]: [How it helps specific users]

**Progressive Disclosure Examples:**
- [Information]: [Why hidden until needed]
- [Information]: [Why hidden until needed]

**Error Prevention:**
- [Mechanism]: [What mistake it prevents]
- [Mechanism]: [What mistake it prevents]

**Performance Considerations:**
- [Optimization]: [Why it matters for this scenario]
- [Optimization]: [Why it matters for this scenario]
</contextual_annotations>

<demo_delivery_guide>
<pre_demo_setup>
**Prototype Configuration:**
- [Setting to configure]: [Specific value]
- [Data to load]: [Where to source realistic content]
- [Browser/device]: [Recommended setup]

**Rehearsal Checklist:**
- [ ] All hotspots clickable and lead to correct screens
- [ ] Realistic data loaded (names, numbers, dates)
- [ ] Timing rehearsed (should feel natural, not rushed)
- [ ] Annotations hidden unless presenter decides to show
- [ ] Fallback screenshots available if tech fails
</pre_demo_setup>

<live_demo_script>
**Opening (30 seconds):**
"Let me show you how [persona] uses this to solve [specific problem]. Watch for how the design handles [key challenge]."

**Scene Setting (15 seconds):**
"[Vivid description of scenario - day, time, what just happened]"

**Walkthrough (5-10 minutes):**
[Step by step with exact interactions:]
1. [Action to take] → [What to say while doing it] → [What to point out]
2. [Action] → [Narration] → [Callout]
3. [Continue for key flow]

**Pause Points:**
- After [moment]: "Notice how [design element] helps with [user need]"
- After [moment]: "Have you encountered this problem in your workflow?"
- After [moment]: "Unlike [current process], this approach [advantage]"

**Closing (30 seconds):**
"In under [time], Jordan accomplished [outcome] - compared to [old way]. Key differentiators: [list 2-3 specific advantages shown]."

**Q&A Preparation:**
- If asked about [edge case]: [Navigate to X screen and show Y]
- If asked about [integration]: [Show Z and explain technical approach]
- If asked about [alternative path]: [Click A instead of B to demonstrate]
</live_demo_script>

<pacing_notes>
**Total Time:** [Recommended duration for full narrative]

**Section Breakdown:**
- Setup and context: [X minutes]
- Core task demonstration: [Y minutes]
- Completion and outcome: [Z minutes]
- Q&A buffer: [W minutes]

**Speed Guidelines:**
- Speak at conversational pace (not presentation pace)
- Allow 3-5 seconds after each screen transition for audience to orient
- Pause after key moments to let impact land
- Don't rush through error recovery - that's valuable to show

**Energy Modulation:**
- Build excitement as user progresses toward goal
- Allow authentic hesitation moments (makes it believable)
- Emphasize relief/satisfaction at completion
</pacing_notes>

<fallback_plans>
**If Technology Fails:**
- Option 1: [Screenshot walkthrough prepared]
- Option 2: [Video recording as backup]
- Option 3: [Whiteboard sketch of key screens]

**If Audience Derails:**
- [Polite redirect]: "Great question - let me finish showing [X], then circle back to that"
- [Mark for later]: Add to parking lot list visible on screen

**If Demo Breaks Mid-Flow:**
- [Recovery line]: "Let me skip ahead to the outcome..." [show completion state]
- [Acknowledge]: "That's actually helpful - shows why we need robust error handling"
</fallback_plans>
</demo_delivery_guide>

<audience_variations>
<executive_version>
**Duration:** 5 minutes
**Focus:** Business outcomes, ROI, strategic fit
**Script Adjustments:**
- Start with the time/cost savings number
- Skip interaction details, show before/after states
- Emphasize competitive advantage and market differentiation
- End with adoption plan and success metrics

**Key Moments to Show:**
1. Problem statement with financial impact
2. Solution in action (fast-forward through steps)
3. Outcome with measurable results
</executive_version>

<end_user_version>
**Duration:** 15 minutes
**Focus:** Complete workflow, all features, realistic use
**Script Adjustments:**
- Show every step with natural pacing
- Include error recovery and edge cases
- Demonstrate all key features, not just happy path
- Allow time for questions throughout

**Key Moments to Show:**
[All moments from main script, plus:]
- Secondary features in context
- Settings and customization options
- Help resources and tooltips
</end_user_version>

<technical_version>
**Duration:** 10 minutes
**Focus:** Integration points, data architecture, technical capabilities
**Script Adjustments:**
- Open with architecture overview
- Show API endpoints or integration points during workflow
- Highlight data transformation and validation
- Demonstrate error handling and edge cases
- End with scalability and security considerations

**Key Moments to Show:**
1. Data input and validation
2. System processing (what happens under hood)
3. Integration with other systems
4. Performance under load
</technical_version>

<sales_version>
**Duration:** 8 minutes
**Focus:** Competitive advantages, objection handling, customer value
**Script Adjustments:**
- Start with customer's current pain
- Emphasize differentiation vs. alternatives
- Show ROI calculation in real-time
- Address common objections proactively
- End with implementation ease

**Objection Handling Built In:**
- "Unlike [competitor], we handle [X] by..."
- "Customers worried about [Y] appreciate how we..."
- "This approach means you avoid [common pitfall]"
</sales_version>

<stakeholder_review_version>
**Duration:** 20 minutes
**Focus:** Design rationale, research validation, decisions made
**Script Adjustments:**
- Include all contextual annotations visible
- Reference specific user research findings
- Show alternative approaches considered
- Highlight open questions and areas for feedback
- Discuss iteration plans

**Key Moments to Show:**
- Research insight → Design decision connection
- A/B test results informing choices
- Accessibility compliance
- Technical constraint handling
</stakeholder_review_version>
</audience_variations>

<branching_scenarios>
**If Audience Asks "What If User Wants to [Alternative Path]":**
[Describe the alternate route, which screens to show, how system adapts]

**If Asked About Error States:**
[Which error to demonstrate, what recovery looks like]

**If Asked About Mobile Experience:**
[How narrative changes on mobile device, what's different]

**If Asked About First-Time vs. Returning User:**
[How onboarding differs, what changes after initial use]
</branching_scenarios>
</demo_narrative>

Remember: The best demo narratives feel like watching a real person solve a real problem. Avoid the temptation to show every feature - instead, show one complete journey that makes the value undeniable. Your audience should leave saying "I can see myself using this" rather than "That looks interesting."
</task_requirements>

FORMAT
Return exactly this structure:

<demo_effectiveness_checklist>
Before finalizing your demo narrative, verify:
- [ ] Persona feels like a real person (not "User A" or generic archetype)
- [ ] Scenario is specific and believable (not abstract or overly broad)
- [ ] Stakes are clear (audience understands why this matters)
- [ ] Timeline creates appropriate urgency (not manufactured drama)
- [ ] Journey shows realistic pacing (allows time for thinking, not just clicking)
- [ ] Errors/uncertainty included (demonstrates resilience, not just happy path)
- [ ] Design decisions explained (audience learns the "why" behind the "what")
- [ ] Outcome is measurable (time saved, quality improved, frustration reduced)
- [ ] Emotional journey is authentic (frustration → clarity → confidence)
- [ ] Technical feasibility confirmed (everything shown actually works in prototype)
</demo_effectiveness_checklist>

FAILURE
- Output misses required sections, steps, or reasoning required by `<task_requirements>`.
- Required format/schema is missing, malformed, or incomplete.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
