# HR Screening

Screen inbound applications against role requirements. Filter, summarize, and route to the CAO.

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Gmail | Read applications, send screening responses |
| Notion | Update candidate tracking board |

## Hard filters checklist

Before summarizing, check each application against these filters. If any are NOT met, mark as "filtered out" with the reason.

| Filter | Check |
|--------|-------|
| **Location** | Within required timezone range or willing to relocate (if specified) |
| **Experience level** | Meets minimum years / seniority for the role |
| **Core skills** | Has the must-have technical skills listed in the job description |
| **Language** | Meets language requirements (English fluency for all roles) |
| **Availability** | Can start within the required timeframe |
| **Work authorization** | Has or can obtain work authorization (if applicable) |

## Process

1. **Read the job description** - load the role requirements from `hr/roles/`
2. **Read all new applications** - process the full batch
3. **Apply hard filters** - check each application against the checklist above
4. **Summarize passing candidates** - for each:
   - Name, current role, company
   - Years of relevant experience
   - Key matching skills (mapped to job requirements)
   - Notable strengths or concerns
   - Recommendation: strong yes / yes / maybe / no
5. **Route to the CAO** - save the screening summary to `hr/_drafts/YYYY-MM-DD_screening-[role].md`

## Summary format

```markdown
## [Candidate Name]
- **Current**: [role] at [company]
- **Experience**: [X years relevant]
- **Key skills**: [skill 1, skill 2, skill 3]
- **Strengths**: [brief]
- **Concerns**: [brief or "none"]
- **Recommendation**: [strong yes / yes / maybe / no]
```

## Guardrails

- **No name-based inference of nationality, ethnicity, or gender** - evaluate skills and experience only
- **No age inference** from graduation dates
- **Never reject automatically** - flag as "filtered out" with reason; the CAO makes final calls
- **No outreach to candidates** - screening only, no communication
- **Keep all candidate data in** `hr/` folder only - never copy to other locations
- **PII handling** - do not include candidate emails or phone numbers in the summary

## Self-improvement

After the CAO reviews a screening batch:

1. If the CAO overrides a recommendation (promotes a "maybe" to "yes" or rejects a "yes"), note why in `hr/_insights.md`
2. If her overrides reveal a pattern (e.g. "values startup experience over years of experience", "cares more about portfolio than pedigree"), add it to the Hard filters checklist or create a new soft-signal section
3. If the summary format wasn't useful - too long, missing context, wrong emphasis - update the Summary format section
4. If a screening summary was particularly well-calibrated, save it to `hr/_examples/` as a reference (with PII removed)
