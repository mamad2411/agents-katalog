# Field Classifier Skill

Purpose: assign each field a canonical kind before choosing an answer.

Examples:
- `First Name` -> `identity.first_name`
- `LinkedIn Profile` -> `links.linkedin`
- `Current/Previous Employer` -> `work.current_or_previous_employer`
- `Last University Attended` -> `education.school`

Rules:
- Use the field's own label/name/id/placeholder first.
- Treat surrounding text as context only.
- Classify work and education identity fields before generic website/link fields.

Code:
- Chrome extension: `autofill_extension/src/content.js` `classifyFieldKind`.
- Playwright agent: `application_agent/agent/field_kinds.py`.
