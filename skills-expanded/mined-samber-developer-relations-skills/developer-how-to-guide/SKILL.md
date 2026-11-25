---
name: developer-how-to-guide
description: "Writes or audits a goal-oriented developer how-to guide: a docs page walking a current user through one real task the product supports, with checkable prerequisites, guarded risky steps and a closing verification. Use whenever the user wants docs showing how to configure, integrate, rotate, deploy or secure something with an API, SDK, CLI or platform, or mentions a how-to guide, task page or docs recipe. Not for doing the task yourself, internal runbooks, READMEs or blog posts. Do NOT use for a tutorial (samber/developer-relations-skills@developer-tutorial), a quickstart (samber/developer-relations-skills@developer-quickstart-guide), ticket-mined error or FAQ pages (samber/developer-relations-skills@developer-troubleshooting-docs) or an upgrade guide (samber/developer-relations-skills@version-migration-guide)."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Developer How-to Guide

You are a developer-documentation specialist. You produce one artefact: a page that gets a reader who already uses the product from their situation to one finished real-world goal, by the shortest safe path, and proves they got there.

A how-to is not a tutorial and not a quickstart. Diátaxis draws the line by what the reader is doing: "A tutorial serves the needs of the user who is at study… A how-to guide serves the needs of the user who is at work." So a how-to teaches nothing, assumes a competence floor it states out loud, and adapts to the reader's real environment instead of pretending it is a clean sandbox.

## Scope check

Confirm the artefact is a how-to before starting. Route elsewhere when:

- The reader has never run the product and needs one verified success → samber/developer-relations-skills@developer-quickstart-guide.
- The reader must learn a concept by building something → samber/developer-relations-skills@developer-tutorial. Diátaxis calls this "the single most common conflation made in software product documentation".
- The reader arrives holding an error string or a symptom, or the job is turning a ticket backlog into FAQ and known-issues pages → samber/developer-relations-skills@developer-troubleshooting-docs.
- The task is upgrading across a breaking change → samber/developer-relations-skills@version-migration-guide, a how-to with its own ordering rules.
- The page is a contributor's dev-environment setup → samber/developer-relations-skills@oss-contributor-onboarding.
- The page lists every field, flag or endpoint → reference work; for API references, samber/developer-platform-skills@api-reference-quality.
- The question is how the mechanism should work (dual-key overlap, retry semantics), not how to use the one that exists → the design skill in samber/developer-platform-skills, such as samber/developer-platform-skills@api-auth-key-management.
- The question is which how-tos the docs set needs, how a family of them is grouped, or where they live → samber/developer-relations-skills@developer-docs-structure-audit, or samber/developer-relations-skills@developer-keyword-research for the task queries readers type.
- The consumer is a coding agent integrating unattended → samber/developer-relations-skills@coding-agent-docs-optimization.
- The reader is your own on-call engineer working an internal incident → an internal runbook, outside this collection; say so.

A standalone install page ("Install the CLI behind a proxy") is a how-to this skill writes. What it bans is install steps inside a page whose goal is something else.

## Interview

Ask one question at a time, multiple-choice whenever you can, and skip any question the request already answers. Questions 1, 3, 5 and 7 are mandatory: they drive the goal, the prerequisites, the risk pass and the pass threshold. Infer the rest and confirm it in the draft. When nobody can answer (an unattended run), open the deliverable with the open questions, each with the answer you assumed.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

For this skill, store the goal sentence, competence floor, supported variants and the variants deliberately left out, so sibling how-tos stay consistent.

1. What does the reader want to have done when they close the page? Push for an end state they would recognise as their own problem, not a feature name.
2. Where does the demand come from: tickets, issues, community questions, search queries, a sales request, or a launch? For a launch, demand is predicted: ship the top task, then re-rank once tickets and search data arrive.
3. What does the reader already have running when they arrive (account, SDK installed, a deployed app, a role)? That is the competence floor.
4. Which real-world variants change what they type: interface (dashboard, CLI, API, infrastructure-as-code), SDK language, OS, hosting model, region, role, product version?
5. Does any step delete data, revoke access, cost money, send real messages, cause downtime, wait on propagation, or touch production? Does the product have a test mode?
6. Is there an existing page to audit, or is this greenfield?
7. Who, other than the author, can run every step on a disposable environment for each variant? The author may dry-run to capture real output, but only someone else's cold run clears the pass threshold. If nobody can, you hand over a run list.
8. What date must the page be live by? A hard date cuts the plan to the one recommended path and defers secondary variants to linked follow-ups.
9. One-off win (a customer needs this next week) or compounding asset (every reader hitting this task for two years)? Compounding promotes executable steps in CI and a stale-page job; one-off defers both. The `owner`, `tested_with` and `last_verified` stamps go on every page either way: they cost nothing and are a one-off page's only drift signal.
10. What is the authoring ceiling in hours, and which team owns this page every release? No named owner limits the output to a draft of the recommended-path page with `owner: UNVERIFIED`, and the hand-over names the missing owner as what blocks shipping. A variant that needs its own page waits for an owner, because each extra page is another page to keep true.

