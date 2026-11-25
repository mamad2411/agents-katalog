---
name: cbm
description: 当需要架构概览/模块聚类/复杂度热点排行（codegraph 无架构视图）、commit 影响半径（diff 驱动，codegraph impact 只能符号驱动）、大型或陌生仓库整体理解、全仓符号/调用图查询时，用 codebase-memory-mcp 查询预索引知识图谱（CLI 全量，或 MCP 最小 4 工具 search_graph/query_graph/get_architecture/get_graph_schema）。小项目或单符号查询直接用 grep/codegraph。
---

# cbm（codebase-memory-mcp fork）— 架构级图谱查询（低频重型工具）

定位：**只做 codegraph 和 grep 做不了/不划算的事**。两种形态共享同一份预索引图谱：CLI（`codebase-memory-mcp`，17 工具全量，安装见下节）与 MCP 最小面（4 个只读工具，细则见「MCP 工具面细则」）。shell 可用的会话优先 CLI；受限客户端嵌 MCP 面。
实测依据（2026-09-05，websearch-mcpserver 三场对照实验）：

- **赢的场景**：架构概览（fan-in 热点/边界权重/分层/聚类，grep 需十几次调用）、全仓函数复杂度排行（cognitive 维度 LOC 给不出）、commit 级爆炸半径（唯一 diff 驱动形态）
- **输的场景**（别用 cbm）：单符号影响查询（codegraph impact 0.7s 全对）、单函数复杂度验真（`grep -c` 更快）、小仓库结构（`ls`+`wc -l` 两秒八成）

## 安装（一次性）

CLI 是单文件可执行程序，从 fork release 下载放进 PATH 即可：

- release 地址：https://github.com/daidaiJ/codebase-memory-mcp/releases
- Windows amd64：下载资产 `codebase-memory-mcp-windows-amd64.exe`，改名为 `codebase-memory-mcp.exe` 放入 PATH 目录（或 `gh release download --repo daidaiJ/codebase-memory-mcp`）
- 其他平台：fork release 目前仅构建 windows-amd64；可从源码构建（msys2 CLANG64 环境，`scripts/build.sh`），或改用上游版（可用，但下方配方依赖的 fork 行为差异见 fork README 的 fork-patch 章节）
- 验证：`codebase-memory-mcp --version`，`codebase-memory-mcp cli --help` 可见工具列表

## 前置

- 索引由 SessionStart hook 自动维护（fast 模式：跳过嵌入/相似度/githistory）；图谱只保证**会话开始时新鲜**，会话中途的变更不追同步
- project 名派生规则：路径分隔符 `/`→`-`，如 `C:\dev\web-app` → `C-dev-web-app`、`/home/me/work/web-app` → `-home-me-work-web-app`；拿不准跑 `codebase-memory-mcp cli list_projects`
- fork 默认值已反转，无需手动补偿：`auto_watch=false`（不自动注册 watcher）、日志默认 `error`、内存预算封顶 2048MB、UI 不自启；Windows 缓存目录 DACL 检查**默认跳过**（属主校验保留；多用户主机才需 `CBM_DACL_HARDENING=1` 开回）
- 缓存/配置根：默认 `~/.cache/codebase-memory-mcp`，可用 `CBM_CACHE_DIR` 重定向（如指到本地快速盘）；除它外没有别的 CBM 环境变量
- 每次调用冷启临时 daemon 约 5 秒——**把问题攒一批问，别一条一条聊**
- 原始 JSON 传参有 deprecation 警告（未来版本可能移除），届时 `codebase-memory-mcp cli <tool> --help` 查 flag 形式

## 命令配方（实测可用语法）

（以下 JSON 体与 MCP `tools/call` 的 arguments 同构，工具名即 CLI 子命令名；MCP 会话可直接换成对应工具调用。）

### 1. 架构概览（陌生/大型仓库第一站）

```bash
codebase-memory-mcp cli get_architecture '{"project":"<PROJECT名>","aspects":["hotspots","boundaries","layers","clusters"]}'
```

输出判读：`hotspots`（fan-in 排行=枢纽符号）、`boundaries`（跨模块调用权重）、`layers`（core/internal/entry 分层）、`clusters`（Leiden 聚类+cohesion）。overview 里的 node/edge 计数和 packages 清单是废物，跳过。

### 2. 复杂度热点排行（review 优先级）

```bash
codebase-memory-mcp cli query_graph '{"project":"<PROJECT名>","query":"MATCH (f:Function) WHERE f.complexity IS NOT NULL RETURN f.qualified_name, f.complexity, f.cognitive, f.loop_depth ORDER BY f.complexity DESC LIMIT 10"}'
```

