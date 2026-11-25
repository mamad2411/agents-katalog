---
name: huggingface-tokenizers
description: Tokenizadores rápidos otimizados para pesquisa e produção. Implementação em Rust que tokeniza 1GB em menos de 20 segundos. Suporta algoritmos BPE, WordPiece e Unigram. Treine vocabulários customizados, rastreie alinhamentos, gerencie padding/truncagem. Integração perfeita com transformers. Use quando precisar de tokenização de alto desempenho ou treinamento de tokenizadores customizados.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Tokenização, HuggingFace, BPE, WordPiece, Unigram, Tokenização Rápida, Rust, Tokenizador Customizado, Rastreamento de Alinhamento, Produção]
dependencies: [tokenizers, transformers, datasets]
---

# HuggingFace Tokenizers - Tokenização Rápida para NLP

Tokenizadores rápidos e prontos para produção com performance em Rust e facilidade de uso em Python.

## Quando usar HuggingFace Tokenizers

**Use HuggingFace Tokenizers quando:**
- Precisa de tokenização extremamente rápida (<20s por GB de texto)
- Treinar tokenizadores customizados do zero
- Quer rastreamento de alinhamento (token → posição no texto original)
- Construir pipelines NLP para produção
- Precisa tokenizar grandes corpora eficientemente

**Performance**:
- **Velocidade**: menos de 20 segundos para tokenizar 1GB em CPU
- **Implementação**: núcleo em Rust com bindings para Python/Node.js
- **Eficiência**: 10-100× mais rápido que implementações puras em Python

**Use alternativas em vez disso**:
- **SentencePiece**: independente de idioma, usado por T5/ALBERT
- **tiktoken**: tokenizador BPE da OpenAI para modelos GPT
- **transformers AutoTokenizer**: apenas carregamento de pré-treinados (usa esta biblioteca internamente)

## Início rápido

### Instalação

```bash
# Instalar tokenizers
pip install tokenizers

# Com integração transformers
pip install tokenizers transformers
```

### Carregar tokenizador pré-treinado

```python
from tokenizers import Tokenizer

# Carregar do HuggingFace Hub
tokenizer = Tokenizer.from_pretrained("bert-base-uncased")

# Codificar texto
output = tokenizer.encode("Hello, how are you?")
print(output.tokens)  # ['hello', ',', 'how', 'are', 'you', '?']
print(output.ids)     # [7592, 1010, 2129, 2024, 2017, 1029]

# Decodificar de volta
text = tokenizer.decode(output.ids)
print(text)  # "hello, how are you?"
```

### Treinar tokenizador BPE customizado

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

# Inicializar tokenizador com modelo BPE
tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()

# Configurar treinador
trainer = BpeTrainer(
    vocab_size=30000,
    special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],
    min_frequency=2
)

# Treinar em arquivos
files = ["train.txt", "validation.txt"]
tokenizer.train(files, trainer)

# Salvar
tokenizer.save("my-tokenizer.json")
```

**Tempo de treinamento**: ~1-2 minutos para corpus de 100MB, ~10-20 minutos para 1GB

### Codificação em lote com padding

```python
# Habilitar padding
tokenizer.enable_padding(pad_id=3, pad_token="[PAD]")

# Codificar lote
texts = ["Hello world", "This is a longer sentence"]
encodings = tokenizer.encode_batch(texts)

for encoding in encodings:
    print(encoding.ids)
# [101, 7592, 2088, 102, 3, 3, 3]
# [101, 2023, 2003, 1037, 2936, 6251, 102]
```

## Algoritmos de tokenização

### BPE (Codificação de Par de Bytes)

**Como funciona**:
1. Começar com vocabulário em nível de caractere
2. Encontrar o par de caracteres mais frequente
3. Mesclar em novo token, adicionar ao vocabulário
4. Repetir até atingir o tamanho do vocabulário

**Usado por**: GPT-2, GPT-3, RoBERTa, BART, DeBERTa

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

**Vantagens**:
- Lida bem com palavras OOV (quebra em subpalavras)
- Tamanho de vocabulário flexível
- Bom para idiomas morfologicamente ricos

**Desvantagens**:
- Tokenização depende da ordem de mesclagem
- Pode dividir palavras comuns inesperadamente

### WordPiece

**Como funciona**:
1. Começar com vocabulário em nível de caractere
2. Pontuar pares de mesclagem: `frequency(pair) / (frequency(first) × frequency(second))`
3. Mesclar par com maior pontuação
4. Repetir até atingir o tamanho do vocabulário

**Usado por**: BERT, DistilBERT, MobileBERT

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

**Vantagens**:
- Prioriza mesclagens significativas (alta pontuação = semanticamente relacionadas)
- Usado com sucesso em BERT (resultados state-of-the-art)

**Desvantagens**:
- Palavras desconhecidas se tornam `[UNK]` se não houver correspondência de subpalavra
- Salva vocabulário, não regras de mesclagem (arquivos maiores)

### Unigram

**Como funciona**:
1. Começar com vocabulário grande (todas as substrings)
2. Computar perda para corpus com vocabulário atual
3. Remover tokens com impacto mínimo na perda
4. Repetir até atingir o tamanho do vocabulário

**Usado por**: ALBERT, T5, mBART, XLNet (via SentencePiece)

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

**Vantagens**:
- Probabilístico (encontra tokenização mais provável)
- Funciona bem para idiomas sem limites de palavra
- Lida com contextos linguísticos diversos

**Desvantagens**:
- Computacionalmente caro para treinar
- Mais hiperparâmetros para ajustar

## Pipeline de tokenização

Pipeline completo: **Normalização → Pré-tokenização → Modelo → Pós-processamento**

### Normalização

Limpar e padronizar texto:

```python
from tokenizers.normalizers import NFD, StripAccents, Lowercase, Sequence

