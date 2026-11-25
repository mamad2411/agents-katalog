---
name: jobos
version: 0.2.0
description: AI求职操作系统 - 岗位采集/简历定制/面试准备/投递指南一条龙
author: bcefghj
triggers:
  - jobos
  - 找工作
  - 求职
  - 简历
  - 面试准备
  - 投递
  - job search
  - resume
  - interview prep
tools:
  - jobos_search
  - jobos_analyze
  - jobos_resume
  - jobos_interview
  - jobos_pipeline
---

# JobOS - AI 求职操作系统

基于 MiniMax M2.7 的一站式 AI 求职助手，覆盖「岗位采集 → 简历定制(LaTeX PDF) → 面试资料生成 → 投递指南」全链路。

## 功能

### `/jobos-search` — 岗位搜索
搜索 AI/Agent/大模型 相关的实习和工作岗位。
- 支持 Boss直聘、牛客网、猎聘等中国主流平台
- 支持按地区、关键词、岗位类型筛选
- 自动去重和结构化存储

**示例**: "帮我搜索武汉的AI Agent暑期实习"

### `/jobos-analyze` — 岗位分析
对单个岗位进行深度分析和10维评分。
- JD 关键词和技能要求提取
- 10维评分系统（角色匹配/技能对齐为门槛）
- 公司画像生成（薪资/评价/加班情况）

**示例**: "分析一下华为武汉的AI实习岗位"

### `/jobos-resume` — 简历定制
根据目标岗位 JD 生成高度定制化的 LaTeX PDF 简历。
- YAML 个人数据 + AI 定制 + LaTeX 渲染
- STAR 法则润色项目经历
- ATS 关键词注入和评分
- Boss直聘打招呼语生成

**示例**: "针对华为AI实习，帮我生成一份简历"

### `/jobos-interview` — 面试准备
生成从零到面试的完整资料包。
- 技能树提取（必需/加分/基础）
- N周学习路径（从零到面试通关）
- 八股文速查手册（针对岗位技能点）
- 模拟面试真题（字节/阿里风格，不接受模糊回答）

**示例**: "帮我准备华为AI实习的面试资料"

### `/jobos-pipeline` — 一键全流程
输入关键词和地区，自动完成全部流程。
- 采集岗位 → 10维评分 → 筛选Top-N → 逐个生成简历+面试资料
- 支持批量模式（夜间自动运行）

**示例**: "帮我完整跑一遍武汉AI Agent实习的求职流程"

## 配置

在 `config.yaml` 中设置:
- MiniMax API Key
- 默认搜索地点和关键词
- 评分权重
- 输出目录

## 数据格式

个人信息使用 YAML 格式存储（Resume as Code 理念），维护一份数据源，AI 生成 N 份定制简历。

## 技术栈

- LLM: MiniMax M2.7 (OpenAI SDK 兼容)
- 简历: YAML + Jinja2 + XeLaTeX
- 爬虫: Playwright + 牛客 API
- 存储: SQLite
