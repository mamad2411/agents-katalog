# AI Agent Instructions — SaaS Playbook

You are helping a founder build out their complete SaaS company operating system. This repository contains 26 departments with 130+ subfolders, each with an `INSTRUCTIONS.md` file that tells you what to create.

## Your Mission

Help the founder populate every folder with actionable, specific documentation for their SaaS startup. You are not generating generic advice — you are creating their actual operating documents.

## How to Work Through This Playbook

### Step 1: Gather Context

Before populating any folders, you need to understand the founder's SaaS. Ask these questions if the answers aren't already provided:

1. **What is the name of your SaaS?**
2. **Describe your product in 2-3 sentences. What does it do?**
3. **Who is your target customer?** (e.g., "small business owners", "enterprise DevOps teams", "freelance designers")
4. **What problem does it solve?** (the specific pain point)
5. **How do you plan to make money?** (subscription tiers, usage-based, freemium, etc.)
6. **What stage are you at?** (idea, building MVP, launched, growing)
7. **What's your team size?** (solo, 2-5, 5-20, 20+)
8. **What's your budget/runway?** (bootstrapped, pre-seed, seed, Series A+)

Store the answers in `company-profile.md` at the root of this repository.

### Step 2: Work Through Departments in Order

The departments are numbered 01-26 for a reason. Work through them sequentially:

```
01-idea → 02-validation → 03-planning → 04-design → 05-development →
06-infrastructure → 07-testing → 08-launch → 09-acquisition →
10-distribution → 11-conversion → 12-revenue → 13-analytics →
14-retention → 15-growth → 16-scaling →
17-legal → 18-finance → 19-sales → 20-customer-success →
21-product-management → 22-brand-and-positioning → 23-documentation →
24-competitive-intelligence → 25-data-and-ai → 26-people-and-culture
```

However, skip departments that aren't relevant to the founder's current stage. For example:
- If they're pre-launch, focus on 01-08, plus 17-legal, 18-finance, 22-brand
- If they're post-launch looking to grow, focus on 09-16 and 17-26
- If they need everything, go through all 26

### Step 3: For Each Subfolder

1. Read the `INSTRUCTIONS.md` file in the subfolder
2. Note the YAML frontmatter for priority, dependencies, and estimated time
3. Ask the founder any clarifying questions listed in the instructions
4. Generate the output document(s) specified in the instructions
5. Save the output in the same subfolder (not in a different location)

### Step 4: Generate Cross-References

After populating folders, create links between related documents. For example:
- The pricing strategy (11-conversion/pricing-strategy) should reference the revenue model (12-revenue/subscriptions)
- The tech stack (03-planning/tech-stack) should align with infrastructure choices (06-infrastructure)
- The content marketing plan (09-acquisition/content-marketing) should reference SEO strategy (09-acquisition/seo-wins)

## Output Format Rules

When generating documents for each subfolder, follow these rules:

1. **Use Markdown** — all output files should be `.md` files
2. **Be specific** — use the founder's actual product name, target customer, and details (never use placeholder text like "[Your Product]" in final output)
3. **Be actionable** — every section should contain things the founder can act on today
4. **Include metrics** — wherever possible, include specific KPIs and targets
5. **Include timelines** — give realistic time estimates for each action item
6. **Link to tools** — recommend specific tools (free and paid) for each department
7. **Prioritize** — mark items as P0 (must do), P1 (should do), P2 (nice to have)

## File Naming Convention

- Main output document: `README.md` (in each subfolder, alongside INSTRUCTIONS.md)
- Supporting documents: `[descriptive-name].md`
- Templates: `template-[name].md`
- Checklists: `checklist-[name].md`

## Handling Dependencies

Some folders depend on others being filled out first. The YAML frontmatter in each `INSTRUCTIONS.md` has a `requires` field listing dependencies. Check if those folders have been populated before proceeding. If not, either:
- Go fill them out first, or
- Ask the founder for the missing information directly

## Quality Checklist

Before marking a folder as complete, verify:

- [ ] All template sections are filled with specific, non-generic content
- [ ] Metrics and KPIs are included where relevant
- [ ] Action items have owners and timelines
- [ ] Tool recommendations are current and relevant
- [ ] Cross-references to other departments are included
- [ ] The founder has reviewed and approved the content

## Context Window Management

This repository is large. To work efficiently:

1. Don't try to read all files at once
2. Work through one department at a time
3. Keep the `company-profile.md` loaded for context
4. Reference specific files by path when creating cross-links

## Supported Workflows

### Cursor (Composer)
- Open the repo in Cursor
- Use Composer to read this file and the company profile
- Work through departments one at a time using Composer

### GitHub Copilot Workspace
- The structured INSTRUCTIONS.md files work as natural prompts
- Copilot can fill in templates based on the company profile

### OpenAI Codex / ChatGPT Code Interpreter
- Share the AGENTS.md and company-profile.md
- Work through departments sequentially in conversation

### Claude / Any LLM
- Same approach — share context, work through departments
- Use the YAML frontmatter to prioritize which folders to tackle first

### Devin / SWE-Agent / Autonomous Agents
- Clone the repo
- Read this AGENTS.md file first
- Create company-profile.md from user input
- Autonomously populate all folders following the instructions
- Create a summary PR when complete
