---
name: changelog-output
pack: universal
description: 任意功能变更、bug修复、接口改动完成后，生成PR前必须在对应服务的变更记录文件追加条目——keep-a-changelog格式，落点见项目 AGENTS.md「目录结构」节。
when_to_use: 任何有用户可感知行为变化的改动完成后，生成PR草稿前。
when_NOT_to_use: 纯注释/文档格式修改，无用户可感知的行为变化。
---

# Skill: Changelog 产出

## 格式（Keep a Changelog）

```markdown
## [Unreleased]

### Added
- 新增 JWT refresh 端点，access_token 过期后自动续期 (#123)

### Changed
- 订单撮合优先级从价格优先改为时间优先

### Fixed
- 修复并发下单时的双重扣款问题 (#98)

### Breaking
- `GET /orders` 响应中 `price` 字段从 float 改为 string，影响所有调用方
```

## 规则

1. **追加到 `## [Unreleased]`** — 不写版本号，发版时统一替换
2. **按服务隔离** — 各服务独立的变更记录文件（落点见项目 AGENTS.md「目录结构」节；默认模板 `docs/changelogs/<service>/CHANGELOG.md`，或按项目约定为 `docs/services/<服务名>/CHANGELOG.md`），多服务变更分别写
3. **Breaking Changes 单独一节** — 任何影响对外接口或数据结构的改动必须在 `### Breaking` 里标出
4. **引用 PR/issue 编号** — `(#123)` 便于追溯，PR 提交前可用占位 `(#TBD)` 后补
5. **时态用过去式** — "修复" 而非 "修复中"；"新增" 而非 "新增了"

## 写什么

- 用户/调用方能感知到的变化（新功能、行为变更、接口变更、bug修复）
- **不写**：重构、代码格式、注释更新（内部实现变化，用户无感知）

## 反模式
- ❌ 改完代码不写 changelog（PR 被 harness hook 拦截）
- ❌ 把多服务变更全写到一个 changelog（应各写各的）
- ❌ Breaking change 混在 `### Changed` 里不单独标注
- ❌ `### Added: 优化了内部逻辑` — 用户无感知，不应出现在 changelog
