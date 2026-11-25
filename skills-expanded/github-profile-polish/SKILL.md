---
name: github-profile-polish
description: 为 GitHub 个人账号审计、设计和生成主页 README，提供四种风格、亮暗双版、本地预览、真实公开贡献展示与可选每日刷新。适用于新手、求职者、维护者和作品集作者。触发词：GitHub 主页、profile README、主页美化、主页重做、贡献展示、PR 卡片、开源贡献怎么展示。具体项目仓库的 README 装修和组织主页不在本 skill 范围内。
metadata:
  agent_created: "true"
---

# GitHub 个人主页

把用户自己的介绍、作品与真实贡献整理成可直接使用的主页。**没有 PR、没有高星仓库，也能完成主页。**风格由用户选择；受众和内容只是建议依据，不替用户决定审美。

## 先确定什么

- 目标账号：GitHub 用户名，不是邮箱或网址。组织账号走 `<org>/.github/profile/README.md`，不要套个人流程。
- 内容：显示名、希望别人知道的一句话、已有作品或联系链接。用户已给过的信息不要重复问；缺少非必要项就省略，不能编造履历、成果或项目。
- 风格：有偏好就沿用；没有偏好先给四种预设的预览。用户只想快速完成时默认 `t1 + blue`，不为选择风格反复打断。
- 修改范围：新建同名仓库还是修改已有主页？先看准确工作目录与 Git 状态。发布、覆盖现有 README、修改账号设置是不同操作，不能从“美化”推定全部授权。

用户只需说“用这个 skill 美化我的 GitHub 主页，用户名是……，偏好……”，不必自己知道脚本怎么拼装。助手负责把已确认内容写成配置、运行工具和展示结果。

## 四种可直接运行的风格

| 参数 | 风格 | 视觉差异 | 常见用途 |
|---|---|---|---|
| `t1` | Editorial / 编辑排版 | 透明背景、名字为焦点、细线与留白 | 通用个人介绍、求职 |
| `t2` | Terminal / 终端 | 窗口标题栏、提示符、静态光标；贡献图也采用终端框架 | 喜欢 CLI、后端或系统风格 |
| `t3` | Card / 卡片 | 克制的边框和底色；身份与贡献分区 | 喜欢明确的信息分组 |
| `t4` | Minimal / 极简 | 完全使用 Markdown；贡献也以文本列表展示，不生成 SVG | 零图片依赖、低维护、文字优先 |

强调色独立选择 `blue / purple / green / orange`；内容语言支持 `zh / en`。预设不绑定职业，也不因用户的 star 数拒绝重做。

```bash
python scripts/build_profile.py --gallery ./style-preview
```

打开输出的 `index.html` 比较亮暗双版；也可以加 `--config ./profile.json`，用用户自己的名字比较。图库不联网、不填入虚构贡献数字。详细排版规则按需读 [design-system.md](references/design-system.md)。

## 可复现的首次使用路径

以下命令从本 skill 目录运行。助手从其他目录执行时，使用实际 skill 的绝对路径，不能硬编码作者机器的路径。只有 Python 3.10+ 是必要依赖。

```bash
python scripts/build_profile.py --init ./profile.json --username YOUR_USERNAME
python scripts/build_profile.py --config ./profile.json --mode projects --out ./profile
python scripts/verify_render.py --local ./profile
```

把 `YOUR_USERNAME` 换成用户账号；在第二步前填写真实的显示名、定位、作品和联系链接。配置结构、Windows 用法与故障处理见 [first-run.md](references/first-run.md)。也可直接用 `--username / --name / --tagline / --theme` 生成，无需配置文件。

`projects` 路径完全离线。生成后打开 `preview.html` 检查亮暗效果；它是本地近似预览，**不是 GitHub 已发布的证明**。

## 根据内容选择模式

| 模式 | 行为 |
|---|---|
| `projects` | 不联网，使用已确认的介绍、作品和链接；无需任何 PR 或 token |
| `auto` | 获取真实公开已合并 PR；数量为零时自动省略贡献卡，保留介绍与作品 |
| `contributions` | 明确以已合并 PR 为主；没有可展示 PR 时停止并建议改用其他模式 |

```bash
python scripts/build_profile.py --config ./profile.json --mode auto --out ./profile-live
```

认证不是必填项。公开 API 可匿名调用，但有额度限制；有需要时使用环境变量 `GH_TOKEN` / `GITHUB_TOKEN` 或已有的 `gh auth`。**不把 token 写进配置、README、命令示例的真实值或输出日志。**网络失败不能冒充“零贡献”；可先用 `projects`，或在已有匹配缓存时明确使用 `--offline`。

