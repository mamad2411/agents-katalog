---
name: test-stack-discovery
description: Deeply studies how the user's own test automation is built — inside the product repo or in a separate test repo — in focused sessions that each write their own file in `.qa-skills/`, the repo's long-term memory for other QA skills. It covers stack and how to run every suite (e2e UI, API, contract, unit, performance, mobile); the architecture (Page Objects, Screenplay, services, step layers, how far the code really follows OOP or is inconsistent); how test cases are written (Gherkin/BDD and its step definitions, test-case docs, title patterns, Jira/Xray/TestRail traceability); naming, selector and assertion conventions and the team's rules; step-by-step recipes for adding a test, a page object, a step, a fixture or a factory the way the team does; test data, auth, environments, CI and coverage per area — with file:line evidence for every claim. Use whenever the user wants to understand, map, document, onboard onto or learn the patterns of a test/automation project, or before writing new automated tests where conventions aren't known yet — e.g. "analyze my test repo", "learn our test conventions", "entende meu projeto de testes", "mapeia a stack e a arquitetura da automação", "como esse repo de testes funciona?", "analiza mi repositorio de pruebas". Read-only: never runs the tests or copies secrets.
---

# Test Stack Discovery

Study the user's tests the way a senior automation engineer studies a codebase in their first week on a team — patiently, file by file, until they could write a new test that nobody would notice wasn't written by the team. Then write that knowledge down in `.qa-skills/`, where other skills (automation, test design, review, exploratory) read it before they work.

**This skill is meant to be slow and thorough.** Its output is reused by every later skill, many times, so a gap or a wrong guess here is multiplied downstream. Take the time to read the architecture for real, follow how a test flows through its layers, and confirm every convention with counts. Speed is not a goal; fidelity is.

It **reads and documents** — it never runs tests, installs dependencies or edits the user's code; it writes only inside `.qa-skills/`.

**What to read, and when:** [references/output-index.md](references/output-index.md) at the start (the index contract, markers and session-file rules). Each session's template in [references/templates/](references/templates/) only when you're about to write that session's file. [references/architecture-assessment.md](references/architecture-assessment.md) in session 2. [references/where-to-look.md](references/where-to-look.md) only for the ecosystem and topic you need — list its headings with `grep -n '^#' references/where-to-look.md` and read just that section. [references/labels.md](references/labels.md) only when talking to the user in a language other than English.

## Reading economy
Thorough doesn't mean wasteful. Every tool call re-sends the whole conversation, so the cost of a discovery grows with the number of calls and the size of what each one prints. Spend the budget on understanding the code, not on mechanics:
- **Start with the inventory script** (session 0): one call replaces dozens of `ls`/`grep`/`git` calls.
- **Read each file once, and take what you need from it the first time.** Later sessions reuse what earlier ones learned — refer back to your own notes and session files instead of re-reading code.
- **Batch small files** into one read (`for f in a b c; do echo "== $f"; cat -n "$f"; done`) and **read big files by range** (`sed -n '40,120p'`) after locating what matters with `grep -n`. Keep a single command's output under roughly 15k characters; split it rather than produce one that has to be saved and re-read.
- **Count instead of listing**: `grep -c`, `grep -o … | sort | uniq -c`, `wc -l` give the numbers the files need without printing every match.
- **Never print** lockfile bodies, OpenAPI/swagger files, compiled or minified code, generated reports or binary files — search them for the one fact you need.
- **Don't re-read this skill's references** once loaded; open a template only for the session you're writing.

## Language
Look for `.qa-skills.yaml` in the test repo's root, then `~/.qa-skills.yaml`. `language` is for what you say to the user; `report_language` (default: `language`) is for the prose inside the `.qa-skills/` files. Section titles, fixed table rows and markers in the files are always in English, because other skills look them up by name. An explicit request overrides the file — one that targets only the files changes only the files; any other changes both. Otherwise use the language of the user's message. Don't mention a missing file. Code, identifiers, test titles, Gherkin steps and messages are quoted as they are, never translated.

