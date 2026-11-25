---
name: configure-profile
description: >
  Create or update the global learner profile. Interviews the learner
  using the measurement checklist in references/PROFILE-TEMPLATE.md and
  writes the structured result to profile/PROFILE.md. Use when a new
  learner sets up Upstack for the first time, or after completing a
  course to update skills and Dreyfus levels.
metadata:
  version: '1.0'
---

## Purpose

The learner profile is the full anatomy — who the learner is across all
courses. Every future course calibrates against this profile. The quality
of the profile determines the quality of tutoring.

This is a conversation, not a form. The tailor takes the measurements —
the customer doesn't arrive with them. Interview the learner naturally,
probe when answers are vague, and capture the result in structured
markdown. If this is the learner's first time using Upstack, set the
tone: thoughtful, personal, unhurried.

---

## Before You Start

Read `references/PROFILE-TEMPLATE.md` — the measurement checklist with
all 7 fields, probe guidance, example answers, output format, and
recording rules. This must be in your context before the conversation
begins.

If `profile/PROFILE.md` already exists, read it too — this determines
whether you are creating a new profile or updating an existing one.

---

## Procedure

### Step 1 — Determine mode

- If `profile/PROFILE.md` does not exist → **New Profile** (Step 2a)
- If `profile/PROFILE.md` exists → **Update Profile** (Step 2b)

### Step 2a — New Profile: Interview

Open by asking if the learner has a professional bio or CV to share:
"Do you have a professional bio, CV, or LinkedIn summary you'd like to
paste to the chat? I can use it as a starting point and only ask for
what's missing."

**Path A — No bio or CV:**

Walk the learner through all 7 measurement fields in order. Use the
primary Ask prompt for each field. Probe if the answer is sparse — see
the template for probe questions and examples.

1. **Name** — "What name should the tutor use for you?"
2. **Professional Background** — "What's your professional background?
   Domain, role, years of experience. What do you do day-to-day?"
3. **Skills Inventory** — "What are your strongest skills — technical,
   domain, or otherwise? What can you do confidently, without looking
   things up?"
4. **Mental Models** — "How do you naturally think about problems? What
   paradigms, frameworks, or habits shape your default approach?"
5. **Skill Level Self-Assessment** — "Looking at your main areas of
   expertise, where do you sit on the skill spectrum? Rate yourself
   honestly — not where you want to be, but where you are now."
   Offer the five levels as a guide (do not name the framework to the
   learner):
   > Here's a five-level scale, from first exposure to deep expertise:
   >
   > 1. **Novice** — No prior exposure. You need step-by-step guidance.
   > 2. **Beginner** — Some exposure. You can follow instructions but
   >    can't improvise yet.
   > 3. **Competent** — You can work independently on routine tasks and
   >    understand the *why*, not just the *how*.
   > 4. **Proficient** — You see the big picture and handle exceptions well.
   > 5. **Expert** — Intuitive grasp. You can teach others and spot edge
   >    cases instinctively.
   >
   > Most people land in the middle for most areas — that's normal.
6. **Learning Preferences** — "How do you learn best? Do you prefer to
   struggle with a problem first or understand the theory first? Do you
   like analogies or formal definitions? Do you want to be pushed hard
   or guided gently?"
7. **Completed Courses** — "Have you completed any Upstack courses?"
   For a new profile, record "None — this is a new profile."

Move through the fields conversationally. If the learner's answer to one
field naturally covers another, acknowledge what you heard and confirm
rather than re-asking. Do not present all 7 questions as a numbered list
— ask one at a time, respond to the answer, then move on.

**Path B — Bio or CV provided:**

1. Parse the pasted text. Extract what you can for each measurement
   field. Note which are fully covered, partially covered, or missing.
   - Name, Background, and Skills Inventory are usually well-covered.
   - Mental Models can often be inferred (e.g. 15 years of Java → likely
     OOP-oriented thinking) — flag these as inferences for confirmation.
   - Skill levels can be estimated from years of experience and roles,
     but flag these as estimates.
   - Learning Preferences are rarely in a bio — these will almost always
     need a direct question.
   - Completed Courses: note any Upstack courses mentioned.
2. Present what you extracted in conversational form — not as a formatted
   profile. When presenting skill level estimates, briefly show the
   five-level scale before stating the estimate — the learner has not
   yet seen it. Example:
   "From what you've shared, it sounds like you're a senior engineer
   with strong C++ and Python background, probably thinking in OOP terms
   — is that right? And for skill level — five levels from first exposure
   to deep expertise: Novice → Beginner → Competent → Proficient →
   Expert. I'd put you around Proficient in systems programming — does
   that fit?"
3. Confirm the covered fields, correct any misreadings.
4. Ask targeted questions only for fields that are missing or uncertain.
   Learning Preferences will almost always need a direct question.
5. Once all measurement fields are covered, proceed to Step 3.

### Step 2b — Update Profile: Targeted conversation

Present a brief summary of what the current profile says (2–3 sentences).
Ask what has changed. Suggest natural triggers: completed a course, career
change, starting a new domain, skills grown since last update.

Only interview the fields that need updating — do not re-ask all 7. For
completed courses specifically, ask about new courses, new skills gained,
and Dreyfus shifts.

### Step 3 — Confirm before writing

Summarise what you will write in each section. Ask the learner to confirm
or correct. If the learner says "just write it", respect that and proceed.

### Step 4 — Write the profile

Write `profile/PROFILE.md` using the output format defined in the
template. Create the `profile/` directory if it does not exist.

Follow the 6 recording rules from the template's Recording Guidance:
exact section headings, Strong/Moderate/Weak groupings, Dreyfus table
with exact labels, Dreyfus shift notation for completed courses, named
paradigms in Mental Models, and the learner's own words preserved.

For updates: preserve sections that did not change, update only the
sections discussed. Always update the "Updated" date.

### Step 5 — Commit

- New profile: `git add profile/PROFILE.md && git commit -m "profile: configure learner profile"`
- Update: `git add profile/PROFILE.md && git commit -m "profile: update learner profile"`

---

## Interview Guidelines

- **Don't rush.** This may be the learner's first experience with
  Upstack. Take time to make it feel personal, not administrative.
- **Don't accept vague answers.** "I know some Python" is not a
  measurement. Probe for specifics — see the template's Tips section.
- **Watch for overstatement and understatement.** Use probe questions
  to triangulate. What learners claim and what they can demonstrate
  often differ.
- **Domain-agnostic language.** Do not assume the learner is a
  programmer. They may be studying accounting, project management,
  networking, or any other domain.
- **Preserve the learner's own words.** The profile should sound like
  the learner, not like a standardised form. Structured doesn't mean
  sterile.
- **Use the tailor analogy if helpful.** If the learner is confused
  about why you are asking these questions: "I'm taking your full
  measurements now — this helps me tailor every future course to fit
  you specifically."
- **No internal language.** Never surface filenames, internal framework
  terms, or git commands in learner-facing language during the interview.
  Handle file writes and commits silently — the learner never needs to
  know these happen.

---

## Reference

- Measurement checklist and output format: `references/PROFILE-TEMPLATE.md`
- Two-layer calibration model: `references/PROFILE-TEMPLATE.md` §Relationship to Learner Context
- How the tutor reads the profile: `references/PROFILE-TEMPLATE.md` §How the Tutor Reads the Profile
- Tutor interview tips: `references/PROFILE-TEMPLATE.md` §Tips for the Tutor During Measurement
