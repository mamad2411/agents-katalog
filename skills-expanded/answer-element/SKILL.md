---
name: answer-element
description: "Work skill. An element of this node comes to you: it asks how the node works — the wake text «Element <id> asks about the node's architecture: «…»» — or it tells the architect something, an alarm of its clock first of all — «Element <id> tells the architect: «…»». Every wake ends with an answer to the element: done, or «the core cannot — the architect must …» with the exact action. A question: find the answer in the core's instruction by its words, read only that section, answer in at most 10 lines with npm run task -- <id> \"Answer from the core to «<question>»: …\" (the only case where you read a file of the core). A message: pass the element's words to the person where they read you now, naming the element."
---

# Answer an element — its question or its message for the architect

**Process: working** — nothing changes in git: you read one section and answer, or you pass words on.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions.

## Never leave an element waiting (node step 679)

The owner, 2026-11-08: «я был на связи с агентом элемента клип и он продолжает ждать твой ответ … может быть именно там сейчас находится
архитектор … ты должен ответить ему о том что задача решиться не может и нужно вмешательство архитектора». The architect is often in the
element's chat, not in yours: whatever you tell only your own chat may reach nobody. So every wake by an element ends with an answer TO
the element (`npm run task -- <id> "Answer from the core to «…»: …"`), one of two:
- **done** — the element passes on the architect's verbatim word for a change the core has a command for (the link to CONFIG —
  `npm run look -- <id> --own|--linked`; a name — `npm run rename`): do it, check it, answer what changed;
- **the core cannot** — say it plainly, why in one line, and exactly what the architect must do (the button, the page with its full
  link, the words to say), for the element to tell the architect in its own chat. Never «sent to the architect» when it went only to
  your chat.

## A question about the node

1. Two to four English words of the question (the core's instruction is English):
   `grep -n -i "<word>" ../../CLAUDE.md | head -20` — the line numbers show the section.
2. Read only that section: `sed -n '<from>,<to>p' ../../CLAUDE.md` — tens of lines, the file is about 24 thousand
   characters, eight sections: role, context, building blocks, scenarios, modes, laws, glossary, where the details are.
3. Answer in at most 10 plain lines — what the node does and which door or command the element uses:
   `npm run task -- <id> "Answer from the core to «<the question>»: …"` — the question goes in: the answer may reach a fresh
   session that never asked. Only what you read; a path or a door you did not see is not named.
4. Nothing found → `npm run task -- <id> "Answer from the core to «<the question>»: the core's instruction does not say …; ask your architect."`

## A message for the architect (`tell-core`)

The element's agent says «Element <id> tells the architect: «…»» — work its clock woke it for ended with words the person must hear
(node step 636). A plain reminder never comes here: it surfaces in the main chat by itself through the core's notice door (636-8).

1. `npm run person` — where the architect reads you now (woken by an element, this session has no chat of its own: send with the reply
   tool to the chat_id it names); write there in the person's language — the element's words translated if they came in another,
   nothing else changed — as a working-process event: `⚙️ *Рабочий процесс · <the element's name>*`, the words a quote.
   **How it looks in Telegram** (the owner, 2026-11-03: «Цитата + значок + шапка (Рекомендую)»): the reply tool with `format:
   "markdownv2"` — the first line is the mark and the header in bold, the words a quote, one `>` per line. In the text put a backslash before each of
    _ * [ ] ( ) ~ > # + - = | { } . ! and the backquote; a send refused for its entities goes again as plain text.
2. Nothing added: no plan, no offer, no work. The person answers about it («перенеси на завтра») — the answer goes back to the element:
   `npm run task -- <id> "<their words>"`.
3. The person cannot be reached (no channel) — say so to the element: `npm run task -- <id> "Answer from the core to «…»: not delivered — …"`.

## Both

Never `.env.local`, never an element's files, never a change. Then `npm run done -- --close` when the element woke you; inside a live
conversation with the person — go on with it.
