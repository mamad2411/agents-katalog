---
name: every-joule-style
description: 用用户自己的内容做一本“会动的书”网站：写实的书摆在木桌上，翻到每一课，右页的钢笔墨线插图先一笔一笔画出来、再从纸面立起来，变成可以拖动的 3D 小装置（读数杯、纸签、开关），左页是“预测 → 动手 → 掀开翻盖看解释 → 挑战盖章”。风格类似 Every Joule。任何学科都能用（物理、化学、生物、地理、数学、历史、语文……）。当用户想做互动教材、互动书、3D 立体书、可探索式讲解、把课文 / 讲义 / 知识点做成能动手的网页，或者说“做成 Every Joule 那样”时使用。Use for interactive pop-up book / explorable textbook / ink-line 3D lesson websites built from the user's own content.
license: PolyForm Noncommercial 1.0.0（见 LICENSE.md）
---

# every-joule-style：Every Joule 风格的墨线立体互动书（非官方复刻）

这个 skill 带着一套完整的引擎（`template/`）：书本、桌子、光照、墨线笔画、插图“印在纸上再立起来”、翻盖、印章、控制条、放大镜、音效、自动演示、附页都已经做好。**你要做的只有三件事：写内容、写每课的立体装置、截图自查。** 不要从零写引擎，也不要改引擎的视觉参数。

做出来的东西要像一本精心排版的真书：写实的书和桌子，衬着手绘墨线插图；每一屏只有一个大装置，留白多；学生直接拖装置本身，读数马上跟着变。细节见 `references/style.md`。

## 工作流程

按顺序做，每一步做完再进下一步。**加粗的两处必须停下来等用户回答。**

### 1. 收集内容

用户可能给了课文、讲义、知识点清单、PDF，也可能只说了一个主题。先读完材料，弄清：主题、覆盖哪些知识点、给谁看。材料不够时，用你的知识补全，但要在第 2 步告诉用户哪些是你补的。

### 2. 第一轮问答（**一次问完，最多 4 个问题**）

按 `references/questions.md` 的写法问：分课表、书名和封面、读者和难度、附页要哪些。每个问题都给出推荐的默认值；告诉用户“回复‘默认’就全按推荐来”。有提问工具（如 AskUserQuestion）就用它，没有就发一条编号的消息。语言、字体、音效不问，按默认。

### 3. 第二轮：每课的装置方案（**必须让用户确认**）

装置是最费工的部分，方向错了要全部重做。按 `references/questions.md` 的表格，每课列出：装置叫什么、学生动手做什么（拖什么、点什么）、仪表架上的杯子量什么、开关有哪些、预测题、挑战。构思时参考 `references/subjects.md` 的各学科配方。用户确认或修改后再动手；用户说“你定”就按你的方案做。

### 4. 建项目

```bash
node <skill目录>/scripts/new-book.mjs <新书文件夹> --title "书名" --lang zh
cd <新书文件夹> && npm install
```

`--lang` 跟内容的语言走：中文写 `zh`，英文写 `en`。

### 5. 写文字内容

按 `references/content-format.md` 改三个文件：`src/content/config.js`（书名、封面颜色、图例、来源、给老师）、`src/content/lessons.js`（每课左页的文字、图注、开关、演示字幕）、`src/content/quiz.js`（测验）。模板自带的两课示例要换掉。写完运行：

```bash
node tools/check.mjs --content
```

### 6. 先做第 1 课的装置，给用户看

1. 读 `references/apparatus.md`（写装置的接口和零件），再看 `template/src/lessons/ramp.js`、`contour.js` 两个示例；需要更复杂的写法时看 `examples/`（第一期《抛体运动》五课的装置代码，每个文件开头写了它示范了什么）。
2. 在 `src/lessons/` 下写这一课的装置类，在 `src/lessons/index.js` 按课号登记。
3. 运行 `node tools/check.mjs --only <跨页号> --demo`，**自己打开截图看**（`check-shots/` 里）。对照 `references/checklist.md` 逐条查，有问题就改，再查。跨页号就是网址里 `#` 后面的数字（扉页 1、目录 2，第 1 课通常是 3）。
4. 把第 1 课的截图或 `npm run dev` 的地址给用户看，**问风格和质量是否满意**，满意再做其余各课。

### 7. 其余各课和收尾

每做完一课都跑一次 `node tools/check.mjs --only <跨页号> --demo` 并看图。全部做完后：

```bash
node tools/check.mjs          # 全书检查，错误必须为 0
npm run build                 # 输出到 dist/，是纯静态文件，可以放到任何静态网站托管
```

最后告诉用户：怎么在本地打开、怎么发布 `dist/`，以及还有哪些警告没处理、为什么。

## 必须遵守

- **只改内容和装置**：`src/content/`、`src/lessons/`（以及需要时 `public/audio/`）。`src/engine/`、`src/book/`、`src/ink/`、`src/ui/`、`src/app/` 是引擎，除非修 bug，否则不改。
- **数值要对**：装置里的物理 / 数学 / 化学模型单独写（`run`、`model` 这类纯数据），画面只负责显示。读数、手写数据、预测题答案、翻盖解释、测验答案必须和模型算出来的一致。关键时刻（例如到达坡底）用公式取准确值，不让逐帧积分的误差露出来。
- **每课都要能动手**：至少一个能拖或能点的东西（`handles()`），操作后读数立刻变化；挑战必须用装置才能完成，完成时调用 `this.earnStamp()`。
- **一屏一个大装置**：一课有几个装置时，用“装置”开关切换，同一时间只摆一个，放大 1.3–2 倍、四周留白。纸签、仪表架不能压住装置或互相重叠。
- **不抄 Every Joule**：这种风格受 Every Joule（iamtechartist.com/every-joule）启发。只用这个 skill 里的代码和你自己写的内容；不要复制原作的代码、文字、插图、声音，不要用它的名字当书名。`config.sources` 里的致谢那一行保留。
- **每次改完都检查**：`check.mjs` 报的错误必须清零；警告要么改掉，要么向用户说明为什么保留。不要只看报告，要看截图。

## 文件地图

| 位置 | 内容 |
|---|---|
| `references/questions.md` | 两轮问答怎么问、默认值 |
| `references/content-format.md` | config / lessons / quiz 每个字段、字数预算、写作要点 |
| `references/apparatus.md` | 写装置：坐标、生命周期、零件、拖动、开关、演示镜头 |
| `references/subjects.md` | 各学科的装置配方 |
| `references/style.md` | 风格规范：颜色、线条、构图、节奏、语气 |
| `references/checklist.md` | 交给用户前的自查清单和常见坑 |
| `template/` | 引擎 + 两课示例（物理“滑下斜坡”、地理“等高线”） |
| `template/tools/check.mjs` | 内容校验 + 逐页截图 + 报错和排版警告 |
| `examples/` | 第一期《抛体运动》的五课装置和文字，只供阅读参考 |
| `scripts/new-book.mjs` | 用模板建新书 |
