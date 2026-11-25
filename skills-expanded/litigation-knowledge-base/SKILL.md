---
name: litigation-knowledge-base
version: "1.0.0"
description: 诉讼知识管理中枢——统一管理 A 区（部门法知识库·公域检索）、B 区（办案笔记·私域沉淀与检索）、C 区（工作笔记·私域沉淀与检索）。主路径通过 `KB.*` 能力槽调用（`KB.retrieve` / `KB.rag` / `KB.upload`），支持 qmind、飞书知识库、钉钉知识库、语雀、Obsidian Vault + Grep、ima 知识库六种后端，可按三区分开绑定实现混用；降级路径为本地 Read/Grep。本技能提供知识库注册入口，检索路由由用户注册知识库时自行配置。触发词：知识库、沉淀、知识沉淀、知识图谱、经验库、类案库、问知识库、办案笔记、工作笔记。
---

# 诉讼知识库（litigation-knowledge-base）· 知识管理中枢

> 三区架构统一管理：A 区（部门法知识库·公域）供检索、B 区（办案笔记·私域）供沉淀与检索、C 区（工作笔记·私域）供沉淀与检索。
> 主路径：通过 `KB.*` 能力槽调用后端知识库（语义检索 `KB.retrieve` / RAG 问答 `KB.rag` / 沉淀 `KB.upload`），后端由用户在 `profile.md` 中绑定。
> 降级路径：本地目录 Read/Grep。
> **只读不改原始文档，绝不臆造 ID。**

---

## 0 | 前置

1. 读 `profile.md`「知识库注册表」获取：
   - 已绑定的 `KB.*` 后端（qmind / 飞书 / 钉钉 / 语雀 / 本地 Vault 等）与鉴权环境变量
   - 各区 notebook / space / repo 标识（由用户自行注册，本 skill 不硬编码）
   - 降级路径（如 `~/.knowledge-base/<region>/<domain>/`）
2. **意图判定**：
   - **A 区检索**：查部门法知识库中的条文解读/裁判规则/学术文献 → §1
   - **B/C 区沉淀**：把产出归入办案笔记或工作笔记 → §2
   - **B/C 区检索**：搜索历史沉淀的办案经验 → §3

---

## 1 | A 区（部门法知识库）

### 1.1 注册表（配置入口，由用户在 profile.md 中维护）

用户将已有的本地或云端知识库按部门法注册进专家套件。注册表结构示例：

```yaml
kb_registry:
  a_region:
    - domain: civil-code                    # 域名标识（本 skill 内引用）
      title: 民法典                        # 通用法律领域名，不指向特定出版物
      notebook_id: <用户填>                  # KB 后端中的库 ID
      fallback_path: <用户填>                # 本地降级路径（可空）
    - domain: civil-procedure
      title: 民事诉讼法
      notebook_id: <用户填>
      fallback_path: <用户填>
    - domain: contract-law
      title: 合同法
      notebook_id: <用户填>
      fallback_path: <用户填>
    - domain: company-law
      title: 公司法
      notebook_id: <用户填>
      fallback_path: <用户填>
    # ... 按需增删（如刑法、行政法、知识产权法、劳动法、个人信息保护等）
    # 域名标题使用部门法名称，用户注册时可搭配自己的知识库资料（学术专著、案例解读、条文解读等）
```

### 1.2 检索与降级

检索通过 `KB.retrieve(domain=<域名>, query="...", top_k=5)` 和 `KB.rag(domain=<域名>, query="...")` 调用。案由→域名的路由策略由用户在注册知识库时自行配置，本技能不预设。

`KB.*` 调用失败时降级到本地 `fallback_path` 目录的 Read/Grep，输出标注 `[KB:降级-本地]`。

---

## 2 | B/C 区沉淀（办案笔记 + 工作笔记）

### 2.1 区标识（由用户在 profile.md 中注册）

| 区 | 域名标识 | profile.md 字段 | 用途 |
|----|---------|--------------|------|
| B | case-notes | `kb_registry.b_region.case_notes` | 个案办案手记 |
| C | work-notes | `kb_registry.c_region.work_notes` | 日常研究/新法解读/方法论 |

### 2.2 B 区目录（按案件类型，默认模板；用户可在 profile.md 中覆写）

| 一级目录 | 沉淀内容 |
|---------|---------|
| 合同纠纷 | 合同攻防策略、结算规则、复盘 |
| 侵权纠纷 | 侵权认定、损害计算、复盘 |
| 建设工程 | 工程结算、实际施工人、优先受偿、鉴定 |
| 公司纠纷 | 股东权利、决议效力、人格否认 |
| 知产纠纷 | 商标/著作权/专利/商业秘密 |
| 数据合规 | 个人信息、数据出境、竞争 |
| 主诉催收 | 催收策略、不当得利、财产保全 |
| 其他 | 其他被诉/主诉类型经验 |

### 2.3 C 区目录（按主题，默认模板）

法律研究 / 新法解读 / 法院观察 / 方法论 / AI 与法律

### 2.4 沉淀触发路由表

