---
name: contact-email
description: Write and check academic contact emails for job and fellowship applications, four kinds with one rule set, a first-contact inquiry to a prospective postdoc host or PI, a request asking someone to be the host, sponsor, or mentor for a fellowship (Humboldt, MSCA, institute fellowships that need a host letter or workplace confirmation), a request to a referee for a recommendation letter with the materials they need, and a follow-up or reminder. Rules come from an evidence-based guideline compiled from funders (Humboldt Foundation, MSCA), university postdoc and career offices (Waterloo, Caltech, Stanford, MIT, UW, Yale, Pitt, Auburn, Oregon), the ASBMB and the National Postdoctoral Association, and Nature. Korean working draft, user revision, English final; `scripts/ce_check.py` checks subject line, length, the ask, salutation, attachments, dates, apologies, hedges, dashes, and wrong names. Drafts only, never sends. Use when the user mentions 컨택 메일, contact mail, 교수에게 첫 연락, 호스트·멘토 요청, 추천서 요청 메일, reminder, follow-up, cold email to a PI, or asking a host for a fellowship. Use `cover-letter` for the application letter itself and `research-statement` for the proposal.
---

# Contact Email

A contact email asks one person for one thing they can say yes to quickly. Everything else (fit, evidence, attachments) exists to make that yes easy.

## When to use

| Kind | Typical ask |
|---|---|
| Host inquiry | "Do you anticipate a postdoc opening, or could we talk about fit?" |
| Sponsor or mentor request | "Would you host or mentor my application to [scheme], including [letter / workplace confirmation / joint proposal] by [date]?" |
| Referee request | "Could you write a strong letter for [post], due [date] via [route]?" plus a materials package |
| Follow-up or reminder | Restate the same ask in the same thread, with the date |

Not for application cover letters (`cover-letter`), proposals (`research-statement`), or replies in an ongoing exchange that need no new ask.

## Inputs to confirm

Ask only what files and the call cannot answer.
- Recipient: name, title, current affiliation (verify on an official page; people move), and any posted contact instructions on their group page.
- The concrete ask and its deadline, including what the scheme requires from them (letter, statement, workplace confirmation, joint proposal, form) and the submission route.
- The connection: one specific paper, project, or resource of theirs, and how the applicant's work meets it. Any real prior contact (met at, referred by).
- The applicant's one or two strongest relevant results, current position, PhD date, availability, funding status.
- Attachments: CV, and only what the ask needs (one-page project summary for sponsors; full package for referees).
- Name form the applicant uses (referees and portals must match it).

## Workflow

1. **Read the call or scheme** for what the contact must deliver and by when. Work backwards: the email must reach them early enough for a reply, a conversation, and their own writing time.
2. **Verify the recipient** (title, affiliation, eligibility as host, posted instructions). For fellowships check host requirements (e.g. host employed through the whole period, a separate statement per host, not the doctoral advisor).
3. **Draft in Korean** as `<recipient>_<kind>_ko_vN.md`, with the English subject line already decided, plus `_guide/<recipient>_notes_vN.md` mapping each fact to its source. Unknowns stay as `[확인 필요: ...]`.
4. **Check** with `python3 scripts/ce_check.py DRAFT.md --kind host|sponsor|referee|followup` and the checklist. Show the user the draft and the open questions.
5. **Translate after approval**, run the check on the English file with `--strict`, and hand the text to the user. The user sends it.
6. **Plan the follow-up**: note the date to follow up (see timing below) and what to resend; for referees, the reminder date.

## Core rules

Short form; quotes and sources in `references/evidence.md`.

1. **Ask first, clearly, once.** State who you are and what you want in the first short paragraph; background comes after. One main ask per email, phrased as a direct question the recipient can answer.
2. **Short, structured, formal.** About 150 to 250 words for an inquiry (some advice goes as low as four sentences); clarity beats brevity when the ask needs detail. Short paragraphs, numbered items for multiple requests. "Dear Professor/Dr. Surname"; switch to first names only after they do.
3. **Specific subject line** naming the topic and, if relevant, the scheme and date: "Prospective postdoc: [topic], available [month year]", "Host request: [scheme] application, deadline [date]".
4. **Why this person, concretely.** One specific paper, project, or resource and the actual link to the applicant's work. Never a mass email; check every name and detail.
5. **What you bring.** One or two results with the applicant's role, or transferable skills when changing field. Attach the CV, but the body must carry the essentials.
6. **Say what you are asking for and what it costs them.** Hosting only or funding too; for fellowships give the scheme, value, duration, their required deliverables, and deadlines. The proposal is the applicant's own work; offer to develop it with them, never ask them to write it.
7. **Referees get a package.** Ask whether they can write a strong letter; give the post, deadline with time zone, submission route, and name form; attach CV, statement or proposal, the ad, and a short factual list of what to cover. Ask four to six weeks ahead when possible; when the lead time is shorter, say so plainly and make the ask smaller.
8. **Tone.** Direct and polite, enthusiastic without pressure. No heavy apologies or gratitude ("Thank you for your time" is enough), no hedging, no "bumping this", no casual greetings. Write it in the applicant's own voice; assistance is fine for editing, not for inventing.
9. **Timing.** Send in the recipient's working hours. Follow up in the same thread after about a week for non-urgent requests (Caltech: at least two business days; MIT: 5 to 10 business days, 2 to 3 if urgent), briefly restating the ask and the date. After one follow-up, try another channel (a referral, the group administrator) instead of repeating.
10. **Graceful outcomes.** Accept a no and keep the door open; thank referees and tell them the outcome.

## Checklist

- [ ] Subject line names the topic (and scheme or date when relevant).
- [ ] First paragraph: who the applicant is and the ask.
- [ ] Exactly one main ask, as a direct question; deadline and route stated when there is one.
- [ ] A specific, verified link to the recipient's work; no sentence that fits any recipient.
- [ ] One or two results with the applicant's role; CV attached and mentioned.
- [ ] Sponsor request: scheme, value or duration, what the host must provide, and dates.
- [ ] Referee request: post, deadline with time zone, route, name form, materials list, and a "strong letter" question.
- [ ] Formal salutation with correct title and spelling; signature with position, institution, email.
- [ ] Inquiry under about 250 words unless the ask needs more; follow-up under about 100.
- [ ] No over-apology, hedges, "bumping", casual greeting, em/en dashes, or placeholders in the version to send.
- [ ] Follow-up date recorded.

## scripts/ce_check.py

Standard-library Python 3. Expects a Markdown or text email with a `Subject:` (or `제목:`) line. Reports subject line, body words, number of question sentences, salutation form, whether an attachment is mentioned, whether a date appears, apologies and gratitude stacking, hedges, "bumping"-style phrases, casual greetings, em/en dashes, non-Hangul CJK, placeholders, and `--expect` / `--forbid` names. `--kind` sets the word limit and the required elements (sponsor and referee need a date; host, sponsor, referee need an attachment mention). `--strict` exits 1 on any failure.

```bash
python3 scripts/ce_check.py host_inquiry_ko_v1.md --kind host
python3 scripts/ce_check.py --strict mentor_request_en.md --kind sponsor --expect "Professor Example" --forbid "Other University"
```

## Output layout

```
<application dir>/
  <recipient>_<kind>_ko_vN.md   Korean working drafts
  <recipient>_<kind>_en.md      English text to send (the user sends it)
  _guide/<recipient>_notes_vN.md  sources, open questions, follow-up date
```

## References

- `references/evidence.md`: each rule with verbatim, string-checked quotes from its sources, and gaps in the evidence.
- `references/sources.md`: the sources with type and URL.
