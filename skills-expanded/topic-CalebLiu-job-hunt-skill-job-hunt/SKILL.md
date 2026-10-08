---
name: job-hunt
description: End-to-end job application pipeline orchestrator. Triggers on user pasting JD URL, asking "what should I apply to", saying "submitted" / "I'm at the form" / "follow up", or giving review feedback on a draft. Routes to one of 8 phases — bootstrap, research, tailor, review, submit walkthrough, track, outreach, learn — based on user intent. Per-role tailoring is delegated to the cv-tailor skill. Designed to be forked; configuration in your workspace's config.yaml drives paths and context.
---

# Job-Hunt Pipeline (Generic)

You are running a user's job application pipeline end-to-end. **Always read the workspace config and memory files first** — they tell you who the user is, what market they're targeting, and what writing rules they've codified.

## Configuration

The workspace path is set when the user installs this skill. Default expectation:

```
config.yaml at:           ${WORKSPACE}/config.yaml
Master CV:                ${WORKSPACE}/cv_master.tex
Build script:             ${WORKSPACE}/build.sh
Experience bank:          ${WORKSPACE}/experience-bank/
Templates:                ${WORKSPACE}/templates/
Applications:             ${WORKSPACE}/applications/<company>-<role>-<YYYY-MM-DD>/
Tracker:                  ${WORKSPACE}/applications/_tracker.md
Memory (per Claude Code session): in your project's memory directory, conventionally:
  - project.md             (user profile, target market, eligibility)
  - feedback.md            (writing rules — accumulates over time via Phase 7)
Sub-skill:                cv-tailor
```

If `${WORKSPACE}` isn't set or `config.yaml` doesn't exist, ask the user where their workspace is, or trigger Phase 0.

## State detection — pick the right phase

| User intent | Trigger phrases | Phase |
|---|---|---|
| First-time setup | "build my CV", no `cv_master.tex` exists, "let's start" | **0. Bootstrap** |
| "What should I apply to" | "find me jobs", "what roles fit me", "research target companies" | **1. Research** |
| Specific role discussed | pasted JD URL or full JD text, "apply to this", "tailor for this" | **2. Tailor** |
| Drafts ready, not yet submitted | follows Phase 2 automatically; or "review this" | **3. Pre-submission Review** |
| About to submit | "I'm at the form", "ready to submit", screenshot of application form | **4. Submit walkthrough** |
| Just submitted | "submitted", "applied", "投了" | **5. Track + propose follow-up** |
| Post-application warmth | "follow up on X", "DM the founder", "cold outreach" | **6. Outreach** |
| Reviewing weekly | "this week's pipeline", "status of applications" | **5. Status review (read tracker)** |
| Learning from feedback | user critiques a draft, says "change X to Y" | **7. Learn + backport** |

If unsure which phase, ask. Don't auto-pick a phase that costs many tokens.

---

## Phase 0 — Bootstrap (one-time per user)

**Run when:** no `cv_master.tex` exists, OR user explicitly asks to rebuild.

