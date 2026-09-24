---
name: skillspector
description: Security scanner for AI agent skills. Use BEFORE installing/running any Claude Code, Codex, or MCP skill from untrusted sources — detects prompt injection, data exfiltration, malicious patterns, and supply-chain risks.
---

# SkillSpector — scan skill sebelum dipasang

NVIDIA/SkillSpector adalah security scanner untuk skill AI agent. Pindai
SKILL.md / MCP / Codex skill sebelum dijalankan untuk deteksi:
- prompt injection
- data exfiltration
- malicious patterns
- supply-chain risks

## Kapan pakai

- Sebelum `git clone` / install skill dari repo tidak dikenal.
- Sebelum menjalankan skill hasil mining dari `skill-miner.py`.
- Audit berkala terhadap skill yang sudah terpasang di `~/.agents/skills/`.

## Cara pakai

```bash
# Scan satu skill
skillspector path/to/skill/SKILL.md

# Scan seluruh katalog lokal
skillspector --recursive ~/.agents/skills/

# Output JSON untuk CI/pipeline
skillspector --format json ~/.agents/skills-expanded/mined-*/
```

## Sumber
- Repo: https://github.com/NVIDIA/SkillSpector
- Lokal: `~/.agents/repo-refs/nvidia_skillspector/`
- Dokumen: `~/.agents/repo-refs/nvidia_skillspector/README.md`
