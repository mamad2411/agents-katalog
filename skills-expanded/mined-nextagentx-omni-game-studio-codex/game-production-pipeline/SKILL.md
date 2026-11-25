---
name: game-production-pipeline
description: Run an end-to-end game production pipeline with hard stage gates — idea to brief, GDD, tech plan, art and audio specs, placeholder assets, a compilable project from templates, build verification, and release plan. Use when the user wants the whole flow from an idea to a shippable build, not just one document.
---

# 端到端游戏流水线

把一个想法推进到**可构建产物 + 发布方案**。每个阶段有固定工件、固定路径、可执行的门禁，不允许跳阶段。

以下角色是可选分工：仅在当前环境支持且允许委派时使用；否则由当前助手直接完成。按用户实际授权和项目阶段选择工作范围。状态脚本只检查文档标题和 TODO，不会自动检查资源、实际构建或真机验证；这些需要分别执行并记录结果。

制作的五阶段、G1–G5 里程碑、Sprint 循环和团队规模裁剪见 [references/production-cycle.md](references/production-cycle.md)。下表七个阶段是文档工件子门禁，与制作里程碑不是一一对应。

## 阶段与工件

| 阶段 | 产出 | 负责角色 |
|------|------|---------|
| `brief` | `docs/00-brief.md` 立项卡 | 制作人（你自己） |
| `gdd` | `docs/01-gdd.md` | `game-narrative-designer` |
| `tech` | `docs/02-tech.md` | `cocos-engineer`、`unity-engineer`、`godot-engineer` 或 `unreal-engineer` |
| `art` | `docs/03-art.md` + `docs/art-style-bible.md` + 正式美术 + `assets/manifest.json` | `game-art-director` |
| `audio` | `docs/04-audio.md` + 正式音频 | `game-audio-designer` |
| `qa` | `docs/05-qa.md` | `game-qa-engineer` |
| `release` | `docs/06-release.md` | `game-release-operator` |

骨架全部在插件的 `templates/docs/`，复制到项目的 `docs/` 再填。**骨架里的 `[TODO]` 不填完，门禁不放行。**

## 工具（插件自带，用 python 直接调）

脚本目录 = 本插件根下的 `scripts/`。若不确定绝对路径，先 `codex plugin list` 找到插件路径。

| 用途 | 命令 |
|------|------|
| 初始化状态 | `python scripts/omni_state.py init --root . --engine godot --platforms web,android` |
| 看阶段进度 | `python scripts/omni_state.py status --root .` |
| 校验单阶段 | `python scripts/omni_state.py check --root . --stage gdd` |
| 推进阶段（带门禁） | `python scripts/omni_state.py advance --root .` |
| 生成占位美术（仅验证管线） | `python scripts/gen_placeholder_art.py --manifest assets/manifest.json --root .` |
| 制作路线图 | 复制 `templates/docs/07-production-roadmap.md` 到 `docs/` |
| Sprint 计划与复盘 | 复制 `templates/docs/08-sprint-review.md`，每轮记录集成版本、测试和反馈 |
| 门禁评审 | 复制 `templates/docs/09-milestones.md`，记录 G1–G5 与上线后运营评审 |
| 正式图后处理 | `python scripts/process_art.py --in raw/x.png --out assets/art/x.png --size 256x64 --key-color "#FFFFFF" --check-nine --nine-slice 24` |
| AI 动画切帧 | `python scripts/split_sprite_sheet.py --input raw/sheet.png --cols 4 --rows 2 --fps 12 --loop --out-dir assets/animation/run --backup-dir doc/temp/run-frames` |
| AI 图片 / GIF | `python scripts/gen_ai_image.py --prompt "single game icon" --format png --out assets/art/icon.png --backup-dir doc/temp --dry-run` |
| AI 音效 | `python scripts/gen_ai_audio.py sfx --prompt "short sci-fi pickup" --duration 1 --out assets/audio/pickup.mp3` |
| AI 音乐 | `python scripts/gen_ai_audio.py music --prompt "gentle space exploration" --duration 30 --instrumental --out assets/audio/main.mp3` |
| 生成 BGM（chiptune） | `python scripts/gen_music.py --style upbeat --out assets/audio/bgm_main.wav --tempo 132 --bars 16` |
| 合成音效 | `python scripts/gen_sfx.py --preset hit --out assets/audio/sfx_hit.wav` |
| 音频压缩核算 | `python scripts/compress_audio.py --dir assets/audio --check` |
| 打包图集 | `python scripts/pack_atlas.py --input assets/art/ui --out-sheet assets/art/ui_atlas.png --out-data assets/art/ui_atlas.json` |
| 校验资源清单 | `python scripts/validate_assets.py --manifest assets/manifest.json --root .` |
| 发布前终检 | `python scripts/validate_assets.py --manifest assets/manifest.json --final --strict-license` |
| 构建检查/验证 | `python scripts/build_check.py --project .` → 加 `--run` 实际构建 |

