---
name: job-hunt-cheat-code
description: Turn a job posting into a tailored resume and an outreach plan to actually land the role. Use whenever the user shares a job posting URL or pasted job description and wants to pursue it - even if they only drop a link with no other instructions, or say things like "tailor my resume for this," "how would I land this job," "help me go after this role," or "who should I talk to at [company]." Fetches and decodes the job, gives an honest fit assessment, rewrites the bundled baseline resume truthfully (never inventing experience), and builds a sequenced outreach plan with real, verified people to contact plus drafted messages in the user's voice - because applying through job boards alone almost never works. Do NOT use for general resume feedback with no target job in mind, or for hiring-side tasks like screening candidates.
license: MIT
metadata:
  author: "Matt Paige"
  source: "https://github.com/mattp68/job-hunt-cheat-code"
  source_commit: "d36a9c0336b63348f0d8768b0d2f6af1edd8e427 (2026-07-20)"
  installed_by: "Claude Code (Fable 5), 2026-07-20, per Skill Install Security Review SOP"
---

# Job Hunt Cheat Code

> **Baza guard header (local edit, 2026-07-20).** This copy is adapted for Kamilla.
> 1. Drafts only. Kamilla sends all applications and outreach herself; never send, post, or submit anything on her behalf.
> 2. Before writing any resume, profile, or outreach text, read the "Hard content rules" section at the top of `references/candidate-profile.md` and obey it without exception.
> 3. No em dashes in any output (global rule, 2026-06-12).
> 4. Any fact only Kamilla can confirm goes in as a `[KAMILLA: ...]` slot, never invented. Voice: plain, specific, no self-mythologizing.
> 5. The author-voice details in `references/outreach-playbook.md` have been replaced with Kamilla's; if any "matt"-style remnant surfaces, it is upstream residue, not her voice.
> 6. Before drafting ANY free-text application answer ("why us", "what motivated you"), cover letter, or outreach message, read and apply `../humanize-application-writing/SKILL.md` (local edit, 2026-08-06). Its Step 0 (extract her real reason before drafting) is mandatory for motivation questions.

This skill takes one input - a job posting - and produces the full attack plan for landing it: an honest fit assessment, a truthfully tailored resume, and a sequenced outreach strategy that treats the job-board application as table stakes rather than the plan. The premise: a resume in an ATS pile is a lottery ticket; a resume in a human's hands, delivered by someone they've already heard from, is a candidate.

The "cheat code" is not cheating. It's doing the two things the other 800 applicants won't: telling the truth with precision, and talking to actual humans instead of a submit button.

Two failure modes would make this skill worse than useless, so hold these as hard rules throughout:

1. **Never fabricate resume content.** Every claim in the tailored resume must be traceable to the baseline resume, the candidate profile reference, or something the user tells you in this conversation. A resume that gets an interview it can't survive wastes everyone's time and burns the candidate's reputation.
2. **Never invent people.** Every named person in the outreach plan must be verified by search results in this session. A message addressed to a hiring manager who doesn't exist (or left the company two years ago) is instantly disqualifying. When you can't verify a name, give role-based targeting with the exact searches the user should run instead.

## Inputs

- **The job**: usually a URL, sometimes a pasted description. See "Getting the posting" below.
- **The baseline resume**: `references/baseline-resume.md` is the source of truth for the candidate's history. On first use, copy `references/baseline-resume.template.md` to `references/baseline-resume.md` and fill it in with the candidate's real resume (or have them paste/upload one). Exception: if the user uploaded a newer resume in this conversation, prefer that and mention you're using it.
- **Extra ammunition**: `references/candidate-profile.md` - assets beyond the resume (audience, platform, shipped work, ecosystem relationships). On first use, copy `references/candidate-profile.template.md` and fill it in. Read it before both the resume rewrite and the outreach plan; it changes what's possible. If the candidate has no such file yet, ask a few questions to build one, then save it.
- **The angles**: `references/resume-angles.md` - five template specs (AI/GTM, Startup Ops, Community/Education, Events, Sport). Pick the angle in Step 2 and render Step 3 from it. Angles vary emphasis ONLY; the Integrity Core (company, title, dates, location) is frozen verbatim from the baseline.
- **The playbook**: `references/outreach-playbook.md` - read it before drafting the strategy.

### Getting the posting

Try `web_fetch` on the URL first. LinkedIn job URLs and some ATS pages sit behind login walls and will fail - that's expected, not a dead end:

1. Web-search the role title + company name; the same posting usually exists on the company's careers page, Greenhouse/Lever/Ashby, or an aggregator that fetches cleanly.
2. If you can only find partial text, work with it and say so.
3. If nothing fetches, ask the user to paste the description. Don't guess at requirements from the job title alone.

While you're there, also skim the company itself (recent news, funding, product launches, strategy shifts). This research feeds both the resume angle and the outreach plan, so do it once, early.

## Step 0 - The question gate

Ask clarifying questions **only if the answer would materially change positioning** - for example: which track to lead with when the role could be read two ways (operator vs. builder vs. creator), an unexplained constraint (location, comp band, timing), or whether this is a lateral move vs. a deliberate stretch. Cap it at 4 questions, ask them once, together.

