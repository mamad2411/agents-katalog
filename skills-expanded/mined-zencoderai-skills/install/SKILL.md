---
name: install-skill
description: This skill should be used when the user asks to "install a skill", "import a skill", "add this skill", "try this skill from GitHub", or mentions installing, importing, or adding any AI coding skill/prompt from an external source. Gates external skill installs with a security assessment and installs across all supported CLIs.
metadata:
  version: 1.0.0
---

# Install Skill (Secure + Multi-CLI)

Gate every skill installation from an external/public source with a security assessment, then install across all supported CLIs via symlinks.

## CLI Skill Locations

| CLI | Skill Directory |
|-----|-----------------|
| Claude Code | `~/.claude/skills/` |
| Claude Desktop | `~/Library/Application Support/Claude/skills/` |
| Zen CLI | `~/.zencoder/skills/` |
| Codex CLI | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| Codex App | `~/Library/Application Support/Codex/skills/` |

## Trigger

Any user request that involves installing, importing, or adding a skill from an external source (GitHub, URL, shared file).

## Workflow

### 1. Identify the source

| Source | Example | Action |
|--------|---------|--------|
| GitHub repo | `github.com/org/skills` | Run the security gate |
| Shared URL | `https://gist.github.com/...` | Run the security gate |
| Local file the user wrote | `~/my-skill/SKILL.md` | Skip the gate — it's local |
| Previously approved | Already in the team's vetted list | Skip the gate |

For GitHub repos, extract `<owner>/<repo>`. If the skill is a single file (gist, URL), download it to a temp directory for scanning.

### 2. Security gate (external sources only)

Read and execute the full assessment defined in the `oss-security-check` skill (`../oss-security-check/SKILL.md`).

Pass it:
- `<url>` — the source repository or file URL
- `<owner>/<repo>` — extracted from the source (or "gist/<id>" for gists)
- `<host>` — github.com, etc.
- Context: "This is an AI skill. Run a thorough security assessment across all categories. Skills can contain both markdown instructions and executable code (.py, .js, .sh)."

Wait for the assessment to complete.

### 3. Skill-specific checks (in addition to the base assessment)

After the base `oss-security-check` completes, perform these additional checks specific to skills:

#### Executable code review

For every `.py`, `.js`, `.sh`, or other executable file in the skill directory:
- What does it do? Install helper vs. runs at invocation time?
- Does it access the network?
- Does it read files outside the skill directory (especially `~/.ssh/`, `~/.env`, `~/.aws/`)?
- Is any code obfuscated (base64, eval, exec)?
- Does it import external packages? If so, apply the supply chain checks below.

#### Supply chain verification (for skills with dependencies)

If the skill includes `package.json`, `requirements.txt`, `pyproject.toml`, or other dependency files:

**Lock file and pinning:**
- Verify a lock file exists and versions are pinned — not `*`, `latest`, `>=`, or unpinned ranges
- Run `npm audit` / `pip audit` and flag high-severity CVEs
- Check for `curl | bash` or `wget | sh` install patterns in scripts

**Package provenance (for dependencies from small/single-maintainer projects):**
- Verify the package owner matches the expected author
- Check publish history for anomalies (sudden activity after dormancy, unexpected version bumps)
- Flag any post-install scripts (`postinstall` in `package.json`, custom build commands in `setup.py`) that execute automatically during install

#### Staged delivery detection (ClickFix-style attacks)

This is the attack pattern used in the [OpenClaw malware campaign](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface): a skill's markdown directs users to install a "prerequisite" that is actually malware.

In the SKILL.md and any README/INSTALL files, check for:

- **External prerequisite instructions** — Does the skill tell the user or agent to install another tool, package, or binary from an external URL? Flag any `curl`, `wget`, `pip install`, `npm install`, `brew install` commands that point to URLs outside the skill's own repo.
- **Copy-paste shell commands** — Are there shell commands the user is told to run manually? Especially commands that download and execute external code.
- **Obfuscated payloads** — Base64-encoded strings, hex-encoded commands, or multi-stage decode-and-execute chains in any file (code or markdown).
- **macOS security bypass** — Commands like `xattr -d com.apple.quarantine`, `xattr -cr`, or `spctl --master-disable` that remove Gatekeeper protections. These are a strong signal of ClickFix-style malware delivery.
- **Binary downloads** — Instructions to download `.dmg`, `.pkg`, `.app`, or `.exe` files from external sources.

**Flag:** Any skill that requires installing external prerequisites from URLs outside its own repository. This is the primary delivery mechanism for skill-based malware.

#### Permission footprint

What does the skill instruct the agent to do?

- Read files? Which ones?
- Write files? Where?
- Run shell commands? What kind?
- Access external services? Which ones?
- Modify agent configuration?

### 4. Present combined results

```
## Skill Assessment: <name>

[Base assessment table from oss-security-check]

### Skill-Specific Findings

**Prompt injection:** [Automated scan result — always treat as unreliable, human review required]
**Staged delivery / ClickFix:** [None detected | Describes any external prerequisite installs, copy-paste commands, or binary downloads found]
**Scripts included:** [count] — [summary of what they do]
**Permission footprint:** [read-only | read-write | shell execution | network access]
**Agent behavior modifications:** [None | Describes any attempts to modify agent defaults]

### Recommendation
[Combined recommendation based on all findings]
```

### 5. User decision

Ask the user:
- **Install** — proceed with installation to skill directories
- **Install and review** — install but open the SKILL.md for the user to read first
- **Abort** — do not install

### 6. Execute the installation

**Prefer source code over registry packages.** Clone the repo, check out a specific tag, and install from the audited source:

```bash
# Good — clone, audit, pin to tag
git clone https://github.com/author/skill-repo.git ~/skills/skill-name
cd ~/skills/skill-name
git checkout v1.0.0
npm install  # or pip install -r requirements.txt — from audited source
```

If prompt injection was detected at any level, **always** recommend "Install and review" over direct install.

### 7. Install across all CLIs

Use the bundled install script to symlink the skill into every supported CLI at once:

```bash
# Install to all CLIs
./scripts/install-skill.sh skill-name

# Uninstall from all CLIs
./scripts/install-skill.sh skill-name --uninstall

# List installed skills
./scripts/install-skill.sh --list
```

The script creates symlinks from `~/skills/[skill-name]/` to each CLI's skill directory. One source of truth, available everywhere.

**Manual alternative** — if you prefer not to use the script:

```bash
SKILL="skill-name"
ln -sf ~/skills/$SKILL ~/.claude/skills/$SKILL
ln -sf ~/skills/$SKILL ~/.zencoder/skills/$SKILL
ln -sf ~/skills/$SKILL ~/.codex/skills/$SKILL
ln -sf ~/skills/$SKILL ~/.gemini/skills/$SKILL
```

### 8. Verify installation

Test that the skill is recognized in each CLI:
- Claude Code: ask the agent to use the skill
- Zen CLI: ask the agent to use the skill
- Codex CLI: ask the agent to use the skill
- Gemini CLI: ask the agent to use the skill

## Notes

- Skills have two attack vectors: the prompt vector (SKILL.md instructions) and the code vector (`.py`, `.js`, `.sh` files). Check both.
- Prefer source-code install at a pinned tag over registry packages to avoid supply chain attacks.
- Always recommend "Install and review" — human review of SKILL.md is the gold standard.
