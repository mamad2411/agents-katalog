---
name: shorter
description: Make the draft shorter
metadata:
  godwit-action-on: "draft,selection"
  godwit-action-output: "replace-draft"
---

Make the text noticeably shorter by removing filler and repetition.

If a subject is provided in <subject>, keep it unless it is clearly wordy, in which case shorten it. Format your output as:
<subject>Subject</subject>
<body>Concise HTML body</body>

If no subject was provided, return only the rewritten body as HTML.

Keep the meaning, facts, names and links. Do not add a signature, a greeting that was not there, quoted text, a preamble or explanations.
