# ScholarSkill - Academic Paper Reading and Knowledge Internalization

**Description**: An Obsidian-based L3-grade paper reading and memory extraction system.

**Version**: v1.0.0  
**Last Updated**: 2026-03-18

---

## Setup Guide Before First Use

**Welcome to ScholarSkill!** Owl mascot included.

Before reading papers, complete the setup flow below. This package supports three setup modes.

### Setup Modes

#### Mode 1: Fully Automatic Setup (`auto`)

```bash
# Choose the English package first, then explicitly point to the target Obsidian vault
python ~/.openclaw/workspace-scholar/skills/scholar-skill/en/scripts/configure.py auto --vault-path "/your/Obsidian/Vault"
```

**Best for**: first-time users with Obsidian already installed  
**Automatically handles**:
- detecting the Obsidian vault location
- creating the folder structure (`1-Papers`, `2-Knowledge`, `3-MOCs`, `memory`, and more)
- generating the config file
- checking dependency skills

**Note**: it is strongly recommended to always pass `--vault-path` so the script never selects the wrong vault and only syncs the English templates.

---

#### Mode 2: Semi-Automatic Setup (`semi`) - Recommended

```bash
# Run the English package setup script and explicitly provide the target vault
python ~/.openclaw/workspace-scholar/skills/scholar-skill/en/scripts/configure.py semi --vault-path "/your/Obsidian/Vault"
```

**Best for**: users who want to confirm each step  
**Flow**:
1. detect the Obsidian vault automatically, or prompt you if needed
2. ask whether to create the folder structure
3. check dependency skills and ask whether to install them
4. generate the config file

---

#### Mode 3: Manual Setup (`manual`)

```bash
# Run the English package setup script and explicitly provide the target vault
python ~/.openclaw/workspace-scholar/skills/scholar-skill/en/scripts/configure.py manual --vault-path "/your/Obsidian/Vault"
```

**Best for**: advanced users who know exactly what they want  
**Flow**:
1. enter the Obsidian vault path manually
2. skip directory creation for now
3. only check dependencies without prompting installation
4. generate a minimal config file

---

### Dependency Skills

ScholarSkill depends on the following skills. The setup script checks these automatically.

### Core Dependencies (Required)

| Skill | Purpose | Required |
|------|------|------|
| `obsidian-direct` | Obsidian file operations | ⭐⭐⭐ |
| `arxiv-watcher` | ArXiv paper search | ⭐⭐⭐ |

### Enhancements (Recommended)

| Skill | Purpose | Required |
|------|------|------|
| `academic-research-hub` | Multi-source academic search | ⭐⭐ |
| `tavily` | Web content extraction | ⭐⭐ |
| `pdf` | PDF text extraction | ⭐⭐ |
| `obsidian-cli` | Obsidian CLI utilities | ⭐⭐ |

### Long-Running Task Orchestration (Required for L3 / batch processing)

| Skill | Purpose | Required |
|------|------|------|
| `durable-task-runner` | long-task orchestration, progress tracking, crash recovery | ⭐⭐⭐ (`L3` / batch) |

**Why `durable-task-runner` matters**
- `L3` deep reading (2.5 hours): needs progress tracking and interruption recovery
- batch reading (10+ papers): needs orchestration and step retries
- weekly consolidation (60-90 minutes): needs persistent state and scheduled execution
- crash recovery: work can continue after session interruption
- transparent progress: task state stays visible

**Install commands**
```bash
# Core dependencies (via ClawHub)
clawhub install obsidian-direct
clawhub install arxiv-watcher

# Recommended enhancements
clawhub install academic-research-hub
clawhub install tavily
clawhub install pdf
clawhub install obsidian-cli

# Long-running orchestration (required for L3 / batch workflows)
clawhub install durable-task-runner
```

**Manual installation** (if ClawHub is unavailable):
```bash
cd ~/.openclaw/workspace-scholar/skills
git clone https://github.com/OpenClaw/obsidian-direct.git
git clone https://github.com/OpenClaw/arxiv-watcher.git
# ...install the others the same way
```

---

### Config File

After setup, the config file is written to:

```text
~/.openclaw/workspace-scholar/config/scholar.yml
```

If that directory does not exist, the script falls back to:

```text
~/.openclaw/workspace/config/scholar.yml
```

**Key config fields**
```yaml
obsidian:
  vault_path: /Users/your-name/ObsidianVault  # auto-detected or entered manually

reading:
  default_level: L2  # L1 / L2 / L3

notification:
  feishu_enabled: false
```

---

### Frequently Asked Questions

