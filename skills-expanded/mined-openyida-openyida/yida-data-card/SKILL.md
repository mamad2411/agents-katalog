---
name: yida-data-card
description: 仅在用户明确要求操作宜搭原生数据卡片资源时使用，支持创建、读取、配置保存、发布及投放播报。自定义页面展示卡片、仅修改原生卡片引用外层及泛称卡片、指标卡、看板或播报不触发；已明确的原生卡片操作可继续沿用。
---

# 宜搭原生数据卡片

先核对用户是否显式选择本能力：明确要求“宜搭原生数据卡片”，或主动提供原生卡片管理、设计、投放链接并要求操作该资源；已明确的原生卡片上下文可继续沿用，无需重复确认。仅有“卡片、数据卡片、指标卡、看板、投放、数据播报、发送到群”等泛称，或环境中存在 CARD 资源，均不能自动触发。用户明确不使用原生卡片时不进入此技能；按实际页面、图表或自动化任务选择相应技能，意图仍不清楚时再澄清。

按用户选择、资源类型和配置归属区分同名“数据卡片”：

- 宜搭原生数据卡片是独立 `CARD-xxx` 资源，组件、数据集和布局归卡片 Schema，使用本技能保存、发布及配置播报。
- 宜搭原生酷卡片使用 `cardPageCode`、`cardTemplateId`，包含交互卡片 `im` 与置顶卡片 `onebox`，由独立 `yida-cool-card` Skill 处理。`dataCardDesigner.html?cardCode=CARD-...` 仍属原生数据卡片，不能因为用户口头叫“酷卡片”就切换接口。
- 自定义页面里的指标卡、统计卡是 Canvas/React 页面组件，随所属页面源码和页面发布；页面通常有 `FORM-xxx` 标识，仍需核实页面类型和源码。已有页面中新增展示卡片走页面开发，接真实数据走页面数据绑定，只改外观走现有 UI 改造流程，不自动创建 CARD 资源。
- 页面引用 `CARD-xxx` 时，页面是展示位置，原生卡片仍是独立资源。只改引用外层布局或页面配置，按页面任务处理；用户明确要求修改所引用卡片自身指标、数据源或布局时，才进入本技能。不因发现引用而获得修改源卡片的授权；不据此宣称已支持门户自动挂载。

不能仅扫描 ID 前缀判断操作对象：原生卡片也会引用 `FORM-xxx` 作为数据源，自定义页面也可能含 CARD 引用。缺少明确上下文时先澄清类型，不自动新建任何一种卡片。

多组件搭建先读 [图表配置与验收](references/chart-config.md)：支持九类原生组件、多指标、日期维度、同源下拉筛选和运行时探测；包含错误引导和当前能力缺口。

已满足上述原生卡片触发条件，再处理其投放、播报或使用记录时读 [投放与播报](references/release.md)。`publish` 不会启用播报；启用和测试发送还需明确发送授权。门户目前只支持使用记录查询与入口，不自动挂载组件。

先用 auth snapshot 核对目标组织和应用。已有 cardCode 时复用；用户要求新建时使用 create。卡片与表单、页面是不同资源，不调用 create-page 或 publish 页面命令替代。

## Skill 与 CLI 执行边界

- 应用搭建由本 Skill 编排，通过 OpenYida CLI 完成字段查询、卡片创建、组件配置、保存和发布。基础指标卡优先使用 `save --config`；完整配置使用 `save --schema`，由已核实的原生契约生成，不能要求用户先在浏览器拖拽出样本。
- 开发 OpenYida 能力时，可以用浏览器分析接口、参数、组件类型、配置选项和原生行为；核实后将可复用实现落入 CLI，并把操作方法、支持范围和验收规则写入 Skill。
- 正式搭建中的浏览器用于预览、原生可编辑性和真实取数验收。若某个组件或配置尚无 CLI 路径，明确说明缺口；在开发任务中补齐 CLI 与 Skill 后，再验证搭建，不用浏览器代替该步骤并宣称已支持。
- 验证记录区分浏览器调研、CLI 搭建和浏览器验收；全 CLI 搭建必须能从配置与真实元数据完成，不依赖本轮浏览器保存或临时控制台脚本。

## 配置入口

用户只询问配置位置时，执行下列只读命令并返回其中 `url`，不触发设置变更：

```bash
openyida app-settings APP_XXX --section theme --json
openyida app-settings APP_XXX --section basic --json
openyida app-settings APP_XXX --section data-card --json
```

