---
name: arch-new-org
description: Bootstrap ArchKit for a new organisation — gather org context, configure ARCH_CONFIG.md, clone the repos folder, and populate ARCH_COMMANDMENTS.md. Use when the user asks for /arch-new-org or wants to initialise ArchKit in a new project.
---

You are an expert software architect helping a new organisation set up ArchKit for their codebase.

$ARGUMENTS

Read these files first:
- Base commandments to extend: @.archkit/ARCH_COMMANDMENTS.md
- Org commandments template to fill: @.archkit/ARCH_COMMANDMENTS_TEMPLATE.md
- Current config: @.archkit/ARCH_CONFIG.md

---

You will produce three outputs:
1. A populated `.archkit/ARCH_COMMANDMENTS.md` for this org
2. A configured `.archkit/ARCH_CONFIG.md` — Folder Roots + Repos Discovery
3. A populated `Repos/` folder (or whatever folder the user chose) with the source repos cloned

Do not write anything until all questions in Step 1 are answered.

---

## Step 1 — Gather answers

Ask all of the following at once if the answers have not been provided in $ARGUMENTS. Group them as shown so the user can answer in one block.

### A. Organisation
1. Organisation name?
2. What does the organisation build? (product, domain, purpose)
3. System type? (microservices / modular monolith / monolith / data pipeline / mix)
4. Languages and frameworks? (backend, frontend, data, infrastructure)
5. Repo structure? (monorepo / polyrepo / mixed)
6. Messaging / eventing? (Azure Service Bus / Kafka / RabbitMQ / SQS / none)
7. Primary database?
8. Auth provider?
9. Cloud platform?
10. Any rules about data ownership or cross-service data access?
11. Who approves architecture decisions?
12. Any standing constraints or non-negotiables AI agents must always respect?

### B. Output paths
13. Where should architecture docs be written? (default: `docs/`)
   - Examples: `docs/`, `documentation/`, `arch/`, or empty for repo-root
   - This becomes the **Docs root**. Architecture / Features / Decisions folders sit underneath.
14. Where will source repos live? (default: `Repos/`)
   - Each subfolder = one cloned repo
   - Or pick "scan CWD" if ArchKit will run inside the source repo itself

### C. Repos to track
15. List every repo to track. For each:
   - **Name** (folder name to use under the repos folder)
   - **Git URL** (HTTPS or SSH — leave blank if it should be cloned manually)
   - **One-line description**

---

## Step 2 — Update `.archkit/ARCH_CONFIG.md`

Update only the Folder Roots and Repos Discovery sections based on answers to B.

**Folder Roots** — derive all four from the Docs root:

| Docs root answer | Architecture folder | Features folder | Decisions folder |
|---|---|---|---|
| `docs/` | `docs/architecture/` | `docs/features/` | `docs/decisions/` |
| `arch/` | `arch/architecture/` | `arch/features/` | `arch/decisions/` |
| `` (empty) | `architecture/` | `features/` | `decisions/` |

**Repos Discovery** — set Repos folder to the answer (default `Repos/`). If the user chose "scan CWD", set Repos folder to `.` and remove the fallback line.

Leave the Output Files filenames unchanged — those are stable. Leave Document Layers unchanged.

---

## Step 3 — Set up the repos folder

For the repos folder configured in Step 2:

1. Create it if it does not exist (e.g. `mkdir Repos`).
2. For each repo from question 15 that has a Git URL, run:
   ```
   git clone <url> <repos-folder>/<name>
   ```
   Show the user each clone command before running it. If a clone fails (auth, network), record it and continue — do not abort the whole setup.
3. For each repo without a Git URL, write a one-line stub `<repos-folder>/<name>/README.md` saying "Clone <name> here manually" so the folder structure is clear.
4. After all clones, run `git -C <repos-folder>/<name> log -1 --oneline` for each successful clone to confirm it worked.

If the user chose "scan CWD" in question 14, skip this step entirely.

---

## Step 4 — Populate `.archkit/ARCH_COMMANDMENTS.md`

Complete the org commandments template from ARCH_COMMANDMENTS_TEMPLATE.md using answers from Section A.

Rules:
- Mark every inferred or assumed value as **[SUGGESTED — confirm]**
- Mark every incomplete section as **[TO COMPLETE]**
- Do not invent technology decisions — only record confirmed answers
- Keep Section 9 (AI agent instructions) specific and actionable

---

## Step 5 — Summarise

Output a final summary:

```
## Setup complete

### ARCH_CONFIG.md
- Docs root: <value>
- Repos folder: <value>

### Repos
| Repo | Status |
|---|---|
| name-1 | ✅ cloned |
| name-2 | ⚠️ clone failed — <reason> |
| name-3 | 📝 stub created (clone manually) |

### ARCH_COMMANDMENTS.md
- <N> sections populated
- <N> sections marked [TO COMPLETE]

### Next steps
1. Resolve any [TO COMPLETE] sections in ARCH_COMMANDMENTS.md
2. Manually clone any repos marked ⚠️ or 📝
3. Run `/arch-scan` to produce architecture docs for each repo
```
