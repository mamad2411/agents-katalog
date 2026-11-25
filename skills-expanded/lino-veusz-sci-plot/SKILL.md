---
name: lino-veusz-sci-plot
description: 用 Veusz 自动化画全部类型科学图（折线/散点/柱状/箱线/直方图/等高线/热图/矢量场/极坐标/三元图/3D/多面板），脚本批量出 PNG/PDF
---

# lino-veusz-sci-plot — Veusz 科学绘图自动化（全图型）

用 Veusz（开源 Origin 替代品）把数据画成出版级科学图。环境：Veusz 4.x（官方免费，下载 https://veusz.github.io/download/ ；Windows 绿色版自带 Python + Qt + numpy，无需单独装 Python），官方 GPL 软件。下文以 Windows 为例，用 `<veusz-exe>` 代指 Veusz 可执行文件路径（如绿色版解压目录或安装版的 `veusz.exe`）。

## 运行方式（唯一正解）

Veusz 文档脚本是 **Python 语法**（不是 Veusz 命令语言），脚本文件里直接调用预置函数：`Add` / `Set` / `SetData` / `SetData2D` / `SetDataExpression` / `ImportFileCSV` / `ImportFile` / `To` / `Export` / `Save`，并预置 `from numpy import *`。执行：

```powershell
$dir = "输出目录"; $script = "plot.py"   # 脚本内容见下
$p = Start-Process -FilePath "<veusz-exe>" `
    -ArgumentList "--export-option","dpi=300","--export","$dir\out.png","$dir\$script" `
    -PassThru -NoNewWindow `
    -RedirectStandardError "$dir\err.log" -RedirectStandardOutput "$dir\out.log"
$p.WaitForExit(60000)   # 必须用 Start-Process + WaitForExit；直接管道/同步调用会触发工具 WaitDelay 误判
```

- **分辨率坑（重要）**：`--export` 模式下脚本里 `Export(..., dpi=300)` 的 dpi 参数**被忽略、固定 100dpi** → 出图偏小。必须命令行加 `--export-option dpi=300`（或 600）。
- **页面尺寸坑**：`Set('width','16cm'); Set('height','11cm')` 必须放在 `To('page1')` **之后**（page 的设置，写在 Add('page') 之前无效）。16×11cm + 300dpi ≈ 1890×1300px 大图。出图后用 PIL 核对像素：`python -c "from PIL import Image; print(Image.open('out.png').size)"`。
- 脚本可含多个 `Export()` 调用（PNG/PDF/SVG/EPS/TIFF/EMF 按扩展名）；`--export` 参数给出第一个文件名，脚本内 export 全部生效。
- 报错看 `err.log`（Python traceback）。`--export` 渲染完自动退出（ExitCode=0）。
- **不要用** `veusz --listen`（Windows 绿色版管道 EOF 不退出，会挂死）。
- 装库：pip 源码装 veusz 需要 qmake，会失败 → 永远用绿色版 exe。

## 通用脚本骨架

```python
# 1. 数据（任选）
SetData('x', arange(0, 10, 0.5))                     # 1D
SetData('y', 5*exp(-0.3*x))                 # 带对称误差：再 SetData('y (+-)', 误差数组)
SetData2D('z', Z, xrange=(0,100), yrange=(0,80))     # 2D（xedge/yedge/xcent/ycent 亦可）
SetDataText('labels', ['a','b'])                     # 文本数据集
ImportFileCSV('data.csv', 'x y_meas (+-) y_fit', linked=False)  # CSV；descriptor 见下

# 2. 页面与画布
Set('width', '8cm'); Set('height', '6cm'); Set('colorTheme', 'colorbrewer1')
Add('page', name='page1', autoadd=False); To('page1')
Add('graph', name='g1', autoadd=False); To('g1')
Add('axis', name='x', autoadd=False); To('x'); Set('label', 'Time (s)'); To('..')
Add('axis', name='y', autoadd=False); To('y'); Set('label', 'Value'); Set('direction', 'vertical'); To('..')

