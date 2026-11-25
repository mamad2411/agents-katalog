---
name: huggingface-tokenizers
description: Fast BPE/WordPiece tokenization and custom vocab training.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [tokenizers, transformers, datasets]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Tokenization, HuggingFace, BPE, WordPiece, Unigram, Fast Tokenization, Rust, Custom Tokenizer, Alignment Tracking, Production]

---

# HuggingFace Tokenizers——面向自然语言处理的快速分词工具

兼具 Rust 语言的高性能与 Python 的易用性，是可用于生产环境的快速分词器。

## 何时使用 HuggingFace Tokenizers

**以下情况建议使用 HuggingFace Tokenizers：**
- 需要极快的分词速度（每 GB 文本处理时间 <20秒）
- 需要从零开始训练自定义分词器
- 需要实现标记与原始文本位置的对应关系跟踪
- 构建用于生产环境的大语言处理流程
- 需要高效地对大规模语料库进行分词处理

**性能特点：**
- **速度**：在 CPU 上处理 1GB 文本仅需不到 20 秒
- **实现架构**：以 Rust 为核心，同时提供 Python/Node.js 接口
- **效率**：相比纯 Python 实现，速度提升 10 到 100 倍

**可选择的其他替代工具：**
- **SentencePiece**：与语言无关，被 T5/ALBERT 模型采用
- **tiktoken**：OpenAI 为 GPT 模型开发的 BPE 分词器
- **transformers AutoTokenizer**：仅用于加载预训练模型（其内部实际使用该库）

## 快速入门

### 安装

```bash
# Install tokenizers
pip install tokenizers

# With transformers integration
pip install tokenizers transformers
```

### 加载预训练分词器

```python
from tokenizers import Tokenizer

# Load from HuggingFace Hub
tokenizer = Tokenizer.from_pretrained("bert-base-uncased")

# Encode text
output = tokenizer.encode("Hello, how are you?")
print(output.tokens)  # ['hello', ',', 'how', 'are', 'you', '?']
print(output.ids)     # [7592, 1010, 2129, 2024, 2017, 1029]

# Decode back
text = tokenizer.decode(output.ids)
print(text)  # "hello, how are you?"
```

### 训练自定义 BPE 分词器

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

# Initialize tokenizer with BPE model
tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()

# Configure trainer
trainer = BpeTrainer(
    vocab_size=30000,
    special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],
    min_frequency=2
)

# Train on files
files = ["train.txt", "validation.txt"]
tokenizer.train(files, trainer)

# Save
tokenizer.save("my-tokenizer.json")
```

**训练时间**：100MB的语料库大约需要1-2分钟，而1GB的语料库则需约10-20分钟。

### 带填充的批量编码

```python
# Enable padding
tokenizer.enable_padding(pad_id=3, pad_token="[PAD]")

# Encode batch
texts = ["Hello world", "This is a longer sentence"]
encodings = tokenizer.encode_batch(texts)

for encoding in encodings:
    print(encoding.ids)
# [101, 7592, 2088, 102, 3, 3, 3]
# [101, 2023, 2003, 1037, 2936, 6251, 102]
```

## 分词算法

### BPE（字节对编码）

**工作原理**：
1. 从字符级词汇表开始
2. 找出出现频率最高的字符对
3. 将其合并为一个新标记，并加入词汇表
4. 重复上述步骤，直至达到设定的词汇表大小

**被以下模型采用**：GPT-2、GPT-3、RoBERTa、BART、DeBERTa

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import ByteLevel

tokenizer = Tokenizer(BPE(unk_token="<|endoftext|>"))
tokenizer.pre_tokenizer = ByteLevel()

trainer = BpeTrainer(
    vocab_size=50257,
    special_tokens=["<|endoftext|>"],
    min_frequency=2
)

tokenizer.train(files=["data.txt"], trainer=trainer)
```

**优势**：
- 能很好地处理词汇表外的单词（会将其拆分为子词）
- 词汇量大小可调
- 非常适合形态变化复杂的语言

**局限性**：
- 分词结果取决于合并顺序
- 可能会意外拆分常见单词

### WordPiece

**工作原理**：
1. 从字符级词汇表开始
2. 计算各合并对的得分：`频率(对) / (频率(第一个词) × 频率(第二个词))`
3. 合并得分最高的词对
4. 重复上述步骤，直至达到目标词汇量

**被以下模型采用**：BERT、DistilBERT、MobileBERT

```python
from tokenizers import Tokenizer
from tokenizers.models import WordPiece
from tokenizers.trainers import WordPieceTrainer
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.normalizers import BertNormalizer

tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))
tokenizer.normalizer = BertNormalizer(lowercase=True)
tokenizer.pre_tokenizer = Whitespace()

trainer = WordPieceTrainer(
    vocab_size=30522,
    special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],
    continuing_subword_prefix="##"
)

tokenizer.train(files=["corpus.txt"], trainer=trainer)
```

**优势**：  
- 优先处理具有实际意义的合并操作（得分越高，语义关联度越强）；  
- 已在 BERT 中得到成功应用，并取得了当前最先进的性能成果。  

