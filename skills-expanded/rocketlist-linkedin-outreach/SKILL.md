---
name: rocketlist-linkedin-outreach
description: Use when writing or sending a recruiter's LinkedIn invite note, first message or follow-up to a candidate, so every line is true to the profile and the approved role facts, fits the account's limits, and passes the send guardrails before anything goes out.
---

# LinkedIn candidate outreach

Part of the Rocketlist recruiting skills. Write a short, specific LinkedIn approach to one candidate for one role that explains why this person and why this role, check it for defects, and only then let a human approve it. The approved text is the text that is sent, character for character.

## Access: manual by default, browser mode only on explicit opt-in

Default to **manual mode** unless the user explicitly asks for browser mode in this session.

**Manual mode (default).** LinkedIn interaction is manual. Never use an agent, browser automation, extension or other third-party software to read, navigate, extract from, fill fields in, or otherwise interact with LinkedIn unless LinkedIn has explicitly authorized that integration or method. The recruiter may manually provide the candidate profile, thread and account information to this skill. The skill may draft and check text from that supplied data. The recruiter manually copies or types the approved text into LinkedIn and sends it.

**Browser mode (opt-in only).** Use it only if the user explicitly asks for it in this session. Before first use, show this warning once and wait for an explicit yes:

> LinkedIn's terms do not allow third-party software or extensions that read, fill in, or automate activity on LinkedIn. Using browser mode can get your LinkedIn account restricted. Manual mode avoids this.

