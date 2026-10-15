---
name: playbook-name-to-other-prospects
description: Names 2 other right-fit people at the prospect's own company so an email can ask "is this you or them?" without ever naming the person being emailed. Triggers on "name two other people at the company", "who else works there", "should I be talking to someone else", "colleague name variable", "other prospects line", "wrong person CTA". Outputs other_prospects, a ready-to-drop phrase like "Jeff Barg or Rob Cook".
---

# Playbook: Name 2 Other Prospects

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the email needs a "not sure if this is you" or "who owns this" angle, or any CTA that
offers the reader an easy referral instead of a yes or no.

**Do not use when:** you want the buying committee itself as separate leads. **You never email the
people named in this variable** unless they are separately in the list on their own merits.

**One-line output:** `other_prospects = "Jeff Barg or Rob Cook"`

## 1. Trigger and scope

This produces one variable: the names of up to 2 **other** people at the same company as the person
receiving the email. It exists so a first email can say "if this sits with Jeff Barg or Rob Cook
instead, happy to talk to them" — **without the reader feeling surveilled and without guessing wrong
about who owns the problem.**

### ⛔ The one absolute rule: never name the recipient to themselves

`Hey John, should I reach out to John?` is the worst possible outcome, and it is the thing this
playbook is built to prevent.

**No campaign, brief, or operator preference makes it acceptable.** It is enforced from the
recipient's full name **and** their profile URL, in a formula, on every row, always.

⚠️ **A row without `recipient_full_name` is not runnable.** The script should throw, and the build
must not start. Treating a missing name as "nothing to exclude" is how this fails.

### A second, softer exclusion

Optionally exclude **everyone else from the same company who is also in this campaign** — otherwise
two colleagues receive emails naming each other. Default it off, turn it on when a campaign has real
multi-contact density at one domain, and decide it at setup rather than mid-run.

## 2. Output contract

### Inputs required per row

| Field | Type | Required? |
|---|---|---|
| `domain` (bare, lowercase) | string | yes |
| `company_name` | string | no, improves the web verifier |
| `recipient_linkedin_url` | string | yes when known |
| **`recipient_full_name`** | string | **yes, always. This is the hard exclusion** |
| `all_campaign_recipients_at_this_domain` | string[] | only when same-campaign exclusion is on |
| `persona_titles` | string[] | yes — this is the title cascade |

### Output fields

| Field | Type | Example | Null? |
|---|---|---|---|
| `other_prospects` | string | `Jeff Barg or Rob Cook` | yes, `""` |
| `other_prospects_count` | int | `2` | no, `0` |
| `other_prospect_1_title`, `_2_title` | string | `Chief Operating Officer` | yes |

**Abstain value:** `""`. Never a single name padded to look like two, never a job title standing in
for a name.

### Copy-fit rules

- Slots into a sentence like `If this sits with {{other_prospects}} instead, happy to talk to them.`
- **Two names joined by " or ".** One name is fine and reads naturally; the sentence must still work.
- Real names, correctly capitalized, **full last names**.
- **Never a title instead of a name.** "your VP of Ops" is not this variable.

### Downstream gate

If empty, the whole sentence must disappear — **not just the variable.** Put the referral CTA in its
own sentence and use a pre-rendered whole-sentence field, or split the list at upload. **Spintax
cannot branch on an empty variable.**

## 3. Source chain (cost-tagged)

| # | Source | Cost | What it does |
|---|---|---|---|
| 1 | A colleagues-by-domain lookup | plan credits | returns people at the domain. Cheapest first pass |
| 2 | A title-cascade people search on the same domain | credits per company | ordered `include_title` / `exclude_title` cascade from the campaign's persona list |
| 3 | **The model judge** | CHEAP | screens candidates, cleans names, drops bad data |
| 4 | **A still-there web check** | FREE | confirms the named people are still at the company |

**Step 4 is not optional.** Provider job titles go stale, and this variable puts a **named human
being** into a stranger's inbox. A wrong name is not a soft miss.

## 4. Verification

**VERDICT: PASS 7/8.**

## 5. Clay implementation

- **`clay-table.md`** — the column build, including the two exclusion tiers as formulas.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt

Params: `max_completion_tokens=3000` (never `max_tokens` on a reasoning model),
`reasoning_effort="low"`, never `temperature`, JSON response format, flex tier for batch.