Never stall waiting for metrics. If a number would strengthen a bullet, write `[METRIC NEEDED: what to measure]` and move on. If nothing would materially change positioning, don't ask anything - proceed and flag your assumptions inline.

## Step 1 - Decode the job

Classify every requirement in the posting into four tiers, because resume space should be spent proportionally:

- **Required** - explicitly stated must-haves, repeated themes, anything in the first three bullets
- **Strongly preferred** - "ideal candidate" language, seniority signals, domain specifics
- **Supporting** - nice-to-haves, tools, adjacent skills
- **Boilerplate** - culture-speak that appears in every posting; spend zero space on it

Also read between the lines: what problem is this hire solving? A "VP of Marketing" posting that mentions pipeline three times is a demand-gen problem wearing a brand title. Name the real job - it sharpens everything downstream.

## Step 2 - The honest fit call

Before touching the resume, call the fit: **Strong / Moderate / Stretch**, with the driving factors and the single biggest objection an interviewer will raise. Then answer honestly: is that objection something resume tailoring can fix, or is it a real gap (experience, portfolio, role selection)? If it's the latter, say so plainly and name what would actually close it. The user has explicitly asked for unvarnished assessments - a diplomatic fit call is a disservice.

This comes first because it sets the tailoring strategy: a Strong fit resume plays it straight; a Stretch fit resume needs a deliberate bridge narrative (and the outreach plan has to carry more weight).

## Step 3 - Tailor the resume

**Evidence rules (non-negotiable):**

- Every claim traceable to the baseline resume, candidate profile, or the user's answers in this session.
- Preserve the original level of ownership, scope, and certainty. Never upgrade "assisted" to "led," "supported sales" to "drove revenue," "contributed to" to "built."
- Use exact JD terminology only where the record shows real evidence for it. Never imply proficiency from an adjacent skill - "ran analytics in SQL" does not become "data engineering."
- Quantify where credible and decision-relevant; use `[METRIC NEEDED: …]` placeholders rather than forcing numbers onto qualitative wins.

**Prioritization rules** - cutting and reordering matter more than rewording:

- 2 pages max. 3–5 bullets for recent/relevant roles; 1–2 or none for older ones; compress or drop what doesn't serve this job.
- Lead each role with the bullet that maps to a Required-tier item.
- The executive profile / summary is rewritten per-job - it's the 7-second read, and it should mirror the role's actual problem (from Step 1) in the candidate's real experience.
- The candidate profile reference may contain assets the baseline resume undersells (audience size, shipped products, partner status). Pull them in when they map to a Required or Strongly-preferred item - with the profile's own caveats about confirming current numbers.

**Style rules:**

- No claim that could apply to any candidate. Kill inflated corporate language and repeated verbs (spearheaded, leveraged, results-driven, passionate).
- ATS-safe: single column, standard headings, no tables, no text boxes, no graphics, no critical info in headers/footers.
- Reverse-chronological by default.

**Output:** produce the resume as a `.docx` file. If a docx-creation skill is available in the environment, read its SKILL.md first and follow it. Alongside the file, give the user in chat:

1. **Top fixes** - the 3–5 highest-impact changes, including what you cut and why
2. **Keyword table** - `term | tier | present/missing | where placed, or why honestly omitted`

The keyword table's "why honestly omitted" column is where integrity lives: if the JD wants Kubernetes and the record has none, the table says so instead of the resume lying.

## Step 4 - The game plan

Read `references/outreach-playbook.md`, then build a sequenced plan. The shape:

1. **The targets** - 3–5 real people, each verified via search this session (name, title, why them, and the evidence you found). Where verification fails, give the role to find plus the exact LinkedIn/Google searches to find them. Never present an unverified name as fact, and never present a guessed email address as real - flag patterns as patterns to be verified.
2. **The sequence** - day-by-day plays over ~2 weeks, starting with the application itself (table stakes, day 0) and escalating through connection, value-add, and proof-of-work.
3. **The messages** - copy-ready drafts for each play: LinkedIn connection note (under 300 characters - hard platform limit), follow-up DM, email. If a personal-voice skill (e.g. `my-voice`) is available in the environment, read it before drafting; otherwise use the voice section of the playbook. These are drafts for the user to send - never send anything yourself.
4. **The asymmetric plays** - the candidate profile lists assets most candidates don't have (podcast, audience, shipped products). The playbook covers when each is worth deploying and when it's cringe. Recommend at most one or two per campaign.
5. **Cover letter** - only if the application requires one or the situation earns it (career pivot, Stretch fit, a named human will read it). Default is a short, specific note; the playbook has the format. Skip it entirely for most Strong-fit applications where outreach is doing the work.

## Output contract

Deliver, in this order:

1. **Fit call** (Strong/Moderate/Stretch, driving factors, biggest objection, whether tailoring can fix it)
2. **Tailored resume** (.docx file) + top fixes + keyword table
3. **Game plan** (targets → sequence → messages, with any asymmetric play and cover letter if warranted)

Keep the chat portion skimmable - the user should be able to act on this within the hour. Prose over bullet-spam, but messages formatted as clean copy-paste blocks. End with the single next action to take today, not a menu.
