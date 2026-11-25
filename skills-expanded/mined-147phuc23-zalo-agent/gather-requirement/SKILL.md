# Gather Requirement
Description: Extract and update the candidate's job-search requirements from Zalo chat text.

Use this skill whenever the candidate gives information about desired role, salary, location, skills, experience, work mode, language, availability, or constraints. (Note: it automatically parses and converts USD salaries like "2k" or "2000" into VND).

Input contract:
- `messages`: recent candidate messages as text.
- `existingRequirement`: current known requirement fields.

Output contract:
- `requirement`: merged candidate requirement.
- `missingFields`: important fields still missing.
- `confidence`: low, medium, or high.

The skill is deterministic and should be called before matching jobs when the latest user message changes job-search criteria.
