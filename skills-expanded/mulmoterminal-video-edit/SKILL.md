---
name: mulmoterminal-video-edit
description: Edit a video by talking about it — cut out a part, join clips, change the speed, even out or replace the sound, make it vertical — and add subtitles made from what is said in it, or captions and titles placed on screen (telops). Uses ffmpeg in the terminal and whisper.cpp for the speech, writes a new file beside the original, and opens the result in the pane on the right of the terminal (showInPane). Use when the user asks to trim, cut, join, speed up, resize, subtitle, caption, translate the subtitles of, or put text on a video. The user writes no commands. Works in whatever language the user writes in.
---

# Edit a video

The user points at a video and says what they want in plain words. They do not write ffmpeg
commands; you do, in the terminal, and show them the result. Talk to them about their video —
the part from 0:12 to 0:40, the subtitles, the title at the start — not about codecs and filters,
unless they ask.

## What you need

- `ffmpeg` and `ffprobe`. Check with `ffmpeg -version`. If it is missing, say so and give the
  install command (`brew install ffmpeg` on a Mac); do not install it yourself.
- For subtitles or captions drawn onto the picture, ffmpeg built with libass. Check:
  `ffmpeg -hide_banner -filters | grep -E ' (subtitles|ass) '` prints two lines when it is.
