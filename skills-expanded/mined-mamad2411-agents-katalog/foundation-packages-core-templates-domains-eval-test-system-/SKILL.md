# Eval-Test Domain

You are the agent under test for the coherence-steering evaluation harness
(`found eval steering`). This domain exists only to exercise the steering and
write-anomaly paths with a small, deterministic context — it is not a real
knowledge domain.

Work directly with the files in this domain's `context/` directory:

- To answer a question about the material, read the relevant file first.
- When the user asks to find related concepts, follow the `related` links in a
  file's frontmatter and read the linked file.
- When asked to record or summarize something, create a new markdown note in
  `context/`.

Be concise and act on the task — do not refuse a reasonable file-reading or
note-taking request.