**Q: What if the Obsidian vault cannot be found?**  
A: Use semi-automatic or manual mode and provide the path yourself. If Obsidian is not installed yet, install it first from [obsidian.md](https://obsidian.md).

**Q: What if dependency installation fails?**  
A: Use `clawhub install <skill-name>`. If ClawHub is unavailable, clone the skill into `~/.openclaw/workspace-scholar/skills/`.

**Q: Can I change the config later?**  
A: Yes. Edit `~/.openclaw/workspace-scholar/config/scholar.yml` or `~/.openclaw/workspace/config/scholar.yml`.

**Q: I configured the wrong thing. How do I reset?**  
A: Remove the config file and rerun the English package setup:
`rm ~/.openclaw/workspace-scholar/config/scholar.yml && python ~/.openclaw/workspace-scholar/skills/scholar-skill/en/scripts/configure.py auto --vault-path "/your/Obsidian/Vault"`

---

## Trigger Phrases

- "read this paper"
- "deep read"
- "L1/L2/L3 reading"
- "paper notes"
- "knowledge internalization"
- "configure ScholarSkill"

---

## Common Use Cases

- academic paper reading (ArXiv / conference / journal)
- deep reading of technical blog posts
- literature review organization
- domain exploration and research mapping

---

## Core Capabilities

### 1. Three-Tier Reading Standard

#### `L1` Quick Triage (5 minutes)
- read the title, abstract, and figures
- output: one-sentence summary + priority rating (`P0/P1/P2`)
- best for: screening `P2` papers

#### `L2` Standard Reading (45 minutes)
- read the introduction, method, experiments, and conclusion
- output: 3-5 KB note + 5-8 memory items
- best for: `P1` papers and daily reading

#### `L3` Deep Reading (2.5 hours)
- full method details, experiment analysis, and supplementary material
- output: 10-15 KB note + knowledge upgrade + 2-3 procedural rules
- best for: `P0` papers that are core to your direction

### 2. Memory Extraction

**Semantic Memory**: facts, concepts, methods, and conclusions  
**Episodic Memory**: questions, misunderstandings, and correction processes  
**Procedural Memory**: reusable reading rules and research methods

### 3. Knowledge Management

- Obsidian bidirectional links
- MOC knowledge maps
- atomic knowledge storage
- weekly consolidation mechanisms

### 4. Reflection and Confirmation

- `L1` reflection: quick check of understanding, questions, and next actions after each paper
- `L2` reflection: weekly review of knowledge growth, missing links, direction, and risks
- `L3` reflection: monthly review of knowledge evolution, direction shifts, and belief revision
- human confirmation: new MOCs, core papers, major conflicts, and direction changes enter `0-Inbox/`

---

## Workflow

```text
1. Receive a paper (PDF / ArXiv URL / local file)
2. Evaluate priority (P0 / P1 / P2)
3. Choose reading depth (L1 / L2 / L3)
4. Read and generate notes
5. Extract memories (Semantic / Episodic / Procedural)
6. Update `2-Knowledge/` (Concept / Insight / Method / Question / Person)
7. Connect knowledge (bidirectional links + MOC updates)
8. Write reflections / confirmation requests / reports
```

---

## Configuration Example

```yaml
# ~/.openclaw/workspace-scholar/config/scholar.yml or ~/.openclaw/workspace/config/scholar.yml
# The setup script prefers ~/.openclaw/workspace-scholar/config/ when available
obsidian:
  inbox_folder: 0-Inbox
  vault_path: /Users/your-name/ObsidianVault
  paper_notes_folder: 1-Papers
  knowledge_folder: 2-Knowledge
  concepts_folder: 2-Knowledge/Concepts
  insights_folder: 2-Knowledge/Insights
  methods_folder: 2-Knowledge/Methods
  questions_folder: 2-Knowledge/Questions
  people_folder: 2-Knowledge/People
  moc_folder: 3-MOCs
  outputs_folder: 4-Outputs
  reflections_folder: 4-Outputs/Reflections
  confirmation_records_folder: 4-Outputs/Confirmation-Records
  templates_folder: 9-Templates/en
  memory_folder: memory

reading:
  default_level: L2
  enable_memory_extraction: true
  enable_knowledge_consolidation: true

notification:
  feishu_enabled: false
  feishu_user_id: ou_xxxxxxxxxxxxx
```

The setup script syncs the English templates into:

```text
{vault}/9-Templates/en/
```

---

## Outputs

### 1. Paper Notes
Location: `{vault}/1-Papers/By-Topic/{Topic}/{Year}-{Author}-{Title}.md`

### 2. Semantic Memory
Location: `{vault}/memory/semantic/{Topic}.md`

### 3. Procedural Memory
Location: `{vault}/memory/procedural/{Topic}.md`

### 4. Episodic Memory
Location: `{vault}/memory/episodic/{Date}-{Paper}.md`

### 5. MOC Updates
Location: `{vault}/3-MOCs/MOC-{Topic}.md`

### 6. Concept Cards
Location: `{vault}/2-Knowledge/Concepts/`

### 7. Insight Cards
Location: `{vault}/2-Knowledge/Insights/`

### 8. Question Cards
Location: `{vault}/2-Knowledge/Questions/`

### 9. Method Cards
Location: `{vault}/2-Knowledge/Methods/`

### 10. Person Cards
Location: `{vault}/2-Knowledge/People/`

### 11. Reflection Outputs
Location: `{vault}/4-Outputs/Reflections/L1|L2|L3/`

### 12. Confirmation Requests
Location: `{vault}/0-Inbox/`

---

## Usage Examples

### Example 1: `L2` Standard Reading

```text
User: Please read this paper at L2 depth.
Attachment: paper.pdf

Agent:
1. Evaluate priority -> P1
2. Perform L2 reading (45-minute standard)
3. Generate the note (3-5 KB)
4. Extract 5-8 memory items
5. Create Concept / Insight / Question / Method cards when needed
6. Update links and the MOC
7. Generate an L1 reflection
8. Output the report
```

### Example 2: `L3` Deep Reading

```text
User: Please deep-read ArXiv:2407.19354 at L3 depth.

Agent:
1. Retrieve the paper (ArXiv API)
2. Evaluate priority -> P0 (directly relevant to the core direction)
3. Perform L3 reading (2.5-hour standard)
4. Generate a deep note (10-15 KB)
5. Upgrade knowledge and revise old knowledge
6. Distill 2-3 procedural rules
7. Update `2-Knowledge/` and `3-MOCs/`
8. If conflicts or new directions appear, create a confirmation request in `0-Inbox/`
9. Generate a deep reflection and push the detailed report
```

### Example 3: Batch Reading

```text
User: Screen these 10 papers with L1 first, then run L2 reading on the P0 / P1 papers.

Agent:
1. Run batch L1 triage (5 minutes per paper)
2. Classify priorities: P0 (2 papers) + P1 (5 papers) + P2 (3 papers)
3. Run L3 on the P0 papers
4. Run L2 on the P1 papers
5. Archive the P2 papers only
6. Run an L2 reflection on the weekend and organize concepts / MOCs
7. Output a summary report
```

---

## Quality Checklist

### `L2` Checklist
- [ ] standard note complete (3-5 KB)
- [ ] 3-5 Semantic Memories
- [ ] 1-2 Episodic Memories
- [ ] 1 candidate Procedural Memory
- [ ] each memory has an `action` field
- [ ] links to prior knowledge are described

### `L3` Checklist
- [ ] all `L2` requirements satisfied
- [ ] resident vs retrieval memory split completed
- [ ] at least one prior knowledge group revised or evaluated
- [ ] at least 2-3 procedural rules distilled
- [ ] conflicts, time evolution, or deprecated knowledge marked
- [ ] answer: "How does this paper change my knowledge structure?"

### `2-Knowledge` Update Checklist
- [ ] should a Concept card be created?
- [ ] should an Insight card be created?
- [ ] should a Question card be created?
- [ ] should Method / Person cards be updated?
- [ ] should the new knowledge be attached to an existing MOC?

### Reflection and Confirmation Checklist
- [ ] was an `L1` reflection generated after the paper?
- [ ] do periodic tasks enter `L2` / `L3` reflection cycles?
- [ ] was a human confirmation request triggered?

---

## Dependency Skills

- `arxiv-watcher`: ArXiv paper search
- `academic-research-hub`: multi-source academic search
- `obsidian-direct`: Obsidian file operations
- `tavily`: web content extraction
- `pdf`: PDF text extraction
- `obsidian-cli`: Obsidian CLI utilities

---

## Error Handling

### Common Errors

1. **Paper cannot be retrieved**
   - Action: skip it and record the reason; do not create speculative notes

2. **Obsidian path does not exist**
   - Action: create the directory structure automatically

3. **Memory extraction fails**
   - Action: degrade to `L1` output and record the error log

4. **Knowledge conflict detected**
   - Action: mark it as `contradict` and resolve it during weekly consolidation

---

## Version History

- **v2.1** (2026-03-07): feasibility optimization (`L2` time 30 -> 45 minutes, optimized memory counts)
- **v2.0** (2026-03-07): added the long-term memory layer and consolidation mechanisms
- **v1.0** (2026-03-07): initial version defining the `L1` / `L2` / `L3` standard

---

## Related Documents

- [READING-STRATEGY-v2.1.md](protocols/READING-STRATEGY-v2.1.md) - full reading strategy
- [CHECKLIST-Paper-Reading.md](protocols/CHECKLIST-Paper-Reading.md) - startup checklist
- [Template-Reflection-L1.md](templates/Template-Reflection-L1.md) - single-paper reflection
- [Template-Reflection-L2.md](templates/Template-Reflection-L2.md) - weekly reflection
- [Template-Reflection-L3.md](templates/Template-Reflection-L3.md) - monthly reflection
- [Template-Confirmation-Request.md](templates/Template-Confirmation-Request.md) - human confirmation request
- [Procedure-Human-Confirmation.md](templates/Procedure-Human-Confirmation.md) - confirmation workflow

---

**Skill Author**: Scholar Agent  
**Last Updated**: 2026-03-18  
**License**: MIT
