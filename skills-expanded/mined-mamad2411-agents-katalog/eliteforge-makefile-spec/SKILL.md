---
name: eliteforge-makefile-spec
description: 识别仓库并通过统一命令接口生成或重构根目录 Makefile。用户要求创建、规范化、审查或更新 Makefile，统一 make help/doctor/install/clean/format/lint/test/build/dev/deploy 目标，支持 VERSION、SKIP_TESTS 等动态参数，发布 JAR 等版本化制品，适配 Docker push、Electron/Tauri/Capacitor 等应用壳，或要求兼容 GNU Make 3.81、macOS 和 Windows 时使用。
metadata:
  version: 1.0.0
---

# EliteForge Makefile 规范

## 目标

生成一个位于仓库根目录的 `Makefile`：对外命令和参数保持统一，内部实现适配实际检测到的仓库拓扑、构建系统、制品发布方式、Docker 配置和应用壳，并兼容 GNU Make 3.81、macOS 与 Windows。已有 Makefile 必须原地重构，不得在外层叠加重复配方。

## 统一公共接口

- 所有仓库都必须定义 `help`、`doctor`、`install`、`clean`、`format`、`lint`、`test`、`build`、`dev`、`deploy`。
- 不再生成 `check`、`run`、`verify` 公共目标；迁移已有 Makefile 时，仅在仓库自动化仍有调用方的情况下保留隐藏兼容别名。
- 所有 Makefile 都接受 `VERSION` 和 `SKIP_TESTS` 命令行变量，例如 `make build VERSION=1.2.3 SKIP_TESTS=true`。只将变量传给语义适用且仓库真实支持的目标；不得静默忽略已传入的值。
- `deploy` 只发布版本化软件包或构建制品，例如 JAR、npm 包或 Python 包，不负责部署运行中的服务。
- Docker 能力统一为 `docker-build`、`docker-run`、`docker-stop`、`docker-push`；应用壳能力统一为 `app-build`、`app-dev`、`app-clean`。
- 生成的语法必须兼容 GNU Make 3.81。Windows 兼容指 Windows 上的 GNU Make，不得宣称兼容 NMake。

## Output Path

按以下优先级确定主 Makefile 路径：

1. 用户为当前任务明确指定的文件路径；
2. 用户明确指定仓库目录下的 `Makefile`；
3. `<git-top-level>/Makefile`。

如果输入是目录，则在末尾追加 `Makefile`。除非用户明确要求其他文件名，否则使用区分大小写的标准文件名 `Makefile`。将该文件作为唯一事实来源；未经用户明确要求，不得创建或修改其他项目文件。

## 必读资料

1. 每次任务都读取 [references/target-contract.md](references/target-contract.md)。
2. 每次任务都读取 [references/detection-rules.md](references/detection-rules.md)。
3. 仅按检测到的技术栈读取 [references/ecosystem-adapters.md](references/ecosystem-adapters.md) 中的对应章节。
4. 仓库属于多项目仓库、存在 Docker/Compose 或应用壳、需要编排多个开发进程，或已有 Makefile 较复杂时，读取 [references/orchestration-patterns.md](references/orchestration-patterns.md)。

## 执行流程

### 1. 盘点仓库

确定仓库根目录后，使用绝对路径运行技能内置的只读检测器：

```bash
python3 <skill-dir>/scripts/inspect_repository.py <repository-root> [--no-git-root]
```

当用户明确将任务范围限定在更大 Git 仓库内的某个子目录时，传入 `--no-git-root`。记录检测结果中的仓库拓扑、组件清单、锁文件与包管理器、现有 Makefile、Docker/Compose 文件、应用壳证据、CI 文件和警告。

### 2. 核实证据

读取所有相关清单文件，以及现有 Makefile、包脚本、构建插件、仓库脚本、CI、Dockerfile/Compose 文件和仓库文档中包含命令的部分。核实版本来源、跳过测试参数、制品仓库、发布任务、镜像名称与 Registry。修改旧目标名称前，先搜索仓库内是否仍有调用方。

不得仅根据目录名作出结论。编辑前先解决包管理器冲突、主应用归属或运行路径冲突；只有仓库证据无法消除会实质影响结果的歧义时，才询问用户。

### 3. 设计映射

将 `target-contract.md` 中的每个统一目标和动态变量映射到仓库真实存在的命令。对于多项目仓库，确定组件依赖顺序，并将组件操作隐藏在 `_...` 私有目标后。对于 Docker 或应用壳，只使用契约规定的稳定能力目标名。