# 3. 图元：Add('typename', name='p1', autoadd=False) → To('p1') → Set(...) → To('..')

# 4. 图例 / 导出
Add('key', name='key1', autoadd=False); To('key1')
Set('Border/hide', True); Set('horzPosn', 'right'); Set('vertPosn', 'top')   # 位置: left/right/centre x top/bottom/centre；若被高柱子/高曲线盖住，改放柱子矮的一侧（见排查清单 2）
To('/')
Export('C:/path/out.png', dpi=150)
Export('C:/path/out.pdf', pdfdpi=150)
```

## ImportFile descriptor 语法（CSV/TXT 导入）

`ImportFile(filename, descriptor, useblocks=False, linked=False, prefix='', suffix='', ignoretext=False, encoding='utf_8')`

- descriptor：空格/逗号分隔的列映射，如 `'x y (+-)'`（第三列作 y 的对称误差）、`'x+-,y'`、`'z+-[1:5]'`（生成 z_1..z_5）、`` `带空格名` ``。
- 误差标记：`(+-)`=对称 serr；`(+)`=perr；`(-)`=nerr。
- 类型标记：`(text)`/`(date)`/`(float)`。
- 无 header 参数：`ignoretext=True` 跳过文本表头行；空 descriptor 自动命名 col1,col2…。
- 列名与 CSV 表头同名时自动匹配并跳过表头（例：表头 `x,y_meas,y_err,y_fit` + descriptor `'x y_meas (+-) y_fit'`）。
- `ImportFileCSV(filename, descriptor, linked=True)` 是 CSV 专用入口，同样 descriptor 规则。

## 全图型速查（typename + 数据 + 关键设置）

样式走子路径：`Set('PlotLine/hide', True)`、`Set('MarkerFill/color', 'red')`、`Set('BarFill/fills', ...)`。数据/表达式/字面列表三用（如 `Set('xData', [1,2,3])`）。

### 2D（父 = graph，需手动 Add axis x/y）
- **xy**（折线/散点/误差棒）：`xData`/`yData`（默认 'x'/'y'）；`marker`(none/circle/square…)、`markerSize`、`errorStyle`(none/bar/barends/curve/box/diamond…)、`PlotLine/steps`(off/left/right/vcentre/hcentre…)、`PlotLine/interpType`、`PlotLine/width`、`FillBelow/fillto`、`nanHandling`。误差取误差数据集：`SetData('y (+-)', arr)`（对称）/ `'y (+)'`(perr) / `'y (-)'`(nerr)，或 CSV `(+-)` 列导入。
- **bar**（柱状）：`lengths`(默认 ('y',)，多数据集元组)；`mode`(grouped/stacked/stacked-area)、`direction`、`barfill`、`errorstyle`(none/bar/barends)；`BarFill/fills`、`BarLine/lines`。**图例：bar 不用 `key` 而用 `keys`**（每数据集标签元组，如 `Set('keys', ('A','B'))`），`posn` 可给 x 位置数据集。
- **boxplot**（箱线）：`values`(默认 ('data',))；`calculate`(True)、`whiskermode`(默认'1.5IQR')、`direction`、`fillfraction`、`outliersmarker`、`meanmarker`；`calculate=False` 时给 `whiskermin/max、boxmin/max、mean、median` 数据集。
- **histo**（直方图）：`data`；`calcmode`(counts/fraction/density/…cumulative…)、`binning`(constant/manual/auto/fd/…)、`numbins`(10)、`scaling`、`errormode`(默认 gehrels)、`style`(step/join)；`Fill1`/`Fill2`/`PostLine`。
- **function**（函数曲线）：`function`(默认 'x')、`variable`('x'/'y')、`steps`(50)、`min`/`max`(Auto)、`color`；表达式环境含 numpy，如 `Set('function', 'exp(-0.3*x)*sin(x)')`。
- **fit**（拟合曲线）：继承 function；`xData`/`yData`、`function`(默认 'a + b*x')、`values`(FloatDict {'a':0.0,'b':1.0})；y 误差取数据集 serr，无则 `defErr`(0.05)+`defErrType`。注意：**拟合由 'fit' action 触发**，纯脚本需要 `Action('fit', 'p1')` 才会算结果。
- **contour**（等高线）：2D `data`（SetData2D）；`min`/`max`、`numLevels`(5)、`scaling`(linear/sqrt/log/squared/manual)、`manualLevels`、`ContourLabels`、`Lines`、`Fills`、`SubLines`。
- **image**（热图）：2D `data`；`colorMap`(grey/heat/jet/viridis/inferno/magma/plasma/cubehelix…)、`colorInvert`、`colorScaling`(linear/sqrt/log/squared)、`min`/`max`(Auto)、`mapping`(pixels/bounds)、`transparency`、`drawMode`。加色标：`Add('colorbar')` + `Set('widgetName','img1')` + `Set('label','Intensity')` + `Set('direction','vertical')`。
- **vectorfield**（矢量场）：两个 2D 同形数据集 `data1`(dx/r)、`data2`(dy/θ)；`mode`(cartesian/polar)、`rotate`、`reflectx/y`、`baselength`(10pt)、`arrowsize`(2pt)、`scalearrow`、`arrowfront/back`(none)；`Line`、`Fill`。
- **covariance**（误差椭圆）：`xData`/`yData`(默认 x/y)；`covxx/covxy/covyx/covyy` 留空自动算；`Line/steps`(25)、`Fill`。
- **polar**（极坐标）：自含图（父 = page/grid，非 graph）；`minradius`/`maxradius`、`units`(degrees/radians/…)、`direction`、`position0`、`log`、`SpokeLine/number`(12)、`RadiiLine/number`(6)；**子 plotter 用 `nonorthpoint`（`data1`=r、`data2`=θ，marker/PlotLine 样式）+ `nonorthfunc`（`function` 表达式、`variable`='b' 角度变量）**，不能用 xy（2D plotter 只允许 graph 父）。
- **ternary**（三元图）：自含图（父 = page/grid）；`mode`(percentage/fraction)、`coords`、`labelbottom/left/right`、`MajorTicks/number`(10)、`MinorTicks/number`(50)、`GridLines`；**子 plotter 用 `nonorthpoint`（`data1`=第一组分、`data2`=第二组分，第三组分自动 1-a-b）**。

### 3D（结构：page → scene3d → graph3d → 3D plotter；graph3d 用 autoadd=True 自动建 x/y/z 轴）
**graph3d 不能直接挂 page 下（RuntimeError: Widget parent is of incorrect type），必须先建 scene3d 容器：**
```python
Add('page', name='page1', autoadd=False); To('page1')
Add('scene3d', name='sc1', autoadd=False); To('sc1')
Add('graph3d', name='g3')          # autoadd 默认 True → 自动建 x/y/z 轴
To('g3')
Add('point3d' / 'surface3d' / 'function3d' / 'volume3d', ...)
```
- **point3d**：`xData`/`yData`/`zData`；`marker`(circle)、`markerSize`(10)、`scalePersp`、`PlotLine/hide`(True)、`MarkerFill/colorMap`；误差 3D 线段。
- **surface3d**：2D `data`；`mode`(默认 'z(x,y)'，6 种)、`highres`、`Line`、`Surface/colorMap`(grey)、`DataColor/points`(2D 可选)。
- **function3d**：`fnx/fny/fnz/fncolor` 表达式；`mode`('x,y,z=fns(t)' 或曲面模式)、`linesteps`(50)、`surfacesteps`(20)、`color`；`Line`/`GridLine`/`Surface`。
- **volume3d**（体素）：`xData`/`yData`/`zData` + `DataColor/points`(默认 'v')；`colorMap`(grey)、`colorInvert`、`transparency`(50)、`reflectivity`、`fillfactor`、`Line`。

### 容器 / 装饰 / 特殊
- **grid**（多面板）：`rows`(2)/`columns`(2)、`scaleRows/Cols`、各 `Margin`；父只能是 page 或 grid；子图 Add('graph', parent='grid1')。
- **label**（文本标注）：`label`（字符串或文本数据集）；`alignHorz/alignVert`、`angle`、`Text`、`Background`、`Border`(hide True)；支持 LaTeX 风格 `\chi^{2}`。
- **shape 四兄弟**：`rect`/`ellipse`/`imagefile`/`svgfile`：`xPos/yPos/width/height`（分数）、`rotate`、`clip`、`Fill`、`Border`；rect 有 `rounding`。
- **line**（箭头线）：mode=`length-angle`(`length`+`angle`) 或 `point-to-point`(`xPos2/yPos2`)；`arrowright`/`arrowleft` 值用 ArrowCodes：`none`/`arrow`/`arrownarrow`/`arrowtriangle`/`arrowreverse`/`linearrow`/`linearrowreverse`/`bar`/`linecross`/`asterisk`/`circle`/`square`/`diamond`/`lineup`/`linedown`/`lineextend`（没有 'solid'）；`arrowSize`、`Line`。
- **axis-broken**（断裂轴）：替换 graph 中普通 axis；`breakPoints`(成对起止)、`breakPosns`(断裂位置分数)。

## 颜色 / 主题 / colormap

- colorTheme：`black`、`default1`、`colorbrewer1`、`colorbrewer2`、`rgb6`、`max128`。
- 颜色名：`auto`、`foreground`、`background`、`transparent`、`white/black/red/green/blue/cyan/magenta/yellow/grey`、`dark*`、主题循环 `theme1..themeN`；也接受 `#RRGGBB`。
- colormap：`grey`、`heat`、`jet`、`cool`、`hot`、`reds`、`greens`、`blues`、`oranges`、`portland`、`rdbu`、`purd`、`cubehelix`、`viridis`、`inferno`、`magma`、`plasma`、`none`(按数据着色关闭)。

