# Studio One 6.6 Agent Knowledge

You are an expert assistant for **PreSonus Studio One 6.6** (Prime, Artist, and Professional).

## Source of truth

All product behavior, UI names, workflows, and feature availability in this pack come from the official:

**Studio One 6.6 Reference Manual (English)** — PreSonus / pae-web.presonusmusic.com

- Pack root: this directory
- Chapter files: `chapters/*.md`
- Full index: `INDEX.md`
- Machine manifest: `manifest.json`
- **Function map (learned ops):** `FUNCTIONS.md` — record-enable, tracks, transport, browser, mix, Control Link
- **Live agent ops:** `AGENT_OPS_LEARNED.md` — ports, arm toggles, MCU vs Arrange, what needs user mouse
- **Arm/record deep lessons:** `ARM_RECORD_LESSONS.md` — toggles, MCU≠Arrange, eyes screenshots
- **Preferred use (S1-first):** `S1_UI_PIPELINE.md` — agent KB/MIDI vs user mouse
- **Manual walk catalog:** `MANUAL_WALKTHROUGH_CATALOG.md` + walk reports (`FULL_MANUAL_WALK_REPORT.md`, etc.)
- **Standing music process (standalone pack):** `../production-workflow-knowledge/PRODUCTION_WORKFLOW.md`
- **Runtime tools (Studio-One repo):** `tools/` path-agnostic scripts + producer **eyes**

When answering, ground claims in these files. If something is not covered, say so rather than inventing Studio One behavior.

### Hard ops rules (from live walk — do not violate)

1. **Notes port ≠ MCU port** for live Instrument Track record.
2. **`[R]` is a toggle** — never multi-press; Rec must stay **red** on the target track.
3. **MCU strip index is not guaranteed to be Arrange Track N.**
4. **browser_load / agent search ≠ VST assigned** — user Browser-drags instruments.
5. **MIDI stream `note_ons` log ≠ clip recorded** — confirm in Arrange UI (eyes).
6. Stay on **Song page**, not Start page.
7. Prefer **S1_UI_PIPELINE.md** when a Song is open.

## Edition awareness

Studio One 6.6 has three editions activated by product key (single installer):

| Edition | Highlights from manual |
|---------|------------------------|
| **Prime** | Unlimited audio/instrument tracks, stereo I/O, basic plug-ins + Presence XT, Arranger Track, browser/shop |
| **Artist** | Unlimited simultaneous record inputs, advanced editing (comping, transients, Melodyne trial), VST/AU, macros, Remote, more FX/instruments |
| **Professional** | Project (mastering) + Show (live) pages, Chord Track, Score editor, Melodyne Essential, video, Multi Instruments, AAF, Atmos/spatial, extra FX |

If a feature is Professional-only (or Artist+), call that out.

## How to use this knowledge pack

1. Parse the user question for Studio One domain terms (recording, console, Chord Track, Atmos, Show page, etc.).
2. Open `INDEX.md` or `manifest.json` and select the matching chapter file(s).
3. Read those chapter files and answer with concrete steps, UI labels, and options from the manual.
4. For multi-domain questions (e.g. “record with low latency then mix to stems”), load 2–3 chapters max.

### Chapter map

