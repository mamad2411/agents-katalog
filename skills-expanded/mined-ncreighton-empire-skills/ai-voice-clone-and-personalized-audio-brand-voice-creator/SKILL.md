---
name: ai-voice-clone-and-personalized-audio-brand-voice-creator
description: "Create custom AI voice clones from audio samples, then generate branded audio content for YouTube, podcasts, audiobooks, and IVR systems. Use when the user needs voice cloning, audio branding, podcast production, or narration automation."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": [
          "ELEVENLABS_API_KEY",
          "GOOGLE_CLOUD_SPEECH_API_KEY",
          "AWS_ACCESS_KEY_ID",
          "AWS_SECRET_ACCESS_KEY"
        ],
        "bins": ["ffmpeg", "sox"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎙️"
    }
  }
---

## Overview

The AI Voice Clone and Personalized Audio Brand Voice Creator is a comprehensive audio production automation skill that transforms raw voice samples into a professional, reusable AI voice clone. This skill empowers content creators, podcasters, audiobook authors, and enterprises to maintain consistent brand voice across all audio touchpoints—from YouTube intros and podcast bumpers to customer IVR systems and audiobook narration.

**Why This Matters:**
- **Consistency**: Maintain identical emotional tone, accent, and speaking patterns across 100+ audio pieces
- **Scalability**: Generate hours of branded audio in minutes instead of weeks of studio recording
- **Cost Efficiency**: Eliminate expensive voice talent sessions while maintaining professional quality
- **Compliance**: Automatic licensing tracking and usage rights documentation for commercial distribution
- **Integration Ready**: Seamless connections to WordPress audio plugins, Slack notifications, Google Drive, YouTube automation, and podcast management platforms like Anchor and Podbean

**Primary Use Cases:**
1. YouTube creators building consistent intro/outro sequences
2. Podcast networks maintaining brand voice across multiple shows
3. Audiobook publishers automating narration for multiple titles
4. Enterprise IVR systems with branded customer service voice
5. E-learning platforms with consistent course narration

---

## Quick Start

### Example 1: Clone Your Voice from Sample Audio
```
Create an AI voice clone for me using these audio samples:
- Sample 1: 3-minute intro read (natural, conversational tone)
- Sample 2: 2-minute product description (professional, energetic)
- Sample 3: 2-minute storytelling excerpt (warm, engaging)

Voice profile name: "BrandVoice_2024"
Accent: American English (neutral)
Age range: 30-40
Emotion baseline: Friendly, professional
```

### Example 2: Generate YouTube Intro Sequence
```
Generate 5 unique YouTube intro variations using my cloned voice:
1. Tech review opener (energetic, 15 seconds)
2. Tutorial intro (clear, instructional, 10 seconds)
3. Vlog opener (casual, friendly, 12 seconds)
4. Announcement intro (authoritative, 8 seconds)
5. Collab intro (enthusiastic, 10 seconds)

Include background music bed (royalty-free, upbeat)
Format: MP3 (320kbps) and WAV (48kHz)
Export with auto-normalized levels
```

### Example 3: Batch Generate Podcast Bumpers
```
Create 10 podcast bumper variations from my voice clone:
- 3x episode intro bumpers (5 seconds each)
- 3x mid-roll transition bumpers (3 seconds each)
- 2x outro/call-to-action bumpers (4 seconds each)
- 2x sponsor read bumpers (6 seconds each)

Tone: Conversational, energetic
Include: [SHOW_NAME], [EPISODE_NUMBER], [GUEST_NAME] variable placeholders
Output: MP3, AAC, and OGG formats
Add: Fade in/out, compression, EQ preset for podcast distribution
```

---

## Capabilities

### Voice Cloning & Analysis
- **Multi-Sample Processing**: Accepts 10-15 minutes of reference audio (MP3, WAV, M4A, FLAC)
- **Emotional Tone Extraction**: Analyzes pitch, pace, prosody, and emotional undertones
- **Accent & Dialect Preservation**: Maintains regional accent characteristics, speech patterns, and unique vocal quirks
- **Voice Profile Creation**: Generates reusable voice model with 95%+ similarity to original speaker
- **Quality Verification**: Automated comparison testing between original and cloned voice samples

### Audio Content Generation
- **Template Library**: 50+ pre-built templates for YouTube intros, podcast bumpers, audiobook chapters, IVR scripts, e-learning modules
- **Variable Substitution**: Dynamic text insertion for names, numbers, dates, product names
- **Emotion Control**: Fine-tune emotional delivery (0-100 scale): neutral, happy, sad, angry, excited, professional, casual
- **Pacing Options**: Slow (0.8x), normal (1.0x), fast (1.2x), ultra-fast (1.5x)
- **Batch Generation**: Create 50+ variations in a single request with different parameters

### Audio Enhancement & Formatting
- **Noise Reduction**: Remove background hum, room noise, wind noise from cloned voice
- **EQ Presets**: Industry-standard profiles (podcast, audiobook, YouTube, IVR, voice-over)
- **Compression & Normalization**: Professional loudness matching (LUFS standards)
- **Background Music Integration**: Add royalty-free music beds, fade in/out transitions
- **Multi-Format Export**: MP3, WAV, AAC, OGG, FLAC, M4A with custom bitrate settings

