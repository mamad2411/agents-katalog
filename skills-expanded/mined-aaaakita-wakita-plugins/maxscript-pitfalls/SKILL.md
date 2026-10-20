---
name: maxscript-pitfalls
description: |
  当用户正在编写、修改或调试 3ds Max MaxScript 脚本时，必须使用本 skill。
  本 skill 记录了 MaxScript 开发过程中踩过的坑和解决方案，
  涉及语法陷阱、API 差异、文件路径处理、材质贴图遍历等关键知识点。
  适用于所有 3ds Max MaxScript 脚本的编写、调试与维护。
---

# MaxScript 踩坑记录

## 核心规则

### 一、语法陷阱速记

- **顶层代码不能用 `local`**：`local` 只在函数内部或块级作用域生效，顶层会报 `Compile error: no local declarations at top level`。
- **没有 `+=` / `-=` 复合赋值运算符**：必须写成 `x = x + 1`。
- **单行 `if` 多语句必须用括号包裹**：或改用三元表达式 `result = if cond then val1 else val2`。
- **字符串拼接用 `+`**。
- **不支持行首 `+` 续行**：会报 `expected <factor>`，必须写在一行。
- **.NET DataGridView 索引必须用 `.Item`，不能用 `[]`**：不支持 C# 风格的字符串索引器 `columns["name"]`。
- **.NET 链式调用避免空格分割**：`(dgv.Rows.Item i).Cells.Item "colCheck" .Value` 中间的空格会让 MaxScript 误解析 `.Value` 为独立表达式，应拆分为局部变量。

### 二、文件路径处理

| 全局变量 | 内容 | 示例 |
|---------|------|------|
| `maxFilePath` | 仅目录路径（含末尾 `\`） | `E:\Project\` |
| `maxFileName` | 仅文件名 | `scene.max` |

- 保存时必须 `fullPath = maxFilePath + maxFileName` 后再 `saveMaxFile fullPath quiet:true`，否则会丢失文件名。
- 解析相对路径用 `mapPaths.getFullFilePath relPath`（不是 `resolvePath`，方法不存在）。
- `getFilenamePath` 返回**含末尾分隔符**的路径，可直接拼接文件名。

### 三、材质与贴图遍历

- `sceneMaterials` 里混有非材质节点（BitmapTexture、VRayBitmap 等贴图也可能出现），必须按 `classOf`/`superclassOf` 过滤。
- `getClassInstances` 支持用 `target:mat` 参数获取绑定到特定材质的贴图节点。
- 贴图可能嵌套在 `VRayNormalMap`、`Falloff`、`ColorCorrection` 等中间节点里，需要递归查找。
- 从外部导入的模型，Standardmaterial 的贴图可能放在 `.maps` 数组中而非单独属性上，需后备遍历。

### 四、属性访问安全

- 不同版本的 V-Ray 创建的 VRayMtl 属性集合可能不同，访问不存在的属性会直接报错。
- **必须用 `try-catch` 包裹**属性访问，且判空 `mat.metalness != undefined` 后再比较。

### 五、文件操作

- 用 .NET 类复制文件：`(dotNetClass "System.IO.File").Copy srcPath dstPath`（`copyFile` 功能有限）。
- 复制前后检查 `doesFileExist`，源文件不存在或目标已存在时跳过。

### 六、保存与退出

- **脚本末尾不要调用 `quitMAX #noPrompt`**：会导致 3dsmaxbatch 批处理模式挂起。只保存，不退出。

### 七、常见材质类型判断

用 `classOf mat` + `case` 表达式判断 VRayMtl / Standardmaterial / PhysicalMaterial / CoronaMtl 等类型。

### 八、工作流检测（MR vs SG）

| 材质类型 | MR 标志 | SG 标志 |
|---------|---------|---------|
| VRayMtl | `texmap_metalness` 存在，或 `metalness > 0` | 无 metalness 相关属性 |
| PhysicalMaterial | 固定 MR | - |
| Standardmaterial | 固定 SG | - |
| CoronaMtl | `texmapMetallic` 存在 | 无 |

### 九、调试技巧

- 在监听器打印变量：`format "变量值: %\n" myVariable`
- 检查类型：`classOf obj`（精确类名）/ `superclassOf obj`（父类，如 material、textureMap）
- 查看属性：`getPropNames obj` 列出所有属性名；循环 `getProperty` 读取值并用 `try-catch` 容错。

## 参考示例库

完整的语法陷阱、文件路径、材质遍历、属性访问等分类代码示例与报错信息见 `references/pitfalls.md`。
