---
name: vtt-to-text
description: >
  This skill should be used when the user pastes WebVTT (.vtt) closed caption
  content and wants it converted into a clean text file. Trigger when the user
  pastes content that starts with "WEBVTT" or contains VTT timestamp arrow
  patterns between timecodes, asks to "clean up captions", "convert subtitles
  to text", "extract text from VTT", "turn captions into a transcript", or
  wants to turn video closed captions into readable text. Also trigger when the
  user mentions converting course lecture captions or subtitle files.
---

# VTT to Text Converter

Convert pasted WebVTT closed caption content into clean, readable plain text files.

## Workflow

### Step 1: Identify VTT Content

The user will paste VTT content directly into the conversation. Recognizable by:
- A `WEBVTT` header line
- Numbered sequence blocks (bare integers on their own line)
- Timestamp lines with `-->` arrows (e.g., `00:00:03.885 --> 00:00:05.395`)
- Caption text lines between timestamps

### Step 2: Ask for Filename Details

Before processing, ask the user for three things using AskUserQuestion:

1. **Tier** — e.g., "Tier 1", "Tier 2", "Tier 3"
2. **Sprint number** — e.g., "Sprint 1", "Sprint 2", "Sprint 14"
3. **Title** — the class or lecture name, e.g., "Introduction", "Growth Strategy", "Financial Planning"

The final filename pattern is: `{Tier} - {Sprint} - {Title}.txt`
Example: `Tier 3 - Sprint 1 - Introduction.txt`

If the user has already provided any of these details in their message, skip those questions and use what they gave.

### Step 3: Parse and Clean

Save the raw VTT content to a temp file and run the bundled parser:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/vtt-to-text/scripts/parse_vtt.py < /tmp/raw_vtt.txt > /tmp/cleaned.txt
```

The parser:
- Strips the `WEBVTT` header
- Removes sequence numbers and timestamp lines
- Strips inline VTT tags
- Joins caption fragments into a continuous text stream
- Breaks into readable paragraphs (roughly every 5 sentences)

### Step 4: Save and Deliver

Read the cleaned output, save it to the user's workspace folder with the filename from Step 2, and provide a `computer://` link.

Keep the response brief — confirm the file was created and link it. No need to show the full text content.