### Licensing & Compliance
- **Usage Rights Tracking**: Automatic documentation of commercial vs. personal use rights
- **Export Metadata**: Embed licensing information in audio file metadata
- **Compliance Reports**: Generate usage reports for commercial distribution, monetization, or licensing agreements
- **Archive Management**: Version control and backup of all voice clones and generated content

---

## Configuration

### Required Environment Variables
```bash
# ElevenLabs API (primary voice synthesis engine)
export ELEVENLABS_API_KEY="your_elevenlabs_api_key"

# Google Cloud Speech-to-Text (voice analysis and verification)
export GOOGLE_CLOUD_SPEECH_API_KEY="your_google_cloud_api_key"

# AWS Polly (backup synthesis and voice comparison)
export AWS_ACCESS_KEY_ID="your_aws_access_key"
export AWS_SECRET_ACCESS_KEY="your_aws_secret_key"

# Optional: Slack notifications for batch job completion
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Installation & Setup
```bash
# Install required audio processing tools
brew install ffmpeg sox  # macOS
sudo apt-get install ffmpeg sox  # Linux
choco install ffmpeg sox  # Windows (with Chocolatey)

# Verify installations
ffmpeg -version
sox --version
```

### Configuration Options
```yaml
voice_clone_settings:
  sample_duration_min: 10  # minimum minutes of reference audio
  sample_duration_max: 15  # recommended maximum
  quality_threshold: 0.92  # minimum similarity score (0-1)
  supported_formats: ["mp3", "wav", "m4a", "flac", "ogg"]

generation_settings:
  max_batch_size: 50  # maximum items per generation request
  default_bitrate: "320k"  # MP3 bitrate
  default_sample_rate: 48000  # Hz (48kHz for professional audio)
  emotion_scale: [0, 100]  # fine-grained emotion control
  pacing_range: [0.8, 1.5]  # speed multiplier

export_settings:
  formats: ["mp3", "wav", "aac", "ogg", "flac", "m4a"]
  loudness_target_lufs: -14  # podcast standard
  include_metadata: true
  auto_backup: true
```

---

## Example Outputs

### Voice Clone Quality Report
```
VOICE CLONE ANALYSIS REPORT
==========================

Profile Name: BrandVoice_2024
Creation Date: 2024-01-15
Reference Audio: 14 minutes, 32 seconds
Status: ✅ APPROVED (Quality Score: 0.96/1.0)

Vocal Characteristics:
- Pitch Range: 85Hz - 240Hz (male, baritone)
- Speaking Rate: 142 words/minute (slightly above average)
- Accent: American English (neutral Midwest)
- Emotional Baseline: Friendly, professional
- Unique Markers: Slight pause before emphasis, warm resonance in lower frequencies

Similarity Metrics:
- Pitch Accuracy: 97%
- Prosody Match: 94%
- Tone Color Match: 95%
- Overall Similarity: 96%

Recommended Use Cases:
✓ YouTube content (intro/outro)
✓ Podcast production (bumpers, intros)
✓ Audiobook narration (fiction/non-fiction)
✓ Corporate IVR systems
✓ E-learning narration

Licensing Status: Commercial Use Approved
```

### Generated YouTube Intro Sequence
```
FILE: youtube_intro_tech_review_v1.mp3
Duration: 15 seconds
Loudness: -14 LUFS (podcast standard)
Bitrate: 320kbps
Format: MP3 (stereo, 48kHz)

Transcript:
"Hey everyone, welcome back to the channel! Today we're diving deep into 
the latest tech that's about to change everything. Stick around!"

Emotional Delivery: Energetic, excited
Pacing: 1.1x (slightly faster than normal)
Background Music: Upbeat electronic bed (fade in 0-2s, fade out 13-15s)
Processing: Noise reduction, compression, EQ preset: YouTube_Optimized
```

### Podcast Bumper Batch (10 Items)
```
BATCH GENERATION COMPLETE: podcast_bumpers_jan2024
Total Items: 10
Total Duration: 3 minutes, 42 seconds
Processing Time: 2 minutes, 15 seconds
Status: ✅ ALL SUCCESSFUL

Generated Files:
1. intro_bumper_episode_47.mp3 (5s) - [SHOW_NAME] Episode [EPISODE_NUMBER]
2. intro_bumper_episode_48.mp3 (5s) - with guest intro
3. intro_bumper_episode_49.mp3 (5s) - seasonal variant
4. midroll_transition_v1.mp3 (3s) - smooth transition
5. midroll_transition_v2.mp3 (3s) - energetic variant
6. outro_cta_patreon.mp3 (4s) - call-to-action bumper
7. outro_cta_newsletter.mp3 (4s) - newsletter signup
8. sponsor_read_audible.mp3 (6s) - natural read
9. sponsor_read_skillshare.mp3 (6s) - enthusiastic variant
10. channel_promo.mp3 (4s) - cross-promotion

