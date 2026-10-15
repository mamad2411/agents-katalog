---
name: "cc-feat"
description: "特性设计与实现。需求→设计→编码→验收。含 design/impl/accept 三子流程。"
---

# Feat - 特性开发

## 职责
需求/架构 → 技术设计 → 编码实现 → 验收

## 规模上限 (Production Ready)

| 维度 | 上限 | 说明 |
|------|------|------|
| 文件变更数 | ≤ 6 个 | 新建 + 修改总数 |
| 新增/修改代码行数 | ≤ 300 行 | git diff 统计 |
| 新增公共 API | ≤ 4 个 | 对外暴露函数/类/接口 |
| 新增函数/方法 | ≤ 8 个 | 包含私有函数 |
| 模块跨度 | ≤ 2 个模块 | 一级目录数 |

**超出任一维度时**: 拆分为多个子 feat，每个子 feat 都必须独立满足完整 DoD。

---

## 前置检查（必须全部通过）

1. **上游 stale 检查**: REQ/ARCH 任一 `stale=true` 则暂停
2. **冲突检测**: Grep `status: designing` + `status: implementing` → files.path 重叠则警告（design 阶段即检测，不等到 impl）
3. **依赖顺序**: `depends_on` 引用的 FEAT 未完成则等待
4. **Roadmap 上下文** (关联时): 用 read-yaml 提取 priority/depends_on + 接口契约
5. **接口合规** (多模块时): design 接口须与 roadmap 定义对齐
6. **入口来源验证** (非 REQ 驱动时): 以下任一即可替代 REQ 作为前置条件

### 入口来源类型

| origin_type | 含义 | 前置条件 | design.md frontmatter 额外字段 |
|-------------|------|---------|-------------------------------|
| `req` (默认) | 需求驱动 | REQ 文档存在且 status=approved | (无额外) |
| `origin_fix` | Bug 修复衍生 | fix-report 存在且 status=fixed | `origin_fix: "{fix-slug}"` |
| `origin_refactor` | 重构/技术债 | 无硬性前置，但须在 design.md 说明重构动机和预期收益 | `origin_refactor: true` + `refactor_motivation:` |
| `origin_spike` | Spike 验证后实现 | spike 文档存在且 status=validated | `origin_spike: "{spike-slug}"` |

> 非 REQ 驱动的 feat 在 feat-accept 通过后，不更新 REQ status (因为没有关联 REQ)，但仍同步 roadmap (如关联)。

---

## 子流程

### feat-design 技术设计

**输入**: REQ + ARCH 文档 (或 origin_fix/origin_refactor/origin_spike 替代 REQ)  
**输出**: `features/{slug}YYYYMMDDHHMM/{slug}-design.md` + `impl-checklist.yaml`

design.md 必须包含:
1. 实现思路概述
2. 文件变更清单 (新建/修改/删除)
3. 接口与类型引用
4. **测试策略** (必填，含测试金字塔比例、Mock 策略、关键路径覆盖计划)
5. 风险与依赖
6. **DoD 验收标准** (必填)

**测试策略最低要求**:

| 项目 | 要求 |
|------|------|
| 测试金字塔 | 单元:集成:E2E 比例明确 (推荐 7:2:1) |
| Mock 策略 | 外部依赖如何 mock/stub |
| 关键路径 | 列出必须覆盖的核心场景 (≥3 个) |
| 边界测试 | 空值/异常/并发等边界场景 (≥2 个) |

> checklist 格式详见 `templates/design.md`

### feat-impl 编码实现

**输入**: design.md + impl-checklist.yaml  
**输出**: 实际代码 + 更新的 checklist.yaml

**规则**: 先类型后实现；遵循现有风格；小步提交；避免 any

**每完成一个文件**: 更新 checklist status; 运行 validate-yaml 校验

**异常处理**:

| 场景 | 动作 |
|------|------|
| 需求不清 | ↩ 回退 cc-req 补充具体缺失点 |
| 设计不可行 | ↩ 回退 feat-design 修改 |
| 发现 bug | → 分支创建 issue |
| 发现好模式 | → 触发 cc-kb 记录 pattern (不中断主流程) |

**设计-实现小循环** (迭代是常态):

```
design(v1) → impl(发现问题) → design(v2) → impl(继续) → accept
                                     ↑              │
                                     └─ 回退≤3次 ───┘
```

同一功能回退 >3次 → 暂停，评估是否需求问题，回退 cc-req

### feat-accept 验收测试

#### 统一 DoD (Definition of Done)

```yaml
must_have:
  build: ["构建零错误"]
  typecheck: ["类型检查零 error (允许 deprecated 警告)"]
  test: ["单元测试100%通过", "核心路径覆盖率≥90%"]
  code_quality: ["Lint零error", "格式一致", "无console.log/debugger/TODO/HACK/FIXME残留"]
  documentation: ["公共API有JSDoc", "复杂逻辑有解释性注释(why not how)"]
  checklist_complete: ["impl-checklist.yaml 所有条目=done", "所有文件变更已记录"]
```

**不满足任一 must_have → ❌ 不通过**

#### 验收结果处理

| 结果 | 动作 |
|------|------|
| ✅ 通过 | `meta.status: done`; 更新REQ `status: implemented`; 同步roadmap |
| ❌ 不通过 | ↩ 回退 feat-impl 或 feat-design |

**验收后**: 触发 **cc-review**

---

## 内置安全检查点 (feat-impl阶段)

安全检查内嵌到实现流程中，编码完成后自动执行。

### OWASP Top 10 核心项

| # | 检查项 | 严重级别 |
|---|--------|---------|
| S1 | 输入验证与清洗 (XSS/SQL注入防护) | **Critical** |
| S2 | 认证与授权 (越权访问?) | **Critical** |
| S3 | 敏感数据处理 (明文密码/token?) | High |
| S4 | 依赖安全 (已知CVE?) | Medium |
| S5 | 错误信息泄露 (堆栈暴露?) | Medium |

### 结果处理

- ✅ 全部通过 → 进入 feat-accept
- ❌ 有 Critical/High 问题 → **阻止验收**，必须修复后重检

> 安全检查增量传递: cc-review Axis 2 将读取 `security_check` 字段跳过已通过项。详见 `cc/SKILL.md` § 安全检查增量传递。

---

## 输出规范

| 项目 | 格式 | 时机 |
|------|------|------|
| Feature 目录 | `features/{slug}YYYYMMDDHHMM/` | design开始 |
| 设计文档 | `{slug}-design.md` | feat-design完成 |
| 进度追踪 | `impl-checklist.yaml` | design创建，impl持续更新 |
| 审查报告 | `{slug}-review-report.yaml` | accept后由review-generate.mjs生成 |