贡献统计必须满足：
- 只查询 `is:public`，即使 token 能读取私有仓库，也不能把私有贡献发布到主页。
- 默认排除自有仓库的 PR；显式包含时必须写“包含自有仓库”，不能标成上游贡献。
- 搜索过滤按账号名下仓库区分，不能自动判定组织所有权；组织项目是否属于第三方上游、个人承担什么角色仍需确认。
- 逐仓库 PR 数使用精确查询，不拿抽样数量替代。API 返回不完整结果或核实失败时停止，保留原输出。
- 候选仓库未抓全时，只说“展示若干已核实仓库”，不能声称是全局排名。
- 缓存必须匹配用户名、公开范围和统计口径。旧缓存缺少这些字段时重新联网生成，不能静默迁移成可信证据。
- 仓库 star 反映该仓库的关注度，不证明用户能力。作品说明与个人贡献范围仍需用户确认。

## 修改已有主页

先只读运行 `scripts/audit_profile.py USERNAME`；只改用户希望改的层。已有强作品不意味着必须保持原视觉，初学者也不需要凑满六个置顶仓库。

生成器默认拒绝覆盖。先生成到新目录供用户看，再列出确切覆盖文件；确认后才用 `--overwrite`。这个参数会重建同名生成文件，**不是合并用户手写 README 的保证**，其他文件保持不动。不同账号使用不同输出目录。

日常贡献刷新只替换一组 `CONTRIB:BEGIN / END` 标记内的内容，保留用户在标记外添加的文案。标记重复或顺序错误时停止，不尝试猜测。

头像、bio、置顶和社交链接的内容建议按需读 [content-model.md](references/content-model.md)。账号设置不由本地生成器自动修改；置顶通常需要用户在网页操作。

## 可选自动刷新

```bash
python scripts/build_profile.py --config ./profile.json --mode auto --automation --out ./profile-live
```

额外产出 `.github/workflows/update-stats.yml` 和其所需的三个独立脚本。发布到 `USERNAME/USERNAME` 后，由 GitHub Actions 每日刷新，也可手动触发；无需访问原 skill 安装目录。网络或数据检查失败则任务失败，不提交伪造或部分统计；内容不变时不追加提交。

自动化是可选项，不给纯作品模式强加后台任务。不能默认加入 snake、打字动画或第三方实时统计卡；用户明确需要时，说明维护与自动化提交的代价。第三方服务状态需实时验证，[widget-liveness.md](references/widget-liveness.md) 的日期记录不是永久结论。

## 验证和发布

1. 本地：`scripts/verify_render.py --local DIRECTORY` 检查 README、亮暗配对、本地文件和 SVG 合规。`t4` 必须无图片。
2. 视觉：打开 `preview.html`，检查桌面与窄屏上的长名字、中英文、颜色与排版。字宽估算不保证真机准确。
3. 发布：展示目标仓库、可见性和 diff，取得用户授权后再建仓、push 或改账号设置。个人主页要使用公开的同名仓库，不改其他项目的 README。
4. 线上：发布后运行 `scripts/verify_render.py USERNAME` 并查看 GitHub 实际页面。404、主题不一致或图片格式错误仍属于未完成。

GitHub 图片和 HTML 限制按需读 [github-rendering.md](references/github-rendering.md)。仓库内引用 SVG，亮暗选择用 `<picture>`，logo 内嵌为 data URI；不要在 README 内联 SVG 或在 SVG 中引用远程图片。

交付时说清：选择了什么风格、生成/覆盖了哪些文件、哪些数据来自 API、是否只使用缓存、哪些检查实际通过、是否已发布、还有哪些账号设置需用户操作。不能把本地结构检查说成线上验收。

## 脚本职责

| 脚本 | 用途 |
|---|---|
| `build_profile.py` | 首次配置、完整生成、风格图库、近似预览、可选工作流；推荐入口 |
| `scaffold.py` | 单独生成身份层与基础 README，默认保护已有文件 |
| `generate_contrib.py` | 获取或重渲染真实公开贡献；只更新标记区，支持四种风格 |
| `audit_profile.py` | 只读审计现有线上账号和主页 |
| `verify_render.py` | 发布前离线结构检查、发布后线上资源检查；不替代视觉检查 |

维护本 skill 时，运行所有脚本的 `--help`、四种离线风格与本地检查；覆盖保护、零贡献、错误用户名/配置、失效缓存与联网失败都要验证。不要只用“可编译”证明工作流可用。
