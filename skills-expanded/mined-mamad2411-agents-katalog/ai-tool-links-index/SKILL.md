---
name: ai-tool-links-index
description: Router for the ~400 AI tools, websites and repos saved in Dimitrios's iCloud note "Links and sites" (https://www.icloud.com/notes/0034G1gqR4ra1BTR13sd25fdw). Use first whenever a user asks "is there a tool/site/repo for X" (video, images, websites/apps, voice, PDFs, slides/infographics, writing/research, business/automation, free utilities); it names the category skill to load and lists what was intentionally excluded.
---

# Links and Sites - Router

The note is a flat list of ~400 site names (many duplicated), 9 identifiable open-source projects and 67 TikTok short links. It contains **no written procedures or workflows**, so none were built. Everything below is a directory built from the saved names plus general knowledge; capability claims were not re-verified on the live sites.

## Which skill to load
| User need | Skill |
|---|---|
| Video generation, avatars, dubbing, clipping | `ai-video-generators` |
| Image generation, cleanup, logos, mockups, UI design | `ai-image-design-tools` |
| Build a site, app, chatbot, UI components | `ai-website-app-builders` |
| TTS, voice cloning, music, transcription | `ai-voice-audio-tools` (open-source voice repos: `ai-voice-tools`) |
| PDFs, conversion, translation, spreadsheets | `pdf-document-conversion-tools` |
| Slides, infographics, diagrams, charts | `presentations-infographics-diagrams` |
| Writing, summarising, research, study, chat models | `ai-writing-research-tools` |
| Sales, marketing, competitor research, automation | `business-growth-automation-tools` |
| Free utilities, learning, catalogues, maps | `free-utility-learning-resources` |
| The 67 saved TikToks | `tiktok-saved-links` |

## Repo skills (cloned shallow, read-only)
| Note entry | Repo | Skill | Licence note |
|---|---|---|---|
| Wan2.1 | Wan-Video/Wan2.1 | `repo-wan21` | Apache-2.0 |
| Hunyuan | Tencent-Hunyuan/HunyuanVideo | `repo-hunyuanvideo` | **Excludes EU/UK/South Korea** |
| Cogvideo | zai-org/CogVideo | `repo-cogvideo` | Apache-2.0 code; separate model licence |
| ominicontrol | Yuanshi9815/OminiControl | `repo-ominicontrol` | Apache-2.0 |
| stirlingpdf.io | Stirling-Tools/Stirling-PDF | `repo-stirling-pdf` | Open-core |
| reactbits.dev | DavidHDev/react-bits | `repo-react-bits` | MIT + Commons Clause |
| roadmap.sh | kamranahmedse/developer-roadmap | `repo-developer-roadmap` | see repo `license` |
| pinokio.computer | pinokiocomputer/pinokio | `repo-pinokio` | MIT-style |
| azgaar.github.io/fantasy-map-generator | Azgaar/Fantasy-Map-Generator | `repo-fantasy-map-generator` | MIT |

Not cloned: n8n (already in `setup-repos.sh`; see the existing `n8n-*` skills). Other entries (webcrumbs, uiverse, opensourcealternative.to, ninite, agent.ai, etc.) were saved as sites; their repos were not confirmed, so none were guessed.

## Other saved names (not in a category skill)
Added after a coverage check against the note. "Known" means Claude recognises the product from general knowledge; "unverified" means the note gives no description and Claude has not confirmed what it does. Verify on the live site before recommending any of them.

| Name as saved | Status | Likely use |
|---|---|---|
| Dishgen | known | AI meal and recipe planning |
| Mindgrasp (Mindgraspai) | known | AI summaries and study notes from lectures, PDFs, videos |
| yarn.co | known | Find a spoken phrase in video clips (like playphrase.me) |
| supermeme.ai | known | AI meme generator |
| Simplified.ai | known | Design, writing and video suite |
| loom.ai, muse.ai | known (check which product) | Video recording, video hosting |
| temp-mail.org | known | Disposable email; some sites block it |
| Popai / Pop.ai | unverified | Name is ambiguous (several products share it) |
| nuclearjs.org, uiball.com, official.minduck.com, xecutethevision.com | unverified | Unknown from the note |
| Cognifyminds, Doctapus, Rapid.ai, amee.la, bigteam.ai, effy.ai | unverified | Unknown from the note |
| 10015.io, nodsgy.com, thetwinai.com, genyou, chatjams.ai | unverified | Unknown from the note |
| prompthackers.co, prmpthero.com, prompmetheus.com, promptcraft.ai | unverified | Prompt libraries or prompt tools; confirm before use |
| documator.cc, commontools.org, thebricks.com, phase.com | unverified | Unknown from the note |
| seelab.ai, blaze.today.study, silo.team, buildpad.io, picdoc.ai | unverified | Unknown from the note |
| modulify.ai / modulify.com, productioncreate.com, n3.app (thumbnails), ai.tenorshare.com | unverified | Unknown from the note except n3.app (thumbnails) |
| pdftobrainrot.org | unverified | Turns PDFs into short-form "brainrot" style content per its name |
| quicktools | unverified | Name only |
| Billygram | known per note | Business videos |

Spelling variants in the note (for example hailouai.video and hailuoai.video, appob.ai and apob.ai, jilter.video and jitter.video, oldmaponline.org and oldmapsonline.org, text2ingfographic.com and text2infographic.com) are typos or duplicates of entries already covered; check the correct domain before sharing a link.

## Intentionally excluded from the skills
- A free movie/series streaming site (copyright-infringement risk).
- A service described in the note as bypassing card checks on free trials (terms-of-service violation).
- fakedetails.com (fake identity and address generator, commonly used to get around sign-up checks).
- AI-detector "bypass" tools are listed in `ai-writing-research-tools` only with a policy restricting help to disclosed, permitted use.

## Maintenance
When the note changes, re-fetch it (CloudKit public share resolves the text), add new names to the matching category skill, re-verify any site before recommending it, and delete dead links.
