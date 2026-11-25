---
name: lsdyna-kfile
description: 生成独立 LS-DYNA 关键字卡片，或编写、修改、调试、试算和验证 `.k`/`.key`/`.dyn` deck；覆盖材料、EOS、碰撞、跌落、侵彻、成形、ALE、SPH 等需求。
---

# LS-DYNA K 文件编写与自动验证

完整模型交付物只能是**经本机求解器实际计算验证的完整 k 文件和验证报告**，不可“写完就交”。
仅要求独立关键字卡片时走下述极简模式，只承诺 L0 静态检查。
以下把本文件所在目录称为 `SKILL_DIR`；脚本、知识、协议和模板分别位于 `SKILL_DIR/scripts/`、
`SKILL_DIR/knowledge/`、`SKILL_DIR/references/`、`SKILL_DIR/templates/`。

## 1. 路由与环境

- **极简模式（优先路由）**：用户明确只要一个或少量独立关键字卡片/片段（如 `*MAT_*`、
  `*EOS_*`），且不要求完整模型、修改现有 deck 或试算时启用。直接生成目标卡片，按要求交付文本
  或 `.k` 文件；不走任务书确认、模板/基准检索、M0~M3、L1/L2、求解器或 §5 完整报告。
  参数优先取用户给定值和本地资料，用 `units.py` 核对换算、用 `kfile-format.md` 或手册核对字段；
  缺少参数时可按 `references/literature-parameter-routing.md` 的参数检索链路按需联网，但不触发
  完整模型的强制基准/文献双链路。除非用户明确要求记录来源，不创建 `spec.md`、
  `research/literature-evidence.json` 或文献来源清单；关键值无可靠依据就询问，不编造。
  将卡片置于临时 `*KEYWORD`/`*END` 包裹的独立文件，以
  `python "SKILL_DIR/scripts/check_kfile.py" fragment.k --fragment` 做 L0，要求 0 errors；
  仅用户要求文件时保留 `.k`，否则交付卡片文本。若卡片依赖未提供的外部模型实体，
  不虚构配套模型；说明引用检查结果及静态检查覆盖边界。简要报告单位制、假设、
  L0 errors/warnings 和未验证项，不把 L0 PASS 称为求解器验证或参数标定。
- **模板制作模式**：用户上传主 `.k`/`.key`/`.dyn`，明确说明其要作为某类模板，并要求抽象、整理、
  参数化或沉淀。优先执行 `references/template-authoring-protocol.md`；先运行
  `python "SKILL_DIR/scripts/prepare_existing_deck.py" user_model.k --outdir template_build/<模板名称> --objective "制作 <模板用途> 模板"`，
  将源文件和 include 闭包置于只读 `source/`，只在独立 `working/`（候选模板）与 `validation/` 目录工作。
  该模式必须先完成结构化分析和模板适用性判断；会影响模板物理、参数接口或验收结论的问题，整个请求
  最多集中询问 5 个关键问题。问题未回答前不得抽象最终模板或进行最终 L2 验证；用户确认后才写入
  `template_spec.md`、`NOTES.md` 和模板文件。来源 deck 的验证结果不可直接替代模板候选的重新验证。
- **已有 deck 模式**：用户提供主 `.k`/`.key`/`.dyn` 并要求修改、调试、运行或修复。跳过 §1 需求头脑风暴、
  `spec.md` 确认、模板/基准/学术门和新建流程，执行 `references/existing-deck-repair.md`；仍须做
  环境检查、`knowledge/errors.md` 预检、L0/L1/L2、§5 交付报告和经验追加。无 `spec.md` 时保持
  原 deck 的物理意图，仅解决用户目标范围的问题。先运行
  `python "SKILL_DIR/scripts/prepare_existing_deck.py" user_model.k --objective "用户目标"`，不得直接修改原文件。
- **新建 deck 模式**：无可用主 deck 或要求重新建模，执行 §2-§5。

完整模型模式会话首次运行：

```bash
python "SKILL_DIR/scripts/kagent_config.py"
```

默认求解器为 `C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64`（LS-DYNA R14.1.1）；用
`LSDYNA_BIN`、`LSDYNA_MPIEXEC` 或 `~/.lsdyna-kagent.json` 覆盖。不得使用 R14 之后才支持的关键字或字段。
凡标注 R15 及以上的功能一律回避。手册缺失时运行 `python "SKILL_DIR/scripts/fetch_manuals.py"`。

## 2. 新建 deck：任务书与基准门

读取 `references/brainstorm-protocol.md`。它是 12 项收敛清单、6 类工况问题库、`spec.md` 模板、
模板适用性和文献/官方基准门的唯一细则。

