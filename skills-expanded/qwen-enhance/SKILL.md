---
name: qwen-enhance
description: 增强通义千问 (Qwen) 模型的适配能力，特别是 Qwen-VL 多模态输入格式化。在处理视觉任务时使用。
metadata:
  example_query: 生成 Qwen-VL 视觉 Prompt
---

# Qwen Enhance

此 Skill 专为阿里云通义千问（Qwen）系列模型设计，提供多模态输入（Qwen-VL）和长文本处理的辅助工具。

## 能力描述
- **多模态适配**：自动生成 Qwen-VL 的图片/文本混合 Prompt 格式（如 `<img>url</img>`）。
- **Prompt 优化**：针对 Qwen 的指令遵循能力进行 Prompt 调优。

## 典型用法
1. **生成视觉任务 Prompt**：
   ```bash
   python3 .trae/skills/qwen-enhance/scripts/qwen_vl.py "描述这张图片" "https://example.com/image.jpg"
   ```

## 输出示例
```text
<img>https://example.com/image.jpg</img> 描述这张图片
```
