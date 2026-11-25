---
name: psd-to-cocos
description: |
  将 Photoshop (PSD) 设计稿转换为 Cocos Creator 布局参考。
  自动导出 PNG 切片并生成坐标 JSON，支持中文图层名。

  触发条件：当用户提到以下关键词时激活本技能：
  - "PSD 转 Cocos"、"导出 PSD 到 Cocos"、"PSD 切图 Cocos"
  - "设计稿导入 Cocos"、"PSD 生成 Cocos 布局"
  - "Photoshop 转 Cocos"、"PSD 导出坐标"
---

# PSD to Cocos

将 Photoshop 设计稿一键转换为 Cocos Creator 可用的布局参考。

## 工作流程

```
PSD 文件
    ↓
psd-layer-reader (已有技能) → psd_layers.json (图层结构)
    ↓
psd-slicer (已有技能) → images/*.png (PNG 切片)
    ↓
psd-to-cocos (本技能) → cocos_layout.json (Cocos 坐标)
```

## 使用方法

### 方式 1: AI 调用

当用户需要转换 PSD 时：

1. 确认 PSD 文件路径
2. 运行完整转换流程：
   ```bash
   python .claude/skills/psd-to-cocos/scripts/psd_to_cocos.py <psd_file> -o <output_dir>
   ```
3. 输出结果给用户

### 方式 2: 命令行直接使用（旧版 - 基础功能）

```bash
# 基础用法
python scripts/psd_to_cocos.py design.psd

# 指定输出目录
python scripts/psd_to_cocos.py design.psd -o ./assets/ui/

# 详细输出
python scripts/psd_to_cocos.py design.psd -v
```

### 方式 3: 新版 CLI（推荐 - 增强功能）

支持批量处理、中文文件名转拼音、冲突策略、失败重试等增强功能。

```bash
# 单个文件转换
python scripts/run_cli.py convert design.psd

# 指定输出目录
python scripts/run_cli.py convert design.psd -o ./output/

# 批量处理目录（交互式选择）
python scripts/run_cli.py convert psd-folder/

# 批量处理目录（全部转换）
python scripts/run_cli.py convert psd-folder/ --all

# 递归扫描子目录
python scripts/run_cli.py convert psd-folder/ --recursive

# 指定冲突策略（覆盖/跳过/重命名/询问）
python scripts/run_cli.py convert design.psd --conflict=skip

# 重试之前失败的文件
python scripts/run_cli.py convert psd-folder/ --retry

# 详细输出
python scripts/run_cli.py convert design.psd --verbose
```

#### 新版 CLI 功能特性

- **批量处理**: 支持目录级批量转换，自动识别所有 PSD 文件
- **中文转拼音**: 自动将中文 PSD 文件名转为拼音输出目录（如 `首页.psd` → `shouye/`）
- **冲突策略**: 支持 `overwrite`（覆盖）、`skip`（跳过）、`rename`（重命名）、`ask`（询问）
- **失败重试**: 自动记录失败文件，支持 `--retry` 参数重试
- **进度显示**: 实时显示转换进度和结果汇总
- **原子操作**: 使用临时目录确保操作安全，失败不残留脏数据

## 依赖

### 必需技能

- `psd-layer-reader` - 导出 PSD 图层结构
- `psd-slicer` - 导出 PNG 切片

### Python 依赖

```bash
pip install psd-tools Pillow
```

## 输出格式

### 文件结构

```
output/
├── psd_layers.json       # 图层树（psd-layer-reader 生成）
├── images/               # PNG 切片（psd-slicer 生成）
│   ├── btn_login.png
│   └── ...
└── cocos_layout.json     # Cocos 布局参考（本技能生成）
```

### cocos_layout.json 结构