三项依次为主题与导航、基础设置（业务前后台配置所在入口）、原生数据卡片管理。使用实际应用的返回地址，不固定示例域名或应用。地址生成不证明接收者拥有管理权限。

## 卡片操作

```bash
openyida data-card list APP_XXX --size 50 --json
openyida data-card create APP_XXX --name '销售数据卡片' --out .cache/openyida/data-card/new.json --json
openyida data-card get APP_XXX CARD-xxx --out .cache/openyida/data-card/draft.json --json
openyida data-card save APP_XXX CARD-xxx --config .cache/openyida/data-card/indicators.json --expected-hash <get返回的schemaHash> --json
openyida data-card publish APP_XXX CARD-xxx --expected-hash <最新草稿schemaHash> --json
openyida data-card get APP_XXX CARD-xxx --published --json
openyida data-card probe APP_XXX CARD-xxx --published --json
```

`get` 默认读取草稿，可通过 `--version` 读取指定版本。输出 `card.schemaBody` 为完整配置，`--out` 单独导出该 Schema；输出文件已存在时拒绝覆盖。平台初始 Schema 可以没有 schemaType/schemaVersion，保留其实际结构。

使用 `--schema` 保存是完整 Schema 替换：在本次读取的副本上编辑，保留未知键、pages、动作、组件映射、数据集和多语言引用。保存和发布都要求原始草稿摘要，写前自动备份并再次读取检查；平台没有原子锁，摘要不是并发事务。`backupPath` 可用于恢复前取证；不要无条件覆盖发生变化的卡片。

原生组件使用 Youshu 图表、基础指标卡、基础表格、下拉或时间筛选等物料。数据在 `props.dataSetModelMap` 及 `dataViewQueryModel`，样式在 `settings`。字段与数据集引用必须来自真实配置或已核实元数据；不根据展示名称臆造 cubeCode 或字段 ID。开启筛选涉及头部及筛选容器节点和联动引用，不是添加任意 enableFilter 键。支持完整 Schema 读写不等于已经支持任意自然语言自动生成图表。

`config.i18nKeyList` 与组件内词条引用一起保留；词条集合改变时 CLI 在保存前同步 dataCard 词条绑定。绑定成功、草稿写入失败时保留备份并核对远程状态，不盲目重放。

## 完成证据

- create 必须返回真实 cardCode 并读取其初始配置；创建空壳不等于配置完成。
- save 必须返回 `readbackVerified=true`；它只证明草稿配置回读一致，不证明发布成功。`published=false` 表示本次操作没有发布，不表示平台一定没有旧发布版。
- publish 发布当前已保存草稿，不自动读取并保存本地文件；必须返回 `published=true`、发布版本及已发布 Schema 回读证据。
- `urls.designerUrl/previewUrl/dataCardManageUrl` 可用于验收；渲染、编辑和真实取数需分别验证。

写请求不自动重放。创建超时或回读失败时先按返回 cardCode 或列表核对，不能直接再次新建。权限、卡片数量和图表数量权益失败时保留平台错误码，建议管理员处理或升级；不修改应用标记、版本、额度或权益。卡片发布不包含播报，播报使用独立 release 命令；不包含删除。


## 通过 CLI 搭建指标卡

创建、读取、配置保存和发布默认通过 CLI 完成，浏览器用于最终查看与编辑验收。新卡片无需先在浏览器拖拽生成 Schema。先用 `get-schema APP_XXX FORM-xxx --field-map-json` 核对真实字段，再准备配置文件：

```json
{
  "indicators": [{
    "title": "报名统计",
    "formUuid": "FORM-真实表单ID",
    "fieldId": "serialNumberField_真实字段ID",
    "aggregate": "COUNT",
    "label": "报名总数"
  }]
}
```

```bash
openyida data-card save APP_XXX CARD-xxx --config indicators.json --expected-hash <当前草稿schemaHash> --json
```

`--config` 与 `--schema` 二选一。上例 indicators 是兼容格式；复杂卡片使用参考文档中的 charts/filters 格式。CLI 校验真实字段，生成原生组件、查询模型、组件映射和布局，追加到当前卡片并保存草稿；已有组件及未知配置保留，再次保存相同配置会再次追加。单卡现有加新增最多五个图表。数字字段支持 COUNT/SUM/AVG/MIN/MAX；文本计数、分类维度和日期粒度按参考文档约束。子表、跨源筛选和未注册组件明确拒绝；权限和权益仍由平台校验，失败停止，不更改应用标记或额度。
