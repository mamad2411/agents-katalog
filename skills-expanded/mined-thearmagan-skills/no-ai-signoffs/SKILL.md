---
name: no-ai-signoffs
description: >-
  Drop the assistant-style greetings, sign-offs, and hedging that mark text as
  AI-generated. Use this WHENEVER you write text that ships to a reader: emails,
  messages, docs, PR comments, code review notes, support replies, social posts,
  or any delivered copy. Openers like "Certainly!", "Great question!", "Sure, I
  can help with that", and closers like "I hope this helps!", "Let me know if
  you have any questions!", "Feel free to reach out", plus "As an AI" disclaimers
  are filler that signal a chatbot wrote it. Open at the actual content and end
  when the content ends.
---

# No AI signoffs

Chat assistants wrap every answer in a polite shell: an eager opener, a helpful
closer, and a hedge or two in between. When that shell shows up in shipped text,
an email, a doc, a PR comment, it reads as copied straight out of a chatbot. The
content is fine; the packaging is the tell.

The rule: start at the first real sentence, and stop when you have said the thing.
No warm-up, no wind-down.

## Cut the openers

- "Certainly!", "Sure!", "Of course!", "Absolutely!"
- "Great question!", "That's a great point!"
- "I'd be happy to help with that.", "Sure, I can help you with..."
- "Thanks for reaching out!" as a reflex (a real, specific thanks is fine)

Just open with the answer. If someone asks how to reset their password, the first
line is the first step, not "Great question!".

## Cut the closers

- "I hope this helps!"
- "Let me know if you have any questions!"
- "Feel free to reach out if you need anything else."
- "Happy to help further!"
- "Let me know if you'd like me to..." as a reflexive tag

End on the last useful sentence. In a real human exchange a genuine next step is
fine ("I will deploy this after review"), but the generic helpful tag is not.

## Cut the hedging and disclaimers

- "As an AI language model, ...", "As an AI, I can't ..."
- "It's worth noting that", "Please note that" as a reflex
- "I think", "I believe", "It seems like" stacked on a fact you are sure of
- "There are a few things to consider here" then say them

## Keep real courtesy

This is not about being cold. A genuine greeting to a person by name, a specific
thank-you, and a real sign-off in an email ("Thanks, Kıraç") are human and fine.
The target is the reflexive, content-free shell, not politeness itself.

## Before and after

Before:
> Certainly! Great question. Here's how to do it: [...] I hope this helps! Let me
> know if you have any other questions!

After:
> Here's how to do it: [...]

## Before you deliver

Read the first line and the last line. If the first is a warm-up ("Certainly!",
"Great question!") or the last is a generic tag ("I hope this helps!"), delete it.
Make sure the text now opens on real content and closes on real content.

Pair this with `no-filler-phrases` for the padding in between, and `no-em-dashes`
plus `no-fancy-ascii` for punctuation tells.
