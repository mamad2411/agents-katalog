---
name: project-init
description: "[治理] 在 01_PROJECTS 下新建项目时使用。触发条件：用户要求新建/导入项目。v1 六步流程的极简版。"
---

# 新建项目（两件套）

## 流程

1. `01_PROJECTS/{name}/` 建目录
2. 写 `AGENTS.md`（项目级指令：项目定位、技术栈事实、约束、敏感信息表只引用 credentials.json 的 id）
3. 写 `README.md`（基本信息）
4. `04_MEMORY/project/proj_{name}.md` 建项目记忆 + INDEX.md 加一行指针

## 项目类型

- 单一项目：`src/` 直接放代码
- 项目集：`src/` 放子项目目录，AGENTS.md 含子项目清单
- 子目录按 file-placement skill §2 标准骨架与按需启用规则创建（有文件才建目录，禁过度建层）

## 导入已有项目（额外步骤）

- 服务发现：`nssm list`、`docker ps -a`、端口监听扫描
- 凭据提取 → credentials.json（引用不复制）
- 依赖推断（端口连接/配置引用）记入 AGENTS.md"相关项目"

## gotchas

- 禁止 `src/{name}/` 冗余嵌套
- PROGRESS.md/STATUS.md 已废弃：长任务用 goal，项目状态写 AGENTS.md 头部小节
- 敏感信息表只写 credentials.json 的 id，绝不复制 value
