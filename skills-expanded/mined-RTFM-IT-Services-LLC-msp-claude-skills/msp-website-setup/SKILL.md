---
name: msp-website-setup
description: Your MSP's standard process for setting up a new static client website hosted on
  your static hosting platform with a git-based dev/prod CI/CD pipeline, plus the
  client-practice rules around it. Use this skill whenever starting a new website project for a
  client, setting up a static site, initializing a website repo, connecting a site to your
  static hosting platform, or wiring up dev and prod deployments for a small business site, even
  if the user just says "let's build a site for this client" or "set up the repo for the new
  website". Also trigger for questions about who owns a client's site, domain, repo, or content,
  which agreements a website project needs (Addendum, SOW, Care Order) and when in the sequence
  (drafting the documents themselves is msp-legal), taking over an existing site, Website Care,
  website accessibility (WCAG, alt text, contrast),
  privacy policy or form-data questions on a client site, and handing a site back at
  offboarding. Load before writing any site code or running git init.
---

# {{COMPANY_NAME}} Static Website Setup

Standard process for standing up a new static client website: paper first, then client info, then git repo with a two-branch pipeline, then hosting on your static hosting platform. The order matters: content and structure decisions are cheaper before any code exists.

Writing form: the setup phase notes, the Website Plan in `COMPANY-INFO.md`, and the deployment steps follow msp-technical-writing (Zone 1, strict mode for steps). Copy for the client's site follows the client's voice, not msp-technical-writing.

## Phase 0: Paper Gate (before any site work)

No website work starts until the right paper is signed and the deposit is in. The documents
are in msp-legal, document-stack entry 13; every number in them comes from msp-pricing
("Websites: Builds and Website Care").

| Situation | Client signs |
|---|---|
| New website build | MSA (if not already signed) + Website Services Addendum + Website Development SOW |
| Build with Website Care | The above + Website Hosting and Care Service Order (one-year minimum) |
| Care only, for a site {{COMPANY_NAME}} did not build | MSA (if not already signed) + Website Services Addendum + Website Hosting and Care Service Order + a fixed-fee SOW for the takeover work (see "Taking Over an Existing Site" below) |

- **The Addendum is signed once per website client.** It carries the ownership model below,
  the client-content warranties, and the third-party platform terms. A later build or Care
  Order for the same client does not need a new one.
- **Offer Care at the SOW stage, not after launch** (msp-sales section 10). A one-year Care
  Order signed on or before the SOW date waives the site setup fee (msp-pricing; $300 as the
  shipped example default). A client who declines Care is a break-fix client for their website
  after launch.
- **Deposit before work.** The build is 50% on signing and before work begins, 50% at launch
  approval or deemed acceptance (msp-pricing, shipped example default). The signed SOW is not
  enough on its own; the first payment must be received.
- **Managed IT clients still get their own website paper.** A build is project work outside
  their managed Order, so it gets its own Development SOW, and Care gets its own Service Order
  under the same MSA. Neither rides along on the managed agreement.
- If someone says "just start the site, we'll paper it later", stop and route to msp-legal.

The website documents are not included in the kit (msp-legal, document-stack entry 13). Draft
them with an attorney licensed in {{STATE}} before your first website client; the drafting
notes in entry 13 cover the Care Order wording.

## Taking Over an Existing Site (Care-Only Clients)

When a client wants {{COMPANY_NAME}} to look after a site it did not build:

1. **Paper first:** MSA + Website Services Addendum + Care Order, plus a fixed-fee SOW for the
   takeover work (Phase 0 table). The takeover is priced from estimated hours at the
   managed-client rate (msp-pricing, "Websites: Builds and Website Care") and quoted before any
   work starts.
2. **Assess before quoting Care.** A static site you can run on your static hosting platform is
   the standard case, and the Care tiers are priced against that platform's plans. A site on a
   platform you do not normally manage (a hosted site builder, a content management system,
   e-commerce) is judged case by case: take it on as it is if you can support it properly, or
   propose a rebuild under a Development SOW. Decide before quoting, and record the decision and
   the reason in `COMPANY-INFO.md`.
