---
name: sync-docs-and-code
description: Use when modifying code OR as a standalone maintenance task to scan the entire repository for outdated documentation, obsolete code, lingering temporary files, and useless assets, then sync or delete them
---

# Sync Docs and Code (代码、文档与过时内容同步清理)

## Overview

**Core principle:** Documentation, code, and repository assets must remain clean, accurate, and aligned. A codebase with stale documentation, lingering obsolete code, or unnecessary dead files creates technical debt and misleads both developers and AI agents.

**Violating this process leaves silent discrepancies, orphaned artifacts, and parallel dead code paths.**

Per `CLAUDE.md`:
> “文档与代码同步：当代码修改与仓库现有文档相左（即文档落后于代码）时，必须顺带同步更新相应文档，保持文档与代码一致。”
> “Remove or account for obsolete code; do not leave parallel paths by default.” (Golden Principle #6)
> “Search for and extend existing code before adding helpers, managers, parsers or targets.”

---

## When to Use

**Run this skill in either scenario:**
1. **修改代码后（Post-modification）**：功能开发、Bug 修复、重构后，确保文档与新增/变更逻辑完全同步。
2. **日常无代码修改时（Standalone maintenance）**：独立巡检整个仓库，查找并清理陈旧文档、已废弃接口、僵尸代码及无用文件。

---

## The Four-Step Process

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 1. 范围与实体提取 │ ──→ │ 2. 文档漂移扫描   │ ──→ │ 3. 过时/无用内容 │ ──→ │ 4. 修正删除与验证│
│ Git 状态或全量盘点│     │ 全局 Grep 比对   │     │ 孤儿代码/僵尸文件│     │ 批量清理+跑单测  │
└──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Step 1: 确定检查范围与关键实体 (Scope & Entity Extraction)

根据使用场景确定基准：
- **有代码改动**：分析 `git diff` 提炼当前变更触及的接口、宏、常量、类、探针与构建项。
- **无代码改动（全量审计）**：盘点仓库中的所有 `.hpp/.h` 导出头文件、`server/src/*.cpp` 实现、`*.bpf.c` 探针、CMake 目标及所有 `docs/` Markdown 文件。

**重点盘点实体：**
1. **接口与签名**：C API（`weaknet_client.h`）、D-Bus 接口（`dbus_service.cpp` / XML）、CLI 命令参数
2. **架构指标与数量**：监控器个数（`MonitorManager`）、后台线程数（`ServerContext`）、eBPF 探针清单（`*.bpf.c`）
3. **配置项与常量**：`weaknet_config.hpp` 中的白名单配置、默认采样间隔、默认端口/路径
4. **存储与持久化**：SQLite 表结构、数据库文件路径（`history.db`）
5. **构建与依赖**：CMakeLists 编译选项、产物路径（如 `build-x86/`、`build-arm64/`）
6. **废弃旧方法**：被标记或替换掉的旧函数、旧常量

---

### Step 2: 全仓库检索过时文档 (Scan Stale Documentation)

对项目全部文档进行全局正则扫描，找出陈旧数值、失效描述与失效指令：

```bash
# 核心文档清单扫描
# 1. 架构与顶层说明：README.md, docs/架构设计.md, docs/项目评估.md, docs/学习路线图.md
# 2. 客户端与集成说明：client/README_CLIENT.md, client/README_LIBRARY.md, docs/weaknet_cli_usage.md
# 3. 部署与环境说明：docs/交叉编译与开发板部署.md, docs/ci-测试使用指南.md
# 4. 技能与规范文档：CLAUDE.md, docs/skills-and-openspec-guide.md, skills/
```

**检索比对项清单：**
- [ ] **eBPF 程序清单**：统计当前实际 `.bpf.c` 数量（`find server/src -name "*.bpf.c"`），核对文档中的表格与总数是否缺漏。
- [ ] **监控线程与插件清单**：核对文档中记录的监控器矩阵是否与 `server.cpp` / `monitor_registry.cpp` 实际启动项一致。
- [ ] **构建与测试指令**：检查所有 Markdown 中出现的编译测试命令是否包含旧路径（如陈旧的 `build/` 而不是 `build-x86/`），是否缺少新增的单测过滤项。
- [ ] **D-Bus 方法与信号**：核对文档中描述的 D-Bus 接口是否包含最新扩展（如 `GetHistory`、`SetMonitorParam` 等）。
- [ ] **配置键名与类型**：核对文档中给出的 `weaknet-cli set/get` 示例参数是否与代码中的白名单匹配。
- [ ] **路径硬编码**：检查文档中是否存在违规过时的 `/tmp/weaknet/` 路径（应为持久化路径）。

---

### Step 3: 全仓库排查过时代码、孤儿接口与无用文件 (Scan Obsolete Code & Dead Assets)

检查仓库内是否存在无用或多余的内容：

1. **过时/冗余文件识别（识别后直接删除或归档）**：
   - 检查临时排查脚本、实验性 probe、重复保留但已无调用的 mock 源码；
   - 检查是否有遗留在源码树下的临时文件（`*.tmp`, `*.bak`, `*.orig`, `*.log`, `~*`）；
   - 检查构建遗留物是否误入版本控制（`build/`, `bin/`, `*.o`, `*.so` 等）；
   - 检查已归档或被彻底废弃的旧设计草案是否有必要保留或打上 `[DEPRECATED]` 标记。
2. **废弃函数与平行代码（修改或删除）**：
   - 搜索已被新接口替换的旧函数（如已迁移至 `MonitorManager` 却仍残留的旧单例启动逻辑）；
   - 坚决杜绝“为了所谓向后兼容但完全无人调用的平行实现”；
   - 移除无调用方的旧宏定义、枚举项与类型声明。
3. **孤儿接口（Orphan Interfaces）**：
   - 检查 `server/src/` 中导出的非内部辅助函数是否有真实生产调用方（不能仅被单元测试调用）。无调用方则删除。
4. **过时注释与 TODO**：
   - 检查代码中是否残留已被证伪的技术假设、已修复问题的临时注释或已过期的 TODO/FIXME。

---

### Step 4: 修正/删除与全量回归验证 (Fix, Prune & Verify)

1. **修正过时内容**：
   - 更新文档中的数据、架构图、表格和命令参数；
   - 修正代码中因接口更新导致的过时注释。
2. **删除无用内容**：
   - 对 Step 3 中确认无生产调用、无长远保留价值的无用文件和僵尸代码，坚决执行删除；
   - 删除后确认 `CMakeLists.txt` 或构建系统未引用已删文件。
3. **运行全量测试验证（绝不盲目提交）**：
   清理或同步后，必须执行全量编译与单测，确保没有误伤任何现行逻辑：
   ```bash
   cmake -B build-x86 -DCMAKE_BUILD_TYPE=Debug -DBUILD_EBPF=OFF && \
   cmake --build build-x86 -j$(nproc) && \
   ctest --test-dir build-x86/server -R "test_net_info|test_quality|test_anomaly|test_audio|test_band|test_serializer|test_event|test_bt_full|test_bt_monitor$|test_iface|test_logger|test_traffic|test_database|test_weaknet_config|test_monitor" --output-on-failure
   ```
4. **原子性提交**：
   清理与更新操作必须提交到 Git 历史（例如 `chore(repo): 清理过时代码与文档同步`），保持工作区 clean。
