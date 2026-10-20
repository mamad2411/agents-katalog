---
name: expert-team-converter
metadata:
  short-description: 外部专家包转项目专家团格式工具
description: "把外部专家包转换为当前仓库的专家团 Skill 包。适用于导入 WorkBuddy、CodeBuddy、插件、提示词或文件夹形式的专家团，并需要判断子项是真实顶层 skill、混合映射，还是 router 内部能力标签，同时同步更新 registry/catalog 索引。"
---

# 外部专家团转换成Codex专家团 / External Expert-Team to Codex Expert-Team Converter

## Overview

使用这个 skill 将外部专家包转换为当前仓库的专家团格式。转换结果必须是普通 Codex Skill 包和对应目录索引记录。子项可以使用仓库接受的三种专家团模式：全部是真实顶层 skill、真实 skill 与内部标签混合，或仅作为 router 内部能力标签。

这个包本身是普通工具型 skill，不是专家团入口。`expert-team-converter` 只注册到 `indexes/skill-registry.md` / `indexes/skill-registry.json`，不要写入 `indexes/expert-team-file-list.md`。它不是运行时人格、插件安装器、市场发布器，也不能提取隐藏 prompt。

## Triggers

- "把这个专家包转成当前项目里的专家团格式，并判断子技能是真实 skill 还是内部能力标签。"
- "Use this CodeBuddy/WorkBuddy/plugin expert package and generate repository skills plus indexes."
- "把 design-engine 这种专家包按 harmony-expert-team 的表格格式整理进项目，并保留它的 router 内部能力标签。"
- "检查项目里是否已有相同能力，有就引用已有 skill；没有就判断是新建顶层子 skill 还是保留为内部标签。"

## Required Reading

When converting a package, read [references/guide.md](references/guide.md) first. Use [references/target-structure.md](references/target-structure.md) for exact output paths, naming, index updates, and validation gates.

## Inputs

- Source expert package path, archive, copied folder, screenshot, card metadata, or prompt text.
- Target repository root, usually the current `tiny-agents` repository.
- Desired expert-team name, category, display name, or routing style if the source does not state them.
- User authorization for optional side effects such as commit, push, installation, deletion, or overwriting existing packages.

## Outputs

- One expert-team entry package under `skills/<team-name>/`.
- Optional top-level child skill packages under `skills/<child-skill-name>/` only when the source child is reusable as a standalone capability or the user explicitly requests it.
- References to existing top-level skills when the repository already contains the same capability.
- A child-entry mode classification: `all-top-level-skills`, `hybrid`, or `internal-router-labels`.
- Updated `indexes/skill-registry.md`, `indexes/skill-registry.json`, and `indexes/expert-team-file-list.md`.
- Validation evidence and a handoff summary listing created packages, reused packages, internal labels, unresolved mappings, assumptions, and remaining risks.

## Workflow

1. Inspect the repository state with `git status --short --branch -uall` before editing. Preserve unrelated user changes.
2. Inventory the source package. Prefer structured files such as `plugin.json`, `README.md`, `settings.json`, `agents/*.md`, and nested `skills/*/SKILL.md`. Ignore avatars, install caches, runtime state, and local absolute paths.
3. Resolve each child entry against `indexes/skill-registry.md` and `indexes/skill-registry.json` first, then against top-level `skills/*/SKILL.md`. Reuse an existing skill when name, purpose, inputs, and outputs materially match.
4. Classify the team mode. Use `all-top-level-skills` when every child entry resolves to a real top-level skill, `hybrid` when only some entries resolve, and `internal-router-labels` when the entries are only local phases, roles, or ability labels.
5. Create missing child skills as real top-level packages only when the source child has enough standalone workflow to be safely callable outside the team or when the user asks for that. Otherwise preserve it as an internal router label.
6. Create or update the expert-team router package. Its `Expert Roles` section must clearly distinguish real top-level skills from internal capability labels when the team is hybrid or internal-only.
7. Update indexes. Run `python3 scripts/generate_skill_registry.py` for the registry, then manually add or update the matching row in `indexes/expert-team-file-list.md` with the category, team link, display name, and child skill or capability-label names.
8. Validate the new and changed packages. Run structural validation, YAML/JSON parsing, `git diff --check`, and the repository tests when conversion logic or scripts changed.
9. Report created files, reused skills, internal labels, unresolved matches, validation commands, and remaining risks.

## Child Entry Modes

The catalog row and router package can use three accepted shapes:

- `all-top-level-skills`: every child entry is a real top-level skill. Example: `harmony-expert-team` coordinates `harmony-os-ask`, `harmony-os-act`, `generate-ui-code`, and `service-widget`.
- `hybrid`: some child entries are real top-level skills and some are team-local capability labels. Use this when existing skills cover part of the workflow but the source package also has local phases or role labels that should not become standalone skills.
- `internal-router-labels`: every child entry is a local role, phase, or capability label inside the router. Use this for many WorkBuddy/CodeBuddy expert cards and folder packages where child agents are not reusable standalone skills.

Use real top-level skills only when they exist or are intentionally created. Use internal labels when they are team-specific routing names. Do not imply that an internal label can be invoked as `$label`.

If a child capability is ambiguous, keep it as an internal label with a clear description or ask the user before mapping it to an unrelated existing skill. Do not silently map unrelated skills just to make a team look fully top-level.

## Guardrails

- Do not commit local absolute paths, tokens, credentials, runtime caches, generated local reports, avatars, or plugin install metadata.
- Do not claim access to hidden expert prompts. Use only visible package files and mark missing details as assumptions.
- Do not overwrite an existing package unless the user explicitly asks for an upgrade and the diff is scoped.
- Do not install, commit, push, delete, or publish without explicit user authorization.
- Prefer updating or reusing existing skills over creating duplicates when capability overlap is clear.
- Do not add this converter skill itself to `indexes/expert-team-file-list.md`; only converted expert-team packages belong there.

## Validation

At minimum, run:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/<team-name>
# Only when new top-level child skills were created:
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/<new-child-skill-name>
python3 scripts/generate_skill_registry.py
python3 - <<'PY'
import json, yaml
from pathlib import Path
json.loads(Path("indexes/skill-registry.json").read_text())
yaml.safe_load(Path("skills/<team-name>/agents/openai.yaml").read_text())
print("json/yaml ok")
PY
git diff --check
```

Also run `python3 -m unittest` when repository import logic, scripts, or generated deterministic helpers changed.
