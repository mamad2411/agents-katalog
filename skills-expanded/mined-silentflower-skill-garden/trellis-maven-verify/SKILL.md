---
name: trellis-maven-verify
description: 为 Trellis 的 Maven/Java 项目生成分层验证计划、裁剪多模块 reactor 与昂贵 lifecycle goal，并执行或复用可审计证据。用于 Java 8 或大型 Maven 多模块编译很慢、`-am` 拉起过多模块、compile/package 额外运行 sources jar、copy-dependencies、repackage、shade、assembly、javadoc、frontend 等 goal，或 implement 与 Check-All 之间需要避免重复构建时；不用于发布、deploy、修改 POM/settings/JDK 或非 Maven 构建系统。
---

# Trellis Maven Verify

为 Maven 验证选择最短且足够的生命周期，并让 implement 产生的结果能被 Check-All 只读复用。不要修改业务 POM、Maven settings、JDK 或本地仓库。

## 选择模式

- `quick`：编码过程中的局部反馈。默认选择变更模块并加 `-am` 覆盖必要上游；compile 且 compiler plugin 兼容时使用 source-stale，避免陈旧 SNAPSHOT 和无变化整模块重编。不得把结果宣称为最终消费者覆盖。
- `final`：implement 收口。覆盖变更模块、必要上游和已确认消费者，默认使用 conservative 编译并生成可复用 evidence。只有任务材料已确认模块内部低风险变化时，才显式选择 source-stale。
- `reuse`：Check-All 或复查阶段。只运行 `check`，不得运行会写 `target/`、本地仓库或缓存的 Maven goal。

没有 `pom.xml` 时报告 `N/A` 并返回原工作流。需要决定业务测试、消费者或制品验收范围时，先从 PRD、design、implement、项目 spec 或用户输入获取，不要猜测。

## 工作流

1. 读取 [references/lifecycle-policy.md](references/lifecycle-policy.md)，确定需要的最低 lifecycle、测试和附属制品。
2. 生成计划。优先把计划写入 gitignored runtime 目录：

   ```bash
   python3 ./.trellis/scripts/maven_verify.py plan \
     --mode quick \
     --goal compile \
     --output .trellis/.runtime/maven-verification/quick-plan.json
   ```

3. 检查 JSON 中的 `status`、`selectedModules`、`argv`、`toolchain.maven.buildSide`、`toolchain.maven.source`、`lifecycle.expensiveBindings`、`warnings` 和 `confidence`。`blocked` 不得执行；`not-applicable` 返回原工作流。
   - quick 的 `compileStrategy.effective=source-stale` 只证明局部源码 stale 编译，不覆盖公共 API/ABI、常量内联、注解处理器、POM或资源契约风险。
   - `fallbackArgv` 存在时，它保留 reactor 范围但恢复 conservative 编译；source-stale 结果异常时可按该 argv 重跑。
   - 是否使用并行由模型结合 reactor 范围、依赖拓扑、插件线程安全、测试共享资源和机器资源自行决定；不得为了选择并行度额外重复构建。
4. 只有 implement 或具备正常构建写权限的主会话可以执行计划：

   ```bash
   python3 ./.trellis/scripts/maven_verify.py run \
     --plan-json .trellis/.runtime/maven-verification/quick-plan.json
   ```

5. 交付前用 `final` 重做计划。显式传入已确认消费者；不要用全仓 `-amd` 代替影响分析：

   ```bash
   python3 ./.trellis/scripts/maven_verify.py plan \
     --mode final \
     --goal test \
     --consumer api-app \
     --output .trellis/.runtime/maven-verification/final-plan.json
   python3 ./.trellis/scripts/maven_verify.py run \
     --plan-json .trellis/.runtime/maven-verification/final-plan.json
   ```

   只有任务材料明确确认没有公共 API/DTO/常量、注解处理器、POM、资源契约或跨模块协议变化时，才可把 final 改为：

   ```bash
   python3 ./.trellis/scripts/maven_verify.py plan \
     --mode final \
     --goal compile \
     --compile-strategy source-stale \
     --output .trellis/.runtime/maven-verification/final-plan.json
   ```

6. Check-All 只读复用 evidence：

   ```bash
   python3 ./.trellis/scripts/maven_verify.py check \
     --latest \
     --require-plan .trellis/.runtime/maven-verification/final-plan.json
   ```