## Source fidelity
Another skill will generate code from these files without double-checking them. A guessed framework version, an assumed `npm` when the team uses `yarn`, or a "Page Object" claim based on one file produces code the team has to rewrite — or worse, code that looks right and quietly breaks their conventions. An honest `⚠️ UNCERTAIN` costs far less.

- **Every claim carries evidence** as `path:line`, or `path` for whole-file facts. Paths are relative to the test repo; for files in a separate product repo, prefix them with `product:` (`product:src/routes.ts:12`). A commit (`a1b2c3d "Move new tests to JUnit 5"`) is valid evidence for *when* a convention changed. Patterns seen across files say how many and of what: "`test.step` in 19/20 tests", "`getByRole` in 15/17 locators".
- **Declared beats inferred.** A config value, dependency or written rule is a fact. A convention seen in the code is an observation — say so with the count. Something you can't back with a file becomes an `⚠️ UNCERTAIN` entry and, if it matters for writing tests, a question.
- **Describe, don't prescribe.** Record how the team *does* it, including the inconsistent parts. Your opinion of what would be better belongs only in the architecture assessment, clearly labeled, never in the rules a generator follows.
- **Never invent:** versions not in a manifest/lockfile/toolchain file, scripts/profiles/flags that don't exist, environments or env vars not referenced in code, CI that isn't there, how the app is started when nothing says so, helpers or base classes that don't exist. Two things are allowed because they can't send anyone the wrong way: a command built from something declared (a Maven profile in the pom → `-Psmoke`, with the pom line as evidence), and the tool's own standard CLI syntax for something the repo doesn't document — labeled `(standard <tool> CLI, not documented in repo)`.
- **Secrets never leave their file.** Record only *names* and *locations*: env var names, "credentials are hardcoded in `support/users.ts:9`", "`playwright/.auth/user.json` is generated storage state". Don't open `.env`, storage-state/cookie files, keystores or credential files beyond what's needed to list variable names; never copy a password, token, key, cookie, connection string with credentials or test-account password into the files or the chat (a test username or email alone isn't a secret). Non-secret config values — `localhost` URLs, timeouts, browser lists, committed base URLs — can be quoted.

## How the work is organized
The discovery runs as **eight sessions**, in order. Each session has one focus, ends by writing (or completing) its file, and records itself as done in the index before the next one starts. Working this way keeps attention on one subject at a time, makes later sessions build on what earlier ones confirmed, and means nothing learned is lost if the conversation is cut short — a re-run picks up from the first session not marked done.

| # | Session | Writes | Focus |
|---|---|---|---|
| 0 | Reconnaissance | `test-stack.md` (index) | repositories and layout, suites, documented rules, inventory |
| 1 | Stack and execution | `test-stack/stack.md` | per suite: versions, libraries, how to run, folder structure |
| 2 | Architecture | `test-stack/architecture.md` | layers, how a test flows through them, OOP and consistency assessment |
| 3 | Test case writing | `test-stack/test-case-writing.md` | Gherkin/BDD and step definitions, titles, test-case docs, traceability |
| 4 | Conventions and rules | `test-stack/conventions.md` | naming, selectors/requests, assertions, waits, hooks, style, team rules, rules for new tests |
| 5 | Data, auth, environments, CI | `test-stack/environment-and-data.md` | test data lifecycle, authentication, config and env vars, app under test, CI |
| 6 | Recipes | `test-stack/recipes.md` | step-by-step: how to add each kind of artifact the way the team does, with skeletons and reference tests |
| 7 | Coverage and review | index (coverage, uncertainties) | what each area has covered, final skeptical review, questions |

Each session file has a template with the same name in `references/templates/` (`stack.md`, `architecture.md`…); open it when the session's investigation is done and you're ready to write. Write each file as soon as its session ends — don't hold everything for the end. In each session, before writing, ask yourself: *could a new engineer, given only this file and the code, do this part of the job the way the team does?* If not, keep reading.

Several suites: every session file has one `## Suite: <name>` section per suite (plus a short shared section when suites share code), so a reader asked to write an API test reads only the API parts.

## Session 0 — Reconnaissance

**Find the repositories.** There are three layouts:

| Layout | Where `.qa-skills/` goes | What you read from the product |
|---|---|---|
| **A. Tests inside the product repo** | product repo root | only what the tests depend on, from the same repo |
| **B. Separate test repo, product repo available** | **test repo** root | only what the tests depend on, from the product repo |
| **C. Separate test repo, product not available** | test repo root | nothing — every test-side fact is documented; how the app is reached and started becomes a question |

- **The user gave a path** → that's the repo to analyze. **Otherwise** look at the folders open in the workspace (working directory plus added dirs). Skip folders that are only a skill collection (mostly `skills/*/SKILL.md`, no test code — like the qa-skills repo itself). A repo that contains `.claude/`, `.agents/`, `_bmad/` or other AI-agent folders is still a normal repo.
- **Separate test repo?** Look for its product among the other workspace folders and the test repo's siblings on disk, using the pairing signals in where-to-look.md (matching names, baseURL port vs the product's dev port, routes and tables the tests use existing in the product, README links). Paired → layout B; say which folder you paired and why. Not found → layout C; record the product's git URL or name if the README/CI mentions it.
- No candidate with test code → ask **one** question for the path, mentioning `/add-dir <path>` (Claude Code) or "Add folder to workspace". Several unrelated test repos → ask which one, in the same question.

