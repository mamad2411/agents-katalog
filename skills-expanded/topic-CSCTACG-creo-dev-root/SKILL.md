---
name: creo-dev
description: >
  Creo Parametric Pro/TOOLKIT 二次开发完整资源。涵盖 C/C++ API 开发、特征创建（Element Tree、
  孔/倒角/圆角/基准/拉伸）、ProMdl/ProSolid/ProFeature 对象操作、Visit 遍历与过滤、
  ProSelection 几何引用、曲线/面集合（ProCrvcollection/ProSrfcollection）、
  UI 编程（ProUIDialog/MFC/Qt 三种框架）、菜单/Ribbon 集成、异步与 DLL 模式、
  注册文件（protk.dat/creotk.dat）、ProError 错误处理、几何遍历与细分、装配操作、
  工程图自动化、层/关系/参数/材料、质量属性计算、制造/NC 编程、项目脚手架与构建配置、
  代码生成工作流。当用户需要 Pro/TOOLKIT 开发、Creo 插件开发、Pro*.h API 调用、
  MFC/Qt 对话框集成、或调试 TOOLKIT 应用时触发。
version: 1.0.0
---

# Creo Parametric Pro/TOOLKIT 开发指南

Pro/TOOLKIT 是 PTC Creo Parametric 的 C 语言 API，通过 Pro* 前缀函数提供对 Creo 数据库和 UI 的受控访问。我们用 C++ 封装并搭配 MFC 或 Qt 构建 UI。

## 首次使用：检测 Pro/TOOLKIT 路径

每次新会话开始时，如果 `$PROTOOL_SRC` 尚未确定，按以下顺序自动检测：

1. **检查环境变量**: 运行 `echo %PROTOOL_SRC%`
2. **检查常见安装路径**（Windows）:
   - `D:\PTC\Creo *\Common Files\protoolkit`
   - `C:\Program Files\PTC\Creo *\Common Files\protoolkit`
3. **询问用户**: 如果自动检测失败，询问用户的 Creo 安装路径

确定路径后，在后续所有 API 文档查阅和代码生成中使用该路径。记为 `$PROTOOL_SRC`。

## 开发环境

| 项目 | 相对路径 |
|------|---------|
| Pro/TOOLKIT 根目录 | `$PROTOOL_SRC` |
| API 头文件 | `$PROTOOL_SRC/includes/` (413 个 `Pro*.h`) |
| API 文档 (Wizard) | `$PROTOOL_SRC/protkdoc/manual0/loadApiWizard.html` |
| API 文档 (单函数) | `$PROTOOL_SRC/protkdoc/api/{N}.html` |
| API 文档 (对象索引) | `$PROTOOL_SRC/protkdoc/api/Pro{Object}.html` |
| 示例代码 (C 源文件) | `$PROTOOL_SRC/protk_appls/` (406 个 .c + 71 个 .h) |
| 用户指南 (HTML) | `$PROTOOL_SRC/protkdoc/manual0/tkusetoc.htm` |
| 链接库 (64-bit) | `$PROTOOL_SRC/x86e_win64/obj/` |
| Makefile 模板 | `$PROTOOL_SRC/x86e_win64/obj/make_*` |
| 注册文件示例 | `$PROTOOL_SRC/protk.dat` |
| API 迁移脚本 | `$PROTOOL_SRC/scripts/protkmap.txt`, `depr_map.txt` |

## 工作流程

### Phase 1: 明确需求

生成代码前先确认：

1. **运行模式**: DLL 模式（推荐）还是同步 EXE 模式
2. **UI 框架**: Pro/TOOLKIT 原生对话框 (`ProUIDialog`)、MFC 还是 Qt
3. **代码类型**:
   - UI/对话框（菜单、Ribbon、对话框）
   - 业务逻辑（特征创建、模型操作、参数管理）
   - 项目脚手架（入口、构建配置、注册文件）
   - 工具类（日志、文件操作、几何计算）
