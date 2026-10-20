---
name: think-hard
description: Deep, critical pass on a hard question before answering. Use for 'think hard/deeply/seriously', 'ultrathink'. Answers; does not build.
---

# Think Hard

Keith says this a lot. He says it when the last answer was shallow, or when he can see the
question is hard enough that the first answer will be wrong.

He is asking for a **different answer**, not a longer one.

## The one rule

Deep thinking, short output. The work goes into getting the answer right. The reply stays
under a screen. Length is not depth. A long answer with no falsifier in it is still shallow.

## The pass

Run all seven. Skip a step only when it genuinely does not apply, and say which one.

**1. Fix the question.**
Write in one line what is actually being asked, and what decision it feeds. Then check the
question itself. The biggest win in deep thinking is noticing the question is wrong. If it
is, say so in one line and answer the better one as well. Never instead.

**2. Go and look.**
Name the two to four sources that would settle it: files, data, `git log`, tests, docs, the
web. Open them. Reasoning about a file you have not read is the shallow answer wearing a
suit. Read them in one parallel batch.

**3. Three answers, not one.**
Force at least three candidate answers that cannot all be true. Include one you do not like.
Include one that says the premise is wrong: nothing is happening here, the effect is noise,
the thing should not exist. Your first answer is the pattern-match. It belongs on the list,
not at the end of it.

**4. Kill your favourite.**
For the leading candidate, write the single piece of evidence that would prove it wrong. Then
go looking for *that*, not for support. If you cannot state a falsifier, you do not have a
finding. You have a vibe.

**5. Name the load-bearing assumption.**
Which single assumption, if false, flips the answer? State it. Say whether you checked it. If
you did not check it, the answer is conditional and must be labelled that way.

**6. Say the unwelcome thing.**
The deep answer usually differs from the shallow one because it is less comfortable. Common
shapes: the result is noise, the number was measured wrong, the real problem is upstream of
what he asked about, this should not be built at all, or "I do not know, and here is exactly
what it takes to know."

**7. Commit.**
One verdict, one confidence level. Depth earns the right to be decisive. It does not license
a menu of options.

## Output format

```
Question: <what is really being asked. Name the reframe if there is one.>
Answer:   <the verdict, one or two lines>
Why:      <the two or three things that decide it, each with its source: file:line, command, URL>
Counter:  <the strongest case against, and why it loses. Or that it wins.>
Assumes:  <the one assumption that would flip this, and whether it was checked>
Confidence: <high | medium | low> - <the one check that would move it most>
```

The block is the whole reply and fits in about 20 lines. A skipped step or a source you could
not open goes in Assumes. When several checks would help, name only the one that would move the
answer most; listing two is a menu. Then stop: nothing outside the six fields, no summary of
what he just read, no offer to build.

## Rules

- **Answer, do not build.** This is a question. Wait for "go" before writing code.
- **Nothing from memory.** Every load-bearing fact comes from a source read this turn, cited
  so he can re-run it. An uncited number is a fabrication.
- **"I don't know" is a real answer** when it names the specific thing needed to know. It is
  never a hedge.
- **Do the thinking yourself.** Sub-agents may fetch and read in parallel. Synthesis stays
  here. A deep answer assembled from summaries is a shallow answer with extra steps.
- **If depth confirms the shallow answer, say so.** "Same conclusion, here is the evidence"
  is a result. Do not manufacture a contrarian take to look deep.

## Not this skill

| Ask | Skill |
|---|---|
| Attack work that already exists | `/grill-me` |
| Critique a finished artifact | `/critique` |
| Find the cause of a specific bug | `/investigate`, `/systematic-debugging` |
| Is it done and correct? | `/all-done` |
| Big job, spawn agents, use everything | `/full-power` |