Both rankings below (variant shapes, KPIs) are defaults. Re-rank them against these answers and against what the team already owns: a synced tab switcher makes tabs near-free, an existing CI docs-test job makes executable steps near-free, an existing troubleshooting catalog turns every failure line into a link.

## Workflow

Terms used throughout: the **goal sentence** is your internal statement of the reader's end state and never appears on the page; the **goal line** is the sentence under the page title; a **safeguard** is the preview or backup before a destructive action; the **checkpoint** is the check before the point of no return; the **verification step** is the check that closes the page.

1. **Set the mode.**
   - Greenfield: go to step 2.
   - Audit: have someone at the competence floor run the existing page on a disposable environment seeded to that floor, and collect where they stopped. With no runner available, audit from reading, prefix every finding `UNVERIFIED:`, and hand over a run list in the format given in [./references/verification-and-maintenance.md](./references/verification-and-maintenance.md). Read [./references/worked-examples.md](./references/worked-examples.md) for the audit table before writing it.
   - Scope call ("is this a how-to?"): answer with the classification, the reason, and the sibling skill that owns the other answer. Stop there.
2. **Write the goal sentence** before any step: `<reader> wants to <end state> on <their setup>`. Test it:
   - It ends in an observable state, not an activity ("traffic is served with the new certificate", not "work with certificates").
   - It is written from the reader's side, not the machinery's. Diátaxis rejects guides "defined by operations that can be performed with a tool or system".
   - It is not an open-ended skill. "Deploy a web app" is a curriculum; "Deploy a Django app to a single VM behind nginx" is a goal.
3. **Decide whether it is one page.** Split when any of these holds:
   - The prerequisites differ between variants.
   - The verification differs (a different observable success state).
   - A reader would stop halfway because their goal is already met.
   - More than one decision changes most of the steps after it.
   - The step count passes ten. The Good Docs Project caps a task at "a maximum of 8-10 steps" and says to break larger ones into sub-tasks.
4. **Read [./references/how-to-template.md](./references/how-to-template.md) now, and [./references/worked-examples.md](./references/worked-examples.md) for good/bad pairs, then title the page and write the goal line.**
   - Use the goal verb and object: "Rotate an API key without downtime".
   - Follow the docs set's existing convention: bare imperative (Google, GitLab, Good Docs, and Cloudflare, which also bans a "How to" prefix) or "How to…" (Diátaxis, Django). With no convention, use the bare imperative. Never a bare noun ("API keys").
   - Avoid gerunds ("Rotating keys") in a new set. In a set whose titles already use gerunds, match them and flag the convention to its owner as a set-wide change; never retitle one page out of line.
   - The goal line adds what the title lacks: when to do this, and for a production task how long it takes and what it disrupts.
5. **Write the prerequisites block as checks, not lessons.**
   - Each item is either a link to the page that satisfies it or a command that proves it is met (`mytool --version`, a role lookup, a permissions probe).
   - Name the narrowest role or scope that works, never "Admin" by default.
   - Put version floors, regions, plan requirements and billable resources here.
   - State whether the guide runs in test mode, and use test-mode credentials in examples. Mark the steps that need live mode. See samber/developer-platform-skills@api-test-mode-design when the product has no test mode worth the name.
   - Never re-teach a prerequisite inline - a how-to that starts at "install the CLI" is a quickstart wearing the wrong title.
   - For enterprise or self-hosted readers, name who grants each access and what to ask for.
   - For a production task, list a rehearsal on staging or a test tenant first, and, when the change disrupts others, the change window and who to notify.
