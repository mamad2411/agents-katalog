---
name: interview-post-process
description: Post-process a Design & Architecture interview scorecard. On first use, copies a template scribble sheet to the user's GDrive. On subsequent uses, duplicates the template tab for a new candidate. Reads rough notes, cross-references the playbook and appropriate leveling cheat sheet (SA or DSA), and writes polished refined notes back into the doc. Use when the interviewer says "post-process interview", "refine interview notes", "help me with my scorecard", or "formulate my interview rating".
user-invocable: true
---

# Interview Post-Process Skill

Manages the full interview scorecard lifecycle: template setup, rough note capture, and polishing notes into leveling-aligned refined text for Greenhouse.

## Overview of the User Flow

1. **First time**: Copy the template doc to the user's GDrive. Tell them to fill in their rough notes and come back.
2. **Returning with an existing doc**: Either duplicate the template tab for a new candidate, or polish existing rough notes.
3. **Polishing**: Read rough notes, cross-reference playbook + leveling guide (SA or DSA), write refined notes, confirm ready for Greenhouse.

---

## Step 1: Determine State

Check what the user has provided:

- **No doc URL provided** → This is likely a first-time setup. Proceed to Step 2 (First-Time Setup).
- **Doc URL provided, no specific tab** → Ask if they want to add a new candidate tab or polish existing notes.
- **Doc URL provided with a specific tab** → Read the tab. If it has rough notes with ratings filled in, proceed to Step 4 (Polish). If it's mostly empty/template, tell them to fill in their notes first.

To check if the user already has a scorecard doc, look for a memory file in the user's project memory directory that stores their scorecard doc ID (the memory system will have the correct path available at runtime). If found, skip to Step 3.

## Step 2: First-Time Setup (Copy Template)

The template document is: `1msDakphsQsGFzuAL-DhLoXZlh2Vhq_mGJT5SDqQf_EE`

Copy it to the user's GDrive:

```bash
TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null)
curl -s -X POST "https://www.googleapis.com/drive/v3/files/1msDakphsQsGFzuAL-DhLoXZlh2Vhq_mGJT5SDqQf_EE/copy" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"name": "xSA Design & Architecture Interview Scorecards"}'
```

After copying:
1. Save the new document ID to memory so future invocations can find it automatically.
2. Tell the user:
   - "I've created your personal scorecard doc: [link]"
   - "Open the tab '[make copy] XX.XX.2026 [Name]' before your next interview"
   - "Fill in: SA or DSA, the candidate name in the tab title, your rough notes and ratings under each heading"
   - "When you're done, come back and I'll polish the notes for Greenhouse"

## Step 3: Add a New Candidate Tab (Duplicate Template Tab)

When the user already has a scorecard doc and wants to start a new interview, duplicate the template tab.

First, find the template tab -- it's the one whose title starts with "[make copy]":

```bash
TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null)
curl -s "https://docs.googleapis.com/v1/documents/${DOC_ID}?includeTabsContent=true" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Iterate through tabs to find the one with title starting with "[make copy]". Then use the Sheets-style tab duplication -- unfortunately the Docs API doesn't support tab duplication directly, so use this approach:

**Option A: Use the Google Docs API `duplicateTab` request** (preferred if available):
```bash
TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null)
curl -s -X POST "https://docs.googleapis.com/v1/documents/${DOC_ID}:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [{
      "duplicateTab": {
        "tabId": "<TEMPLATE_TAB_ID>",
        "insertionIndex": <INDEX_AFTER_LAST_TAB>
      }
    }]
  }'
```

The response will contain the new tab's ID. Then rename it using `updateTabProperties`:
```bash
curl -s -X POST "https://docs.googleapis.com/v1/documents/${DOC_ID}:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [{
      "updateTabProperties": {
        "tabId": "<NEW_TAB_ID>",
        "tabProperties": {
          "title": "<DATE> <CandidateName>"
        },
        "fields": "title"
      }
    }]
  }'
