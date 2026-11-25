---
name: jd-analyser
description: Read a job description the way an ATS and a recruiter actually do, then score the candidate against it - FIT out of 100 across six weighted categories (hard skills, relevant experience, education, languages, certifications, preferred extras), with evidence strength and a confidence level, after a pass/fail check of hard knock-out gates. Soft personality traits are never scored. Non-JD factors (employer history, warm contacts, unknowns) are plain flags in words, and every read ends with the honest improvements that would raise the score. Use the moment a posting arrives, before writing a line of any document.
---

# JD Analyser

**When to use:** the moment a job description arrives — pasted, URL, or screenshot — and before
any CV or cover-letter skill writes a line.

## Why this exists

A Power BI apprenticeship was once read wrong. Its *mission* bullets said "take ownership of
Power BI developments of increasing complexity", so a Power-BI-specialist CV was drafted with
DAX and data-modelling framing. The JD's actual requirement list was four lines long and did
not mention Power BI at all. Its first mission line read: *"we will support your skills
development on the Power BI tool."*

They were hiring to train. The candidate caught it and called the draft delusional.

Reading responsibilities as requirements inflates the CV, invites interview questions you
cannot defend, and mis-positions you against the role. This skill exists to make that
mistake structurally impossible, and then to put an honest number on what is left.

---

## Step 0 — Quick score first

Before anything else, output one line:

`**<Company> — <Role>. FIT X/100 (<band>, <confidence> confidence).**  <one-sentence reason>`

If a gate failed, say so in the same line: `**... FIT 70/100 — BLOCKED: <gate>.**`

Then run the analysis. Do not build any document until the user gives a go-ahead. A fast,
honest verdict is worth more to them than a slow, thorough one they did not ask for yet.

## Step 1 — Load ground truth

1. **`facts.md`** — the only source of claimable facts. Its **Evidence Index** carries
   per-skill caveats, and those caveats are binding. If it says *"SharePoint — not verified,
   never claim"*, then SharePoint never appears, no matter what the JD wants.
2. **`profile.yml`** — location, duration, exclusions, deal-breakers, granted exceptions.
3. Any wider knowledge base, only if the JD touches something `facts.md` does not cover.

If neither file exists, say so and offer to scaffold them from `examples/` before continuing.
Do not proceed on guesses about the user's background.

## Step 2 — Bucket every line of the JD

Sort each statement into exactly one bucket.

| Bucket | What it is | Headings it usually sits under |
|---|---|---|
| **BAR** | What you must already have to be considered | "Requirements", "Your profile", "Qualifications", "Profil recherché", "Type d'études" |
| **WORK** | What you will do *after* being hired | "Mission", "Responsibilities", "Objectives", "You will join…" |
| **BONUS** | Explicitly optional | "nice to have", "a plus", "ideally", "familiarity with", "highly valued" |
| **NOISE** | Employer branding | headcount, ESG targets, "why join us", awards, training-hours stats |

**Training-signal override.** If the JD says it will teach a skill — *"we will support your
skills development on X"*, *"you will learn"*, *"training provided"*, *"opportunity to develop
skills in X"* — then **X is taught, not required**, even when X appears in the job title. It
carries zero weight in the score. Flag it explicitly in the output. This is the single most
common misread in the entire process.

**Study-path lines are BAR.** Postings often name target schools or degree types. Treat these
as a real signal about the intended profile, not decoration.

**Soft traits are never scored, in any bucket.** *Dynamic · rigorous · proactive · team player ·
good communicator · organised · curious · high potential · entrepreneurial spirit · strong
appetite for X.* No application can falsify them, so a score that counts them measures nothing.
List them once, marked `S`, and move on. (What the CV does with them is `cv-tailor`'s job: show
the trait through a concrete result, never by naming it.)

## Step 3 — Hard gates (pass / fail, before any number)

A hard gate is a requirement no amount of CV craft can close. This is how real screening
works: ATS knock-out questions (location, work authorisation, required licence, required
language, required degree) remove a candidate before any ranking happens. Check all six:

