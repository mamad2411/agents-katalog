---
name: youtube-extractor
description: Extracts transcript, metadata (title, channel, duration), thumbnail URL, and other details from YouTube videos, then generates an Obsidian note using the youtube-video-notes template. Use when the user provides YouTube links and wants structured notes in Obsidian format.
license: MIT
compatibility: Requires Python 3.8+, yt-dlp library, and internet access.
metadata:
  author: opencode
  version: "1.0"
---

# YouTube Video Extractor Skill

This skill extracts comprehensive data from YouTube videos and formats it into an Obsidian note using the provided template.

## Usage

When given a YouTube URL, follow these steps:

1. **Extract Video Data**: Run the extraction script to get metadata, transcript, and thumbnail.
   - Command: `python scripts/extract_youtube.py <YOUTUBE_URL>`
   - This will output JSON with extracted data.

2. **Generate Obsidian Note**: Use the extracted data to fill the template from `../../../obsidian-templates/templates/youtube-video-notes/advanced.md`

3. **Fill Template Placeholders**:
   - Replace `{{date}}` with current date (YYYY-MM-DD)
   - Replace `{{video_url}}` with the YouTube URL
   - Replace `{{channel}}` with channel name
   - Replace `{{title}}` with video title
   - Replace `{{duration}}` with video duration (HH:MM:SS)
   - Replace `{{topic}}` with inferred topic (e.g., from title or description)
   - Add transcript content to the note if available
   - Fill in Key Takeaways, Quotes, etc. from transcript if possible (or leave as template)

4. **Output the Complete Note**: Provide the filled template as the final output.

## Dependencies

- Python 3.8+
- External libraries (install via `pip install -r requirements.txt`):
  - `yt-dlp`: For video metadata
  - `youtube-transcript-api`: For extracting transcripts
  - `google-generativeai`: For AI analysis and summarization
  - `python-dotenv`: For managing environment variables


## Examples

Input: https://youtu.be/OPH4yNvuMr8

Output: A complete Obsidian note with filled frontmatter and sections.

## Edge Cases

- If no transcript available, note that in the template.
- If video is private or unavailable, handle error gracefully.
- For long transcripts, summarize or truncate appropriately.