**Steps:**
1. Get raw material from the user via conversation:
   - Education (institutions, dates, grades / GPA, relevant modules)
   - Work history — **honest** (dates, role, what was actually done; don't inflate "shadowing" to "managed")
   - Projects — name, what it does, real numbers if any (users / revenue / stars)
   - Skills (real, with depth)
   - Languages
   - Visa / work authorisation status
   - Target roles + target market (e.g., "UK AI startups, junior")
2. Pull verifiable evidence in parallel via WebFetch:
   - GitHub profile + repo metadata (`gh api repos/<user>/<repo>` if `gh` is installed)
   - Personal sites / live products
   - LinkedIn URL (user must provide; LinkedIn blocks scrapers)
3. Write `cv_master.tex` (1-page, ATS-friendly LaTeX, sections: About → Projects → Skills → Education → Experience).
4. Build `experience-bank/<project>.md` files: at least 4–6 bullet variants per project, framed by role type (Growth / Engineering / Data / BizOps / Product / etc.).
5. Build `templates/cover_letter.template.md`, `linkedin_dm.template.md`, `why_i_fit.template.md` (or copy from this skill's defaults).
6. Save `memory/project.md` and `memory/feedback.md` with:
   - Profile snapshot (verified, dated)
   - Default positioning ("AI Product Builder", "Founding Engineer-track", etc.)
   - Initial writing rules (start with the 9 generic rules in `feedback.template.md`)
7. Verify build: `cd ${WORKSPACE} && ./build.sh` → 1-page PDF.

**Output:** master CV + experience bank + templates + memory in place.

**Don't:** invent metrics. If user can't confirm a number, drop it.

---

## Phase 1 — Research (target discovery)

**Run when:** user asks "what should I apply to" / "research X / Y companies" / "salary at <company>".

**Steps:**
1. List 8–12 candidate companies based on user's target market + role types. Tier them: high-fit / mid-fit / stretch.
2. For salary or open-role data — **always dispatch sub-agent(s)** rather than serially WebFetch. Glassdoor / LinkedIn block scrapers; ATS pages (Ashby / Greenhouse / Lever / Workable) work better.
3. Sub-agent brief (template):
   ```
   For each company: title, location, JD content summary (60–100 words),
   required + nice-to-have, salary disclosed verbatim, salary triangulation
   from 3+ sources (levels.fyi, Glassdoor, RepVue, WTTJ, 4dayweek, Reddit),
   user-fit score /10, visa risk flag.
   ```
4. Deduplicate against tracker — don't re-research already-applied companies.
5. Output: ranked table (company × role × fit × est. comp × confidence × visa flag) + top 3-5 picks.

**Hard rules:**
- Don't invent salaries. "Not disclosed" is acceptable.
- Always flag visa gates (e.g., UK Security Clearance, "no sponsorship now or in the future" clauses) for blocked roles.
- Don't pad the list. 5 well-researched > 20 generic.

---

## Phase 2 — Tailor (per role) — DELEGATE TO `cv-tailor`

**Run when:** user pastes a JD URL/text or says "apply to this".

**Delegates to:** the `cv-tailor` skill (separate `SKILL.md` at `skills/cv-tailor/`).

`cv-tailor` produces:
```
applications/<company>-<role>-<date>/
├── analysis.md              # JD analysis + tailoring decisions
├── cv.tex / cv.pdf          # 1-page tailored CV
├── cover_letter.tex / .pdf  # 250–400 word cover letter
├── linkedin_dm.txt          # ≤60-word cold DM
└── why_i_fit.txt            # 3 bullets ≤25 words for application form
```

After cv-tailor finishes, **always** proceed to Phase 3 before Phase 4.

---

## Phase 3 — Pre-submission Review

**Run when:** Phase 2 just produced application materials.

**Steps:**
1. Tell user PDFs are ready, give `open` commands.
2. **Ask user to review and critique** before any submission. Do not push to submit.
3. If user gives feedback:
   - Apply each edit verbatim where possible.
   - Re-build PDF. Verify still 1 page.
   - **Mark the rule for backport in Phase 7.**

**Common review-loop edits to apply preventively** (read user's `memory/feedback.md` for accumulated rules):
- Don't claim measurement frameworks the user hasn't actually built (e.g., "weekly cohort review", "retention model") if they haven't confirmed they built one — use softer language like "weekly user-feedback reviews".
- Don't write end-to-end ops responsibility lists with words user hasn't validated — confirm scope before adding "finance", "fundraising", "hiring", etc.
- Don't use pitch-deck phrasing ("anti-spoonfeeding", "10x productivity", "redefining X") — concrete capability + behaviour wins.

If you find yourself re-applying the same edit twice across applications, hard-stop and update the relevant `experience-bank/*.md` so it's permanent.

---

## Phase 4 — Submission Walkthrough

**Run when:** user says "ready to submit" / shows a form screenshot.

**Branch on browser-automation availability:**
- Connected (e.g., Claude in Chrome extension) → use browser tools to navigate, read form, paste field-by-field. **Never click final Submit** — user clicks.
- Not connected → produce a paste-by-field playbook. User does the clicks.

**Field-by-field playbook template:**

```
| Field                                          | What to paste                                |
|------------------------------------------------|----------------------------------------------|
| First / last name                              | <from memory/project.md>                     |
| Email                                          | <from memory/project.md>                     |
| Phone                                          | <local format>                               |
| Location                                       | "<city>, <country>"                          |
| Resume / CV                                    | upload <abs path to applications/<x>/cv.pdf> |
| LinkedIn                                       | <full URL>                                   |
| GitHub / Portfolio                             | <full URL>                                   |
| Cover letter (file or text)                    | upload <cover_letter.pdf> OR paste content   |
| Custom Q1 (e.g. "why are you interested")      | from why_i_fit.txt or analysis.md            |
| Visa: right to work without sponsorship now?   | Honest answer (varies by user)               |
| Visa: future sponsorship needed?               | Honest answer — never lie                    |
| Salary expectations                            | from Phase 1 research, range not single      |
| Earliest start date                            | "Negotiable, ideally within X weeks"         |
| Where did you hear about us                    | "<company> careers page" or "<job board>"    |
```

**Common ATS custom-question patterns:**
- "Do you have prior X experience?" → answer honestly. "No" is fine if JD waives it.
- "Please expand on X experience" (often required even if previous answer was No) → use **adjacent-evidence framing**: "I haven't done X formally, but here's the closest work — [3 concrete bullets from experience bank]"
- "What excites you about <company>'s mission?" → tie user's specific angle to something verifiable about the company. Cite a recent post, blog, talk, or feature. Never generic.

**Hand off:** wait for user to click Submit. Don't simulate it. Don't auto-fill fields like "voluntary self-identification" demographics — those are user-only.

---

## Phase 5 — Track

**Run when:** user says "submitted" / "applied" / "投了".

**Steps:**
1. Append row to `applications/_tracker.md`:
   ```
   | <date> | <company> | <role> | <channel> | 📤 submitted | <folder> | <follow-up TBD> |
   ```
2. Schedule mental follow-up reminders:
   - **T+24h**: LinkedIn DM to hiring manager / recruiter (if not already sent)
   - **T+1 week**: status check — if no response, optional second-touch DM
   - **T+2 weeks**: move to "no response" if still nothing
3. Propose immediate next-best application from the tracker's pending / Wave backlog.

**Tracker status legend:**
📤 submitted · 👀 under review · 📞 phone screen · 💬 onsite · ✅ offer · ❌ rejected · 🚫 withdrew · ✏️ draft

---

## Phase 6 — Outreach (LinkedIn / cold email)

**Run when:** user says "follow up", "DM", "冷启动", or T+24h after a submission.

**Steps:**
1. If application folder has `linkedin_dm.txt`, use it as base.
2. Locate 1–2 specific people via WebFetch on `linkedin.com/company/<company>/people` if accessible, otherwise tell user to search manually for hiring manager / recruiter / employees in similar roles.
3. Customise hook per person: cite a recent post, talk, blog, or feature they shipped. **Never use generic hooks** ("I love your mission", "Saw your impressive profile").
4. ≤60 words, no emoji, no "hope this finds you well".

**For cold outreach to companies with no posted role (e.g., adjacent-product founder approach):**
- Talent pool form first
- LinkedIn DM to founder / Head of <relevant function>
- Email careers@<company> CC
- Lead with **the angle no one else has** (e.g., "I shipped <adjacent product> — same space, different wedge — here's what I learned about [retention / pricing / onboarding]")

---

## Phase 7 — Learn + Backport

**Run when:** user gives review feedback during Phase 3, OR after a meaningful event (rejection feedback, recruiter call insight, interview signal).

**Steps:**
1. Apply the edit to the **current application** files (Phase 3).
2. **Backport** the rule to the right place so it persists:
   - Reusable writing rule → `memory/feedback.md`
   - Master CV improvement (not application-specific) → `cv_master.tex`
   - Project-bullet variant fix → `experience-bank/<project>.md`
   - Template improvement → `templates/*.md`
3. After backport, the next Phase 2 invocation should produce drafts that already have the fix applied.

**Don't:** silently swallow user feedback. Each polish should leave a trail in either memory or the bank.

---

## Cross-phase hard rules

1. **Never auto-submit.** The Submit button is always the user's. Even with browser automation, stop before clicking Submit.
2. **Never invent metrics.** No churn rate, retention %, MRR, MAU unless user has confirmed.
3. **Never overclaim measurement frameworks.** Don't say "cohort review", "funnel analysis", "retention model" unless user has actually built one.
4. **Master CV is canonical.** Per-application work always copies + edits a copy in `applications/<x>/`. Never modify master directly via Phase 2 / 3.
5. **1 page CV always** (or whatever convention `config.yaml`'s `cv_format.length` specifies — UK convention is 1 page; US allows 2 for non-junior; academic CV is multi-page). Verify with `pdftotext -bbox-layout cv.pdf - | grep -c '<page'`.
6. **Cite something verifiable** for "why this company" — recent funding, blog post, talk, feature. Not generic praise.
7. **Visa honesty.** Form questions about authorisation and future sponsorship are answered honestly per the user's status.
8. **Tracker is source of truth.** Every submission goes in `_tracker.md`.
9. **Sub-agent for research, not WebFetch.** Glassdoor / LinkedIn block; multi-source triangulation is sub-agent work.
10. **Phase order matters.** Don't skip Phase 3 (review) to go straight Phase 2 → 4. Always pause for user critique.

---

## Quick-reference flowchart

```
User input → state detection
              │
              ├─ First time / no master CV ───────────────→ Phase 0 Bootstrap
              ├─ "what to apply to" ──────────────────────→ Phase 1 Research (sub-agent)
              ├─ JD URL / text pasted ────────────────────→ Phase 2 Tailor (cv-tailor)
              │                                            └→ always Phase 3 Review
              │                                              └→ Phase 4 Submit walkthrough
              │                                                └→ user clicks Submit
              │                                                  └→ Phase 5 Track
              │                                                    └→ propose Phase 6 Outreach
              ├─ user critiqued draft ─────────────────────→ Phase 7 Learn + backport
              ├─ "follow up / DM" ────────────────────────→ Phase 6 Outreach
              └─ "this week's status" ────────────────────→ Phase 5 review tracker
```

---

## Notes for adopters

- **Customise `memory/feedback.md` aggressively.** The skill's value compounds over time as your writing rules accumulate. After 3 applications, your `feedback.md` should have rules specific to YOU that the generic version doesn't.
- **After ~5 applications, scan `_tracker.md` for callback patterns.** Roles that get callbacks → double-down. Roles that don't → diagnose materials or stop.
- **After first phone screen, capture insights in a new memory file** like `interview_signals_<company>.md` — use them for subsequent applications at peer companies.
- **Sub-agent dispatch in Phase 1 burns tokens.** Run it once per ~10 candidate companies, not once per 1.

See `docs/customization.md` for guidance on adapting to: different markets (US / EU / APAC), different career stages (senior / career-changer), different industries (consulting / banking / academic), different output formats (Word / Google Docs / Markdown).
