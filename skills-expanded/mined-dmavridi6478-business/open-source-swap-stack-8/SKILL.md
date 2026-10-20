---
name: open-source-swap-stack-8
description: Verified register of the eight "if you're paying for X, try this instead" tools from a @coreclasseducation carousel - Jaaz, CutScript, OmniVoice Studio, Meetily, OpenDraft, InteraOne, Graphic Walker and OpenWhispr - each matched to its real repo, licence and last commit, with the claims that fail (Jaaz is not open source, OpenDraft and InteraOne are not what their slides show, the UI screenshots are mockups). Use when someone wants to replace a paid tool (Canva AI, Descript, ElevenLabs, Otter, Notion AI, Tableau, Whisper) with open source, or asks whether one of these is real, free or safe for commercial use.
---

# The "$200/month tool stack" swap list, checked

Source: a @coreclasseducation carousel, "8 underrated open source tools that can replace your $200/month tool stack" (10 slides). I matched each tool to a repo by web search and then cloned it to read its licence and README on 4 October 2026.

**Read this first.** The product screenshots on the slides look like generated mockups: stock-style avatars, a "Sep 2, 2024" date in a post about 2026 tools, and every UI in the same purple style. They do not show the real apps. The cover icons (GitHub, Notion, Docker, Blender, PostgreSQL, GIMP and others) are not the eight tools inside, and Notion is not open source. The "$200/month" figure has no source. [Certain]

| Slide tool | Slide says it replaces | Real repo | Licence | Last commit | Verdict |
|---|---|---|---|---|---|
| Jaaz | Canva AI and image/video generators | `11cafe/jaaz` | **Dual: free Community licence or paid Commercial licence** | 2026-03-02 | **Not open source.** Free for individuals. Organisations may use it only unmodified, for evaluation or non-commercial use. Team deployment, modification and redistribution need the paid licence |
| CutScript | Descript | `DataAnts-AI/CutScript` | MIT | 2026-03-06 | Real: local text-based video editor (Electron, FastAPI, Whisper-based transcription). Small project |
| OmniVoice Studio | ElevenLabs | `debpalash/OmniVoice-Studio` | AGPL-3.0; models carry their own licences | 2026-10-04 | Real, in beta. Clone voices only with permission |
| Meetily | Otter, Fireflies | `Zackriya-Solutions/meeting-minutes` | MIT | 2026-09-10 | Real, local-first. A paid "PRO" tier exists, so "all open source" is only partly true |
| OpenDraft | Notion AI, ChatGPT | `federicodeponte/opendraft` | MIT | 2026-10-01 | **Mismatch.** It drafts research papers with citation checking; it is not a general writing workspace |
| InteraOne | ChatGPT, Claude | not located | not checked | not checked | **Mismatch [Likely].** Web search describes an embeddable AI support assistant (an Intercom alternative). The slide shows a local "InteraOne 7B" chat app. I could not find the repo, so treat it as unverified |
| Graphic Walker | Tableau, Power BI | `Kanaries/graphic-walker` | Apache-2.0 | 2026-10-01 | Real: an embeddable drag-and-drop visualisation component, not a full BI platform |
| OpenWhispr | Whisper, Otter | `OpenWhispr/openwhispr` | MIT | 2026-10-02 | Real. Dictation first; its README also lists meeting transcription with speaker identification |

## Rules before swapping a paid tool

1. Read the licence file, not the slide. For anything a company will use, confirm that the licence permits team use and modification.
2. AGPL-3.0 (OmniVoice Studio) means: if you modify it and let others use it over a network, you must offer them your source.
3. "Open source" and "free for personal use" are different things; Jaaz is the second.
4. Match the real feature list to your need. Two of the eight do something different from the slide.
5. Compare on your own files before cancelling a subscription. A swap that costs a day a week is not a saving.
6. Local models mean your hardware does the work and quality varies; test with a real sample.

Not done: none of the eight was installed; InteraOne was not found; star counts and the "$200/month" claim were not verified.
