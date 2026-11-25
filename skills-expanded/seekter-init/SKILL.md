---
name: seekter-init
description: Set up Seekter for a new candidate. Interviews the user one question at a time and writes profile/profile.md, profile/settings.json and profile/documents/. Use when the user runs /seekter-init, says "set up seekter", or when profile/profile.md is missing.
---

# /seekter-init — build the candidate profile

The goal is a complete `profile/profile.md` (from `templates/profile.md`) and `profile/settings.json` (from `templates/settings.json`). Every other Seekter skill reads only these files, so nothing may be guessed here: a value the user didn't give stays `ASK` in the profile, and a setting they didn't answer keeps the template's default.

## Rules for the interview

- **One question per message.** Short, plain, in the user's language. Offer choices with the question tool when the answer is one of a few options; free text otherwise.
- **Draft, then confirm.** If a resume (or a LinkedIn profile saved as PDF) is available, read it first and turn questions into confirmations ("Your resume says 8 years in this field. Correct?"). Never write a value from the resume without the user confirming it.
- **Skippable.** "Skip" or "later" writes `ASK` and moves on. Sensitive items (birth date, ethnicity, disability, gender, salary history) default to "prefer not to say" unless the user volunteers a value.
- **Resumable.** After each answered section, save progress to `profile/.init-state.json` (`{"done": ["identity", ...], "answers": {...}}`) and write what's known into `profile/profile.md`. Settings are written the moment they are answered, not at the end of a section. On restart, read the state file, say where you're resuming, and continue.
- **A half-finished setup still runs.** Only three profile values have no default: the application email, the default resume and the country. With those three in place, `/seekter-run` works; every other gap is asked when a form needs it, and every unanswered setting runs on its default.
- **Explain once why** at the start, right after the disclaimer: "I'll ask about 40 short questions in 9 groups. Everything stays in `profile/`, which git ignores."
- Don't ask what you can derive: timezone from city, ASCII fallback from name, E.164 phone from local number + country.

## Order

**Before anything else: the disclaimer.** Show this, as one message, before creating a folder or reading a file:

> Before we start: Seekter sends applications in your name and you are responsible for what they say, the terms of the job sites you use are yours to follow, and it runs on your own paid Claude plan with no guarantee of results. Details are in [DISCLAIMER.md](DISCLAIMER.md). Shall we continue? (yes / no)

- **No**, or anything that is not a yes: stop. Create nothing, write nothing, and say they can run `/seekter-init` again whenever they want.
- **Yes**: keep the date in `profile/.init-state.json` and write it to the profile's `Disclaimer accepted:` line when the profile is first written. Then run `node scripts/seekter.mjs settings > /dev/null`: it moves an older `profile/search.json` to `profile/settings.json` with its values intact, or copies `templates/settings.json` if there is neither, so a valid settings file is there before the first question. Never copy the template by hand: on an older setup that would shadow the user's `search.json`. Then continue.
- Don't paraphrase it into something softer or longer, and don't ask it again on a resumed run that already has the date.

0. **Setup check.** Create `profile/`, `profile/documents/`, `applications/`, `runs/` if missing. If `profile/profile.md` already exists, ask: update section by section, or start over (keep a copy as `profile/profile.backup-<date>.md`). An older setup may have `profile/search.json` instead of `profile/settings.json`: `node scripts/seekter.mjs settings` moves it across with its values unchanged, so don't rebuild it.
1. **Documents first** (they make the rest faster). Ask for the resume file path(s). Copy them into `profile/documents/` keeping the file name. Ask which is the default and whether another resume is for a different role type. Optional: portfolio PDF.
   Read the resume and pre-fill a draft of §1, §3 (employer, years, education), §8 (work history, facts, stack, certifications).
