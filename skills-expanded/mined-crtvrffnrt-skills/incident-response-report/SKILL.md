---
name: incident-response-report
description: "Incident-response reporting skill for decision-ready summaries, timelines, containment records, executive handoff, remediation plans, and unresolved evidence gaps."
---

# Incident Response Report

## Mission
Turn an investigation into a concise report that a human analyst can review and close. Optimize for clarity, evidence traceability, and remediation follow-up.

## Writing rules
- Keep the tone direct and professional.
- Separate confirmed facts, indicators, and hypotheses.
- Use UTC timestamps unless the user asks otherwise.
- Cite the telemetry source or log family when possible.
- Do not overstate certainty.
- If evidence is partial, say what is missing and how that limits the conclusion.
- Default to Markdown unless the user requests HTML or another format.
- If public IPs appear in the source material and no enrichment is already present, prefer local enrichment before finalizing the report. If enrichment tooling is unavailable, mark the gap and avoid overclaiming.

## Standard structure
1. Executive Assessment
2. Confirmed Facts
3. Key Indicators
4. Analytical Assessment
5. Containment and Remediation
6. Recommended Actions
7. Timeline
8. Limitations
9. Appendix / IoCs

## Suggested content

### Executive Assessment
- State whether compromise is confirmed, suspected, historical, attempted, or unsupported.
- Note severity.
- List the primary affected users, hosts, or resources.

### Confirmed Facts
- Include only telemetry-supported statements.

### Key Indicators
- List IOCs and behavioral indicators with confidence notes.
- For public IPs, include the combined results from `/root/Tools/IncidentResponseScripts/vpnchecker.sh` and `/root/Tools/IncidentResponseScripts/ipir.sh` when available, or state clearly that enrichment could not be completed.

### Analytical Assessment
- Explain the likely attack path.
- Note alternative explanations and gaps.

### Containment and Remediation
- Record actions already taken and who took them.
- Include preservation steps when relevant.

### Recommended Actions
- Add scoped containment, scoping, eradication, and recovery steps.

### Timeline
- Order by first seen to last seen.
- Include source references where practical.

### Limitations
- Note missing telemetry, retention constraints, license gaps, or unvalidated assumptions.

## Output quality
- Use tables when they improve clarity.
- Prefer short sections over narrative walls.
- Keep the report suitable for technical stakeholders and leadership handoff.
- Keep raw-tool provenance for public IP assessments so another analyst can reproduce the conclusion.
- Report unresolved evidence gaps explicitly and keep severity tied to demonstrated impact and available telemetry.
