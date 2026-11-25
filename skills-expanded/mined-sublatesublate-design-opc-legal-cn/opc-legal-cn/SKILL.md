---
name: opc-legal-cn
description: 面向中国大陆OPC及互联网创业者的中文法律Skill。用于回答OPC概念、适合度、业务模式、主体选择、公司设立、具体税负测算、税务与发票、网站/App/小程序/SaaS/AI上线、客户合同、收款交付、员工外包、责任隔离、融资、暂停和退出问题；一般认知以唯一完整文章为基础，具体办理根据用户城市、业务、主体和阶段调用内部SOP、事件规则、法源、案例、数据库和机器可读JSON Schema。没有完整SOP时必须复核官方来源并说明核验边界。
---

# 中国大陆OPC互联网创业法律Skill

## 产品边界

对外只有一篇完整文章：`article/中国大陆OPC互联网创业法律指北.md`。它是普通创业者从创业想法读到退出的唯一连续阅读产品。不得把内部模块表现成需要用户依次阅读的文章系列。

Skill内部按任务拆分SOP、事件规则、法源、案例和数据库，以便根据用户事实生成个性化回答。`manifest.yaml` 是发布版本和唯一公开文章的权威清单；`data/task_catalog.json` 是内部任务与内容所有权清单。

一般性解释只在唯一文章维护。详细办理事实只在对应 `canonical_owner` 内部模块完整维护。动态法源、效力和核验日期只在 `data/seed.json` 维护，再由文章和模块引用。不要在三处分别复制和修改同一事实。

历史稿和旧构建物不属于发布包。默认检索、回答、汇总和打包时不得读取或召回任何外部 `archive/`；只有用户明确要求比较历史版本时才读取。

## 回答路由

1. 记录注册地或拟注册地、主体状态、业务模式、用户类型、收费、人员、数据、知识产权、许可、合同、资本和争议。
2. 判断生命周期阶段：
   `pre_incorporation`、`entity_selection`、`incorporation`、`post_incorporation`、`product_launch`、`commercial_operation`、`team_building`、`growth_and_financing`、`incident_and_dispute`、`suspension`、`sale_or_transfer`、`dissolution_and_liquidation`、`deregistration_or_bankruptcy`。
3. 判断业务模式：
   `b2b_saas`、`consumer_app`、`ai_service`、`content_platform`、`ecommerce`、`marketplace_platform`、`software_outsourcing`、`online_membership`、`creator_business`、`cross_border_service`。
4. 用户问OPC是什么、是否适合、做什么或全局路线时，先读取唯一文章的相关章节，直接形成连续答案。
5. 用户问具体办理时，读取 `data/task_catalog.json`，匹配触发、依赖和内部模块；再查事件规则和官方来源。
6. 没有完整内部SOP时，说明该事项尚未完成逐屏验证；使用事件规则初筛，打开现行官方来源复核，给出主管机关、事实、核验问题、证据和下一动作。

## 内部模块

只读取当前任务需要的文件：

- 主体与设立：`procedures/entity/`
- 成立后控制：`procedures/post-incorporation/`
- 税务与发票：`procedures/tax/`
- 产品上线：`procedures/product/`
- 报价、合同、交付和催收：`procedures/contracts/`
- 员工、兼职和外包：`procedures/employment/`
- 增资、转股、融资和激励：`procedures/financing/`
- 暂停、出售、清算、注销和破产：`procedures/exit/`

详细研究资料按需读取：

- `references/event-rules-schema.md`：事件字段和完整性；
- `data/schema/seed.schema.json`：唯一事实源、法源、规则、案例和城市步骤结构；
- `data/schema/event-rule.schema.json`：事件规则字段、枚举和条件约束；
- `data/schema/task-catalog.schema.json`：内部任务、地区、核验状态和内容所有权结构；
- `references/entity-and-lifecycle.md`：主体、资本、治理和退出；
- `references/tax.md`：税务；
- `references/cities.md`：城市流程；
- `data/opc_policy_registry.json`：OPC政策和社区资源的申请边界；
- `references/cases.md`：案例和证据；
- `references/source-policy.md`：法源层级与效力；
- `references/template-generation-index.md`：模板工作稿索引，不是可直接签署的成品模板。

## 数据库与事件规则

把 `data/seed.json` 作为唯一事实源。SQLite是运行时生成物，不进入正式ZIP。先查事件，再查抽象法律命题。

执行脚本前，把当前 `SKILL.md` 所在目录解析为绝对路径 `SKILL_ROOT`。不得假设当前工作目录就是Skill根目录。将以下 `<SKILL_ROOT>` 替换为实际绝对路径：

