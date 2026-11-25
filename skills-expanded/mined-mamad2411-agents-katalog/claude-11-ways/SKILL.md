---
name: claude-11-ways
description: Seven habits for using Claude as a thinking partner instead of a search box - build persistent context (Projects and an identity file), bring real problems with goal/context/constraints/stakes, challenge your own thinking, make it sound like you with writing samples, clarify before creating, upgrade the process with extended thinking, and control and validate the output. Each comes with a copy-paste prompt. Use when the user wants better answers from Claude. Source @aicareersuite "11 Ways to Master Claude" (Batch 99); only slides 01 to 07 and the cover were in the upload.
---

# 11 ways to master Claude - the seven that were shown

Stop using Claude like search; use it as a thinking partner. The slides give principles; the prompts below are written from them (not quoted).

| # | Habit | One-line version |
|---|---|---|
| 01 | Build persistent context | Projects plus an identity file so Claude remembers how you work |
| 02 | Bring real problems | Goal + context + constraints + stakes beat a search-style question |
| 03 | Challenge your thinking | Ask Claude to disagree with you on purpose |
| 04 | Make it sound like you | Share samples; match tone, structure, rhythm, vocabulary |
| 05 | Clarify before creating | Ask Claude to ask questions before it writes |
| 06 | Upgrade the process | Extended thinking, steps, let Claude design the prompt |
| 07 | Control and validate | Set length, audience, format; stress-test the answer |

## Prompts

**01 Identity file** (save the result as `identity.md` in the Project):
```
Interview me, one question at a time, to build an identity file for how I work: my goals, the work I do, my preferences, my tone of voice, and the files I keep. When you have enough, write it as a one-page file I can keep in this Project so you remember how I work.
```

**02 Real problem**
```
Our goal is [GOAL]. Context: [CURRENT SITUATION AND DATA]. Constraints: [TIME, BUDGET, RULES]. What is at stake: [STAKES]. Before answering, tell me what else you need to know.
```

**03 Challenge**
```
Here is my plan: [PLAN]. Disagree with me on purpose. Expose the weakest assumptions, give the strongest counterarguments, show the opposite view, then help me improve the plan.
```

**04 Sound like me**
```
Here are three samples of my writing: [SAMPLES]. Describe my tone, structure, rhythm and vocabulary in five bullets. Then write [TASK] in that voice and mark anything you were unsure about.
```

**05 Clarify first**
```
Before you write anything, ask me the questions you need: why this exists, who it is for, what constraints apply, and what success looks like. Ask them one at a time.
```

**06 Better process**
```
This is a hard task: [TASK]. Think it through in steps before answering, and tell me which parts you are least sure of. If my prompt is weak, rewrite it first and ask me to confirm.
```

**07 Control and validate**
```
Answer in [LENGTH] for [AUDIENCE] as [FORMAT]. Direct answers, no fluff. Then stress-test your own answer: what could go wrong, what are the risks, are there better alternatives, and what would success look like?
```

Related commands: `/clarify-first`, `/premortem`, `/redteam`, `/plain-human`, `/research-skeptic`.
