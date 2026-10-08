---
name: repository-resource-portal
description: Maintain this repository as a growing educational LLM knowledge base. Use when Codex needs to add, reorganize, or review homepage navigation, localized landing pages, directory-level catalogs, dataset and guide links, Codex Goal templates, or resource-portal documentation while preserving concise root navigation and relative links.
---

# Repository Resource Portal

Use this skill when changing repository navigation or knowledge-base catalogs.

## Maintenance Rules

- Keep the root README concise and navigational.
- Preserve four-language landing-page backups before major rewrites.
- Add new content to directory-level catalogs first.
- Use moderate, consistent emojis.
- Preserve relative links.
- Update English, Chinese, Korean, and Japanese landing pages when homepage navigation changes.
- Keep detailed tool documentation inside the relevant subproject.
- Avoid duplicating the full MTP pipeline explanation in the root README.
- Add new Codex Goal workflows and Skills in both `.agents/skills/` and `codex-goals/` when they are meant to be reusable.
- Run repository-relative link checks and privacy checks before any sync.

## Canonical Locations

- Root navigation: `README.md`
- Localized landing pages: `docs/README_zh.md`, `docs/README_ko.md`, `docs/README_ja.md`
- Goal catalog: `codex-goals/`
- Repository Skills: `.agents/skills/`
- MTP implementation: `qwen-mtp-gguf/`
- Training notebooks: `train_code/`
- Dataset folders: `High-fidelity Dataset/`
- PDF guides: `guidePDF/`
