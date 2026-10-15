---
name: phonetic
version: 0.1.16
description: 英语音标查询——查询单词的英式/美式音标和简明释义。用户询问英语单词读音、音标或释义时使用。
---

# 英语音标查询

## 用法

```bash
cyeam phonetic <word>
cyeam --pretty phonetic <word>
```

默认输出 JSON 信封，`data` 中包含 `word`、`uk_phonetic`、`us_phonetic` 和 `definitions`。使用 `--pretty` 可输出适合人读的文本。

## 示例

```bash
cyeam phonetic hello
cyeam --pretty phonetic "C++"
```

查询依赖有道词典网页；网络不可用、单词不存在或页面无法解析时，命令会返回错误。