| Gate | Fails when |
|---|---|
| **Degree field** | JD names a field the candidate does not hold (chemistry, law, pharmacy, design) |
| **Specialised school** | JD names a school type they are not in, as an exclusive requirement |
| **Stated language** | JD explicitly requires a language above the candidate's stated level |
| **Hard tool bar** | A named tool is a listed *requirement* and `facts.md` has no evidence for it |
| **Location** | Outside the commutable zone, with no exception granted in `profile.yml` |
| **Work authorisation** | Requires nationality, clearance, or status the candidate lacks |

If any gate fails: **eligibility = BLOCKED**, the recommendation is automatically **don't
build**, and you name the gate in one sentence. **Still compute FIT** and show it — a blocked
role that would otherwise score 85 tells the user something different from one that would
score 40, and flattening both to one capped number hid exactly that.

Do not spend paragraphs arguing around a failed gate. Do not let strong evidence elsewhere
talk you past it.

**Contract duration is NOT a hard gate.** A shorter-than-preferred contract is a flag, never an
automatic no. That is the user's call, not the filter's.

### The stated-language rule, in both directions

Read the language bar **only as written**, and apply it symmetrically. Never infer an
unstated requirement from the posting's own language or the company's country.

- JD states English only, written in English → write English, do not hedge about the local language.
- JD states "intermediate English", written entirely in French → still just English. Do not
  invent a French bar from the fact that the posting is in French.
- JD states French proficiency → that is a real gate. Fail it honestly.

### The title trap

The job title is marketing copy; the responsibilities define the domain. Read the
responsibilities before trusting the title.

One posting titled *"Analytical Development & AI"* read like a data role. Its responsibilities —
*"correlations between the structural characteristics of molecules and multi-technique
analytical profiles"* — made it analytical **chemistry**. Always ask what the word means
**in this industry**.

## Step 4 — FIT: score the evidence against the whole posting

**FIT answers one question: how well does this candidate's real evidence answer this job
description?** Not the employer, not the network, not the candidate's preferences.

### Why the model looks like this

The weights are not invented. They follow how the matching engines behind most enterprise ATS
platforms rank candidates, and what recruiters say they filter on:

- Matching engines extract structured **categories** — skills, job titles, education,
  certifications, languages, management level, industry — and score each one separately, with
  **skills carrying the dominant weight** (typically 30–65%), job titles next (15–30%),
  education 5–20%, certifications 5–15%, languages 0–10%.
- **Hard skills outweigh soft skills** at the engine level, and match-rate tools publish their
  priority order as hard skills first, then education and job title, with soft skills last.
- **Evidence in dated experience outweighs a skills-list mention.** A skill inside a dated role
  lets the engine compute recency and duration; a bare list gives it neither.
- Keyword engines read **the whole posting**, responsibilities included. So a tool named only in
  the mission block still counts toward fit — at lower weight than a stated requirement, and at
  zero weight if the JD says it will teach it.
- Callback rates rise steeply up to a match of roughly 75 and flatten above 90. That is where
  the bands below come from.

An earlier version averaged only the requirement lines that survived a "testable" filter. In
this market most requirement blocks are 1–2 testable lines plus personality traits, so that
average hit 5.0/5 almost everywhere — including a role whose central task (running A/B tests)
the candidate had no evidence for at all. A score that is always top marks is not a score.

### The six categories

Score only the categories the JD actually mentions. Weights of absent categories are dropped
and the rest renormalised, so a posting with no language line is not scored on languages.

| Category | Weight | What goes in it |
|---|---|---|
| **H — Hard skills & tools** | 40 | Named tools, languages, methods, platforms — from BAR **and** WORK |
| **E — Relevant experience** | 20 | Role family, domain, level/years if stated, "able to turn a business need into X" type deliverables |
| **D — Education** | 15 | Degree level and field |
| **L — Languages** | 10 | Each stated language and level |
| **C — Certifications / licences** | 5 | Only those the JD names |
| **B — Preferred / bonus** | 10 | Everything in the BONUS bucket |

### Credit per item — evidence strength

Every item gets one credit, from `facts.md` and nothing else:

| Credit | Evidence | Example |
|---|---|---|
| **1.0 DEMONSTRATED** | Used in a dated role or a shipped project, with an outcome | "Built Power BI dashboards for 30+ clients, weekly" |
| **0.6 CLAIMED** | Skills list, coursework, or certification only — no dated use | "SQL (coursework)" |
| **0.3 ADJACENT** | A named, transferable equivalent — say what it is | Tableau against a Power BI requirement |
| **0 NONE** | Nothing in `facts.md` | — |