可用属性：`complexity`（圈复杂度）、`cognitive`（认知复杂度）、`loop_depth`、`transitive_loop_depth`、`linear_scan_in_loop`（循环内线性扫描=隐藏 O(n²)）。排序选中后**用 Read 验真**再下结论。

### 3. commit 影响半径（唯一 diff 驱动形态）

```bash
PARENT=$(git rev-parse <commit>^)   # ⚠️ 不接受 ^ ~ 后缀，必须传完整 SHA
codebase-memory-mcp cli detect_changes "{\"project\":\"<PROJECT名>\",\"since\":\"$PARENT\",\"scope\":\"impact\"}"
```

⚠️ `direction`/`scope` 传非法值会显式报错（2026-09-30 起 fail-loud，不再静默空）。`changed_files` 里的非代码文件是噪声，`impacted` 按 hop 距离排序。

### 4. 信任前置闸门

```bash
codebase-memory-mcp cli check_index_coverage '{"project":"<PROJECT名>","scopes":["."]}'
```

大范围采信图谱结果前先跑：`parse_partial` 文件的图谱可能局部失明（cbm 索引自己源码时 81 个文件解析失败）。

## MCP 工具面细则（渐进披露）

MCP `tools/list` 的 description 有意只保留触发语与判读契约（瘦身记录见 docs/FORK_PATCHES.md §11）：参数语义在各自 inputSchema 里，本节承接 schema 表达不了的组合方式与诚实性边界。

| 工具 | 触发 | 机制与判读边界 |
|---|---|---|
| `search_graph` | 定位定义/调用方、按名称模式扫符号面 | `query`（BM25 关键词）与 `semantic_query`（嵌入相似）互斥；行带 qn/file/lines，degree 列只统计 CALLS/USAGE/CALL_REFERENCE/INHERITS/IMPLEMENTS 五族边 |
| `query_graph` | 多跳/聚合/复杂度排行/跨服务分析（配方见上节） | 总数是精确值或下界并带截断标记；**用 `next_cursor` 续读**（保持 query/project/graph 不变，format/max_rows 可变）；`graph=missed` 是覆盖盲区文件树，缺席≠完备；属性拼错会显式报错（2026-09-30 起目录校验），报错指引 `get_graph_schema` |
| `get_architecture` | 陌生/大型仓库第一站 | 省略 aspects = languages/packages/entry_points；`overview` = 除 file_tree 外的紧凑集；`cycles` 永远 opt-in；`path` 按目录前缀收窄 |
| `get_graph_schema` | 写 Cypher 前查节点/边目录（无 skill 客户端的属性发现通道） | 默认返回各 label/edge 计数；`diagnostics=full` 追加可查属性清单（约 5KB，随项目图谱规模变化）；query_graph 对未知属性**显式报错**（2026-09-30 起目录校验，CLI 与 MCP 同一条文案并指引本工具；取不到 schema 目录时 fail-open）——引擎内部仍把未知属性当空值求值，校验层负责拦住那个误导性的 total: 0 |

MCP 最小面没有 trace_path / index_status / detect_changes：一跳调用链直接用 query_graph 的 Cypher（`MATCH (c:Function)-[:CALLS]->(f:Function …)`）；Cypher 可用属性直接用上节配方 2 的属性表或 `get_graph_schema`；索引新鲜度与影响半径走 CLI（或 `--tool-profile=all`）。MCP 最小面也不会自动建索引（auto-index 仅 ALL profile 生效），受限客户端场景先用 CLI 建索引。

## 硬规则

1. **空结果 ≠ 真阴性**：依次排查 ① 参数非法（direction/项目名/SHA 格式）→ ② coverage 盲区 → ③ grep 复核，三关过了才准信"没有调用方/没有影响"。
2. 图谱与代码文件冲突时，以代码文件为准，会话开头重跑 hook 或 `codebase-memory-mcp cli index_repository --repo-path . --mode fast`。
3. 变异管理类（index_repository / delete_project / manage_adr / ingest_traces）同样走 CLI，非必要不碰。
4. 若要恢复 MCP 形态（受限客户端嵌入场景）：fork 的 MCP 默认只暴露 **4 个工具**（search_graph / query_graph / get_architecture / get_graph_schema；fork issue #5 将 detect_changes 换出，待可信度修复；get_graph_schema 为 2026-09-30 增补的无 skill 客户端属性发现通道），`--tool-profile=all` 恢复全量，`--tool-profile=minimal|analysis|scout` 可选；全局 `tools_disabled` 名单与项目本地 `.cbm/config.json` 可细粒度禁用（双侧生效、fail-loud）。配置键见 `codebase-memory-mcp config list`。