**AI-agent content inside the target.** Agent skill libraries, knowledge bases and generated agent output are not part of the suite: leave them out of counts and don't mine them for conventions — generic advice there says nothing about how *this* team writes tests. The exception is anything written *for this repo*: context files (`AGENTS.md`, `CLAUDE.md`, `project-context.md`, `.github/copilot-instructions.md`, `.cursor/rules`), customized agent config (e.g. `_bmad/custom/*.toml`) and agent skills or agents that cite this repo's own files — the inventory script lists them. They are the team's documented rules: read them like a CONTRIBUTING and check the code still follows them.

**Inventory** — run the bundled script, adding the product folder once you've found it:

```bash
python3 -I <this skill's folder>/scripts/inventory.py <test repo> [--product <product repo>]
```

It prints, compactly and without file contents or secret values: folder and extension counts (AI-agent and vendor folders excluded and reported), test files by folder, test/scenario counts (including Gherkin keywords, language and tag patterns), the most imported modules, declared versions and scripts from manifests, lockfile type, toolchain files, rule/context files, repo-specific files inside AI folders, docs, CI, recent history and most-changed test files, and for the product its folders, route candidates and migrations. Treat its output as leads to confirm, not as findings: a count is evidence once you know what it counted. If Python isn't available, do the same by hand (`git ls-files`, a find that skips `node_modules`, `target`, `build`, `dist`, `.venv`, reports and caches).

**Find every suite.** A suite is a group of tests with its own type, stack and way of running: e2e UI, API, contract, unit, component, performance, mobile. Find them all and treat **each one with the same depth** — developer unit tests count as much as the QA e2e suite, because later skills may be asked to extend any of them. Name suites by type (`e2e`, `api`, `unit`…), adding a qualifier only to tell two of the same type apart (`api-payments`). Decide by how tests are written and run, not by folder name (see where-to-look.md).

**List the documented rules** — README, CONTRIBUTING, `docs/`, PR templates, agent context files, lint/format configs, commit conventions. Just locate them here; sessions 3–5 read them in depth.

**Existing `.qa-skills/` files?** Read them now. Entries marked `(confirmed by QA)` must be carried into the new files. Follow "Writing files" below for how to save the new version. If the index has a Sessions table with sessions marked done *and its commit matches HEAD*, you're resuming an interrupted run: continue from the first session not done.

Write the index from [output-index.md](references/output-index.md) with header, Summary (provisional), Repositories, Suites and the Sessions table (session 0 done, the rest `pending`).