```json
{
  "metadata": {
    "version": "1.0.0",
    "psd_file": "design.psd",
    "canvas_size": [1920, 1080],
    "export_time": "2026-02-15T10:30:00",
    "element_count": 25
  },
  "elements": [
    {
      "id": "btn_login",
      "name": "btn_login",
      "original_name": "按钮_登录",
      "type": "sprite",
      "visible": true,
      "psd_bbox": [100, 200, 300, 260],
      "cocos_position": { "x": 200.0, "y": 850.0 },
      "cocos_size": { "width": 200, "height": 60 },
      "cocos_anchor": { "x": 0.5, "y": 0.5 },
      "image_file": "images/btn_login.png"
    }
  ]
}
```

## 坐标转换说明

PSD 和 Cocos 使用不同的坐标系：

| 属性     | PSD    | Cocos           |
| -------- | ------ | --------------- |
| 原点     | 左上角 | 左下角          |
| Y 轴方向 | 向下   | 向上            |
| 锚点     | 无     | 中心 (0.5, 0.5) |

转换公式：

```python
# PSD bbox [x1, y1, x2, y2] → Cocos position
width = x2 - x1
height = y2 - y1
x = x1 + width / 2
y = (canvas_height - y2) + height / 2
```

## 脚本说明

### scripts/psd_to_cocos.py

CLI 入口，协调完整转换流程。

### scripts/converter.py

坐标转换模块，提供 `bbox_to_cocos_position()` 函数。

### scripts/layout_generator.py

JSON 生成器，将 psd-layers.json 转换为 cocos_layout.json。

## 在 Cocos Creator 中使用

### 方式 A: 手动创建（基础）

1. 将 `images/` 文件夹复制到 Cocos 项目的 `assets/` 目录
2. 打开 `cocos_layout.json` 查看每个元素的坐标
3. 在 Cocos 场景中创建 Sprite 节点
4. 根据 `cocos_position` 设置节点位置
5. 根据 `image_file` 关联对应的图片资源

### 方式 B: 使用 PSDImporter 扩展（推荐）

本技能提供 **Cocos 编辑器扩展**，可一键自动导入：

#### 1. 安装扩展

将 `assets/PSDImporter.ts` 复制到你的 Cocos 项目：

```bash
cp .claude/skills/psd-to-cocos/assets/PSDImporter.ts \
   <your-cocos-project>/assets/scripts/editor/
```

#### 2. 准备资源

确保资源目录结构如下：

```
assets/
├── psd-output/              # Python 技能生成的输出
│   ├── images/              # PNG 切片
│   │   ├── btn_login.png
│   │   └── ...
│   └── cocos_layout.json    # 布局数据
└── scripts/
    └── editor/
        └── PSDImporter.ts   # 编辑器扩展
```

#### 3. 使用扩展

1. 在 Cocos 场景中创建空节点（右键 → Create Empty Node）
2. 选中节点，在 **Inspector** 面板点击 **Add Component**
3. 选择 **Custom Script** → **PSDImporter**
4. 在 Inspector 中配置：
   - **Layout Json**: 拖入 `cocos_layout.json` 文件
   - **Images Path**: 图片资源路径（默认：`psd-output/images`）
   - **Verbose**: 是否显示详细日志
5. 点击 **Import To Scene** 按钮

#### 4. 自动导入

扩展会自动：

- 创建根节点（以 PSD 文件名命名）
- 为每个元素创建 Sprite 节点
- 自动设置位置、尺寸、锚点
- 自动加载并关联图片资源
- 在 Console 显示导入进度

**注意**：图片资源需要在 Cocos 中先导入（拖入 assets 目录），扩展才能正确引用。

## 注意事项

- 仅导出可见图层
- 中文图层名通过 `psd-layer-reader` 的映射功能处理
- 本技能不生成 `.prefab` 或 `.scene` 文件，仅生成参考 JSON
- 实际布局仍需在 Cocos 编辑器中手动完成
- 坐标基于 Cocos 3.8.4 的坐标系（锚点中心）

## 故障排除

### 错误：psd-tools not installed

```bash
pip install psd-tools
```

### 错误：psd-layer-reader not found

确保 `psd-layer-reader` 技能已安装在 `.claude/skills/` 目录。

### 错误：无法提取画布尺寸

检查 PSD 文件是否包含有效的根图层边界框。
