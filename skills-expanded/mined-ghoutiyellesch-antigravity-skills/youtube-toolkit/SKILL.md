---
name: youtube-toolkit
description: Consolidated toolkit for youtube. Covers youtube-summarizer, youtube-automation
---
# Youtube Toolkit

## Core Capabilities
# Youtube Toolkit

# youtube-summarizer

## Purpose

This skill extracts transcripts from YouTube videos and generates comprehensive, verbose summaries using the STAR + R-I-S-E framework. It validates video availability, extracts transcripts using the `youtube-transcript-api` Python library, and produces detailed documentation capturing all insights, arguments, and key points.

The skill is designed for users who need thorough content analysis and reference documentation from educational videos, lectures, tutorials, or informational content.

## When to Use This Skill

This skill should be used when:

- User provides a YouTube video URL and wants a detailed summary
- User needs to document video content for reference without rewatching
- User wants to extract insights, key points, and arguments from educational content
- User needs transcripts from YouTube videos for analysis
- User asks to "summarize", "resume", or "extract content" from YouTube videos
- User wants comprehensive documentation prioritizing completeness over brevity

## Step 0: Discovery & Setup

Before processing videos, validate the environment and dependencies:

```bash
# Check if youtube-transcript-api is installed
python3 -c "import youtube_transcript_api" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  youtube-transcript-api not found"
    # Offer to install
fi

# Check Python availability
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi
```

**Ask the user if dependency is missing:**

```
youtube-transcript-api is required but not installed.

Would you like to install it now?
- [ ] Yes - Install with pip (pip install youtube-transcript-api)
- [ ] No - I'll install it manually
```

**If user selects "Yes":**

```bash
pip install youtube-transcript-api
```

**Verify installation:**

```bash
python3 -c "import youtube_transcript_api; print('✅ youtube-transcript-api installed successfully')"
```

## Main Workflow

### Progress Tracking Guidelines

Throughout the workflow, display a visual progress gauge before each step to keep the user informed. The gauge format is:

```bash
echo "[████░░░░░░░░░░░░░░░░] 20% - Step 1/5: Validating URL"
```

**Format specifications:**
- 20 characters wide (use █ for filled, ░ for empty)
- Percentage increments: Step 1=20%, Step 2=40%, Step 3=60%, Step 4=80%, Step 5=100%
- Step counter showing current/total (e.g., "Step 3/5")
- Brief description of current phase

**Display the initial status box before Step 1:**

```
╔══════════════════════════════════════════════════════════════╗
║     📹  YOUTUBE SUMMARIZER - Processing Video                ║
╠══════════════════════════════════════════════════════════════╣
║ → Step 1: Validating URL                 [IN PROGRESS]       ║
║ ○ Step 2: Checking Availability                              ║
║ ○ Step 3: Extracting Transcript                              ║
║ ○ Step 4: Generating Summary                                 ║
║ ○ Step 5: Formatting Output                                  ║
╠══════════════════════════════════════════════════════════════╣
║ Progress: ██████░░░░░░░░░░░░░░░░░░░░░░░░  20%               ║
╚══════════════════════════════════════════════════════════════╝
```

### Step 1: Validate YouTube URL

**Objective:** Extract video ID and validate URL format.

**Supported URL Formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

**Actions:**

```bash
# Extract video ID using regex or URL parsing
URL="$USER_PROVIDED_URL"

# Pattern 1: youtube.com/watch?v=VIDEO_ID
if echo "$URL" | grep -qE 'youtube\.com/watch\?v='; then
    VIDEO_ID=$(echo "$URL" | sed -E 's/.*[?&]v=([^&]+).*/\1/')
# Pattern 2: youtu.be/VIDEO_ID  
elif echo "$URL" | grep -qE 'youtu\.be/'; then
    VIDEO_ID=$(echo "$URL" | sed -E 's/.*youtu\.be\/([^?]+).*/\1/')
else
    echo "❌ Invalid YouTube URL format"
    exit 1
fi

echo "📹 Video ID extracted: $VIDEO_ID"
```

**If URL is invalid:**

