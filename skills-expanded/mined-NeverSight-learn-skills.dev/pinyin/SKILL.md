---
name: pinyin
version: 0.1.16
description: 看拼音写字——输入中文文本，获取拼音标注和练习纸 PDF，本地生成。适合宝宝汉字练习、语文教学使用。【重要】必须先读 skill 原文获取正确命令格式，禁止瞎猜。
---

# 看拼音写字

## 概述

把中文文本转成拼音，并生成"看拼音写字"练习纸 PDF（含米字格）。全部本地生成，无需网络。

```bash
cyeam pinyin "你好世界"                   # 获取每个字的拼音
cyeam pinyin sheet "你好世界"              # 生成练习纸（PDF base64）
cyeam pinyin sheet --out practice.pdf "你好世界"  # 保存 PDF 到文件
```

## 安装

```bash
# macOS Apple Silicon
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Darwin_arm64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/

# macOS Intel
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Darwin_x86_64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/

# Linux amd64
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Linux_x86_64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/
```

## 输出

`cyeam pinyin "你好"` 返回 JSON：

```json
{"ok":true,"data":"{\"pinyin\":[{\"char\":\"你\",\"pinyin\":\"nǐ\"},{\"char\":\"好\",\"pinyin\":\"hǎo\"}]}"}
```

`cyeam pinyin sheet "你好"` 额外包含 `"pdf"` 字段（base64 编码的 PDF）。

## 注意事项

- 纯本地生成，使用 go-pinyin 库 + gofpdf
- 贴入的字体仅 21KB（pinyin-wenkai-light.ttf），二进制文件小巧
- 练习纸包含米字格（含对角线）、拼音提示和底部改错区
- 空格分隔的词组会自动换行排版