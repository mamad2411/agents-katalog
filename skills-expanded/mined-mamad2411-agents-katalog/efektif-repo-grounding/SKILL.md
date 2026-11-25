---
name: efektif-repo-grounding
description: Inspect the current checkout before answering repo-dependent questions.
---

# Efektif Repo Grounding

Use this skill when you need to inspect the current checkout before answering repo-dependent questions.

## Steps

- Check cwd, git status, relevant files, scripts, and docs.
- Prefer exact file paths and commands over subsystem guesses.
- Separate confirmed repo facts from inferred context.

## Output

- Keep responses short and evidence-backed.
- Name verification performed or explain why it was not run.
- Prefer concrete next actions over broad advice.
