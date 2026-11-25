---
name: rgaa-multimedia
description: "Audit a web page for RGAA v4.1.2 Theme 4 – Multimedia accessibility compliance. Checks pre-recorded media for transcriptions, subtitles, audio descriptions, identification, alternatives for non-temporal media, auto-play sound control, keyboard controls, and assistive technology compatibility. Use this skill when someone asks to check video/audio/media accessibility, verify RGAA Theme 4, or audit multimedia compliance on a website."
---

# RGAA Multimedia Accessibility Audit (Theme 4)

Audits a web page against the 13 criteria of RGAA v4.1.2 Theme 4: Multimedia.

## Audit procedure

### Step 1: Gather multimedia data

```javascript
(() => {
  const media = { videos: [], audios: [], objects: [], embeds: [], iframes: [] };

  document.querySelectorAll('video').forEach(el => {
    const tracks = Array.from(el.querySelectorAll('track')).map(t => ({
      kind: t.kind, srclang: t.srclang, label: t.label, src: t.src?.substring(0, 100)
    }));
    media.videos.push({
      src: el.src?.substring(0, 100) || el.querySelector('source')?.src?.substring(0, 100),
      controls: el.controls,
      autoplay: el.autoplay,
      muted: el.muted,
      tracks: tracks,
      ariaLabel: el.getAttribute('aria-label'),
      title: el.getAttribute('title'),
      hasTranscriptLink: !!el.parentElement?.querySelector('a[href*="transcript"], a[href*="transcription"]')
    });
  });

  document.querySelectorAll('audio').forEach(el => {
    media.audios.push({
      src: el.src?.substring(0, 100) || el.querySelector('source')?.src?.substring(0, 100),
      controls: el.controls,
      autoplay: el.autoplay,
      ariaLabel: el.getAttribute('aria-label'),
      title: el.getAttribute('title')
    });
  });

  // Embedded media (YouTube, Vimeo, etc.)
  document.querySelectorAll('iframe').forEach(el => {
    const src = el.src || '';
    if (src.match(/youtube|vimeo|dailymotion|soundcloud|spotify/i)) {
      media.iframes.push({
        src: src.substring(0, 150),
        title: el.getAttribute('title'),
        ariaLabel: el.getAttribute('aria-label')
      });
    }
  });

  document.querySelectorAll('object[type^="video"], object[type^="audio"], embed[type^="video"], embed[type^="audio"]').forEach(el => {
    media.objects.push({
      tag: el.tagName.toLowerCase(),
      type: el.type,
      ariaLabel: el.getAttribute('aria-label')
    });
  });

  return JSON.stringify(media, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 4.1** – Pre-recorded temporal media has a text transcription (if needed).
Check that videos and audio have a nearby transcription or link to one.

**Criterion 4.2** – Transcription is relevant.
If a transcription exists, it should accurately represent the content.

**Criterion 4.3** – Pre-recorded synchronized media has subtitles.
Check `<track kind="subtitles">` or `<track kind="captions">` on video elements.

**Criterion 4.4** – Subtitles are relevant.
Subtitles must be synchronized and accurately represent dialogue and important sounds.

**Criterion 4.5** – Pre-recorded media has audio description (if needed).
Check for `<track kind="descriptions">` or an alternative audio-described version.

**Criterion 4.6** – Audio description is relevant.
Must accurately describe important visual elements.

**Criterion 4.7** – Temporal media is clearly identified.
Media must have a title or label identifying its content.

**Criterion 4.8** – Non-temporal media has an alternative.
SVG animations, canvas animations, etc., must have text alternatives.

**Criterion 4.9** – Non-temporal media alternative is relevant.

**Criterion 4.10** – Auto-playing sound is controllable.
Any sound playing automatically must have a mechanism to stop/pause or control volume, accessible within the first 3 elements of the page.

**Criterion 4.11** – Temporal media is controllable by keyboard.
Play, pause, volume, subtitles toggle, audio description toggle must be keyboard-accessible.

**Criterion 4.12** – Non-temporal media is keyboard-controllable.

**Criterion 4.13** – Media is compatible with assistive technologies.
Media player controls must have accessible names and roles.

### Step 3: Generate report

For each media element found, evaluate all applicable criteria. Many criteria (relevance of transcription, audio description content) require human review — flag these as requiring manual verification.