```
❌ Invalid YouTube URL

Please provide a valid YouTube URL in one of these formats:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID

Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Step 2: Check Video & Transcript Availability

**Progress:**
```bash
echo "[████████░░░░░░░░░░░░] 40% - Step 2/5: Checking Availability"
```

**Objective:** Verify video exists and transcript is accessible.

**Actions:**

```python
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import sys

video_id = sys.argv[1]

try:
    # Get list of available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print(f"✅ Video accessible: {video_id}")
    print("📝 Available transcripts:")
    
    for transcript in transcript_list:
        print(f"  - {transcript.language} ({transcript.language_code})")
        if transcript.is_generated:
            print("    [Auto-generated]")
    
except TranscriptsDisabled:
    print(f"❌ Transcripts are disabled for video {video_id}")
    sys.exit(1)
    
except NoTranscriptFound:
    print(f"❌ No transcript found for video {video_id}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error accessing video: {e}")
    sys.exit(1)
```

**Error Handling:**

| Error | Message | Action |
|-------|---------|--------|
| Video not found | "❌ Video does not exist or is private" | Ask user to verify URL |
| Transcripts disabled | "❌ Transcripts are disabled for this video" | Cannot proceed |
| No transcript available | "❌ No transcript found (not auto-generated or manually added)" | Cannot proceed |
| Private/restricted video | "❌ Video is private or restricted" | Ask for public video |

### Step 3: Extract Transcript

**Progress:**
```bash
echo "[████████████░░░░░░░░] 60% - Step 3/5: Extracting Transcript"
```

**Objective:** Retrieve transcript in preferred language.

**Actions:**

```python
from youtube_transcript_api import YouTubeTranscriptApi

video_id = "VIDEO_ID"

try:
    # Try to get transcript in user's preferred language first
    # Fall back to English if not available
    transcript = YouTubeTranscriptApi.get_transcript(
        video_id, 
        languages=['pt', 'en']  # Prefer Portuguese, fallback to English
    )
    
    # Combine transcript segments into full text
    full_text = " ".join([entry['text'] for entry in transcript])
    
    # Get video metadata
    from youtube_transcript_api import YouTubeTranscriptApi
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print("✅ Transcript extracted successfully")
    print(f"📊 Transcript length: {len(full_text)} characters")
    
    # Save to temporary file for processing
    with open(f"/tmp/transcript_{video_id}.txt", "w") as f:
        f.write(full_text)
    
except Exception as e:
    print(f"❌ Error extracting transcript: {e}")
    exit(1)
```

**Transcript Processing:**

- Combine all transcript segments into coherent text
- Preserve punctuation and formatting where available
- Remove duplicate or overlapping segments (if auto-generated artifacts)
- Store in temporary file for analysis

### Step 4: Generate Comprehensive Summary

**Progress:**
```bash
echo "[████████████████░░░░] 80% - Step 4/5: Generating Summary"
```

**Objective:** Apply enhanced STAR + R-I-S-E prompt to create detailed summary.

**Prompt Applied:**

Use the enhanced prompt from Phase 2 (STAR + R-I-S-E framework) with the extracted transcript as input.

**Actions:**

1. Load the full transcript text
2. Apply the comprehensive summarization prompt
3. Use AI model (Claude/GPT) to generate structured summary
4. Ensure output follows the defined structure:
   - Header with video metadata
   - Executive synthesis
   - Detailed section-by-section breakdown
   - Key insights and conclusions
   - Concepts and terminology
   - Resources and references

**Implementation:**

```bash
# Use the transcript file as input to the AI prompt
TRANSCRIPT_FILE="/tmp/transcript_${VIDEO_ID}.txt"

# The AI agent will:
# 1. Read the transcript
# 2. Apply the STAR + R-I-S-E summarization framework
# 3. Generate comprehensive Markdown output
# 4. Structure with headers, lists, and highlights

Read "$TRANSCRIPT_FILE"  # Read transcript into context
```

Then apply the full summarization prompt (from enhanced version in Phase 2).

### Step 5: Format and Present Output

**Progress:**
```bash
echo "[████████████████████] 100% - Step 5/5: Formatting Output"
```

**Objective:** Deliver the summary in clean, well-structured Markdown.

**Output Structure:**

```markdown
# [Video Title]