3. **Move it into the client's own accounts.** Registrar and hosting account (an account on
   your static hosting platform for a static site) in the client's name, with {{COMPANY_NAME}}
   as administrator, never a {{COMPANY_NAME}}-owned account (msp-onboarding credential
   checklist). For a static site, get the source into a repo under the standard two-branch
   structure (Phases 2 and 3), then connect the hosting platform (Phase 5).
4. **Run the Definition of Done checks** that apply to an existing site: accounts in the
   client's name, privacy policy if it collects form data, accessibility baseline, contact
   links verified.
5. Hand off to msp-maintenance for the recurring Website Care work.

A Care-only client does not go through the full managed-IT process in msp-onboarding.

## Ownership Model

The client owns their website. Specifically:

- The client owns their domain, their content, and their site code.
- The domain registrar account and the static hosting platform account are in the client's name, with {{COMPANY_NAME}} added as an administrator.
- The repo on your git hosting provider is transferred to the client (or their successor provider) at offboarding.
- {{COMPANY_NAME}} retains a license to reuse its generic tooling and pipeline configs (the deployment setup, build scripts, and boilerplate it uses across client sites), not the client's content or design.

The Website Services Addendum (msp-legal document-stack entry 13) states this ownership model, so it is contract, not just practice. The point: no client is ever hostage to {{COMPANY_NAME}} for their own website, and no dispute can turn the site into leverage. This is standing policy, not a one-time decision; apply it to every client site.

## Architecture Overview

- Static site (plain HTML/CSS/JS, no framework unless the project demands one)
- Code on your git hosting provider, one repo per client site
- Hosting on your static hosting platform via its git integration
- A host that auto-deploys from a git branch, with a separate preview/dev branch environment, arranged as a two-branch pipeline:
  - `dev` branch → dev/preview deployment (a preview URL or dev subdomain)
  - `main` branch → production deployment on the client's custom domain
- Workflow: build and review on `dev`, merge to `main` to ship

## Phase 1: Company Info Document (before any code)

Create `COMPANY-INFO.md` in the project root capturing everything about the client before building. Gather from the client and their existing online presence:

- Legal business name, website domain, industry, service area
- Services offered (this becomes the site's core content)
- Contact info: phone, email
- Online presence: social profiles, review sites, and business directory listings
- Key selling points and existing taglines/messaging (reuse their voice)

Also include a "Website Plan" section in the same file: stack, repo/branching model, CI/CD flow, and a to-do checklist. This file doubles as the project brief and the deployment runbook.

### Content and legal checklist (part of Phase 1, before build)

- **Content ownership confirmed in writing.** The client confirms, in writing, that they own or have licenses for all photos and copy they supply. Copyright demand letters routinely target small-business sites over one lifted image; a stock photo grabbed from a web image search is not licensed. Keep the confirmation with the project file.
- **Photo consent for people.** Verify consent for any image showing a recognizable person, and treat photos of children as a hard stop until consent is confirmed. Childcare and education clients carry photo-consent obligations, and a consent failure is an easy, avoidable liability.
- **Privacy policy if the site collects anything.** Any form that takes a name, email, phone, or message means the site collects personal data, and a privacy policy page is required before launch. See msp-legal document-stack entry 11 for the shape of one.
- **Accessibility baseline: WCAG 2.1 AA intent.** Alt text on meaningful images, logical heading order, sufficient color contrast, and keyboard-navigable menus and forms. Check these before launch, not after; accessibility demand letters are the other letter small businesses get.

## Phase 2: Git Repo

```bash
cd <project-folder>
git init -b main
```

Create `.gitignore` before anything else so secrets never get staged:

```gitignore
# Secrets - never commit
.env

# OS junk
.DS_Store

# Dependencies / build output (if ever added)
node_modules/
dist/
```

Commit the info doc and .gitignore, then create the dev branch:

```bash
git add COMPANY-INFO.md .gitignore
git commit -m "Add company info and website plan"
git branch dev
```

## Phase 3: Remote and Push

Repos live in your organization's account on your git hosting provider (name the repo after the site's domain, e.g. `example.com`).

```bash
git remote add origin <your-git-host-url>/<your-org>/<repo>.git
git push -u origin main dev
```

