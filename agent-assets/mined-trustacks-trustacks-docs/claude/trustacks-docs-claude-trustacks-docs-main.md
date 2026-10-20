  # trustacks-docs — Working Agreement for Claude Code                            
                                                             
  This file is read automatically at the start of every Claude Code session in    
  this repo. It defines what this repo is, what it isn't, how we work together,
  and how to bootstrap product context.                                           
                                                             
  ## What this repo is

  `trustacks-docs` is the **technical documentation hub** for TruStacks, served at
   `docs.trustacks.com`. Built with:
                                                                                  
  - **Next.js 15+** (App Router) + TypeScript                
  - **Nextra v4** (`nextra-theme-docs`) — MDX-based docs framework
  - **Vercel** hosting; subdomain `docs.trustacks.com`                            
                                                                                  
  It is **not** the marketing site (that's `trustacks-www` at `trustacks.com`). It
   is **not** the product (that's `trustacks-mvp`). The split exists because      
  Nextra v4 wants to own the root layout, which conflicts with the marketing      
  site's chrome. Subdomain isolation is the standard pattern (Stripe, Linear,
  Cursor, Resend all do `docs.<domain>`).

  ## How to pick up product context (deterministic onboarding)                    
  
  Before writing any documentation, read these in order:                          
                                                             
  1. **`README.md`** (this repo) — quick orientation on the docs structure.
  2. **`SITE_BRIEF.md` and `BRAND_GUIDE.md` in `trustacks-www`** — voice rules,
  brand palette, logo assets. Voice on this site MUST match the marketing site    
  exactly; readers shouldn't notice a tonal shift when they cross domains.
     - Local: `/Users/blitzbrgh/Documents/projects/trustacks-www/SITE_BRIEF.md`   
     - Brand assets:                                                              
  `/Users/blitzbrgh/Documents/projects/trustacks-www/public/brand/` (read-only)   
  3. **The canonical product docs in `trustacks-mvp`** — your primary source of   
  technical truth:                                                                
     - `docs/why-trustacks.md` — full-length customer-voice product primer
     - `PROJECT_BRIEF.md` — architectural source of truth                         
     - `UI_DESIGN.md` — visual / design language reference                        
     - `SOFT_LAUNCH_PLAN.md` — Beta launch plan + voice constraints
     - `docs/decisions/0013-open-core-boundary.md` — the open-core story          
     - Local: `/Users/blitzbrgh/Documents/projects/trustacks-mvp/<path>`          
                                                                                  
  If trustacks-www's SITE_BRIEF and a trustacks-mvp canon doc disagree, **the     
  canon doc wins** — flag the drift.                         
                                                                                  
  ## Cross-repo boundary (load-bearing)                      

  **This session must not modify any file outside 
  `/Users/blitzbrgh/Documents/projects/trustacks-docs/`.** Specifically:          
  
  - ❌ Never write to `trustacks-mvp` (product) or `trustacks-www` (marketing).   
  - ❌ Never run state-changing commands (`git`, `make`, `kubectl`, `helm`) 
  against sibling repos.                                                          
  - ❌ Never `cd` into sibling project directories.
  - ✅ You may **read** files in `trustacks-mvp` and `trustacks-www` for context —
   read-only.                                                                     
  
  The reciprocal boundary holds: sessions in those repos won't write here. If you 
  discover content drift in a sibling repo (e.g., a feature documented here that's
   been removed from trustacks-mvp), surface it to the user — let the *other* 
  session ship the fix.

  **Carve-out — trustacks-mvp session as authorized contributor (locked
  2026-05-18).** The trustacks-mvp session may also write here for sweeping
  mvp-derived changes — renamed CLI flags, updated diagrams, new reference
  pages when a slice ships customer-visible surface — that would otherwise
  need a handoff prompt. Both sessions follow PR-only on `main` + the
  CodeRabbit-on-every-PR rule; coordinate via the user when both sessions
  might touch overlapping files the same day. The trustacks-www session
  has no such carve-out — it still won't write here. Reciprocal entry
  lives in the trustacks-mvp CLAUDE.md sibling-repos section.                                                           
                                                             
  ## Working agreement

  Mirror the trustacks-www workflow:
                                                                                  
  - **PR-only on `main`**. Every change goes through a feature branch + PR.
  - **Conventional-commits with path scope**: `docs(getting-started): add         
  prerequisites`, `feat(reference): document MCP server integration`,             
  `chore(theme): bump nextra to 4.7`, `fix(installation): correct ArgoCD command`.
  - **One slice = one focused PR.** No bundling unrelated changes.                
  - **Branch only off main, target only main.** No stacked PRs — CodeRabbit's 
  auto-review skips PRs targeting non-default branches.                           
  - **CodeRabbit on every PR.** Wait for the review, triage each comment, reply 
  inline with the commit hash that addressed it. Don't declare a PR ready until   
  CodeRabbit is happy. (See trustacks-www's `feedback_coderabbit_on_every_pr` 
  memory for the polling pattern — count final summary comments excluding the     
  - **Voice constraint, non-negotiable.** Coworker-not-replacement framing for 
  agents. Anti-patterns: *"fully autonomous,"* *"replace your DevOps team,"* *"set
   it and forget it."*                                                            
  - **No em-dashes** in customer-facing copy. Use periods, colons, commas, or 
  parentheses. Interpunct (`·`) is the brand-rhythm separator and is preserved.   
  - **"Agents propose. Policy decides. Humans approve."** is the canonical        
  three-beat. "Decides" not "disposes."                                    
  - **Specialist Pack** is the canonical add-on term. "Practice Pack" and         
  "compliance pack" are retired customer-facing.                          
                                                                                  
  ## Stack — committed decisions                             
                                                                                  
  - **Framework:** Next.js 15+ (App Router), TypeScript 5+   
  - **Docs theme:** Nextra v4 (`nextra-theme-docs`). The Nextra Layout owns the 
  root — that's why we're not in trustacks-www.                                   
  - **Styling:** Nextra's built-in theme. Override colors via CSS variables to    
  match the brand palette (Deep Navy `#0F172A` = `--background-dark`, Green-Teal  
  `#10B981` = accent). Don't import Tailwind.                                     
  - **Deployment:** Vercel auto-deploy on `main` push to `docs.trustacks.com`; 
  preview URL per PR.                                                             
  - **Search:** Pagefind via Nextra's built-in integration (`postbuild: pagefind  
  --site .next/server/app --output-path public/_pagefind`). The
  `--output-path` is load-bearing: Nextra's search client fetches
  `/_pagefind/pagefind.js`, so the index has to land in `public/`, not in the
  `.next/server/app` build directory (which is never served).                   
  - **Analytics:** Vercel Analytics. No third-party trackers.                     
                                                             
  ## Repo layout (target)                                                         
                                                             
                                                                                  
  trustacks-docs/                                            
  ├── README.md
  ├── CLAUDE.md                   # this file                                     
  ├── next.config.mjs             # withNextra wrap
  ├── mdx-components.tsx          # Nextra theme MDX components                   
  ├── tsconfig.json                                                               
  ├── public/      
  │   └── brand/                  # logo + favicon (copy from                     
  trustacks-www/public/brand)                                
  ├── app/                                                                        
  │   ├── layout.tsx              # Nextra Layout at root (owns html/body)
  │   ├── page.mdx                # /docs landing (overview + nav)                
  │   ├── _meta.js                # top-level sidebar config                      
  │   ├── getting-started/                                  
  │   │   ├── _meta.js                                                            
  │   │   └── *.mdx                                          
  │   ├── installation/                                                           
  │   │   ├── _meta.js                                       
  │   │   └── *.mdx   
  │   ├── workshops/                                                              
  │   │   ├── _meta.js
  │   │   └── *.mdx                                                               
  │   └── reference/                                         
  │       ├── _meta.js
  │       └── *.mdx   
  └── .coderabbit.yaml            # match trustacks-www config                    
  
  Note: `contentDirBasePath` in `next.config.mjs` should be `/` (this repo's      
  content lives under `app/`, not `app/docs/`, since the entire site IS the docs).
                                                                                  
  ## Brand consistency with marketing site                                        
                                                             
  - **Logo + favicon:** copy the relevant PNGs from `trustacks-www/public/brand/` 
  into `public/brand/` here. Don't re-create.
    - `logo-icon.png` → favicon + Navbar icon                                     
    - `logo-color.png` → full-wordmark uses (e.g., OG cards)                      
    - `logo-reversed.png` → dark backgrounds                                      
  - **Colors:** match the brand palette exactly. Deep Navy `#0F172A` / Slate      
  `#475569` / Light Slate `#94A3B8` / Pale Slate `#E2E8F0` / Green-Teal `#10B981`.
   Override Nextra's theme CSS variables to hit these.       
  - **Wordmark text:** "TruStacks" in Nextra's default Inter-like font is fine;   
  close enough match to marketing's Inter.                                        
  - **Header link back to marketing:** add a Nextra Navbar link to
  `https://trustacks.com` so docs visitors can get back to marketing.             
                                                             
  ## Initial content scaffold (target by Beta, July 2026)                         
                                                             
  Skeleton pages to create first (even if mostly placeholder):                    
                                                             
  - `/` (page.mdx) — overview + nav                                               
  - `/getting-started/quickstart` — install runner, point at first repo, see your
  first PR                                                                        
  - `/installation/local-dev` — local development environment
  - `/installation/cluster` — k3d / k3s / production cluster deploy               
  - `/installation/secrets` — credential setup               
  - `/installation/gitops` — ArgoCD/Flux integration                              
  - `/workshops/ci-cd-generation` — guided walk through a CI/CD generation crew
  run                                                                             
  - `/workshops/policy-authoring` — write your first customer-overlay Rego rule
  - `/reference/architecture` — high-level architecture (matches                  
  trustacks.com/product overview)                                                 
  - `/reference/constitution` — what's in the constitution
  - `/reference/specialist-packs` — SOC 2, HIPAA, PCI, FedRAMP, ITIL pack contents
  - `/reference/runner-cli` — CLI commands                                        
  - `/reference/mcp-server` — MCP server integration surface (TruStacks consumes  
  from customer-side MCP servers)                                                 
  - `/reference/policy-linter` — Rego linter usage                                
                                                                                  
  Start with skeleton stubs; fill them in iteratively. Each page can be a PR.     
                                                                                  
  ## What to ask permission for                                                   
                                                             
  **Pre-authorized inside this repo:**
  - Reading/writing files in `/Users/blitzbrgh/Documents/projects/trustacks-docs/`
  - `git add`, `git commit`, `git checkout -b <branch>`, `git push -u origin      
  <feature-branch>`
  - `gh pr create`, `gh pr view`, `gh pr checks`, `gh pr comment`                 
  - `npm install` / `pnpm add` / dev-server commands                              
  - Reading sibling repos for context
                                                                                  
  **Always ask before:**                                     
  - `gh pr merge` — explicit per-PR user OK                                       
  - Anything that touches `trustacks-mvp` or `trustacks-www` 
  - Force-push, rebasing published commits, destructive git operations            
  - Adding a paid third-party service
  - Quoting a price not already in trustacks-www's `SITE_BRIEF.md` — pricing is   
  the user's call (defer to marketing)                                            
  - Naming competitors in published copy — voice review required (same rule as    
  trustacks-www)                                                                  
                                                             
  ## Style and conventions                                                        
                                                             
  - **MDX:** GitHub-flavored markdown. Code blocks with language tags. Use        
  Nextra's `<Callout>` for Note/Tip/Warning/Error admonitions.
  - **Headings:** sentence case. No trailing periods on H1/H2/H3.                 
  - **Code samples:** always runnable. Prefer Bash for shell, TypeScript/Rego for 
  code where applicable.                                                          
  - **Cross-linking:** internal Nextra links. External links to `trustacks.com`   
  open same tab (same brand). Links to `github.com/TruStacks/*` open new tab.     
  - **Frontmatter:** every MDX page has `title:` and `description:` for SEO and
  Nextra sidebar.                                                                 
                                                             
  ## What this repo will never do                                                 
                                                             
  - **Sell anything.** Pricing lives at `trustacks.com/pricing`. Link there, don't
   replicate.
  - **Substitute for marketing voice.** Positioning is owned by `trustacks-www`.  
  If documentation needs a positioning beat, lift it from `SITE_BRIEF.md` — don't 
  invent.
  - **Host customer data.** No accounts, no logins, no personalization.           
  - **Link to internal/private resources.** All links public.

  ## Current phase                                                                
  
  **Bootstrap (2026-05-12).** Repo created. First PR should:                      
  1. `npm i nextra nextra-theme-docs` (+ standard Next.js setup)
  2. Configure `next.config.mjs` with `withNextra(...)` wrap                      
  3. Create root `app/layout.tsx` per Nextra v4 example pattern (Layout at root,
  owns html/body)                                                                 
  4. Add `mdx-components.tsx` at repo root                   
  5. Copy brand PNGs from `trustacks-www/public/brand/` into `public/brand/`      
  6. Create `app/page.mdx` skeleton with overview + navigation                    
  7. Add `app/_meta.js` with the four top-level sections (getting-started,        
  installation, workshops, reference)                                             
  8. Create one skeleton page per section so the navigation isn't empty
  9. Add `.coderabbit.yaml` matching trustacks-www's config                       
  10. Confirm `docs.trustacks.com` Vercel deploy is wired    
  11. Verify the link from `trustacks.com` nav resolves correctly                 
    After that, individual content PRs fill in skeletons.                                                                                                           