**Canal:** [Channel Name]  
**Duração:** [Duration]  
**URL:** [https://youtube.com/watch?v=VIDEO_ID]  
**Data de Publicação:** [Date if available]

## 📝 Detailed Summary

### [Topic 1]

[Comprehensive explanation with examples, data, quotes...]

#### [Subtopic 1.1]

[Detailed breakdown...]

### [Topic 2]

[Continued detailed analysis...]

## 📚 Concepts and Terminology

- **[Term 1]:** [Definition and context]
- **[Term 2]:** [Definition and context]

## 📌 Conclusion

[Final synthesis and takeaways]

### **Example 2: Missing Dependency**

**User Input:**
```
claude> summarize this youtube video https://youtu.be/abc123
```

**Skill Response:**

```
⚠️  youtube-transcript-api not installed

This skill requires the Python library 'youtube-transcript-api'.

Would you like me to install it now?
- [ ] Yes - Install with pip
- [ ] No - I'll install manually
```

**User selects "Yes":**

```bash
$ pip install youtube-transcript-api
Successfully installed youtube-transcript-api-0.6.1

✅ Installation complete! Proceeding with video summary...
```

### **Example 4: Invalid URL**

**User Input:**
```
claude> summarize youtube video www.youtube.com/some-video
```

**Skill Response:**

```
❌ Invalid YouTube URL format

Expected format examples:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID

Please provide a valid YouTube video URL.
```

## 📊 Executive Summary

This video provides a comprehensive introduction to the fundamental concepts of Artificial Intelligence (AI), designed for beginners and professionals who want to understand the technical foundations and practical applications of modern AI. The instructor covers everything from basic definitions to machine learning algorithms, using practical examples and visualizations to facilitate understanding.

[... continued detailed summary ...]
```

**Save Options:**

```
What would you like to save?
→ Summary + raw transcript

✅ File saved: resumo-exemplo123-2026-02-01.md (includes raw transcript)
[████████████████████] 100% - ✓ Processing complete!
```

Welcome to this comprehensive tutorial on machine learning fundamentals. In today's video, we'll explore the core concepts that power modern AI systems...
```

**Version:** 1.2.0
**Last Updated:** 2026-02-02
**Maintained By:** Eric Andrade

---

# YouTube Automation via Rube MCP

Automate YouTube operations through Composio's YouTube toolkit via Rube MCP.

## Prerequisites

- Rube MCP must be connected (RUBE_SEARCH_TOOLS available)
- Active YouTube connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `youtube`
- Always call `RUBE_SEARCH_TOOLS` first to get current tool schemas

## Setup

**Get Rube MCP**: Add `https://rube.app/mcp` as an MCP server in your client configuration. No API keys needed — just add the endpoint and it works.

1. Verify Rube MCP is available by confirming `RUBE_SEARCH_TOOLS` responds
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `youtube`
3. If connection is not ACTIVE, follow the returned auth link to complete Google OAuth
4. Confirm connection status shows ACTIVE before running any workflows

## Core Workflows

### 1. Upload and Manage Videos

**When to use**: User wants to upload a video or update video metadata

**Tool sequence**:
1. `YOUTUBE_UPLOAD_VIDEO` - Upload a new video [Required]
2. `YOUTUBE_UPDATE_VIDEO` - Update title, description, tags, privacy [Optional]
3. `YOUTUBE_UPDATE_THUMBNAIL` - Set a custom thumbnail [Optional]

**Key parameters**:
- `title`: Video title (max 100 characters)
- `description`: Video description (max 5000 bytes)
- `tags`: Array of keyword tags
- `categoryId`: YouTube category ID (e.g., '22' for People & Blogs)
- `privacyStatus`: 'public', 'private', or 'unlisted'
- `videoFilePath`: Object with `{name, mimetype, s3key}` for the video file

**Pitfalls**:
- UPLOAD_VIDEO consumes high quota; prefer UPDATE_VIDEO for metadata-only changes
- videoFilePath must be an object with s3key, not a raw file path or URL
- Tags total must not exceed 500 characters including separators
- Angle brackets `< >` in tags are automatically stripped
- Description limit is 5000 bytes, not characters (multibyte chars count more)

### 2. Search YouTube Content

**When to use**: User wants to find videos, channels, or playlists

**Tool sequence**:
1. `YOUTUBE_SEARCH_YOU_TUBE` - Search for content [Required]
2. `YOUTUBE_VIDEO_DETAILS` - Get full details for a specific video [Optional]
3. `YOUTUBE_GET_VIDEO_DETAILS_BATCH` - Get details for multiple videos [Optional]

**Key parameters**:
- `q`: Search query (supports exact phrases, exclusions, channel handles)
- `type`: 'video', 'channel', or 'playlist'
- `maxResults`: Results per page (1-50)
- `pageToken`: For pagination

**Pitfalls**:
- Search endpoint only returns 'snippet' part; use VIDEO_DETAILS for statistics
- Search results are capped at 500 total items
- Search has higher quota cost (100 units) vs list endpoints (1 unit)
- BATCH video details practical limit is ~50 IDs per call; chunk larger sets

### 3. Manage Playlists

**When to use**: User wants to create playlists or manage playlist contents

**Tool sequence**:
1. `YOUTUBE_LIST_USER_PLAYLISTS` - List user's existing playlists [Optional]
2. `YOUTUBE_CREATE_PLAYLIST` - Create a new playlist [Optional]
3. `YOUTUBE_ADD_VIDEO_TO_PLAYLIST` - Add a video to a playlist [Optional]
4. `YOUTUBE_LIST_PLAYLIST_ITEMS` - List videos in a playlist [Optional]

**Key parameters**:
- `playlistId`: Playlist ID ('PL...' for user-created, 'UU...' for uploads)
- `part`: Resource parts to include (e.g., 'snippet,contentDetails')
- `maxResults`: Items per page (1-50)
- `pageToken`: Pagination token from previous response

**Pitfalls**:
- Do NOT pass channel IDs ('UC...') as playlist IDs; convert 'UC' to 'UU' for uploads
- Large playlists require pagination via pageToken; follow nextPageToken until absent
- items[].id is not the videoId; use items[].snippet.resourceId.videoId
- Creating duplicate playlist names is allowed; check existing playlists first

### 4. Get Channel and Video Analytics

**When to use**: User wants to analyze channel performance or video metrics

**Tool sequence**:
1. `YOUTUBE_GET_CHANNEL_ID_BY_HANDLE` - Resolve a handle to channel ID [Prerequisite]
2. `YOUTUBE_GET_CHANNEL_STATISTICS` - Get channel subscriber/view/video counts [Required]
3. `YOUTUBE_LIST_CHANNEL_VIDEOS` - List all videos from a channel [Optional]
4. `YOUTUBE_GET_VIDEO_DETAILS_BATCH` - Get per-video statistics [Optional]
5. `YOUTUBE_GET_CHANNEL_ACTIVITIES` - Get recent channel activities [Optional]

**Key parameters**:
- `channelId`: Channel ID ('UC...'), handle ('@handle'), or 'me'
- `forHandle`: Channel handle (e.g., '@Google')
- `id`: Comma-separated video IDs for batch details
- `parts`: Resource parts to include (e.g., 'snippet,statistics')

**Pitfalls**:
- Channel statistics are lifetime totals, not per-period
- BATCH video details may return fewer items than requested for private/deleted videos
- Response data may be nested under `data` or `data_preview`; parse defensively
- contentDetails.duration uses ISO 8601 format (e.g., 'PT4M13S')

### 5. Manage Subscriptions and Comments

**When to use**: User wants to subscribe to channels or view video comments

**Tool sequence**:
1. `YOUTUBE_SUBSCRIBE_CHANNEL` - Subscribe to a channel [Optional]
2. `YOUTUBE_UNSUBSCRIBE_CHANNEL` - Unsubscribe from a channel [Optional]
3. `YOUTUBE_LIST_USER_SUBSCRIPTIONS` - List subscriptions [Optional]
4. `YOUTUBE_LIST_COMMENT_THREADS` - List comments on a video [Optional]

**Key parameters**:
- `channelId`: Channel to subscribe/unsubscribe
- `videoId`: Video ID for comment threads
- `maxResults`: Results per page
- `pageToken`: Pagination token

**Pitfalls**:
- Subscribing to an already-subscribed channel may return an error
- Comment threads return top-level comments with up to 5 replies each
- Comments may be disabled on some videos
- Unsubscribe requires the subscription ID, not the channel ID

## Common Patterns

### Channel ID Resolution

**Handle to Channel ID**:
```
1. Call YOUTUBE_GET_CHANNEL_ID_BY_HANDLE with '@handle'
2. Extract channelId from response
3. Use in subsequent channel operations
```

**Uploads Playlist**:
```
1. Get channel ID (starts with 'UC')
2. Replace 'UC' prefix with 'UU' to get uploads playlist ID
3. Use with LIST_PLAYLIST_ITEMS to enumerate all videos
```

### Pagination

- Set `maxResults` (max 50 per page)
- Check response for `nextPageToken`
- Pass token as `pageToken` in next request
- Continue until `nextPageToken` is absent

### Batch Video Details

- Collect video IDs from search or playlist listings
- Chunk into groups of ~50 IDs
- Call GET_VIDEO_DETAILS_BATCH per chunk
- Merge results across chunks

## Known Pitfalls

**Quota Management**:
- YouTube API has a daily quota limit (default 10,000 units)
- Upload = 1600 units; search = 100 units; list = 1 unit
- Prefer list endpoints over search when possible
- Monitor quota usage to avoid hitting daily limits

**ID Formats**:
- Video IDs: 11-character alphanumeric strings
- Channel IDs: Start with 'UC' followed by 22 characters
- Playlist IDs: Start with 'PL' (user) or 'UU' (uploads)
- Do not confuse channel IDs with playlist IDs

**Thumbnails**:
- Custom thumbnails require channel phone verification
- Must be JPG, PNG, or GIF; under 2MB
- Recommended: 1280x720 resolution (16:9 aspect ratio)

**Response Parsing**:
- Statistics values are returned as strings, not integers; cast before math
- Duration uses ISO 8601 format (PT#H#M#S)
- Batch responses may wrap data under different keys

## Quick Reference

| Task | Tool Slug | Key Params |
|------|-----------|------------|
| Upload video | YOUTUBE_UPLOAD_VIDEO | title, description, tags, categoryId, privacyStatus, videoFilePath |
| Update video | YOUTUBE_UPDATE_VIDEO | video_id, title, description, tags |
| Set thumbnail | YOUTUBE_UPDATE_THUMBNAIL | videoId, thumbnailUrl |
| Search YouTube | YOUTUBE_SEARCH_YOU_TUBE | q, type, maxResults |
| Video details | YOUTUBE_VIDEO_DETAILS | id, part |
| Batch video details | YOUTUBE_GET_VIDEO_DETAILS_BATCH | id, parts |
| List playlists | YOUTUBE_LIST_USER_PLAYLISTS | maxResults, pageToken |
| Create playlist | YOUTUBE_CREATE_PLAYLIST | (check schema) |
| Add to playlist | YOUTUBE_ADD_VIDEO_TO_PLAYLIST | (check schema) |
| List playlist items | YOUTUBE_LIST_PLAYLIST_ITEMS | playlistId, maxResults |
| Channel statistics | YOUTUBE_GET_CHANNEL_STATISTICS | id/forHandle/mine |
| List channel videos | YOUTUBE_LIST_CHANNEL_VIDEOS | channelId, maxResults |
| Channel ID by handle | YOUTUBE_GET_CHANNEL_ID_BY_HANDLE | channel_handle |
| Subscribe | YOUTUBE_SUBSCRIBE_CHANNEL | channelId |
| List subscriptions | YOUTUBE_LIST_USER_SUBSCRIPTIONS | (check schema) |
| List comments | YOUTUBE_LIST_COMMENT_THREADS | videoId |
| Channel activities | YOUTUBE_GET_CHANNEL_ACTIVITIES | (check schema) |

---
