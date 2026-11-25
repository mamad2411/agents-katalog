---
name: vibe-file-list
description: Use this skill to generate or check the framework file list.
---

# VIBE 框架文件清单

> 路径约定说明：所有 VIBE 框架管理的文档统一存放在项目根目录下的 `.vibe/` 目录中，便于与 Claude Code 的 `.claude/` 目录区分。

## 1. 状态与启动文件 (`.vibe/`)
- `.vibe/stage.md` - 当前项目开发阶段文件（由 vibe-stage-update 维护）
- `.vibe/startup.md` - 项目启动工作流文件
- `.vibe/tasks.md` - 任务清单（autopilot 引擎的"状态机"，由 vibe-plan 初始化）

## 2. 工作流程文档 (`.vibe/workflows/`)
所有工作流定义文档统一存放在此目录。

### 2.1 需求与设计类
- `analyze-req.md` - 项目需求分析流程
- `architecture.md` - 架构设计流程
- `database.md` - 数据库设计流程
- `api-rules.md` - API 规则文档设计流程

### 2.2 计划与检查类
- `plan.md` - 项目阶段开发计划流程
- `review.md` - 代码检查流程
- `integrate.md` - 前后端代码对接流程
- `meta.md` - AI 工作流制作流程（用于自举新工作流）

### 2.3 开发执行类
- `frontend.md` - 前端开发流程
- `backend.md` - 后端开发流程
- `stage-update.md` - 阶段更新流程
- `test.md` - 测试与质量门禁流程
- `security.md` - 安全审查流程
- `ui-design.md` - UI 设计系统流程
- `ui-beautify.md` - UI 美化与动效流程

## 3. 项目文档 (`.vibe/docs/`)

### 3.1 需求文档 (`docs/requirements/`)
- `prd.md` - 产品需求文档（Product Requirements Document）

### 3.2 技术文档 (`docs/technical/`)
- `architecture.md` - 系统架构设计文档
- `api-rules.md` - API 设计规则文档
- `api-spec.md` - API 设计规范文档

### 3.3 开发计划 (`docs/plan/`)
- `overview.md` - 项目阶段开发计划总览
- `frontend.md` - 前端开发计划
- `backend.md` - 后端开发计划
- `review-report.md` - 代码检查问题报告

### 3.4 报告 (`docs/reports/`)
- `test/` - 测试报告
- `security/` - 安全审查报告
- `design/` - 设计系统文档
- `motion/` - 动效清单

## 4. API 相关文件
- `API表.md` - API 端点清单（项目根）
- `API规范表.md` - API 设计规范表（项目根）

## 5. 开发手册
- `frontend/doc/README.md` - 前端开发指南
- `backend/doc/README.md` - 后端开发指南

## 6. 项目架构文档
- `.vibe/docs/technical/architecture.md` - 项目整体架构设计文档

## 7. 其他文件
- `README.md` - 项目说明文件（项目根）
- `LICENSE` - 许可证文件（项目根）
- `package.json` / `requirements.txt` / `go.mod` 等依赖文件

## 路径迁移说明

本文件由旧版 `doc/workflaw/`、`doc/workfile/`、`doc/wroktwo/`、`doc/项目文档/` 体系迁移到 `.vibe/` 统一目录。迁移映射：

| 旧路径 | 新路径 |
|--------|--------|
| `.trae/rules/kaifa.md` | `.vibe/stage.md` |
| `.trae/rules/kaifa1.md` | `.vibe/startup.md` |
| `doc/workflaw/*` | `.vibe/workflows/*` |
| `doc/workfile/*` | `.vibe/workflows/*` |
| `doc/wroktwo/*` | `.vibe/workflows/*` |
| `doc/项目文档/需求文档/` | `.vibe/docs/requirements/` |
| `doc/项目文档/技术文档/` | `.vibe/docs/technical/` |
| `doc/项目文档/开发计划/` | `.vibe/docs/plan/` |
