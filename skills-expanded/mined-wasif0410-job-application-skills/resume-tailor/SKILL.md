---
name: resume-tailor
description: Tailor a resume to one specific job posting and produce an ATS-friendly, one-page PDF in Jake's LaTeX resume template, plus a report of which posting keywords were added (and where) and which were left out (and why). Use this whenever the user pastes a job description or job link and wants their resume adapted — "tailor my resume", "optimize my resume for this job", "make it pass ATS", "keyword-match this posting", "make a resume for this role", "fix my resume for this internship" — or asks why their resume isn't getting interviews for a role, even if they never say "tailor". Also use it for follow-up edits (wording, metrics, layout, titles) to a resume produced by this workflow.
---

# Resume Tailor

One job posting in → one tailored, one-page resume (`.tex` + `.pdf`) + a keyword report.

The point is to get the user an interview. That takes three things that pull against each other:
1. **Rank in ATS keyword searches.** Recruiters search and sort the applicant pool by the posting's terms.
2. **Win a ~7-second human scan.** Recruiters look at titles, companies, dates and education first, and they've learned to spot generated, keyword-stuffed resumes.
3. **Hold up in the interview.** Interviewers go line by line, and anything implausible costs the offer the keyword won.

Most rules below balance these three. When a rule feels fussy, ask which of the three it protects.

---

## 0. Workspace setup (first run in a folder)

This skill works out of a folder the user owns (the **workspace**), so their source material and every tailored version stay together. All three skills (resume-tailor, cover-letter, /apply) share this **standard layout**:

```
<workspace>/
├── checkpoint.md               # overview + handoff notes: who the user is, what's been done, what's next
├── resumes/                    # the user's ONE original resume: .pdf/.docx/.tex/.md/.txt (ground truth)
├── personal-info/
│   ├── tailor-profile.md       # Identity, contact line, titles, confirmed facts, preferences
│   ├── cover-letter-profile.md # how their letters look and sound
│   ├── cover-letter-examples.md# (optional) their approved letters
│   ├── source-cache.md         # the resume's text + repo facts, read every run; refreshed every 5 runs
│   └── projects.md             # (optional) projects not fully on the resume
├── job-tracker/
│   └── applications.csv        # one row per posting
└── tailored/
    └── <Company>_<Role>_<Term>/ # one folder per posting: jd.md, research.md, resume.tex, PDFs, report.md…
```

**Paths:** whenever these skills name a file without a folder, it lives here:

| File | Path |
|---|---|
| original resumes | `resumes/` |
| `tailor-profile.md`, `cover-letter-profile.md`, `cover-letter-examples.md`, `source-cache.md`, `projects.md` | `personal-info/` |
| `applications.csv` | `job-tracker/` |
| `jd.md`, `research.md`, `report.md`, `resume.tex`, PDFs | `tailored/<posting>/` |
| `checkpoint.md` | workspace root |

**Finding the workspace:** it's the folder Claude is working in. If that folder has a `personal-info/` or `resumes/` folder, it's an existing workspace.

**Older flat layout** (resumes and profiles loose in the root): offer once to reorganize it into the standard layout, moving the files with the user's OK. If they decline, read the files where they are.

**Personal information lives only in the user's workspace files, never in this skill.** The skill folder holds rules and blank templates only. Never write a user's name, contact details, employers, resume content or letters into any file under the skill folder.

**First run in a folder (onboarding).** Check the workspace before doing anything else. If something is missing, don't create files silently. Tell the user what's missing and why it's needed, offer to create it, and wait for their yes:

