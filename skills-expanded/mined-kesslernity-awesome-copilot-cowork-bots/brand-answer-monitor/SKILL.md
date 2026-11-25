---
name: brand-answer-monitor
description: Tracks how the open web describes the brand on the questions that matter, and builds a weekly trend sheet of what a research tool finds when it looks the brand up. Use when the user asks how the brand is being described, what sources say about the company, to track brand visibility, or to see whether published positioning is being picked up.
---

# Brand Answer Monitor

Tracks what a researcher finds when they look you up, week over week.

🔴 **Read this before using it.** The original idea was to track the brand's position inside
ChatGPT, Gemini and Perplexity answers. **This skill does not do that, and cannot.** Those are
competitor products behind their own interfaces, not open-web sources, and nothing in Cowork's
documentation establishes that Deep Research can query them. Shipping an "AEO tracker" on that
assumption would be inventing a capability.

What this does instead is honest and still useful: it records **what Deep Research surfaces about
the brand on a fixed set of questions**, week over week, so movement in sources and framing is
visible. Treat it as a proxy for what a research tool sees, not as a measurement of any specific
assistant's answer. If you later confirm a way to query those assistants, this skill's trend sheet
is the right shape to carry it.

## Inputs
- **Deep Research**, over the fixed question set in config
- `references/config.md` for the brand, the questions and the competitor set
- The prior weeks' sheet, for the trend

## Procedure
1. **Ask the same questions every week, unchanged.** A question edited mid-series breaks the
   trend, so changed questions start a new series and the sheet says so.
2. **For each question, record**: whether the brand appeared, in what position among named
   organizations, which sources were cited, and the framing in one quoted phrase.
3. **Record competitor appearances** on the same questions, since relative presence is the signal.
4. **Append to the trend sheet.** Never overwrite history.
5. **Report only the deltas** against last week, plus a four-week direction per question.

## Output
Appended to `/Documents/Cowork/output/brand-answers.xlsx`:

| Week | Question | Brand appeared | Position | Sources cited | Framing | Competitors named |

Then: what moved since last week, the four-week direction, and new sources appearing for the
first time, which is usually the most actionable column.

## Definition of done
Every configured question is asked unchanged, the sheet is appended rather than replaced, and the
report covers deltas only.

**A flat week is normal.** One line: "no movement across N questions." Visibility changes slowly
and a monitor that finds drama weekly is measuring its own noise.

## When there is no data
- The brand appears nowhere: that is a finding, recorded as a zero, not an error.
- Deep Research returns different sources run to run: note the instability. **Do not average it
  away**: an unstable result is itself the finding.
- A question's wording had to change: start a new series, say so, do not splice.

## Boundaries
- **Never claim to show what ChatGPT, Copilot or any other assistant answers.** This reports
  what the open web says about the brand, through Deep Research. It cannot see inside
  anyone else's assistant and must never imply that it can.
- Never act on the findings: no content is published, no page is edited, nothing is sent.
- Never record a competitor's non-public information.
- **Draft only.**

## Self-check
- Did I ask the questions exactly as configured?
- Did I append rather than overwrite?
- Did I avoid claiming anything about a specific assistant's answers?