1. 缺 7 项关键输入（工况、目的/输出、几何/尺寸、材料、边界、初始条件、单位制）时，最多 5 轮、
   每轮最多 4 个问题，按工况→物理→数值提问；给 2-4 个推荐选项。用户说“你定”时采用推荐值并标
   `[默认]`。用户未指定单位制时默认 `mm-ton-s` 并声明；每轮做量级检查和收敛面板。
2. 在选模板、生成网格、写任何卡前读取 `knowledge/errors.md`，将命中项写为预防检查；无命中也记录。
   L0 前逐项核对；仅在新症状或预检未覆盖时重查。
3. 完成模板适用性判断和基准方案。**模板目录存在不等于模板可用**：只有物理机制、建模方法、主要载荷/
   边界、关注输出均能支撑当前骨架时可用；否则是无适用模板。
   **无适用模板时，必须先完成 LS-DYNA 官方资料/官方算例检索和学术文献检索**，
   不得用普通网页搜索、既有经验或相邻模板直接替代该双链路；
   触发学术检索时必须有
   `research/literature-evidence.json` 和任务书文献摘要。爆炸焊接、界面波、飞板碰撞、爆轰耦合、
   热-塑性-失效耦合且无专用模板时默认无适用模板。
4. 模板速查：跌落 `templates/drop/`（mm-ton-s）、碰撞/压溃 `templates/crash/`（mm-ton-s）、侵彻
   `templates/penetration/`（cm-g-us）、成形 `templates/forming/`（mm-ton-s）、ALE `templates/ale/`
   （m-kg-s）、SPH `templates/sph/`（mm-kg-ms）。无相似案例时标 `no-similar-case`，按任务书的
   `M0~M3` 阶梯：M0 最小模型→M1 材料→M2 相互作用→M3 完整模型逐步验证。M0 先过 L0/L1 并核对单位、时间步和运动
   方向；M1 用单单元/简化试件核对本构、失效/EOS、趋势或标定点；M2 检查穿透、初始间隙、反力、
   能量传递和约束；M3 每次只增加一类复杂度并重跑 L0/L1，全部集成后才做 L2。关键无证据参数需给出
   范围并做敏感性分析，报告参数区间、响应区间和结论稳定性。
5. 将完整任务书写为工作目录 `spec.md`，状态“待用户确认”，展示内容和路径并问“按此任务书执行？”。
   **在收到用户明确同意前停止：不得生成、复制、修改或运行任何最终 `.k` 文件、网格 include 或写卡脚本，
   也不得进入资料补全或生成阶段。** 修改请求只更新 `spec.md` 后重新确认；同意后标“已确认（日期）”。
   这是全流程唯一一次强制确认。无人值守才可不阻塞，所有缺项标 `[假设]` 并在最终报告显著提示。

单位制速查：`python "SKILL_DIR/scripts/units.py" list`。

基准后只补齐写卡细节：读取模板 `NOTES.md`，材料一律用
`python "SKILL_DIR/scripts/units.py" material <system> <name>`，不得手抄换算；字段不确定时运行
`python "SKILL_DIR/scripts/manual_index.py" find <KEYWORD>`，再
`python "SKILL_DIR/scripts/manual_index.py" read <KEYWORD>` 直接输出该关键字的手册页文本，
不得跳过字段核实。CONTACT_* 查询会命中变体子索引（共享卡页 + 变体专属 Card 4），
不再是 139 页整章区间。仅在证据缺口、资料冲突或新增明确
文献请求时按 `references/literature-parameter-routing.md` 联网；文献工程输入与求解器专属问题不可互换链路。

## 3. 建模

格式、字段、特殊列宽和建模惯例以 `references/kfile-format.md` 为准。**固定格式数据卡一律优先用
`python "SKILL_DIR/scripts/write_card.py" --spec <spec.json> [-o deck.k --append]` 从 JSON 生成**
（spec 每卡是字段值数组，int/float/`null` 留空/字符串原样；`--fmt free` 出逗号格式），脚本自带
列宽对齐自校验，写卡与 L0 用同一套仲裁规则，从根上杜绝手拼列宽错位；手工写卡仅限调试，
且必须过 L0。用 `$ ==== CONTROL ====` 等横幅分节，
按 CONTROL→DATABASE→MATERIALS→
SECTIONS/PARTS→MESH INCLUDES→CONTACT→BOUNDARY/INITIAL→LOADS 组织，并以 `*END` 收尾；每张卡前加 `$#`
字段名。部件 n：`PID=SECID=MID=n`，`nid0=eid0=n*100000`，节点集 `sid0=n*10`，曲线从 901、part set 从 801。

