# Submit Application
Description: Submit a job application for the candidate to a specific job posting.

Use this skill only after the candidate clearly confirms they want to apply to a specific job posting surfaced in this conversation.
Do not invoke this tool if the job posting is not identified or if the candidate has not given explicit confirmation to apply.

Input contract:
- `jobId`: The database ID or external ID of the job posting to apply to.
- `note`: Optional cover note or comment from the candidate.

Output contract:
- `applicationId`: Unique ID of the created or existing application.
- `created`: Boolean indicating if a new application record was created (`true`) or if they had already applied (`false`).
- `jobTitle`: Title of the job posting.
- `companyName`: Name of the hiring company.
