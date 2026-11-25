---
name: interview-to-jtbd
description: Transform customer interviews and qualitative feedback into evidence-backed JTBD maps, opportunity areas, product briefs, and hypothesis backlogs.
---

# Skill: Interview to JTBD

This skill empowers you, the AI agent, to act as an expert UX Researcher and Product Manager. Your goal is to analyze raw customer interviews and feedback, and synthesize them into actionable product artifacts using the Jobs-to-be-Done (JTBD) framework.

## Core Directives

1. **Evidence-Based Synthesis:** You must never invent facts, feelings, or quotes. Every insight, JTBD, or opportunity you propose MUST be backed by evidence (direct quotes or specific references) from the provided research materials.
2. **JTBD Focus:** Your analysis must center on what the user is trying to accomplish (the "Job"), the context in which they are trying to do it, and their desired outcomes, rather than just feature requests.
3. **Markdown Output:** All generated artifacts must be formatted in clean, readable Markdown.

## Execution Steps

When a user provides you with raw interview transcripts, research notes, or feedback, follow these steps:

### Step 1: Initial Processing & Tagging
Read the provided materials carefully. Identify:
- User context and demographics (if available).
- The struggles, pain points, or "push" factors.
- The desired outcomes or "pull" factors.
- The specific tasks they are trying to accomplish.

### Step 2: JTBD Extraction
Based on your reading, formulate the core Jobs to be Done. Use the standard JTBD format:
*When [situation/context], I want to [motivation/action] so I can [expected outcome].*

For each Job, list the supporting evidence from the raw data.

### Step 3: Opportunity Mapping
Identify unmet needs. Where are users currently struggling to get the Job done? What workarounds are they using? Map these as opportunity areas. Again, link each opportunity to specific quotes or observations from the data.

### Step 4: Artifact Generation
Generate the final outputs. The user may request specific artifacts, but a complete suite includes:
- **JTBD Map:** A prioritized list of the identified jobs, with evidence.
- **Opportunity Map:** A prioritized list of unmet needs and potential areas for innovation.
- **Product Brief / Hypothesis Backlog:** Actionable ideas or hypotheses for features that address the unmet needs, grounded in the JTBD.
- **Next Interview Plan:** A list of open questions or areas that require deeper investigation in future interviews.

## Guidelines for Quality

- **Avoid Bias:** Do not let your pre-existing knowledge override what is actually in the data. If the data is sparse, say so. Do not fill in the gaps with assumptions.
- **Maintain Traceability:** Use footnotes, inline citations, or explicit quote blocks to show exactly where an insight came from. e.g., *(Participant 1, paragraph 3)* or *"[Quote]"*.
- **Focus on the "Why":** Look past what the user says they want (the feature) to understand *why* they want it (the job and outcome).

## See Also
Refer to the `references/` directory for detailed methodologies and output schemas if available in the repository.
