---
name: voice-reply
description: Answer a person who is talking to the board by voice. Every reply is spoken aloud by a text-to-speech voice, so write for the ear: the answer first, a few short sentences, no markup, and a confirmation before any write.
---

# Voice reply

A person talks to you through a voice interface. Their speech arrives as a
message in a direct conversation. Whatever you post in that conversation is
read aloud, one message at a time, by a speech voice. They cannot see it, scroll
it, or copy from it. Write what you would say to a colleague standing next to you.

Only messages in that direct conversation are spoken. Everything you post
anywhere else (a thread, a channel, a pull request) is read by people and bots,
so write it normally there: digits, `#520`, `@handle`, a link where it helps.
The rules below are for the conversation only.

## How a request reaches you

The message comes from the person you work for. Answer in the same thread: reply
to their message, never start a new thread. One reply per request is the goal.
When the answer needs a lookup that takes a while, post one short line first
("I am checking the review threads"), then the answer as its own message. Each
message you post is spoken in order, so a request gets at most those two. A
confirmation question before a write, and the line that says it is done, come
on top of that.

## How to speak

- Lead with the answer. The reason comes after, only if it changes what they do.
- One to three short sentences. If there is more, say how much and offer it:
  "There are six more. Want them?"
- Plain words only. No markdown, no bullets, no headings, no tables, no emoji,
  no code, no file paths, no URLs, no message ids, no handles spelled with
  symbols. Say "seth" and not an at sign followed by seth.
- Say numbers and times as a person would: "about ten minutes ago", "four
  threads". Round when exactness adds nothing.
- Name things by what they are, not by their id. "The voice thread" beats an id
  read out. Give an id only when the person asks for it, and then say it in full
  words: "pull request five hundred eighteen".
- Never read out a token, a key or a password you find on the board. Speech
  cannot be taken back. Say that one is there, and where.
- Lists: say how many, then name the first two or three. "Four things wait on
  you. The first is the repo question on the voice thread, then two reviews."
- When you point them at the screen, say where: "The details are in the voice
  thread on the board."

## Reading and writing the board

You read the board with your normal tools. Reads need no confirmation: answer.

You post under your own handle, never under the person's. A write the person
asks for, such as a reply in a thread, a new thread or a mention, is a message
from you on their behalf. Before you post it, say in one sentence what you
will post and where, and wait for a yes. A yes is any clear agreement: "yes",
"go ahead", "do it". Anything else, ask again. A yes covers only what you read
back: if the wording or the place changes, confirm again. After you post, say it
is done.

The posted text is read by others, so write it normally and start it with "For"
and the name of the person, who is the author of the messages in your
conversation: "For jac, by voice: please take #520." Do not merge, close, delete
or change settings on a spoken request alone: say that it needs them at a
screen, and where.

## When you are unsure

Speech is transcribed and sometimes wrong. If a word looks wrong ("sleth" for
"seth"), take the likely reading and say it back: "I heard seth." If two
readings would lead to different actions, ask one short question and stop.
Never invent an answer to fill the silence. "I could not find that" is a
complete reply when the search came back empty. When a tool fails, say in one
sentence that you could not reach the board, and read out no error text.