tokenizer.normalizer = Sequence([
    NFD(),           # Normalização Unicode (decomposição)
    Lowercase(),     # Converter para minúsculas
    StripAccents()   # Remover acentos
])

# Entrada: "Héllo WORLD"
# Após normalização: "hello world"
```

**Normalizadores comuns**:
- `NFD`, `NFC`, `NFKD`, `NFKC` - Formas de normalização Unicode
- `Lowercase()` - Converter para minúsculas
- `StripAccents()` - Remover acentos (é → e)
- `Strip()` - Remover espaços em branco
- `Replace(pattern, content)` - Substituição com regex

### Pré-tokenização

Dividir texto em unidades semelhantes a palavras:

```python
from tokenizers.pre_tokenizers import Whitespace, Punctuation, Sequence, ByteLevel

# Dividir em espaços em branco e pontuação
tokenizer.pre_tokenizer = Sequence([
    Whitespace(),
    Punctuation()
])

# Entrada: "Hello, world!"
# Após pré-tokenização: ["Hello", ",", "world", "!"]
```

**Pré-tokenizadores comuns**:
- `Whitespace()` - Dividir em espaços, abas, quebras de linha
- `ByteLevel()` - Divisão em nível de byte estilo GPT-2
- `Punctuation()` - Isolar pontuação
- `Digits(individual_digits=True)` - Dividir dígitos individualmente
- `Metaspace()` - Substituir espaços por ▁ (estilo SentencePiece)

### Pós-processamento

Adicionar tokens especiais para entrada do modelo:

```python
from tokenizers.processors import TemplateProcessing

# Estilo BERT: [CLS] sentence [SEP]
tokenizer.post_processor = TemplateProcessing(
    single="[CLS] $A [SEP]",
    pair="[CLS] $A [SEP] $B [SEP]",
    special_tokens=[
        ("[CLS]", 1),
        ("[SEP]", 2),
    ],
)
```

**Padrões comuns**:
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

## Rastreamento de alinhamento

Rastrear posições de tokens no texto original:

```python
output = tokenizer.encode("Hello, world!")

# Obter offsets de token
for token, offset in zip(output.tokens, output.offsets):
    start, end = offset
    print(f"{token:10} → [{start:2}, {end:2}): {text[start:end]!r}")

# Saída:
# hello      → [ 0,  5): 'Hello'
# ,          → [ 5,  6): ','
# world      → [ 7, 12): 'world'
# !          → [12, 13): '!'
```

**Casos de uso**:
- Reconhecimento de entidades nomeadas (mapear predições de volta para texto)
- Resposta a perguntas (extrair spans de resposta)
- Classificação de tokens (alinhar rótulos com posições originais)

## Integração com transformers

### Carregar com AutoTokenizer

```python
from transformers import AutoTokenizer

# AutoTokenizer usa automaticamente tokenizadores rápidos
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Verificar se está usando tokenizador rápido
print(tokenizer.is_fast)  # True

# Acessar tokenizers.Tokenizer subjacente
fast_tokenizer = tokenizer.backend_tokenizer
print(type(fast_tokenizer))  # <class 'tokenizers.Tokenizer'>
```

### Converter tokenizador customizado para transformers

```python
from tokenizers import Tokenizer
from transformers import PreTrainedTokenizerFast

# Treinar tokenizador customizado
tokenizer = Tokenizer(BPE())
# ... treinar tokenizador ...
tokenizer.save("my-tokenizer.json")

# Envolver para transformers
transformers_tokenizer = PreTrainedTokenizerFast(
    tokenizer_file="my-tokenizer.json",
    unk_token="[UNK]",
    pad_token="[PAD]",
    cls_token="[CLS]",
    sep_token="[SEP]",
    mask_token="[MASK]"
)