**局限性**：  
- 若找不到子词匹配，未知词汇将显示为 `[UNK]`；  
- 该算法仅能压缩词汇表，无法优化合并规则，因此会导致文件体积增大。  

### 单词级模型（Unigram）  

**工作原理**：  
1. 从包含所有子串的庞大词汇表开始；  
2. 使用当前词汇表计算语料库的损失值；  
3. 删除对损失影响最小的词汇；  
4. 重复上述步骤，直至达到目标词汇表大小。  

**被以下模型采用**：ALBERT、T5、mBART、XLNet（通过 SentencePiece 实现）。

```python
from tokenizers import Tokenizer
from tokenizers.models import Unigram
from tokenizers.trainers import UnigramTrainer

tokenizer = Tokenizer(Unigram())

trainer = UnigramTrainer(
    vocab_size=8000,
    special_tokens=["<unk>", "<s>", "</s>"],
    unk_token="<unk>"
)

tokenizer.train(files=["data.txt"], trainer=trainer)
```

**优势**：
- 基于概率模型（可找到最可能的分词方式）
- 非常适用于没有词界分隔的语言
- 能够处理多种不同的语言场景

**缺点**：
- 训练过程计算成本较高
- 需要调整的超参数更多

## 分词流程

完整流程：**标准化 → 预处理分词 → 模型处理 → 后处理**

### 标准化

对文本进行清洗与规范化处理：

```python
from tokenizers.normalizers import NFD, StripAccents, Lowercase, Sequence

tokenizer.normalizer = Sequence([
    NFD(),           # Unicode normalization (decompose)
    Lowercase(),     # Convert to lowercase
    StripAccents()   # Remove accents
])

# Input: "Héllo WORLD"
# After normalization: "hello world"
```

**常用规范化处理函数**：
- `NFD`、`NFC`、`NFKD`、`NFKC` —— Unicode标准化形式
- `Lowercase()` —— 转换为小写
- `StripAccents()` —— 移除重音符号（如 é 转为 e）
- `Strip()` —— 删除空白字符
- `Replace(pattern, content)` —— 正则表达式替换

### 分词前处理

将文本拆分为类似单词的单元：

```python
from tokenizers.pre_tokenizers import Whitespace, Punctuation, Sequence, ByteLevel

# Split on whitespace and punctuation
tokenizer.pre_tokenizer = Sequence([
    Whitespace(),
    Punctuation()
])

# Input: "Hello, world!"
# After pre-tokenization: ["Hello", ",", "world", "!"]
```

**常用预分词器**：
- `Whitespace()` - 按空格、制表符和换行符进行分割
- `ByteLevel()` - 采用 GPT-2 风格的字节级分割
- `Punctuation()` - 分离标点符号
- `Digits(individual_digits=True)` - 分别拆分各个数字
- `Metaspace()` - 用 ▁ 替换空格（SentencePiece 风格）

### 后处理

为模型输入添加特殊标记：

```python
from tokenizers.processors import TemplateProcessing

# BERT-style: [CLS] sentence [SEP]
tokenizer.post_processor = TemplateProcessing(
    single="[CLS] $A [SEP]",
    pair="[CLS] $A [SEP] $B [SEP]",
    special_tokens=[
        ("[CLS]", 1),
        ("[SEP]", 2),
    ],
)
```

**常见模式**：
```python
# GPT-2: sentence <|endoftext|>
TemplateProcessing(
    single="$A <|endoftext|>",
    special_tokens=[("<|endoftext|>", 50256)]
)

# RoBERTa: <s> sentence </s>
TemplateProcessing(
    single="<s> $A </s>",
    pair="<s> $A </s> </s> $B </s>",
    special_tokens=[("<s>", 0), ("</s>", 2)]
)
```

## 对齐跟踪

追踪原始文本中的标记位置：

```python
output = tokenizer.encode("Hello, world!")

# Get token offsets
for token, offset in zip(output.tokens, output.offsets):
    start, end = offset
    print(f"{token:10} → [{start:2}, {end:2}): {text[start:end]!r}")

# Output:
# hello      → [ 0,  5): 'Hello'
# ,          → [ 5,  6): ','
# world      → [ 7, 12): 'world'
# !          → [12, 13): '!'
```

**应用场景**：
- 实体识别（将预测结果映射回原文）
- 问答系统（提取答案片段）
- 词元分类（将标签与原始位置对应）

## 与 Transformer 的集成

### 使用 AutoTokenizer 加载模型

```python
from transformers import AutoTokenizer

# AutoTokenizer automatically uses fast tokenizers
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Check if using fast tokenizer
print(tokenizer.is_fast)  # True

# Access underlying tokenizers.Tokenizer
fast_tokenizer = tokenizer.backend_tokenizer
print(type(fast_tokenizer))  # <class 'tokenizers.Tokenizer'>
```

### 将自定义分词器转换为 Transformers 格式

