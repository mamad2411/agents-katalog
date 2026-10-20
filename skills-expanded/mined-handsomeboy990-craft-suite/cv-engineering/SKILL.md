---
name: cv-engineering
description: Builds and improves a CV or resume from the candidate's real profile: the format the target market and the applicant-tracking systems expect, achievement bullets that quantify a real result, tailoring to a specific role without invention, ruthless relevance and length, and a pass for the parsing that machines do before a human reads. Every line is true and supportable. Use to write a CV, improve one, or tailor it to a shortlisted role.
license: MIT
metadata:
  category: career
  version: 1.0.0
  depends_on: [career-core, career-profile]
  outputs: [cv-document, achievement-bullets, tailoring-notes, ats-check]
---

# CV Engineering

A CV has two readers: a machine that parses it in a second, and a human who scans
it in six. It has to survive both, and it has to be true. This skill renders the
candidate's real profile into a document that passes the parser, holds the human,
and states nothing the candidate cannot support.

## 1. The format the market expects

```
target       the format the candidate's market and level expect: the conventions
             differ by country, industry, and seniority, and are not assumed
ats          a layout an applicant-tracking system can parse: real text not images,
             standard section headings, no tables or columns that scramble on
             extraction, a common font, standard bullet characters
scan         a human's six-second scan lands on the name, the current role, and
             the top achievements; the layout puts those where the eye goes
length       one page early-career, two mid-to-senior, rarely more; length is
             earned by relevance, never by padding
```

## 2. Achievement bullets that quantify

The unit of a strong CV is the achievement bullet, and the weak version is a duty.

```
duty         "Responsible for the billing system"          (what the job was)
achievement  "Rebuilt the billing pipeline, cutting failed
             charges 40% and month-end close from 3 days to 1"   (what changed)
formula      action verb + what was done + the quantified result, true
number       a real number from the profile; if none exists, a real qualitative
             outcome, never an invented figure
relevance    the bullets chosen are the ones that matter to the target role, not
             the candidate's favourites
```

## 3. Tailoring without invention

```
emphasise    for a specific role, lead with the real experience that matches it;
             the same true history, ordered to the role
language     mirror the role's real vocabulary where the candidate's experience
             genuinely fits it, so the parser and the human both recognise the match
never        add a skill, tool, or result the candidate does not have to match the
             listing; tailoring reorders and reframes truth, it does not add to it
cut          the experience irrelevant to this role, to make room for what matters
```

## 4. Relevance and length, ruthlessly

```
keep         what advances the candidate's case for this role
cut          old roles at bullet length once they are far behind; a line each is enough
compress     early-career detail as the career grows; the graduate project leaves
             when the senior achievements arrive
zero         no objective-statement cliches, no skill bars, no "references
             available", no filler that survives only because it is traditional
```

## 5. The parsing pass

```
extract      run the CV as a machine would: does the text extract cleanly, do the
             sections parse, do the dates and titles come through
keywords     the real, relevant terms from the target role appear where the
             candidate's experience genuinely supports them, so a keyword filter
             does not drop a qualified candidate
contact      name and contact details parse correctly; a CV that scores well and
             loses the phone number has failed
```

## 6. Prohibitions

- Never state a skill, title, result, date, or tool the candidate cannot support.
- Never invent a number; use a real one or a true qualitative outcome.
- Never add to the truth to match a listing; tailoring reorders, it does not fabricate.
- Never use a layout that a tracking system cannot parse (image text, complex
  columns) if the candidate's market uses such systems.
- Never pad length; relevance earns length.
- Never keep a cliche (objective statement, skill bars, "references available")
  because it is traditional.

## 7. Protocol

1. Read the real profile from `career-profile` and the target role.
2. Choose the market- and level-appropriate, parseable format.
3. Write achievement bullets: action verb, what was done, quantified true result.
4. Order and emphasise to the target role, adding nothing untrue.
5. Cut to relevance and to the right length.
6. Run the parsing pass: clean extraction, real keywords, correct contact details.
7. Verify every line is supportable in an interview, per career-core.

## 8. Auto-critique

Score from 0 to 5: format appropriate and parseable, bullets are quantified
achievements not duties, tailoring reorders truth without adding to it, ruthless
relevance and correct length, parsing pass clean with real keywords, every line
supportable, no cliche filler.

Threshold: no axis below 3, average at least 4. A single line the candidate
cannot support, or an invented number, caps the score until corrected, per
career-core.

## 9. Interfaces

- Upstream: `career-core` for honesty, `career-profile` for the real material,
  `job-search` for the specific role to tailor to.
- Downstream: `cover-letter` complements the CV without repeating it,
  `interview-preparation` drills the achievements the CV claims.
- Lateral: `document-design` and `pdf-production` in `documents/` render the CV
  to a polished, correctly paginated PDF; `administrative-writing` for a formal
  application package.

## 10. Note on rendering

This skill produces the CV's content and structure. When a polished PDF is
required, the rendering (typography, pagination, a clean single- or two-column
layout that still parses) is handed to `document-design` and `pdf-production`,
which verify the rendered pages rather than trusting the generator. A CV that
looks perfect and does not parse is a failure this handoff exists to prevent.