Until the user answers yes, read nothing and fill nothing in LinkedIn; continue in manual mode. After a yes:
- Work only in the recruiter's own logged-in LinkedIn tab in their own browser, at human pace, with the recruiter present, one candidate at a time.
- You may read the profile or conversation shown on screen and fill text into the message or invite box. The recruiter clicks Send or Invite; you never click it.
- Never use any LinkedIn API (official or unofficial), background or headless runs, any account other than the recruiter's own, or loops over many profiles or conversations.
- If no browser tool is available in this session after the yes, do not stop at "I cannot reach the browser". Describe the plan (the recruiter's own tab, one profile at a time, you only fill text, the recruiter clicks Send) and ask the recruiter to paste the profile or conversation so you can continue in manual mode now.

**Many candidates at once.** If asked to invite or message many people ("invite all 40", "the whole search page"), work one candidate at a time: prepare one draft, wait until the recruiter says it was sent or skipped, then move to the next. A short list the recruiter pasted (about 10 profiles or fewer) may be drafted together in one answer, each with its own checks. Never offer to draft a whole search page or a longer list in one go.

**Authorized integration.** If an integration explicitly authorized by LinkedIn is available, use only the actions that integration permits.

## Inputs you need

Required to draft (if one is missing, say which and stop for that candidate):

- Candidate profile (pasted by the recruiter, or read on screen in browser mode): first name, current title, current employer, headline, about text, experience entries, location.
- Role record: exact title, approved display aliases if any (otherwise the exact title is the only alias), work city, seniority level.
- Approved role facts: 1 to 4 facts the hiring team has signed off, such as scope, the problem the role solves, stack or domain, team ownership, remote setup, or compensation when approved for outreach.
- Contact direction: did this person apply on their own, or are we approaching them?

Used when supplied (if missing, still draft, and list it under "check before sending"):

- Approved company proof points. Never infer company facts.
- Sender name, plus the other sender names in the workspace.
- Workspace-wide contact record for this candidate across all Rocketlist senders, and the do-not-contact list.
- Workspace policy: any notice text it requires and the earliest contact point for it (invite note or first message), its retention rule. Do not invent a policy, a notice or a legal basis.
- Optional `approved_follow_up_text`. If absent, you draft the follow-up (Step 4).
- Account info: `invite_character_limit` (fallback 200), invites sent today and in the last 7 days, any restriction LinkedIn shows on the account.
- Current date and time, so the weekday window can be checked.

## Step 1: Hard blocks and review flags

Hard blocks apply only to **known** violations. Report the reason and do not mark the draft ready.

1. **Applicant.** The person applied for the role themselves: never cold-contact. Skip them individually, keep processing the rest, report how many were skipped.
2. **On the do-not-contact list.** Skip them.
3. **Prior contact in the workspace.** Someone in the workspace has contacted this person before: show that history (oldest first, at most the last 12 messages, reactions removed) and stop. A human may decide to send anyway only after seeing it. "No messages found" and "could not read" are different results; if the record could not be read, say so and put it on the check list; never report it as "none".

Review flag (draft anyway, status `review_required`):

4. **Level mismatch.** Map the candidate's current title to one of five levels: student or intern, entry, experienced, senior, leadership. If the candidate is two or more levels above the role (for example a director for an associate role), write the draft but mark it `review_required` with "confirm the level gap is intentional". It is never ready to paste until a human confirms. Only a clearly more senior person approached for a more junior role triggers this; a step up (for example a Partner Manager for Head of Partnerships) is never a level gap.

## Step 2: Find the link between the person and the role

Pick one concrete achievement from the profile (something the person built, changed, owns or measured) and the one approved role fact it connects to most directly. The message lives or dies on this link: it should explain why you thought of this person for this role, not prove you read the profile.

Truth rules for the achievement:
- It must come from the profile. You may lightly paraphrase (tense, word order, "our" to "your") as long as the meaning is unchanged. Numbers, product names and company names stay exactly as written.
- Restate title and employer only if nothing more concrete exists.
- "Self-employed", "Freelance", "Independent", "Various" in the employer field are not employers.
- Match keywords as whole words only ("Java" inside "JavaScript" is not a fact). A hyphen counts as a word boundary; a letter next to the keyword does not.
- No judgement or praise about the person: fit, suited, qualified, strong, excellent, ideal, perfect, impressive, amazing, great, candidate, applicant, match.

**Sensitive traits are off limits.** Never personalize from, mention or infer age, race or ethnicity, nationality, religion, disability or health, pregnancy, sexual orientation or gender identity, family or marital status, political views, union membership, or languages spoken. Do not infer any of these from names, photos, graduation years, groups, volunteering or profile text. Use professional work only.

If no achievement connects honestly to an approved role fact, write the note without a personal link rather than force one.

## Step 3: Write it like a sharp recruiter

**Invite note** shape:
`Hi <first name>, <one natural sentence linking their achievement to the role and its approved fact> <short ask>[ <policy notice>]`

- One flowing sentence carries the link: their achievement, then why it matters for this role, with the role named in natural words ("our Staff Engineer, Checkout role in Lisbon", "the team I am hiring for"). The exact approved title or alias may appear once.
- Never write "the person in this role", "we are hiring X in Y" as a stand-alone sentence after the link, or three stacked statements.
- Second person, plain words, no buzzwords, no exclamation marks, no emoji, no dash.
- Ask: short and low-commitment, the same for every level ("Up for a 15 minute call?", "Open to a short chat?"). Do not state assumptions about the person's job search.
- The first name must be a real name: strip emoji and symbols from the profile name. Strip gender suffixes such as "(m/f/d)" from the title.
- If the city is unknown, leave it out rather than guess.
- **Policy notice:** if the workspace policy is known and requires a notice at the invite, include it. If it then cannot fit the limit after Step 5, the invite is `blocked` with "required notice does not fit". Never defer a known required notice to a later message.

Examples (all data invented):

Profile: "Cut checkout latency from 900ms to 200ms by moving payment calls to an async queue." Role: Staff Engineer, Checkout, Lisbon. Approved fact: "owns checkout reliability across 3 markets".
- Good: `Hi Dana, cutting checkout latency from 900ms to 200ms is the core of our Staff Engineer, Checkout role in Lisbon, which owns reliability across 3 markets. Up for a 15 minute call?`
- Bad: `Hi Dana, you cut checkout latency from 900ms to 200ms. The person in this role owns checkout reliability across 3 markets. We are hiring Staff Engineer, Checkout in Lisbon. Up for a 15 minute call?` (stacked statements, no link, "the person in this role")

Profile: "Built the hiring dashboards our 12 recruiters use every day." Role: People Analytics Lead, remote. Approved fact: "first analytics hire in the people team".
- Good: `Hi Sam, since you built the dashboards your 12 recruiters work from every day, I thought of you for our People Analytics Lead role, the first analytics hire in the people team. Open to a short chat?`
- Bad: `Hi Sam, your impressive dashboard work makes you a great fit for People Analytics Lead! Let's talk?` (praise and judgement, no concrete link, exclamation mark)

**First message after the invite is accepted:** thank them for connecting in a few words, restate the link in one sentence if the invite had none, add one or two further approved role facts and one approved company proof point in natural sentences, the workspace notice if the known policy requires it here and it was not already given, a concrete ask for 15 minutes this week or next, and a sign-off with the sender's own name.

**Follow-up:** at most 3 sentences. If `approved_follow_up_text` is given, use it with only the first name filled in. Otherwise write a light nudge: a short reference to the earlier note that names one profile detail from it (for example "your settlement work"), one approved role fact not used before, the same ask. It goes through the same checks and approval. Not before 72 hours after the previous message; if that time is unknown, list it under "check before sending".

## Step 4: Validate the text

Validate every field after writing it. Reject and rewrite (never patch the wording just enough to pass) if it contains:
- an internal marker: a score, tier, risk flag, TODO, `{{`, `}}`, `::`, or text from an internal review note;
- a number of two or more digits that is not in the profile, the role record or the approved facts;
- a capitalised word of four or more letters (not sentence-initial, not the first name) that is not in the profile, role record, approved facts or sender name;
- the person's last name inside the body, a judgement or praise word, a sensitive trait, an emoji, or a pseudo-employer.

If the personal link cannot pass, drop it. A note without a personal link is better than one with an invented fact.

## Step 5: Check the length, never trim

- The invite limit is `invite_character_limit` if supplied, else 200. Direct messages: 2,000 unless the account reports a stricter limit.
- Count characters as UTF-16 code units (in JavaScript, `text.length`). An emoji counts as 2.
- The only allowed normalisation is before approval: CRLF to LF, trim leading and trailing whitespace. After approval the text is never touched again.
- A limit is a check, not scissors. Never cut, never add "...".
- If the invite is too long, rewrite it as a whole, still one natural sentence: drop the city, then the role fact detail, then compress the achievement. Never drop or shorten a known required notice. Recount after each rewrite.
- If it is still too long, the invite is `blocked` with "N of L characters".

## Step 6: Defect checks

Run on each field separately. Any hit blocks.

- **A. Injected company:** a company that is neither the hiring company nor an employer taken verbatim from this candidate's profile (for example a brand carried over from another client's or role's context).
- **B. Wrong work city:** a work location for the role that differs from the role record. The candidate's own city is not a claim about the role.
- **C. Wrong sender:** signed with a name other than the sender's.
- **D. Stored text is not sent text:** empty, edge whitespace, over the limit, an unresolved placeholder, or any difference between the approved text and what will be pasted or filled.
- **E. Wrong role:** a role title in the text that is not exactly the role title or an approved alias (case-insensitive). No substring matching: "Engineer" is not an alias of "Sales Engineer".
- **F. Two messages in one field:** more than one greeting at the start of a line.

Also block any role or company fact not in the approved lists.

## Step 7: Send guardrails

The recruiter sends; you prepare. In manual mode, missing information never stops you from producing a ready-to-paste draft: list it under "check before sending" instead. Hard blocks are only for known violations. A timing block (weekday window or internal cap) is never presented as optional: give the reason and the next allowed slot, and stop.

1. **Approved text is sent text.** Hand over or fill exactly the approved characters. If the recruiter edits it, it needs re-approval and a recheck.
2. **Platform restriction known.** If LinkedIn shows a restriction or warning on the account, stop preparing invites and tell the recruiter. Never switch accounts or change timing to get around it. If you do not know, add "confirm no LinkedIn restriction on your account" to the check list.
3. **Rocketlist internal caps.** 20 invites per day and 100 per rolling 7 days per recruiter account, counted from the recruiter's own record. These are Rocketlist's own conservative caps, not published platform limits; any stricter platform or workspace limit applies instead. Known counts at or over a cap: blocked, park for the next free day. Unknown counts: check list.
4. **Weekday window in the recipient's time zone.** Monday to Friday, 10:00 to 18:00 local time (18:00 is outside), resolved from the candidate's location, then the role's location, then the workspace default. If the current time is known and outside the window: blocked for now, and state the exact reopen day and time in the recipient's zone (for example "Wednesday 10:00 Berlin"). A weekend or window block is not a choice: never offer to send anyway, never ask the recruiter to pick between waiting and sending manually now ("your call: wait or send manually"). State the next allowed slot and stop. Use the current day and time exactly as supplied; do not second-guess it. If the time or time zone is unknown: check list, stating the window.
5. **Replies are different.** A reply to someone who has just written is not held to the window.
6. **Recheck** the workspace contact record and do-not-contact list just before sending if they were supplied; if not, they are on the check list.
7. **Human pace, one at a time.** Never click Send or Invite, never loop over a list in LinkedIn.

## Output format

Lead with the text, then the essentials:

```
candidate: <first name> (<role title>)
status: ready_to_paste | review_required | blocked
invite_note (<N>/<limit>): <text>
first_message (<N>): <text, if requested>
follow_up (<N>): <text, if requested>
check_before_sending: <short list of what was not supplied, e.g. "do-not-contact list", "workspace notice requirement", "send between 10:00 and 18:00 Mon to Fri, Berlin time", "no LinkedIn restriction on your account"; or none>
reason: <for blocked or review_required only>
sources: link from "<profile sentence>"; role fact "<approved fact>"
defects: <A to F hits, or none>
```

Never present a blocked or review_required result as ready. Never claim the message will get a reply.
