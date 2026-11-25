---
name: sentencepiece
description: Tokenizador agnóstico de linguagem que trata texto como Unicode bruto. Suporta algoritmos BPE e Unigram. Rápido (50k sentenças/seg), leve (6MB de memória), vocabulário determinístico. Usado por T5, ALBERT, XLNet, mBART. Treina em texto bruto sem pré-tokenização. Use quando você precisar de suporte multilíngue, linguagens CJK ou tokenização reproduzível.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Tokenization, SentencePiece, Language-Independent, BPE, Unigram, Multilingual, CJK Languages, Unicode, Deterministic, Google]
dependencies: [sentencepiece, transformers]
---

# SentencePiece - Tokenização Agnóstica de Linguagem

Tokenizador não supervisionado que funciona em texto bruto sem pré-processamento específico de linguagem.

## Quando usar SentencePiece

**Use SentencePiece quando:**
- Construir modelos multilíngues (sem regras específicas de linguagem)
- Trabalhar com linguagens CJK (Chinês, Japonês, Coreano)
- Precisar de tokenização reproduzível (vocabulário determinístico)
- Quiser treinar em texto bruto (sem pré-tokenização necessária)
- Exigir deployment leve (6MB de memória, 50k sentenças/seg)

**Performance**:
- **Velocidade**: 50.000 sentenças/seg
- **Memória**: ~6MB para modelo carregado
- **Linguagens**: Todas (agnóstico de linguagem)

**Use alternativas em vez disso**:
- **HuggingFace Tokenizers**: Treinamento mais rápido, mais flexibilidade
- **tiktoken**: Modelos OpenAI (GPT-3.5/4)
- **BERT WordPiece**: Tarefas centradas em inglês

## Início rápido

### Instalação

```bash
# Python
pip install sentencepiece

# C++ (requer CMake)
git clone https://github.com/google/sentencepiece.git
cd sentencepiece
mkdir build && cd build
cmake .. && make -j $(nproc)
sudo make install
```

### Treinar modelo

```bash
# Command-line (BPE com vocab de 8000)
spm_train --input=data.txt --model_prefix=m --vocab_size=8000 --model_type=bpe

# Python API
import sentencepiece as spm

spm.SentencePieceTrainer.train(
    input='data.txt',
    model_prefix='m',
    vocab_size=8000,
    model_type='bpe'
)
```

**Tempo de treinamento**: ~1-2 minutos para corpus de 100MB

### Codificar e decodificar

```python
import sentencepiece as spm

# Carregar modelo
sp = spm.SentencePieceProcessor(model_file='m.model')

# Codificar para pieces
pieces = sp.encode('This is a test', out_type=str)
print(pieces)  # ['▁This', '▁is', '▁a', '▁test']

# Codificar para IDs
ids = sp.encode('This is a test', out_type=int)
print(ids)  # [284, 47, 11, 1243]

# Decodificar
text = sp.decode(ids)
print(text)  # "This is a test"
```

## Design agnóstico de linguagem

### Espaço em branco como símbolo (▁)

```python
text = "Hello world"
pieces = sp.encode(text, out_type=str)
print(pieces)  # ['▁Hello', '▁world']

# Decodificar preserva espaços
decoded = sp.decode_pieces(pieces)
print(decoded)  # "Hello world"
```

**Princípio-chave**: Tratar texto como Unicode bruto, espaço em branco = ▁ (símbolo meta)

## Algoritmos de tokenização

### BPE (Byte-Pair Encoding)

```python
spm.SentencePieceTrainer.train(
    input='data.txt',
    model_prefix='bpe_model',
    vocab_size=16000,
    model_type='bpe'
)
```

**Usado por**: mBART

### Unigram (padrão)

```python
spm.SentencePieceTrainer.train(
    input='data.txt',
    model_prefix='unigram_model',
    vocab_size=8000,
    model_type='unigram'
)
```

**Usado por**: T5, ALBERT, XLNet

## Configuração de treinamento

### Parâmetros essenciais

```python
spm.SentencePieceTrainer.train(
    input='corpus.txt',
    model_prefix='m',
    vocab_size=32000,
    model_type='unigram',
    character_coverage=0.9995,  # 1.0 para CJK
    user_defined_symbols=['[SEP]', '[CLS]'],
    unk_piece='<unk>',
    num_threads=16
)
```

### Cobertura de caracteres

| Tipo de Linguagem | Cobertura | Justificativa |
|-------------------|-----------|---------------|
| Inglês            | 0.9995    | Caracteres mais comuns |
| CJK (Chinês)      | 1.0       | Todos os caracteres necessários |
| Multilíngue       | 0.9995    | Equilíbrio |

## Opções de codificação

### Regularização de subword

```python
# Amostrar diferentes tokenizações
for _ in range(3):
    pieces = sp.encode('tokenization', out_type=str, enable_sampling=True, alpha=0.1)
    print(pieces)

# Output (diferente a cada vez):
# ['▁token', 'ization']
# ['▁tok', 'en', 'ization']
```

**Caso de uso**: Aumento de dados para robustez.

## Padrões comuns

### Treinamento no estilo T5

```python
spm.SentencePieceTrainer.train(
    input='c4_corpus.txt',
    model_prefix='t5',
    vocab_size=32000,
    model_type='unigram',
    user_defined_symbols=[f'<extra_id_{i}>' for i in range(100)],
    unk_id=2,
    eos_id=1,
    pad_id=0
)
```

### Integração com transformers

```python
from transformers import T5Tokenizer

# T5 usa SentencePiece internamente
tokenizer = T5Tokenizer.from_pretrained('t5-base')
inputs = tokenizer('translate English to French: Hello', return_tensors='pt')
```

## Benchmarks de performance

### Velocidade de treinamento

| Corpus | BPE (16k)  | Unigram (8k) |
|--------|------------|--------------|
| 100 MB | 1-2 min    | 3-4 min      |
| 1 GB   | 10-15 min  | 30-40 min    |

### Velocidade de tokenização

- **SentencePiece**: 50.000 sentenças/seg
- **HF Tokenizers**: 200.000 sentenças/seg (4× mais rápido)

## Modelos suportados

**Família T5**: `t5-base`, `t5-large` (vocab de 32k, Unigram)
**ALBERT**: `albert-base-v2` (vocab de 30k, Unigram)
**XLNet**: `xlnet-base-cased` (vocab de 32k, Unigram)
**mBART**: `facebook/mbart-large-50` (vocab de 250k, BPE)

## Referências

- **[Guia de Treinamento](references/training.md)** - Opções detalhadas, preparação de corpus
- **[Algoritmos](references/algorithms.md)** - BPE vs Unigram, regularização de subword

## Recursos

- **GitHub**: https://github.com/google/sentencepiece ⭐ 10.000+
- **Paper**: https://arxiv.org/abs/1808.06226 (EMNLP 2018)
- **Versão**: 0.2.0+