---
name: rapidocr
description: 使用RapidOCR识别图片中的文字，支持中英文识别。当用户在飞书发送图片并提到"识别图片"、"ocr"、"提取文字"等关键词时使用。
version: 3.0.1
---

# RapidOCR 图片文字识别

## 功能描述
使用RapidOCR识别图片中的文字，只返回识别到的文字内容，每行一条。

## 使用场景
当用户在飞书发送图片并提到以下关键词时触发：
- 识别图片
- OCR
- 提取文字
- 识别文字

## 环境说明
本 skill 自带独立 uv 环境，所有依赖在 skill 目录内的 pyproject.toml 管理，不依赖外部项目目录。

首次使用前如需重建环境：
```bash
cd ~/.hermes/skills/rapidocr && uv sync
```
依赖见 pyproject.toml：rapidocr-onnxruntime、onnxruntime、opencv-python、numpy、pillow、PyYAML。

## 目录结构
```
rapidocr/
├── SKILL.md              # 技能定义文件（Agent 自动加载）
├── pyproject.toml          # uv 环境依赖声明
├── .python-version         # 3.13
├── uv.lock
├── .venv/                  # uv sync 创建（.gitignore 排除）
├── scripts/
│   ├── ocr_rapid.py        # 主识别脚本（自动启动服务→优先走服务→降级直连）
│   ├── ocr_server.py       # 常驻 HTTP 服务 (端口 9898)
│   └── ocr_preload.py      # 模型预加载
└── references/
    └── rapidocr-api.md     # RapidOCR API 参数参考
```

所有脚本通过 `SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` 自动定位 skill 目录，不硬编码绝对路径。

## 执行步骤

### 1. 启动常驻服务（首次使用）
```bash
cd ~/.hermes/skills/rapidocr && uv run python scripts/ocr_server.py &
```

### 2. 执行OCR识别
```bash
cd ~/.hermes/skills/rapidocr && uv run python scripts/ocr_rapid.py <image_path>
```
ocr_rapid.py 会自动检测服务是否运行，未运行则自动启动，无需手动管理服务。

### 3. 返回结果
直接返回识别到的文字，每行一条，不添加任何额外说明。

## 优化配置
- 常驻服务模式：模型只加载一次，后续识别约3秒
- 禁用方向分类 (`use_cls=False`)
- 减小最大边长 (`max_side_len=640`)

## 注意事项
1. 使用 skill 目录内的 uv 环境运行（cd 到 skill 目录后 uv run）
2. 支持中英文混合识别
3. 图片路径可以是本地路径或URL
4. .venv 不纳入 git，重建环境只需 `uv sync`
