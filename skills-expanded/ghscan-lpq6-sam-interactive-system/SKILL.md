# SAM Interactive System - 技能文档

## 📋 技能概述

基于 Facebook Research 的 Segment Anything Model (SAM) 构建的交互式图像分割系统。用户可以通过点击或框选的方式，对图像中的任意目标进行精准分割。

## 🎯 核心能力

### 1. 点击分割 (Point-based Segmentation)
- 在图像上点击标记前景/背景点
- 支持多点迭代优化分割结果
- Shift+点击标记背景区域

### 2. 框选分割 (Box-based Segmentation)  
- 拖拽绘制矩形选框
- 自动分割框内主要目标
- 适合规则形状物体

### 3. 实时预览
- 分割掩码半透明叠加显示
- 置信度评分和区域统计
- 一键导出 PNG 掩码

## 🛠️ 技术架构

```
┌─────────────────────────────────────────────┐
│              React Frontend                 │
│  (Vite + Canvas API + CSS Variables)       │
├─────────────────────────────────────────────┤
│              FastAPI Backend                │
│  (Python + Uvicorn + CORS)                 │
├─────────────────────────────────────────────┤
│         Segment Anything Model              │
│  (PyTorch + ViT-B/L/H)                     │
└─────────────────────────────────────────────┘
```

## 📡 API 接口

### 健康检查
```
GET /api/health
→ { status, device, model_loaded }
```

### 上传图片
```
POST /api/upload
Content-Type: multipart/form-data
→ { image_id, width, height, filename }
```

### 点击分割
```
POST /api/segment/point
{
  "image_id": "abc123",
  "points": [[100, 200], [300, 400]],
  "labels": [1, 0]  // 1=前景, 0=背景
}
→ { success, mask (base64), score, bbox, area }
```

### 框选分割
```
POST /api/segment/box
{
  "image_id": "abc123", 
  "box": [x1, y1, x2, y2]
}
→ { success, mask (base64), score, bbox, area }
```

### 多掩码输出
```
POST /api/segment/multi
{
  "image_id": "abc123",
  "points": [[100, 200]],
  "labels": [1],
  "multimask": true
}
→ { success, results: [{mask, score, bbox, area}, ...] }
```

## 🚀 快速开始

```bash
cd sam-interactive-system
chmod +x start.sh stop.sh
./start.sh
# 访问 http://localhost:5173
```

## 📦 模型说明

| 模型 | 大小 | 速度 | 精度 | 推荐场景 |
|------|------|------|------|---------|
| ViT-B | 375MB | ⚡ 快 | ★★★ | 开发测试、CPU环境 |
| ViT-L | 1.2GB | 🔄 中 | ★★★★ | 生产环境 |
| ViT-H | 2.4GB | 🐢 慢 | ★★★★★ | 高精度需求 |

### 下载模型

```bash
# ViT-B (推荐)
mkdir -p backend/models
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth \
  -O backend/models/sam_vit_b_01ec64.pth
```

## 🎨 前端特性

- **深色主题** - 减少视觉疲劳，专注标注任务
- **双层 Canvas** - 底层原图 + 顶层掩码叠加
- **实时交互** - 点击即时显示标记，拖拽实时绘制选框
- **响应式布局** - 适配不同屏幕尺寸

详见: [FRONTEND_DESIGN.md](./FRONTEND_DESIGN.md)

## 🔧 开发指南

### 后端开发
```bash
cd backend
source venv/bin/activate
python app.py  # 热重载开发
```

### 前端开发
```bash
cd frontend
npm run dev  # Vite HMR
```

### 目录结构
```
sam-interactive-system/
├── backend/
│   ├── app.py           # FastAPI 主应用
│   ├── requirements.txt # Python 依赖
│   └── models/          # SAM 模型文件
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # 主组件
│   │   └── styles.css   # 样式
│   ├── index.html
│   └── vite.config.js
├── docs/
│   ├── FRONTEND_DESIGN.md
│   └── SKILL.md
├── start.sh             # 启动脚本
└── stop.sh              # 停止脚本
```

## 🐛 常见问题

### Q: SAM 模型加载失败？
A: 检查 `backend/models/` 目录是否有模型文件，无模型时系统使用模拟模式。

### Q: GPU 不可用？
A: 确保安装了 CUDA 版 PyTorch：`pip install torch --index-url https://download.pytorch.org/whl/cu118`

### Q: 前端无法连接后端？
A: 检查 CORS 配置和 Vite proxy 设置。开发模式下 Vite 自动代理 `/api` 到 `localhost:8000`。

## 📄 许可

- SAM 模型: Apache 2.0 (Facebook Research)
- 本项目代码: MIT License
