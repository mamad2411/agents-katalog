# Onboarder

A multi-tier Claude Code skill that onboards new hires through conversation. Combines company, domain, and team knowledge into one personalised experience — replacing static handbooks with an interactive guide available from day one.

## Architecture

Three knowledge layers, each in its own GitHub repository:

```
your-org/onboarder                         ← Organisation layer (this repo)
├── SKILL.md                               ← Orchestrator skill
├── registry.json                          ← Points to domain repos
├── data/organisation.json                 ← Company culture, policies, tools
├── templates/
│   ├── domain/                            ← Starter template for new domains
│   │   ├── SKILL.md
│   │   ├── data/domain.json
│   │   └── registry.json
│   └── team/                              ← Starter template for new teams
│       ├── SKILL.md
│       └── data/team.json
└── examples/
    ├── onboarder-domain-engineering/      ← Example domain repo
    │   ├── SKILL.md
    │   ├── data/domain.json
    │   └── registry.json                  ← Points to team repos
    └── onboarder-team-platform/           ← Example team repo
        ├── SKILL.md
        └── data/team.json

your-org/onboarder-domain-engineering      ← Separate repo, owned by domain lead
your-org/onboarder-team-platform           ← Separate repo, owned by team lead
```

### How It Fits Together

```
┌─────────────────────────────────────────────────────┐
│  Orchestrator (this repo)                           │
│  ┌───────────────┐  ┌────────────────────────────┐  │
│  │ organisation  │  │ registry.json              │  │
│  │ .json         │  │  engineering → repo URL    │  │
│  │               │  │  data-science → repo URL   │  │
│  └───────────────┘  └─────────┬──────────────────┘  │
└───────────────────────────────┼──────────────────────┘
                                │ git clone at runtime
                    ┌───────────▼───────────┐
                    │  Domain repo          │
                    │  ┌─────────────────┐  │
                    │  │ registry.json   │  │
                    │  │  platform → URL │  │
                    │  │  payments → URL │  │
                    │  └────────┬────────┘  │
                    └───────────┼───────────┘
                                │ git clone at runtime
                    ┌───────────▼───────────┐
                    │  Team repo            │
                    │  team.json            │
                    └───────────────────────┘
```

### Ownership Model

| Repo | Owned by | Updates require |
|------|----------|-----------------|
| `onboarder` | HR / People team | Only when adding a new domain |
| `onboarder-domain-*` | Domain lead | Only when adding a new team or updating domain knowledge |
| `onboarder-team-*` | Team lead | Anytime — no upstream changes needed |

Teams update their own knowledge independently. No PRs to a central repo. No coordination bottleneck.

## Installation

Add to your Claude Code skills:

```bash
claude skills add github:your-org/onboarder
```

## Setup

### 1. Populate organisation knowledge

Edit `data/organisation.json` with your company's information — name, values, policies, tools, first-day checklist.

### 2. Create a domain repo

```bash
# Copy the template into a new GitHub repo
cp -r templates/domain/ /path/to/onboarder-domain-yourname/

# Edit the SKILL.md — replace DOMAIN_NAME with your domain
# Populate data/domain.json with your domain's knowledge
# Push to GitHub as your-org/onboarder-domain-yourname
```

Then register it in this repo's `registry.json`:

```json
{
  "domains": {
    "yourname": {
      "repo": "your-org/onboarder-domain-yourname",
      "ref": "main",
      "description": "What this domain covers"
    }
  }
}
```

### 3. Create a team repo

```bash
# Copy the template into a new GitHub repo
cp -r templates/team/ /path/to/onboarder-team-yourteam/

# Edit the SKILL.md — replace TEAM_NAME with your team
# Populate data/team.json with your team's knowledge
# Push to GitHub as your-org/onboarder-team-yourteam
```

Then register it in the domain's `registry.json`:

```json
{
  "teams": {
    "yourteam": {
      "repo": "your-org/onboarder-team-yourteam",
      "ref": "main",
      "description": "What this team does"
    }
  }
}
```

### 4. Use it

```
> I'm joining the Platform team in Engineering. Help me get started.
```

The orchestrator reads `registry.json`, clones the engineering domain repo, reads its `registry.json`, clones the platform team repo, then combines all three layers into a personalised onboarding plan.

Ad-hoc questions work too:

```
> What's the deployment process for the platform team?
> Who should I talk to about the API gateway?
> What coding standards does engineering use?
```

## Runtime Flow

1. Orchestrator reads local `data/organisation.json` (always)
2. Orchestrator reads `registry.json` to find the domain repo URL
3. Shallow clone of the domain repo into `/tmp/onboarder-cache/`
4. Read domain's `SKILL.md` and `data/domain.json`
5. Read domain's `registry.json` to find the team repo URL
6. Shallow clone of the team repo into `/tmp/onboarder-cache/`
7. Read team's `SKILL.md` and `data/team.json`
8. Combine all three layers and respond

Clones are cached per-session — no re-cloning within the same conversation.

## Adding Knowledge Conversationally

You don't have to edit JSON by hand. Tell the skill you want to set up a new domain or team:

```
> I want to add the Data Science domain to the onboarder.
```

It will ask questions about your domain and generate the JSON, SKILL.md, and registry entries from your answers.

## Examples

The `examples/` directory contains fully populated example repos:

- `examples/onboarder-domain-engineering/` — A complete engineering domain with architecture, tech stack, standards, and glossary
- `examples/onboarder-team-platform/` — A complete platform team with people, repos, workflows, rituals, and getting-started steps

Use these as reference when populating your own domains and teams. All values are prefixed with "Example:" so you can easily find and replace them.

## Design Principles

- **Distributed ownership.** Each team maintains their own repo. Knowledge stays current because the people closest to it own it.
- **Runtime assembly.** The orchestrator fetches only what it needs. No monorepo that everyone has to update.
- **Most specific layer wins.** If the team has a different process than the domain default, the team version is what the new hire hears.
- **Honest about gaps.** If knowledge hasn't been populated, the skill says so and suggests who to ask — it never fabricates.
- **Composable.** Add or remove domains and teams without affecting others. Just update a registry entry.
