---
name: use-deep-memory
description: "Work skill. The person wants something kept for later or brought back — «запомни», «запиши», «сохрани», «не забудь», «напомни о», «что я говорил про…», /remember or /remind from the bot's menu, in any language and any words — or sends a photo, a document or a voice note with such words in the same or the next message. Load it before npm run remember or npm run remind."
---

# The node's deep memory: remember and remind

**Process: working** — data only: no commit, no build. Answer in a few lines, in the person's language.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions.

## A memory request — by purpose, never by a word

The owner, 2026-10-26: «анализ прямого совпадения это вариант который нельзя использовать» — 82 languages, typos, a phone's autocorrect.
Read what the person wants:
- to keep a fact, a thing or a document for later → **remember**;
- to get back what was said or kept → **remind**;
- how you should work with them («отвечай коротко», «зови меня Ромой») → your picture of them (`know-the-architect`), and remember too
  when they asked to remember it;
- the same word in another task is not memory: «запиши меня к врачу» (a booking), «сохрани файл в проект» (a build), «пометь задачу
  готовой», «напомни завтра в 9 позвонить маме» (a time — a schedule, `core-schedule`);
- a decision about the product or the work you are shaping with the person right now («запомни, у каждой соцсети десятки аккаунтов»
  in a talk about their projects) is a decision of the step: verbatim into `current-steps.md` (skill `use-development-steps`), not the
  deep memory (node step 683; ✗ 2026-11-07 the owner: «не уверен что мы должны через память их отслеживать»).
Unclear — one short question.

## A thing and its words — one call

Telegram sends a photo, a document or a voice note as a message of its own; its words most often come in the next one («фото» → «запомни,
это моя мама»), sometimes before («сейчас пришлю фото мамы, запомни»); several photos may share one phrase. The memory ties a thing to its
words only inside one call, so you are the one who pairs them:
- a photo arrives with `image_path` — that file; a document, a voice note, audio or video arrive with `attachment_file_id` — call
  `download_attachment` first and take the path it returns; a message the node passed while you were off says «[вложение: …, file_id …]»
  — the same;
- a thing with no words yet → do not store it; one line: «Получил фото. Что с ним сделать? Например: «запомни, это моя мама»». The words
  that come next are its words;
- words that announce a thing → wait for the thing, then one call;
- then `npm run remember -- "<the person's words, as said>" --file <path> [--file <path> …]`.

## Remember

`npm run remember -- "<the words, as said>" [--file …]`. The command turns the memory element on for the task and off after (the first start
≈ 20 s, then seconds; a phrase ≈ 15–30 s, a thing longer). In Telegram reply first, in one line: «Принято, запоминаю — около минуты»; then the
result. Say what memory kept, from its answer, in plain words — never more than it said. A refusal — its reason, in the person's words.

## Remind

`npm run remind -- "<the question>"` prints two sources: **the deep memory** (element memory — facts, things, the date, how sure) and **the
diary** of everything said in the node (found by meaning). Give one answer: the fact, its date and where it comes from («из глубокой памяти»,
«из нашего разговора 24 октября»); a guess said as a guess. A found thing prints its file path — attach it to your Telegram reply (the reply
tool's files). Nothing in either — «об этом ничего не записано».

**How it looks in Telegram** (the owner, 2026-11-03: «Цитата + значок + шапка (Рекомендую)»): the reply tool with `format:
"markdownv2"` — the first line is the mark and the header in bold, the words a quote, one `>` per line. In the text put a backslash before each of
 _ * [ ] ( ) ~ > # + - = | { } . ! and the backquote; a send refused for its entities goes again as plain text. The deep memory's answer: `🟢 *Глубокая память*`, then the answer; reminders («⏰ Напоминание · …») come by
themselves and are never written by you.

## Whose memory

Every element keeps its own space in the memory and in every store behind it, opened with its own key (node step 654): an element never
finds what was said through another. You, the main agent, read every space with the node's data key and say whose each finding is;
what you keep yourself goes into the space `node`.

## Never

- Store or recall when the person switched memory off («не запоминай», `know-the-architect`): the commands refuse until «запоминай снова».
- Turn the memory element on by hand for these — the commands do it.
- Promise forgetting: the deep memory cannot forget yet (its graph keeps what it learned); web pages and YouTube links are not read on this
  node; a video needs ffmpeg on the machine.
