---
name: explain-project-design
description: 把这个仓库解释成一个从 coordinator-heavy live loop 演进到 standalone bridge 的版本化多智能体设计。
---

# 讲清项目设计

适用场景：向评审、同事、面试官介绍这个仓库。

## 需要覆盖

1. V1：coordinator-heavy 多智能体 runtime
2. V2：standalone-bridge runtime
3. player / runtime / reviewer 的职责边界
4. 为什么第一版 live 路径效果一般
5. 为什么第二版 bridge 设计更强
6. `.github` 标准 Copilot 资产和 `archive/legacy-runtime-assets/` 的区别
7. 为什么这个项目仍然值得写进简历

## 参考文件

- `README.md`
- `PROJECT_DESIGN.md`
- `AGENTS.md`
- `STARTUP.md`

## 约束

- 同时讲清架构故事和真实 live 运维故事。
- 不要把归档的 legacy runtime 资产说成当前活动的标准 Copilot skill。
