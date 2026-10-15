---
name: bms-testing-patterns
description: 用于为 OpenHarmony BundleManager 添加、定位或调整测试。 当需求涉及单元测试、系统测试、模块测试、benchmark、fuzz、GN 测试 target、mock、测试 HAP/resource、安装流程测试、IPC 测试、权限/校验测试或回归测试设计时使用。
---

# BMS 测试模式

使用此 skill 为 BundleManager 修改选择合适测试位置和测试粒度。

## 工作流程

1. 判断测试类型：
   - 单个类或函数：优先 `services/bundlemgr/test/unittest/`。
   - inner API/proxy/host：看 `interfaces/inner_api/test/unittest/` 或服务单测。
   - JS/native kit：看对应 `interfaces/kits/*/test`。
   - 端到端安装、卸载、权限、资源：看 `test/systemtest/common/bms/`。
   - 异常输入和安全边界：看 `test/fuzztest/`。
   - 性能或结构体基准：看 `test/benchmarktest/`。

2. 阅读 `references/test-map.md`，找相近目录和已有模式。

3. 阅读 `references/test-checklist.md`，确认 mock、资源、GN 和验证命令。

4. 优先扩展已有测试目录和 BUILD.gn，只有找不到合适归属时再新增目录。

## 测试策略

- 修改共享逻辑、安装链路、权限、IPC、RDB 时要补测试。
- 小范围条件分支优先补单测；跨进程或真实 HAP 行为优先补系统测试。
- 使用现有 mock，不要为一个测试重新发明整套伪服务。
- 测试命名跟随已有 `Bms...Test` 和目录命名习惯。

## 参考资料

- `references/test-map.md`：测试目录地图。
- `references/test-checklist.md`：补测试检查清单。
