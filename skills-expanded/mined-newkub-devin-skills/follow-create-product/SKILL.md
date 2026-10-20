---
name: follow-create-product
description: Build a product end to end from idea to website with auth, payments, dashboard, and ship
argument-hint: "[product-idea]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - follow-create-web
  - follow-my-techstack
  - clone-product-with-my-techstack
  - follow-service-workos
  - follow-service-stripe
  - follow-service-cloudflare
  - follow-lib-unocss
  - follow-design-system
  - deep-review-codebase
  - ship
  - report
  - enhance-prompt
  - implement-to-production

---

## Goal

Turn an idea or requirements into a ready-to-use product, covering product spec, UX/UI, landing page, and the standard pages — `features`, `pricing`, `user`, `dashboard` — with auth, payments, and ship

## Scope

- Use for products with a website, user pages, billing, and a dashboard
- Create the product spec, user stories, and roadmap before starting the build
- Invoke `/follow-create-web` to create the website project
- Invoke `/follow-service-workos` for auth
- Invoke `/follow-service-stripe` for payments, pricing, billing
- Invoke `/ship` when the work is done
- Building from an existing product instead of an idea — cloning a live product or a GitHub repo to rebuild it — use `/clone-product-with-my-techstack` (it covers this skill's flow plus research, captures, and parity verification)

- Latest: (version-agnostic — product scaffolding guide) (verified 2026-09-12)

## Execute

### Workflows

| Argument | Workflow |
|----------|----------|
| `scaffold`, `setup` | `workflows/setup-scaffold/SKILL.md` — scaffold product structure (monorepo, packages) |
| `deploy` | `workflows/deploy-mvp/SKILL.md` — deploy the product MVP to a platform + verify the live URL |

1. If the argument matches a workflow → read `workflows/<arg>/SKILL.md` and follow its flow
2. If not specified → follow the normal Steps

### 1. Review Tech Stack And Understand Input

> Goal: Review the tech stack and analyze the product idea before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns
2. Run `/follow-my-techstack` to pick the stack from the canonical catalog; run `/deep-review-codebase` to summarize any tech stack already in use
3. Record the rationale for the chosen stack and libraries for later reference (create product)
4. Take `product-idea`, requirements, or feedback from the user
5. Identify target users and personas
6. Identify the problems to solve
7. Identify the value proposition
8. If the input is ambiguous → use `/enhance-prompt` or `/ask-me` first

### 2. Define Product Scope

> Goal: Define the product scope

1. Identify core features
2. Identify the MVP scope
3. Identify what is out of scope
4. Identify success metrics
5. Use `/report` to summarize scope, priority, effort

### 3. Build Product Spec

> Goal: Write the product specification

1. Overview and goals
2. User personas and use cases
3. Feature list with priority
4. User stories in the form `As a [user] I want [feature] so that [benefit]`
5. Acceptance criteria for each feature
6. Metrics and KPIs

### 4. Create Roadmap

> Goal: Plan the development

1. Split into phases: `now`, `next`, `later`
2. Identify dependencies between features
3. Estimate effort roughly (S/M/L)
4. Use `/report` to summarize the roadmap

### 5. Design UX And Pages

> Goal: Design the UX/UI and page structure

1. Use `/follow-design-system` to define design principles
2. Use `/follow-lib-unocss` to install UnoCSS and create HSL theme tokens
3. Plan the page structure: `/` landing, `/features`, `/pricing`, `/user`, `/dashboard`
4. Use `/deep-review-codebase` to check layout, navigation, responsive, CTA
5. Create wireframes/sketches with `/report-uxui` if needed

### 6. Create Website

> Goal: Create the website project

1. Invoke `/follow-create-web` with the product spec and page list
2. Create routes for `/`, `/features`, `/pricing`, `/user`, `/dashboard`
3. Use `/follow-single-responsibility` to check each page/component
4. Test the dev server and build

### 7. Add Authentication

> Goal: Add user auth

1. Invoke `/follow-service-workos` if you need SSO/Directory Sync
2. Or invoke `/follow-lib-better-auth` for in-app auth
3. Create the `/user` page showing profile and settings
4. Protect `/dashboard` with an auth guard

### 8. Add Payments

> Goal: Add billing and pricing

1. Invoke `/follow-service-stripe`
2. Create the `/pricing` page showing plans with CTAs
3. Create the `/user/billing` page for managing subscriptions
4. Connect Stripe webhooks to `/dashboard`

### 9. Build Product Pages

> Goal: Build content and features on each page

1. `/` landing page: hero, value prop, social proof, CTA
2. `/features`: feature list with screenshots/illustrations
3. `/pricing`: plans, comparison, FAQ
4. `/user`: profile, settings, billing shortcut
5. `/dashboard`: overview, metrics, upgrade prompts
6. Use `/implement-to-production` to verify there are no TODO/MOCK/placeholders

### 10. Ship

> Goal: Deliver the product

1. Invoke `/deep-validate` for types, quality, security, cross-reference
2. Invoke `/run-test all` if tests exist
3. Invoke `/ship` to commit and deploy
4. Report the product URL, features, and next actions

## Rules

### 1. MVP First

- Create the product spec before building
- Build one phase at a time
- Do not over-engineer before validating

### 2. User Centric

- Focus on the user problem and benefit on each page
- Every feature should have a user story and acceptance criteria
- Define personas clearly

### 3. Page Conventions

- `/` is the landing page
- `/features` showcases capabilities
- `/pricing` shows plans and CTAs
- `/user` is for profile and billing
- `/dashboard` is for the post-login overview

### 4. No Leaks

- Never hardcode API keys, secrets, credentials
- Use `/follow-secret-manager` for all secrets and environment variable management
- Verify webhook signatures

### 5. UX Quality

- Use `/deep-review-codebase` before shipping
- Make it responsive, dark-mode ready, accessible
- Use design tokens consistently

- Use /open-web-for-config-secret when needed (create product)
- Use /follow-service-cloudflare when deploying on Cloudflare Workers/Pages

## Expected Outcome

- Complete product spec
- User stories with acceptance criteria
- Phased roadmap
- Website runs with all pages in place
- Auth and payments work
- `/pricing`, `/user`, `/dashboard`, `/features` are ready to use
- The product is shipped with a URL and next actions