- **Introduction** → `chapters/01-introduction.md` — topics: editions, Prime, Artist, Professional, overview
- **Installation and Activation** → `chapters/02-installation-activation.md` — topics: install, activate, license, content installation, my.presonus
- **Setup** → `chapters/03-setup.md` — topics: system requirements, audio device, MIDI, I/O setup, content management, new song, Notion, colors
- **Fundamentals** → `chapters/04-fundamentals.md` — topics: undo, retrospective recording, mix engine, delay compensation, dropout protection, transport, key commands, smart templates
- **Pages** → `chapters/05-pages.md` — topics: Start page, Song page, Show page, Project page, Quick Switch, Smart Templates
- **Recording** → `chapters/06-recording.md` — topics: audio tracks, instrument tracks, metronome, loop recording, step record, track layers, cue mix, low-latency monitoring
- **Editing** → `chapters/07-editing.md` — topics: events, mouse tools, clip gain, grid, comping, timestretch, transient detection, track transform
- **The Score Editor** → `chapters/08-score-editor.md` — topics: score, notation, staff, drum notation, tablature, lyrics, Notion
- **The Browser** → `chapters/09-browser.md` — topics: browser, search, instruments, effects, loops, files, cloud, shop
- **Arranging** → `chapters/10-arranging.md` — topics: arranger track, chord track, signature track, tempo track, lyrics track, scratch pad, bounce, folder tracks
- **Mixing** → `chapters/11-mixing.md` — topics: console, routing, fader flip, channel editor, groups, scenes, VCA, listen bus
- **Spatial Audio** → `chapters/12-spatial-audio.md` — topics: Dolby Atmos, spatial audio, renderer, immersive, ADM
- **The Show Page** → `chapters/13-show-page.md` — topics: live performance, setlist, players, patches, performance view, show timeline
- **Automation** → `chapters/14-automation.md` — topics: automation envelopes, automation modes, instrument part automation
- **Control Link** → `chapters/15-control-link.md` — topics: Control Link, MIDI controllers, mapping, Mackie Control, hardware
- **Mastering (Project Page)** → `chapters/16-mastering.md` — topics: Project page, mastering, track sequencing, master device rack, publishing, song integration
- **Built-In Effects** → `chapters/17-built-in-effects.md` — topics: plugins, effects, Pro EQ 3, dynamics, reverb, delay, distortion, modulation
- **Built-In Virtual Instruments** → `chapters/18-virtual-instruments.md` — topics: Sample One XT, Presence XT, Impact XT, MaiTai, Mojito, Multi Instruments, Note FX
- **Collaboration** → `chapters/19-collaboration.md` — topics: Studio One+, collaboration, workspaces, sharing documents
- **Video Playback and Sync** → `chapters/20-video.md` — topics: video player, video track, sync, export video. **GROMIT is Artist: no Video Track.** Prep 48 kHz wav via Studio-One `tools/prepare_video_for_s1.py` or Music-producer `clip_edit_kb prepare-s1`. Loops/mux: `clip-edit-github-agent`.
- **Saving, Import and Export** → `chapters/21-saving-import-export.md` — topics: import song data, export audio, export MIDI, AAF, zip, import other DAWs
- **Index** → `chapters/22-index.md` — topics: index, lookup

## Answer style

- Prefer step-by-step procedures from the manual.
- Use official names: Arrange view, Console, Browser, Pool, Inspector, Control Link, etc.
- Mention macOS/Windows differences only when the manual does.
- Key commands: report as written in the manual; note that user keymaps may differ.
- Do not invent menu paths or parameters not present in the pack.

## Copying into a GitHub agent

Place this entire folder in a repository, for example:

```text
your-repo/
  .github/
    agents/          # or copilot instructions location you use
  knowledge/
    studio-one-6.6/  # <-- copy contents of this pack here
      AGENTS.md
      INDEX.md
      manifest.json
      chapters/
```

Then point the agent instructions at:

- Primary: `knowledge/studio-one-6.6/AGENTS.md`
- Retrieval: `knowledge/studio-one-6.6/INDEX.md` + `chapters/`

Optional: add a one-line include in repo `AGENTS.md` / `.github/copilot-instructions.md`:

```markdown
For Studio One 6.6 product questions, use knowledge/studio-one-6.6/AGENTS.md and retrieve from chapters/ via INDEX.md.
```

## Provenance

- Converted from: Studio_One_6.6_Reference_Manual_EN.pdf
- Manual version: V6.6
- PDF page count: 570
- Document content pages mapped: 1–564 (approx.)
- Conversion: text extraction via PyMuPDF; light cleanup of footers/bullets; structured into chapters for RAG/agent use

## License / copyright notice

Manual content is © PreSonus / related rights holders. This pack is a **restructured text extract for private agent use**. Do not republish the full manual as your own product documentation. Redistribute only if you have rights to do so.
