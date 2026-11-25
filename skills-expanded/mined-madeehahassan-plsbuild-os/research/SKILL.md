---
name: Research
description: Find out if you're building the right thing, for the right person. Use when you don't know who your user is yet, when you want to run your first user interview, or when you're trying to turn feedback into real signal. Adapts to Claude Code, claude.ai, and Cowork.
---

# /research

Use this when you want to understand your user — whether you've never spoken to one yet, or you've done twenty calls and need to make sense of what you heard.

The goal is always the same: find out what people actually do and feel, not whether they like your idea.

---

## Which surface are you on?

**Claude Code**
Save interview scripts, notes, and analyses to files in the project repo (e.g. `research/2026-04-14-user-interview-alex.md`). Read existing notes before pattern-matching across interviews.

**claude.ai chat**
Return scripts, analyses, and pattern summaries inline as copy-ready markdown. Tell the user where to save each one. When analyzing, ask the user to paste their raw notes — you can't read their files.

**Cowork**
Same as Code — save to the workspace folder. Read existing notes before analyzing new ones.

Either way: quote users in their exact words. Never paraphrase into corporate-speak.

---

## Stage 0: Before you talk to anyone

Most first-time founders skip this and jump straight to building. Don't. Spend one hour here first — it saves weeks of building the wrong thing.

**Who is this actually for?**

Write down one sentence: "This is for [type of person] who [has this specific problem]."

Be as specific as possible. Not "busy professionals." Try "freelance designers who lose track of which clients owe them money." The narrower it is, the easier everything else gets.

If you can't write that sentence yet, that's your first research goal: figure out who the person is before you build anything for them.

**Can you name five real humans who fit that description?**

Not in theory. Actual people. People you could message today. If yes — message one of them this week. If no — that's your first problem to solve.

Where to find your first user if you have no one:
- Post in a relevant subreddit or community and ask if anyone has the problem (don't pitch — just ask)
- Search X or LinkedIn for people complaining about the exact thing you're solving
- Ask in your own network: "do you know anyone who struggles with X?"
- Look for communities where your target user already hangs out and join them

You only need one person to start. One honest conversation is worth more than a hundred assumptions.

---

## Before the interview

**Write the script. Then cut half of it.**

Good interviews are short and narrow. One topic. Five open questions max. Everything else is a follow-up in the moment.

**Only ask about past behavior, not future intent.**

Wrong: "Would you use this?" They'll say yes to be nice.
Right: "The last time you had this problem, what did you do?"

Past behavior is evidence. Future intent is flattery.

**Do not pitch. At all.**

The moment you describe your solution, the interview is over. They start optimising their answers to make you feel good. Save the pitch for the end, after you've already gotten everything you need.

---

## Questions that actually work

- "Tell me about the last time you [did the thing my product helps with]."
- "Walk me through what you did, step by step."
- "What was the hardest part of that?"
- "What did you try before that?"
- "What did you wish existed?"
- "How much time did it take?"
- "How much did it cost you to solve, in time or money?"

Follow up with "why?" and "tell me more about that." Stay quiet. Let them fill the silence. Silence is where the real answers come from.

---

## Traps to catch

**Validation theater.** They are being polite. Your job is to make it safe for them to say no. Try: "A few people told me they wouldn't pay for this. Where do you land?"

**Solution-not-problem.** They jump to features they think they want. Bring them back to the actual moment. "Before we talk about how, tell me more about the last time this became a real problem."

**Leading questions.** Anything starting with "Would you..." or "Do you think..." Rewrite those. Ask about what they have already done instead.

**Nodding without listening.** Stop thinking about your next question. Write their words down verbatim. You will use them later.

**The friend problem.** If your first five users are people who like you, their feedback is biased. You need people who don't care about your feelings. A stranger who tells you it's confusing is more valuable than a friend who says it's great.

---

## After the interview

Do not trust your memory. Within 30 minutes of the call:

1. Write down 3 direct quotes, in their exact words.
2. Write down any surprises — things you did not expect them to say.
3. Write down what they did not say. If you expected them to mention something and they didn't, that is a signal.
4. Write down a one-sentence summary of their pain.

After 5 interviews, look for patterns. The same words, the same workflow, the same pain described differently. That is real signal. Anything only one person said is noise until another person independently says it too.

---

## Using Claude to analyse your notes

After your interviews, paste your raw notes and ask Claude:

"Here are my notes from [X] user interviews. What patterns do you see? What did multiple people say independently? What surprised me should I pay attention to?"

Then ask: "Based on this, what should I stop building, and what should I prioritise?"

Claude will find patterns faster than you will. But it can only work with what you actually heard — not what you hoped to hear. Be honest in your notes.

---

Return a script when asked for one. Return a short analysis after an interview, quoting the user directly. No filler. No "here is what I learned in general." Name the specific human and what they actually said.