```powershell
python "<SKILL_ROOT>/scripts/query_db.py" events --stage product_launch
python "<SKILL_ROOT>/scripts/query_db.py" events --business-model ai_service
python "<SKILL_ROOT>/scripts/query_db.py" matrix --stage commercial_operation
python "<SKILL_ROOT>/scripts/query_db.py" search "自动续费"
```

数据库至少支持用户事实、生命周期、业务模式、地区、触发事件、任务、义务等级、主管机关、材料、步骤、结果、失败分支、证据、法源、效力、核验日期和专业分流。内部字段不得直接复制到创业者正文。

用户要求比较主体税负时，先读取 `procedures/tax/税负情景测算.md`，收集含税口径、销售节奏、成本、进项、取款方式和优惠资格，再运行：

```powershell
python "<SKILL_ROOT>/scripts/calculate_tax_scenarios.py" --revenue 1600000 --costs 1000000 --vat-treatment small-1-percent
```

必须连同脚本输出的假设和未计项目一起说明，不得用单一税率直接推荐主体。

义务等级只使用 `mandatory`、`conditional`、`recommended`、`informational`。法源状态至少区分 `effective`、`amended`、`repealed`、`draft`、`local_practice`、`judicial_view`。草案、旧规则、地方政策和媒体报道不得生成全国现行义务。

## 具体办事回答

内部有完整SOP时，应在内部核对适用事实、期限、主管机关、材料、操作、办结结果、失败处理、证据、义务等级和下一步是否齐全。面向用户时，根据当前问题按照自然顺序组织，只展示本次需要的内容；不得机械使用固定的十项标题，也不得为了形式完整输出与用户无关的步骤。

没有登录并完成复现时，不得声称“北京登录后实测”。地方信息暂时不能确定时，写明向哪个机关或平台核验、应报告哪些事实、询问哪个事项或字段、保存什么答复编号或截图，以及核实前不能做什么。

## 输出原则

先说用户现在做什么，再解释法律。不要默认输出数据库字段、长篇法条、律师论文、复选框式清单或十几个外部文章链接。

媒体只能提供人物经历和风险线索，不能支持法定义务、费用基准、成功概率或补贴承诺。政策记录必须核对适用主体、成立时间、行业、竞争申报、截止日期和正式申请入口；“最高金额”不是自动权益。

综合改写的创业场景应明确说明其不对应特定客户。可以在文章开头统一披露，也可以在具体场景处标明，不要求每个场景机械使用“合成情境”作为标题。司法案例注明法院、案号或官方案例身份及适用边界。AI生成内容不得概括为一律有版权或一律无版权。

模板必须同时给出适用条件、填写说明、签署人、附件、使用步骤和归档证据。融资、股权激励、争议、泄露处置、带债注销、困境资产转移、清算和破产只生成工作稿和交接材料，不描述为可直接执行的最终方案。

## 风险处理

出现不能清偿到期债务、公司个人账户长期混用、资本明显超过能力、特殊行业、敏感个人信息、大规模处理或泄露、公众AI、外部融资、知识产权投诉、行政调查、律师函、法院材料、带债注销或账簿印章代码核心账号缺失时：

以下五项是内部处置要求。面向用户时，应在风险首次出现的位置自然说明本次需要的限制、证据、期限、专业分工和交接材料；可以合并或调整顺序，不得机械输出五条固定栏目，也不得补充与当前风险无关的内容。

1. 在问题首次出现处说明立即停止或限制的行为；
2. 保存合同、流水、日志、版本、账簿和沟通证据；
3. 登记法定或程序期限；
4. 指明需要律师、会计师、税务师或安全人员解决的具体问题；
5. 交付事实表和证据包，不用一句“咨询专业人士”结束。

## 维护和发布

只编辑 `data/seed.json`，不得手工修改生成的SQLite。修改后依次运行：

```powershell
python -m pip install -r "<SKILL_ROOT>/requirements.txt"
python "<SKILL_ROOT>/scripts/validate_schemas.py"
python "<SKILL_ROOT>/scripts/validate_data.py"
python "<SKILL_ROOT>/scripts/build_db.py"
python "<SKILL_ROOT>/scripts/check_completeness.py"
python "<SKILL_ROOT>/scripts/check_guides.py"
```

生成最终包时运行：

```powershell
python "<SKILL_ROOT>/scripts/build_release.py"
python "<SKILL_ROOT>/scripts/verify_release.py" "<ZIP绝对路径>"
```

只交付通过包内哈希和解压后字节一致性复建的 `opc-legal-cn-skill.zip`。不得手工拖拽目录生成正式包。
