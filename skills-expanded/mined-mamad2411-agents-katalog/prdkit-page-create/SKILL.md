---
name: prdkit-page-create
description: 当用户提出创建原型、起原型、生成页面原型、搭建移动端原型、搭建 PC 后台原型。该 skill 采用两阶段流程：先生成方案文档等待用户确认，再创建原型。
allowed-tools:
  - Read
  - Grep
  - Glob
  - LS
  - AskQuestion
  - Bash(command -v prdkit)
  - Bash(prdkit info*)
  - Bash(prdkit init*)
  - Bash(prdkit prototype create*)
  - Bash(prdkit prototype list*)
  - Bash(prdkit serve*)
  - Bash(npm install -g @huangqz/prdkit-cli*)
  - Bash(rm *)
  - Edit
  - MultiEdit
  - Write
---

# 创建页面原型

## 工作流程

### 两阶段流程

采用两阶段流程确保方案准确：

#### 第一阶段：生成方案文档

1. **检查环境和项目状态**：
   - 运行 `command -v prdkit` 和 `prdkit info`
   - 如果需要，安装 CLI 或初始化项目

2. **读取项目上下文**：
   - `context/`、`draft/`
   - 已有 `workspace/prototypes/`
   - 相关的 `workspace/prds/` 或 `workspace/discussions/`

3. **分析需求来源并分类**：
   - **文字描述**：使用 `AskQuestion` 工具确认需求细节
   - **有参考截图/页面**：先判断是"完全复刻"还是"参考设计"
     - **完全复刻**：布局、文案、样式都要保持一致 → 重点确认还原细节
     - **参考设计**：只参考样式和布局，内容可调整 → 重点确认业务逻辑

4. **使用 `AskQuestion` 工具确认需求**：
   - 参考 [references/phase-1-requirements.md](references/phase-1-requirements.md)
   - 提出 3-4 个高信息密度问题
   - 优先确认平台类型：`mobile` / `admin` / `web`
   - **完全复刻场景**：
     - 第一个问题必须确认：是否需要保持文案、布局、样式完全一致？
     - 重点确认：页面结构、元素顺序、文案内容、视觉参数（颜色、间距、圆角）
     - 让用户按从上到下的顺序描述页面元素
   - **参考设计场景**：重点确认布局结构、交互逻辑、数据层级

5. **生成方案文档**：
   - 保存到 `draft/reference/<title>-prototype-plan.md`
   - 包含：任务清单、已确认信息、当前假设、待确认项
   - 包含：ASCII 线框图、交互说明
   - 包含：视觉样式参数、画布规格
   - **完全复刻场景**：必须包含详细的元素清单（文案、颜色、间距、圆角等）和 wireframe
   - **参考设计场景**：必须包含从参考中提取的结构分析和 wireframe
   - 明确标注”当前处于第一阶段，尚未创建页面”和需求类型（完全复刻/参考设计/文字描述）

6. **停止并等待用户确认**

#### 第二阶段：创建页面

6. **用户确认方案后，执行创建**：
   ```bash
   prdkit prototype create “<title>” --template <platform> --dir ./workspace/prototypes
   ```

7. **按方案文档补充内容**：
   - 页面结构、交互逻辑、mock 数据
   - 参考 [references/phase-3-implementation.md](references/phase-3-implementation.md)

8. **创建 checkpoint**：
   ```bash
   prdkit checkpoint create
   ```

9. **清理临时文档**：
   - 删除 `draft/reference/<title>-prototype-plan.md`

10. **引导预览**：
    - 检查并启动预览服务器

## 命令映射

- 移动端 App / H5：

```bash
prdkit prototype create "<title>" --template mobile --dir ./workspace/prototypes
```

- PC 后台 / 工作台 / 仪表盘：

```bash
prdkit prototype create "<title>" --template admin --dir ./workspace/prototypes
```

- 通用 Web 页面：

```bash
prdkit prototype create "<title>" --template web --dir ./workspace/prototypes
```

可选补充命令：

```bash
prdkit prototype list
prdkit serve
```

## 方案文档格式

第一阶段的方案记录保存到 `draft/reference/<title>-prototype-plan.md`，复用 references 中的格式模板。

## 约束规则

**流程控制**
- 第一阶段必须落盘方案文档并暂停，等用户确认后再继续
- 项目未初始化时，先完成初始化再执行原型命令

**交互要求**
- 必须使用 `AskQuestion` 工具提问
- 任务计划使用 `TodoWrite` 工具呈现
- 问题应短、准、高信息密度，避免宽泛开放式提问

**技术规范**
- 显式指定模板，不依赖默认值
- 默认尺寸：`mobile` 用 `390 x 844`，`admin/web` 用 `1440 x 900`
- **样式框架**：使用 Tailwind CSS（CDN 引入），优先使用工具类而非自定义 CSS
- **图标库**：使用 Font Awesome（CDN 引入），不使用其他图标库
- 参考 `phase-3-implementation.md` 的画布、圆角、弹窗和 `z-index` 规则
- 页面内部不使用 `z-index: 9999`（预留给 viewer）
- 数据结构：每页一个 `mock.js`，`script.js` 只消费数据
- ASCII 线框图只确认结构，保持简洁易读
- **图片占位**：禁止使用真实图片链接（unsplash、placeholder.com 等），统一使用纯色背景 + 文字标注的方式占位

## 决策树

```
用户需求
    │
    └─ 两阶段流程
        │
        ├─ 第一阶段：生成方案文档
        │   ├─ 检查环境和项目状态
        │   ├─ 读取项目上下文
        │   ├─ 使用 AskQuestion 确认需求
        │   ├─ 生成方案文档到 draft/reference/
        │   └─ 停止并等待用户确认
        │
        └─ 第二阶段：创建页面（用户确认后）
            ├─ 执行 prdkit prototype create
            ├─ 按方案文档补充内容
            ├─ 创建 checkpoint
            ├─ 清理临时文档
            └─ 引导预览
```

## 资源说明

### references/

- `phase-1-requirements.md`：需求澄清阶段的提问模板和确认记录格式
- `phase-2-wireframes.md`：结构确认阶段的 ASCII 线框图模板和交互说明要求
- `phase-3-implementation.md`：实现阶段的视觉参数、画布规范、Tailwind CSS 使用指南、Font Awesome 图标规范、图片占位方案
