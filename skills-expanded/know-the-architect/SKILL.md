---
name: know-the-architect
description: "Both natures. Build and keep a small, honest picture of the person you work for: first contact, saving, updating, forgetting. Load it at the first contact of a session with no picture in your memory, when the person corrects how you speak or work, and when they say «что ты обо мне знаешь», «забудь» or «не запоминай». Keeping something for later («запомни», «напомни о») — use-deep-memory."
---

# Know the architect

**Process: both.** A small picture, not a file on a person. It exists to build the dialogue, nothing else. Written by the main agent
of the node at the architect's request (2026-10-24), placed by the node in step 595.

## Where the picture lives

Your native memory (the index `MEMORY.md` and one file per fact, type `user` or `feedback`) — the node keeps it in its own data
folder, so it survives a moved node. The elements' agents get the `user` and `feedback` lines of your index at the start of their
sessions: what you write here is how every agent of the node will speak to this person.

## First contact (no picture in memory)

One message, in the person's language, and say any question can be skipped (the owner, 2026-11-04, step 643: «главное агент получает
информацию о том как зовут или о том как лучше обращаться, в какой стиле лучше общаться с новым архитектором, а также как язык по
дефолту установить для его проекта и нужно ли сразу делать перевод … заведомо предупреждая что чем больше языков тем дольше и дороже
разработка»):
1. How should I call you — and «ты» or «вы»?
2. How do you like answers — short and straight, or detailed and warm?
3. What are you building, or what do you want from the node right now?
4. The project's language — the one its pages are written in first — and are other languages needed now? Say the price in the same
   line: every language is translated, checked and kept up on every change, so each one makes the work longer and dearer; another
   language can be added later at any time.
5. Anything I should never do or never touch?
6. What name or nickname should I answer to? And, if you like, what behaviour do you expect from me? (The owner, 2026-11-06, step
   661: «на какое имя или прозвище ты хочешь чтобы я откликался, если хочешь расскажи о том какое поведение ты от меня ожидаешь».) The
   name and the behaviour go into the person's block `data/main-agent/CLAUDE.user.md`; it yields to the instruction and the soul.
If the first message is a concrete task, answer the task first and put the questions at the end of the same reply. Save the answers as
they were said. Before you say anything about the project's languages, read the current set (skill `manage-app-settings` — reads work
from the file on disk); never assume which one is the default. The language set is changed only after the person's yes to it, through the node's setter (skill
`manage-app-settings`, `POST /api/config/languages`), and the rebuild it needs is named first (a few minutes, the pages stop for it);
other languages later — skill `expand-site-language`.
In the same message, two sentences on the modes, once: building the elements with their agents is ordinary work on the person's own
Claude Code subscription; when the built tools start doing tasks by themselves, that is a grey zone — Anthropic's limits assume
ordinary, individual use and name no threshold, so the more automatic work on the subscription, the higher the risk, and the tools' own
AI work (texts, pictures, voice) goes through the node's OpenAI key («Строительство → Переменные окружения»). Details on a question — skill
`provider-rules`. Never offer an Anthropic API key, and never promise that some amount is safe. Do not interview; the rest is learned by working together. Say once that the person can always see, correct and delete
their picture, and name the node's commands once, in one line (owner 2026-10-25, step 597): «Команды узла: запомни, напомни о, включить,
выключить — своими словами или из меню бота; «команды» — весь список».

## What to keep

- `user`: role, experience, what they build, language — a few lines.
- `feedback`: how they want you to work, with the reason and when it applies.
- One file per fact, one line in `MEMORY.md` for each; at most 15 facts about the person — when it grows, merge or drop the weakest.
- A preference is recorded after the person states it or repeats it, not after one guess; a correction replaces the old line the same
  day.

## What not to keep

Health, money, family, private opinions, anything said in passing or as a test («легенда», a made-up scenario), anything that would hurt
if it leaked. If it would help but is sensitive, ask first and save only with a clear «yes».

## «Запомни …», «что ты обо мне знаешь», «забудь …», «не запоминай»

The node keeps more than your picture: a diary of everything said (every agent, copied without a model), your notes «where I stopped»,
the last exchange given at a session's start and associations before a message. The person controls all of it with plain words; every
answer ends with one line confirming what changed.
- «Запомни …» (any words with that purpose) → the node's deep memory, skill `use-deep-memory` (step 597). When it is about the person or how
  to work with them, it is also a fact here.
- «Что ты обо мне знаешь» → `npm run memory -- show`, then in plain words: the picture, how much of the diary is kept and since when, and
  that the search by meaning sends each line to OpenAI for its vector (not used for training by default) and keeps it on this computer.
- «Забудь X» (a fact about the person) → delete its file and its index line.
- «Забудь, что было <день>» / «забудь вчерашний разговор» → `npm run memory -- forget --day <YYYY-MM-DD>` (the person's day, this
  computer's clock).
- «Забудь всё обо мне» → ask once; after «да» → `npm run memory -- forget --all` and delete every `user` and `feedback` file with its
  index line.
- «Не запоминай меня» → ask once; after «да» → `npm run memory -- off`: no agent of the node writes or recalls anything, and you stop
  saving facts. «Запоминай снова» → `npm run memory -- on`. What was said while it was off is never kept.
- When the person forgets something, say in the same line that Claude Code keeps its own session logs until it deletes them itself.

## Before you rely on it

Memory names what was true then, not now: before a recommendation that depends on the person, check it against what they say today.

## Test

Next session, with no help, you greet the person the way they asked and continue the last open task.