```python
from tokenizers import Tokenizer
from transformers import PreTrainedTokenizerFast

# Train custom tokenizer
tokenizer = Tokenizer(BPE())
# ... train tokenizer ...
tokenizer.save("my-tokenizer.json")

# Wrap for transformers
transformers_tokenizer = PreTrainedTokenizerFast(
    tokenizer_file="my-tokenizer.json",
    unk_token="[UNK]",
    pad_token="[PAD]",
    cls_token="[CLS]",
    sep_token="[SEP]",
    mask_token="[MASK]"
)

# Use like any transformers tokenizer
outputs = transformers_tokenizer(
    "Hello world",
    padding=True,
    truncation=True,
    max_length=512,
    return_tensors="pt"
)
```

## 常见模式

### 通过迭代器进行训练（适用于大型数据集）

```python
from datasets import load_dataset

# Load dataset
dataset = load_dataset("wikitext", "wikitext-103-raw-v1", split="train")

# Create batch iterator
def batch_iterator(batch_size=1000):
    for i in range(0, len(dataset), batch_size):
        yield dataset[i:i + batch_size]["text"]

# Train tokenizer
tokenizer.train_from_iterator(
    batch_iterator(),
    trainer=trainer,
    length=len(dataset)  # For progress bar
)
```

**性能表现**：处理1GB数据大约需要10至20分钟

### 启用截断与填充功能

```python
# Enable truncation
tokenizer.enable_truncation(max_length=512)

# Enable padding
tokenizer.enable_padding(
    pad_id=tokenizer.token_to_id("[PAD]"),
    pad_token="[PAD]",
    length=512  # Fixed length, or None for batch max
)

# Encode with both
output = tokenizer.encode("This is a long sentence that will be truncated...")
print(len(output.ids))  # 512
```

### 多进程处理

```python
from tokenizers import Tokenizer
from multiprocessing import Pool

# Load tokenizer
tokenizer = Tokenizer.from_file("tokenizer.json")

def encode_batch(texts):
    return tokenizer.encode_batch(texts)

# Process large corpus in parallel
with Pool(8) as pool:
    # Split corpus into chunks
    chunk_size = 1000
    chunks = [corpus[i:i+chunk_size] for i in range(0, len(corpus), chunk_size)]

    # Encode in parallel
    results = pool.map(encode_batch, chunks)
```

**加速效果**：配备8核处理器时，处理速度可提升5至8倍。

## 性能基准测试

### 训练速度

| 数据集规模 | BPE（3万词汇量） | WordPiece（3万词汇量） | Unigram（8千词汇量） |
|-------------|-----------------|---------------------|--------------------|
| 10 MB       | 15秒            | 18秒                | 25秒               |
| 100 MB      | 1.5分钟          | 2分钟               | 4分钟              |
| 1 GB        | 15分钟           | 20分钟              | 40分钟             |

**硬件配置**：16核CPU，基于英文维基百科进行测试

### 分词速度

| 实现方式       | 1 GB数据集   | 处理吞吐量     |
|----------------|-------------|----------------|
| 纯Python实现   | 约20分钟    | 约50 MB/分钟    |
| HF分词器库     | 约15秒      | 约4 GB/分钟     |
| **加速比**     | **80倍**    | **80倍**       |

**测试内容**：英文文本，平均句子长度为20个单词

### 内存占用

| 任务类型         | 内存占用 |
|------------------|----------|
| 加载分词器       | 约10 MB  |
| 训练BPE模型（3万词汇量） | 约200 MB |
| 编码100万条句子   | 约500 MB |

## 支持的模型

可通过`from_pretrained()`函数加载预训练分词器，支持的模型包括：

**BERT系列**：
- `bert-base-uncased`、`bert-large-cased`
- `distilbert-base-uncased`
- `roberta-base`、`roberta-large`

**GPT系列**：
- `gpt2`、`gpt2-medium`、`gpt2-large`
- `distilgpt2`

**T5系列**：
- `t5-small`、`t5-base`、`t5-large`
- `google/flan-t5-xxl`

**其他模型**：
- `facebook/bart-base`、`facebook/mbart-large-cc25`
- `albert-base-v2`、`albert-xlarge-v2`
- `xlm-roberta-base`、`xlm-roberta-large`
浏览全部模型：https://huggingface.co/models?library=tokenizers

## 参考资料

- **[训练指南](references/training.md)** - 自定义分词器的训练方法、训练器配置以及大规模数据集的处理技巧
- **[算法深度解析](references/algorithms.md)** - 详细讲解 BPE、WordPiece 和 Unigram 算法
- **[流水线组件](references/pipeline.md)** - 规范化工具、预分词器、后处理模块及解码器
- **[与 Transformers 的集成](references/integration.md)** - AutoTokenizer、PreTrainedTokenizerFast 以及特殊标记的使用方法

## 资源链接

- **文档**：https://huggingface.co/docs/tokenizers
- **GitHub 仓库**：https://github.com/huggingface/tokenizers ⭐ 9,000+ 次点赞
- **当前版本**：0.20.0+
- **课程**：https://huggingface.co/learn/nlp-course/chapter6/1
- **相关论文**：BPE（Sennrich 等人，2016年），WordPiece（Schuster 和 Nakajima，2012年）


