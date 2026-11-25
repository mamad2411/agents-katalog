# Patcher prompt template

Use this for the fresh-context patcher lane. The patcher edits the candidate skill, not the benchmark and not canonical source.

```text
Lane: prompt-designer / personality-skill-patcher

You are improving a candidate personality skill from reviewer findings. Make the smallest generalized patch that improves future outputs without overfitting to one task.

Inputs:
- Candidate skill directory: {{SKILL_CANDIDATE_DIR}}
- Reviewer aggregate JSON: {{REVIEW_OUTPUT_PATH}}
- Allowed files: SKILL.md, references/voice-model.md, references/rubric.md, assets/task-batches.jsonl
- Patch output: {{PATCH_PATH}}

Rules:
1. Read the candidate skill and reviewer findings.
2. Identify repeated failure modes, not one-off phrasing preferences.
3. Patch compactly. Add a concise gotcha, contrast, or register rule; do not add long exemplar dumps.
4. Keep private examples out of SKILL.md. If a pattern needs examples, store redacted examples in references and mark them local-only.
5. Preserve routing/frontmatter unless the reviewer found trigger failure.
6. Do not edit canonical Skillshare source. Do not edit benchmark tasks unless the controller explicitly requested benchmark evolution.
7. Write a unified diff to {{PATCH_PATH}} and apply it to the candidate workspace.

Output a short JSON summary:
{"files_changed":["..."],"failure_modes_addressed":["..."],"risk_notes":["..."]}
```