优先采用已被 CI 验证的命令、包装脚本、锁文件和仓库本地二进制。不得虚构缺失脚本，也不得静默更换包管理器、构建配置、测试范围、版本来源、制品流向或主要开发入口。

### 4. 生成或重构 Makefile

严格实现统一目标与参数接口。将重复逻辑收敛为变量、可复用配方或私有目标。只有仓库内自动化仍在调用旧目标时，才将旧目标保留为不出现在帮助信息中的轻量兼容别名。

Makefile 语法不得使用 GNU Make 3.81 之后才提供的特性。配方必须使用仓库相对路径、非交互执行并限定作用范围，优先调用跨平台的仓库工具或包装脚本；需要操作系统差异时显式处理 `OS=Windows_NT`。保留锁文件和用户数据。不得加入全局安装、`sudo`、破坏性的 Git/Docker 清理、无范围删除，也不得在命令或帮助信息中暴露密钥。

`doctor` 必须区分统一主路径所需的必备工具与可选能力工具，并检查当前操作系统对应的 wrapper 或命令。当本地统一目标不依赖 Docker 时，Docker 缺失只能产生非阻断警告。

不得为了绕过 Makefile 设计而额外创建辅助脚本。如果正确的跨平台或进程生命周期行为必须依赖新的非 Makefile 文件，则停止并请求用户扩大任务范围。

### 5. 验证

在仓库根目录执行：

1. `make help`；
2. 对每个统一目标和已生成的能力目标执行 `make --no-print-directory -n <target>`；
3. `make doctor`；
4. 使用 `VERSION=0.0.0-test SKIP_TESTS=true` 对 `build`、`deploy` 和适用的能力目标执行试运行，确认动态变量被正确消费或明确拒绝；
5. 在非 Windows 环境对目标执行 `make --no-print-directory -n OS=Windows_NT <target>`，静态检查 Windows 分支；
6. 当依赖已经就绪且执行属于当前任务范围时，运行 `make lint`、`make test` 和 `make build`。

不得仅为验证而执行 `install`、`dev`、`deploy`、`docker-run`、`docker-push` 或其他长时间运行、会改变本地或远程状态的目标。报告每个未执行命令及原因。无法在 Windows 上实测时，明确说明只完成了 Windows 分支静态检查。完成前修复语法错误、缺失的目标依赖、不安全清理、重复工作、变量未消费和目标语义不一致。

## 强制规则

- 所有仓库必须使用完全一致的统一公共目标名称和语义。
- 技术栈与组件差异不得泄漏到公共接口。
- Makefile 中面向用户的帮助、检查、跳过、警告和错误文案必须使用中文；命令、目标名和技术标识保持原样。
- `lint` 必须汇总已配置的非修改式格式检查、静态检查、类型检查和编译检查；`build` 必须覆盖全部本地交付产物，`dev` 必须覆盖完整可用的开发拓扑。
- `deploy` 必须发布 `VERSION` 对应的软件包或制品；无法解析版本、制品或发布目标时必须失败，不得假装成功。
- `SKIP_TESTS=true` 只能跳过 `install`、`build`、`deploy` 等生命周期中隐含的测试，不能让显式 `test` 目标跳过测试。
- 必须检测 Docker 和应用壳，但不得因此强制本地构建经过 Docker。
- `docker-push` 必须推送明确带版本标签的镜像；禁止静默推送 `latest`。
- 只有确实不存在的非发布能力才能明确输出 `跳过：`；不支持的 `dev` 或 `deploy` 必须输出清晰的 `错误：`。
- 必须兼容 GNU Make 3.81；禁止使用 `.ONESHELL`、`.RECIPEPREFIX`、`.WAIT`、`$(file ...)`、分组目标 `&:` 等较新语法。
- 仓库存在 wrapper 时，禁止改用系统工具替代。
- 仅做过试运行或已跳过的命令，禁止声称验证成功。

## 完成报告

返回：

- 输出 Makefile 路径；
- 检测到的仓库拓扑及支撑证据；
- 检测到的 Docker/Compose 与应用壳能力；
- 统一目标到实际实现的映射摘要；
- `VERSION`、`SKIP_TESTS` 及其他覆盖变量的适用目标；
- macOS、Windows 与 GNU Make 3.81 兼容性验证范围；
- 验证命令与结果；
- 尚未解决的歧义，或有意保留的兼容别名。
