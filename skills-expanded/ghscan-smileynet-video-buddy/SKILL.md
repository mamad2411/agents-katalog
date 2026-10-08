# video-buddy Claude Code skill

Use `video-buddy` as the source of truth for mechanical pipeline steps.

When handling `/intake <url>`:
- call `video-buddy --json fetch <url>` first
- if the fetched artifact is a YouTube video, continue with `transcribe`, `frames`, `correlate`, `render`
- if it is an article or paper, continue with `render`
- read the rendered draft note and companion prompt files under `intermediates/agent-prompts/`
- write prose directly into the draft note
- call `video-buddy --json finalize <id>` at the end

Do not:
- write your own fetchers or transcript extractors
- invent output paths
- skip the finalize step when the user asked for a finished note