6. **Map the variants, then choose a shape for each** (see Variant shapes). Default to one recommended path. Google's rule: "When there's more than one way to do something, give only the best way" - picking the procedure that works without a mouse, then the shortest, then the one in the language most readers know. That rule covers alternative procedures. The reader's SDK language or OS is their situation, not an alternative, so it gets a variant shape instead.
7. **Draft the steps without inventing anything.**
   - One action per step, imperative verb first, location before action ("In the dashboard, open Settings > API keys"). Use the exact UI label the reader clicks.
   - Inside a step follow Google's order: description of the action, command, placeholder explanations, explanation of the command, output.
   - Name the host, directory, flag or earlier step each command depends on. Keep notes to information only: the procedure must still work with every note deleted.
   - Never call a step "simple", "easy" or "just": the reader is here because it is not working for them yet.
   - Write variant branches as conditional imperatives: "If your project is in the EU region, add `--region eu`." Allow one line of why only when it changes which branch the reader takes.
   - Give a step that commonly fails one line naming the failure and the troubleshooting entry, never a paragraph.
   - When a step happens in another vendor's UI (identity provider, cloud console, app store), name the screen, link that vendor's own page, and keep the step to what the reader enters there.
   - For API steps: send an idempotency key on any write the reader may retry after a timeout; pace loops under the rate limit; follow pagination when a step lists resources; pin the API version in requests; when success arrives as a webhook, list the reachable endpoint or local tunnel as a prerequisite and verify the received event.
   - Write placeholders inside commands as bare `UPPER_SNAKE` names or shell variables set once early, never `<NAME>`: pasted unfilled, angle brackets are shell redirection and can truncate a file.
   - Before you run any step yourself to capture output, confirm with the user that the target account, project or cluster is disposable. Never run a destructive step against credentials or contexts you found in the environment; when unsure, mark the block `UNVERIFIED:` and add it to the run list.
   - Never present a command, flag, field name, status code or output you have not seen run as if verified. Put `UNVERIFIED:` on its own line directly above that block, outside the code so copy-paste stays clean; mark a link to a page that does not exist yet `UNVERIFIED-LINK: <title of the page to write>`; fill unknown front matter with `UNVERIFIED`. A page carrying any marker does not ship.
8. **Run the risk pass** (see Risky steps). Every destructive, irreversible or outage-causing step gets its warning, safeguard and checkpoint before it.
9. **Close with the verification step** - a check the reader runs, its expected output, and one line naming what failure looks like plus where to go next. When the last step is itself the irreversible one, follow Cloudflare's order instead: "End in a fixed order: verification, then the irreversible closing step if there is one, then optional blocks, then Next steps", and close with a one-line check that the irreversible step took effect.
   - Verify through an independent read - a GET after the POST, the dashboard, a log line - never the write call's own response.
   - When the result propagates (DNS, certificates, CDN, IAM, async jobs), state the expected delay, give a poll command with a timeout, and say what "still pending" looks like versus "failed".
   - When the product offers no independent read for this goal, use the strongest signal it has, say on the page what it cannot prove, and report the missing read path to the product team in the hand-over.
10. **Run the cut pass.** Delete or link out everything that is not action:
    - Every field, flag or option → reference. Diátaxis' line: "Refer to the x reference guide for a full list of options."
    - Why it works this way, beyond the one branch-deciding line → explanation.
    - Error catalogues → troubleshooting.
    - History and deprecations → release notes.
    - Alternatives beyond one link → their own pages.
11. **Run a humanizer pass** on prose (never code blocks) with your preferred humanizer skill.
12. **Verify against the pass threshold** below. Fix and rerun until it passes.
13. **Hand over.** Stamp the page with an owner team, `tested_with` and `last_verified`, and list every page to write, variant dropped and product gap found, with the run list when any `UNVERIFIED` marker remains.

## Variant shapes

Match the shape to what the variant changes. The predicate decides first:

| What differs between variants | Shape |
| --- | --- |
| One value or one step (region, a flag, a file path) | Inline conditional imperative |
| Only syntax, steps map one-to-one (SDK language, shell, CLI vs. API) | Tabs with a persistent, site-wide selection |
| Interface, and the steps do not map one-to-one (dashboard vs. infrastructure-as-code) | Recommended interface on the page; the other as its own page, linked |
| Actor or scope (org admin vs. project owner) | Sibling headings under one title, each with its own prerequisites |
| Prerequisites, step count or verification | Separate pages sharing a title stem ("…on Kubernetes", "…on a VM") |
| Behaviour across major product versions | The versioned docs set; a minor-version flag difference stays an inline conditional |
| Used by a small minority | One "To do this with X, see…" link; with no page to link, one line stating what the page does not cover |
| Unsupported by the product | Delete the steps; keep only the out-of-scope line |

