---
name: business-decision-frameworks
description: Reference library of named business frameworks: prioritization (MoSCoW, RICE, OKRs, Kano, Value vs Effort, Opportunity Solution Tree), product decision-making (CIRCLES), roadmap formats (Now/Next/Later, Hybrid, Strategic, Gantt, OKR, Dashboard), argument/slide storytelling (Minto Pyramid), leadership self-assessment (LEADERSHIP model), messaging/communication frameworks (AIDA, PAS, FAB, STAR, SMART, SWOT), leadership narrative storytelling frameworks (Pixar's Story Spine, The Golden Circle, Duarte's Sparkline, The Hero's Journey, And-But-Therefore, What/So-What/Now-What), and fast-tempo decision-making frameworks (Eisenhower Matrix, OODA Loop, Five Whys root-cause analysis). Use when the user asks to prioritize a backlog/roadmap, score or rank initiatives, choose a roadmap display format, structure a product decision or interview answer, build a persuasive slide, assess leadership competencies, write ad/sales copy, structure an interview answer, set a goal, run a strategic SWOT scan, triage a task list by urgency/importance, make a fast decision under changing conditions, drill down to a root cause, lead a team through change, or make an announcement/vision talk/debrief memorable — even unnamed (e.g. "what should we build first", "what roadmap format should I use", "make this slide land better", "help me write this ad", "how do I announce this change well", "why does this keep happening"). Also trigger on direct framework-name references or requests to compare methods.
---

# Business Decision Frameworks

A reference library of four named-framework domains extracted from business/product-management source material. Each domain is a separate reference file — load only the one relevant to the request, not all four.

## Important caveat on source quality

**!! [Certain]** This content originates from LinkedIn-style infographics (Paul Evans, Ronnie Kinsey, Jay Mount) and similar condensed-marketing sources (Hustle Badger) — not primary sources or peer-reviewed methodology. Treat every framework below as a **starting scaffold**, not a definitive spec:

- MoSCoW, RICE, Kano, and the Opportunity Solution Tree are legitimate, widely-used PM frameworks — the summaries here are accurate but shallow. For rigor (e.g. exact RICE scoring formula, Kano survey methodology, Teresa Torres' actual OST rules), verify against primary sources before using in a high-stakes deliverable (board deck, investor material).
- CIRCLES is a PM-interview mnemonic (Lewis C. Lin), not an industry-standard framework — treat it as an answer-structuring tool, not a strategic methodology.
- The six roadmap formats in `references/roadmap-format-selector.md` are a vocabulary/trade-off checklist, not a standardized taxonomy — they're presented as mutually exclusive when most orgs actually run two formats of the same plan for two audiences at once. See that file's own caveat section before using it for a formal planning process.
- The "LEADERSHIP" acronym in `references/leadership-cheatsheet.md` is the weakest of the five: a mnemonic word-list with one line per letter, no underlying model, no citations. Use it only as a talking-points checklist, never as the basis of a leadership development plan or formal competency framework. If the user needs the latter, push back and suggest a real model (Situational Leadership, Kouzes & Posner's Five Practices, or the Zenger-Folkman competency model) instead.

## Routing

| User need | Load |
|---|---|
| Prioritizing a backlog, roadmap, or feature list; scoring initiatives; "what should we build first" | `references/prioritization-frameworks.md` |
| Choosing or designing a roadmap *display format* (Now/Next/Later, Hybrid, Strategic, Gantt, OKR, Dashboard); "what roadmap format should I use", "how do I show this to the board" | `references/roadmap-format-selector.md` |
| Structuring a product decision, framing a PM interview answer, "how do I think through this problem" | `references/circles-framework.md` |
| Building a persuasive slide, exec summary, or narrative; "make this land better"; structuring a deck | `references/storytelling-pyramid.md` |
| Leadership self-assessment, competency talking points, team culture language | `references/leadership-cheatsheet.md` (see caveat above — offer a stronger alternative if this is for formal use) |
| Writing ad/sales/email copy, structuring an interview or case-study answer, setting a SMART goal, running a quick SWOT scan | `references/messaging-frameworks.md` |
| Leading a team through change, a vision/values talk, a team debrief, or making an announcement memorable rather than a bulleted list | `references/leadership-storytelling-frameworks.md` |
| Triaging a task list by urgency/importance, making a fast decision under changing conditions (competitive move, incident response), or drilling down from a symptom to a root cause | `references/decision-making-frameworks.md` |

## How to use these references

1. Identify which domain(s) the request touches — usually one, sometimes two (e.g. prioritizing AND presenting the result).
2. Load only the relevant reference file(s).
3. Apply the framework's "How To Use" steps to the user's actual content — don't just recite the framework back.
4. If the user is choosing *between* frameworks (e.g. "MoSCoW or RICE?"), use the decision guidance at the top of `prioritization-frameworks.md` rather than presenting all six as equally applicable — they solve different problems and picking the wrong one for the situation is a common, correctable mistake.
5. For prioritization work specifically, check whether `product-strategy-session` (if installed) is a better fit — that skill runs the full positioning → discovery → roadmap process; this skill is the lighter-weight reference for a single scoring/ranking decision.

## Related skills in this repo

- **quarterly-okr-architect**: Once initiatives are prioritized here, feed the top ones into that skill to build a full quarterly goal architecture around them.
- **content-strategy**: Use the prioritization frameworks (RICE, Value vs Effort) to rank topic/content ideas before building an editorial calendar.
- **business-intelligence-report** / **ceo-reporting-skill**: The storytelling pyramid (Minto) reference here pairs with those skills when a report needs a persuasive executive narrative, not just a data table.
- **growth-operating-framework**: Step 6 of that framework ("what works best, scalable, replicable") is a prioritization decision — apply RICE/Value-vs-Effort here to rank growth channels/experiments.
- **outreach-execution**: AIDA/PAS/FAB from `references/messaging-frameworks.md` structure the copy; that skill supplies the channel-specific length/tone constraints.
- **resume-prompt-kit**: STAR (same reference file) is the standard structure for resume experience bullets and interview prep.
