---
name: open-video-harness
description: Make videos with code (video-as-code / code2video) through the OpenVideoHarness workbench. Covers 3Blue1Brown-style math and science explainers, knowledge shorts (vertical or horizontal; 抖音, B站, 小红书, Shorts), product launch films and promos, lyric videos and music videos, data stories, paper explainers, hand-drawn or watercolour shorts, meme or fast-cut edits, long landscape explainers, recaps from the user's own photos and clips (weddings, trips, a year; 照片回顾), and cutting the user's own footage (talking heads, interviews, vlogs; 剪口播). Also covers voiceover (Chinese or English), bilingual captions, code-composed music, sound effects, and reverse-engineering a reference video. Use it whenever the user asks to make, animate, render, remake or cut a video, 做视频, 做动画, 做科普视频, 做宣传片, 做 MV, 讲解视频, 片头, 剪用户自己录的素材, or 剪口播, even if they don't name the harness.
---

# OpenVideoHarness

Harness path (set by install.sh): ~/OpenVideoHarness

This skill is a thin pointer. All workflows, rules and tools live in the OpenVideoHarness repository.

## 1. Locate the harness

Sent here by the stub `bin/vh install-skill` writes? Then you have found it already: it is the clone this file is in.
Otherwise use the first of these that exists and contains `bin/vh`:

1. `$OVH_DIR`
2. the path on the "Harness path" line above
3. `~/OpenVideoHarness`
4. the current working directory

If none exists, ask the user for permission, then install it:

```bash
curl -fsSL https://raw.githubusercontent.com/ZLHad/OpenVideoHarness/main/install.sh | bash
```

Read the installer's last lines, not its exit status: it exits 0 whenever the install itself worked, and its last lines
say whether a first film can be made here ("✗ Not ready for a first film yet" lists what is missing, each with how to
get it). Tell the user what is missing before starting a film.

## 2. Follow the harness, not this file

Read `<harness>/CLAUDE.md` (Codex: `<harness>/AGENTS.md`, which is identical) and follow it:

- for an existing film or a resumed conversation, run `<harness>/bin/vh status <project>` first and use the reported next step, review record, and reading list;
- route the request to one of the 11 `video-types/` docs (09, editing the user's own footage, and 11, a recap of the user's own photos, are experimental);
- create the project with `<harness>/bin/vh new <type> <slug>`;
- stop for the user where CLAUDE.md says ("停在哪" and "导演模式"): a `standard` or `studio` film stops at the **concept** and the **first draft**, and at the **storyboard** too when the next step is expensive (a film longer than about 90 s, a heavy 3D render, paid calls); a short film's storyboard is shown on the draft's page. `quick` renders straight through. Say at the first stop where this film will stop; only the user's own words take a stop away. Anything the user said they want to decide themselves (hook, main character, theme music, title and cover …) adds a stop before anything downstream needs it, or rides on the next gate if it can wait. Each stop is one command, `bin/vh gate <project> <n>`: by default a local review page with at most three decisions; send the user the lines it prints, then wait;
- follow the hard rules: every frame is a pure function of t; picture, sound and text share one timing source (the narration's word times, the score's beats, or an event table); plan the shots and their reads before code; look at the real frames of what you made or changed; facts are copied from the source, never made up; no API key in a file;
- keep work inside `<harness>/projects/`; when the user names another directory, create the project there with `<harness>/bin/vh new <type> <slug> --dir <that directory>` (or set `OVH_PROJECTS`).

Audio tools:
- `bin/vh tts` — voiceover, Chinese or English, local Qwen3-TTS by default;
- `bin/vh captions` — zh/en/bilingual subtitles;
- `bin/vh music` — code-composed soundtrack;
- `bin/vh sfx` — sound effects;
- `bin/vh mix` and `bin/vh mux` — mixing and muxing.

When the user says "打开 Studio", "打开控制台" or "open Studio", run `<harness>/bin/vh studio` (with a project: `bin/vh studio <project>`): Studio's own window opens, or comes to the front when it is open already, also when you run it. Tell them what it printed. There is no address to pass on.

