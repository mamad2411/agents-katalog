---
name: explainer-video
description: Make narrated, animated explainer videos. Use when the user wants an explainer, tutorial, demo, promo or executive-overview video, or a new version of one.
---

# Explainer video

Scenes are HTML pages whose `render(t)` is a pure function of time. Headless Chromium screenshots each frame, and ffmpeg joins the frames, narration and music. Work in a copy of `templates/` in a fresh project directory (the scratchpad unless the user names one), and run `npm install` there, as in every copied version. Gotchas for each step are in [REFERENCE.md](REFERENCE.md).

Leading words:
- **sourced:** every claim traces to a line in the product's docs or code.
- **word-synced:** each element appears on the word that names it, or up to 0.3 s early.
- **real output:** terminal text is captured from real runs.
- **new version:** a change is a copy, `vN` → `vN+1`, and earlier versions stay.

## Steps

1. **Ground.** Read the source of truth: README, guide, site pages and code. List the claims the video will make. *Done when* every planned claim has its file:line, and the user has picked the audience (engineers, executives, new users, public).
2. **Research the audience** with the `research` skill, unless a note in REFERENCE.md's "Research to reuse" covers it. *Done when* the note ends in checkable rules and a beat outline.
3. **Script** `narration.json`. Use one scene per idea, written conversationally, and speak every on-screen label. Overclaiming hides in "never", "only" and "free", in a bare "the" over a set ("the skills are adapted…" when most are), in a passive that hides who gave a permission ("allowed to add it" rather than "its owner allowed it to add it"), and in speed or productivity numbers. A proof point is a real, dated artifact the viewer can open, such as an issue and its PR: name each by its title rather than its number, and give times in the viewer's time zone. *Done when* every sentence is **sourced** and the word count at 140 wpm fits the audience.
4. **Voice.** Generate per-scene audio with timestamps using `tts.py`, with `ELEVENLABS_API_KEY` in the environment. On a new project, audition voices with the user. Then run `gen_cues.py` to get `cues/NN.js` and `plan.json`. *Done when* every scene has audio, cues and a planned length.
5. **Harness.** Write `storyboard.md`: the rules plus a direction for each scene. Adapt `style.css` and `lib.js` to the look, and set `window.BRAND` for the corner wordmark. *Done when* each direction gives its cue words in the order they are spoken, checked against `cues/NN.js`, and a still of a throwaway scene shows the loaded fonts and the wordmark, with an element landing on its cue word.
6. **Build scenes** with background subagents, one per scene, or one per group of scenes that share a continuous diagram. Give each the storyboard and its cues, and have it check its stills with Read before rendering video. *Done when* every `out/NN.mp4` matches `plan.json` within 0.05 s.
7. **Review.** An independent subagent that hasn't seen the code judges stills of every scene against the source, including one in each scene's final hold, after its last cue. It names any factual errors and at most one scene to fix. Check one frame of each new scene yourself as well. *Done when* the flagged fixes are made and every claim still holds against its source.
8. **Assemble** with `build.py`. It joins the scenes, places narration at each scene's lead, keeps music to the unnarrated head and tail, normalises loudness, and writes a WebVTT caption file and a player page. Make a poster from the strongest frame. *Done when* loudness reads −16 ±1 LUFS and the player loads its captions over http.
9. **Present** the video in a served index page: one card per video, newest version first, captions off by default. Add the card to an existing index page in place, since other sessions may be editing it. Open it in the user's browser. *Done when* the page is open and you've told the user what was checked and what wasn't. Review used stills, so no one has yet watched the video end to end with sound.

For a change to a finished video, make a **new version**: copy the project directory, change only what was asked, re-voice only the changed lines, and re-render the scenes whose cues or counters changed.