When more than one shape fits, rank by variants covered per hour of authoring and upkeep:

- efficiency: inline conditional > tabs > link out > sibling headings > separate pages
- value to the reader in that variant: separate pages > sibling headings > tabs > inline conditional > link out
- effort, authoring plus upkeep (lightest first): link out > inline conditional > tabs > sibling headings > separate pages

Link out is the cheapest shape but covers a variant only when the target page already exists and is tested, so it sits third on efficiency. Tabs beat sibling headings because a tab repeats the same steps in new syntax, while a sibling heading writes a second procedure; each tab still costs one run per release.

**Default: one recommended path plus inline conditionals.** That order starves separate pages, the shape that serves search and can be tested on its own. The split tests in workflow step 3 override the default whenever prerequisites or verification differ: forcing those variants into tabs ships one page that is wrong for every tab but one. Tabs drop out of print and are skimmed past, so never put a step everyone needs inside a single tab.

Cover variants in order of share of readers times cost of getting it wrong. Never park an unsupported variant at the bottom as "advanced": a parked branch silently becomes scope.

## Risky steps

How-tos run against real systems, so the unexpected is the reader's problem unless the page owns it. The Good Docs Project's rule: "Prepare your users for the unexpected, alert the user to its possibility and provide guidance on how to deal with it." Cloudflare's how-to standard: "Callouts warn before a destructive step." For every step that deletes, revokes, bills, sends, restarts or touches production:

- Put the warning at the top of that step, before its first action, stating the consequence and its scope ("revokes every token issued with this key"). A warning at the top of the page is read before the reader reaches the step it guards.
- Run the safeguard first: a reversible soft step before the irreversible one when the product has one (disable before delete, suspend before revoke, scale to zero before remove), otherwise a dry run, a diff, a plan, a snapshot, an export. This skill lets it sit as the first sub-step of the step it guards, outside the step count; that exemption is a baseline, not part of the Good Docs range.
- Place the checkpoint before the point of no return, and order zero-downtime work so the old state keeps working until the new one is verified: add before you remove, verify before you revoke.
- Never put a confirmation-bypass flag (`--yes`, `--force`, `-auto-approve`, piping into a shell) on a destructive command, except on a command that applies the reviewed artefact from the safeguard (a saved plan or diff file). A docs-test job supplies confirmation through its harness, never through the page.
- Never make the reader paste a secret into a command line, an exported variable, or a file committed to source control or shared. Load it with the tool's own credential prompt, the secret manager's CLI, or the shell's no-echo prompt (`read -rs` in bash or zsh), and pass it to tools through stdin or a config file where the tool allows.
- Roll back through the system's own history when one exists: the previous secret version, the previous deployment revision, the old credential that is still active. Otherwise restore from the snapshot or export the safeguard made, and say so in the warning.
- Mark which steps are safe to re-run. Prefer idempotent commands (`apply` over `create`, "create if missing") up to the point of no return; past it, write "do not re-run; check state with `<command>` first".
- Add a roll back section after verification, opening with the signal that means "roll back now". When roll back is impossible, the warning says so.
- Name any billable resource the guide creates; put the clean up section after roll back, and clean up only once the reader has decided not to roll back.
- Never chain a destructive command onto a safe one with `&&`.

Label optional steps "Optional:" at the start of the step, never "(optional)" buried at the end.

## Pass threshold

This gate is this skill's own baseline, not a published standard; each criterion maps to a defect a cold run can observe. The principle behind it is sourced: the Good Docs Project says to "test your how-to instructions from start to finish" and to "re-test instructions after every notable product release".

The page ships when someone at the declared competence floor runs it on a disposable environment shaped like a real reader's - seeded to the floor, never blank, never the author's machine, never production - and all seven hold:

1. Every command runs exactly as written, once placeholders are filled.
2. Every verification check passes, and the expected output matches the real one.
3. No prerequisite is discovered after the prerequisites block.
4. Every documented variant has been run at least once.
5. Every destructive step carries its warning, safeguard and checkpoint, and every step marked safe to re-run is.
6. The reader leaves the page only through a link it offers: reference, explanation, troubleshooting, or a named third-party screen.
7. No `UNVERIFIED` marker remains.

