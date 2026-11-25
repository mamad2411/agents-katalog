---

name: rei-ai-zoom-processor
description: rei-ai-zoom-processor lets the user turn a Zoom or any video transcript into a structured Markdown document and PDF with bullet-point summaries, timestamps, and extracted resources, which is useful when they want to capture meeting notes, create training materials, or turn recorded conversations into searchable, shareable documents without manual summarization.

---
Processes a Zoom (or any video) transcript with an LLM to produce three structured sections — summary, timestamped key topics, and resource list — then writes them to a Markdown file and PDF.

## What This Skill Does

This skill rei-ai-zoom-processor lets the user turn a Zoom or any video transcript into a structured Markdown document and PDF with bullet-point summaries, timestamps, and extracted resources, which is useful when they want to capture meeting notes, create training materials, or turn recorded conversations into searchable, shareable documents without manual summarization.

## Workflow

1. **Save the transcript** to a `.txt` file (e.g. `~/upload/transcript.txt`). If the user pastes raw text, write it to a file first.

2. **Run the processing script:**

```bash
python3 ~/.openclaw/workspace/skills/rei-ai-zoom-processor/scripts/process_transcript.py /path/to/transcript.txt
```

3. **Outputs** are saved alongside the transcript file (or use `--output-dir` to specify):
   - `transcript_output.txt` — raw structured text with all three sections
   - `transcript_summary.md` — formatted Markdown (title, summary, bullets, resources)
   - `transcript_summary.pdf` — PDF version via `pandoc` (requires `pandoc` installed on the system)

4. **Deliver** both `transcript_summary.pdf` and `transcript_summary.md` to the user as attachments.

## Optional: Google Doc Creation

Pass `--google-doc` flag to also attempt creating a Google Doc:

```bash
python3 ~/.openclaw/workspace/skills/rei-ai-zoom-processor/scripts/process_transcript.py /path/to/transcript.txt --google-doc
```

This requires a `credentials.json` file placed at `~/.openclaw/workspace/skills/rei-ai-zoom-processor/credentials.json`. Follow the [Google Docs API Python Quickstart](https://developers.google.com/workspace/docs/api/quickstart/python) to obtain one. On first run, a browser window will open for OAuth authorization; a `token.json` is saved for subsequent runs.

If `credentials.json` is absent, the script skips Google Doc creation gracefully and still produces the Markdown and PDF outputs.

## Notes

- The script auto-infers the document title from the transcript's first line or via LLM.
- Source URL detection: if a YouTube or HTTP URL appears in the first 10 lines of the transcript, it is included as the source link in the Markdown header.
- Default LLM model: `gemini-2.5-flash`. Change via the `model` parameter in `llm()` if needed.
