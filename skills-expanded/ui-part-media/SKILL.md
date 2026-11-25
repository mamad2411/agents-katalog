---
name: ui-part-media
description: "Video, audio and embeds: players with accessible controls, captions and transcripts, posters, autoplay rules, embeds that load lightly, aspect ratios, audio and podcast players, and galleries. Read before placing a video, an audio file or an embed."
---

# Video, audio and embeds

The naive page drops in a YouTube iframe that loads a megabyte of script
before anyone presses play, autoplays a video with sound, leaves a black box
that shifts the layout when it loads, has no captions, and wraps a custom
player in buttons with no names. This skill picks the right element, the
files, captions and transcripts, the autoplay rules, embeds that load only
when wanted, and players anyone can operate. Images and galleries are in
`ui-part-images`; product demos and background loops in `motion-demo`.

## 1. Choose the player

- Native `video` and `audio` with `controls`: keyboard operable, a captions
  menu, picture in picture and full screen, for free. The default.
- A custom player when the design needs one look across browsers or more
  features (chapters, quality, speed): Media Chrome (web components over the
  native element), Vidstack, Plyr or Video.js; never a hand-made `div` of
  icons.
- Long videos, many viewers or several qualities: a streaming service (Mux,
  Cloudflare Stream, Bunny Stream, or YouTube and Vimeo when their audience
  matters) with adaptive HLS; hls.js where the browser does not play HLS
  itself (`canPlayType("application/vnd.apple.mpegurl")` is empty).
- A short clip can be a self-hosted MP4 (H.264 and AAC plays everywhere),
  with a smaller WebM (VP9 or AV1) listed first for browsers that take it.

## 2. Size, poster, place

- Reserve the space: `width` and `height` attributes, or `aspect-ratio: 16 /
  9` on the element or its frame with `width: 100%`, so nothing moves when
  the metadata arrives.
- A poster that shows what the video is about (a real frame with the
  subject, not a black frame or a logo), at the video's ratio, compressed
  like any image.
- Vertical video (9:16) capped at about 80vh on wide screens instead of
  stretching to the column's width.
- Inside the text column on reading pages; wider (a breakout column) for
  the one video a page is built around.

## 3. Files and loading

- `preload="metadata"` for a video on the page (duration and first frame),
  `preload="none"` when there are several; `playsinline` so iPhones do not
  jump to full screen.
- Sources with their types, so the browser picks one without downloading
  the others:

```html
<video controls preload="metadata" playsinline width="1280" height="720"
       poster="/media/filter-poster.jpg">
  <source src="/media/filter.webm" type="video/webm">
  <source src="/media/filter.mp4" type="video/mp4">
  <track kind="captions" src="/media/filter.en.vtt" srclang="en" label="English">
  <a href="/media/filter.mp4">Download the video (MP4, 18 MB)</a>
</video>
```

- Many videos below the fold: set their sources when they come near the
  viewport (IntersectionObserver), not on page load.
- Downloads name the format and size in the link; the `download` attribute
  only works on the same origin.

## 4. Captions, transcripts, audio description

- Captions for every video with speech (WCAG 1.2.2, level A): WebVTT files
  in a `track` with language and label; speaker names and the sounds that
  matter; auto-generated captions checked by a person before publishing.

```
WEBVTT

00:00:00.000 --> 00:00:03.200
Switch the purifier off and unplug it.

00:00:03.200 --> 00:00:06.800
[click] The cover lifts from the left side.
```

- A transcript for audio (podcasts, voice notes: WCAG 1.2.1), on the page
  under the player, in a `details` when long, with speakers and timestamps
  that seek the player.
- Audio description when the pictures carry what the speech does not (a
  demo without narration, text shown on screen): a described version, or
  narration written to say what is shown (WCAG 1.2.5, AA).
- Tracks from another origin need CORS, and `crossorigin` on the media
  element. Style `::cue` lightly, so people's own caption settings still
  apply.

## 5. Autoplay

- With sound: never. Browsers block it anyway, and it startles people and
  drowns out screen readers.
- Muted autoplay only for short loops that show something (the product in
  use): `autoplay muted loop playsinline`, a visible Pause (WCAG 2.2.2, for
  anything moving longer than 5 seconds), paused when scrolled out of view,
  and not started at all under `prefers-reduced-motion` or the `Save-Data`
  hint: the poster with a Play button instead (`motion-demo`, section 8).