0. **The folders.** If the standard layout doesn't exist yet, show the user the tree above and ask: *"Should I set up your workspace like this?"* On yes, create `resumes/`, `personal-info/`, `job-tracker/` (with an `applications.csv` holding just the header row, see /apply §8) and `tailored/`, plus a root `checkpoint.md` from `assets/checkpoint_template.md`. If resume files are sitting loose in the folder, offer to move them into `resumes/`.
1. **Original resume (exactly one).** If `resumes/` is empty, stop. Ask the user to put their resume there, or to open Claude in the folder that has them. Explain that the original resume is the ground truth for what they've done. If `resumes/` holds more than one resume, ask which one is the ground truth and offer to move the others out (to the Recycle Bin/Trash or an `archive/` folder), so every later run finds exactly one and configures itself.
1b. **`source-cache.md`.** If `personal-info/source-cache.md` is missing, create it from `assets/source_cache_template.md` (no need to ask; it holds only text copied from the user's own resume and repos): paste the resume's text (extracted as the refresh step in §1 describes), then the facts from **every** public repo on the user's GitHub (see "Pull all repos" in §1). See §1 for how it's used and refreshed.
2. **`tailor-profile.md`.** If it's missing, say something like: *"You don't have a `tailor-profile.md` yet. It's where your name, contact details, school, graduation date, work authorization and preferences live, so the skills never store them. Should I create it for you? I'll fill in what I can from your resume and ask you for the rest."* On yes:
   - Copy `assets/tailor_profile_template.md` to `personal-info/tailor-profile.md` and pre-fill everything the resume shows (name, contact line, school, degree, dates, employers and titles).
   - Then ask for the rest in **one** message, with suggested defaults:
     - the file prefix (default: FirstnameLastname)
     - city
     - work authorization and whether they need sponsorship, per country they're applying in
     - which job titles may be adjusted to mirror a posting (default: official titles only; see §4)
     - their GitHub or projects (or a `projects.md`)
     - any experience missing from the resume (contract work, other roles)
   - Write the answers into the profile and show the user the finished Identity section.
3. **Projects.** If the profile has no GitHub or projects and the user didn't give any, note that projects are where many keywords legitimately live. "I have no projects" is a fine answer.
4. **Tools (requirements check).** Check each of these is available, and report any that are missing in one message:

   | Tool | Used for | Usually comes from |
   |---|---|---|
   | `pdflatex` | building resume and letter PDFs | MiKTeX (Windows), MacTeX/BasicTeX (macOS), TeX Live (Linux); see `references/latex-build.md` |
   | `pdftotext`, `pdftoppm` | checking text and rendering pages | MiKTeX on Windows; poppler on macOS (`brew install poppler`) and Linux (`poppler-utils`) |
   | `perl` | the page-fill check (`scripts/measure_fill.pl`) | Git for Windows (Git Bash) on Windows; built in on macOS and Linux |
   | `zip` | packaging (/apply) | MiKTeX on Windows (or PowerShell's `Compress-Archive`); built in on macOS and Linux |

   Installing anything changes the user's system, so offer the install command and wait for their OK. Overleaf is the fallback for building PDFs, but then the page checks have to be done by eye.
5. **Companion skills.** The cover-letter step uses the `humanizer` skill, which ships alongside this one, and the optional `structural-humanizer` skill, which is installed separately. If either is missing, say so once and carry on with cover-letter's built-in read-aloud check.

If the user declines a file, continue with what's available and ask for the missing details inline when they're needed, without saving them anywhere.

---

## 1. Ground truth

**Content** always comes from three sources:
- the one original resume in `resumes/`, read through `personal-info/source-cache.md` (§1),
- the repo facts in `personal-info/source-cache.md` (plus `projects.md` if the user keeps one),
- the confirmed facts in `tailor-profile.md`.

**Format** comes from `assets/jake_template.tex`, or from the user's latest tailored `.tex` if they've customized the layout.

Never start a new posting from a previous tailored resume's content. Inferences made for job A, its keywords and its wording, would leak into job B as if they were facts. Re-derive them every time.

**Read the source cache, not the sources.** Everything read stays in the conversation and is re-read on every later step, so pulling the resume PDF and GitHub READMEs each run costs many times over. Instead:
- **Every run reads `personal-info/source-cache.md` only:** the resume's text and a short fact list per repo. Don't open the resume PDF or fetch repos.
- **Count runs.** Each tailoring run for a new posting adds 1 to "Runs since refresh" in the cache's header (follow-up edits to the same posting don't count).
- **Refresh every 5 runs**, or right away when the user asks (e.g. "I updated my resume", "refresh the cache", "reset the cache", "my repo changed"): re-extract the resume once (PDF: `pdftotext -layout`; .md/.txt/.tex: read it directly; .docx: `pandoc -t plain` or the docx skill), pull all repos again (see "Pull all repos" below), then **update the cache in place**: replace the resume text, add new repo facts, and change or remove a fact only when the new source contradicts it. Keep facts that came from elsewhere (code, approved letters, the user). Set "Last refreshed" to today and reset the count to 0. Tell the user in one line that the cache was refreshed.
- **Pull all repos** (on the first build and at every refresh): list every public repo on the user's GitHub (from the profile's GitHub link), e.g. `gh repo list <user> --limit 200 --json name,description,isFork,isArchived,primaryLanguage,pushedAt`, or `curl https://api.github.com/users/<user>/repos?per_page=100` if `gh` isn't available. Skip private repos (recruiters can't open them), forks, empty repos and any repo the profile marks "skip". For each remaining repo, read its README's opening section (what it is, stack, numbers, results; no diagrams, badges or full file trees) and record a short fact list. If a repo has no README, record its description and main language. Add new repos, update changed ones, mark deleted or renamed ones. The user never has to list their projects.
- **Between refreshes:** if the user mentions a repo the cache doesn't have, fetch that one README once and add it.
- Project bullets may only state what the cache (i.e. the repo) shows: numbers, stack, results. Recruiters click those links.

