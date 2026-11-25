---
name: tone-friendly
description: Rewrite the draft in a friendly tone
metadata:
  godwit-action-on: "draft,selection"
  godwit-action-output: "replace-draft"
---

Rewrite the text in a warm, friendly and natural tone.

If a subject is provided in <subject>, keep it unless its tone clearly clashes with a friendly email, in which case make it friendly. Format your output as:
<subject>Subject</subject>
<body>Friendly HTML body</body>

If no subject was provided, return only the rewritten body as HTML.

Keep the meaning, facts, names and links. Do not add a signature, a greeting that was not there, quoted text, a preamble or explanations.