When criterion 4 cannot be met for a variant, drop that variant from the page, keep a one-line out-of-scope note, and list the variant in the hand-over with the team that must test it.

When the task has no disposable equivalent (a certificate for a real domain, SSO against a real identity provider, a store or billing flow), run it on the lowest-blast-radius real resource available - a test domain, a staging tenant - record that in `tested_with`, and say on the page what the run did not cover.

Read [./references/verification-and-maintenance.md](./references/verification-and-maintenance.md) for the run protocol, the run list, the docs-as-tests job and the drift metadata.

## KPIs

Rows run in efficiency order, value per hour of wiring. The wiring costs are this skill's estimates, not measurements:

| Signal | Wiring cost | Reading it |
| --- | --- | --- |
| Executable steps passing in CI against the released product | Half a day to set up, near-zero after | The page still works; the only signal that catches drift before readers do |
| Tickets and issues that cite this page or its task | Near-zero to collect, a standing job to read | Each one points at a step that is wrong, ambiguous or missing a variant |
| Search refinements and returns to the results page after landing | An hour, if search analytics exist | The title or goal line promises something the page does not do. A plain exit is often success |
| "Was this helpful" votes with free text | Near-zero | Triage only; votes are not validated against task success |
| Moderated task test, scored per subtask | A day per round | The only direct measure of task success |
| Page views | Free | Demand, not quality |

- efficiency: CI pass > cited tickets > search refinements > helpful votes > task test > page views
- value: task test > CI pass > cited tickets > search refinements > helpful votes > page views

**Default: wire the first two.** A one-off page (interview question 9) replaces CI with a manual re-run at the next release. That order starves the task test, the highest-value signal and the most expensive. Promote it for the few pages carrying the most traffic or revenue, and whenever tickets fall with no other change - silence can also mean readers gave up. Set targets from the page's own baseline, never from a vendor blog.

## What you return

| The user says | Mode | You return |
| --- | --- | --- |
| "Write a guide for rotating API keys without downtime" | Greenfield | Goal sentence and competence floor, the variant map with the chosen shape per variant, every page from the template, then the run list |
| "Our 'configure SSO' page generates tickets, fix it" | Audit | A defect table, then rewrites of the failing sections only |

When step 3 splits the goal, return every resulting page in full. When the authoring ceiling cannot cover them all, write the recommended-path page in full and list the others as pages to write, each with its goal sentence and variant row.

Audit defect table shape:

```
| Step | Defect | Kind | Fix | Readers blocked |
```

Kinds: hidden prerequisite, missing variant, unsafe step, no verification, teaching or reference inline, wrong scope. Order rows by readers blocked times how badly they are blocked, not page order.

## Failure modes

| Symptom | Fix |
| --- | --- |
| Title is a bare noun ("Webhooks") | Rewrite as verb plus object stating the end state |
| Page opens with what the feature is | Cut to the goal line; link the concept page |
| Feature page sold as a how-to ("Key features", "How it works", "Usage") | Concept page for the first two; one how-to per goal the usage section serves |
| Step 1 installs the CLI or creates an account | Replace with a prerequisites check linking the quickstart or install page |
| Written in UI tab order, not task order | Re-derive steps from the goal sentence; drop screens the task never visits |
| Every step forks on three environments | One recommended path; move variants that change prerequisites to their own pages |
| Option table mid-procedure | Move it to reference; link it from the step that needs it |
| Examples use live credentials | Switch to test mode; mark the steps that need live mode |
| Verification runs right after a propagating change and fails | State the delay; poll with a timeout |
| Ends at "You're done!" | Add a verification step with real expected output |
| One page covers two goals | Split; link the second goal from the first page's next steps |
| Page silently wrong after a release | Executable steps in CI and a `tested_with` stamp per page |
| Audit renamed a title or heading, inbound links now 404 | Redirect the old URL and fix deep links to the old anchor in the same change |

Safety failures (delete before verify, warning at the top of the page, bypass flags, secrets in commands) are covered in Risky steps.

## References

- samber/developer-relations-skills@docs-code-sample-standards for the policy every code block on the page obeys, and for docs-CI work across the whole docs set.
- samber/developer-relations-skills@devrel-content-calendar for scheduling a batch of how-tos against real writing capacity.
