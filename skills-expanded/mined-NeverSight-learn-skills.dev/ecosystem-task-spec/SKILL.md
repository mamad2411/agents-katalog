---
name: ecosystem-task-spec
description: 回答 PetConnect 生态任务的设计规范、完成进度时间轴、交付验证。当用户问设计规格、spec、验收标准、进度、时间轴、交付情况、任务状态、认领情况时使用。按统一模板凝练输出，数据来自 tasks/、docs/demand/。
---

# 生态任务设计规范与交付验证

## 数据源

| 问题类型 | 数据源 |
|---------|--------|
| 进度/认领状态 | `tasks/_ecosystem-parallel-index.md` |
| 设计规范/验收 | `tasks/ecosystem-N-xxx/spec.md` |
| 开发约束/自检 | `docs/prompts/ecosystem-boundary-rules.md` |
| 总览/阶段索引 | `docs/demand/ecosystem-extensions/00-overview.md` |

回答时注明「数据来自 xxx」，便于核对。

---

## 1. 设计规范回答

**凝练原则**：目标 | 范围 | 验收，每段 2~3 行。

**回答要点**：Goal、专属文件、共享资源、验收标准、开发约束。从对应 `spec.md` 提取，不展开实现细节。

**速查模板**（填空输出）：

```markdown
## 生态 N：{名称}

| 项 | 内容 |
|---|------|
| 目标 | {Goal 一句话} |
| 专属文件 | {lib/api/xxx.ts、pages/Xxx.tsx} |
| 共享资源 | {points/healthDiary 等，仅读/仅增} |
| 验收标准 | {3~5 条核心验收} |
```

---

## 2. 进度时间轴回答

**凝练原则**：只列关键状态，不展开细节。

**输出格式**：表格（生态 | 状态 | 认领者 | 预计工时）。先读 `tasks/_ecosystem-parallel-index.md`，再输出。

**进度汇报模板**：

```markdown
## 生态模块进度（数据来自 tasks/_ecosystem-parallel-index.md）

| 生态 | 名称 | 状态 | 认领者 | 预计工时 |
|:---:|---|:---:|---|:---:|
| 1 | 社区达人 | ⬜/🚧/✅ | - | 30h |
| ... | ... | ... | ... | ... |

**下一步**：{待认领生态的 spec 路径，或「全部完成」}
```

甘特图等可选格式见 [reference.md](reference.md)。

---

## 3. 交付验证回答

**凝练原则**：先结论（通过/未通过），再列未通过项。

**输出格式**：Checklist + 验证命令。对照 `spec.md` 验收标准 + `ecosystem-boundary-rules.md` 验收自检。

**交付总结模板**：

```markdown
## 生态 N 交付验证

**结论**：✅ 通过 / ❌ 未通过

### 验收 Checklist
- [ ] 验收项 1 来自 spec.md
- [ ] 验收项 2 ...
- [ ] 未修改其他生态专属文件
- [ ] types.ts 仅追加
- [ ] npm run build 通过

### 验证命令
```bash
npm run build
```

### 文件清单（如有）
| 文件 | 状态 |
|------|:---:|
| lib/api/xxx.ts | ✅ |
```

---

## 4. 快速响应

**用户说「给我进度汇报」**：读取 `tasks/_ecosystem-parallel-index.md`，输出上述进度汇报模板（填好数据）。

**用户说「生态 N 的设计规范」**：读取 `tasks/ecosystem-N-xxx/spec.md`，输出速查模板（填好数据）。

**用户说「交付验证」**：读取对应 spec + boundary-rules，输出交付总结模板（填好 Checklist）。
