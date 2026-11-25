# Load Jobs
Description: Query and filter mocked job postings for HR recruiter conversations.

Use this skill when the candidate has enough requirement details to search jobs, or when the agent needs to explain what opportunities are available.

Input contract:
- `role`: desired role.
- `location`: desired location.
- `workMode`: remote, hybrid, or onsite.
- `salaryMinVnd`: expected minimum salary in Vietnamese Dong (VND). IMPORTANT: If the candidate gives the salary in USD (e.g. 2k net, 2,000 USD), you MUST convert it to VND by multiplying by 25,000 (e.g. 2000 USD = 50,000,000 VND) before passing it.
- `skills`: relevant skills.

Output contract:
- Matching jobs sorted by rough relevance.
- `filtersApplied` for transparency.
