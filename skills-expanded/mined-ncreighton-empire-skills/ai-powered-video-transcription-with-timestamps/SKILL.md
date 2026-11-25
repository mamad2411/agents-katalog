---
name: ai-powered-video-transcription-with-timestamps
description: "Transcribe videos to text with automatic timestamped segments for editing, SEO, and content repurposing. Use when the user needs accurate transcripts, captions, clip extraction, or searchable video archives."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "DEEPGRAM_API_KEY"],
        "bins": ["ffmpeg"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎬"
    }
  }
---

# AI-Powered Video Transcription with Timestamps

## Overview

This skill transforms video and audio files into searchable, timestamped transcripts with speaker identification and automatic segment detection. Perfect for content creators, podcasters, educators, and enterprises who need to extract maximum value from video content.

**Why This Matters:**
- **Content Repurposing**: Automatically extract quotes, clips, and highlights from full recordings
- **Accessibility**: Generate accurate captions and transcripts for compliance (ADA, WCAG 2.1)
- **SEO & Discovery**: Searchable transcripts improve video discoverability in Google, YouTube, and WordPress
- **Editing Efficiency**: Timestamps let editors jump to key moments without watching entire videos
- **Knowledge Management**: Build searchable video archives for internal training, documentation, and support

**Integrations & Compatibility:**
- **Video Platforms**: YouTube, Vimeo, Wistia, Loom
- **Content Management**: WordPress (via plugins), HubSpot, Contentful
- **Productivity**: Slack (post transcripts to channels), Notion (save as database entries)
- **Editing Tools**: Adobe Premiere Pro, Final Cut Pro, DaVinci Resolve (via EDL/SRT export)
- **Cloud Storage**: AWS S3, Google Drive, Dropbox, OneDrive

---

## Quick Start

### Example 1: Transcribe a Local Video File
```
Transcribe the video file at /Users/sarah/Downloads/podcast-episode-42.mp4 
with speaker identification. Output as JSON with timestamps every 30 seconds.
Include a summary of key topics discussed.
```

**What You Get:**
- Full transcript with [00:00:15] style timestamps
- Speaker labels (Speaker 1, Speaker 2, etc.)
- JSON output with start/end times for each segment
- Auto-generated summary of main topics

---

### Example 2: Extract Clips from a Long-Form Video
```
Transcribe my 2-hour webinar (webinar-2024-01-15.mov) and identify 
the top 5 most quotable moments. For each, provide:
- The exact quote
- Start and end timestamps
- Why this moment stands out
- Suggested social media caption

Format as markdown for easy sharing.
```

**What You Get:**
- 5 highlighted moments with precise timestamps
- Ready-to-post social captions
- Markdown file for documentation
- Timestamps formatted for video editors

---

### Example 3: Generate SRT Captions for YouTube
```
Convert this YouTube video (https://youtube.com/watch?v=dQw4w9WgXcQ) 
to an SRT subtitle file with timestamps. Group sentences into 
5-6 word chunks for readability. Include speaker labels.
```

**What You Get:**
- SRT file (compatible with YouTube, Vimeo, all video platforms)
- Properly timed subtitle blocks
- Ready to upload directly to video hosting platforms

---

## Capabilities

### 1. **Multi-Format Video & Audio Support**
- Video: MP4, MOV, WebM, AVI, MKV, FLV
- Audio: MP3, WAV, M4A, AAC, OGG, FLAC
- Live streams: YouTube, Twitch, Vimeo (via URL)
- Maximum file size: 2GB (larger files processed in chunks)

### 2. **Automatic Speaker Identification**
Detects and labels different speakers with confidence scores:
```
[00:00:15] Speaker 1: "Welcome to the podcast..."
[00:00:45] Speaker 2: "Thanks for having me!"
[00:01:20] Speaker 1: "So tell us about your background..."
```

### 3. **Intelligent Timestamping**
- Configurable interval: 15s, 30s, 60s, or per-sentence
- Automatic paragraph breaks at natural pauses
- Scene change detection (for multi-camera videos)
- Silence detection and removal (optional)

### 4. **Multiple Output Formats**
- **JSON**: Structured data with confidence scores
- **SRT**: Subtitle format for all video platforms
- **VTT**: WebVTT captions for web video
- **Markdown**: Human-readable with timestamps
- **EDL**: Edit Decision List for video editors
- **CSV**: Spreadsheet format for analysis

### 5. **Advanced Filtering & Cleanup**
- Remove filler words (um, uh, like, you know)
- Correct common speech-to-text errors
- Normalize timestamps across multiple speakers
- Detect and flag potentially sensitive content (PII, profanity)

### 6. **Keyword & Topic Extraction**
Automatically identifies:
- Key phrases and terminology
- Named entities (people, places, organizations)
- Sentiment per segment (positive, neutral, negative)
- Topic clusters (machine learning powered)