Run `bin/vh doctor` if anything looks missing, and before the first film in a host that only lets you write the workspace (a sandbox): its `caches` line names the download folders it cannot write and what to set, and its `skills` line says when the installed skill needs `bin/vh install-skill` again (a stub reads this file in the clone, so a `git pull` keeps it current; a whole copy does not).

## 3. When the user asks what this can do

Answer with a short menu in the user's language, not the routing table: the kinds of film, and a sentence that starts each. A request can be one line; the type's defaults fill in the rest.

| Film | A way to ask |
|---|---|
| Knowledge short, vertical or landscape | "做一支 60 秒的竖屏科普，讲飞机的窗户为什么是圆的" · "A 60-second vertical explainer on why plane windows are round" |
| Math, physics or algorithm explainer | "用 3b1b 的风格讲清楚傅里叶变换，两分钟" · "Explain the Fourier transform in two minutes, 3Blue1Brown style" |
| Product or launch film | "给这个 App 做一支 30 秒的发布片，官网是 …" · "A 30-second launch film for this app; the site is …" |
| Paper explainer | "把这篇论文讲成三分钟的视频：<PDF>" · "Turn this paper into a three-minute video: <PDF>" |
| Data story | "用这份 CSV 做一支数据故事" · "A data story from this CSV" |
| Lyric video or music video | "给这首歌做一支 MV：<音频>" · "A music video for this song: <audio>" |
| Hand-drawn short | "做一支水彩手绘的小短片，讲 …" · "A hand-drawn watercolour short about …" |
| Meme or fast cut | "做个 15 秒的快剪，科技推特那种风格" · "A 15-second fast cut, tech-Twitter style" |
| Long explainer, 10 minutes or more | "做一支 15 分钟的长片，把 … 讲透" · "A 15-minute film that explains … in full" |
| 3D scene or shader short | "把 … 做成一个能走进去的 3D 世界，一镜到底，60 秒" · "Build … as a 3D world, one unbroken move, 60 seconds" |
| Recap from the user's photos (experimental) | "用这个文件夹里的照片做一支旅行回顾" · "A trip recap from the photos in this folder" |
| Cutting the user's own footage (experimental) | "把这段口播剪掉口水词，加字幕，出竖屏" · "Cut the filler out of this talking head, add captions, export vertical" |
| How a reference video was made | "拆一下这支视频是怎么做的：<链接或文件>" · "Break down how this video was made: <link or file>" |

Then say that they choose how often to look, in one of three phrases: "直接出" (just make it: no stops), "看方向和初版" (the direction and the first draft), "每步都看" (every step). With nothing said, the agent stops at the concept and the first draft, and at the storyboard too when the film is long, heavy to render or paid.

## 4. Use what the host can show

The harness prints paths and chat lines because every agent can read those. When the host you run in can do more, use it; what a stop is and what goes on record stay the same.

- **Show the page and the film beside the chat.** If the host can display a local file next to the conversation (a side panel, a preview pane, a file card), open the stop's review page (`out/review/gate-<n>.html`), the contact sheet and the draft or final film there when you stop or deliver. Give the path as well.
- **Ask with the host's question tool.** If the host has a tool that asks the user a question with options (Claude Code's `AskUserQuestion`, for one), put the stop's decisions there: one question a decision, at most three, the options and the recommended one taken from the gate JSON, the recommended one first. What the user picks and any note they type are their words: copy them into `REVIEW.md` verbatim, as you would a chat reply.
- **Carry on in the same turn.** When the answer comes back, record it and go on to the next step at once. Do not end the turn to say that you will.
- **Resume a Studio review in Codex.** Publish with `bin/vh gate <project> <n> --desk` and tell the reviewer to return to the conversation after submitting. On return, run `bin/vh status`: notes nobody has taken yet are listed first, and `bin/vh desk wait <project>` hands them all over at once. Use `--wait` in hosts that wake the agent after the command completes.
- **No such tools** (a plain terminal, another agent): send the lines `bin/vh gate` prints and wait for the reply, as CLAUDE.md says.