## 执行顺序

### 0. 落地工程骨架

```bash
cp -r <plugin>/templates/godot4/* .        # 或 unity / cocos3；Unreal 暂无起步模板，见下表
mkdir -p docs assets/art assets/audio doc/temp
cp <plugin>/templates/docs/*.md docs/
cp <plugin>/templates/assets-manifest.json assets/manifest.json
python scripts/omni_state.py init --root . --engine godot --platforms web,android
python scripts/omni_state.py checkpoint --root . --task "立项" --next "写 brief"
```

开工前先读 `.omni/active.md`（若有）：那是上个会话留下的当前任务与卡点，压缩或换会话后比对话可靠。

三个起步模板的成熟度不同，**必须如实告诉用户**；Unreal 方向暂未提供起步模板：

| 模板 | 状态 | 需要的手动步骤 |
|------|------|---------------|
| `godot4` | 可直接运行（已实测导入 + 跑通主场景） | 无 |
| `unity` | 可打开，场景需生成 | 菜单 Tools ▸ Omni ▸ Create Main Scene |
| `cocos3` | 代码与配置就绪 | 新建场景 → 挂 `GameRoot` 到 Canvas → 设起始场景 |
| `unreal5` | **暂未提供起步模板** | 由 `unreal-engineer` 生成 .uproject、Source/、Build.cs 与两个 Target.cs |

### 1. 立项与概念（G1）

问清五件事：核心体验、平台优先级、MVP 范围、变现与合规、现有资产与引擎。填 `docs/00-brief.md` 与 `docs/01-gdd.md`，记录待验证假设和 Go / No-Go 决议。预算与里程碑按团队规模估算并标注不确定性。

### 2. gdd

派 `game-narrative-designer`。要求：数值给具体值、每条可验收、单列「对引擎能力的要求」。填完 `advance`。

### 3. 预制作与垂直切片（G2）

按引擎派 `cocos-engineer`、`unity-engineer`、`godot-engineer` 或 `unreal-engineer`；Unreal 方向暂无起步模板，需由 `unreal-engineer` 生成 .uproject、Source/、Build.cs 与两个 Target.cs 骨架（见下表）。要求：先给剖析数据再给优化；分平台构建配置要具体到纹理格式与分包策略。提早实现可玩原型来验证核心循环。

### 4. art（正式资源落地）

派 `game-art-director` 出 `docs/03-art.md` 与 `assets/manifest.json`，并按 `game-art-production` 技能执行：

1. **先做风格圣经** `docs/art-style-bible.md`：一段固定风格锚定文本 + 色板 + 禁止项
2. **逐资产生成**：调用当前会话图像工具或已配置的 AI 图片 API，按需生成变体；需要透明背景时请求透明输出，遵守项目图片备份规则。动画按 `game-animation-production` 生成 GIF 或精灵表并检查切帧。
3. **后处理成规格**：

```bash
python scripts/process_art.py --in raw/btn_raw.png --out assets/art/ui/ui_btn_primary.png \
  --size 256x64 --mode fit --key-color "#FFFFFF" --key-tolerance 14 \
  --nine-slice 24 --check-nine
```

4. **登记** manifest：`tier: "final"` + `source` + `license` + `commercial_ok` + `ai_generated`
5. **终检**：`validate_assets.py --final --strict-license`

在 G2 前制作一个完整但范围小的垂直切片，把程序、策划、美术和音频集成到目标引擎；实测画面品质、资源管线、构建和性能。切片未证明方案可重复、成本可接受前，不根据 demo 估量产排期。插件里的状态脚本只检查文档，不会替你验证这道门禁。

### 5. 音频制作

派 `game-audio-designer` 出 `docs/04-audio.md`，并按 `game-audio-production` 技能选路线：

- **路线 A（AI 生成）**：优先使用当前可用的音频生成工具；或使用 `gen_ai_audio.py` 接 ElevenLabs API，详见 `game-audio-production`。服务的密钥、权限、计费和授权需事先明确。
- **路线 B（8-bit，离线零成本）**：

```bash
python scripts/gen_music.py --style upbeat --out assets/audio/bgm_main.wav --tempo 132 --bars 16
python scripts/gen_sfx.py --list
python scripts/gen_sfx.py --preset hit --out assets/audio/sfx_hit.wav
```

- **必须压缩**：`python scripts/compress_audio.py --dir assets/audio --bitrate 96k`；无 ffmpeg 时按脚本提示改用引擎导入期压缩（Godot QOA / Unity Vorbis / Cocos mp3-ogg / Unreal Vorbis 与平台压缩设置）
- **必须写平台差异**：小游戏需交互后播放、iOS 静音键、Web 自动播放策略

### 批量制作（G3）与 Sprint 循环

