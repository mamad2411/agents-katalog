---
name: artifact-plugin-creator
description: Design Web Terminal template artifact plugins with schema, demo data, and live preview sessions.
---

# Artifact Plugin Creator

Use this skill when creating or refining a Web Terminal artifact plugin.

Required workflow:

1. Clarify the artifact purpose: usage scenario, audience, source data, terminal or agent workflow, decisions supported, and final artifact name candidates.
2. Draft the data contract first. Define `json_schema` with required fields, types, constraints, and representative nested structures.
3. Create English and Chinese demo data that match the schema and show realistic content. Include edge cases when they affect the UI.
4. Build template plugin components:
   - `python_source` declares at least `ARTIFACT_KIND`, `LABEL`, and `DEFAULT_TITLE`.
   - `prompt_template` tells the generating agent what JSON to produce.
   - `html_template` renders `content` without external assets.
   - `json_schema` validates generated and demo content.
   - English and Chinese demo JSON preview the artifact before real generation.
5. Keep a stable `preview_id` for the whole drafting session. Generate it once if the user did not provide one.
6. Call `upsert_artifact_plugin_preview` after each meaningful schema, prompt, HTML, or demo-data update. Reuse the same `preview_id`.
7. If the preview is invalid, inspect `last_error`, update the schema/data/template, and upsert again.
8. Ask the user to review the rendered artifact preview in the current terminal's Artifacts tab before finalizing.
9. Only prepare the final plugin for save after the user accepts the schema, demo data, and preview behavior.

Preview tool payload:

```json
{
  "preview_id": "stable optional UUID",
  "title": "Preview title",
  "python_source": "...",
  "prompt_template": "...",
  "html_template": "...",
  "json_schema": {},
  "demo_content_json": {}
}
```

Design rules:

- Use `preview_id` as the draft identity; never depend on `artifact_kind` for preview continuity.
- Keep both demo variants schema-valid. Use one variant in `demo_content_json` for each preview upsert, and mention the other variant to the user so both rendered outputs can be reviewed.
- Prefer explicit schema fields over loose free-form objects when the UI needs stable rendering.
- Keep the demo data small enough to inspect but complete enough to catch layout and validation failures.
- Do not create real `TerminalArtifact` rows for design previews.
- Do not invent production data. Mark uncertain fields and ask before baking them into the schema.
