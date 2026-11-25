---
name: pdf2indd
description: 把 PPTX/PDF 重建为可编辑 InDesign 文档(.indd)。跑 pdf2indesign 管线 → 逐页视觉QA → 按缺陷修复 → InDesign打包交付。输入一个 .pptx(推荐)或 .pdf 的路径。适用于"把这个PPT/PDF转成InDesign"类请求。
---

# pdf2indd — PPTX/PDF → 可编辑 InDesign（含视觉QA闭环）

你是这条流水线的**驾驶员**：引擎是确定性的（本仓库的 Python+JSX），但每个新文档都会带来新怪癖。
你的职责 = 跑引擎 → **亲眼逐页对比** → 用下方"缺陷→旋钮"表修复 → 直到通过 → 打包交付。
**绝不要跑完管线不看结果就交付。**

仓库根目录 = 本 skill 文件向上三级（`.claude/skills/pdf2indd/` 的上层）。下文命令均在仓库根执行。

## 0. 前置检查（一次性）
```bash
python -c "import fitz, PIL, pptx; print('py deps OK')"   # 缺则 pip install -r requirements.txt
```
- Windows + Adobe InDesign（COM，已验证 2026/v21）；PowerPoint（若输入是 pptx）
- 字体：**思源黑体 CN** 必装（缺失字体统一回退它——用户既定规则）

## 1. 输入处理
- 输入是 **.pptx**：先用 PowerPoint COM 导出"真实渲染"PDF（这是版式基准 truth）：
```powershell
$ppt=New-Object -ComObject PowerPoint.Application
$pres=$ppt.Presentations.Open("<abs>.pptx",$true,$false,$false)
$pres.SaveAs("<abs>_导出.pdf",32); $pres.Close(); $ppt.Quit()
```
- 输入只有 **.pdf**：直接用它；但**中文极可能乱码**（PowerPoint 导出的 PDF 字体子集无 ToUnicode）——没有 pptx 时向用户说明该风险。

## 2. 跑管线（生成重建数据）
```bash
python pdf2indesign.py "<truth>.pdf" --pptx "<源>.pptx" --out "<名>_indd" --no-indesign
```
产出 `<名>_indd/`：`build.json`(纯PDF) + `build_hybrid.json`(PDF视觉+PPTX文字，**有pptx必用这个**) + `img/` + `slides/`。

## 3. InDesign 构建（COM 稳健调用——照抄，别简化）
```powershell
$dir="<abs输出目录, 正斜杠>"
$jsx="<repo>/jsx/build_hybrid.jsx"      # 纯PDF模式用 build.jsx
$src="var __DIR__=`"$dir`";`n" + [IO.File]::ReadAllText($jsx,[Text.Encoding]::UTF8)
$app=New-Object -ComObject InDesign.Application.2026
try{ $app.Visible=$true }catch{}
for($i=0;$i -lt 40;$i++){ try{ $null=$app.DoScript("1;",1246973031); break }catch{ Start-Sleep -Milliseconds 750 } }
$app.DoScript($src,1246973031)
```
**COM 踩坑速查**（都真实发生过）：
- `Object reference not set` ≈ 被包装的 **JS 内部错误**（常见：同名 indd 已打开导致保存失败）。用 try/catch 包 JSX 体、把 `e+' line '+e.line` 写进文件来拿真错。
- `app.modalState=True` = **崩溃恢复对话框**挡住脚本 → 清 `%LOCALAPPDATA%\Adobe\InDesign\Version *\zh_CN\Caches\InDesign Recovery`（移走别删）。
- 别用 ScriptArgs / 别传 jsx 文件路径（新实例不可靠）——**源码字符串 + `__DIR__` 注入**。
- 产物验证看 `build_log.txt` 尾行 `SAVED ... PDF ok`，别信 COM 返回值。

## 4. 视觉QA（核心环节）
逐页渲染 truth vs 重建 的并排图并**亲眼看**（8~10页/批，覆盖全书）：
```bash
python src/compare.py "<truth>.pdf" "<名>_indd/<名>_indd_预览.pdf" "<名>_indd"
```
（或用 PyMuPDF+PIL 自拼 montage，60~90dpi 足够。）

### 缺陷 → 旋钮 对照表
| 看到的症状 | 根因 | 修哪里 |
|---|---|---|
| 图片溢出/互相压盖 | 用了裁剪前 bbox | 已内置(`explode.py` 用 rawdict 可视bbox)；若再现查该页 transform |
| 透明图变黑块 | SMask 未合成 | 已内置(mask→RGBA)；查 `mask_applied` 统计 |
| 中文变"创创创" | PDF 无 ToUnicode | 必须 `--pptx`（hybrid） |
| 标签没进框/没居中 | 位置漂移 | `hybrid.py`: `snap_texts`(内容匹配+对齐感知) / `center_in_box`(矩形框) / `snap_labels_to_bubbles`(气泡,全局1:1) / `center_h_in_panel`(满版色块) |
| 白字看不见 | 深色底衬在导出中丢失 | `inject_backings`(PPTX有深rect则补回) / `synth_banner`(无底的≥20pt白标题→合成黑条+白字页面居中) |
| 文字重影(一粗一细) | 转曲文字被栅格化+PPTX字叠加 | `_is_outlined_text_raster` 过滤(细长栅格 h<16 且 w>1.8h) |
| 填充块多出细描边 | InDesign怪癖:先设strokeColor=NONE再设Weight=0会残留 | 已内置(JSX **先weight后color**)——新写JSX务必保持此顺序 |
| 同名标签叠在一处 | 重复标签都吸到首个位置 | 已内置(同名收集所有位置,就近1:1) |
| 短标签(如"01")消失 | 框太窄溢流(overset)不渲染 | 已内置(宽度取max/高度余量)；新症状查框尺寸 |
| 彩色块上白字被改灰 | 校色误判"无底" | `fix_text_colors`/`synth_banner` 的 backing 判定=任何 fill sum<700 |

改完旋钮后：重跑 `src/hybrid.py <目录> <目录>/slides` → 重跑步骤3 → 重新渲染核对该页。**只有肉眼确认修好才算修好。**

### 通过标准
版式贴合 truth、中文正确、标签居中于所属图形（格式塔）、无重影/黑块/溢出、深底白字&无底标题有黑条。
换字体导致的字形/字宽差异是**接受的**（思源黑体规则）；PDF 里本来不可见的内容被我们修可见（如分隔页标题）是**改进**，向用户说明即可。

## 5. 打包交付
用打包 JSX（安全要点：**若文档已在用户 InDesign 里打开，用现有文档并先保存，绝不关闭用户文档**；只关自己打开的）：
```
doc.exportFile(ExportFormat.INDESIGN_MARKUP, File(pkg+'/<名>.idml'));
doc.packageForPrint(pkgFolder, true,true,true,true,false,true,true,true,false);
```
交付物：`<名>_可编辑.indd` + `_预览.pdf` + 打包文件夹(Document fonts/Links/idml)。
最后给用户：结果摘要 + 抽查对比图 + 残留已知差异清单（诚实列出）。

## 已知边界（提前告知用户）
- 复杂矢量(曲线/渐变)栅格化置入：100%还原但该块不可编辑
- CMYK/专色/混合模式简化为 RGB
- 思源黑体字形与原字体不同（位置对、字样不同）
- 扫描型 PDF 无文字可炸