7. 按 [references/evidence-contract.md](references/evidence-contract.md) 解释 `reusable`、`partial`、`stale`、`failed`、`blocked`。覆盖不足时报告精确重跑缺口，不要无条件全仓构建。

## 执行边界

- 构建侧由 Maven 根所在的原生文件系统决定。原生 Windows/Linux 使用本侧工具链；WSL 的 drvfs/9p Windows 盘项目使用 Windows Maven/JDK/本地仓库，不依赖 automount root 是否为 `/mnt`；WSL ext4 项目使用 Linux Maven/JDK/本地仓库。
- 默认优先同侧项目 wrapper，其次复用同侧 PATH 中的 Maven；不下载、不安装、不固定升级 Maven 3.9+。显式 `--maven-executable` 只能覆盖为同侧 Maven。
- Maven、JDK、`MAVEN_ARGS`/`MAVEN_OPTS`、settings 和本地仓库必须来自同一构建侧。Windows 项目显式指向 WSL ext4 Maven/仓库，或 POSIX 项目指向 Windows Maven/仓库时必须 blocked。
- 默认停在 `compile`；只有测试验收进入 `test`，只有制品验收进入 `package` 或更后阶段。
- 默认不加 `clean`、`install`、`deploy`、`-amd`；是否显式传入并行参数由模型根据当前项目和验证目标判断。
- quick auto 只在 effective model 确认 `maven-compiler-plugin >= 3.1` 时加入 `-Dmaven.compiler.useIncrementalCompilation=false`；无法确认时自动降级 conservative。显式 source-stale 无法确认兼容性时必须 blocked。
- final auto 固定为 conservative。不要从文件名猜测低风险；必须从 PRD、design、implement、spec 或用户确认获得风险口径。
- 模型可以为存在并行空间的多模块 reactor 选择 `--threads`，也可以因依赖链近似串行、插件非线程安全、测试共享端口/文件、CPU、内存或 I/O 压力而保持串行。常规 implement 只执行当前选定的一份计划，不通过额外试跑比较并行度；Check-All 仍只读复用 evidence。
- skip 参数只能来自脚本已确认的插件兼容表或 effective model 证据；不得自行拼接。
- effective POM 无法读取时，计划必须 `blocked` 或明确降低置信度，不能声称外部父 POM没有额外绑定。
- `quick` 成功只能作为局部反馈。最终报告必须给出 evidence 路径、覆盖等级、模块、测试、跳过项和剩余风险。
- audit-only Check-All subagent 只能调用 `check`。不得调用 `plan` 或 `run`，因为 Maven model/goal 可能写本地缓存；`check` 对项目 wrapper 只复核冻结版本、wrapper 文件与配置指纹，不执行可能下载 Maven 发行包的 wrapper。

## 常用参数

- `--maven-root <path>`：仓库含多个 Maven reactor 时显式选择根目录。
- `--module <selector>` / `--consumer <selector>`：使用真实 module 相对路径或 artifactId，可重复。
- `--test <pattern>`：生成 `-Dtest=` 并进入测试覆盖证据，可重复。
- `--artifact sources|javadoc|assembly|shade|repackage|copy-dependencies`：声明附属制品验收。
- `--offline yes|no|auto`：只有项目或用户已确认离线依赖完整时使用 `yes`。
- `--local-repository <path>`：显式使用已准备好的同侧 Maven 本地仓库。不会自动复制仓库、修改 `settings.xml`，也不会让 Windows Maven跨到 WSL ext4 仓库。
- `--compile-strategy auto|conservative|source-stale`：quick compile 的 auto 可选择 source-stale；final auto 保守。source-stale 只适用于 compile。
- `--threads <count|multiplierC>`：模型按当前 reactor、插件和机器资源选择的 Maven 并行度，例如 `4`、`1C`、`1.5C`；不为选择该值额外执行对比构建。
- `--effective-pom <file>`：使用已冻结的 effective POM 做离线分析；文件内容仍进入 POM 指纹。
- `--maven-executable <path>`：显式选择同侧 Maven。通常无需传入；默认会复用同侧 wrapper 或 PATH Maven。WSL 调用 Windows `.cmd` 时由脚本使用固定 `cmd.exe` argv 包装，不拼接任意 shell 命令。

脚本的 `--help` 是参数事实源；本 Skill 只维护流程和边界。
