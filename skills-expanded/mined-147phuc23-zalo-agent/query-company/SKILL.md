# Query Company
Description: Query detailed company profile information including introduction, benefits, work style, leadership, products, and materials.

Use this skill when the candidate asks for details about a specific hiring company (such as introduction, work style, benefits, etc.) or when you need to provide context about a company before proposing an interview.

Input contract:
- `name`: exact or partial name of the company to query.

Output contract:
- Company details including: name, introduction, benefits, work style, website, leadership, products, materials, interviewProcess, researchedAt.
- If a requested field is empty or researchedAt is null, answer with what exists and call `knowledge_recordGap`.
