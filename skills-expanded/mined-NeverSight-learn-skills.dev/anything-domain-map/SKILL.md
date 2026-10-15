---
name: anything-domain-map
description: 为任意领域生成面向所有人的全链路知识地图，覆盖模块、可选主题/章节和知识点，以及客观依赖、应用、边界与来源。产出 domain-map.json、domain-map.md、domain-map.html、validation.md。当用户要领域全貌、完整知识体系、全链路大纲、知识地图、domain map，而不是个人学习路线时使用。
---

# anything-domain-map

生成与具体学习者无关的公共领域地图。核心目标是让人先看见全局，再决定自己的路线。

## 不可违背

1. **公共地图不是个人课程**：不根据某位学习者删减领域，不生成个人能力或进度。
2. **完整等于边界清楚**：覆盖基础、核心、主要分支、典型应用、相邻接口和前沿；不追求无限细节。
3. **结构有证据**：优先消费 `anything-research` 的领域制图卷宗；所有进入正式产物的 URL 必须实际打开验证。
4. **层级服从知识内聚**：结构固定为 `模块 →〔主题〕→〔章节〕→ 知识点`。模块和知识点必有，主题/章节仅在能聚合至少两个有意义子项时出现。
5. **一个机器正本**：先完成并验证 `domain-map.json`，再由它生成 Markdown 与 HTML，禁止三份内容分别编造。
6. **典型顺序不是个人路线**：可给客观依赖和典型遍历顺序，但必须显式声明不针对任何学习者。
7. **产品功能可见**：软件、平台或工具的正式用户入口是公共地图的一等对象；不能用宽泛的能力分类掩盖可配置、可调用、可观察的具体功能。
8. **稳定结构与当前状态并存**：地图既要呈现领域长期有效的知识结构，也要呈现截至明确日期的最新基线、近期变化和生命周期；新消息不能冲掉稳定依赖，旧路径也不能冒充当前默认。

## 输入

调用：`/anything-domain-map <领域> [范围说明]`

领域有实质歧义时问一个范围问题。若范围仍宽，采用主流定义，并把包含/排除项写入地图；不要向用户索取学习背景，因为本 skill 与个人背景无关。

## 工作流

### 1. 获取证据

- 优先寻找同领域、仍在有效期内的领域制图 `research.md`。
- 没有时，若 `anything-research` 可用，以“领域制图模式、深度=深”调用它，并要求两个独立研究轨：一轨深挖领域边界、稳定知识结构、依赖与主要分支；另一轨深挖截至当前日期的现行基线、最新变化、废弃迁移和生态动态。
- 已有卷宗只有稳定结构、只有一次最新功能扫描，或其 `as_of` 已不符合领域变化速度时，先让 `anything-research` 补齐或刷新第 8 节，不能直接制图。
- 第 8.4 节“最新知识点候选处置表”是入图门禁：每个候选必须有证据和唯一处置；空表、占位内容或只列版本事件的卷宗不可用于正式制图。
- 底层联网工具只是被 research 层使用的资料访问路由，不是领域地图的研究入口，也不应直接替代 research dossier；面向用户只报告 research 层的证据进展。
- research 不可用时自行完成同等调研，并在 `validation.md` 声明降级。
- 结构来源优先级：官方知识体系/标准 → 大学培养方案与课程群 → 权威教材目录 → 专业组织知识体 → 多条高质量课程路线的共识。

### 2. 划定边界

写清领域定义、包含项、排除项、相邻接口和时效截止日。若同名异义未解决，不进入制图。

同时声明当前信息基线：`as_of`、最新信息窗口、当前稳定版本/现行规范（适用时）以及变化速度。快速变化领域不得省略。

### 3. 建模

阅读 [references/domain-map-schema.md](references/domain-map-schema.md)，先构建 `domain-map.json`：

- 模块按领域结构而非学习周次划分；
- 知识点是展示叶子；
- 跨模块关系放 `relationships`，不靠重复节点表达；
- 每个知识点记录为何重要、解决什么问题、应用和来源；
- 使用稳定 ID；显示名变化不应改变 ID；
- `typical_traversal` 只表达一种常见浏览顺序。

若领域对象是持续更新的软件、平台或产品，再执行产品功能面盘点：

- 对照官方 README、文档导航、CLI/API 公开入口、版本说明与源码中的用户入口；
- 将可直接配置、调用、观察结果或排障的功能建成独立知识点；
- 保留功能之间以及功能与底层概念之间的依赖；
- 不用“自动化”“集成”“高级功能”等总括节点替代具体功能；
- 在 `validation.md` 记录核验日期、尚未覆盖的实验性功能和版本差异。

把最新研究轨落实到地图：稳定、实验性、废弃、移除和计划中内容必须明确区分；已废弃或移除的路径可为迁移而保留，但不能作为典型遍历的默认入口；未经证实的“最新”说法只进入缺口，不进入正式节点事实。

逐项消费最新知识点候选处置表：`新增节点`、`修改节点`、`降级/移除` 和 `仅作关系变化` 必须反映到 JSON 正本；`排除` 和 `待验证` 必须写入 `validation.md` 并保留理由。任何会改变用户行为、心智模型、依赖、适用边界或验证标准的已证实变化都不能只留在“近期变化”附录。

### 4. 验证结构化正本

运行：

```bash
python scripts/validate_domain_map.py <项目根目录>/anything-domain-map/domain-map.json
```

修复所有 error 后再渲染。warning 必须在 `validation.md` 解释或修复。

### 5. 生成四个产物

复用 research 所在的学习项目根目录；若单独调用且不存在项目根目录，则创建 `./<project-slug>-learning/`。本 skill 只写：

```text
<project-slug>-learning/
└─ anything-domain-map/
   ├─ domain-map.json
   ├─ domain-map.md
   ├─ domain-map.html
   └─ validation.md
```

不要再创建独立的 `<domain>-domain-map-<version>/` 同级目录。版本保存在 `domain-map.json` 内；`research_ref.path` 使用 `../anything-research/research.md`。

- `domain-map.json`：机器正本。
- `domain-map.md`：按 [references/domain-map-template.md](references/domain-map-template.md) 生成的人类可审阅全链路大纲。
- `domain-map.html`：复制 `references/template.html`，用脚本嵌入 JSON：

```bash
python scripts/render_domain_map.py <项目根目录>/anything-domain-map/domain-map.json <项目根目录>/anything-domain-map/domain-map.html
```

- `validation.md`：按 [references/validation-template.md](references/validation-template.md) 记录事实、来源、结构、覆盖、渲染检查和缺口。

### 6. 验收

- JSON 校验通过；
- Markdown 与 HTML 的模块数、知识点数、ID 和来源数与 JSON 一致；
- 所有中间层至少有两个子项；
- 所有关系端点和来源引用存在；
- HTML 单文件、零 CDN、键盘可操作、支持窄屏/打印/`prefers-reduced-motion`；
- 用户能从总览逐层下钻到知识点，并可单独查看跨模块关系；
- `validation.md` 坦白覆盖边界、低置信结构和信息缺口。
- 产品型地图已对照官方功能面，所有影响日常工作流、权限或结果投递的正式入口均可见。
- `validation.md` 写明 `as_of` 和最新信息窗口；稳定结构轨与最新状态轨均有多轮证据，当前基线、近期变化、废弃/迁移及未证实说法均已处理。

交付时列出四个文件的绝对路径。不要替用户生成个人路线；那属于 `anything-roadmap`。
