---
name: fullstack-web-delivery
description: "Plan and deliver complete websites with adaptive discovery, industry research, client-specific UI/UX, frontend, backend, authentication, persistent data, local preview, and evidence-based acceptance. Use for new sites or substantial redesigns; keep targeted fixes within their existing scope."
---

# Fullstack Web Delivery

Turn a project brief into a runnable, reviewable website. Select only the modules the project needs. Communicate in the user's language. Version: 0.9.1.

## 1. Establish the scope

Read applicable project rules, current source, supplied material, and existing authorization. Reuse answered requirements. Verify available file, terminal, search, browser, screenshot, and service capabilities. The skill adds workflow instructions, not execution privileges.

Distinguish planning, visual prototyping, and complete implementation. Deliver the complete plan before implementation. Continue authorized local development after that delivery unless the user requested a specific approval gate. Follow [platform setup](references/platforms.md) for installation and capability limits.

## 2. Ask only for decisions that are missing

Use the [discovery pool](references/discovery.md). Ask four to six consequential questions per round, within the host tool's limits. Forty questions form a candidate pool; they are not a quota. Skip answered questions. Inspect technical facts yourself. Use reversible, reasoned defaults when authorized; ask for business facts and material preferences.

Begin with who needs to accomplish what and what success looks like. Record user decisions, verified facts, assumptions, and pending dependencies. For consequential layout, navigation or interaction choices, prepare a [visual decision](references/visual-decisions.md) before asking: runnable alternatives where possible, otherwise annotated views or a diagram. Pause only the branch that needs a missing decision. Stop general discovery once a complete plan and acceptance scenarios are possible.

## 3. Research and deliver the complete plan

Read [research](references/research.md) and [client-specific design](references/custom-design.md). Start with the client's industry, audience, and tasks; study relevant mature businesses, then design principles, then GitHub implementation candidates. Record sources, observed scope, adoption, rejection, licenses, and integration cost. Mark unavailable research honestly.

Before implementation, deliver the complete [site plan](references/site-planning.md): layer responsibilities, sitemap, page-count basis, menus, page templates, copy logic, company facts, form-to-admin flow, APIs, roles, data, milestones, delivery, and acceptance. Apply [content and commercial boundaries](references/content-commerce.md) when relevant.

Automatically turn the answered brief into the [project specification pack](references/specification-pack.md) in the same handoff. Include a filled UI/UX implementation prompt, page audiences/content/actions, state and motion contracts, relevant engineering/module specifications and requirement-to-acceptance traceability. Use concrete project decisions, not empty templates. The optional Python renderer is a convenience; hosts can write the same documents directly. Preserve authored revisions and mark unexecuted acceptance NOT_RUN.

Map each requirement to a task and a verification method. Define legal business states and access boundaries before interfaces and screens. Order work with [business-flow decisions](references/development-workflow.md); revise the plan when evidence changes the route.

## 4. Compare three layouts and resolve the client's design

Read [client-specific design](references/custom-design.md) and [design and motion](references/design-motion.md). Derive composition from the brief, real content, user tasks, and brand constraints. Translate references into one coherent system, with concrete adoption and rejection decisions.

For a new site or substantial visual redesign, follow [visual decisions](references/visual-decisions.md): build three materially different layouts for a representative page and critical interaction using the same realistic content and brand constraints. Open the working comparison in the user's browser and provide identifiable option links, matched desktop/phone views, differences and tradeoffs. Gather selection, combination or revision feedback before expanding the dependent templates, unless the user explicitly delegated the choice. A selected palette alone does not select a layout. Reuse a specifically chosen layout; keep targeted fixes in scope.

Record the actual selection source and update the UI/UX prompt and design contracts. Check visual quality and task usability separately. Verify that promised content is rendered and phone users can discover key states and actions. Record triggers, states, feedback, failure recovery, keyboard/touch behavior, APIs, and motion for each applicable control.

Match typography, nested radii, grouped entrances, heading wrapping and elevation to actual page elements with [UI fit and finish](references/ui-fit-and-finish.md). After the brief, generate UI-MATCH-SPEC.md with adopt/defer/omit decisions, task-specific reasons, implementation, states, fallbacks and verification; include it in the UI/UX prompt. For requested reflective cards, read [metallic surfaces](references/metallic-surfaces.md) and choose CSS or a justified GPU route with an explicit environment source, coupled motion and a readable fallback. Specify light direction/intensity, face and bevel highlights, shadow mechanism, and how each responds to pose; distinguish GPU lighting from a CSS shadow approximation. Verify actual stage pixels and context recovery before claiming a working GPU material.

Every enabled control must act and every link must reach a supported destination. Start feedback at input; show success only after the actual operation confirms it. Derive linked responses from one state. Make animation interruptible and retain keyboard, touch, focus and reduced-motion paths. Select [advanced patterns](references/interaction-patterns.md) by purpose; do not add all six effects to every site. Learn reference principles within their scope: marketing composition, operational usability and a client's existing brand are different constraints.

For scroll effects, video references or coordinated feedback, use [motion placement](references/motion-placement.md) to name the actual driver and assign it to a page/action/task. Persist MOTION-MAP.md with interruption, reduced-motion and verification contracts. Read [mechanism recipes](references/motion-recipes.md) for scroll, authenticated morphs, counts, command search, relationship paths, inline layout and appearance. Select relevant effects; preserve source-backed business state and a complete recovery path.

## 5. Build complete business increments

Read [implementation and preview](references/implementation.md). Preserve an appropriate existing stack. Establish a runnable baseline, then select a flow whose dependencies are satisfied. Prioritize blocking dependencies, business value, and consequential uncertainty. Connect UI, API boundaries, business rules, authorization, storage, and feedback in that increment.

Use real authentication, server-side authorization, and persistent data where required. Commit state and its audit event together. Isolate test accounts and data. Keep mock, sandbox, and real integrations distinct. Preview and verify each flow before expanding the next one.

## 6. Verify, repair, and hand over

Read [delivery](references/delivery.md). Verify normal, failure, access, data, mobile, and interaction scenarios per flow, then regress the site, production build, and agreed restart persistence. Use the same business identifier to match the receipt, database, admin details, and history.

Measure actual CSS viewport and screenshot scale. Check error, success, reset, and settled-exit focus. No page overflow alone does not establish phone task usability. Preserve failures; repair and recheck affected scope. Browser operation, API checks, screenshots, source review, and independent acceptance are different evidence.

After two attempts without new evidence or a plausible repair, stop blind retries in that branch, retain reproduction and recovery conditions, and continue independent work. For uncertain external side effects, inspect the result before retrying.

Deliver source, startup, preview/admin entry points, plan, API/data notes, credentials retrieval method, acceptance evidence, known limits, and release conditions. Use PASS, FAIL, NOT_RUN, BLOCKED, and NOT_APPLICABLE. Apply the user's existing authorization to publication, external messages, payments, and production changes; prepare reviewable work before any required final approval.

## Continuity

Maintain a durable task/decision/evidence record and one accountable integration path. Work sequentially unless the user or applicable instructions authorize delegation. Before resuming, verify current source, process ownership, tools, and authorization. Scheduling requires the user's request and a real scheduling capability.

Use [behavior evaluations](references/behavior-evals.md) to maintain this skill. [Field-trial evidence](references/field-trial.md) separates observed local behavior from untested platforms and scenarios. The source-available license covers these instructions; independent outputs are addressed in the included LICENSE.
