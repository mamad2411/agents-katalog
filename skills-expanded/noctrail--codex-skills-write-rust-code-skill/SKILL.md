---
name: write-rust-code
description: "Rust 代码编写指南。Use when creating or modifying Rust crates, modules, tests, async code, terminal/PTY/rendering/agent/policy code, or APIs in Noctrail; enforce minimal, non-redundant code."
---

# Write Rust Code

## 目标

为 Noctrail 写 Rust 时，优先保证终端正确性、跨平台行为、安全边界和长期可维护性。风格参考 Rust、Cargo、Tokio、ripgrep、Alacritty、WezTerm 等成熟项目的共同做法：小而清晰的 API、显式错误、可靠测试、少量必要抽象。

## 代码最小原则

把代码当成维护负债。每次写代码都先问：能不能通过更好的数据结构、更清楚的边界、删除旧分支或复用已有机制来少写代码。

Linus 式代码态度蒸馏为这些规则：

- 好代码减少特殊情况，而不是给每个例外补一层 `if`。
- 先设计数据结构和不变量；代码应该自然地围绕它们变简单。
- 小 patch 胜过大改动；局部清晰胜过宏大框架。
- 抽象只有在消除真实重复或表达稳定边界时才成立。
- 不为“以后可能需要”写代码；需要时再加。
- 删除死代码、重复状态、重复转换和重复错误路径。
- 让失败路径和正常路径一样直接，避免隐藏控制流。
- 如果实现需要大量解释才能显得合理，优先重新设计。

新增代码前优先尝试：

- 合并重复分支。
- 缩小 public API。
- 用 enum 或类型表达状态，而不是散落布尔值。
- 把平台差异隔离到边界，而不是复制整套逻辑。
- 删除现在不再需要的辅助函数、配置项和测试 fixture。

## 开工前

先读取本地上下文：

- `docs/plan.md` 中的模块边界、平台目标、安全模型和验收标准。
- workspace、crate、`Cargo.toml`、`rustfmt.toml`、`clippy.toml`、CI 脚本和已有模块风格。
- 相关调用方和测试，不只看被改文件。

如果仓库尚未初始化 Rust workspace，按计划中的 crate 边界命名，使用 `noctrail-*` crate 前缀和 `noctrail` CLI 命名。

## 架构边界

- 按职责放代码：`terminal-core` 管状态机和 grid，`pty` 管进程和 ConPTY/Unix PTY，`renderer` 管 wgpu/text cache，`ui` 管 panes/workspaces，`agent` 管模型与上下文，`policy` 管权限、风险和 redaction。
- 默认使用 `pub(crate)`；只有跨 crate API 才 `pub`。
- 让数据所有权跟随模块边界，避免全局可变状态。
- 新抽象必须减少真实复杂度，不能只为了“未来可能需要”。
- 优先减少状态数量和状态转换次数；状态越多，终端、PTY 和 agent 的 bug 面越大。
- 平台差异放进清晰的 `cfg` 模块，不在业务逻辑中散落条件判断。

## Rust 风格

- 运行 rustfmt；不要手调格式。
- 命名遵循 Rust 习惯：类型 `UpperCamelCase`，函数和变量 `snake_case`，常量 `SCREAMING_SNAKE_CASE`。
- import 保持局部清晰，避免通配符导入，测试模块例外需有明显收益。
- 注释解释不明显的约束、协议、unsafe 前提或跨平台坑，不复述代码。
- 文档注释覆盖公共 API 的行为、错误和平台差异。

## 错误处理

- 库 crate 返回具体错误类型，优先 `thiserror` 风格；二进制入口可用 `anyhow` 风格，但先遵循仓库已有依赖。
- 错误要带上下文：哪个 shell、哪个 cwd、哪个 PTY、哪个配置项、哪个 provider。
- 运行时代码不要 `unwrap`/`expect`，除非表达不可违反的不变量并写明原因；测试中可以更直接。
- 区分用户可恢复错误、平台不支持、配置错误、内部 bug 和安全拒绝。
- agent/tool 执行失败不得破坏终端主流程。

## Async 与并发

- UI event loop 不做阻塞 IO。
- PTY read、agent request、文件索引、存储写入放到可取消的后台任务。
- 使用 bounded channel 或背压策略处理高输出，避免无限增长。
- 锁的作用域要短；不要在持锁状态 await。
- task lifecycle 必须可关闭、可超时、可记录错误。

## 跨平台

- Windows、macOS、Linux 都是 P0；不要写只在当前机器成立的路径、shell、PTY 或换行假设。
- Windows 关注 ConPTY、PowerShell/cmd/WSL、路径前缀和 UTF-16/UTF-8 边界。
- Unix 关注 PTY resize、信号、locale、Wayland/X11 降级。
- 平台增强必须有 fallback，尤其是透明、blur、GPU backend、字体 fallback。

## 安全与隐私

- 默认不读取或上传全量环境变量、shell history、SSH key、token、浏览器 cookie。
- 日志、错误、审计记录必须经过 secret redaction。
- shell execution、filesystem write、MCP/tool 调用要穿过 policy 层。
- `unsafe` 只在必要边界使用，必须写明安全条件，并用测试覆盖不变量。

## 终端与渲染细节

- 终端正确性优先于视觉效果；agent 功能不能影响基础终端稳定。
- VT parser、grid、scrollback、alternate screen、bracketed paste、mouse reporting、IME、Unicode width 和 emoji 都要有测试意识。
- renderer hot path 避免无意义 allocation；优化必须有 benchmark 或清晰测量目标。
- DPI、字体 fallback、透明/blur 降级要进入验收思维。

## 测试标准

- 单元测试覆盖纯逻辑：grid、selection、config、policy、redaction、risk classifier。
- 集成测试覆盖 PTY、shell integration、resize、copy/paste、alternate screen。
- golden/snapshot 测试覆盖 ANSI、Unicode、pane border、agent review UI。
- bug fix 必须尽量先写能失败的测试；安全修复必须补 corpus。
- 不可稳定测试的行为至少提供 smoke test 或清晰手动验证步骤。

## 依赖与性能

- 新依赖必须成熟、维护活跃、许可证可接受、功能边界清楚。
- 避免为了少量代码引入重依赖，尤其是终端热路径、启动路径和安全层。
- feature flag 要显式，默认特性不要悄悄启用网络、平台集成或大体积能力。
- 先写可读正确的代码，再用 profile/benchmark 优化。
- 性能优化不能制造长期膨胀；只有测量证明瓶颈存在时才保留复杂实现。

## 提交前检查

优先运行：

```powershell
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-targets
```

如果 workspace 尚不存在或命令不适用，说明当前验证限制，并使用可用的最接近检查。
