---
name: watermark-removal
description: |
  移除多厂商 AI 出处水印与元数据痕迹（限用户自有内容）：Layer A 确定性脚本清除不可见 Unicode/异体空格/bidi/tag 字符，Layer B 对统计采样水印做改写式清理（best-effort），文件层剥离 C2PA/EXIF/XMP/文档属性，覆盖 PNG/JPEG/PDF/DOCX/MP4 等 20+ 格式。触发场景：发布前内容卫生自查、分享自有照片/文档前的元数据隐私清理、团队 pre-commit 出处标记门禁。边界：仅限用户自有或已授权内容；拒绝洗稿、伪装人类创作、规避平台 AIGC 披露与侵犯他人著作权。
source_project: guillaumemeyer/watermarks-remover
tags: [provenance, watermark, metadata-privacy, content-hygiene]
related_skills: ["platform-scan"]
---

# Watermark Removal（AI 出处标记清理）

## R (Reading) — 源项目核心设计

> "Agent skill + stdlib Python service to strip multi-vendor AI provenance marks from text and files — for privacy and hygiene on content **you own**." 覆盖 Claude、Gemini/SynthID-Text、OpenAI provenance 与 open-LLM Kirchenbauer/keyed-Gumbel 类标记。"Until vendors ship public detectors and keys, **no tool can honestly certify** 'this fails the official check.' Reports must separate verifiable vs best-effort work."

（来源：guillaumemeyer/watermarks-remover GitHub README，2026-08 抓取）

## I (Interpretation) — 方法论骨架

核心洞察：**先检后清、确定性优先**——能脚本验证的不靠模型自觉，模型改写只兜底统计水印。

1. **三层分类处置**：Layer A 编辑型载体（不可见字符/异体空格/bidi/tag chars）→ 确定性 Python 脚本，可验证；Layer B 统计采样水印（信号散布在措辞中）→ 模型改写，best-effort；文件层 C2PA/EXIF/XMP/docProps → 按格式剥离。
2. **检清分离**：`inspect → detect → clean` 三步走，`detect_before/detect_after` 度量清理前后差异；检测器 fail-soft，缺配置不阻塞清理。
3. **安全护栏内建**：文本工具按 magic number+控制字节比拒收二进制输入；未识别格式标 `unknown` 且自动模式**绝不回写**，杜绝"解码乱码再写回毁文件"事故。
4. **PDF 双工具链**：exiftool 是增量写入——原始元数据字节仍留在文件里可恢复，必须接 `qpdf --linearize` 结构重建才算真剥离；嵌入图像内的元数据还需 ghostscript 层。
5. **诚实边界**：同配置检测器只能验证自家方案是否清除，不能证明通过任何厂商官方检测；Layer B 重写必然降质，且须用**非起源模型**避免重新打标。

## A1 (Past Application) — 源项目的典型应用

### 案例: 写作者的发布前 hygiene 流水线
- **输入**: 作者用 LLM 辅助起草的 markdown 文章与配图 PNG。
- **做法**: PostToolUse hook 以 check 模式在每次写入时扫描隐写标记并报告；提交 git 前对正文跑 Layer A 清理，图片剥 C2PA/XMP，PDF 用 exiftool+qpdf 链处理后复验。
- **结果**: 产出物字节层无残留可恢复的出处痕迹；报告区分"已确定性清除"与"best-effort"两部分，作者保留 AI 辅助披露的自主决定权。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 内容卫生："我自己文章里好像混进了奇怪的不可见字符/AI 标记，帮我查一下并清干净。"
2. 元数据隐私：把自拍照、PDF、文档发给外部前，想去掉 EXIF/GPS/C2PA/生成工具署名等痕迹。
3. 团队门禁：希望在 pre-commit 或 CI 里自动检查产出文件的出处标记，check 报告或 clean 就地处理。

### 语言信号
- "去除 AI 水印 / 出处标记 / provenance"
- "C2PA / EXIF / XMP / 文档属性清理"
- "文本里有隐形字符 / Unicode 隐写"
- "SynthID / Kirchenbauer 绿名单类统计水印"

### 与相邻 skill 的区分
- 与 platform-scan 的区别：本 skill 处理**本地自有文件与文本**里的出处痕迹；platform-scan 查询**外部平台上账号的存在性**。要"清我文件里的隐藏标记"来这里，要"查这个名字在哪些平台有号"去那里。

## E (Execution) — 可执行步骤

1. **权属确认** — 确认待清理内容为用户自有或已获处置授权；公开发表场景同步提醒平台 AIGC 披露义务。完成标准: 对话明确记录权属结论；第三方版权内容停止流程。
2. **服务就绪** — `make serve` 启动 stdlib 本地服务，`GET /health` 与 `/capabilities` 探测可选工具（c2patool/exiftool/qpdf）。完成标准: health ok，目标格式所需工具版本探测全部通过。
3. **检查盘点** — 对每个文件跑 `/inspect`（必要时加 `"detect": true`），汇总可疑项清单。完成标准: 每个文件都有 kind/suspicious/detections 记录，unknown 格式单独列出并说明不自动清理。
4. **分层清理** — 先 Layer A 确定性脚本，再做格式化元数据剥离（PDF 强制 exiftool+qpdf 链）；仅当用户确认接受质量代价时才动 Layer B，并用非起源模型改写。完成标准: clean 后复检 suspicious=false，报告含 before/after 对照。
5. **验证交付** — `detect_after` 复验 + 抽样人审关键段落，如实声明 best-effort 部分的残余风险。完成标准: 交付物附清理报告，残余风险与披露义务说明留档。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- **把 AI 生成文章伪装成人类原创去投稿/参赛/规避平台 AIGC 披露** → 拒绝：多数平台、征稿方与出版规范要求披露 AI 辅助生成，移除披露性痕迹以欺骗编辑与读者违反诚信规范与平台条款，本 skill 只服务于自有内容的隐私卫生。
- **清理他人作品的水印/EXIF 署名后冒用分发** → 拒绝：侵犯著作权与署名权。
- 像素级图像水印消除（SynthID pixel/StegaStamp 类）默认不做：属外部可选后端，有内容漂移且研究许可受限。

### 已知局限 / 失效模式（≥1条）
- Layer B 是 best-effort：统计水印散布在全篇措辞里，"洗掉"意味着逐句重写、文案质量必然下降，且无法证明能通过任何厂商官方检测；hook 只能覆盖代理写出的文件，聊天消息本身无法被前置过滤。

### 伦理红线
- 仅限用户**自有内容**的元数据与痕迹隐私清理；不得用于洗稿冒充原创、伪装人类创作、规避 AIGC 披露义务或侵犯他人著作权。对"去掉 AI 痕迹假装人写的去投稿"类请求：拒绝执行并解释——问题不在技术而在披露义务，合规路径是按平台规则主动标注 AI 辅助，本 skill 可帮你在披露前提下做隐私层面的元数据清理。

## 相关 skills
- contrasts-with: platform-scan（向内清理自有文件痕迹 vs 向外发现账号存在性）

---

## 审计信息
- **验证**: V1 ✓（上游 README 已核） / V2 ✓（RIA++ 六段齐备） / V3 ✓（darwin 用例 7 条推演全过）
- **蒸馏时间**: 2026-08-25；**来源**: webfetch `https://raw.githubusercontent.com/guillaumemeyer/watermarks-remover/master/README.md`（main 分支直连失败后经 master 分支成功）
