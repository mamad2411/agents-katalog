---
name: internal-expert-finder
description: Finds who inside the organization has already done a given kind of work, with the evidence for each name, and drafts the introduction. Strictly internal, never external sourcing. Use when the user asks who has done this before, who knows about a topic, who to ask internally, or who worked on a similar project.
---

# Internal Expert Finder

Answers "who here has already solved this", with the evidence, before anyone reinvents it.

🔴 **Internal only.** This skill never sources candidates externally, never reads professional
networks, and never touches recruitment. That boundary is the whole design: it is the portable
half of an external-sourcing pattern that does not belong inside a tenant.

## Inputs
- **Enterprise Search** across documents, sites and shared files
- **Meetings** for who presented or led on a topic
- `references/config.md` for the evidence bar and groups to exclude

## Procedure
1. **Turn the request into search terms**, including the vocabulary the organization actually
   uses, not only the user's phrasing. Say which terms you searched.
2. **Find artifacts first, people second.** A person is a candidate because a document, a deck, a
   decision or a meeting ties them to the work. Never nominate someone from a job title alone.
3. **For each candidate, record**: name, what ties them to the topic, the single strongest piece
   of evidence with a link, how recent it is, and whether the tie is direct (they authored or led)
   or indirect (they were present, or were copied).
4. **Rank** by directness, then recency. A direct tie from two years ago outranks an indirect tie
   from last month.
5. **Exclude** anyone in a config-excluded group.
6. **Draft one introduction** to the top candidate, from the user, stating the question.

## Output
| Person | Tie | Direct or indirect | Most recent evidence | Date | Source |

Then: who to ask first and why, who to ask if they are unavailable, and what you searched.

## Definition of done
Every name carries a link, every tie is labelled direct or indirect, and the search terms used
are stated so the user can judge coverage.

**Finding nobody is a real and useful answer.** Say "no internal evidence found, here is what I
searched" and stop. That tells the user this is genuinely new ground, which is worth knowing. Do
not fall back to nominating senior people by title.

## When there is no data
- Nothing found: report the terms searched so the user can add vocabulary.
- Only indirect ties: say so plainly rather than promoting them to direct.
- Evidence is all old: say the organization's knowledge here may have left with people.

## Boundaries
- **Never external.** No sourcing, no candidates, no professional networks, no recruitment use.
- Never infer expertise from a job title, a team name or a reporting line.
- Never surface a document the user cannot already access. Enterprise Search respects permissions
  and this skill must not try to work around that.
- Never characterize someone's performance or suitability. Report the tie and the evidence only.
- Draft the introduction; do not send it.

## Self-check
- Is every nomination evidenced by an artifact, not a title?
- Did I state the search terms?
- If nothing was found, did I say so instead of guessing?
