---
name: test-automation
description: Writes new automated tests in the user's own test repo exactly the way the team already writes them — test case first (a Gherkin scenario in BDD suites, or test and step titles in code-only suites), then the implementation (step definitions, page objects, services, fixtures, data factories) — reusing every step, page object method, service, factory and helper that already exists instead of duplicating code. Works in sessions and consumes the `.qa-skills/` files written by test-stack-discovery (recipes, conventions, architecture, test-case-writing), with a lighter discovery of its own when they don't exist. Covers e2e UI, API and other suites in any stack (Playwright, Cypress, Selenium, Cucumber, REST Assured, pytest, Robot…). Use whenever the user wants a test automated, scripted or implemented — from a user story, acceptance criteria, manual test case, Jira key, bug or plain description — or asks for a new scenario, feature file, step definitions, a page object or a spec — e.g. "automate this scenario", "write an e2e test for the edit flow", "automatiza esse cenário", "cria o teste automatizado da tela X", "escreve a feature e os steps", "implementa os steps desse BDD", "automatiza o caso de teste do Jira", "automatiza la prueba". Not for mapping the test stack (test-stack-discovery), exploratory testing or bug reports.
---

# Test Automation

Write the test a senior engineer on *this* team would write: same layers, same names, same Gherkin voice, same helpers — so that in code review nobody can tell it was generated. The two things that matter most are **fidelity** (it looks like the team's code) and **reuse** (it plugs into what exists instead of growing a parallel copy of it). Duplicated steps, locators and requests are the most expensive thing a generator can leave behind: every copy has to be found and fixed separately the day the screen or the API changes.

The work happens in the user's test repo, never in the qa-skills repo. It writes test code and nothing else: no commits, branches, dependency installs, or edits to `.qa-skills/`.

**What to read, and when:** [references/reuse.md](references/reuse.md) before session 2 (where to look per layer, reuse/extend/create decisions, what may change in existing code). [references/validation.md](references/validation.md) in session 4. [references/without-discovery.md](references/without-discovery.md) only when the repo has no usable `.qa-skills/test-stack.md`. [references/labels.md](references/labels.md) only when talking to the user in a language other than English.

## Language
Look for `.qa-skills.yaml` in the test repo's root, then `~/.qa-skills.yaml`. `language` is for what you say to the user. The test itself follows **the team's language, not the user's**: Gherkin, titles, step titles and identifiers are written in whatever language the existing tests use (`test-case-writing.md` says which), because a Portuguese scenario in an English feature folder is exactly the kind of inconsistency this skill exists to prevent. `report_language` only applies to the chat summary's prose when it differs from `language`. An explicit request in the conversation overrides the file. Otherwise use the language of the user's message. Don't mention a missing file.

## Source fidelity
- **Nothing in the test is invented.** Every import, base class, fixture, helper, step and selector you use exists in the repo (cite `path:line` in your notes); every new one you create follows a recipe or a real example. If `recipes.md` doesn't cover an artifact, copy the closest real file, not a framework tutorial.
- **Expected results come from a source**: the user's request, a requirement or test-case doc, the product code (UI texts, validation messages, routes, status codes — layouts A/B), an OpenAPI/swagger file, or an existing test of the same behavior. When none of them says what should happen, write your best assumption into the test, mark it in the code with the team's comment style (`// ⚠️ UNCERTAIN: expected message not found in product code`) and list it in the final questions. A test with a guessed oracle that passes is worse than one that's honestly marked.
- **Selectors** come from the product code or a live page (Playwright MCP, if connected and the app is up), following the locator strategy in `conventions.md`. Never make up a test id or a label.
- **Secrets never leave their file**: use the env var names and data helpers the suite already uses; never paste a password or token into a test.

## The `.qa-skills/` files
`.qa-skills/test-stack.md` (index, marker `<!-- qa-skills:test-stack v2 -->`) and the session files in `.qa-skills/test-stack/` are your map of the repo. Read them the way docs/configuration.md says:
- **Find the test repo**: the path the user gave; otherwise the workspace folders (skip skill collections like qa-skills). The index's Repositories table tells you where the product repo is.
- **Version marker** unknown or missing → treat as no file ([without-discovery.md](references/without-discovery.md)) and suggest running test-stack-discovery once the test is delivered.
- **Freshness**: `git log --oneline <commit from the header>..HEAD -- <test module paths>`. Relevant commits → one line to the user; trust the files but confirm against the code anything those commits touched.
- **Read only what this task needs**, in this order: the index (suites, coverage map, uncertainties), then for the target suite `recipes.md`, `conventions.md` (Rules for new tests first), `test-case-writing.md`, and `architecture.md` only for the layers you'll touch. `environment-and-data.md` in session 4, or earlier if the test needs data or auth.
- **`(confirmed by QA)` beats everything**, including the code. `⚠️ UNCERTAIN` and `❓` entries are not facts: check the code yourself, and if it still matters for this test, it becomes a question at delivery.
- **The files describe; the code decides.** Before reusing something the files mention, open it — a method signature or a step's exact wording must come from the code, not from a summary.

## How the work is organized
Six sessions, in order. Each one finishes before the next starts, and writing the test case before any implementation is deliberate: it fixes *what* is being tested in the team's own words, and the step list it produces is what the reuse search runs against. If the user asked for several tests, take all of them through each session together — reuse is found across the batch, not test by test.

| # | Session | Produces |
|---|---|---|
| 0 | Context | target suite, the behavior to test and its oracle, the files and reference tests loaded |
| 1 | Test case | the scenario(s) or test/step titles, written in the repo, before any implementation |
| 2 | Reuse map | one row per step/action: what exists, and reuse / extend / create |
| 3 | Implementation | only the missing pieces, bottom-up, following the recipes |
| 4 | Validation | static checks always; the new tests run only when the environment allows |
| 5 | Review and delivery | duplication review over the diff, then the summary and questions |

Keep a short running note of decisions (file:line of everything reused, every assumption) — the delivery summary is built from it.

## Session 0 — Context
- **Which suite.** The request usually implies it (a screen → e2e UI; an endpoint → API). If two suites could fit and the index doesn't settle it, pick the one where the behavior is closest to existing tests and say so in the summary — don't stop to ask.
- **What behavior, and its oracle.** Restate the request as concrete behavior: preconditions, actions, expected results. Find the oracle for each expected result (see Source fidelity). In layouts A/B, read the product code of that screen or endpoint: it gives the real texts, validations and routes, and often a rule the request didn't mention that deserves its own scenario.
- **Already covered?** Search the existing tests for this behavior (coverage map, feature/describe titles, scenario titles, the endpoint or route in step definitions and specs). Fully covered → say where (`path:line`) and stop, unless the user wants it anyway. Partly covered → write only the missing scenarios, ideally next to the existing ones.
- **Open the reference tests** for the suite (listed at the end of `recipes.md`) and the closest existing test to this behavior. Read them in full: they're what your test must look like.
- **Ask only when you can't tell which feature or flow is meant at all.** Everything else — missing oracles, data choices, naming doubts — gets your best evidence-based decision now and a question at delivery.

## Session 1 — Test case
Write *what* is tested, in the team's format and voice, before writing how. Put it in the repo where the team keeps it (a new `.feature` or spec file, or new scenarios in an existing one — `recipes.md` and the folder structure say which).

**BDD suites** (Gherkin):
1. Write the scenario(s) following `test-case-writing.md`: feature language and `# language:` header, Feature/Background/Scenario/Scenario Outline usage, tags and ID scheme (continue the existing numbering: find the highest ID and use the next), title pattern, declarative vs imperative style, steps per scenario.
2. **Speak the existing step vocabulary.** Before inventing a sentence, find the step that already says it: `python3 -I <this skill>/scripts/reuse_index.py <test repo> --grep <keywords>` lists the definitions with their usage counts. Copy the exact wording, including parameter style (`"quoted"`, numbers, data tables).
3. Check the draft: `python3 -I <this skill>/scripts/reuse_index.py <test repo> --check <feature file>`. For each `UNDEFINED` step, look at the `~ similar` definitions it prints: if one does the same thing, **rewrite your step to its exact wording** — a second definition for the same action is a duplicate even if its words differ. Leave a step `UNDEFINED` only when no existing definition does that action; those are the only steps session 3 implements.

**Code-only suites**: create the spec/test file **now, before any page object, fixture or helper exists** — `describe`/class, test titles in the team's pattern, and the step structure the team uses (`test.step` titles, Arrange/Act/Assert comments, `@DisplayName`…), each step's body holding only a comment that says what it will do (`// preencher o formulário com o novo preço`). It's not a formality: an implementation written first quietly shapes the test around what was easy to build, and the user loses the chance to review *what* is tested in their team's words. Session 3 fills these bodies; if implementing shows a step must change, change it there and mention it at delivery.

Both: tag and title the test exactly like its neighbors (Jira/Xray keys, `@regression`, `@smoke`…), and include traceability keys the user gave.

**Choosing the scenarios.** Unless the user limited the scope ("só o caminho feliz"), derive them from the oracle: the main successful flow, then one case per rule the source states (each validation message, limit, status code, permission) — grouped with the team's data-driven pattern (Scenario Outline + Examples, `for … of` over cases, `@ParameterizedTest`) instead of copy-pasted tests. Rules you leave out go in the delivery as "not covered", so a short scope is a visible choice, not an accident.

**Prove the precondition, not only the outcome.** When the expected result is "X goes back to / stays at / changes from its previous value", the test must also show the state really was different in between (the stock went down when the cart was created, the price shown before editing was the old one). Otherwise the test passes even when the action under test does nothing.

## Session 2 — Reuse map
Read [references/reuse.md](references/reuse.md). Run the reuse index once for the whole repo (or `--paths` to the test module in a product repo) and use it, plus targeted reading of the classes it lists, to fill one row per step or action of the test case:

| Step / action | Existing | Decision |
|---|---|---|
| `Given I have a registered customer` | `CustomerSteps.java:41` | reuse |
| fill the address form | `NewAddressPage.fillAddress` `pages/newAddress.page.ts:38` — the edit page shows the same form | extend: move the form into a component both pages use |
| check the success toast | `Toast.message` `pages/components/toast.ts:7` | reuse |
| `When I send a PATCH request to update the address` | none — `~ similar` only finds POST/DELETE of other domains | create (service method + step) |

Decisions are **reuse** (as is), **extend** (add a parameter, an overload or a method to an existing class, keeping its current callers working), or **create** (nothing does it). `create` needs the row to say what you searched for. Before marking a row `reuse`, read the body of what you're reusing down to the framework call — a step or service named after one thing sometimes does another (a wrong endpoint, a field never asserted), and reusing it unread is how a new test inherits an old bug. Prefer the most specific existing layer: an existing step beats a new step calling an existing service; an existing service beats a new raw request.

**A new area from scratch** (a screen, endpoint or domain no test touches yet) is mostly `create` rows, and that's expected. Reuse there is about the **shared infrastructure**: base classes, components the new screen also shows (navbar, toast, modals), auth setup, data factories and DB/API helpers that create the preconditions and clean up, generic steps (status code, message, contract). And the new pieces must **mirror the closest existing area**: copy its folder layout, file and class naming, how its page object/service is built and registered, and how its spec or feature is organized, so the new area reads like a sibling of the old ones rather than a fresh design. Name that model area in the summary.

This table goes into the delivery summary — it's how the user sees that nothing was duplicated.

## Session 3 — Implementation
Implement only the `extend` and `create` rows, **bottom-up**: data model/factory → service/client or page object/component → fixture/registration → step definitions → filling the bodies of the test written in session 1. Bottom-up means each layer is written against code that already exists, so you never call a method you haven't written.

- **Follow the recipe** for each kind of artifact in `recipes.md`: files in that order, the location it names, the wiring (fixture registry, exports, glue path, runner config), and its skeleton. Fill the skeleton's placeholders; don't restyle it.
- **Follow every "Rule for new tests"** in `conventions.md` for the suite, and nothing from "Don't imitate" in `recipes.md`, even when the nearest file does it.
- **Match the neighbors** for anything the files don't cover: indentation, quotes, import order and aliases, logging, comments density, how assertions are phrased, wait strategy. Read the file you're adding to, and write as if it were yours.
- **New step definitions** go in the class/file for their domain (`test-case-writing.md` → From scenario to code), delegate to the layer below like their neighbors, and use the team's shared state (ScenarioContext, World, fixtures) — never a new static/global.
- **Test data**: use the existing factories/builders/fixtures and the cleanup mechanism the suite already has (auto-cleaning fixture, `@After` hook, DB helper). A test that creates data and leaves it behind breaks the next run.
- **Don't break the suite.** The new test must be safe to run the way the suite runs — in parallel, sharing the auth/session state from a setup project, sharing users and data. A test that destroys shared state (a logout that revokes every session of the shared user, deleting or changing a shared user or seed record, a global setting, a DB reset) will pass alone and knock down other tests. Isolate it with the team's own mechanism first (its own user or data, `test.describe.configure({ mode: 'serial' })`, a tag the CI runs separately), and if the only safe option is a runner change (a separate Playwright project that runs after the others, a separate Cucumber runner), make it — that runner change is allowed for this — and report it. Flagging the risk as a question and shipping the test unisolated is not enough.
- **Changes to existing code** are limited to what reuse.md allows. List every one in the summary.
- **A bug in existing test code** that your new test depends on (a service calling the wrong endpoint, a step asserting the wrong field) — fix it when the fix is small and obvious from a source (paths constants, swagger, the step's own name), because building on it would make your test wrong too. Then call it out on its own at delivery: what was wrong (`path:line`), the fix, which existing tests now behave differently and that they weren't re-run against the app. A bug your test doesn't depend on is only reported, never fixed in passing.

## Session 4 — Validation
Follow [references/validation.md](references/validation.md):
- **Static checks always** — they need no environment: compile/type-check (`tsc --noEmit`, `mvn test-compile`…), the runner's list/collect/dry-run mode, the linter the repo uses, and `reuse_index.py --check` on every new or changed feature file (no `UNDEFINED`, no `AMBIGUOUS`). Fix what they report.
- **Run the new tests when it's safe and possible**: the environment is local or a test environment the files or the user allow, the app is reachable, and nothing needs credentials you don't have. Run them alone first (by file, title or tag) and **check the runner really ran only those** — a tag filter can be silently overridden by tags fixed in the runner class. Then, if the new tests touch shared state (login/logout, shared users, shared data) or you changed existing code, run them once **together with the tests that share that state** (the whole suite when it's quick and local), because isolation bugs and regressions only show there. Never against production. If you can't run them, say so and give the exact commands.
- **When a run fails**, read the error. A problem in your code → fix it. A difference between what the product does and the oracle → **don't bend the assertion to make it pass**: keep the test, mark it the way the team marks known defects (`conventions.md` → Known defects), and report it (the bug-report-writer skill can write it up). An environment problem → report it; don't debug their infrastructure.

## Session 5 — Review and delivery
**Duplication review** — read your diff (`git diff` plus new files) as the reviewer from this team would:
- every new step, method, locator, request or helper: search the repo for one that does the same (by behavior, not only by name). Found → replace yours with it;
- no literal (URL, endpoint path, message, selector, test id) that the repo already keeps in a constant, page object or paths class;
- no block repeated across your new tests that the team would extract into a step, fixture or helper — and none extracted where the team keeps things inline;
- the recipe checklist and Rules for new tests, item by item.

**Deliver** (labels in labels.md) with the template below. Every piece of information the user needs is in it; what makes a delivery long is re-describing the code (they'll read the diff), narrating each step of the work, and a paragraph per decision. One line per item, tables over paragraphs, and evidence as a `path:line` instead of an explanation — aim for 300–500 words plus the test case and the reuse table.

````markdown
**<What was automated>** — <suite> · <N tests/scenarios> · modeled on <closest existing area/test>
Created: <files> · Changed: <files>

**Test case**
```<gherkin | text>
<the scenario(s), or the test and step titles, exactly as written>
```

**Reuse map** — <n> reused · <n> extended · <n> created
| Step / action | Existing | Decision |
|---|---|---|

**Existing code changed**
- <path:line> — <what and why, one line>
- ⚠️ Bug fix: <path:line> — <wrong → right>; affects <existing tests>; <re-run: result | not re-run>
- Isolation: <runner/config change made so the suite stays green, if any>

**Validation**
- Static: <command> → <result> · <command> → <result>
- Run: <command> → <N passed / failed: why> | not executed — <reason>; run with `<command>`
- With the suite: <command> → <result> | not needed — <reason>

**Expected results from:** <sources as path:line, one line>
**Not covered:** <rule or variation>, <…>

**Questions**
1. <found> → <what I chose> — <question>  (only those whose answer changes the test; ≤ 6)
````

Omit a section that has nothing (no changed code, no questions), never the information inside one that has something. End with one line inviting adjustments, and — if the `.qa-skills/` files were missing, stale or contradicted the code — one line suggesting test-stack-discovery.

## Not this skill?
Mapping how a test repo works → test-stack-discovery. Exploring the product for bugs → exploratory-testing. Writing up a failure → bug-report-writer. If the user wants an existing test fixed or reviewed rather than a new one, help directly, applying the same reuse discipline.