## Session 1 — Stack and execution
For each suite: language and runtime versions, package manager, frameworks and libraries with declared and locked versions, runner, assertion and reporting libraries, lint/format; every way to run it (install, all, one file/test, by tag, debug/UI mode, report) from scripts, README, CI and build files — **never executed**; and the folder structure with the role of each folder and where new files go. Read manifests, lockfiles, toolchain files and runner configs in full; they are small and they're facts.

## Session 2 — Architecture
This is the heart of the discovery: understand how the code is *built*, so a new test fits into it instead of beside it. Read [architecture-assessment.md](references/architecture-assessment.md) first.

- **Read the structural code in full**: every base class, page object/component, service/client, step-definition class, fixture/hook file and support module — they're what a new test plugs into. Only when a layer has many similar files (dozens of page objects), read a representative sample from different areas and ages and confirm the rest with grep (class declarations, `extends`, constructors, exported functions).
- **Trace one test end to end**, for each suite: from the spec/feature, through fixtures or step definitions, into page objects/services, down to the framework calls and assertions. Write that path down — it's the clearest picture of the architecture.
- **Map the layers** and who depends on whom, how objects are created and handed to tests (fixtures, constructors, dependency injection, `new` inside the test, singletons, static helpers), and where shared state lives (context objects, world, scenario context).
- **Assess the design honestly**: which OOP principles the code actually follows (encapsulation, inheritance, composition, abstraction) and how consistently, using the signals in architecture-assessment.md. Give a verdict — consistent, mostly consistent with deviations, mixed, or no clear structure — with the counts behind it, and list each deviation with evidence. Inconsistency is a finding, not a failure: the rules for new tests will follow the dominant, most recent pattern, and the deviations become "don't imitate".

## Session 3 — Test case writing
How the team expresses *what* is tested, independent of how it's automated:
- **Gherkin/BDD** — feature files and their spoken language (`# language: pt`…), the structure of a feature (Background, Scenario vs Scenario Outline + Examples, tags, how many scenarios per feature), step style (declarative business language vs imperative UI steps), reuse of generic steps, and how steps map to step-definition code (one class per feature or per domain, parameter types, shared context). Count what you claim.
- **Code-only tests** — the titles *are* the test cases: phrasing pattern, language, step titles (`test.step`), and how parametrized/data-driven cases are written.
- **Test-case documents** in the repo (manual cases, specs, Gherkin designs written for people), their format and IDs, and whether automated tests trace back to them.
- **Traceability** — requirement/Jira/Xray/TestRail keys in titles, tags or annotations, reporters that sync results, external tools named in the README.

## Session 4 — Conventions and rules
Everything a generator needs to make code that *looks* like the team's: naming of files, folders, classes, methods, variables and titles; locator strategy (UI) or request building and response checks (API); assertion style; waits and timeouts; hooks; data-driven patterns; tags and grouping; how known defects or flaky tests are marked; code style (indentation, quotes, semicolons, imports) with counts when there is no formatter. Then the **project rules**: what the docs, agent context files, PR template and lint rules require, and where the code disagrees (the code shows what's current). End with **Rules for new tests** per suite — imperative, each with its evidence and whether it's written or observed.