4. **具体需求**: 类名、功能列表、涉及的 Pro/TOOLKIT 对象

使用 AskUserQuestion 收集信息；如不确定，先查阅 `protkdoc` 中的 API Wizard 和示例代码。

### Phase 2: 查阅 API 文档

生成代码前**必须**查阅相关 API 文档：

- 读取 `protkdoc/api/Pro{Object}.html` 了解对象可用函数
- 读取 `protkdoc/api/{N}.html` 了解具体函数签名和参数
- 读取 `protk_appls/pt_userguide/` 下对应章节的示例代码
- 使用 `protkdoc/manual0/` 下的用户指南了解使用场景

### Phase 3: 生成代码

遵循框架特定模式：
- MFC 模板见 [references/mfc-patterns.md](references/mfc-patterns.md)
- Qt 模板见 [references/qt-patterns.md](references/qt-patterns.md)
- Pro/TOOLKIT API 核心模式见本文件下方及 references/ 目录

### Phase 4: 验证输出

- 检查 `#include` 是否引用正确的 `Pro*.h` 头文件
- 检查所有 `ProError` 返回值是否被处理
- 确认 API 函数签名与目标 Creo 版本匹配（注意废弃函数）
- 确认内存管理（`ProArrayAlloc`/`ProArrayFree`、`ProStringToWstring`/`ProWstringToString`）

## API 命名约定

所有函数遵循 `Pro<ObjectType><Action>()` 模式：

```c
ProSolidRegenerate()      // Object=Solid, Action=Regenerate
ProFeatureDelete()        // Object=Feature, Action=Delete
ProSurfaceAreaEval()      // Object=Surface, Action=AreaEval
ProEdgeLengthEval()       // Object=Edge, Action=LengthEval
```

| 动作动词 | 用途 |
|---------|------|
| Get | 从数据库读取 |
| Set | 写入数据库 |
| Eval | 简单计算结果 |
| Compute | 基于几何的数值分析 |
| Visit | 带回调的遍历 |
| Create | 创建新对象 |
| Delete | 删除对象 |
| Alloc/Free | 内存管理 |

函数参数规则：第一个参数为目标对象，输入参数在输出参数之前，返回类型为 `ProError`。

## 对象句柄

### 不透明句柄 (OHandle) — 易失，可能在再生后失效

```c
typedef void* ProMdl;
typedef struct sld_part* ProSolid;
typedef struct geom* ProSurface;
typedef struct curve_header* ProEdge;
typedef struct entity* ProAxis;
typedef struct entity* ProCsys;
```

### 数据库句柄 (DHandle) — 持久标识符

```c
typedef struct pro_model_item {
    ProType type;
    int id;
    ProMdl owner;
} ProModelitem, ProGeomitem;
```

### 句柄转换

```c
// OHandle -> DHandle
ProSurfaceIdGet(surface, &id);
ProModelitemInit(owner, PRO_SURFACE, id, &modelitem);

// DHandle -> OHandle
ProSurfaceInit(modelitem.owner, modelitem.id, &surface);
```

详见 [references/core-objects.md](references/core-objects.md)。

## 应用结构

### 入口函数

```c
#include "ProToolkit.h"

int user_initialize(int argc, char *argv[],
                    char *version, char *build,
                    wchar_t err_buff[80])
{
    // 验证 wchar_t 大小
    int proe_wchar_size;
    if (ProWcharSizeVerify(sizeof(wchar_t), &proe_wchar_size) != PRO_TK_NO_ERROR)
    {
        ProTKSprintf(err_buff, L"wchar_t size mismatch");
        return 1;
    }

    // 注册菜单、通知等
    ProError status = RegisterMenus();
    if (status != PRO_TK_NO_ERROR) return PRO_TK_GENERAL_ERROR;
    return 0;  // 0=成功
}

void user_terminate()
{
    // 清理资源
}
```

### 注册文件 (creotk.dat / protk.dat)