### 7. **SEO Optimization**
- Generate metadata descriptions from transcript
- Create searchable transcripts for WordPress
- Structured data markup for Google Rich Results
- Sitemap entries for transcript pages

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API key (for GPT-4 transcript enhancement and summarization)
export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxx"

# Deepgram API key (primary transcription engine, highly accurate)
export DEEPGRAM_API_KEY="xxxxxxxxxxxxx"

# Optional: For YouTube/Vimeo integration
export YOUTUBE_API_KEY="xxxxxxxxxxxxx"
export VIMEO_API_KEY="xxxxxxxxxxxxx"
```

### Setup Instructions

1. **Install Dependencies:**
   ```bash
   # macOS
   brew install ffmpeg

   # Ubuntu/Debian
   sudo apt-get install ffmpeg

   # Windows (via Chocolatey)
   choco install ffmpeg
   ```

2. **Get API Keys:**
   - Deepgram: https://console.deepgram.com (free tier: 50 hours/month)
   - OpenAI: https://platform.openai.com/account/api-keys
   - YouTube: https://console.cloud.google.com

3. **Configure Transcription Options:**
   ```json
   {
     "transcription": {
       "model": "deepgram-nova-2",
       "language": "en",
       "speaker_detection": true,
       "confidence_threshold": 0.85,
       "punctuation": true,
       "profanity_filter": false,
       "diarization": true
     },
     "output": {
       "formats": ["json", "srt", "markdown"],
       "timestamp_interval": 30,
       "include_speaker_labels": true,
       "include_confidence_scores": false
     },
     "processing": {
       "chunk_duration": 600,
       "parallel_chunks": 4,
       "cleanup_filler_words": true,
       "sentiment_analysis": true
     }
   }
   ```

### Advanced Options

| Option | Values | Default | Notes |
|--------|--------|---------|-------|
| `model` | `nova-2`, `enhanced`, `base` | `nova-2` | Nova-2 is most accurate; Base is fastest |
| `language` | `en`, `es`, `fr`, `de`, `ja`, etc. | `en` | Supports 100+ languages |
| `speaker_detection` | `true`, `false` | `true` | Requires minimum 30s audio per speaker |
| `timestamp_interval` | `15`, `30`, `60`, `sentence` | `30` | Granularity of timestamps |
| `profanity_filter` | `true`, `false` | `false` | Masks or removes profanity |

---

## Example Outputs

### JSON Output
```json
{
  "metadata": {
    "filename": "podcast-episode-42.mp4",
    "duration_seconds": 1847,
    "language": "en",
    "speakers_detected": 2,
    "accuracy_score": 0.94
  },
  "transcript": [
    {
      "timestamp": "00:00:15",
      "speaker": "Speaker 1",
      "text": "Welcome to the podcast.",
      "confidence": 0.98,
      "segment_id": "seg_001"
    },
    {
      "timestamp": "00:00:45",
      "speaker": "Speaker 2",
      "text": "Thanks for having me!",
      "confidence": 0.96,
      "segment_id": "seg_002"
    }
  ],
  "topics": [
    { "topic": "AI and Machine Learning", "confidence": 0.92, "mentions": 14 },
    { "topic": "Business Strategy", "confidence": 0.88, "mentions": 9 }
  ],
  "summary": "A discussion about AI adoption in enterprise...",
  "key_quotes": [
    {
      "quote": "AI is not about replacing humans...",
      "timestamp": "00:12:34",
      "speaker": "Speaker 2"
    }
  ]
}
```

### SRT Subtitle Output
```srt
1
00:00:15,000 --> 00:00:45,000
Speaker 1: Welcome to the podcast.

2
00:00:45,000 --> 00:01:20,000
Speaker 2: Thanks for having me!

3
00:01:20,000 --> 00:02:15,000
Speaker 1: So tell us about your background
and how you got into this space.
```

### Markdown Output
```markdown
# Podcast Episode 42 Transcript

**Duration:** 30:47  
**Speakers:** 2  
**Accuracy:** 94%

---

## Transcript

**[00:00:15] Speaker 1:**
Welcome to the podcast.

**[00:00:45] Speaker 2:**
Thanks for having me!

**[00:01:20] Speaker 1:**
So tell us about your background and how you got into this space.

---

## Key Topics
- AI and Machine Learning (14 mentions)
- Business Strategy (9 mentions)
- Team Building (7 mentions)

