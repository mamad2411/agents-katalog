---
name: convert-to-markdown
description: 'Use to convert files (PDF, Word, Excel, PowerPoint, Images, Audio, HTML, HTM, CSV, JSON, XML, ZIP, EPubs, MHTML) and URLs (YouTube URL, YouTube ID) into Markdown natively.'
---

# Convert files and URLs into Markdown with tools

## When to Use
- You need to read documents or data and pipe them into a Markdown context
- You need a transcript of a YouTube video
- Converting PDF, DOCX, PPTX, XLSX, CSV, JSON, XML, Images, Audio, HTML, HTM, ZIP, EPubs, MHTML

## Procedure

### YouTube Transcript
To extract YouTube captions, run the [youtube-transcript script](scripts/youtube-transcript):
```bash
scripts/youtube-transcript <youtube_video_id_or_url>
```

### YouTube Transcript with metadata
To extract YouTube captions along with metadata, run the [youtube-transcript script](scripts/youtube-transcript):
```bash
scripts/youtube-transcript --info <youtube_video_id_or_url>
```

### MHTML to Markdown
```bash
scripts/mhtml-to-html <path_or_url> | uvx markitdown
```

### File and Web pages Conversion
Run `uvx markitdown` on the file path or URL:
```bash
uvx markitdown <path_or_url>
```

