---
name: translate-draft
description: Translate the draft into the language the user asks for
metadata:
  godwit-action-on: "draft"
  godwit-action-output: "replace-draft"
---

Translate the draft into the target language the host names.

If a subject is provided in <subject>, translate it and format your output as:
<subject>Translated Subject</subject>
<body>Translated HTML body</body>

If no subject was provided, return only the translated body as HTML.

Keep the meaning, facts, names and links. Do not add a signature, a greeting that was not there, quoted text, a preamble or explanations.