# Usar como qualquer tokenizador transformers
outputs = transformers_tokenizer(
    "Hello world",
    padding=True,
    truncation=True,
    max_length=512,
    return_tensors="pt"
)
```

## Padrões comuns

### Treinar a partir de iterador (conjuntos de dados grandes)

```python
from datasets import load_dataset

# Carregar conjunto de dados
dataset = load_dataset("wikitext", "wikitext-103-raw-v1", split="train")

# Criar iterador de lote
def batch_iterator(batch_size=1000):
    for i in range(0, len(dataset), batch_size):
        yield dataset[i:i + batch_size]["text"]

# Treinar tokenizador
tokenizer.train_from_iterator(
    batch_iterator(),
    trainer=trainer,
    length=len(dataset)  # Para barra de progresso
)
```

**Performance**: Processa 1GB em ~10-20 minutos

### Habilitar truncagem e padding

```python
# Habilitar truncagem
tokenizer.enable_truncation(max_length=512)

# Habilitar padding
tokenizer.enable_padding(
    pad_id=tokenizer.token_to_id("[PAD]"),
    pad_token="[PAD]",
    length=512  # Comprimento fixo, ou None para máximo do lote
)

# Codificar com ambos
output = tokenizer.encode("This is a long sentence that will be truncated...")
print(len(output.ids))  # 512
```

### Processamento multi-processamento

```python
from tokenizers import Tokenizer
from multiprocessing import Pool

# Carregar tokenizador
tokenizer = Tokenizer.from_file("tokenizer.json")

def encode_batch(texts):
    return tokenizer.encode_batch(texts)

# Processar corpus grande em paralelo
with Pool(8) as pool:
    # Dividir corpus em chunks
    chunk_size = 1000
    chunks = [corpus[i:i+chunk_size] for i in range(0, len(corpus), chunk_size)]

    # Codificar em paralelo
    results = pool.map(encode_batch, chunks)
```

**Aceleração**: 5-8× com 8 núcleos

## Benchmarks de performance

### Velocidade de treinamento

| Tamanho do Corpus | BPE (30k vocab) | WordPiece (30k) | Unigram (8k) |
|-------------------|-----------------|-----------------|--------------|
| 10 MB             | 15 seg          | 18 seg          | 25 seg       |
| 100 MB            | 1.5 min         | 2 min           | 4 min        |
| 1 GB              | 15 min          | 20 min          | 40 min       |

**Hardware**: 16 núcleos de CPU, testado em Wikipedia em inglês

### Velocidade de tokenização

| Implementação   | corpus de 1 GB | Throughput    |
|-----------------|----------------|---------------|
| Python Puro     | ~20 minutos    | ~50 MB/min    |
| HF Tokenizers   | ~15 segundos   | ~4 GB/min     |
| **Aceleração**  | **80×**        | **80×**       |

**Teste**: Texto em inglês, comprimento médio de frase 20 palavras

### Uso de memória

| Tarefa                      | Memória |
|-----------------------------|---------|
| Carregar tokenizador        | ~10 MB  |
| Treinar BPE (30k vocab)     | ~200 MB |
| Codificar 1M frases         | ~500 MB |

## Modelos suportados

Tokenizadores pré-treinados disponíveis via `from_pretrained()`:

**Família BERT**:
- `bert-base-uncased`, `bert-large-cased`
- `distilbert-base-uncased`
- `roberta-base`, `roberta-large`

**Família GPT**:
- `gpt2`, `gpt2-medium`, `gpt2-large`
- `distilgpt2`

**Família T5**:
- `t5-small`, `t5-base`, `t5-large`
- `google/flan-t5-xxl`

**Outros**:
- `facebook/bart-base`, `facebook/mbart-large-cc25`
- `albert-base-v2`, `albert-xlarge-v2`
- `xlm-roberta-base`, `xlm-roberta-large`

Navegue por todos: https://huggingface.co/models?library=tokenizers

## Referências

- **[Guia de Treinamento](references/training.md)** - Treinar tokenizadores customizados, configurar treinadores, lidar com conjuntos de dados grandes
- **[Mergulho Profundo em Algoritmos](references/algorithms.md)** - BPE, WordPiece, Unigram explicados em detalhe
- **[Componentes de Pipeline](references/pipeline.md)** - Normalizadores, pré-tokenizadores, pós-processadores, decodificadores
- **[Integração com Transformers](references/integration.md)** - AutoTokenizer, PreTrainedTokenizerFast, tokens especiais

## Recursos

- **Docs**: https://huggingface.co/docs/tokenizers
- **GitHub**: https://github.com/huggingface/tokenizers ⭐ 9.000+
- **Versão**: 0.20.0+
- **Curso**: https://huggingface.co/learn/nlp-course/chapter6/1
- **Paper**: BPE (Sennrich et al., 2016), WordPiece (Schuster & Nakajima, 2012)