```
name MyApplication
startup dll
exec_file C:\path\to\myapp.dll
text_dir C:\path\to\text
allow_stop TRUE
end
```

### 应用模式

| 模式 | 说明 | 场景 |
|------|------|------|
| DLL | 动态链接到 Creo | 生产部署 |
| Multiprocess (spawn) | 独立进程 | 开发/调试 |
| Asynchronous | 独立进程控制 Creo | 批量操作 |

## Visit 函数模式

遍历集合的标准模式：

```c
ProError MyVisitAction(ProFeature* feature, ProError status, ProAppData app_data)
{
    // 处理特征
    return PRO_TK_NO_ERROR;   // 继续遍历
    // return PRO_TK_E_FOUND; // 停止遍历
}

ProError MyFilter(ProFeature* feature, ProAppData app_data)
{
    return PRO_TK_NO_ERROR;    // 访问
    // return PRO_TK_CONTINUE; // 跳过
}

ProSolidFeatVisit(solid, MyVisitAction, MyFilter, &my_data);
```

常用 Visit 函数：`ProSolidFeatVisit()`、`ProSolidSurfaceVisit()`、`ProSolidAxisVisit()`、`ProSolidCsysVisit()`、`ProSolidQuiltVisit()`、`ProFeatureSurfaceVisit()`、`ProAsmcompVisit()`。

## ProArray 动态数组

```c
ProArray my_array;
ProArrayAlloc(0, sizeof(ProFeature), 10, &my_array);

ProFeature feat;
ProArrayObjectAdd(&my_array, PRO_VALUE_UNUSED, 1, &feat);

int size;
ProArraySizeGet(my_array, &size);

ProFeature* features = (ProFeature*)my_array;
for (int i = 0; i < size; i++) { /* features[i] */ }

ProArrayFree(&my_array);
```

## ProSelection 几何引用

```c
ProSelection selection;
ProModelitem modelitem;
ProAsmcomppath comp_path;

// 创建
ProSelectionAlloc(&comp_path, &modelitem, &selection);
// 提取
ProSelectionModelitemGet(selection, &modelitem);
ProSelectionAsmcomppathGet(selection, &comp_path);
// 转为 Element Tree 引用
ProReference reference;
ProSelectionToReference(selection, &reference);
// 释放
ProSelectionFree(&selection);
```

## 特征创建概览

特征通过 Element Tree（层次化数据结构）创建：

1. 分配根元素：`PRO_E_FEATURE_TREE`
2. 添加特征类型：`PRO_E_FEATURE_TYPE`
3. 添加特征专用元素（含通过 `ProSelectionToReference` 的引用）
4. 获取当前模型并创建模型选择
5. 调用 `ProFeatureWithoptionsCreate()` 带选项数组

### 标准创建模式（推荐）

```c
ProError CreateFeature(ProFeature* created_feature)
{
    ProElement feat_elemtree, elem_feattype;
    ProMdl model;
    ProModelitem model_item;
    ProSelection model_selection;
    ProErrorlist errors;
    ProFeatureCreateOptions *options = NULL;
    ProError status;

    status = ProElementAlloc(PRO_E_FEATURE_TREE, &feat_elemtree);
    status = ProElementAlloc(PRO_E_FEATURE_TYPE, &elem_feattype);
    status = ProElementIntegerSet(elem_feattype, PRO_FEAT_xxx);
    status = ProElemtreeElementAdd(feat_elemtree, NULL, elem_feattype);

    /* ... 添加特征专用元素 ... */

    status = ProMdlCurrentGet(&model);
    status = ProMdlToModelitem(model, &model_item);
    status = ProSelectionAlloc(NULL, &model_item, &model_selection);

    status = ProArrayAlloc(1, sizeof(ProFeatureCreateOptions), 1, (ProArray*)&options);
    options[0] = PRO_FEAT_CR_DEFINE_MISS_ELEMS;

    status = ProFeatureWithoptionsCreate(model_selection, feat_elemtree,
        options, PRO_REGEN_NO_FLAGS, created_feature, &errors);

    ProArrayFree((ProArray*)&options);
    ProElementFree(&feat_elemtree);
    ProSelectionFree(&model_selection);
    return status;
}
```