```text
You screen colleague candidates for a cold email variable.

You get a target company and a list of people a data provider says work there. Pick up to 3
who are credible senior colleagues at THAT company, best first, and return their cleaned real names.

Return JSON only, exactly this shape:
{"keep":[{"name":"First Last","title":"..."}],"dropped":[{"name":"...","why":"..."}]}

Keep a person only if ALL of these are true:
- Their job title is at the target company, not a different employer.
- Their headline does not contradict the job title. A headline naming another company or a
  different line of work means the data is wrong. Drop them.
- The title is a real decision maker or senior function owner: owner, founder, chief, vice
  president, head of, director, general manager, partner, principal.
- The title is not support staff: assistant, executive assistant, administrator, office
  manager, coordinator, receptionist, intern, apprentice, student, product owner, scrum.
- The name is a real person name with a first name and a last name.

Freshness rule. Provider job titles go stale. When a candidate has no headline and no other
text tying them to the target company, prefer a candidate whose headline names the target
company. Only fall back to a no-headline candidate when there are fewer than 3 candidates
whose text names the company.

Clean the name before returning it:
- Remove credentials, emoji, pronouns, hashtags, hiring banners, quoted nicknames, and any
  text after a comma, pipe, or bracket.
- Fix ALL CAPS and all lowercase to normal capitalization. Keep accents and hyphens as they are.
- Keep the full last name. Never shorten a two word surname. Drop middle names.
- If only one name token exists, drop the person.

A headline that names a different profession from the job title is a hard drop, even when
the job title looks senior. Self reported founder titles are the most common bad data.

Order the kept people most senior first. Keep at most 3. Never invent a person. If nobody
qualifies, return an empty keep list. No em dashes anywhere in your output.

Example input:
Company: Harbor Freight Robotics (harborfreightrobotics.com)
Candidates:
1. Devon Marsh | title at company: Co-founder | headline: Wedding Photographer and Videographer
2. priya RAMANATHAN, MBA | title at company: Chief Operating Officer | headline: COO at Harbor Freight Robotics
3. Sam Whitfield | title at company: Executive Assistant to the CEO | headline: EA to the CEO
Example output:
{"keep":[{"name":"Priya Ramanathan","title":"Chief Operating Officer"}],"dropped":[{"name":"Devon Marsh","why":"headline is wedding photography, the founder title at this company is not credible"},{"name":"Sam Whitfield","why":"executive assistant is support staff, not a decision maker"}]}

Example input:
Company: Delacroix Dental Group (delacroixdental.com)
Candidates:
1. Ana Lucia Perez Ortiz | title at company: Practice Owner | headline: Owner at Delacroix Dental Group
2. T. | title at company: Director of Operations | headline:
3. Marcus Feld 🚀 | Hiring! | title at company: Head of Patient Experience | headline: Head of Patient Experience at Delacroix Dental Group
4. Robin Vale | title at company: Vice President Supply | headline:
Example output:
{"keep":[{"name":"Ana Lucia Perez Ortiz","title":"Practice Owner"},{"name":"Marcus Feld","title":"Head of Patient Experience"}],"dropped":[{"name":"T.","why":"no usable first and last name"},{"name":"Robin Vale","why":"no headline ties this person to the company and two better candidates exist"}]}

PER-ROW DATA (appended last)
Company: <company name> (<domain>)
Candidates:
<numbered candidate list>
```

Two things in this prompt are doing more work than they look:

- **The headline-contradiction rule.** *Self-reported founder titles are the most common bad data in
  contact databases.* A "Co-founder" whose headline says "Wedding Photographer" is a data error, and
  without this rule it ships as a named human in a stranger's inbox.
- **The `dropped` array.** The model must say **why** it dropped someone. That costs a handful of
  tokens and gives you the only cheap way to audit a variable that names real people.

**Truncation guard:** `finish_reason=length` means retry, never abstain.

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| **The email names its own recipient** | The exclusion ran on a name that did not match exactly — a nickname, a middle initial, a maiden name | **Match on normalized name AND profile URL**, and normalize hard: lowercase, strip accents and punctuation, compare first+last only. **When in doubt, drop the candidate** |
| Two colleagues each receive an email naming the other | Same-campaign exclusion is off | Turn it on for campaigns with multi-contact density at one domain |
| The variable names someone who left last year | Provider titles go stale | The still-there check. **Not optional** |
| A "Co-founder" is really a photographer | Self-reported titles | The headline-contradiction rule |
| An executive assistant gets named | Senior-sounding proximity to the CEO | The support-staff exclusion list |
| The name renders as `PRIYA RAMANATHAN, MBA 🚀` | Raw provider strings are not copy | The cleaning rules. See also `playbook-first-name-cleaning` |
| Only one candidate qualifies | Common at small companies | **One name is a fine answer.** Make sure the sentence reads with one |
| The sentence renders with a dangling "or" | The copy assumed two names | Build the joined phrase in code, not in the template |
| Empty variable leaves a broken sentence | Spintax cannot branch on emptiness | Pre-render the whole sentence, or split the list at upload |

### Hard rules

- **Never name the recipient to themselves.** Enforced on every row, always.
- **Never email the people named in this variable** unless they are in the list on their own merits.
- **Never substitute a title for a name.**
- **A row with no recipient name is not runnable.**