A candidate never *exceeds* 1.0 on an item. Clearing a bar with room to spare is worth saying in
the positioning brief; it is not worth a number above the maximum.

**Inside H, items carry a requirement weight:** stated in BAR = **2**, named only in WORK = **1**,
taught (training signal) = **0**. So `H = Σ(weight × credit) / Σ(weight)`.

**E, D, L, C, B** are the plain mean of their item credits. For **L**, one CEFR level below the
stated bar = 0.5; further below is a gate if the language is in BAR.

### The formula

```
FIT = round( 100 × Σ(category weight × category credit) / Σ(weights of categories present) )
```

Show the arithmetic as a scorecard, one row per category present. Never skip the table — the
number without the table is exactly the unreadable output this model replaces.

### Bands

| FIT | Band | Reading |
|---|---|---|
| **80–100** | Strong | The evidence answers the posting. Build |
| **65–79** | Good | Real fit with named gaps. Build, and let the flags decide priority |
| **50–64** | Stretch | Half the posting is unanswered. Build only if a flag is strongly positive |
| **< 50** | Weak | Skip unless there is a warm path |

For trackers that use a 5-point column, record `FIT/20` to one decimal (72 → 3.6).

### Confidence

Count the scored items (everything except soft traits and taught skills):
**8+ = High · 4–7 = Medium · 0–3 = Low.** Print it next to the number, every time. A score
computed from two items is a guess, and it has to look like one.

## Step 5 — Flags: everything that matters but is not JD-match

State each in **one line**, as a fact, never as a number. Omit any that do not apply.

| Flag | Say |
|---|---|
| **Core-task gap** | If the WORK block's centre of gravity (the one thing they will own alone) scored 0 — name it. It will be the hardest interview question |
| **Bar softness** | If most BAR lines are soft traits: *"the stated bar is mostly personality traits, so the CV has to do the sorting"* |
| **Company history** | Prior applications and **how far they got**. An interview is a positive. Repeated CV-screen rejections are a negative, and they compound |
| **Archetype** | Whether the role sits inside the target roles in `profile.yml`, or outside all of them |
| **Warm path** | A named contact, a referral, or nothing |
| **Duration / start / location** | Against stated preferences. If absent from the posting, **say so and ask** |
| **Differentiated asset** | Anything built that names this employer or its exact problem |

Then give the recommendation as **one sentence of judgement**:
*build now · build if the pipeline is thin · don't build · need info first* — and say which
band or flag drove it. A Strong FIT with bad flags is still a skip. A Stretch FIT with a warm
contact and a differentiated asset can still be a build.

## Step 6 — Honest improvements (what would raise FIT)

List at most three, each with its point value, and **only moves that stay true**:

1. **Unrecorded evidence.** A JD skill the user genuinely has but `facts.md` does not record.
   Ask; if confirmed, **update `facts.md` first**, then rescore. Most real gains come from here.
2. **Evidence upgrade.** A skill sitting at CLAIMED (0.6) that a dated role or project in
   `facts.md` actually demonstrates — move it into that role's bullet, and it scores 1.0.
3. **Placement.** The JD's top terms belong in the profile line and the first bullet of the
   most relevant role, and the exact job title in the headline when it is truthful. This
   raises the ATS ranking of the document, not FIT — say so.

Never suggest acquiring a skill to close a gap for *this* application, and never suggest a
wording that implies evidence `facts.md` does not hold.

## Step 7 — Positioning brief

Four lines. Every downstream document skill builds from them, not from its own read of the JD.

- **Lead with:** the items scored 1.0 in H and E — these are why they qualify
- **Mention once:** BONUS-matching evidence, factually, at `facts.md`'s stated depth
- **Do not claim:** every `facts.md` caveat this JD tempts, and every item scored 0, named explicitly
- **Archetype:** one phrase (e.g. "engineering student who already ships dashboards"), never a
  seniority the JD did not ask for

## Anti-inflation rules

1. **Never build a persona out of WORK bullets.** They count toward FIT at weight 1 when the
   evidence is real; they never become claims when it is not.