无一例外包含：`*KEYWORD`、`*TITLE`、`*CONTROL_TERMINATION (ENDTIM)`、
`*CONTROL_ENERGY (HGEN=2 RWEN=2 SLNTEN=2 RYLEN=2)`、`*CONTROL_TIMESTEP (TSSFAC=0.9；准静态加 DT2MS)`、
`*DATABASE_GLSTAT (dt≈ENDTIM/200)`、`*DATABASE_MATSUM`、`*DATABASE_BINARY_D3PLOT (dt≈ENDTIM/20)`、`*END`。

简单几何用 `gen_mesh.py` 的 `plate / box / cylinder / cylshell / sphere / sphbox / sphcyl`，圆柱类支持
`--axis x|y|z`；保留 JSON 摘要并用其中的 ID 范围和集合号编写 SPC/接触。
复杂几何向用户索取含 `*NODE/*ELEMENT` 的 `.k` 网格。示例：

```bash
python "SKILL_DIR/scripts/gen_mesh.py" plate --plane xy --origin -75 -75 0 \
  --size 150 150 --div 30 30 --pid 1 --nid0 100000 --eid0 100000 --sid0 10 -o mesh_plate.k
```

## 4. L0/L1/L2 验证和修复

在专用工作目录用 `verify.py` 一条命令逐级验证（L1 试算天然豁免 G7，L2 自动读取 deck 的
ENDTIM 并启用 `endtim_reached` 门；license 失败自动按 `--retries 2 --retry-delay 60` 重试）：

```bash
python "SKILL_DIR/scripts/verify.py" l0 model.k
python "SKILL_DIR/scripts/verify.py" l1 model.k --endcyc 50 --ncpu 4 --timeout 300
python "SKILL_DIR/scripts/verify.py" l2 model.k --ncpu 4 --timeout 1800 --json report.json
```

摘要输出 ≤ 15 行（verdict、各门槛、关键指标、首要错误）；完整 JSON 只写 `--json` 文件。
底层命令仍可单独使用：`check_kfile.py` / `run_dyna.py [--endcyc|--endtim]` / `parse_results.py`。

L0 必须 0 errors（S-ALE 求解器生成网格的 `PART has no elements` warning 可接受）；L1 通过后删除自动生成的
`model_trial.k`。L2 的 G1-G7 和工况例外仅按 `references/quality-gates.md` 判定。

- `FAIL` 必修：查手册/官方资料，改后从 L0 重跑；最多 8 轮，未修复则如实交代症状和尝试。
- `WARN` 必须在报告中给出量化物理解释。
- 修复触及 `spec.md` 契约（网格、ENDTIM、材料、几何简化）时，交互可用则更新任务书并向用户确认；
  无人值守则采用推荐方案、升格 `[假设]` 并显著报告。
- 任何求解/读卡错误、WARN 修复或新建模坑修复成功后，向 `knowledge/errors.md` 经验追加区记录
  症状/原因/修法/日期，再交付。

大模型可用 `--mode mpp --ncpu 8`，MPP 内存为每进程；并发多任务时各 `--ncpu 2`。license 失败由
`run_dyna.py`/`verify.py` 自动等待重试（默认 60 s、2 次），无须人工重跑。默认单精度 `sp`；需要精度
复核的侵彻/爆炸用 `--precision dp`。`run_dyna.py` 会在重跑前清理旧结果，
手动重跑时避免解析陈旧 `glstat`。用户网格先单独 `check_kfile.py`。带空格路径（如 `K AGENT`、
`Program Files`）必须加引号。Final 前只保留最终主 deck 与实际 `*INCLUDE` 的网格/子模型。

## 5. 最终交付报告

完成验证、清理和经验追加门后，先写 `final_delivery_report.md`，
再向用户发送一份同内容或等价摘要的“最终交付报告”；在报告写入并发送前不得结束任务或只回复“已完成”。
路径必须是最终保留产物，数值只能
来自本次最终 `report.json`、`run.log` 和求解器输出；缺失数据写“未获得”及原因，不得猜测或沿用试算值。

报告必须包含：

1. 最终主 k、实际 mesh include、`spec.md`、验证 JSON/日志、`final_delivery_report.md` 路径。
2. L0/L1/L2、verdict、termination、能量比、沙漏比、附加质量、单元数、耗时、求解器版本。
3. 已确认 `spec.md` 第 6 节验收标准逐条的通过/未通过/未获得及证据。
4. 单位制、材料来源、简化、约束、摩擦和全部 `[假设]`。
5. 触发文献检索时的证据字段、每篇标题/DOI 和 `research/literature-evidence.json`；说明文献值不等于实测值。
6. 改速度/尺寸/材料应修改的卡。
7. 所有 WARN/FAIL、可信度限制和未完成验证；无遗留项也写“无”。
