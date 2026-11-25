---
name: rfi-query-tracker
description: Tracks open requests for information and technical queries: who asked, who owes the answer, how long it has been open and what it is holding up. Use when the user asks what RFIs are open, which queries are unanswered, what is blocked waiting on an answer, or to prepare the RFI log before a progress meeting.
---

# RFI and Query Tracker

Shows which open questions are actually blocking work, rather than which are merely old.

## Inputs
- **Email** and Teams traffic for queries and their answers
- **Enterprise Search** for the RFI log, if one exists
- `references/config.md` for the RFI numbering pattern and response windows by discipline

## Procedure
1. **Find queries** by the numbering pattern and the vocabulary: "RFI", "query", "clarification
   required", "please confirm", "awaiting your response".
2. **For each, extract**: reference, raised by, raised on, directed to, the question in one line,
   the response window from config, whether answered, and the source link.
3. **Determine what it blocks**, from the query text itself only. If it does not say, write
   "impact not stated". 🔴 **Never infer an impact.** An invented blocker reorders a project's
   priorities on a guess, and this is the single most harmful thing this skill could do.
4. **Classify**: `Open, within window`, `Open, overdue`, `Answered`, `Answered but disputed`.
5. **Rank** by stated impact first, then by age. Not by age alone: a six-week query blocking
   nothing sits below a four-day query blocking a pour.
6. **Write** the log, impact-bearing items first.

## Output
| Ref | Question | Raised by | Directed to | Raised | Due | Status | Blocks | Source |

Then: items with a stated blocker, overdue with no stated impact, and answered-but-disputed.

## Definition of done
Every open query has an owner and a status, and every "blocks" cell is either quoted from the
query or says "impact not stated".

**An empty log is a good day on a project.** Say so.

## When there is no data
- Nothing matching the pattern: state the pattern.
- A query with no addressee: mark directed-to UNKNOWN rather than assigning it.
- An answer that raises a new question: create the new row and link it to the old.

## Boundaries
- **Never answer a query on anyone's behalf, and never draft a technical answer.** This tracks;
  it does not opine on design, method or compliance.
- **Never chase externally.** Drafts go to the user.
- Never infer what a query blocks.
- 🔴 Nothing here touches permits, method statements, safety authorisation or inspection sign-off.
  Those are decisions people make in the systems that record them.

## Self-check
- Is every "blocks" value quoted or explicitly absent?
- Did I rank by stated impact before age?
- Did I avoid drafting any technical answer?