---

## 2. Read the posting

Save the posting text to `tailored/<folder>/jd.md`. If you were given a URL, fetch it.

**First, work out what the team actually does, not just the title.** Titles mislead. An "AI Engineer Intern" posting on an *AI Platform* team inside *Infrastructure & Platform*, whose duties are CI/CD, Kubernetes, Terraform and model deployment, is an ML-platform/MLOps role. Leading with chatbot work would miss it. This read decides which experiences go first.

Then sort the posting's terms:
- **Knockouts:** degree, graduation window, work authorization, location, availability. These are mostly answered in application forms. The resume only needs what the posting explicitly asks to see, e.g. "make sure your graduation date is visible".
- **Must-haves:** the Qualifications / Requirements list.
- **Responsibilities and team blurb:** secondary keywords, including the team's own name for its product, e.g. "AI platform".
- **Alternative groups:** "AWS, GCP, or Azure"; "one or more of Snowflake, Trino, Redshift, or Spark". Mark these as groups. One member satisfies the whole group.
- **Domain and soft terms:** "game developers", "producers", "adaptability". Usually not resume keywords. Note them and move on.

If a term is unfamiliar or company-specific, look it up before placing it.

**Research only when the job description is thin.** If the posting already says enough, work from the posting alone and do no web research. That's faster, and every keyword then comes straight from the job description.

**The JD is thin if two or more of these are true:**
- it names fewer than about 4 concrete tools, languages or technologies;
- it has no real responsibilities list (just a sentence or two about the team);
- it has no requirements or qualifications list;
- it's very short (under about 150 words of role-specific content, not counting the company boilerplate and benefits);
- it uses a vague title with no clue what the team works on (e.g. "Software Engineer Intern" and nothing else).

**State the decision in the report and the summary**, e.g. "Research: skipped, because the JD is detailed (names Python, SQL, pandas, PyTorch, LightGBM; full duties and requirements lists)" or "Research: done, because the JD is thin (no tools, no duties list)".

**If the JD is thin, research deeply.** Search the web for:
- **the company's real tech stack:** full-time engineering postings for the same team (they name languages, frameworks, databases, cloud, e.g. "React, TypeScript, Tailwind, Python/FastAPI, Postgres"), cloud/vendor case studies (e.g. a Microsoft Azure customer story), and engineering blog posts about architecture;
- **the product and its vocabulary:** what they build and the words they use for it (e.g. "agentic orchestration", "tool calls", "agent benchmark", "eval gates");
- **other versions of this posting:** previous years, other offices or seasons. They often carry a fuller "preferred qualifications" or values section;
- **the company's values page or hiring guide:** what they screen for (e.g. "Decisiveness, Simplicity, Job's Not Finished", "explain complex ideas clearly");
- **the internship program and interview process:** stages, format (e.g. AI-assisted live coding), timelines, pay, office locations;
- **past interns' accounts:** LinkedIn posts, Reddit, Glassdoor, intern blog posts about what they worked on.

From this, write down two things before drafting:
1. **The real stack.** These terms become keywords and go through §3, inferred into the best-fit role.
2. **What they're really looking for,** in 3–5 bullets. The experience bullets must then show each of these that the user genuinely has.

Both go in the report with source links.