2. **Claim at `facts.md`'s depth, not the JD's.** If the file says "working proficiency, not a
   DBA", the CV says working proficiency.
3. **A low bar is good news — say so.** Clearing modest requirements comfortably is a stronger
   and more defensible position than a stretched claim to seniority.
4. **One line per real skill.** A genuine differentiator earns one honest line, not a
   reordered skills grid, a rewritten headline, and three bullets.
5. **Anything not in `facts.md` does not go on the CV.** No exceptions, ever.

## Output shape

```
**<Company> — <Role>. FIT X/100 (<band>, <confidence> confidence).**  <one-line reason>
Eligibility: PASS | BLOCKED — <gate>

### Scorecard
| Category | Weight | Items | Credit | Points |
|---|---|---|---|---|
| H Hard skills | 40 | A/B testing (W, 0) · Amplitude (W, 0) · QA (W, 1.0) · … | 0.25 | 10.0 |
| …          |    |    |      |      |
| **Total**  | 95 |    |      | **52.3 / 95 → FIT 55** |

### Requirements (BAR), with evidence   ← one row per item, facts.md line refs, soft traits marked S
### Taught, not required               ← training signals, if any
### Flags                              ← Step 5, one line each, words not numbers
### Improvements                       ← Step 6, max three, each with its point value
### Positioning brief                  ← Step 7
### Recommendation                     ← one sentence, naming the band or flag that drove it
```

## Worked examples — the same postings under the old and new model

Three real reads, anonymised, re-scored with this model. The old model returned 5.0, 5.0 and a
capped 2.0 — nothing a person could act on.

**Company J — Product Manager Apprentice (checkout).** Old: **5.0/5**, from 2 testable lines.
New: **FIT 55 — Stretch, High confidence.**
H 0.25 (QA demonstrated; A/B testing, Amplitude, Confluence all named in WORK with no evidence)
· E 0.6 (adjacent: digital delivery and a shipped product, no PM title) · D 1.0 · L 1.0 ·
B 0.53 (developer collaboration 1.0, UX 0.6 claimed, A/B 0).
`(10 + 12 + 15 + 10 + 5.3) / 95 = 55`. **Core-task gap flag:** the one thing the apprentice owns
alone is running A/B tests, and it scored 0. The old 5.0 hid the single most important fact
about this role.

**Company K — AI & Automation Apprentice (media group).** Old: **5.0/5** (raw 5.38), from 2
testable lines. New: **FIT 84 — Strong, High confidence.**
H 0.72 (agent configure/test/document 1.0, an LLM platform 1.0, Power BI 1.0, a named copilot
product 0.6, a named agent builder 0) · E 1.0 (primary archetype, business need to shipped
tool) · D 1.0 · B 0.77 (prompt engineering 1.0, agent building 1.0, no-code automation
platforms 0.3 adjacent via code-based automation). No language line, so L is dropped.
`(28.8 + 20 + 15 + 7.7) / 85 = 84`. **Differentiated asset flag** decides it: BUILD NOW.

**Company L — FinOps & AI Intern (automotive, abroad).** Old: **2.0/5 capped** ("4.6 on every
item except German"). New: **FIT 70 — Good, but BLOCKED: stated language** (very good German,
none held). E 0.6 · D 1.0 · L 0.5 · B 0.66 (SQL, Python, HTML 1.0; Java 0; public cloud 0.3
adjacent via a cloud AI certification). FinOps itself is taught (onboarding promised), weight 0.
The number now says what the old cap could not: the profile fits, one gate kills it.

**Gate-killed reads, for contrast** (from the original set): a digital-marketing role requiring
fluent French against A1 — BLOCKED, stated language, with the responsibilities matching well; an
"Analytical Development & AI" role requiring a chemistry masters — BLOCKED, degree field, title
trap fired; an e-commerce content role requiring Photoshop and Illustrator — BLOCKED, hard tool
bar. **Three consecutive postings that read like a fit and were closed by a gate nobody checked.**

## The pattern to watch

Screen the requirements block for gates first, every time. Then score the whole posting,
because the tools in the mission block are what the ATS ranks on and what the interview
will test.

**A soft bar is a warning, not an invitation.** When a posting's requirements are all
personality traits, FIT is carried by the hard skills in the mission block — which is exactly
where a candidate who only read the requirements would never look.
