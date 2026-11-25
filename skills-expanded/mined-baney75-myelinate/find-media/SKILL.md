---
name: find-media
description: "Use when a learner wants an existing video, licensed figure, model, simulation or diagram to learn a concept. Not stock photos, banners, decor or work diagrams."
---

# Find Media

Media earns its place when it shows something words cannot: spatial layout, a process unfolding, a structure in 3D, a real specimen, a quantity changing. It wastes time or harms learning when it is decoration, when it is wrong, or when watching replaces doing. This skill finds existing outside media for learning, checks its legal use and accuracy, and makes the learner use it actively. Stock or decorative images for websites or marketing, and diagrams for work deliverables, belong outside Myelinate. Requests to draw or show a new teaching diagram or concept map belong to `tutor` for a class or `teach` for self-directed learning, using `references/visual-teaching.md`.

Paths like `references/…`, `templates/…` and `examples/…` are relative to this skill's folder, which carries its own copy of every file it names. Other Myelinate skills are siblings (`../tutor/SKILL.md`) and are installed as their own skills too. If a file is missing from your copy, work from this file and the router's core rules.

Evidence tags: **Strong**, **Moderate**, **Weak**, **Craft** (as in **memory-hooks**). Source table with URLs and licenses: [media-sources.md](references/media-sources.md).

## 0. Rules that override everything else

1. **Every recommendation must exist.** Verify by search or fetch before naming it. Give the exact title, channel or creator, and URL. Never invent a video, figure number, timestamp or license.
2. **License before use.** Record title, author, source and license (TASL) for anything placed in an artifact. "Found on Google Images" is not a license.
3. **Accuracy before beauty.** Check labels, arrows, scale and terminology against the course or a reference. A pretty wrong diagram teaches the error.
4. **Media follows an attempt or prepares one.** It never replaces retrieval and practice.
5. **Course materials stay private.** Use figures from a learner's textbook or slides only in their private study, only when they supplied them, and never publish them.

## 1. When media helps (Mayer's principles)

Mayer's cognitive theory of multimedia learning (Mayer, *Multimedia Learning*, 3rd ed., Cambridge, 2021) is the working model: limited visual and verbal channels, active integration. Principles most relevant here (Moderate-Strong, mostly short lab lessons; effects shrink for experts):

- **Multimedia:** words + relevant pictures beat words alone for novices.
- **Coherence:** cut interesting-but-irrelevant material. Seductive details hurt learning: Sundararajan & Adesope (2020, *Educ Psychol Rev* 32:707 to 734), meta-analysis of 58 studies, >7,500 students; worse when the distractor sits next to a relevant diagram or stays on screen.
- **Signaling:** highlight what matters (arrows, color for the one changing quantity, headings).
- **Spatial and temporal contiguity:** labels on the figure, not in a legend; narration in sync with the animation.
- **Segmenting:** learner-paced chunks beat one continuous stream.
- **Pre-training:** teach the names and parts before the process animation.
- **Redundancy:** do not read on-screen text aloud word for word over a busy graphic.
- **Expertise reversal:** scaffolds that help novices can slow experts. Strip labels and guidance as the learner improves.

Pick the medium by what must be seen:

| Need | Best medium |
| --- | --- |
| Spatial relationships, 3D anatomy, molecular shape | 3D model or multiple labeled views; physical model kit for stereochemistry |
| Real appearance (tissue section, gross specimen, mineral, manuscript, artifact) | Photograph or micrograph with scale bar and stain named |
| Process over time (action potential, mechanism, orbit) | Short animation or simulation the learner can pause, step, and change |
| Relationships among quantities | Interactive graph (Desmos, GeoGebra, PhET) the learner manipulates |
| Classification and structure of an argument or pathway | An existing diagram the learner can complete |
| Expert reasoning aloud (problem solving, clinical case) | Short worked-example video, then a parallel problem |

## 2. Where to search

Start from sources that state a license and have editorial review. Full table, URLs, licenses and caveats: [media-sources.md](references/media-sources.md). Summary:

