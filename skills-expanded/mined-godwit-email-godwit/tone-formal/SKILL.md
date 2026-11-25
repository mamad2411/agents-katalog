---
name: tone-formal
description: Rewrite the draft in a formal tone
metadata:
  godwit-action-on: "draft,selection"
  godwit-action-output: "replace-draft"
---

Rewrite the text in a formal, polite and professional tone.

If a subject is provided in <subject>, keep it unless its tone clearly clashes with a formal email, in which case make it formal. Format your output as:
<subject>Subject</subject>
<body>Formal HTML body</body>

If no subject was provided, return only the rewritten body as HTML.

Keep the meaning, facts, names and links. Do not add a signature, a greeting that was not there, quoted text, a preamble or explanations.
