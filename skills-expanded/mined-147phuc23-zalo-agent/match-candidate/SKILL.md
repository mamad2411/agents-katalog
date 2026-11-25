# Match Candidate
Description: Match the candidate's profile to available active jobs, scoring them based on skills and search terms.

Call this skill to find the best job matches for the candidate based on their profile (skills, summary, experience).
It computes a match score out of 1.0 using full-text search relevance and skill overlap.

Input contract:
- `limit`: Optional max number of jobs to return (default: 5).

Output contract:
- Returns an array of matched jobs, including title, company name, match score, required skills, work mode, location, and a description.
- Salary fields are redacted/redacted as "competitive" or general terms in the output to prevent displaying raw numbers to candidates.