Export Formats: MP3 (320kbps), AAC (256kbps), OGG (192kbps)
Total File Size: 47 MB
Metadata Embedded: ✓ Yes
Licensing Documentation: ✓ Included
```

---

## Tips & Best Practices

### Preparing Reference Audio Samples
1. **Quality Matters**: Use clean, well-recorded audio (minimal background noise, consistent volume)
2. **Variety is Key**: Include different emotional tones, speaking styles, and pacing in your samples
3. **Natural Reading**: Record yourself reading naturally—avoid over-dramatization or artificial delivery
4. **Consistent Recording**: Use the same microphone and recording environment for all samples
5. **Length Sweet Spot**: 10-15 minutes is optimal; more data doesn't always improve quality

### Optimizing Generated Content
1. **Batch Processing**: Group similar requests together for consistent emotional tone and pacing
2. **Template Matching**: Use pre-built templates for your industry (podcasting, YouTube, e-learning)
3. **Emotion Fine-Tuning**: Start with preset emotions, then adjust ±10 points for nuance
4. **Format Selection**: Use MP3 for web/social, WAV for professional production, AAC for Apple platforms
5. **Loudness Standards**: Match LUFS targets to your distribution platform (-16 for YouTube, -14 for podcasts)

### Maximizing Brand Consistency
1. **Create a Voice Guide**: Document your clone's optimal settings, emotion ranges, and pacing preferences
2. **Version Control**: Keep clones organized by date and iteration (v1.0, v1.1, etc.)
3. **Regular Audits**: Compare generated content quarterly to original voice for drift detection
4. **Backup Strategy**: Export and archive master voice clones to cloud storage (Google Drive, Dropbox)
5. **Integration Automation**: Connect to WordPress, Zapier, or Make for automatic audio generation on new blog posts

### Platform-Specific Optimization
- **YouTube**: Use upbeat pacing (1.1-1.2x), add music beds, target -16 LUFS loudness
- **Podcasts**: Natural pacing (1.0x), clear articulation, -14 LUFS loudness standard
- **Audiobooks**: Slower pacing (0.9x), emotional nuance, -18 LUFS for dynamic range
- **IVR Systems**: Clear, professional delivery, 1.0x pacing, high clarity EQ preset
- **E-Learning**: Friendly, encouraging tone, 1.0-1.05x pacing, educational EQ profile

---

## Safety & Guardrails

### What This Skill Will NOT Do
- **Create Impersonation Content**: Will not clone voices for deceptive impersonation, fraud, or identity theft
- **Generate Political Deepfakes**: Refuses to create synthetic audio of real political figures for misleading content
- **Bypass Consent Requirements**: Requires explicit proof of consent from original voice provider before cloning
- **Enable Copyright Violation**: Will not generate content that infringes on existing copyrighted audio or voice talent rights
- **Produce Harmful Synthetic Speech**: Refuses requests for hate speech, harassment, threats, or abusive content
- **Violate Commercial Rights**: Will not create clones for commercial use without proper licensing agreements

### Built-In Safeguards
1. **Consent Verification**: Requires signed consent form or explicit confirmation that you own the voice rights
2. **Watermarking**: Optional invisible watermark embedded in generated audio for authenticity verification
3. **Usage Logging**: All clone creation and generation requests logged with timestamps and metadata
4. **Commercial Licensing Tracking**: Automatic documentation of use rights (personal, commercial, monetized)
5. **Content Filtering**: Automatic rejection of scripts containing hate speech, harassment, or harmful content
6. **Similarity Thresholds**: Will not proceed with cloning if similarity to protected voices is detected

### Ethical Considerations
- Always disclose when audio is AI-generated in video descriptions, podcast show notes, or audiobook metadata
- Maintain proper licensing agreements for commercial use and monetization
- Keep voice clone credentials secure; treat like passwords
- Regularly audit generated content for quality drift or unintended artifacts
- Respect voice talent and original creators; use this for your own voice, not others'

---

## Troubleshooting

### Common Issues & Solutions

**Q: "Voice clone quality score is too low (below 0.90). What should I do?"**
A: Your reference audio likely has background noise or inconsistent volume. Solution: 
- Re-record samples in a quiet environment
- Ensure consistent speaking volume across all samples
- Include more variety in emotional tone and pacing
- Aim for 14-15 minutes of reference audio (longer is better)
- Check that all samples are clear, professional quality (no phone recordings)

**Q: "Generated audio sounds robotic or unnatural."**
A: The voice clone is correct, but generation settings need adjustment. Solution:
- Reduce pacing to 0.95-1.0x (slower sounds more natural)
- Increase emotion intensity (currently too neutral)
- Add micro-pauses in the script before emphasis words
- Try the "natural speech" EQ preset instead of default
- Reduce batch size if generating 50+ items (quality degrades with volume)

**Q: "Export file size is too large for my platform (YouTube, podcast host)."**
A: Your bitrate setting is too high. Solution:
- Use MP3 at 192kbps for web/social (not 320kbps)
- Use AAC at 128kbps for mobile and streaming platforms
- Enable compression in export settings
- For podcasts, 128kbps MP3 is industry standard and sufficient quality