<!-- owner: shared | audience: all-pms | last-updated: 2026-03 -->
<!-- purpose: Export Granola meeting transcripts to markdown files for local reference -->

# Export Granola Transcripts

Export meeting transcripts from Granola's local cache to markdown files. Useful for backing up transcripts, bulk searching across meetings, or working with transcripts offline.

## Instructions

0. Check the auto-memory (MEMORY.md) for the user's initials (e.g. `CR`). Set `{initials}` accordingly.

1. Run the export script:
   ```
   python3 scripts/export_granola_transcripts.py
   ```

2. The script will:
   - Read Granola's local cache at `~/Library/Application Support/Granola/cache-v3.json`
   - Parse all meetings and their transcripts
   - Create markdown files with meeting title, date, participants, speakers, and full transcript
   - Skip files that already exist (safe to re-run)
   - Output to `team/{initials}/granola-transcripts/` (gitignored) by default

3. The output directory can be customised via the `GRANOLA_BACKUP_DIR` environment variable:
   ```
   GRANOLA_BACKUP_DIR=/path/to/dir python3 scripts/export_granola_transcripts.py
   ```

4. After export, report to the user:
   - How many new transcripts were exported
   - How many were skipped (already existed)
   - Date range covered
   - Where the files are located

5. If the user wants to search for something across their transcripts, use Grep to search the output directory.

## Notes

- Granola must be installed and have cached meetings locally for this to work
- Transcripts are gitignored — they contain potentially sensitive meeting content
- File naming format: `YYYY-MM-DD_HHMM_{safe_title}.md`