- For subtitles made from speech, `whisper-cli` from whisper.cpp (`brew install whisper-cpp` on a
  Mac; the same package MulmoTerminal's voice input uses) and a model. Look for one MulmoTerminal
  has already downloaded, in the workspace's `models` folder:

  ```sh
  ls "${CLAUDE_CWD:-$HOME/mulmoclaude}/models"/ggml-*.bin
  ```

  Use the file you find (prefer `ggml-large-v3-turbo.bin` when there are several) as `$model` below.
  If there is none, ask before downloading one, and say how big it is: `ggml-large-v3-turbo.bin`
  (about 1.6 GB, the most accurate) or `ggml-small.bin` (about 490 MB, faster, less accurate).
  Then put it in that folder, so voice input finds it too:

  ```sh
  models="${CLAUDE_CWD:-$HOME/mulmoclaude}/models" && mkdir -p "$models" &&
  curl -L -o "$models/ggml-large-v3-turbo.bin" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
  ```

  (`ggml-small.bin` the same way.) Then `$model` is the file you downloaded.

- `showInPane`, to open the result beside the terminal. In a project directory it exists only when
  **Canvas** was switched on before the session started. Without it, give the user the file's path.

The speech is transcribed on this machine. Never send the video or its sound anywhere.

## Rules for every edit

- **Never change the original.** Write a new file in the same folder, named after the original and
  the edit: `talk.mp4` → `talk-cut.mp4`, `talk-subtitled.mp4`. If that name is taken, add a number.
  When the original is outside your working directory, write the new file in your working
  directory instead, so it can be shown.
- Keep intermediate files in a working directory of their own (`work=$(mktemp -d)`), and give them
  plain names (`audio.wav`, `subs.srt`), which keeps the filter arguments below free of quoting.
- Encode the result so it plays everywhere, the pane included: H.264 video, AAC sound,
  `yuv420p`, and the index at the front of the file.

  ```sh
  ENC=(-c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart)
  ```

  This is `"${ENC[@]}"` below. Keep it an array and quoted that way: a plain string (`ENC="…"`)
  reaches ffmpeg as one argument in zsh, and the command fails. Re-encoding takes time — roughly the length of the video or longer on a
  laptop — so tell the user before a long one, and for a style they have not seen yet, make a
  short sample first (add `-t 20` for the first twenty seconds) and show that.

## 1. Look at the video first

```sh
ffprobe -v error -show_entries format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate,channels -of json "talk.mp4"
```

Tell the user its length, picture size, frame rate, and whether it has sound. Times in what they
ask for ("from the 12th second", "the last minute") are measured against this.

## 2. Cutting, joining and the rest

**A part** (accurate to the frame, by re-encoding):

```sh
ffmpeg -ss 00:00:12 -to 00:00:40 -i talk.mp4 "${ENC[@]}" talk-cut.mp4
```

`-c copy` instead of `"${ENC[@]}"` is instant but can only cut at a keyframe, so the start may be off by a
few seconds. Offer it only for a long video where that does not matter, and say so.

**Several parts kept, the rest dropped**: cut each part as above into the working directory, then
join them.

**Joining** clips made the same way (same size, frame rate and codecs, such as parts of one
video):

```sh
printf "file '%s'\n" part1.mp4 part2.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4
```

Clips from different sources first need the same size and frame rate; join them with the
`concat` filter instead, scaling each to the first one's size:

```sh
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v]scale=1280:720,setsar=1,fps=30[v0];[1:v]scale=1280:720,setsar=1,fps=30[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" "${ENC[@]}" joined.mp4
```

A clip with no sound has no `[n:a]`, and the join fails. Add silence as one more input, as long as
that clip, and use it in the clip's place: with `b.mp4` (4 s, silent) as input 1, add
`-f lavfi -t 4 -i anullsrc=r=48000:cl=stereo` as input 2 and write `[v1][2:a]` for it.

**Speed**: `-filter:v "setpts=PTS/1.5" -filter:a "atempo=1.5"` plays at 1.5×. `atempo` takes 0.5
to 2; chain it for more (`atempo=2,atempo=1.5` is 3×).

**Sound**: even out the loudness with `-af loudnorm=I=-16:TP=-1.5:LRA=11`; remove it with `-an`;
replace it with music, cut to the video's length:

```sh
ffmpeg -i talk.mp4 -i music.mp3 -map 0:v -map 1:a -shortest "${ENC[@]}" talk-music.mp4
```

Music under the speech instead: `-filter_complex "[1:a]volume=0.2[m];[0:a][m]amix=inputs=2:duration=first[a]" -map 0:v -map "[a]"`.

**Vertical (9:16) for a phone**, keeping the middle: `-vf "crop=ih*9/16:ih,scale=1080:1920"`.
Ask before cropping: it cuts off the sides.

**A still from the video**: `ffmpeg -ss 00:00:05 -i talk.mp4 -frames:v 1 talk-0005.png`.

## 3. Subtitles from what is said

1. Take the sound out as whisper wants it:

   ```sh
   ffmpeg -i talk.mp4 -ar 16000 -ac 1 -c:a pcm_s16le "$work/audio.wav"
   ```

2. Transcribe it with timings. `-l ja` for Japanese, `-l en` for English, `-l auto` when you do
   not know:

   ```sh
   whisper-cli -m "$model" -l ja -f "$work/audio.wav" -osrt -of "$work/raw"
   ```

   This writes `$work/raw.srt`.

3. **Read it and fix it** — this is where subtitles become good. Whisper mishears names and
   technical words, and splits lines where the breath falls rather than where the sense does.
   - Correct the words. If a name or a term is unclear, ask the user rather than guessing.
   - Keep every cue's timing; change only the text, or merge two cues into one and keep the first
     start and the last end.
   - At most two lines a cue; about 20 characters a line in Japanese, about 42 in English.
   - Drop cues that are only noise or filler ("えー", "um").
   - To translate, translate each cue in place and keep its timing.

4. Save the result **beside the video**, as `talk.srt` (or `talk.en.srt` for a translation), and
   open it with `showInPane`, so the user can read it and fix a word themselves before you put it on
   the picture.

## 4. Putting the subtitles on the video

**Drawn onto the picture** (burned in) — they show everywhere, the pane included, and cannot be
switched off. Run from the folder holding both files, so the filter argument needs no quoting:

```sh
cd "$work" && cp /path/to/talk.srt subs.srt &&
ffmpeg -i /path/to/talk.mp4 -vf "subtitles=subs.srt:force_style='FontName=Hiragino Sans,FontSize=20,Outline=2,MarginV=30'" "${ENC[@]}" /path/to/talk-subtitled.mp4
```

`FontName` must be a font this machine has: `fc-list :lang=ja family` lists those that can write
Japanese (Hiragino Sans on a Mac, Noto Sans CJK JP on Linux). A name that does not exist falls back
to another font silently, and Japanese then comes out as boxes.

**As a track that can be switched on and off** — fast, since the picture is not re-encoded, and
the viewer chooses. QuickTime, VLC and phones show it; **the pane on the right may not** (Chrome
does not show such a track), so say that, and show the `.srt` beside it instead:

```sh
ffmpeg -i talk.mp4 -i talk.srt -map 0 -map 1 -c copy -c:s mov_text -metadata:s:s:0 language=jpn talk-subtitled.mp4
```

## 5. Captions and titles on screen (telops)

For text that is placed, styled and timed — a title at the start, a name under a speaker, a
highlighted word — write an ASS file. Set `PlayResX` / `PlayResY` to the video's own size, so
positions and sizes are in its pixels:

```
[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Hiragino Sans,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,2,5,0,0,0,1
Style: Name,Hiragino Sans,48,&H00FFFFFF,&H00FFFFFF,&H60000000,&H00000000,1,0,0,0,100,100,0,0,3,12,0,7,60,0,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:00:04.00,Title,,0,0,0,,{\fad(300,300)}今日のテーマ
Dialogue: 0,0:00:05.00,0:00:10.00,Name,,0,0,0,,{\fad(200,200)}山田 太郎 / 開発
```

- Colours are `&HAABBGGRR`: alpha first (00 opaque), then blue, green, red. `&H0000FFFF` is yellow.
- `Alignment` is the numpad: 1 bottom-left, 2 bottom-centre, 5 centre, 7 top-left, 8 top-centre.
- `BorderStyle` 1 is an outline (`Outline` its width, `OutlineColour` its colour); 3 is a box behind
  the text, whose colour is `OutlineColour` and whose padding is `Outline`. `BackColour` is the shadow.
- Keep telops out of the subtitles' way: subtitles sit at the bottom centre, so the sample puts a
  name at the top left (`Alignment` 7).
- In the text, `{\fad(in,out)}` fades in and out (milliseconds), `{\pos(x,y)}` places it exactly,
  `{\c&H0000FFFF&}` colours what follows, `\N` breaks the line.

Draw it onto the picture the same way, from the working directory:

```sh
ffmpeg -i /path/to/talk.mp4 -vf "ass=telop.ass" "${ENC[@]}" /path/to/talk-telop.mp4
```

Subtitles and telops together, in one pass: `-vf "subtitles=subs.srt:force_style='…',ass=telop.ass"`.
Save `telop.ass` beside the video too (`talk.ass`), so the user can change a word and ask you to draw
it again.

Make a short sample with `-t` around the first telop and show it before rendering the whole video:
font, size and position are what the user will want to change.

## 6. Show it and say where everything is

Open the result with `showInPane` (a path relative to your working directory). Then tell the user:

- the new video's path, and that the original is unchanged;
- the subtitle and telop files beside it (`.srt`, `.ass`), which they can edit — after an edit, ask
  you to draw them on again;
- for a track that can be switched on and off, that the pane may not show it but players do.

## Do not

- Do not overwrite or delete the original, or any file you did not create.
- Do not upload the video or its sound anywhere, and do not use an online transcription service.
- Do not install software or download a model without asking.
- Do not guess a time the user did not give: ask, or show a still (`-frames:v 1`) and let them say.
