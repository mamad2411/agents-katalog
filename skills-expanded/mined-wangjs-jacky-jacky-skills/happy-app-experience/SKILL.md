---
name: happy-app-experience
description: "在设计、开发或交付 Happy/Paws App 与 PC Web 时按需参考 Happy/Paws 经验，包括移动端架构、React Native/Expo 取舍、PC Web 视觉基线、验证、OTA、安装包与 Release 边界。用于用户明确要求参考 Happy/Paws，或当前问题与这些真实工程经验高度匹配时；它只提供上下文，不是 Workflow，也不强制复制 Happy 的技术栈或具体尺寸。"
---

# Happy App Experience

这是可插拔的经验源，**不是 App Workflow**。它提供 Happy/Paws 已验证的事实、取舍、证据入口和适用边界；目标、实现顺序与交付仍由当前任务决定。

## 何时加载

- 用户明确说“参考 Happy/Paws 的经验”；
- 当前 App 或移动端问题与 description 高度匹配，且这些经验可能改变决策；
- 当前任务要延续 Happy PC Web 的视觉语言，尤其涉及命令面板、搜索选择器、复杂菜单等桌面浮层的字体层级、密度、圆角、边框、阴影或主题状态；
- 需要比较 OTA、重新构建、安装包、真机验证或 Release 的边界。

不要因为任务提到 App 就自动加载，也**不强制** React Native、Expo 或任何其他技术栈。运行维护、daemon、中继和自托管排障属于运维经验，不在这里展开。

## 渐进读取

1. 先读 `references/INDEX.md`，只判断哪个主题相关。
2. 当前问题命中时至多再读一个 reference；第一项已经足够就停止。
3. Happy 源码可用时重新核验 reference 列出的相对证据路径，并以当前源码为准。
4. 源码或证据不可读时，把内容视为带最近验证日期的**历史经验**，明确不确定性，不冒充当前事实。

同一上下文直接返回相关事实与边界，不创建中转 Markdown。只有跨会话复用、证据或真实交付物才落盘。

## 如何使用经验

- 先提取“决策、成立条件、反例和证据”，再映射到当前 App。
- 区分“Happy 当前这样做”和“其他项目也应该这样做”；迁移前重新验证运行时、原生依赖、发布渠道和团队约束。
- reference 与当前证据冲突时以当前证据为准，并把旧经验留作可追溯的失效历史。
- 不因参考某项目就自动获得 push、OTA、Release、商店提交或其他外部副作用授权。

## 本地 Memory

本 Skill 只拥有自己的 `local/`。第一次需要读取或写入时，从当前 Skill 目录按需加载 `../../docs/philosophy/references/local-memory.md`；独立分发导致引用不可读时，以本节摘要继续并保留诊断。

默认从 `local/INDEX.md` 进入 **1 个根入口**，再读 **1 个作用域 map** 和最多 **3 条**正文，合计不超过 **32 KiB**。定位优先级为：显式 Feature/Task/Goal ID → WorkTree → 分支 → Repo → 主题；Feature 路径必须包含 `repo-key`。

Memory 使用不可变记录，修正时由新记录的 `supersedes` 指向旧 ID。保存不等于可信；只有稳定、脱敏、反复验证且具有迁移价值的结论才晋升到 committed reference。

Token、密码、私钥、完整环境变量和未经授权的私密内容等敏感信息不得进入 `local/`。遇到缺字段、断链或损坏条目时跳过，以当前证据继续并标记待修复；禁止为了找答案递归读取整个 Memory 池。

## 写回判断

每次使用结束都判断：是否出现会改变未来决策的新证据、是否需要更新 Feature map、是否有新记录 supersedes 旧经验，以及是否有足够证据晋升稳定 reference。没有长期价值时不写任何文件。
