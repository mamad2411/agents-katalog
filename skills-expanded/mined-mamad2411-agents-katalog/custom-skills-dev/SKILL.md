---
name: custom-skills-dev
description: |
  Guide development of the ai-dev framework and its first-party skill collection.
  Use when modifying ai-dev CLI code, npx skill integration, copy/distribution logic,
  commands, agents, plugins, first-party skills, tests, or release documentation.
  Triggers: "develop custom-skills", "modify ai-dev", "add skill", "update distribution",
  "release version", "開發 custom-skills", "修改 ai-dev", "新增 skill", "發布版本".
---

# custom-skills-dev

ai-dev 的 framework 與第一方 skills 分成兩個公開 repositories。開始前先確認目標，不要把內容改到錯的 repository。

## Repository ownership

| Repository | 負責內容 |
| --- | --- |
| `ValorVie/custom-skills` | ai-dev CLI、commands、agents、plugins、project-template、OpenSpec、upstream 設定與 `upstream/npx-skills.yaml` |
| `ValorVie/ai-dev-skills` | `npx skills` 可安裝的第一方 `skills/<canonical-id>/`、skill 直接測試及 collection validator |

第一方 skill 內容不得複製回 framework repository。ai-dev baseline 是否採用某個 skill，由 framework 的 `upstream/npx-skills.yaml` 明確決定。

## Runtime flow

```text
ai-dev install
  tools → repos → npx-skills → targets

ai-dev update
  tools → repos → npx-skills
```

- `npx-skills` 安裝或更新第一方與第三方 global skills。
- `targets` 只分發仍由 framework 管理的 commands、agents、workflows、plugins，以及明確保留 clone ownership 的來源。
- ECC 白名單 skills 與 custom repo skills 仍可由 clone 管理；不得與 npx-managed canonical ID 同名。

完整 ownership 與路徑見 [copy-architecture.md](references/copy-architecture.md)。

## 修改 ai-dev framework

1. 在 `ValorVie/custom-skills` checkout 確認現有 dirty files 與 active OpenSpec change。
2. 修改 `script/`、`commands/`、`agents/`、`plugins/`、`project-template/` 或 `upstream/` 中的必要檔案。
3. 為使用者可見行為更新 OpenSpec delta、測試與正式文件。
4. 使用目前 checkout 執行測試，不使用可能過時的已安裝 `ai-dev`。
5. framework release 只提交 framework 範圍，不夾帶另一個 repository 的 skill content。

新增 CLI command 的細節見 [cli-development.md](references/cli-development.md)。

## 新增或修改第一方 skill

1. 在 `ValorVie/ai-dev-skills` 的 `skills/<canonical-id>/` 修改內容。
2. 目錄名必須與 `SKILL.md` frontmatter `name` 相同。
3. 主要流程需要的 scripts、references、assets、templates、evals 與直接測試必須留在 skill root 內。
4. 執行 repository validator、skill 直接測試及 npx discovery：

```bash
python tests/validate_skills.py
DISABLE_TELEMETRY=1 npx --yes skills@1.5.22 add . --list
```

5. 新 skill 只有在 ai-dev 維護者更新 `upstream/npx-skills.yaml` 後，才會進入 baseline。不得用 wildcard 自動採用。

## 修改 npx baseline

在 `ValorVie/custom-skills`：

1. 先用 `npx skills add <repo> --list` 確認來源與 canonical IDs。
2. 檢查同名來源、agent paths 與現有 local modifications。
3. 在 `upstream/npx-skills.yaml` 明確加入 repository 與 skill names。
4. 更新 npx manifest、install/update、list、toggle 與 migration 測試。
5. dry-run 不得執行 npx、寫 lock 或清理 ownership。

## 發布

兩個 repositories 分開發布、分開驗證、分開 commit。`ai-dev-skills` 應先有可讀取的 known-good revision，ai-dev 才能引用它。

任何 repository creation、release、tag 或 push 都要遵循當前專案授權；一般文件或程式修改不自動授權 remote mutation。

framework release 細節見 [release-workflow.md](references/release-workflow.md)。

## Language

- 人類文件使用繁體中文，技術識別字保留原文。
- Commit message 使用 Conventional Commits 與繁體中文摘要。
- 公開內容不得包含內部品牌、repository、host、帳號、credential 位置、private path 或組織專用流程。
