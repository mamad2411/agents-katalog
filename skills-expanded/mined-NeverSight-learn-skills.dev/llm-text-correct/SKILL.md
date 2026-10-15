---
name: LLM-Text-Correct
description: |-
  使用 **pycorrector + MacBERT** 专业模型，自动修正中文拼写、形近字、语法、标点错误。准确率高达 **90%+**，远超普通 LLM 提示词。
metadata:
  openclaw:
    requires:
      bins:
        - python
---

# LLM-Text-Correct

**功能**：使用 **pycorrector + MacBERT** 专业模型，自动修正中文拼写、形近字、语法、标点错误。准确率高达 **90%+**，远超普通 LLM 提示词。

## 支持的模型（推荐顺序）
1. **chinese-kenlm-klm** → 这是一个基于 KenLM 的统计语言模型（N-gram）纠错方法，不是深度学习模型。
2. **shibing624-macbert4csc-base-chinese** → 这是一个基于 Transformer（MacBERT）的深度学习纠错模型。

## 执行步骤
1. **解析目录**：识别用户的源路径（支持单个音频文件或整个文件夹）。
2. **默认目标**：若未指定输出路径，默认在输入同级创建 `[原文件名]_corrected.txt`或[原文件名]_corrected 文件或目录。
3. **调用命令**：使用以下兼容性命令启动脚本（优先 python3，失败则 python）。脚本会自动创建虚拟环境、检测 GPU 并安装对应版本。

   ```bash
   (python3 scripts/corrector.py ["<输入文本/路径>"] [--refine] [--model-path "<模型路径>"]) || (python scripts/corrector.py ["<输入文本/路径>"] [--refine] [--model-path "<模型路径>"])