2. **Identity and contact (§1).** Name as written on the resume, first/last split, **the one email to use in every form**, phone, city + country + postcode, nationality, languages with levels, portfolio / LinkedIn / GitHub / other links, case-study URLs.
3. **Targets (§5).** Titles to apply for (suggest from resume), titles and seniority to exclude, management vs individual contributor, a one-paragraph recruiter statement (draft it, let them edit).
4. **Location and work model (§6).** Work authorization (where they may legally work today). For the home country: on-site / hybrid / remote allowed, and city exceptions. Relocation: yes/no, which countries in priority order, conditions (only with sponsorship?), regions never to relocate to.
5. **Money (§4).** Bands by employer region (monthly or annual, gross or net, currency). Minimum acceptable. Freelance rate if relevant. Salary history answer (a number or "prefer not to say").
6. **Standard answers (§3).** Notice period, contract types (employee / contractor / EOR), VAT or company registration, sponsorship need for remote vs relocation, non-compete, background questions, references, education search terms, AI-usage level, consents. Demographics last, with "prefer not to say" as the first option.
7. **Boundaries (§7).** Sectors never to apply to (offer: gambling/betting, adult, weapons/defense, tobacco, crypto, fast fashion, none). Companies to never apply to. Sectors to ask about first.
8. **Fact bank and stories (§8).** Walk through each job on the resume and ask for **2–3 concrete facts** each (a number, a product, a decision, a tool combination). Then ask for 3 short stories for behavioural questions: a time they were wrong, a conflict, a failure, a system they built outside work. Only facts and stories captured here may appear in applications.
9. **Voice (§9).** Show two short sample answers in different registers and ask which sounds like them. Ask for phrases they hate. Ask about punctuation habits (em dashes, exclamation marks) and US vs UK English.
10. **Search config.** Fill the search keys of `profile/settings.json`. **Every search value is theirs; the template ships them empty on purpose, so fill them from this candidate's field and geography rather than from an example.** Switches with a sensible default (`same_company_days`, `linkedin.read_limits`, `freehire.window_days`) stay as they are unless the user wants them changed; say what each one does in a line and move on.
    - freehire `queries` (their target titles, lowercase) and `categories`: don't guess the taxonomy — run `curl -sS -A seekter "https://freehire.me/api/v1/jobs/facets?q=<their main title>"` and pick the categories that actually carry their field, then show them the counts.
    - `regions` and `home_country` from §6; `languages` from §1.
    - `title_keep`: the title families worth opening. `title_drop`: wrong seniority **plus the other industries that share their job title** — ask them which ones ("who else calls themselves this?"), because they know their field's collisions and you don't. The template's `_title_filters` comment holds a worked example from another discipline; use its shape, not its words.
    - **Platforms: show, don't ask them to remember.** Run `node scripts/catalog.mjs platforms --country <their country> --discipline <design|engineering|product|…>` and show the list in one message, grouped: what always runs (freehire, the company career sites), LinkedIn, and the boards that fit their country and field, each with its one-line note and whether it needs an account. Everything open is picked by default; they drop what they don't want and may name a board that isn't listed. Write each kept board to `boards` with the cadence shown (they can change it). A board they name that has no file in `reference/sources/` has never been measured: write it, and say the first run will measure it. Ask about relocation from §6 first, and pass `--relocation` if they would move, so the relocation-only boards (XING, Dice) appear.
    - **LinkedIn, if they kept it,** gets its own questions next (the two bullets below), because its mode carries a risk to their account.
    - LinkedIn `searches`: one row per title family × geography (`keywords`, `location` for the alert, `geo_id` from the table in `reference/sources/linkedin.md`, `remote` per §6), plus a second row without the remote flag for any geography where they can work on-site. Each row is a job alert **they** create on LinkedIn, delivered by **Email**, and in `read` mode also a search Seekter runs. Apply the alert-quality rules from the same file while building the rows (no quotes, one row per title variant, EEA leaves out the UK and Switzerland, narrow beats broad because a digest mail shows only about six postings).
    - LinkedIn `mode`: ask, and say this first, in plain words: "Seekter never fills Easy Apply and never takes an action on LinkedIn. By default it doesn't open LinkedIn at all: it reads your job-alert emails and any links you give it. It can also read LinkedIn searches and job details itself, with a daily limit and pauses, and it turns that off at the first warning. That is still against LinkedIn's terms, and LinkedIn can restrict accounts that do it. The risk is to your account. Do you want it on?" `email` unless they say yes; on a yes, write `read` and quote their answer in the profile's §10.
    - **Companies, after the platforms.** Run `node scripts/catalog.mjs employers --country <their country> --discipline <field>` (add `--relocation` if they would move, and `--exclude-sectors` with the sectors they ruled out in §7). It prints the companies from `reference/employers/catalog.json` that hire from their own career sites where this candidate can work: **A** says it hires in their country, **B** is remote in a region that includes it, **C** office roles for relocation. Show the count per letter and the names, briefly grouped; the default is **add them all** (rerun with `--add`), and they can drop any or name companies of their own (a company they name gets a row only once its board answers: find its system and slug as in `reference/sources/direct-employer.md`). Say in one line that every run reads these boards, and that a company with nothing open today is still worth keeping.
    Show the finished search config and let them trim it.
11. **Tracker import (optional).** Ask whether they already track applications somewhere. Notion or any spreadsheet → export as CSV → `node scripts/import_csv.mjs <file>.csv --dry-run`, show the counts, then run it for real. This is what makes dedup work from day one.
12. **Finish.** Write the final `profile/profile.md` (fill §10–§12, set "Last updated"), delete `profile/.init-state.json`, run `node scripts/seekter.mjs index`, then print:
    - which fields are still `ASK` (each one line),
    - the browser prerequisite (Claude in Chrome extension, with their webmail logged in in the same Chrome),
    - the LinkedIn alerts to create by hand, one line each from `linkedin.searches`, delivered by Email,
    - that they can drop links they find into `profile/links.txt` (or paste them in chat) and those are filled first,
    - the next command: `/seekter-run`.

## Writing the files

- `profile/profile.md`: copy `templates/profile.md`, replace every `{{…}}`. Remove table rows that don't apply rather than leaving placeholders. Leave no `{{` in the finished file (check with grep).
- `profile/settings.json`: valid JSON, and `node scripts/seekter.mjs settings --check` passes. It lists the settings still on their defaults; read that list out so the user knows what they can change by hand.
- Keep the user's exact words for rules they state; quote them in the profile, as they're the ground truth later.
