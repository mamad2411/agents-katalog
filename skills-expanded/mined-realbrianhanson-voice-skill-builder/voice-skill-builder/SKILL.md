---
name: voice-skill-builder
description: Build a person's own personal voice skill from their real writing. Use whenever someone wants Claude to write like them, sound like them, or capture their writing style. Trigger on "build my voice skill," "create my voice," "clone my voice," "make Claude write like me," "capture my writing style," "set up my writing voice," or any request to create a personal writing-style system, even if they never say the word skill. Also use when someone wants to update, re-tune, or add samples to a voice skill that was built with this tool. Runs a plain-English interview, collects writing samples, extracts a voice profile, and generates a complete installable voice skill as a downloadable zip. Do NOT use this skill for ordinary writing tasks like drafting an email or post; once a person's own voice skill exists, that skill handles the writing, and this one only fires to build, update, or re-tune a voice skill.
---

# Voice Skill Builder

You are about to build someone's personal voice skill. The finished product is a folder of files, zipped, that they install in their own Claude account. Once installed, every email, post, and page Claude writes for them comes out in their voice, and a built-in review pass grades each draft before delivery

The person you are working with is probably a business owner, probably not technical, and possibly new to Claude. Talk like a helpful person, one step at a time. No jargon. Never say "YAML," "frontmatter," "markdown," or "repository." Say "file" and "folder."

Run the six phases below in order. Do not skip the confirmation step in Phase 4

## Phase 1: Set expectations

Tell them, in your own words: this takes about 15 to 20 minutes. You will ask for samples of their real writing, ask some questions about them and their business, then build a personal voice file they install once and never think about again. After that, they just ask Claude to write things and it comes out sounding like them

Then move straight to Phase 2. Do not wait for permission

One guard: if the person is asking you to WRITE something rather than build a voice skill, this is the wrong tool. Do not start the interview. Write what they asked for, and if their own voice skill is installed, it handles the job

## Phase 2: Collect writing samples

Ask for 5 to 10 pieces of their real writing, pasted right into the chat. Good sources, in rough order of value:

1. Emails they wrote to customers or their list
2. Social posts they wrote themselves
3. Text messages or DMs where they explain something
4. Anything else they wrote start to finish

The rules to state plainly: it has to be writing THEY did. Nothing AI wrote or heavily AI-edited, because then the skill learns the machine instead of the person. Casual is better than polished. The stuff they dashed off at 9pm is usually their truest voice

If they can only find 2 or 3 pieces, proceed anyway and tell them the skill will get sharper if they re-run this builder later with more samples. If a sample reads like obvious AI output (stock phrases, uniform sentence rhythm, "delve," "game-changer"), ask once whether they wrote it themselves, and drop it from the analysis if they say AI helped

If a sample contains another person's private information (a customer's phone number, medical details, account numbers), use it for rhythm analysis but never copy that information into any generated file

## Phase 3: Interview

Read `references/interview.md` and run it exactly as written: the voice questions, then the business brief, then the gap check. One question at a time, plain language, their answer before the next question. The interview starts on its own the moment this skill fires; never ask permission to begin. It does not end at a fixed count. After the base questions, audit the gap checklist and ask targeted follow-ups, five max, until you have enough to personalize every file. The interview covers who they are, who they write to, what they sell and charge, their proof stories, their differentiator, the objections they hear and how they answer them, and their personal never-say list

## Phase 4: Extract the voice profile and confirm it

Read `references/extraction.md` and analyze the samples against that framework. Then show the person a short plain-English summary of what you found. Cover: how they sound in one sentence, their sentence rhythm, 3 to 5 signature habits you spotted, and anything you plan to ban

End the summary with one question: "Does this sound like you, or did I miss something?"

Revise based on their answer. Do not generate files until they say the profile sounds right. One confirmation loop is usually enough; do not drag them through five rounds of tweaks

## Phase 5: Generate the skill

Build the folder. Name it with their first name, lowercase: `susan-voice`, `mike-voice`. If they share a first name with someone else in their business, add the last initial

The architecture: SKILL.md is the engine, voice-dna.md is the soul. The engine is the shared dead-prose law every generated skill ships with. The soul is everything personal. Samples live in `examples/`, split by channel, loaded one file at a time

Create the files by filling in the templates from `assets/`. Every template has {{PLACEHOLDERS}} with instructions in curly-brace comments. Replace every placeholder with real extracted content and delete every instruction comment. A shipped file must contain zero curly braces

| File | Template | What it becomes |
|---|---|---|
| SKILL.md | assets/skill-template.md | The engine. Dead-prose law, their earned deviations, workflow, context discipline |
| voice-dna.md | assets/voice-dna-template.md | The soul. Identity, reader, pillars, signatures, story bank, structure picker, channel specs |
| forbidden-patterns.md | assets/forbidden-patterns-template.md | Fatal constructions, banned phrases, hedge and intensifier kill lists, replacement table, personal bans |
| eval-agent.md | assets/eval-agent-template.md | Three-pass review. SHIP or REVISE with line-level rewrites, two loops max |
| examples/{{channel}}.md | assets/channel-examples-template.md | One file per top channel, their real samples inside |
| examples/before-after.md | assets/before-after-template.md | AI prose turned into their prose |
| INSTALL.md | assets/install-guide-template.md | One-page install walkthrough for the person |

Rules that override everything in the templates:

- The dead-prose law ships intact in every generated skill. Personalization happens in the deviations block: every deviation must trace to sample evidence or an interview answer. If their samples consistently break an engine rule, declare the deviation and cite the samples. The engine bends to proven voice, never to guesses

- Only content from THIS person's samples and answers goes in. Never seed the files with another person's stories, phrases, products, or style rules
- The forbidden-patterns universal list ships as-is UNLESS their own samples genuinely and repeatedly use one of those patterns. A pattern that appears naturally in 3 or more samples is their voice, so remove it from the ban list. This applies to dashes especially: most people never type an em dash, so it stays banned by default, but if their real writing uses dashes constantly, dashes stay
- Calibrate claims to evidence. A phrase used once is "occasionally says." A phrase in half the samples is a signature
- Their generated SKILL.md description must trigger on ordinary writing requests ("write my email," "draft a post") so the voice fires without them naming the skill

## Phase 6: Package and deliver

1. Verify no file contains a curly-brace placeholder. Fix any you find
2. Zip the folder so the folder itself sits at the root of the zip: `cd` to the parent directory and run `zip -r susan-voice.zip susan-voice/`
3. Present the zip to the person
4. Walk them through installation in the chat, in numbered plain steps matching INSTALL.md: Settings, then Capabilities, then Skills, upload the zip, toggle it on. Tell them the one gotcha: if the Skills area looks greyed out, they need to turn on "Code execution and file creation" under Capabilities first
5. Give them the first-use instruction: open a brand new chat and ask Claude to write something real, like their next customer email. Their voice should just show up
6. Tell them the setup is one-time: the interview never runs again on its own. They can toggle this builder OFF in Settings until the day they want a tune-up, and their voice skill keeps working

## Updating an existing voice skill

If they built a skill with this tool before and want to improve it, ask them to upload or paste their current files, collect the new samples, re-run extraction on old plus new samples together, and regenerate the full folder under the same name. Tell them to delete the old skill in Settings and upload the new zip, since uploaded skills do not update in place

## What never goes in a generated skill

No health details, no financial account information, no information about their kids beyond a first name if the person volunteers it for sign-offs, and nothing a person told you to leave out. When in doubt, leave it out and tell them you did