Use what you find to decide which experiences lead, and to borrow the company's own words *where the user's experience genuinely matches* (calling a user's eval project an "agent evaluation benchmark" for a company that publishes agent benchmarks). Never add a keyword from research that the user has no basis for. Put the findings, with source links, in the report's *Company research* section, along with interview and application tips.

**When the JD is detailed (no research):** take the real stack and "what they're really looking for" straight from the posting's own sections (About the role, What you'll do, What you'll need, the company paragraph). Don't add keywords the posting doesn't contain. Only the user's own profile facts (e.g. AWS placed by profile rule) may add terms beyond the JD, and they go in Table 2 labelled "profile".

**Research the user's employers too, when it helps.** This is a quick check of the user's own employers, not the target company, and it's allowed either way. Look for product names, the official spelling of the company name (e.g. "eBay", not "Ebay"), public scale numbers for metrics, and anything public that would contradict a claim. For example, a product site saying "since 2015" contradicts "early-stage startup", so write "early-stage product" and tell the user.

---

## 3. Map every keyword to evidence

For each hard keyword, find its source. These are in order of strength:

1. **Explicit in the original resume.** Use the posting's exact wording in that bullet.
2. **Clearly implied by a role.** Infer it and write it in. Example: shipping services to Kubernetes through pull requests implies CI/CD. Processing millions of events on Databricks implies Spark/PySpark. Don't make the user confirm things this obvious. They find it tedious and they're the reviewer anyway. List these inferences in the report so they can veto any.
3. **In a project or repo.** Put it in that project's bullet, but only if the repo shows it.
4. **Confirmed in `tailor-profile.md`.** Use it where it fits.
5. **No direct basis → it still goes in, depending on priority (the user's rule, 2026-10-05):**
   - **Mandatory, Critical and Important JD keywords MUST appear in an EXPERIENCE bullet** (not only in skills or projects), even without direct evidence. Infer that the user did it in the single most plausible role, and write it as part of what that role already did. Examples:
     - credit-risk / fraud-style modelling → the role that already does data analysis and ML
     - LightGBM → the role that already trains or evaluates models
     - drift / data-quality monitoring → the role that already monitors models in production
   - **Nice-to-have and Soft keywords:** try to use them too. Place each where it reads naturally. Skip one only if no bullet can carry it believably, and say so in the report.
   - **Safeguards for every forced placement:**
     - Attach no invented metric. Reuse the bullet's existing real number or none.
     - Use modest verbs ("supported", "contributed to", "worked with", "applied") rather than "led" or "architected".
     - Keep it consistent with that employer's stack (plausibility test below).
     - Label it **forced** in the report and in Table 1's Basis column ("forced: placed at <Employer>").
     - Add each one to the report's **Interview prep: forced keywords** list with one line on how to talk about it honestly.
   - Don't stop at the forced placement. If the same gap keeps coming up across postings, also suggest a weekend project that would make it genuinely true (e.g. a LightGBM credit-default model with a drift check).

Ask the user only for what genuinely can't be inferred: specific numbers, names, dates, client details. Ask once, in one message.

**The stack you find in research counts as keywords too.** When research reveals the company's real stack beyond the posting (e.g. full-time postings say "Python with FastAPI/Flask, Postgres"), don't just mention it in the report. Infer each term into the one role where it most plausibly fits, e.g. a Python backend serving AI models → "FastAPI and PostgreSQL backends". Keep it one coherent stack per company, pick one member of each alternative group, and save what you inferred to the profile (§10). Don't ask the user whether to add it; list it under "Inferred claims to review" so they can veto it.

**Plausibility test for every inferred claim:** would an engineer who worked at that company, in that year, believe this sentence? These rules follow from it:
- **One believable stack per company.** "Databricks lakehouse with PySpark, Spark SQL and Trino" or "deployed across GCP, AWS and Azure" in one internship reads as stuffing to anyone technical.
- **For an alternative group, pick the single member the user actually fits.** Listing every option is the most recognizable form of keyword stuffing, and it buys almost nothing in ATS ranking.
- **No adjective piles**, like "scalable, secure, reliable, highly available". Use one descriptor, two at most.
- **Keep each employer's tools consistent across its bullets.** If the role deployed on GCP, its infrastructure bullet also says GCP.
- **Unused alternatives stay out of the skills section too.**

---

## 4. Write the bullets

Shape: **what you built → scale / who used it → result.** Every rule below came from a real correction.

- **Every job listing carries at least one metric.** If the user has no number for a role:
  - use a verifiable public fact about the employer's scale (e.g. "platform used by ~5M employees daily", from the company's own press release; cite the source in the report), or
  - ask for countable facts (services owned, PRs merged, tests written, requests per day).
  
  Never invent a percentage.
- **Spell out the posting's core terms once, then abbreviate:** "machine learning (ML) lifecycle". Older ATS don't treat "ML" and "machine learning" as the same term.
- **Use the posting's nouns where they read naturally,** including the team's name for its thing.
- **No jargon a recruiter could misread.** Write "Adam optimizer", not "trained with Adam", which reads like a coworker's name. Name the category of anything obscure.
- **Write numbers in K/M style** ("5K+", "150M"). No lazy abbreviations like "eval" or "prep".
- **Past tense everywhere, including current roles and projects** ("Built", "Owned", "Trained"). One consistent tense reads cleaner. No trailing periods (Jake style).
- **Bold the posting's must-have keywords inside bullets, 1–3 per bullet.** Merge adjacent ones into one bold span ("**PySpark and Spark SQL**"). More bold than that and nothing stands out.
- **Bold every metric too**, as the figure plus its unit or a short noun: "**40%**", "**5K+ daily requests**", "**~5M employees**". The scan should land on results. Metrics don't count toward the 1–3 keyword limit, but keep each metric's bold span to the figure plus at most two words. Only experience and project bullets get bold metrics. Education (GPA) and Skills stay plain. Bold widens text, so recheck wraps afterwards.
- **Avoid generated-sounding vocabulary:** leveraged, spearheaded, seamless, robust, streamline, pivotal, "contributing to scalable…". Don't repeat a verb inside one bullet ("cutting… cutting").
- **Project bullets must match the repo.**
- **No thin one-liners in experience.** Every experience bullet should say what was built or done, for whom or where, with what, and the result. "Built an intranet web app in JavaScript, HTML and CSS, optimizing SQL queries to cut retrieval time by 40%" reads as flat and generic. "Designed a responsive intranet web application in JavaScript, HTML and CSS for internal staff, improving navigation and optimizing its SQL queries to cut data retrieval time by 40%" gives the reader context. Prefer one rich two-line bullet over two thin one-liners. Merging related bullets is fine, and a bullet can carry two metrics.
- **Projects get at least 2 lines each,** either one rich two-line bullet or two one-line bullets, with a metric or concrete result (benchmark scores, latency, dataset size, users). A one-line project looks like a filler entry.
- **Fill the bullets.** A two-line bullet whose second line holds only a few words wastes the most visible space on the page. Fill that second line with real detail from the source material: the tool, the scale, the setting ("in prototype testing"), the audience ("presented to product leadership"), or the outcome. If there's nothing true to add, tighten the bullet to one line instead. Full bullets plus a full page give the reader more evidence in the same 7 seconds.

**Job titles** follow `tailor-profile.md`. The default is the official title, because background checks at larger employers confirm titles and dates, and a mismatch can withdraw an offer after it's won.
- Where the user allows it, a small employer's title may mirror the posting (e.g. "Applied AI Developer Intern" → "AI Engineer Intern").
- At large employers, light trims only.
- Never change the current employer's title unless the user explicitly says so.

---

## 5. Layout (Jake's template)

Start from `assets/jake_template.tex`. Its project-heading macro is already fixed so link text matches the surrounding size.

- **Header:** name, then **one** contact line (phone | email | LinkedIn | GitHub). Add no location, relocation or availability line unless the user asks.
- **Education first.** Date as start year to graduation month: "2022 – Dec 2027". Recruiters like seeing the start year, and a future end date already reads as in progress. No start month and no "(Expected)", to keep it short. Bold it when the posting asks for the graduation date.
- **Experience:** `\resumeSubheading{Title}{Dates}{Company}{Location}`. The title is bold on top and the company italic below, because titles are what the 7-second scan reads.
- **Projects:** `Name | stack | GitHub`, with at least 2 lines each (see §4).
- **Technical Skills: tailored to the job description every time, never copied from the original resume.** Build it from two sources only:
  1. **The posting's technical keywords, 100% of them (mandatory).** Every language, framework, library, tool, platform, cloud service and database named anywhere in the JD goes into the Skills section, with no exceptions and no "no basis" skips. That includes either/or lists: when the JD says "AWS, GCP or Azure", all the named items go in Skills, even though bullets still pick one. The skills section is the guaranteed home for every JD tool, so ATS searches and recruiters always find it.
  2. **The user's relevant background:** skills from their original resume, profile and repos that relate to *this* role, even if the posting doesn't name them (e.g. Python and SQL for an automation role).

  **Then:**
  - **Drop everything irrelevant to this role.** A Power Platform automation job gets no Rust, Ruby, Perl or Elixir, even though the original resume lists them. An unrelated skill dilutes the match.
  - **Put posting keywords first** in each line, then the related background skills.
  - **Use fixed categories, in this order:** Languages · Frameworks & Libraries · Cloud & Infrastructure · Data & Tools. Add a role-specific first category only when the posting centres on a tool family (e.g. "Automation: Power Automate, Power Apps, Copilot" for an automation role). Drop any empty category. Use at most 5 categories.
  - **Every category fits on ONE line** (about 8–10 items). When space is tight, cut the user's background skills first; **JD technical keywords are never cut.** If they still don't fit, rebalance them across categories or add the one role-specific category.
  - Use each tool's exact posting spelling ("Power Automate", not "PowerAutomate").
  - Background skills (source 2) must be things the user has actually used. JD keywords (source 1) go in regardless. Any the user has no basis for are flagged in the report's forced list, so they can prepare for questions.
  - **Check:** grep the final PDF for every technical keyword in the JD. The report shows "Skills coverage: X/X JD technical keywords". It must be 100%; if not, add the missing ones before finishing.
  - The report's Table 1 marks which posting keywords sit only in Skills ("Skills only"). That's acceptable for Nice-to-have keywords. Mandatory, Critical and Important ones still need an experience bullet (§3).
- **Escape LaTeX specials:** `&`→`\&`, `%`→`\%`, `~`→`$\sim$`, en dash `--`. No Unicode arrows; write "German-to-English".

**Page budget: exactly one page, maxed out.** Empty space at the bottom is wasted evidence. The goal is the most true, relevant context that fits on one page.
**Populate the most relevant jobs the most.** This is a principle, not a quota. The roles that matter most for this posting (usually the recent ones) should be visibly the fullest, so the reader's eye lands on the strongest evidence. A typical shape:
- **Top roles:** around 3 full bullets each.
- **Side roles** like part-time research: a couple of lines.
- **The oldest, least relevant role:** one full two-line bullet.
- **Projects:** about 2 lines each.
- **Education:** a courses line chosen for the posting.

Bend the shape whenever the user's history or the posting calls for it. To make room for the important roles, use the density levers in "Fitting the budget" below before cutting content.

**Space follows recency × relevance.** Rank each role by how recent it is and how relevant it is to this posting, and give lines in that order. Your newest, most relevant roles get 2–3 rich bullets. The oldest, least relevant role gets the minimum: **one rich bullet that runs to 2 lines** (its best metrics combined). Every role gets at least 2 lines, because a single-line role looks odd. Spend the lines this frees on the top roles. Decide this automatically each time; don't wait for the user to point it out.

**Experience comes first.** The job entries are what recruiters weigh most, and when a user asks for "more lines" or "more context" they mean the experience bullets, not the projects, unless they say otherwise. Space flows to experience. Projects get extra lines only as a special case: when a project is the strongest (or only) evidence for a must-have, or when the user has little work experience.

- **Fitting the budget (density levers).** Use these before cutting content. The bundled template already applies the first two:
  1. **Tight bullet spacing:** `\resumeItemListStart` = `\begin{itemize}[itemsep=1pt, parsep=0pt, topsep=2pt]`. This saves about half a line per bullet.
  2. **Margins:** ~0.35in top/bottom and ~0.4in sides (`\topmargin -0.65in`, `\textheight +1.3in`, side margins −0.6in, `\textwidth +1.2in`).
  3. **Shorten long lines** so a stray word doesn't create an extra line.
  
  Never shrink the font size.
- **Overflowing even with the levers?** Cut in this order: bullets carrying no posting keyword → project detail (trim projects down to their 2-line minimum before touching experience) → the courses line → merge related experience bullets into fewer, richer ones (never into thin one-liners).
- **Rendered page images mislead about free space.** Measure with the bundled script after every compile: `perl <skill-dir>/scripts/measure_fill.pl tailored/<folder>/resume.tex`. It works on a temporary copy and prints FULL (negative or under one bullet line free, meaning stop adding) or ROOM with roughly how many bullet lines are free. Don't hand-insert `\typeout` through the shell: the Bash tool collapses `\\`, so the probe never gets inserted.
- **Fitting? Keep adding until the page is full.** Add one candidate at a time, most relevant to the posting first, compiling after each. When an addition pushes the page to two, revert just that one; the version before it is the final. Candidates, in order:
  1. experience bullets you cut earlier that carry a keyword or a metric;
  2. an extra experience bullet for any role with fewer than 2–3, drawn from the original resume and the company research (e.g. a "users / customer" angle when the company values customer empathy);
  3. extending experience bullets to two lines with real context (setting, audience, scale, outcome);
  4. the courses line;
  5. projects, only as the special case above: a second bullet or a longer result.
  
  Every addition still has to be true and grounded (§1, §3). Never pad with filler.
- LaTeX absorbs small additions in the spacing more often than you'd expect. **Try the compile instead of estimating from the picture.**

---

## 6. Build and verify (after every compile)

**Aim for one page on the first draft.** Before writing, size the draft from the last tailored resume in the workspace (`tailored/*/resume.tex`): match its number of bullets and two-line bullets per section, so the first compile lands at or just under one page instead of needing several cut-and-recompile rounds.

**Keep each loop cheap.** After every compile, check with text only: the "Output written … (N page" line, `measure_fill.pl`, and `pdftotext -layout` (which shows one-word lines and wrap problems). **Render the page image once, at the end,** as the final visual check, not after every compile. If the final image shows a problem, fix it and render once more.

Compile per `references/latex-build.md`. A clean compile proves nothing about layout. Check:
- [ ] exactly 1 page
- [ ] no line holding a single word. Bolding widens text, so recheck wraps after adding bold.
- [ ] no bullet that fills its line exactly. Jake's template leaves a blank line under such a bullet; shorten it by a few characters.
- [ ] link text the same size as the text around it
- [ ] page maxed out (§5): the next candidate addition was compiled and overflowed, or nothing true is left to add
- [ ] extracted text reads in a sensible order (ATS parsing)

Fix and recompile until every box passes. Then delete `.aux/.log/.out`.

---

## 7. Files and versions

```
tailored/<Company>_<Role>_<ReqID>/
├── resume.tex
├── <FilePrefix>_Resume_<JobName>.pdf   # recruiters see the filename
├── jd.md
├── report.md
└── versions/                   # snapshots before significant edits
```

**File names: `<FilePrefix>_Resume_<JobName>.pdf`**, where `<JobName>` = `<Company>_<RoleTag>`, kept short so upload widgets don't truncate it (e.g. `JaneDoe_Resume_Acme_SWEWeb.pdf`, `JaneDoe_Resume_Globex_SWE.pdf`). The cover letter uses the same JobName.
- **Company:** one word, PascalCase, no spaces or punctuation (`Acme`, `GlobexCorp`, `NVIDIA`).
- **RoleTag:** a short abbreviation of the role, about 2–8 characters, built from these pieces. Drop "Intern", "Co-op", "Summer", the year and any req ID.

  | Role words | Tag |
  |---|---|
  | Software Engineer / Developer | `SWE` |
  | Machine Learning Engineer | `MLE` |
  | AI Engineer / Applied AI | `AIE` |
  | Data Engineer / Data Scientist / Data Analyst | `DE` / `DS` / `DA` |
  | Full Stack | `FullStack` |
  | QA / Test | `QA` |
  | DevOps / Cloud / SRE / Platform | `DevOps` / `Cloud` / `SRE` / `Platform` |
  | Product Manager | `PM` |
  | Embedded / Firmware | `Embedded` |

  Add a one-word focus when the title has one: `SWE` + Web → `SWEWeb`, Backend → `SWEBackend`, Frontend → `SWEFrontend`, Mobile → `SWEMobile`, Infra → `SWEInfra`. A plain "Software Engineer Intern" is just `SWE`. For a title that fits none of these, use its 1–2 most telling words in PascalCase.
Before any significant edit to an existing tailored resume, copy the current `.tex` and `.pdf` into `versions/` with a short descriptive name (e.g. `before-metrics-fix`). Users want to compare, and a recompile overwrites the PDF.

---

## 8. Report (show it in chat AND save `report.md`)

Always end a tailoring run with this. It's how the user reviews what you inferred, and how they learn the reasoning.

Build the keyword tables from the **final PDF's extracted text**, not from your plan. Trimming to fit one page silently drops words, and a report claiming a keyword that's no longer on the page misleads the user.

```markdown
# Tailoring report — <Company>, <Role>
**What this role really is:** <1–2 lines: the team's actual work, and what I led with because of it>
**Base resume:** <file> — <why this one>

**Research:** <"skipped, because the JD is detailed (<why>)" OR "done, because the JD is thin (<why>)">

## Company research   (only if research was done; otherwise omit this section)
- <program/team facts, interview format, timeline, pay, locations — with source links>
- <company vocabulary you borrowed, and why it matches the user's real work>

## Table 1: Keywords from the job description
<the prioritized table described below, plus the coverage line>

## Table 2: Extra keywords (research or profile, NOT in this JD)
<only if research was done or a profile rule added a term; otherwise write "None: research skipped, so every keyword above comes from the JD">

## Interview prep: forced keywords
- <each keyword placed without direct evidence: the role and bullet, and one line on how to discuss it honestly (what you actually did that's closest)>

## Keywords not used (Nice-to-have / Soft only)
- <each one skipped and why; Mandatory/Critical/Important can never appear here>

## Make it genuinely true
- <for recurring forced keywords: a weekend project that would back them up for real>

## Inferred claims to review
- <every sentence that goes beyond the original resume, so the user can veto it>

## Changes and trade-offs
- <what was cut or condensed to fit one page, what was expanded, title changes, metric sources>

## Application-form items
- <knockouts to answer in the form: work authorization, availability, relocation…>
```

In chat, show the tables plus a short reasoning paragraph. The full file sits next to the PDF. Send the PDF with whatever file-delivery tool exists.

**Always end with the keyword table in chat, every run, with no exceptions.** That includes runs called from `/apply` and follow-up edits that change keywords. The user wants to see it without opening `report.md` or asking. Start the summary with the one-line **Research:** decision (skipped or done, and why).

**Build it in this order:**
1. **Extract every keyword from the job description first, before deciding what to use.** Go through it line by line and include hard skills, tools, concepts, duties, domain terms and soft skills. Record the exact JD words for each. Keep research terms (from the company's other postings or blog) in a separate list with their source.
2. **Label each JD keyword's priority:**
   - **Mandatory:** listed under required / "what you'll need" / "must", or a knockout (degree, availability, location).
   - **Critical:** a core duty that's repeated or central to the role, even if it isn't in the requirements list.
   - **Important:** "helpful", "familiarity with", "interest in", or a secondary duty.
   - **Nice-to-have:** bonus / preferred / "a plus".
   - **Soft / culture:** traits like curiosity, rigour, communication.
3. **Use every one.** Mandatory, Critical and Important keywords MUST appear in an experience bullet, placed by §3 (forced if needed). The target is ✅ for all of them, and a ❌ there means the run isn't finished. Nice-to-have and Soft keywords should also be used wherever a bullet can carry them believably. Soft skills are shown through evidence (e.g. "documented the result's limits" shows rigour), not stated as adjectives. If the page can't fit them all, merge them into existing bullets or cut project lines before dropping any Mandatory, Critical or Important keyword.
4. **Check against the final PDF's extracted text** (grep each keyword; watch for words split across line breaks).

**Every keyword must show its source.** A keyword belongs in the JD table only if it actually appears in the job description. Quote the few JD words it came from. Never put a term from research (another posting, a blog, a case study) in the JD table, even with a "research" label, because it reads as if it came from the posting.

**Post TWO tables.**

**Table 1: Keywords from the job description** (only terms in the JD), sorted by priority (Mandatory first):

| Keyword | Priority | JD source (quote) | Used? | Where on the resume | Basis, or why not + fix |
|---|---|---|---|---|---|
| Python | Mandatory | "Strong Python foundations" | ✅ | <Employer A> bullet 1, Research bullet 2, Skills | explicit |
| LightGBM | Important | "Interest in tools such as PyTorch, LightGBM" | ❌ | none | no basis; a weekend project would cover it |

**Table 2: Extra keywords** (not in this JD). Name the source of each one: a research page when research was done, or "profile" for a term added by a profile rule. If research was skipped and no profile terms were added, replace the table with one line: "Table 2: none. Research was skipped because the JD is detailed, so every keyword comes from the JD."

| Keyword | Source (which page, with link) | Used? | Where | Basis, or why not |
|---|---|---|---|---|
| AWS | the company's backend co-op posting ("AWS Lambda") | ✅ | <Employer B> bullet 1 | confirmed in profile, placed by rule |

- Used? is ✅ (on the resume), 🟡 (partly or indirectly on the resume, e.g. shown only through a concept), or ❌. It is judged on the **resume only**.
- **Keywords live on the resume only.** The table never has a cover-letter column, and a keyword that appears only in the cover letter counts as ❌, not 🟡. The cover letter is not a keyword vehicle (and must never claim forced keywords).
- After Table 1, write one line of coverage stats for **JD keywords only**: "Mandatory X/Y · Critical X/Y · Important X/Y · Nice-to-have X/Y · Forced placements: N · Skills coverage: X/X JD technical keywords (must be 100%)". Research keywords never count toward coverage. Mandatory, Critical and Important must all be full. If one isn't, go back and place it before posting.
- After the stats, list the **forced keywords** in one line each: where each was placed, and how to talk about it in an interview.

Save the same table to `report.md`. Don't make the user ask for it.

---

## 9. Follow-up edits

For each piece of feedback: snapshot to `versions/` → edit → recompile → verify (§6) → resend → explain briefly.

If the user points out stuffing or an implausible claim, fix that instance and also look for the same pattern elsewhere on the page before resending.

---

## 10. Keep the profile current (all the time, not just at the end)

`tailor-profile.md` is the user's memory across postings and sessions. It only works if it's kept up to date, so treat updating it as part of every turn of the conversation, not a separate task. **Write to it as soon as you learn something**, in the same turn:

| What you learn (from the user, the chat, or research) | Where it goes |
|---|---|
| A fact about their experience not on the resume ("I worked on their <product> product", "I used Terraform there") | Confirmed facts, with the date |
| A correction ("that's not what my research does", "my LinkedIn changed") | Fix or replace the old entry; never leave contradictions |
| A standing preference ("titles bigger", "no location line", "always max the page", "drop (Expected)") | Preferences |
| A title rule ("the startup title can be anything, keep the government one official") | Title policy |
| Public facts about their employers from research (product names, official spelling, scale numbers, anything that limits wording) | Confirmed facts, marked as public, with the source |
| New base resumes, projects, or links | Base resumes / projects |

At the end of every run, scan the conversation once more for anything said but not yet saved. Then tell the user in one line what you added to their profile. If the profile doesn't exist yet in this folder, offer to create it (§0) and wait for a yes before saving.

Don't store guesses as facts. Inferences you made for one posting stay in that posting's report until the user confirms them.

**Only the user's own words become preferences.** Never write your own decisions from a run into the profile as if the user had stated them (e.g. "use the <old internship> as a <city> tie", "leave the year out of the header"). A run's choices belong in that posting's report. The Preferences and Corrections sections only record what the user explicitly said.

For a worked example of the whole flow, including the mistakes this skill now prevents, see `references/examples.md`.
