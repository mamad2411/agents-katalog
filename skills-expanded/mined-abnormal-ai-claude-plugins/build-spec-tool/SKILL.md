# /build-spec-tool

Bootstrap any monorepo with spec-driven development infrastructure. Creates `.ai-dev/` knowledge files, a planning template, review agent, and CLI wrapper.

## What This Creates

```
target-repo/
├── .ai-dev/
│   ├── ARCHITECTURE.md          # Tech stack, patterns, conventions
│   ├── SECURITY.md              # Data classification, access controls, encryption
│   ├── LEGAL.md                 # Data residency, retention, compliance
│   ├── PLAN.md                  # Spec template for implementation plans
│   └── SYSTEM_PROMPT.md         # Planning methodology (injected by bin/plan)
├── .claude/agents/
│   └── plan-review-agent.md     # Reviews plans against .ai-dev/ standards
├── bin/plan                     # Shell wrapper to launch spec generation
└── CLAUDE.md                    # Updated with .ai-dev/ references
```

## Workflow (5 Phases)

### Phase 1: Discovery (parallel)

Run two things simultaneously:

**Codebase exploration** -- spawn 2-3 Explore agents to analyze:
- Tech stack: languages, frameworks, build systems, CI/CD
- Architecture: services, databases, APIs, event systems
- Conventions: testing patterns, linting, PR templates, code ownership

```
Task(subagent_type="Explore", description="Analyze tech stack", prompt="Identify all languages, frameworks, build systems, and CI/CD patterns in this repo. Look at package.json, go.mod, requirements.txt, Makefile, Dockerfile, .github/workflows/, etc.")
Task(subagent_type="Explore", description="Map architecture", prompt="Map the service architecture: find all services/apps, databases, message queues, API patterns. Look at docker-compose, k8s manifests, terraform, service definitions.")
Task(subagent_type="Explore", description="Find conventions", prompt="Identify testing conventions, linting config, PR templates, CODEOWNERS, existing dev docs (*_dev.md, *_usage.md, CONTRIBUTING.md).")
```

**User document ingestion** -- ask the user to provide or paste:
- Existing architecture docs, ADRs, design docs
- Security policies, data classification rules
- Legal/compliance requirements, DPAs
- API conventions, coding standards

Use AskUserQuestion:
```
"Do you have existing documentation to incorporate? I'll use these to populate your .ai-dev/ files."
Options:
- "Yes, I'll paste/provide paths" -> collect and read them
- "No, let's build from scratch" -> proceed to interview
- "Some -- let me share what I have" -> collect partial, fill gaps in interview
```

### Phase 2: Optional Interview (3-5 rounds)

Ask if the user wants to be interviewed to fill gaps. If yes, conduct focused rounds:

1. **Architecture**: Language choices and why, database selection criteria, service communication patterns, deployment model (k8s, serverless, VMs)
2. **Data & Multi-tenancy**: How tenants are identified, data residency requirements, retention policies
3. **Security**: Data classification tiers, auth patterns (SSO, JWT, mTLS), secrets management, encryption requirements
4. **Legal/Compliance**: Regulated industries (healthcare, finance, education), AI/ML data restrictions, third-party DPA requirements
5. **Process**: PR review expectations, testing requirements (coverage, mocking policy), deployment/rollout patterns, feature flag strategy

Each round: show 5-10 bullet points of drafted content, get feedback, iterate.

### Phase 3: Generate Core Files

Read the reference templates from this skill's `references/` directory, then generate each file customized for the target repo:

1. **`.ai-dev/ARCHITECTURE.md`** -- Read `references/architecture_template.md` for structure. Fill in with the repo's actual tech stack, database choices, API patterns, testing conventions, and observability setup discovered in Phase 1-2.

2. **`.ai-dev/SECURITY.md`** -- Read `references/security_template.md` for structure. Fill in with the org's data classification rules, access control patterns, encryption requirements, and AI/ML policies.

