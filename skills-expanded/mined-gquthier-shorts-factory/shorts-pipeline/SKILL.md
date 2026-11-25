---
name: shorts-pipeline
description: Run the Shorts Factory local pipeline from owned long-form video to reviewed short clips. Use for ingestion, clipping, transcription, rendering or QA in this repository.
---

# Shorts Pipeline

Start with Démarrer: creator profile, text provider and local tools. Use `npm run factory -- add <file-or-url> --kind upload --rights` only for media the user can use. The stages are ingest → transcribe → mine → edit → hook → render → QA → review → publish. Review and publication are distinct states.

Choose a format from `templates/README.md` and its `skills/format-*/SKILL.md`. Preserve word-level timings, literal captions, truthful opening and a complete ending. For source issues inspect the job error and retry that stage; do not change clip approval or routing to bypass a failed stage. Use local data paths, never commit data or credentials.

`npm test` covers pipeline invariants with simulated providers. `tools/render-smoke.ts` exercises a real export using generated media. Optional services incur provider charges. Publication requires the user’s selected channels and explicit publish/autopilot choice.