### 类型安全的元素设置（推荐）

```c
ProElementIntegerSet(elem, PRO_FEAT_HOLE);
ProElementDoubleSet(elem, 25.5);
ProName wname; ProStringToWstring(wname, "MY_FEATURE");
ProElementWstringSet(elem, wname);
ProReference reference;
ProSelectionToReference(selection, &reference);
ProElementReferenceSet(elem, reference);
ProElementCollectionSet(elem, collection);
```

详见 [references/element-trees.md](references/element-trees.md) 和 [references/feature-examples.md](references/feature-examples.md)。

## 错误处理

```c
ProError status;
status = ProSomeFunction(...);
if (status != PRO_TK_NO_ERROR) {
    switch (status) {
        case PRO_TK_BAD_INPUTS:   /* 无效输入 */ break;
        case PRO_TK_E_NOT_FOUND:  /* 未找到 */ break;
        default:                  /* 其他错误 */ break;
    }
}
```

常用错误码：`PRO_TK_NO_ERROR`、`PRO_TK_BAD_INPUTS`、`PRO_TK_E_NOT_FOUND`、`PRO_TK_USER_ABORT`、`PRO_TK_GENERAL_ERROR`、`PRO_TK_OUT_OF_MEMORY`、`PRO_TK_BAD_CONTEXT`。

### 便捷检查宏

```c
#define PRO_CHECK(call) \
    do { ProError _s = (call); \
         if (_s != PRO_TK_NO_ERROR) { \
             printf("Error %d at %s:%d\n", _s, __FILE__, __LINE__); \
             return _s; } } while(0)
```

## 宽字符串

```c
wchar_t wname[PRO_NAME_SIZE];
char cname[PRO_NAME_SIZE];
ProStringToWstring(wname, "MyName");
ProWstringToString(cname, wname);
ProWstringCopy(dest, source, PRO_VALUE_UNUSED);
ProWstringCompare(str1, str2, PRO_VALUE_UNUSED, &result);
```

## 项目脚手架

### 目录结构（DLL 模式）

```
my-creo-plugin/
├── protk.dat                 # Creo 注册文件
├── src/
│   ├── main.cpp             # user_initialize / user_terminate
│   ├── MyDialog.h / .cpp    # UI 代码
│   └── MyFeature.cpp        # 业务逻辑
├── include/                  # 公共头文件
├── text/
│   ├── usascii/              # 英文资源
│   └── chinese_cn/           # 中文资源
├── Makefile                  # 基于 protoolkit makefile 模板
└── x86e_win64/
    └── obj/                  # 编译输出
```

### 构建配置要点

- 编译器: MSVC (cl)，定义 `-DPRO_MACHINE=36 -DPRO_OS=4 -DPRO_USE_VAR_ARGS`
- 链接库: `protk_dll_NU.lib` + `ucore.lib` + `udata.lib`
- Include 路径: `-I$(PROTOOL_SRC)/includes`
- 系统库: `libcmt.lib kernel32.lib user32.lib` 等
- 子系统: console (DLL)，平台: amd64

## 命名规范

| 元素 | Pro/TOOLKIT C API | C++ 封装 (MFC) | C++ 封装 (Qt) |
|------|-------------------|----------------|---------------|
| 函数 | `ProFeatureCreate()` | `CMyFeature::Create()` | `MyFeature::create()` |
| 类型 | `ProFeature`, `ProSolid` | `CMyFeature` | `MyFeature` |
| 枚举 | `PRO_FEAT_EXTRUDE` | 保持原样引用 | 保持原样引用 |
| 成员变量 | N/A | `m_feature` (hungarian ok) | `m_feature` (snake_case) |

## UI 方案选择