```

Ask the user for:
- **Candidate name** (for the tab title)
- **Date** (default to today's date)

Then tell them:
- "I've created a new tab: '<Date> <Name>'"
- "Fill in: SA or DSA, your rough notes and ratings"
- "Come back when you're ready and I'll polish them"

Provide the direct link to the new tab: `https://docs.google.com/document/d/${DOC_ID}/edit?tab=${NEW_TAB_ID}`

## Step 4: Read and Validate the Scorecard

Use the Google Docs skill pattern to read the scorecard:

```bash
TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null)
curl -s "https://docs.googleapis.com/v1/documents/${DOC_ID}?includeTabsContent=true" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Find the correct tab (user may specify via URL fragment `tab=t.xxxxx`, or it may be the most recently created non-template tab). Extract:

- **Candidate name** (from tab title)
- **Role type** (SA or DSA -- from the "Interviewing for SA / DSA" line in the rough notes)
- **Rough notes** for each section (Discovery, Core Architecture, Technical Spike, Key Take-Aways)
- **Ratings** (L4/L5/L6 or "no") indicated by the interviewer for each section

### Determine the Role Type (SA vs DSA)

Look for the line "Interviewing for SA / DSA" in the rough notes section. The user should have indicated which one. If not clear, ask the user.

- **SA role**: Use the SA Hiring Leveling Guide (Appendix A)
- **DSA role**: Use the DSA Hiring Leveling Guide (Appendix B)

### Validate Before Polishing

Before proceeding, check that:
- At least the Discovery and Core Architecture sections have rough notes (not just "Rating:")
- Ratings are filled in for at least Discovery and Core Architecture
- The role type (SA/DSA) is indicated

If any are missing, tell the user what's needed and ask them to complete the rough notes first.

## Step 5: Draft Refined Notes

For each section, produce refined notes that follow this structure:

### For Discovery & Framing, Core Architecture, and Technical Spike sections:

1. **State the rating** (e.g., "Rating: L5")
2. **Summarize what the candidate did well**, using specific behaviors from the rough notes and mapping them to the level descriptors from the **role-appropriate** cheat sheet. Quote or paraphrase the official descriptor language where applicable (e.g., "consistent with L5: 'proactively surfaces constraints like API rate limits and aligns design to specific BI/ML business outcomes'").
3. **Note areas where the candidate fell short of the next level**, referencing the L+1 descriptors to explain what would have been needed (e.g., "To reach L6, we would expect the candidate to 'shape the problem definition' and 'challenge the REST approach'").
4. **Call out any red flags** if applicable, using the playbook's red flag language.
5. **Include specific examples** from the rough notes as evidence (e.g., "He worked through the sizing math: 10M records per POS per hour, ~167MB per pull").

### For the Key Take-Aways section:

1. **State the overall recommendation** (e.g., "Recommendation: Hire at L5 SA" or "Recommendation: No Hire")
2. **List strengths** as bullet points, grounded in observed behaviors
3. **List areas for development** as bullet points, tied to level expectations
4. **Provide an overall assessment** paragraph that addresses the "Raise the Bar" questions:
   - Would we fight for this hire?
   - Are they above today's team average in 2+ dimensions?
   - Do they bring a distinctive strength we currently lack?

### Writing Style Guidelines:

- Use professional, objective language suitable for a hiring debrief
- Ground every claim in observed behavior from the rough notes -- do not invent or assume behaviors not mentioned
- Use the exact wording from the **role-appropriate** leveling guide when describing level expectations (put in quotes)
- Be specific: include numbers, scenarios, and concrete examples from the interview
- Keep each section to 2-4 paragraphs -- detailed enough to be useful in calibration, concise enough to read quickly
- Do NOT modify the interviewer's rough notes -- only write in the "Refined Notes" section

## Step 6: Write Refined Notes Back to the Document

Find the insertion points in the "Refined Notes" section of the document. Each sub-heading under "Refined Notes" corresponds to a section that needs to be filled in.

Use the Google Docs API batchUpdate to insert the refined text after each heading. Insert in **reverse order** (bottom-to-top) to avoid index drift.

```bash
TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null)
curl -s -X POST "https://docs.googleapis.com/v1/documents/${DOC_ID}:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"requests": [...]}'
```

IMPORTANT: Insert requests must be ordered from highest index to lowest index in the batch to prevent index shifts. Make sure to specify the correct `tabId` in each location.

## Step 7: Confirm Completion

After writing, tell the user:
- Which sections were filled in
- The role type used (SA or DSA) and which leveling guide was applied
- A brief summary of the ratings and recommendation
- "Review the refined notes in the doc, then copy them into Greenhouse when ready"
- Provide a direct link to the tab

## Important Notes

- **Never modify the rough notes section** -- those are the interviewer's original observations and must be preserved as-is
- **Always authenticate first** -- use the google-auth skill pattern to check/obtain a valid token
- **Handle multi-tab documents** -- the scorecard doc will have many tabs (one per candidate). Always work on the correct tab.
- **The rating comes from the interviewer** -- use their indicated rating (L4/L5/L6 or "no") as the basis. Do not override the interviewer's rating judgment, but do flag if the rough notes seem inconsistent with the chosen level
- **Template doc ID**: `1msDakphsQsGFzuAL-DhLoXZlh2Vhq_mGJT5SDqQf_EE` -- this is the source template, never modify it
- **Always use the correct leveling guide for the role** -- SA and DSA have different descriptors

---

## Appendix A: SA Hiring Leveling Guide (Embedded Reference)

Use this when the candidate is interviewing for an **SA (Solutions Architect)** role.

### Relevant Experience

| | L4 | L5 | L6 |
|---|---|---|---|
| Experience | Junior: 3+ Years | Professional: 5+ Years | Senior: 8+ years |
| Assumptions | Assume they know something | Assume they know most things | Assume they know all things |
| Impact | Will lead smaller geos or emerging accounts, or workstreams on larger accounts | Will lead technical strategy on Geo/Emerging; owns workstreams on Named/Strategic | Will lead technical strategy on Named/Strategic accounts |
| Complexity | Few concurrent, moderately complex engagements or projects | One or more moderately complex accounts or multiple workstreams or projects | High-complexity, multi-LOB / multi-account engagements |
| Influence | First-line managers internally; Frontline leaders & tech stakeholders | Tech leads/architects; Director/VP level externally | BU2-BU1 leaders internally; VP+ level externally |

### Capabilities / Spike Areas (must meet baseline for all, strong in 2 of 4)

**Technical Problem Solving** (First Principles Thinking, Tech Discovery, AI-Builder Mindset, Objection Handling):

- **L4**: "I could trust this person to own a scoped customer problem and build a working solution with light guidance." Described problems with multiple technical components or constraints. Used first principles to reason about the solution before choosing tools. Built, tested, or iterated on something tangible. Field objections or pushback along the way.
- **L5**: "I could put this person in front of a customer, without me in the room, and trust them to discover, build, and defend a credible solution." Worked on problems with unclear requirements, competing constraints, or evolving goals. Prototyped to explore trade-offs (data quality, model choice, scale, cost). Iterated based on feedback or failure, not just success. Turned objections into concrete design changes or experiments.
- **L6**: "I would put this person in front of a top-tier customer or executive sponsor and expect them to raise the bar for how we build and reason solutions." Addressed problems spanning multiple systems, teams, or stakeholders. Used prototyping to challenge assumptions early. Abstracted learnings from builds into reusable patterns or guidance. Anticipated objections and validated solutions before they surfaced.

**Tech Bar** (Design & Architecture, Data & AI Industry, Vibe/Coding Skills, Cloud & Platform, Data Engineering, Data Warehousing, GenAI):

- **L4**: Foundational -- Has basic knowledge of concepts, can describe areas and follow along in conversations, but lacks practical experience to go deep independently. Think: "They mostly get it, but might need support or to double-check documentation before answering."
- **L5**: Proficient -- Is able to apply knowledge practically, provide guidance on technical challenges, and is comfortable leading technical discussions and making recommendations. Think: "They could confidently carry most technical conversations on their own."
- **L6**: Expert -- Recognized as SME with deep and broad expertise. Capable of solving complex problems, understands best practices, and generally stays ahead of trends. Think: "They know this so well they could redesign it if needed."

**Execution & Collaboration** (Customer Advisor, Stakeholder Alignment, Communication, Drives Adoption):

- **L4**: "I would trust this person to clearly communicate status, execute on a defined scope, and confirm the solution met the intended outcome." Owns specific deliverables and follows through with clear updates and next steps. Collaborates effectively with peers and partners to unblock execution. Defines basic success criteria.
- **L5**: "I would trust this person to independently advise a customer, align stakeholders around clear decisions, and drive adoption of the solution." Aligns stakeholders around decisions, success metrics, and timelines. Communicates recommendations, trade-offs, and risks -- not just progress. Measures success using adoption signals (usage, business impact).
- **L6**: "I would trust this person to advise senior executives, drive alignment under tension, and deliver outcomes the business can measure." Communicates with authority at all levels to drive alignment and decisions. Establishes shared success metrics across all key stakeholders. Drives commitment and follow-through that results in sustained adoption and impact.

**Culture Principles & Soft Skills** (First Principles, Bias for Action, Learning & Curiosity, Raise the Bar):

- **L4**: "I would trust this person to keep pace, learn on the fly, and remain effective as things change." Described concrete situations where requirements or constraints changed, and they adjusted without stalling. Gave specific examples of learning something new mid-stream and applying it. Pointed to actions they took to surface or address issues early.
- **L5**: "I would trust this person to operate independently in ambiguity and keep the team moving forward." Walked through ambiguous situations where they made judgment calls without full information. Explained how they rapidly acquired missing context or skills and used it to drive decisions. Demonstrated bringing structure, priorities, or momentum to unclear situations.
- **L6**: "I would trust this person to thrive in rapid growth and help others do the same." Shared examples where they identified emerging risks or opportunities early and mobilized others to act. Described how they created clarity or direction for others when priorities or conditions were shifting. Demonstrated maintaining high standards while operating at sustained velocity.

### Raise the Bar Mentality (ask every time):
- Would we fight for this hire (e.g., if an offer was turned down during approval)?
- Are they above today's team average in >= 2 dimensions?
- Do they bring a distinctive strength we currently lack?
- If the answer is "not sure" for any of these questions -> NO HIRE.

---

## Appendix B: DSA Hiring Leveling Guide (Embedded Reference)

Use this when the candidate is interviewing for a **DSA (Data Science Architect)** role.

### Relevant Experience

| | L4 | L5 | L6 |
|---|---|---|---|
| Experience | Associate: 3+ Years | Professional: 5+ Years | Senior: 8+ years |
| Assumptions | Assume they know something | Assume they know most things | Assume they know all things |
| Impact | Owns post-sales execution, either independently or in partnership with more senior ICs | Influences and/or defines the technical execution strategy for individual use cases | Influences and/or defines the technical execution strategy in high-value or strategic accounts |
| Complexity | Few concurrent, moderately complex use cases | One or more moderately complex use cases or multiple workstreams | High-complexity customer use cases |
| Influence | First-line managers internally; Begins to own frontline customer & tech stakeholders | Tech leads/architects; Trusted advisor to front-line tech stakeholders | BU+2-BU+1 leaders internally; Director/VP/Head of Analytics level externally |

### Capabilities / Spike Areas (must meet baseline for all, strong in 2 of 4)

**Technical Problem Solving** (Platform Operational Excellence, First Principles Thinking, AI-Builder Mindset):

- **L4**: "I could trust this person to own a scoped customer use case and build a working solution with light guidance." Described problems with multiple technical components or constraints. Used first principles to reason about the solution before choosing tools. Hands-on built, tested, or iterated on something tangible to solve scoped problems. Addressed technical (performance, cost, feasibility) pushback along the way, and escalated for complex issues.
- **L5**: "I could put this person in front of a customer, without me in the room, and trust them to scope, implement, and technically defend a credible solution." Independently unblocked complex delivery (unclear requirements, competing constraints, evolving goals). Drove technical decisions with trade-offs (performance, scale, cost, governance) through testing or structured analysis. Iterated based on feedback or failure, not just success. Turned delivery friction or technical objections into concrete design changes or reusable assets.
- **L6**: "I would put this person in front of a top-tier customer or executive sponsor and expect them to raise the bar for how we build and reason solutions." Addressed problems spanning multiple systems, teams, or stakeholders. Used structured validation (e.g., benchmarking, architecture reviews) to challenge assumptions early. Built and scaled reusable assets from identified customer situations. Anticipated technical risks before they surfaced, were trusted in critical escalations.

**Tech Bar** (Design & Architecture, Data & AI Industry, Vibe/Coding Skills, Cloud & Platform, Tech Spike: AI/ML, DE, DW):

- **L4**: Think Proficient: "They get it, but might need support or to double-check documentation before answering." Demonstrates foundational knowledge of cloud-native services and key competitive technologies. Recommends standard features to support small-scale secure deployments. Understands key cloud platform services and how Databricks integrates with them.
- **L5**: Think Proficient: "They could confidently carry most technical conversations on their own." Leads technical post-sales discussions and provides recommendations tailored to customer requirements. Applies knowledge of industry trends and competitive technologies to customer solutions. Designs secure, governed, and scalable Databricks architectures integrated with cloud storage, networking, and identity systems.
- **L6**: Think Expert: "They know this so well they could redesign it if needed." Recognized as SME in one or more Databricks subject areas with deep expertise. Recognized as expert in emerging Data + AI trends or competitive positioning. Solves platform-wide challenges across use cases. Builds reusable frameworks for governance, security, and cloud integration.

**Execution & Collaboration** (Customer Advisor, Stakeholder Alignment, Delivery Leadership, Escalation Management):

- **L4**: "I would trust this person to clearly communicate status, execute on a defined scope, and confirm the solution met the intended outcome." Owns specific deliverables and follows through with clear updates and next steps. Collaborates effectively with account teams, partners, and customer engineers to unblock execution. Defines basic success criteria tied to production readiness or use case completion. Communicates clearly with FLM internally, and technical stakeholders externally.
- **L5**: "I would trust this person to independently advise a customer, align stakeholders around clear decisions, and drive adoption of the solution." Aligns stakeholders around decisions, success metrics, and timelines, pushes back effectively when needed. Communicates recommendations, trade-offs, and risks, not just progress. Measures success using adoption signals (usage, business impact). Drives structured delivery and architecture discussions with senior stakeholders.
- **L6**: "I would trust this person to advise senior executives, drive alignment under tension, and deliver outcomes the business can measure." Communicates with authority at executive levels (BU+1 and BU+2 level internally, VP+ level externally). Establishes shared success metrics across all key stakeholders. Drives commitment and follow-through that results in sustained adoption and measurable business impact. Is able to de-escalate effectively.

**Culture Principles & Soft Skills** (Learning & Curiosity, Bias for Action, Communication):

- **L4**: "I would trust this person to keep pace, learn on the fly, and remain effective as things change." Described delivery situations where requirements, data constraints or performance expectations changed, and they adjusted without stalling. Gave specific examples of learning new platform capabilities or architectural patterns mid-stream and applying them. Pointed to actions they took to surface or address issues early.
- **L5**: "I would trust this person to operate independently in ambiguity and keep the team moving forward." Walked through ambiguous delivery or architectural situations where they made judgment calls without full information. Used data and platform telemetry (Truth-Seeking) to inform decisions rather than relying on opinion or hierarchy. Brought structure and prioritization to unblock use case execution or adoption when stakeholders were misaligned.
- **L6**: "I would trust this person to thrive in rapid growth and help others do the same." Identified systemic risks early and mobilized internal teams, partners, and customers to act. Described how they created clarity or direction for others when priorities or conditions were shifting. Demonstrated maintaining high standards while operating at sustained velocity.

### Raise the Bar Mentality (ask every time):
- Would we fight for this hire (e.g., if an offer was turned down during approval)?
- Are they above today's team average in >= 2 dimensions?
- Do they bring a distinctive strength we currently lack?
- If the answer is "not sure" for any of these questions -> NO HIRE.
