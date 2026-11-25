---
name: jinhezai-writer
description: |
  今何在式中文幻想写作机制 Skill。基于《九州·羽传说》《若星汉天空》本地一手语料、公开访谈、豆瓣/微博主页线索，提炼人物先行、设定即枷锁、神话现代化、悲观理想主义、反类型英雄和对白思辨等写作方法。
  Use when the user asks for 今何在风格、今何在式、悟空传感、九州感、若星汉天空感、中文幻想、神话新编、悲壮少年感、反英雄史诗、宿命感场景、或要求把文本改得更有宏大幻想与哲思张力。
  Do not copy protected text, exact voice, canon characters, canon settings, or recognizable plotlines; transform requests into high-level inspired original writing and revision guidance.
---

# 今何在式幻想写作

## Core Rule

Use this skill to create or revise **original Chinese fantasy writing** using high-level narrative mechanisms associated with Jin Hezai's work. Do not impersonate the author, do not claim the output is by him, and do not reproduce his protected wording, characters, settings, or plots.

If the user asks to “模仿原文/续写原作/写某个原作角色”, redirect to an original analogue:

- Keep the requested emotional function, conflict type, and narrative pressure.
- Replace all canon names, places, organizations, magic rules, and signature lines.
- State briefly that the piece will use high-level mechanisms rather than protected text.

## Read References

- For any generation or revision task, read `references/style-card.md`.
- For source audit, updating the skill, or explaining why a rule exists, read the relevant file in `references/research/`.
- The original book files used during research are not included in the public skill. Use the distilled notes in `references/research/` and `references/style-card.md`; do not quote protected source text.

## Fast Defaults

When the user gives an underspecified writing request, proceed without asking unless a missing fact blocks the task.

- Language: Chinese.
- Output: original fiction, not canon fanfiction.
- Length: 800-1500 Chinese characters for a scene; 6-10 beats for an outline.
- Tone: tragic, romantic, questioning, with controlled lyricism.
- Setting: invent new names and rules.
- End: leave a cost, a question, or a small light in darkness.

Ask at most one clarification only when the user’s desired format is genuinely ambiguous, such as “短篇大纲还是直接写正文？”

## Workflow

### Step 1: Classify The Task

Choose one mode:

| User request | Mode |
|---|---|
| “写一段/写开头/写场景” | Scene Draft |
| “给我故事/短篇/长篇设定” | Story Architecture |
| “帮我改得更有今何在感” | Revision |
| “设计人物/世界观/神话体系” | Character And World |
| “点评这段像不像” | Critique |

### Step 2: Find The One Question

Before writing, identify the single question underneath the story. Do this internally unless the user asks for explanation.

Good questions:

- If a person can fly only by losing a place to stand, is that freedom?
- If the future is already known, what still counts as courage?
- If someone is called a monster by history, who benefits from that name?
- If victory requires becoming what you hate, who has won?

Bad questions:

- “How do I make it cool?”
- “How do I add more worldbuilding?”
- “How do I make the protagonist stronger?”

### Step 3: Build The Pressure System

Every draft needs five parts:

1. **Bright desire**: what the protagonist wants in plain human terms.
2. **Cruel rule**: the fantasy law, prophecy, bloodline, ritual, war, or institution that makes the desire costly.
3. **Counter-voice**: another character who exposes the desire’s selfishness, naivete, or hidden fear.
4. **Visible motif**: sky, wind, snow, moon, darkness, light, old city, song, river, ash, or another concrete image.
5. **Irreversible price**: the choice changes something that cannot be restored.

If one part is missing, add it before drafting.

### Step 4: Draft Or Revise

Use the mode-specific rules.

#### Scene Draft

- Open with a concrete threshold: before departure, under a strange sky, after a battle, beside a wall, in a ruined temple, at a ritual, or in underground darkness.
- Bring the conflict into dialogue by the second or third paragraph.
- Alternate short dialogue with lyrical narration.
- Make one line in the scene act like a blade: it should reveal the truth the protagonist does not want to hear.
- End on action or image, not explanation.

#### Story Architecture

Return:

1. Core question.
2. Protagonist wound and false belief.
3. Fantasy rule that traps them.
4. Opposing force with a self-justifying worldview.
5. 6-10 plot beats.
6. Final cost and remaining light.

Do not overbuild maps, races, dynasties, or magic systems unless each item pressures a character.

#### Revision

Diagnose first, then rewrite.

- Mark what is currently generic: flat villain, decorative setting, easy victory, slogan dialogue, abstract emotion.
- Add a cruel rule or make an existing rule cost more.
- Replace direct philosophy with action, image, or argument.
- Rewrite only the amount requested. If no amount is given, revise the most important 300-800 characters.

#### Character And World

Create characters through contradiction:

- Desire vs fear.
- Public role vs private shame.
- Mythic identity vs ordinary need.
- Power vs price.

Create worlds through restrictions:

- What can people do only once a year?
- What does power take from the body, memory, voice, name, home, or future?
- Which institution turns a miracle into hierarchy?
- Which old story is false, and who keeps repeating it?

#### Critique

Lead with the biggest writing problem. Then give concrete fixes.

Check:

- Does the scene have a single question?
- Does every fantasy element create pressure?
- Are characters arguing from different wounds?
- Is the lyricism earned by action?
- Is the ending too easy?

## Style Rules

### Use

- High-contrast images: sky vs earth, light vs darkness, flight vs exile, king vs child, song vs silence.
- Dialogue as philosophical conflict, not exposition dump.
- A tragic but not nihilistic ending.
- Abstract nouns only after concrete sensory setup.
- Occasional irony toward heroic and prophetic conventions.

### Avoid

- Exact phrases from Jin Hezai or his books.
- Canon settings such as 九州, 羽族, 鹤雪团, 天驱, 悟空传 characters, or directly equivalent renamed copies.
- Slogans detached from scene.
- A protagonist who is special only because the narration says so.
- Villains who exist only to be hated.
- Overuse of “命运、宿命、天空、黑暗、光” without new context.

## Output Checklist

Before finalizing a generated text, silently check:

- The protagonist makes or refuses one meaningful choice.
- At least one fantasy rule has a human cost.
- At least one line of dialogue changes the emotional balance.
- The strongest image appears near the ending.
- The piece does not reuse protected characters, settings, plotlines, or famous lines.
- The result feels like an original story with Jin-Hezai-like mechanisms, not a pastiche.

## Research Boundary

This skill is based on:

- Local user-provided copies of 《九州·羽传说》 and 《若星汉天空》 analyzed during creation; the source books are excluded from the publishable skill.
- Public interviews from 2019 and 2025.
- Public profile links supplied by the user.

Limitations:

- It is not an official author model.
- It cannot predict the author’s private intent.
- Public social-media content was not fully available in this run.
- Research cutoff: 2026-06-26.

Research details are in `references/research/`.

---

> 本 Skill 由女娲 Skill 造人流程辅助生成，并按 skill-creator 规范整理。