G2 通过后才按垂直切片的实际产能计划批量制作。填写 `docs/07-production-roadmap.md`；每轮从策划、程序、美术、音频 backlog 中选一个可验收目标，用 `docs/08-sprint-review.md` 记录范围、负责人、集成构建、测试、反馈与复盘。周期按团队能力定，通常 2–4 周，小团队可以更短。每轮以实际可玩版本评审，失败或未集成的工作明确标记。

### 6. 测试与打磨（G4 / G5）

派 `game-qa-engineer` 出测试计划。Alpha 后进入 Beta 内容锁定，默认停止新增功能；如确需加功能，记录对工期、测试范围和门禁的影响并重新评审。准备 Gold 前**必须真的跑一次构建**，并且**看一眼画面**：

```bash
python scripts/build_check.py --project .                            # 先看命令
python scripts/build_check.py --project . --run --capture g4-beta     # 构建 + 启动 + 截图
python scripts/omni_state.py check --root . --stage qa --evidence     # 文档 + 证据一起校验
python scripts/omni_state.py advance --root . --to release            # 无证据会被拦下
```

截图落在 `docs/qa/evidence/<名字>/`，`receipt.json` 记录所覆盖文件的 sha256。之后任何一次改动都会让这份证据显示过期——过期的截图不算证据，重新截。

解析通过不等于跑起来，跑起来不等于看得对：文字挤出色块、面板溢出、元素没出现，只有看图才发现。Unity、Cocos 与 Unreal 没有插件内置可用的无人值守截图能力，脚本会如实返回 `NOT ASSESSED`；此时用 `--capture-cmd` 给命令，或明说"没看过画面"，**不许当成通过**。确实要先推进可用 `--no-evidence`，但交付时必须写明没看过。

构建失败就把日志原样交给对应引擎工程师，不要自己猜。记录实际测试、平台兼容及候选包证据，邀请负责人评审后再确认 Gold / Release。文档 `advance` 不会自动通过 Alpha、Beta、Gold 或签署发布。

使用 `docs/09-milestones.md` 记录 G1–G5 的负责人、证据路径与决议。Alpha = 功能完整，Beta = 内容锁定，Gold = 目标平台发行候选通过评审；这些状态需要人工基于实际证据确认，不能从文档阶段推断。

### 7. 发布与运营

派 `game-release-operator` 出 `docs/06-release.md`。所有平台数字带"以官方最新为准"与复核入口。

发布后记录线上问题、崩溃/业务指标、玩家反馈和热修复状态，回写下一版本 backlog 与路线图。按需开启下一轮 Sprint；`done` 只代表本轮工件完结，不代表停止运营。

## 交付给用户时

```
## 当前阶段
state.json 里的 stage + 门禁状态

## 已产出工件
docs/ 与 assets/ 清单，标出仍是 placeholder 的数量

## 构建与证据
build_check 的结果：成功 / 失败 / 未执行；有没有截图，截图覆盖哪些文件，是否已过期

## 未完成的真实缺口
明确说清哪些还需要人做
```

## 铁律

1. **不许跳阶段**：`advance` 会拦，别绕过；绕过等于交付不可信
2. **文档不是终点**：`tech` 阶段之后必须真的产生代码与资源文件，只交文档不算完成
3. **构建必须真跑**：`qa` 阶段没有构建结果就不许进 `release`；状态脚本不会自动拦截，需人工核对
4. **draft 不算完成**：`tier: "draft"` 的资源不能进发布；`--final` 终检会拦。交付时必须说清还有多少 draft
5. **数字带出处**：包体上限、引擎能力一律标版本与复核方式
6. **每轮 Sprint 交付可玩构建**：任务完成数不能代替构建、测试和评审
7. **门禁以评审证据为准**：`omni_state.py` 只检查文档标题及 TODO，不能自动验证玩法、构建、设备或发行审批
8. **产物优先于叙述**：派出去的角色声称写了文件，就校验那个路径存在。不存在就是 PHASE FAILED——不推进、不总结为完成。一段流畅的"我将要…"不是证据，磁盘上的文件才是
9. **qa 之后必须有截图**：没有 `docs/qa/evidence/` 里的可用截图，不许进 release；`advance` 会拦。`NOT ASSESSED` 不是通过

## 这套流水线做不到的

- **3D 模型与骨骼动画**：本链路侧重 2D；AI 逐帧结果需要检查并可能需要修图。
- **AI 音乐与音效**：需要当前可用的生成工具或具备权限的外部服务；程序化合成不等同于 AI 生成。
- **商用字体**：只能用 OFL 开源字体，商用字体需用户自购授权
- **替你签名、上架、过审**：只能给清单与排期，不能替你点后台
- **真机兼容验证**：需要真实设备
- **保证代码无 bug**：构建通过 ≠ 功能正确，功能正确 ≠ 好玩