| 套件技能产出 | 目标区 | 目标目录 | 触发方式 |
|-------------|--------|---------|---------|
| /案件复盘 | B 区 | 按案件类型路由 | 复盘完成后自动推荐 |
| /要件攻防分析 | B 区 | 按案件类型路由 | 分析完成后自动推荐 |
| /法律研究 | C 区 | 法律研究 | 报告完成后自动推荐 |
| /新法解读 | C 区 | 新法解读 | 解读完成后自动推荐 |
| /庭审提纲 执行后（法官观察） | C 区 | 法院观察 | 用户主动沉淀 |
| 代理词完成后（攻防策略） | B 区 | 按案件类型路由 | 用户主动沉淀 |

### 2.5 沉淀能力槽调用

```
KB.upload(domain=<域名>, file=<知识卡片.md>)
```

> `domain` 对应知识库注册表中的域名（如 `case-notes`、`work-notes`、`civil-code` 等），由本技能自动映射到对应的区和后端。

**沉淀格式规范**：

```markdown
---
title: {成果标题}
date: {YYYY-MM-DD}
source_skill: {产出技能名}
case_ref: {关联案件简称，如有}
tags: [关键词1, 关键词2, ...]
---

{成果正文或核心摘要，≤500 字}
```

降级：写入本地 `~/.knowledge-base/{B或C}/{目录}/` 以 md 文件保存。

---

## 3 | B/C 区检索

```
KB.retrieve(region=b, query="<检索问题>", top_k=5)
KB.retrieve(region=c, query="<检索问题>", top_k=5)
```

---

## 4 | 执行规则

1. **能力槽优先**：所有检索/沉淀操作首先通过 `KB.*` 能力槽调用后端。
2. **不臆造 ID**：notebook / source / dir 标识全部来自实际返回或 `profile.md` 注册表，禁止编造。
3. **降级透明**：降级到本地 Read/Grep 时必须标注 `[KB:降级-本地]`，让用户知晓。
4. **只读不改**：检索时不修改已有 source 内容。
5. **鉴权安全**：KB 后端所需的 token/密钥仅从环境变量传入，不落盘、不 echo。
6. **保密分级**：B 区内容为私域，不跨案件泄露；开源分发时不含实际 notebook ID。
7. **知识复用**：新案件启动时，先检索 B 区同类案件历史策略。
8. **触发条件**：仅在套件子技能内部触发，或用户直接 @诉讼知识库 时触发。非套件相关的通用工作不自动触发知识沉淀。

---

## 5 | KB.* 能力槽推荐后端

| 后端 | 覆盖能力 | 配置方式 | 说明 |
|------|---------|---------|------|
| qmind CLI | retrieve / rag / upload | PAT 环境变量 | 语义检索，亚秒级响应 |
| 飞书知识库 | retrieve / upload | lark-cli 或飞书 Open API | 团队在线协同 |
| 钉钉知识库 | retrieve / upload | dws 调用 | 团队在线协同 |
| 语雀 | retrieve / upload | Yuque OpenAPI | 文档知识库 |
| **Obsidian Vault + Grep** | **retrieve / upload** | **指定 Vault 路径** | **本地零依赖，Markdown 原生** |
| **ima 知识库** | **retrieve / rag** | **ima-mcp 连接器** | **腾讯 ima，语义检索 + RAG** |
| 自建 RAG 服务 | retrieve / rag / upload | HTTP MCP 桥接 | 完全自主可控 |

### 5.1 Obsidian 配置路径

```
profile.md 配置：
  kb_backend:
    backend: obsidian
    vault_path: "~/Documents/Obsidian/MyVault/"
    a_region_dir: "A-部门法知识库/"
    b_region_dir: "B-办案笔记/"
    c_region_dir: "C-工作笔记/"

检索方式：
  - 主路径：rg/rg --glob '*.md' <关键词> <Vault路径>/<区域目录>/
  - 降级路径：grep -rn <关键词> <Vault路径>/<区域目录>/
  - 输出标注：[KB:Obsidian-本地]

沉淀方式：
  - 直接写入 Markdown 文件到对应区域目录
  - 文件命名：YYYY-MM-DD_<标题>.md
```

### 5.2 ima 配置路径

```
profile.md 配置：
  kb_backend:
    backend: ima
    a_region_space_id: "<ima 部门法知识库空间 ID>"
    b_region_space_id: "<ima 办案笔记空间 ID>"
    c_region_space_id: "<ima 工作笔记空间 ID>"

前置条件：
  - 已安装 ima-mcp 连接器并完成授权
  - 在 ima 中已创建对应知识库空间

检索方式：
  - 通过 ima-mcp 连接器的语义检索能力
  - KB.retrieve → ima-mcp 后端
  - 输出标注：[KB:ima]
```

### 5.3 混用方案

用户可在 profile.md 中按区域分别绑定不同后端：

```yaml
kb_backend:
  a_region: ima              # A区（部门法知识库）用 ima 语义检索
  b_region: obsidian         # B区（办案笔记）本地 Obsidian
  c_region: feishu           # C区（工作笔记）飞书协同
```

套件各子技能按区域自动路由到对应后端，用户无需手动切换。

---

## 6 | 本技能不做什么

- 不硬编码任何具体 notebook / space / repo ID
- 不预设某一家云端服务为唯一后端
- 不替用户决定 A 区书目、B 区目录、C 区主题
- 不预设案由→知识库的检索路由（由用户注册知识库时自行配置）
- 不在检索为空时臆造条目