- **Openly licensed, reusable with attribution (check per item):** Wikimedia Commons (MediaSearch has a license filter; licenses vary per file and Wikimedia does not warrant them); Openverse (aggregator; states it does **not** verify licenses); Servier Medical Art (CC BY 4.0); NIH BioArt Source (per-item: public domain or CC BY); PhET simulations (historical collection CC BY 4.0 with a required attribution line; terms changed for sims published after 2026-03-29); Smithsonian Open Access (CC0); RCSB PDB (data CC0; Molecule of the Month and PDB-101 CC BY 4.0).
- **Open but NonCommercial-ShareAlike:** OpenStax (now CC BY-NC-SA 4.0 across the library; some older editions were CC BY; check the book's license page; third-party images inside may differ); LibreTexts (license varies per page, some "not declared"); Radiopaedia (CC BY-NC-SA 3.0); Michigan Histology (CC BY-NC-SA 4.0; commercial AI training explicitly prohibited); ChemTube3D (CC BY-NC-SA 2.0 UK).
- **Free to view, mixed terms:** NCBI Bookshelf (per-book copyright; embedded figures may be third-party "reprinted with permission"); HHMI BioInteractive (per-resource terms in each "Details" section); MolView, Desmos, GeoGebra (free tools; GeoGebra is non-commercial unless licensed).
- **Proprietary, link, don't copy:** Kenhub (private use only; images licensable separately), TeachMeAnatomy (copies for your own educational needs only), Visible Body (subscription), BioRender (free plan: no publishing figures; standalone redistribution of its icons prohibited on all plans).

Search moves:
- Use the discipline's term plus the view: "nephron diagram labeled SVG", "simple cuboidal epithelium H&E 40x", "SN2 animation".
- Filter by license first (Commons, Openverse), then judge quality.
- For structures, search by PDB ID or molecule name in RCSB and PubChem; for 3D small molecules, MolView or ChemTube3D.
- For histology, use a virtual microscope (Michigan Histology) so the learner pans and zooms, not a single cropped image.

## 3. Vet before use

Check every item against this list:

1. **Exists and loads** at the URL you will give. Record retrieval date.
2. **License** read on the item's own page, not inferred from the site's home page. Record TASL: *Title*, *Author*, *Source* (URL), *License* (with link). Template: `*Title*, by *Author*, *Source URL*, *License* (linked)`. Fill it only from fields read on the file page.
3. **Accuracy:** labels point to the right structure; arrows show the right direction (curved arrows start at electrons); scale bars and stains stated; terminology matches the course (e.g., 2,3-BPG vs 2,3-DPG; Terminologia Anatomica vs eponyms); no outdated taxonomy (five-kingdom posters, "Protista" as a single clade) or retracted models.
4. **Level and convention:** matches the course (MCAT vs upper-level biochem; IUPAC vs common names; sign conventions in physics).
5. **Clutter:** cut or crop decoration (coherence). Prefer SVG you can edit.
6. **Accessibility:** alt text that describes what the figure shows; color is never the only code; captions on video.

**Hotlinking:** do not hotlink images into labs or saved pages. URLs break and images change. Download, store beside the artifact, and record the source and license. Exception: embed players (YouTube, PhET, Desmos) by their official embed method.

**Copyrighted textbook figures:** never place them in public artifacts. In a private study session, use only figures the learner supplied, and do not redistribute them. If the learner needs something to share, make an original figure through `tutor` or `teach` with `references/visual-teaching.md`.

## 4. Quiz images: mask completely

When a figure becomes a quiz ("label structure 3"):
- Remove or cover every label, leader-line text, legend entry and caption that reveals the answer.
- Rename the file (`fig-07.png`, not `left-ventricle.png`); strip title/alt text that names the answer; replace alt text with a neutral description ("Coronal section of heart, structure marked 3").
- Check SVG source text and `<title>` elements, image metadata, and nearby captions.
- One occluded label per card (see **flashcards**); keep the rest visible only if they do not give it away by elimination.

## 5. When an existing figure does not fit

If the learner asks you to draw or show a new diagram, concept map, graph or step-by-step picture to understand a topic, use `tutor` for a class or `teach` outside a class. Follow `references/visual-teaching.md` there. That includes making a blank or masked version for practice and drawing the exact case from the learner's problem. This skill can supply an existing source image or model when the teaching skill needs one. For complex real anatomy, prefer the learner's course figure or a licensed real image over a generated drawing; check the labels before use.

## 6. Videos and YouTube recommendations

Video is best for watching an expert reason or a process move. It is weakest as a substitute for practice. Brame (2016, *CBE Life Sci Educ* 15:es6) summarizes: keep it short, signal key points, segment, and add interactivity (guiding questions, pause points). In MOOC logs, engagement dropped sharply beyond about six minutes (Guo, Kim & Rubin 2014, *Proc. ACM Learning@Scale*: observational, engagement not learning).

**The method is `references/video-finder.md`:** write the target, must-say terms and course claims from their material, search wide, find the segment, vet each course claim against the transcript, and give one segment with pause points, a recall prompt and a problem. The steps below are the minimum when that file is missing.

### Search, verify, give the link

"Give me the link" gets a link, every time. "I couldn't pull the URL, search for the title" is the failure this section exists to prevent: you did the search, and the learner is the one left searching.

1. **Search for the URL, not just the title.** Use the specific concept at the course's level, and aim at the video page: `"SN1 SN2 E1 E2" site:youtube.com`, or the exact title and channel plus `youtube.com/watch`. A page about the video (a course index, a blog, a study site) often links to it; read that page if search doesn't show the URL.
2. **Check each candidate.** If you can fetch pages, fetch `https://www.youtube.com/oembed?format=json&url=<the watch URL>`: a 200 returns the true title and channel, and anything else means don't trust it. Confirm the title and channel match what you meant to recommend. Never give a video ID you didn't read from a page. This proves the video exists and who posted it, and nothing else.
3. **If you have the title but no URL after trying,** give a one-click search for exactly that title, labeled as a search: `[Search YouTube for this video](https://www.youtube.com/results?search_query=SN2+SN1+E1+E2+Reaction+Mechanisms+Made+Easy+Organic+Chemistry+Tutor)`. That link can't be wrong, and it saves them the typing. Never tell them to go search.
4. **Check accuracy** against the transcript or description for the part you'll assign, and against the course source (`../video/SKILL.md` has how to get a transcript). If you can't inspect it, say: "Not reviewed by me; check against your notes." Quote the video or the course only after checking the words (`references/video-finder.md` §4).
5. **Check fit:** level, notation and convention (Na⁺/K⁺ stoichiometry, IUPAC names, sign conventions); date (pre-2015 MCAT content may not match the current outline); length; captions; paywall.
6. **Lead with one pick.** Give the best segment of the best video and say why, then one or two alternatives at most. A timestamp range only if you read it in a transcript ("6:10 to 11:30: the inhibitor graphs").
7. **Show it where you can.** If your host renders HTML inline, adapt the video view in `templates/inline-widgets.html`: the player, what to watch for, pause questions and a recall box. Otherwise give the link and the active-viewing steps below.

**With no search tool this turn:** say so in one line, then still help. Say which channels are worth trying from the list below, as starting points you haven't checked today, and give a one-click search for each. Never name a specific video from memory as if you'd confirmed it. Never say you verified a channel: that list was checked when it was written, not by you now.

### Place it correctly
- **Pre-training:** a short video for names and parts *before* a hard session.
- **After a first attempt:** learner tries a problem, then watches the worked solution, then does a parallel problem unaided.
- **Never as passive substitute** for retrieval or practice.

### Active viewing protocol (give this to the learner)
1. Before playing: write one question the video should answer.
2. **Pause-predict** at each step: "What's the next arrow / next sign / next stage?" then play.
3. After: close it, write or say the key steps from memory, then check.
4. Do one new problem without the video.

### Starter channels

A maintainer last checked this list on 2026-10-06 (channel exists, recent upload seen). It's a list of places to look, not something you verified. If you can, check the specific video this session. Don't tell a learner you checked a channel unless you did.

Channels are starting points; vet the specific video. Free YouTube; many have paid companion sites.

**Biology, physiology, medicine**
- **Ninja Nerd** (youtube.com/@NinjaNerdOfficial), long, whiteboard lectures across physiology, anatomy, pathology; active. Caveat: long; assign segments.
- **Khan Academy Medicine / MCAT** (youtube.com/@khanacademymedicine), MCAT-aligned basics. Caveat: last upload 2021; check against the current AAMC outline.
- **Osmosis from Elsevier** (youtube.com/@osmosis), concise illustrated disease and physiology overviews; active. Caveat: YouTube videos are a subset; full library and question bank are paid.
- **Armando Hasudungan** (youtube.com/@ArmandoHasudungan), hand-drawn physiology, pathology and pharmacology; active. Caveat: medical-school framing; check level.
- **CrashCourse** (youtube.com/@crashcourse), Anatomy & Physiology playlist (49 episodes) and Biology series. Caveat: fast survey-level; not exam-depth.
- **Amoeba Sisters** (youtube.com/@AmoebaSisters), intro biology, clear analogies; active. Caveat: intro/high-school level.
- **Dirty Medicine** (youtube.com/@DirtyMedicine), USMLE-style high-yield facts and mnemonics. Caveat: exam-targeted; audit mnemonics (see **memory-hooks**), not for first-pass understanding.

**Chemistry and organic chemistry**
- **Leah4sci** (youtube.com/@Leah4sci), organic chemistry and MCAT strategy; active. Caveat: MCAT-strategy videos are test-specific; use the concept videos for coursework.
- **The Organic Chemistry Tutor** (youtube.com/@TheOrganicChemistryTutor), enormous library of worked problems in chemistry, physics, math. Caveat: procedure-heavy, light on why; last upload March 2026.
- **Chad's Prep** (youtube.com/@ChadsPrep), full general chemistry, organic chemistry, physics and MCAT courses; active. Caveat: a paid companion site holds additional practice.
- **Professor Dave Explains** (youtube.com/@ProfessorDaveExplains), short tutorials across chemistry, biology, physics, math. Caveat: the channel also posts combative debunking videos; assign tutorials specifically.

**Physics**
- **Flipping Physics** (youtube.com/@FlippingPhysics), AP and intro physics with clear problem setups; active.
- **Michel van Biezen** (youtube.com/@MichelvanBiezen), thousands of short worked problems in physics and math. Caveat: last upload January 2025; style is procedure-first.
- **Physics Girl** (youtube.com/@physicsgirl), conceptual phenomena and demonstrations; uploading again in 2026. Caveat: enrichment, not course-aligned.
- **MIT OpenCourseWare** (youtube.com/@mitocw; ocw.mit.edu), full lectures; for intro mechanics use **8.01SC Classical Mechanics, Fall 2016** (Chakrabarty, Dourmashkin et al.). Note: in December 2014 MIT removed Walter Lewin's lectures from OCW and edX after finding he had engaged in online sexual harassment of a learner, and revoked his emeritus title; copies of his older 8.01 lectures circulate elsewhere. Present this factually if asked; recommend the MIT-maintained course.

**Math and calculus**
- **3Blue1Brown**: *Essence of calculus* playlist (12 videos; youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr): geometric intuition. Caveat: intuition, not drill; pair with problems.
- **Professor Leonard** (youtube.com/@ProfessorLeonard), full-length lecture courses, e.g., *Calculus 1 (Full Length Videos)* (playlist PLF797E961509B4EB5); active. Caveat: lectures run long.
- **Khan Academy** (youtube.com/@khanacademy; khanacademy.org), short videos with practice exercises on the site; active.

**Philosophy and theology** (present theology sources as traditions, not neutral authorities)
- **CrashCourse Philosophy** (playlist, 47 episodes), broad survey. Caveat: survey-level; read the primary text.
- **Kane B** (youtube.com/@KaneB), careful lectures on analytic philosophy topics (metaphysics, epistemology, philosophy of religion); active.
- **Wireless Philosophy / Wi-Phi** (youtube.com/@WirelessPhilosophy), short animated explainers by academic philosophers. Caveat: last upload 2023; wi-phi.com had an expired TLS certificate when checked, link the YouTube channel.
- **BibleProject** (youtube.com/@BibleProject), animated book overviews and biblical themes; non-denominational nonprofit with a Protestant (evangelical) background; active. Caveat: one interpretive tradition; compare with critical and other confessional scholarship on contested points.
- **Bishop Robert Barron / Word on Fire** (youtube.com/@BishopBarron), Roman Catholic commentary and sermons; active.
- **Ligonier Ministries** (youtube.com/@Ligonier), Reformed Protestant teaching (founded by R.C. Sproul); active.
- **Open Yale Courses** (oyc.yale.edu; youtube.com/@YaleCourses), full university lectures, including religious studies, philosophy, history, and sciences.

When teaching theology, say which tradition a source speaks from, pair sources across traditions on contested points, and keep primary texts central.

## 6b. Show it now (during live teaching)

In a tutoring session, an existing figure is a teaching move:
1. Find one vetted figure that shows the single relationship you're teaching. If a new sketch is needed, use `tutor` or `teach` with `references/visual-teaching.md`.
2. Show it inline if the platform renders images or widgets; otherwise give a direct link with the figure number and what to look at ("Figure 22.20, look only at the dashed curve").
3. Ask one question about it ("Where on this curve does exercising muscle sit?"). Hide or cover labels you're about to quiz.
4. Licensing still applies to anything you embed in a saved or shared artifact; a link for private study is fine.

When the learner should operate a figure (rotate a molecule, move a slider, step a mechanism), use `tutor` or `teach` with `references/visual-teaching.md` for the live teaching visual. Use `lab` for a standalone interactive lesson.

In voice mode, describe the figure in words and offer to send it in text.

## 7. Anti-patterns

- Naming a video, figure or license you have not verified.
- Telling a learner to go search for a video you just found, instead of giving a link.
- Saying you verified or checked something in this conversation when you didn't.
- "Watch this channel" with no specific video, or a list of ten.
- Assigning a video in place of retrieval or practice; ending a session with a video.
- Hotlinking images that will break; copying proprietary atlas images into public artifacts.
- Using a course textbook figure in anything shared.
- Quiz images that leak the answer through filename, alt text, caption or a neighboring label.
- Decorative stock images, memes and jokes beside key diagrams (seductive details).
- Trusting an aggregator's license label without opening the source page.
- Generated figures presented as if to scale, or with arrows and labels unchecked.