## Top Quotes
> "AI is not about replacing humans, it's about augmenting human capability."  
> — Speaker 2 at 00:12:34
```

---

## Tips & Best Practices

### 1. **Audio Quality Matters**
- **Best Results**: Quiet environment, good microphone, clear speech
- **Acceptable**: Podcast-quality audio (44.1 kHz, mono/stereo)
- **Challenging**: Noisy backgrounds, multiple overlapping speakers
- **Tip**: Pre-process audio with noise reduction (Audacity, Adobe Audition) for 5-10% accuracy improvement

### 2. **Speaker Identification**
- Works best with 2-4 distinct speakers
- Requires minimum 30 seconds of clear audio per speaker for accurate labeling
- **Tip**: Have speakers introduce themselves at the start ("Hi, I'm Alice...") for better detection
- For 5+ speakers, consider manual speaker labels in post-processing

### 3. **Language & Accents**
- Deepgram Nova-2 handles accents well (95%+ accuracy for native speakers)
- For non-native speakers or heavy accents, use `enhanced` model (+20% processing time)
- Specify language code upfront for best results

### 4. **Timestamp Precision**
- Use `timestamp_interval: 30` for most use cases (good balance of detail and readability)
- Use `timestamp_interval: sentence` for literary/academic transcripts
- Use `timestamp_interval: 15` for music/sound design where timing is critical

### 5. **Repurposing Content**
- **Clips**: Extract 30-60 second segments using timestamps for TikTok/Instagram Reels
- **Blog Posts**: Convert key quotes into blog posts with embedded video timestamps
- **Email Sequences**: Create 5-part email series from major topic breaks
- **Infographics**: Pull statistics and data points for visual content

### 6. **Scaling to Bulk Processing**
```
For 50+ videos, batch process with:
- Parallel chunk processing (set parallel_chunks: 8)
- Schedule during off-peak hours (lower API costs)
- Monitor API usage via Deepgram dashboard
- Implement retry logic for failed segments
```

### 7. **Cost Optimization**
- Deepgram pricing: $0.0043/minute (Nova-2) vs $0.0025/minute (Base model)
- **Savings Tip**: Use Base model for initial processing, Nova-2 only for critical content
- Batch similar videos together (same language, speaker count) for 10-15% cost reduction
- Cache results for re-transcription requests (avoid duplicate charges)

---

## Safety & Guardrails

### What This Skill WILL NOT Do

❌ **Automatic Copyright Detection**: This skill does not detect or prevent transcription of copyrighted content. Users are responsible for ensuring they have rights to transcribe material.

❌ **Real-Time Transcription**: Designed for post-processing; not suitable for live event captions (though output can be used for near-real-time systems).

❌ **Speaker Identification by Name**: Cannot identify who specific speakers are; only labels them as "Speaker 1," "Speaker 2," etc. Requires manual labeling for named identification.

❌ **Automatic Content Moderation**: While profanity filtering is available, this skill is not designed for content moderation at scale. Manual review recommended for sensitive content.

❌ **Emotion/Intent Analysis**: Provides sentiment (positive/negative/neutral) but not nuanced emotion detection or intent classification.

### Limitations & Boundaries

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| **Background Noise** | Accuracy drops 5-15% in noisy environments | Pre-process audio; record in quiet spaces |
| **Overlapping Speech** | Cannot accurately transcribe when 2+ people talk simultaneously | Encourage speaker turns; use speaker labels |
| **Accented Speech** | 3-8% accuracy reduction for non-native speakers | Use `enhanced` model; provide speaker intro |
| **Technical Jargon** | May misidentify domain-specific terms | Provide custom vocabulary list |
| **Audio Quality <16kHz** | Degraded accuracy below 16kHz sample rate | Recommend 44.1kHz or higher |
| **File Size >2GB** | Automatic chunking required; may extend processing | Split large files; process in parallel |

### Privacy & Data Handling

✅ **Data Retention**: Deepgram retains audio for 30 days for quality improvement (can be disabled)  
✅ **Encryption**: All API calls use TLS 1.2+; data in transit is encrypted  
✅ **PII Detection**: Optional PII masking available (detects SSNs, credit cards, phone numbers)  
✅ **GDPR Compliant**: Deepgram is GDPR-compliant; data processed in EU if requested  

⚠️ **Recommendation**: For HIPAA/FERPA content, use on-premise deployment or Deepgram's enterprise plan with data residency guarantees.

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: "Accuracy Score Below 80%"
**Causes & Fixes:**
1. **Background noise**: Re-record in quieter environment or use noise reduction
2. **Heavy accent**: Switch to `enhanced` model (takes 20% longer)
3. **Audio corruption**: Verify file integrity with `ffmpeg -v error -i file.mp4 -f null -` 
4. **Language mismatch**: Confirm language code matches actual audio

**Test Command:**
```bash
# Check audio properties
ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate,channels -of default=noprint_wrappers=1 your-file.mp4
```

---

#### Issue: "Speaker Detection Not Working"
**Causes & Fixes:**
1. **Too many speakers**: Diarization works best with 2-4 speakers; 5+