- Audio that starts by itself and lasts more than 3 seconds needs a way to
  stop it (WCAG 1.4.2).
- No play-on-hover previews on touch screens or under reduced motion.

## 6. Embeds that load lightly

- A facade first: the poster, the title and a real Play button; the iframe
  loads only when pressed. For YouTube, `lite-youtube-embed`
  (`<lite-youtube videoid="..." playlabel="Play: Replacing the filter">`),
  which uses the youtube-nocookie domain. The same idea for Vimeo (with
  `dnt=1`), maps (a static image of the map linking to it, the live map on
  press) and social posts (the post as a quote with a link, the widget
  script only on demand).
- Every iframe has a `title` naming its content ("Video: Replacing the
  filter", "Map: Jl. Kemang Raya 12"), `loading="lazy"` below the fold, a
  reserved aspect ratio, and only the `allow` features it needs.
- Privacy: an embed sets cookies and sends the visitor's address to its
  owner as soon as it loads. Where consent is required (the EU and UK), the
  facade is the consent point ("Playing sends data to YouTube") and
  nothing loads before the press. The CSP's `frame-src` lists the embed
  origins (`frontend-security`).

## 7. Audio and podcast players

- Native `audio controls` for a single clip. For episodes: play and pause,
  a seek bar with elapsed and total time, back 15 seconds and forward 15 or
  30, speed from 0.75 to 2x (remembered), chapters as links that seek, the
  transcript, and a download link with format and size ("MP3, 42 MB").
- The Media Session API (`navigator.mediaSession.metadata`, and handlers
  for play, pause, seekbackward and seekforward) puts the title, artwork
  and controls on the lock screen and on headphones.
- Remember where the listener stopped, per episode.
- Playback that continues across pages only in an app that does not reload
  between them; otherwise leaving the page stops it, and that is fine.

## 8. A custom player's controls and keys

- Every control is a `button` whose name follows its state ("Play" becomes
  "Pause"; "Mute", "Turn captions on", "Enter full screen"), 44px to the
  touch.
- The seek bar is an `input type="range"` (or `role="slider"`) with
  `aria-valuetext` in words ("1 minute 5 seconds of 4 minutes 30"); volume
  the same.
- Keys only while focus is inside the player, never across the page: Space
  or K plays and pauses, Left and Right seek 5 seconds, Up and Down change
  the volume, M mutes, F goes full screen, C toggles captions.
- Controls stay visible while paused, hovered or focused, and hide after 2
  to 3 seconds of playback without interaction.
- Controls sit on a dark gradient at the bottom of the frame so they read
  over any scene, in both themes; an audio player and transcripts take the
  page's tokens (`ui-themes`). Icons switch at once; nothing loops while
  paused (`motion-interface`).

## 9. Galleries

- Mixed galleries follow `ui-part-images` (the grid, a lightbox with arrow
  keys, Escape and a counter "3 of 12", swipe on touch).
- A video tile shows its duration and a play mark, and plays only when
  opened. No autoplaying carousels.

## 10. On a phone

- The main video spans the screen's width, controls at 44px, full screen
  through the native control.
- Audio controls in one row with the seek bar full width above them; speed
  and chapters in a menu.
- Mobile data costs money: nothing heavier than the poster loads before
  the press.

## Check it

- Keyboard only: reach the player, play, seek, turn captions on, move on;
  no trap inside an iframe.
- Captions show and match the speech; audio has its transcript.
- DevTools, Network: no YouTube, Vimeo or map requests before the facade
  is pressed; a video fetches only its metadata until played.
- Reduced motion on: nothing plays by itself; otherwise every loop has a
  visible Pause.
- `preview` at 360, 768 and 1440px: no shift where media loads, iframes
  titled, controls 44px.

## Avoid

Autoplay with sound; a background video with no Pause; iframes without a
title; the full YouTube embed on page load; embeds that set cookies before
consent; black posters; missing captions, or auto-captions nobody checked;
players built from unlabelled `div`s; page-wide shortcuts that steal Space;
media with no reserved space; vertical videos stretched past the screen.