### Token handling (when no credential helper is available)

If pushing from an environment without stored credentials (e.g. a sandbox), use a fine-grained personal access token from your git hosting provider:

- Store it in `.env` as `GIT_HOST_PAT=...` (already gitignored)
- Never hardcode the token in commands that get logged; read it from `.env` and mask it in any output (adjust the token-based push URL syntax to match your git hosting provider):

```bash
PAT=$(grep GIT_HOST_PAT .env | cut -d= -f2)
git push -u "https://x-access-token:${PAT}@<your-git-host>/<your-org>/<repo>.git" main dev 2>&1 | sed "s/${PAT}/***/g"
```

- Recommend rotating the token when the project wraps

### Common push issues

- **Remote already has commits** (the host created a README on repo creation): `git fetch <url> main`, then `git rebase FETCH_HEAD main`, re-point `dev` at the rebased `main` (`git branch -f dev main`), and push. A force push (`+dev`) may be needed for branches pushed before the rebase.
- **`--force-with-lease` rejected with "stale info"**: remote-tracking refs are out of date because you pushed by URL instead of by remote name. Fetch with an explicit refspec first: `git fetch <url> "+refs/heads/*:refs/remotes/origin/*"`, or use `+branch` syntax for a plain force on just that branch.
- **Stale `.git/*.lock` files** (sandboxed environments may fail to unlink them): remove `HEAD.lock`, `index.lock`, and `objects/*/tmp_obj_*` before retrying. In Cowork, if `rm` returns "Operation not permitted", request delete permission with the `allow_cowork_file_delete` tool rather than giving up.

## Phase 4: Build the Site

Build from `COMPANY-INFO.md` content on the `dev` branch. Keep it simple:

- Single-page or small multi-page static HTML/CSS/JS
- Click-to-call phone links (`tel:`), `mailto:` links, and social links throughout
- Mobile-first: most local-service customers arrive on phones
- Include business name, service area, and services in titles/headings for local SEO

### Contact form standard (standing proposal, not yet settled)

When a site needs a contact form, the default is a serverless function on your static hosting platform that emails submissions to the client, with a hidden honeypot field for spam. No third-party form service (such as a hosted form backend) without the client's sign-off, because that puts their visitors' data in a vendor they never chose. Form submissions are the client's data, full stop; {{COMPANY_NAME}} handles them, it does not own them. Flag this as a standing proposal when applying it: it is the working default until you settle it.

## Phase 5: Static Hosting Platform

In your static hosting platform's dashboard, connect the project to your git repo:

1. Connect the repo on your git hosting provider. Framework preset: None; build command: empty; output directory: `/` (or wherever the HTML lives) for a plain static site
2. Set the production branch to `main` (production deploys on push to `main`)
3. Confirm pushes to `dev` automatically create a preview deployment at a preview URL or dev subdomain. Use these for client review
4. Add the custom domain to the production project and follow your host's DNS instructions (easiest when the domain's DNS is already managed by the same platform)

## Definition of Done

- [ ] Signed MSA, Website Services Addendum, and Website Development SOW (plus the Care Order if the client took Care); first 50% payment received
- [ ] `COMPANY-INFO.md` with client info and website plan
- [ ] Content ownership confirmed in writing; photo consent verified for any images of people
- [ ] Git repo with `main` + `dev`, `.gitignore` covering `.env`
- [ ] Repo in your organization's account on your git hosting provider, both branches pushed
- [ ] Site built and reviewed on dev preview URL
- [ ] Privacy policy page live if the site collects any form data
- [ ] Accessibility baseline checked (alt text, heading order, contrast, keyboard navigation)
- [ ] Static hosting platform project connected, custom domain live on `main`
- [ ] Registrar and hosting platform accounts in the client's name with {{COMPANY_NAME}} as administrator
- [ ] Client contact links (phone/email/social) verified on the live site

## At Offboarding

When a client exits, follow msp-offboarding. For their website that means: transfer the repo (on your git hosting provider) to the client or their successor provider, confirm the client controls their registrar, DNS, and static hosting platform account, and remove {{COMPANY_NAME}}'s administrator access last, only after everything else is confirmed in their hands.