## 排查清单

1. `Set('xLabel', ...)` 不存在 → 轴标题是 axis 组件的 `label`：`To('x')` 后 `Set('label', ...)`。
2. 图例位置：`horzPosn`/`vertPosn`（不是 posn）。**图例会被高柱子/高曲线盖住**：不要机械放 right+top，先看数据分布，选柱子矮的一侧放（如右上角柱子最高就放 left+top）；给被遮挡轴留白（`Set('max', 数据最大值×1.3)` 左右）；字号用 `Set('StyleSheet/Font/size', '10pt')` 标准值，14pt 太大。
3. `import('...')` 是 Python 保留字 → 用 `ImportFile`/`ImportFileCSV`。
4. 空图导出报 `IndexError: list index out of range`（paintTo）→ 脚本前面有错导致文档空，看 err.log 完整 traceback。
5. 运行超时误判：一律 `Start-Process` + `WaitForExit(60000)`，不要直接同步调用。
6. 3D 图结构是 page → **scene3d** → graph3d → plotter3d，graph3d 不能直接挂 page。
7. 极坐标/三元图父组件是 page/grid（自含坐标），子 plotter 用 **nonorthpoint/nonorthfunc**；2D plotter（xy/function/fit/bar/contour 等）父必须是 **graph**。
8. 误差棒：**`SetData('y', yv, serr=...)` 的 serr 参数在 4.2.1 会空图 IndexError！** 正确写法是误差数据集命名约定：`SetData('y', yv)` + `SetData('y (+-)', ye)`（对称）/`'y (+)'`/`'y (-)'`；CSV 用 `(+-)` 列（见 descriptor 语法）。plotter 用 `errorStyle` 控制显示样式。
9. 中文/特殊字符标签：Veusz 文本用 LaTeX 风格转义，中文需字体支持（默认 Arial 系可能缺字，谨慎使用）。
10. 脚本环境 numpy 已预置但**数据集名 ≠ Python 变量**：`SetData('x', arr)` 后 `SetData('z', exp(-x**2))` 会 NameError——要么用 Python 变量（`xv=...; SetData('x',xv); SetData('z', exp(-xv**2))`），要么 `SetDataExpression('z', 'exp(-x**2)')`。