3. **`.ai-dev/LEGAL.md`** -- Read `references/legal_template.md` for structure. Fill in with compliance frameworks, data residency rules, retention policies, and third-party service requirements.

4. **`.ai-dev/PLAN.md`** -- Copy from `references/plan_template.md`. Customize the Verification sections with the repo's actual test/lint/build commands discovered in Phase 1.

5. **`.ai-dev/SYSTEM_PROMPT.md`** -- Copy from `references/system_prompt.md`. Customize:
   - Replace references to documentation index files with the repo's actual doc discovery patterns
   - Update ticket/issue tracker references to match the repo's tooling (GitHub Issues, Linear, Jira, etc.)

6. **Update `CLAUDE.md`** -- Append the content from `assets/claude_md_snippet.md` to the repo's existing `CLAUDE.md` (create if it doesn't exist).

### Phase 4: Create Shell Wrapper

1. Read `scripts/plan.sh` for the template
2. Generate `bin/plan` from the template
3. Make executable: `chmod +x bin/plan`
4. Ask the user if they prefer a different location (e.g., `scripts/plan` or a Makefile target)

### Phase 5: Create Plan Review Agent

1. Read `references/plan_review_agent.md`
2. Create `.claude/agents/plan-review-agent.md` in the target repo
3. No customization needed -- the agent reads `.ai-dev/` files dynamically

## After Bootstrap

Present the user with a summary of what was created and next steps:

```
Spec-driven development infrastructure is set up. Here's what was created:

.ai-dev/ARCHITECTURE.md  -- [brief summary of what's in it]
.ai-dev/SECURITY.md      -- [brief summary]
.ai-dev/LEGAL.md          -- [brief summary]
.ai-dev/PLAN.md           -- Spec template for implementation plans
.ai-dev/SYSTEM_PROMPT.md  -- Planning methodology for bin/plan
.claude/agents/plan-review-agent.md -- Validates plans against standards
bin/plan                  -- Launch spec-driven planning sessions

Next steps:
1. Review each .ai-dev/ file and refine as needed
2. Try it: bin/plan "add user authentication"
3. Commit the .ai-dev/ directory and bin/plan to your repo
```

## Critical: No Guessed or Assumed Content

When filling in ARCHITECTURE.md, SECURITY.md, and LEGAL.md, **only include content that is directly sourced from**:

1. **Codebase evidence** -- patterns, tools, and conventions actually found by Explore agents in the repo
2. **User-provided documentation** -- docs, policies, or text the user explicitly provided or pointed to
3. **User interview answers** -- statements the user made during the interview rounds

**Never**:
- Guess at security policies, compliance frameworks, or legal requirements the user hasn't stated
- Assume database choices, auth patterns, or infrastructure details not found in the codebase
- Fill sections with generic best-practice content that wasn't sourced from the user or repo
- Infer organizational policies from the tech stack (e.g., don't assume "GDPR compliance" because there's an EU region)

If a section in the template can't be filled because the user hasn't provided the information and it wasn't discovered in the codebase, **leave the template placeholder brackets intact** with a note like `[Not yet documented -- fill in your org's policy here]`. An empty section with honest placeholders is better than a section with fabricated content that the user then trusts as ground truth.

The `.ai-dev/` files become the source of truth for all future planning. Inaccurate content here propagates into every plan the system generates.

## Other Important Notes

- **Never overwrite existing files** without asking. If `.ai-dev/ARCHITECTURE.md` already exists, show a diff and ask if they want to merge or replace.
- **The PLAN.md template is mostly universal** -- the main customization is the Verification section commands.
- **SYSTEM_PROMPT.md customization is light** -- mainly updating documentation discovery patterns and issue tracker references.
- **ARCHITECTURE.md requires the most work** -- it should reflect the repo's actual patterns, not generic advice.
- **All reference files are in this skill's `references/` directory** -- read them before generating.