## Session 5 — Data, auth, environments, CI
Test data lifecycle (factories/builders, fixture files, faker, DB seeding and cleanup, API setup; who creates and who cleans); authentication (UI login per test, setup project + storage state, tokens, basic auth; where credentials come from — names and locations only); configuration and environments (baseURL per suite, how an environment is selected, the env var table with names only, secret-bearing files and whether they're gitignored); the app under test — how it's started for local runs, from the product repo in layouts A/B, a question in layout C; and CI — provider, workflows, which suites run on which trigger, toolchain, sharding, artifacts.

## Session 6 — Recipes
Turn sessions 1–5 into **step-by-step instructions for each kind of artifact this repo actually has**: a new test in an existing file, a new test file, a new page object or component, a new step definition, a new fixture, a new data factory, a new API service/client, a new DB helper, a new feature file… Only artifacts that exist in the repo — a recipe for something the team doesn't do would teach a generator to invent it.

Each recipe gives: the files to create or touch in order, where they go, what to copy from (a real example as `path:lines`), how it's registered or wired (fixture registry, exports, runner config, glue path), and a **skeleton** derived line by line from that example, with business parts as `<placeholders>` — using only imports, helpers and patterns that exist in the repo. For BDD suites, the main recipe goes from a scenario in the team's Gherkin style to its step definitions and the layer below.

Close the file with the **reference tests** per suite (1–2 recent, readable, non-skipped tests that use the dominant patterns, and why each one is the model) and **Don't imitate** (legacy files and in-file anti-patterns a generator could copy by accident: duplicated credentials, unused helpers, hard waits, a deviation from session 2).

## Session 7 — Coverage and review
**Coverage**: group tests by product area (feature folders, describe/Feature titles, tags, routes or endpoints called) and count them per suite. In layouts A/B, list the product's areas from its routes/pages/controllers/OpenAPI and mark the ones no test touches, as an observation.

**Review**: re-read every file as a skeptical automation engineer about to generate code from them. Every row traces to a file; every skeleton uses only things that exist; the rules don't contradict each other across files; nothing secret is anywhere; uncertainties are listed, not smoothed over. Fix what you find, finalize the Summary, and fill Uncertainties / open questions.

## Writing files
- **No `.qa-skills/` files yet** → create `.qa-skills/` and `.qa-skills/test-stack/` in the root named in session 0 and write each file as its session ends.
- **Files already exist** → don't overwrite: the team may have corrected them by hand. Write each new file beside the old one with `.new.md` (`test-stack.new.md`, `test-stack/architecture.new.md`). At delivery, show what changed (`diff -u` trimmed to the meaningful changes; a bullet list when most of a file changed or the old file is an older format version) with the replace question. Replace only after they say yes, then delete the `.new.md` files and any old file the new format no longer uses (say which). Carry forward entries marked `(confirmed by QA)`; if the code now contradicts one (not just partly deviates — note that inline), flag it instead of silently dropping it.
- Don't touch any other file in `.qa-skills/` (e.g. `environment.md`, written by another skill). You may read `environment.md` for context, but this skill must work the same without it, and environment access details (QA URLs, accounts, tokens) belong there, not here.

## Deliver, then ask
Reply in chat (labels in labels.md) with a **short** summary: layout and repositories; suites with their stack in one line each; the architecture verdict in one line; how test cases are written; the 3–5 most important rules; the reference tests; and the files written (the `.new.md` ones if pending).

**Then ask every question the code couldn't answer clearly** — there's no limit, because each answer makes the files more reliable, and the files are already written with those points marked, so questions never hold up the delivery.
- Ask only what the repos and git history can't answer. Never ask what you could look up.
- One numbered block, grouped by topic (repositories, environment, architecture, test case writing, conventions…), so the user can answer in one message (`1: yes, 2: the new one…`).
- Each question shows what you found and why it matters: "Specs mix `describe('Cart')` (12) and `describe('cart page')` (11) — which style should new tests use?"
- In layout C the environment questions are always there: how the app under test is started or which environment the tests run against, and where the product's code lives (path or git URL).
- When they answer, update the files and mark each entry `(confirmed by QA)`. Unanswered questions stay in the index's Uncertainties with `❓`.

Bugs you happen to notice in the product or tests aren't this skill's job: one line in Uncertainties if they affect how tests run, no investigation.

End with one line inviting corrections ("Anything wrong or missing? Tell me and I'll update the files.") and that the files contain no secrets and can be committed so every teammate's agent uses them.

## Not this skill?
If the user wants a test written, fixed or reviewed, a bug reported, or the QA environment checked, say in one line that this skill maps the test stack, then help with what was asked. If they want new tests written in an unfamiliar repo, offer to run this discovery first — it's what makes the generated code match.
