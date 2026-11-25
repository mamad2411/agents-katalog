---
name: facebook-research-template
parent: facebook-research
version: 1.0.0
description: |
  Download the top 5 best-performing reels from a scraped Facebook page,
  transcribe them with Whisper, analyze the transcripts for structural
  patterns, and generate a reusable video template based on the best
  performer so the user can replicate or exceed its results.
---

# facebook-research-template — Video Template Extraction

Full pipeline: Download → Transcribe → Analyze → Template → Update REPORT.html

## Prerequisites

- `openai-whisper` installed (`pip install openai-whisper`)
- `ffmpeg` installed
- Chrome logged into Facebook (needed to access video pages)
- Previous states completed (scrape + analyze must have run)

## Pipeline Steps

### Step 1: Download Top 5 Reels

```bash
node .fb-research/scripts/download-reels.js <project-name>
```

The script navigates to each of the top 5 posts (from `page-analytics.json` top5), extracts
the `<video>` src, and downloads to `video-template/downloads/post-N.mp4`. If `src` is a
blob URL or download fails, fall back to Chrome DevTools manual capture of the network
request that serves the video.

### Step 2: Transcribe with Whisper

```bash
bash .fb-research/scripts/transcribe.sh <project-name>
```

Processes every file in `video-template/downloads/` with Whisper `base` model (Spanish) and
writes `.txt` + `.srt` to `video-template/transcripts/`. Skips already-transcribed files.
Adjust `--model` in the script for speed (`tiny`) or accuracy (`large`).

### Step 3: Analyze Transcripts

For each of the 5 transcripts, extract:

1. **Hook (0-5s)**: Exact wording, timing, tone
2. **Context (5-15s)**: How the situation is established
3. **Body/Drama (15-40s)**: The narrative arc, key moments
4. **CTA (40-50s)**: Call to action format
5. **Pacing**: Sentence length distribution, questions per video, emphasis patterns
6. **Vocabulary**: Power words, repeated phrases, emotional triggers
7. **Emotional arc**: How the video makes the viewer feel moment-by-moment

Compare all 5 to find:
- What the best performer (#1) does differently
- Common patterns across all top performers
- What the worst performer (#5) is missing

### Step 4: Generate Reusable Template

Create a fill-in-the-blank template based on the #1 post's structure.

The template includes:
- Exact hook formula with slots: `¡[STAR NAME] + [DRAMATIC VERB] + [TEAM]! [EMOJI]`
- Scene-by-scene structure with timing
- Vocabulary list (power words that work)
- CTA formula
- Production specs (duration, text style, audio)

### Step 5: Update REPORT.html

Add a new section "🎬 Video Template" to REPORT.html showing:
- The reusable template
- The best performer breakdown
- Comparison table of all 5 transcripts

## Output Files

| File | Description |
|------|-------------|
| `video-template/downloads/post-1.mp4` through `post-5.mp4` | Downloaded reels |
| `video-template/transcripts/post-1.txt` through `post-5.txt` | Whisper transcriptions |
| `video-template/transcripts/post-1.srt` through `post-5.srt` | Whisper subtitles with timestamps |
| `video-template/transcript-analysis.json` | Structured analysis of all 5 transcripts |
| `video-template/VIDEO-TEMPLATE.md` | Reusable fill-in-the-blank video template |
| `video-template/best-performer-breakdown.md` | Deep analysis of the winner |

## Video Template Format

```markdown
# Video Template: [Pattern Name]

**Based on**: [Post Title] — [views] views · [engagement] engagement
**Pattern**: [star+drama / upset-alert / curiosity-gap]

## 1. Hook Formula (0:00-0:03)

¡[STAR_NAME] [DRAMATIC_VERB] [TEAM/COUNTRY]! [EMOJI]

**Power words that work**:
- SALVA, ELIMINA, ROMPE, DESTROZA, HACE MAGIA
- INCREÍBLE, IMPOSIBLE, NADIE LO ESPERABA
- POLÉMICA, ROBO, INJUSTICIA, SOPRESA

## 2. Scene Structure

| Time | Section | Content | Emotion |
|------|---------|---------|---------|
| 0:00-0:03 | Hook | Bold text overlay + dramatic audio | Shock/Curiosity |
| 0:03-0:10 | Context | "Team was [situation]. But then..." | Tension |
| 0:10-0:30 | Drama | Key moment + reaction + analysis | Peak emotion |
| 0:30-0:45 | Opinion | "The real story is..." → controversial take | Debate |
| 0:45-0:50 | CTA | Question + subscribe prompt | Engagement |

## 3. Narrative Arc

1. **Pattern interrupt** (0s): Bold claim that stops scroll
2. **Context hook** (3s): "Everyone thought X, but Y happened"
3. **Escalation** (10s): Building the drama step by step
4. **Climax** (25s): The key moment described vividly
5. **Resolution** (35s): Your hot take/analysis
6. **Engagement bait** (45s): Question that splits the audience

## 4. Caption Formula

¡[HOOK]! [EMOJI]

[2-3 sentences: context + drama + opinion]

[CONTROVERSIAL QUESTION]
¿Crees que...? ¡Te leo en los comentarios! 👇

[hashtags: 2 viral + 2 niche + 1 branded]

## 5. Production Specs

- Duration: 45-50 seconds
- Text overlay: Bold upper-case, white with black stroke
- Audio: Match commentary + cinematic background music
- Captions: Styled (bold_outline or modern_glow)
- Transitions: Fast cuts (1-2 second clips)
- Color: High contrast, warm tones for excitement

## 6. Fill-in-the-Blanks Template

Copy this for each new video:

```
Hook: ¡[____] [____] [____]! [emoji]
Context: [Team] estaba [situation]. Pero entonces...
Drama: [Key moment] significó [impact] para [team].
Opinion: Lo que nadie dice es [controversial take].
CTA: ¿Crees que [debate question]? ¡Te leo! 👇
```
```

## Notes

- If download fails (Facebook blocks), generate the template from the available metadata + analysis data
- Whisper model can be adjusted: `tiny` (fast) to `large` (accurate)
- For Spanish content, `base` model works well; use `large` for accented speech
