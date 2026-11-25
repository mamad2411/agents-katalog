---
name: your-voice
description: >
  Writes anything in the user's own voice (emails, chat, LinkedIn posts, docs) from
  their voice.md, or a strong default until they have one, with their house style
  applied. Use for "write this in my voice", "draft a reply", "make this sound like
  me", "rewrite in my tone", "polish this", and whenever drafting text the user will
  send or publish. Wording only.
---

# Your voice: write it the way they would

The bar: the user sends or posts the text without changing a word, and the reader
can't tell it wasn't typed by hand.

This skill decides HOW things are said. WHAT is said (facts, numbers, terms, the
decision itself) comes from the task, the user, or whichever skill owns that
subject. Never invent a fact to make a sentence sound better.

## 1. Load the voice (once per session)

1. **Find their voice.md.**
   - With a shell: `python3 "<this skill's folder>/../your-voice-builder/scripts/voice.py" where`.
     It returns the voice home (`~/.claude/voice/` unless `$VOICE_HOME` is set),
     whether `voice.md` exists, and its front matter.
   - Without a shell (Claude.ai chat, a project): look for `voice.md` among the
     project files, uploaded files or the user's own skills.
2. **Found:** read it in full. It wins on every wording question: register,
   openers, closers, phrases, emoji, exclamation marks, the never-list.
3. **Not found:** read `references/default-voice.md` and use it. Say this once per
   session, at the end of the first piece of writing:
   "Using the default voice - say 'build my voice' and it learns yours from your sent
   writing in a few minutes."
   If `where` reports `inbox_voice.filled: true`, say instead: "You have a voice
   profile from Creator Management Inbox - say 'import my voice' to use it here and
   everywhere else."
4. **Never imitate another person's voice as if it were the user's.** Not a
   colleague's, not an example profile's, not the person they're replying to.
   Matching the reader's level of formality is fine; copying their phrases is not.

## 2. Write

1. **Pick the register by channel:** email, chat, LinkedIn or docs. Use the
   matching section of the voice. A register marked `(default)` in voice.md, or
   missing, comes from `references/default-voice.md`.
2. **Use the right shape** when the moment matches one (first reply, feedback,
   decline, a number, a nudge). Shapes are principles: fill them with this task's
   facts, never with the example lines.
3. **Draw on their phrases, don't stack them.** One or two of their real phrases
   where they fit naturally. A text made of catchphrases reads as a parody.
4. **Formatting follows the voice:** paragraph length, bullets, bold, links,
   emoji and exclamation marks at the frequencies voice.md states. A frequency is a
   ceiling over many messages, not a quota for this one.

### Polishing the user's own text

Minimal touch. Fix grammar, flow and house style; tighten only where a sentence is
genuinely confusing or repeated. Keep their words, their order and roughly their
length. Do not rewrite their text into voice.md's phrases: it's already their voice.
Say in one line what you changed if it was more than typos.

## 3. Enforce the house style (every time, before handing over)

voice.md ends with a fenced `house-style` block:

```
em_dashes: replace | allow
banned_words: word=replacement, ...
exclamation_marks: allow | avoid
emoji: never | rare | free
```

- **With a shell:** save the final text to a scratch file and run
  `python3 "<this skill's folder>/../your-voice-builder/scripts/voice.py" check <file>`
  (it reads the user's voice.md, or the default voice if they have none). Use the
  returned `text`. Fix anything listed under `warnings` by rewriting the sentence,
  not by deleting punctuation blindly.
- **Without a shell:** apply the same rules by hand. Em dashes and en dashes become
  a spaced hyphen ( - ), except in number ranges (10-12) and inside URLs or code.
  Banned words are swapped whole-word, keeping a leading capital.
- Write it right the first time; the check is a safety net, not the method.

## 4. Freshness

If voice.md's `refreshed` date (or `built`, if there is no `refreshed`) is more
than 30 days old, add one line at the end of the response, once per session:
"Your voice profile is [N] days old - say 'refresh my voice' to update it from your
recent writing."

Never refresh, rebuild or edit voice.md unasked inside another task. Suggest it;
the user decides.

## 5. Identity is not tone

- Sign as the user. Their name, title and company come from the task, their
  signature or what they've told you, never from voice.md examples.
- Examples in voice.md and the default voice are patterns, not facts. Never reuse
  their names, numbers, dates or situations.
- The email signature usually carries the name: don't type it unless voice.md
  says they do.

## 6. Before you hand it over

- [ ] The point is in the first two lines (email, chat) or the opening (posts, docs).
- [ ] One clear ask, and it's easy to say no to.
- [ ] Nothing said twice; no filler opener or closer.
- [ ] The register matches the channel; the shape matches the moment.
- [ ] House style applied: dashes, banned words, emoji, exclamation marks.
- [ ] Every fact, number and name came from the task, not from an example.
- [ ] It sounds like voice.md, not like an assistant.

## Files

- `references/default-voice.md` - the default voice, used until the user builds
  their own. It shows the shape and depth a good voice.md has.
- `references/voice-template.md` - the structure every voice.md follows.
- The user's `voice.md` - in their voice home, built and refreshed by
  `your-voice-builder`. Plain Markdown they can read, edit and take to any AI tool.
