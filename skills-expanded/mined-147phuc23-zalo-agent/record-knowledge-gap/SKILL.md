# Record Knowledge Gap
Description: Record candidate questions that the agent cannot answer due to missing company or job details.

Call this skill when the candidate asks a factual question about a company, job, benefits, process, or other recruitment facts that you cannot answer because the data does not exist or researchedAt is null.
Do not fabricate information. Instead, record the knowledge gap and tell the candidate in Vietnamese that the question is noted and the team will look into it.

Input contract:
- `question`: The candidate's question that could not be answered.
- `companyName`: Name of the company the question is about.
- `topic`: Classification of the question topic (`company`, `job`, `process`, `benefits`, `other`).