| 方案 | 适用场景 | 依赖 |
|------|---------|------|
| **ProUIDialog** | 简单参数输入表单，无需额外依赖 | 仅 Pro/TOOLKIT |
| **MFC** | 复杂多标签/树形面板 | Windows + MFC |
| **Qt** | 现代跨平台复杂界面 | Qt6 |

详见 [references/ui-programming.md](references/ui-programming.md)、[references/mfc-patterns.md](references/mfc-patterns.md)、[references/qt-patterns.md](references/qt-patterns.md)。

## 最佳实践

1. **始终检查 Pro* 函数返回值**
2. **释放分配的内存** — ProArray, ProSelection, ProElement, ProReference 等
3. **在 user_initialize 中验证 wchar_t 大小** — `ProWcharSizeVerify()`
4. **生产用 DLL 模式，调试用 spawn 模式**
5. **优先用 ProFeatureWithoptionsCreate** 而非 ProFeatureCreate
6. **优先用类型安全设置函数** (ProElementIntegerSet 等) 而非 ProValueData
7. **用 ProSelectionToReference 转换选择到引用** 用于 Element Tree
8. **开发时用 PRO_FEAT_CR_DEFINE_MISS_ELEMS** 选项提示缺失元素
9. **区分 ProUtil* 函数** — 它们是 PTC 示例代码的辅助函数，非官方 API
10. **生成代码前查阅 protkdoc** 确认函数签名匹配目标 Creo 版本

## 常用头文件速查

| 任务 | 必需头文件 |
|------|-----------|
| 特征创建 | ProFeature.h, ProElement.h, ProElemId.h, ProFeatType.h, ProFeatForm.h |
| 孔特征 | ProHole.h |
| 圆角/倒角 | ProRound.h, ProChamfer.h, ProCrvcollection.h |
| 基准特征 | ProDtmPln.h, ProDtmAxis.h, ProDtmPnt.h, ProDtmCsys.h |
| 拉伸/旋转 | ProExtrude.h, ProRevolve.h, ProSweep.h, ProStdSection.h |
| 选择 | ProSelection.h, ProSelbuffer.h |
| 参数 | ProParameter.h, ProParamval.h |
| 材料 | ProMaterial.h, ProMdlUnits.h |
| 层 | ProLayer.h |
| 关系 | ProRelSet.h |
| 菜单 | ProMenu.h, ProMenuBar.h |
| 对话框 | ProUIDialog.h, ProUI*.h |
| 通知 | ProNotify.h |
| 制造 | ProMfg.h, ProNcseq.h |

## 参考文件索引

| 文件 | 内容 |
|------|------|
| [references/core-objects.md](references/core-objects.md) | 核心对象类型与关系（ProMdl/ProSolid/ProFeature/ProSurface/ProEdge 等） |
| [references/element-trees.md](references/element-trees.md) | Element Tree 特征创建详解（ProElempath、XML、诊断） |
| [references/feature-examples.md](references/feature-examples.md) | 完整特征创建示例（孔、基准轴/点、倒角、去除面） |
| [references/common-patterns.md](references/common-patterns.md) | 常用模式（应用初始化、选择、几何计算、参数、尺寸、装配、文件导出、通知） |
| [references/layers-relations-materials.md](references/layers-relations-materials.md) | 层操作、关系、参数（含单位）、材料属性、质量属性 |
| [references/ui-programming.md](references/ui-programming.md) | Pro/TOOLKIT UI 编程（菜单/Ribbon、对话框、组件、图形、鼠标、窗口） |
| [references/mfc-patterns.md](references/mfc-patterns.md) | MFC 对话框模板 + Pro/TOOLKIT 集成 |
| [references/qt-patterns.md](references/qt-patterns.md) | Qt 对话框模板 + Pro/TOOLKIT 集成 + CMake |
| [references/utility-functions.md](references/utility-functions.md) | ProUtil* 辅助函数（数学/矩阵/特征/菜单/文件/几何，非官方 API） |
