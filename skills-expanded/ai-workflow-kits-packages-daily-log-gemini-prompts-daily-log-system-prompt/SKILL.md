# Daily Log Prompt Pack For Gemini

Use this prompt when you want Gemini to append today's activity to a shared daily log file under the multi-AI section contract.

## Core Operating Loop

```text
identify date -> locate or create log file -> append to [Gemini] section only -> verify
```

## Behavior Guidelines

1. **Section isolation**: Gemini writes only to `## [Gemini]`. All other sections (`[Claude]`, `[Codex]`, `[Copilot]`, `[Manual]`) are read-only.

2. **Append only**: Never rewrite the full file. Locate the `[Gemini]` section and add entries at the end of it.

3. **Log file path**: Resolve the path from the user's configured vault:
   ```text
   <vault>/logs/YYYY/MM/YYYY-MM-DD-daily.md
   ```
   Replace `<vault>` with the user's configured vault root (for example, a local Markdown vault or any notes directory).
   Check whether the file exists:
   - **File absent** → create it with the standard structure, including the full section skeleton. Create any missing `YYYY/MM/` folders first.
   - **File present** → append only to the `[Gemini]` section. Leave all other sections and existing content unchanged.

4. **Entry format**:
   ```markdown
   ### HH:MM - HH:MM / topic-slug
   - what was done
   - what was verified or found
   - what is still open (if any)
   ```

5. **Verification**: After writing, confirm the file exists, the `[Gemini]` section contains the new entry, and other sections are unchanged.

## New File Structure

If no file exists for today, create:

```markdown
# Daily Log | YYYY-MM-DD

> Shared daily log. Each AI appends to its own section only. Contract: LOG_CONTRACT.md

## [Claude]
*(no activity yet)*

## [Codex]
*(no activity yet)*

## [Gemini]
### HH:MM - HH:MM / topic-slug
- entry

## [Copilot]
*(no activity yet)*

## [Manual]
*(user entries)*
```

## Output Contract

Every response should include:

```text
- Date: YYYY-MM-DD
- Log file: <path>
- Section: [Gemini] — appended
- Entry: HH:MM - HH:MM / topic-slug (N bullets)
- Other sections: unchanged
- Verification: file confirmed on disk
```

## Rules

- Do not touch other AI sections.
- Do not summarize or reorganize other sections.
- Do not claim completion without confirming the file on disk.
- If the file cannot be found or written, report the path and the error — do not silently skip.

See `LOG_CONTRACT.md` for the full multi-AI contract.
