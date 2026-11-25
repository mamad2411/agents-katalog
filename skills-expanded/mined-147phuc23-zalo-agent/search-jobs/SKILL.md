# Twenty — Search jobs

Description: Query Twenty job postings with optional filters (search + filter combined).

When to use:

- Candidate asks for openings or after enough requirement detail exists.

Input contract:
- `salaryMinVnd`: expected minimum salary in Vietnamese Dong (VND). IMPORTANT: If the candidate gives the salary in USD (e.g. 2k net, 2,000 USD), you MUST convert it to VND by multiplying by 25,000 (e.g. 2000 USD = 50,000,000 VND) before passing it.
